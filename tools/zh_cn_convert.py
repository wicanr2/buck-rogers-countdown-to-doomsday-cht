#!/usr/bin/env python3
"""規格 041：由正式繁中譯文產生簡體（zh-CN）檔。

只在 buck-zhcn-opencc:1.4.2（tools/docker/opencc/）內、--network none 執行：

  python3 tools/zh_cn_convert.py                    # 產生（寫 text/*.zh-CN.tsv 等）
  python3 tools/zh_cn_convert.py --check            # 重新產生並比對、驗證詞表／覆寫表／帳本
  python3 tools/zh_cn_convert.py --review-dir workplace/zh-cn-review   # 另輸出審閱清單（不進版控）

流程：OpenCC 官方 tw2sp（include_tofu_risk_dictionaries=True），在第一段用語群組最前面插入專案詞表
text/zh-CN-phrases.tsv；以「標記字典追蹤」取得原樣 tw2sp 與專案設定兩種設定下的逐處匹配（位置、長度、
詞條、來源字典），並先驗證追蹤輸出與正式設定逐列相同。自檢、遮蔽偵測、字數核算、帳本都以追蹤結果為準。

輸入：text/*.zh-TW.tsv（排除 translit-chars、host-ui、manual-english-panel）、name-glossary.tsv、
name-glossary-exclude.tsv、translit-chars.zh-TW.tsv。
輸出：text/<family>.zh-CN.tsv、name-glossary.zh-CN.tsv、name-glossary-exclude.zh-CN.tsv、
translit-zh-CN-map.tsv。手工不得編輯產生檔；修正只經詞表或覆寫表（text/zh-CN-overrides.tsv）。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

LANG = "zh-CN"
EXCLUDED_FAMILIES = ("translit-chars", "host-ui", "manual-english-panel")
MANUAL_FAMILIES = frozenset({"manual"})  # 帳本 note 留空；錯誤訊息不印內容
CATALOG_HEADER = ["key", "translation", "source"]
PHRASE_HEADER = ["tw", "cn", "kind", "reason"]
OVERRIDE_HEADER = ["family", "key", "zh_tw_sha256", "translation", "reason"]
LEDGER_HEADER = ["family", "key", "zh_tw_sha256", "occurrence", "term_id", "verdict", "note"]
GLOSSARY_HEADER = ["english", "english_mixed", "chinese", "kind", "person", "basis", "note"]
EXCLUDE_HEADER = ["phrase", "scope", "note"]
MAP_HEADER = ["tw", "cn"]
KINDS = ("keep", "map", "guard", "char")  # char：OpenCC 之後逐字套用（修訂 2026-09-30）
VERDICTS = ("ok", "override")
PROJECT_DICT = "zh-CN-phrases"
PHRASES_REV = "TWPhrasesRev"
HALFWIDTH = frozenset(range(0x20, 0x7F)) | {0x2022}  # 規格 039（同 tools/halfwidth.py）
STAGE1_MARK = 0xF0000
STAGE2_MARK = 0x100000


class ConvertError(ValueError):
    pass


# ---------------------------------------------------------------- 基本工具

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_han(ch: str) -> bool:
    n = unicodedata.name(ch, "")
    return n.startswith("CJK UNIFIED IDEOGRAPH") or n.startswith("CJK COMPATIBILITY IDEOGRAPH")


def han_count(text: str) -> int:
    return sum(1 for ch in text if is_han(ch))


def skeleton(text: str) -> str:
    return "".join(ch for ch in text if not is_han(ch))


def half_units(text: str) -> int:
    return sum(1 if ord(ch) in HALFWIDTH else 2 for ch in text)


def is_private(ch: str) -> bool:
    return unicodedata.category(ch) == "Co"


def read_tsv(path: Path, header: list[str], allow_missing: bool = False) -> list[list[str]]:
    if not path.exists():
        if allow_missing:
            return []
        raise ConvertError(f"{path.name}: 不存在")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        raise ConvertError(f"{path.name}: 不允許 BOM 或 CR")
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8")), delimiter="\t", quoting=csv.QUOTE_NONE, strict=True))
    if not rows or rows[0] != header:
        raise ConvertError(f"{path.name}: 標頭必須精確為 {'/'.join(header)}")
    for n, r in enumerate(rows[1:], start=2):
        if len(r) != len(header):
            raise ConvertError(f"{path.name}:{n}: 必須恰有 {len(header)} 欄")
    return rows[1:]


def tsv_bytes(header: list[str], rows: list[list[str]]) -> bytes:
    for r in rows:
        for v in r:
            if "\t" in v or "\n" in v or "\r" in v:
                raise ConvertError(f"欄位含 tab 或換行：{r[0]}")
    return ("\t".join(header) + "\n" + "".join("\t".join(r) + "\n" for r in rows)).encode("utf-8")


def row_invariant_errors(where: str, tw: str, cn: str) -> list[str]:
    out = []
    if unicodedata.normalize("NFC", cn) != cn:
        out.append(f"{where}: 非 NFC")
    if any(unicodedata.category(ch).startswith("C") for ch in cn):
        out.append(f"{where}: 含控制、格式或私用區字元")
    if skeleton(tw) != skeleton(cn):
        out.append(f"{where}: 去掉漢字後的字元序列與 zh-TW 不同")
    for a, b in (("(", ")"), ("（", "）")):
        if tw.count(a) != cn.count(a) or tw.count(b) != cn.count(b):
            out.append(f"{where}: 括號數改變")
    return out


def occurrences(text: str, word: str) -> list[int]:
    out, i = [], text.find(word)
    while i >= 0:
        out.append(i)
        i = text.find(word, i + 1)
    return out


# ---------------------------------------------------------------- 資料模型

@dataclass(frozen=True)
class Phrase:
    row: int  # 詞表資料列號（1 起算，不含標頭）
    tw: str
    cn: str
    kind: str
    reason: str

    @property
    def term_id(self) -> str:
        return f"{PROJECT_DICT}:{self.row}"


@dataclass(frozen=True)
class Override:
    family: str
    key: str
    sha: str
    translation: str
    reason: str


@dataclass(frozen=True)
class Match:
    start: int
    end: int
    dict: str
    idx: int
    key: str
    value: str
    ostart: int
    oend: int

    @property
    def term_id(self) -> str:
        return f"{self.dict}:{self.idx}"


@dataclass
class Track:
    """一個設定下一列的兩段追蹤：輸入位置 → 第一段輸出位置 → 最終輸出位置。"""
    s1: list[Match]
    out1: str
    map1: dict[int, int]
    s2: list[Match]
    out2: str
    map2: dict[int, int]

    def align(self, a: int) -> int | None:
        m = self.map1.get(a)
        return None if m is None else self.map2.get(m)


@dataclass
class Row:
    family: str
    key: str
    tw: str
    source: str
    raw: Track | None = None
    proj: Track | None = None
    cn: str = ""  # 產生結果（覆寫前）
    final: str = ""  # 覆寫後
    override: Override | None = None

    @property
    def where(self) -> str:
        return f"{self.family}:{self.key}"


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    ledger_errors: list[str] = field(default_factory=list)
    outputs: dict[str, bytes] = field(default_factory=dict)  # repo 相對路徑 → 位元組
    review: list[dict] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


# ---------------------------------------------------------------- OpenCC 引擎

def opencc_share() -> Path:
    import opencc  # noqa: PLC0415  只在 image 內可用
    return Path(opencc.__file__).parent / "clib" / "share" / "opencc"


def opencc_dict_bin() -> Path:
    import opencc  # noqa: PLC0415
    return Path(opencc.__file__).parent / "clib" / "bin" / "opencc_dict"


def verify_official(share: Path, sha_list: Path) -> None:
    for line in sha_list.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        want, name = line.split()
        got = hashlib.sha256((share / name).read_bytes()).hexdigest()
        if got != want:
            raise ConvertError(f"官方字典 {name} SHA-256 不符：{got}")


class Engine:
    def __init__(self, phrases: list[Phrase], tmp: Path, share: Path | None = None):
        import opencc  # noqa: PLC0415
        self._opencc = opencc
        self.share = share or opencc_share()
        self.tmp = tmp
        self.phrases = phrases
        self.base = json.loads((self.share / "tw2sp.json").read_text(encoding="utf-8"))
        chain = self.base["conversion_chain"]
        if len(chain) != 2 or any(c["dict"].get("match_policy", "short_circuit") != "short_circuit" for c in chain):
            raise ConvertError("tw2sp.json 結構與規格 041 假設不符")
        self.stage_dicts = [[d for d in c["dict"]["dicts"]] for c in chain]
        self.entries: dict[str, list[tuple[str, str, str]]] = {}
        for d in self.stage_dicts[0] + self.stage_dicts[1] + [self.base["normalization"][0]["dict"]]:
            name = d["file"][: -len(".ocd2")]
            if name in self.entries:
                continue
            txt = tmp / f"{name}.txt"
            subprocess.run([str(opencc_dict_bin()), "-i", str(self.share / d["file"]), "-o", str(txt),
                            "-f", "ocd2", "-t", "text"], check=True, capture_output=True)
            ents = []
            for line in txt.read_text(encoding="utf-8").splitlines():
                k, v = line.split("\t")
                ents.append((k, v.split(" ")[0], v))
            self.entries[name] = ents
        self.normalization_keys = {k for k, _, _ in self.entries["CJK_Compatibility_Ideographs"]}
        self._cc: dict[tuple, object] = {}
        self._markers: dict[tuple, dict[str, tuple[str, int, str, str]]] = {}

    # 設定檔 ------------------------------------------------------------------

    def _ocd2(self, d: dict) -> dict:
        out = dict(d)
        out["file"] = str(self.share / d["file"])
        return out

    def _project_file(self, rows: tuple[Phrase, ...], values: str, tag: str) -> str:
        path = self.tmp / f"project-{tag}.txt"
        lines = sorted((p.tw, p.cn) for p in rows)
        path.write_text("".join(f"{k}\t{v}\n" for k, v in lines), encoding="utf-8")
        return str(path)

    def config(self, project: tuple[Phrase, ...] | None, s1: str, s2: str | None) -> tuple[object, dict]:
        """s1／s2：official（ocd2）、text（匯出 text、真值）、marker（標記）；s2=None 只保留第一段。"""
        ck = (tuple(p.row for p in project) if project is not None else None, s1, s2)
        if ck in self._cc:
            return self._cc[ck], self._markers[ck]
        tag = f"{len(self._cc)}"
        markers: dict[str, tuple[str, int, str, str]] = {}
        cfg = json.loads(json.dumps(self.base))
        cfg["name"] = f"buckrogers zh-CN {tag}"
        cfg["normalization"][0]["dict"] = self._ocd2(cfg["normalization"][0]["dict"])
        cfg["segmentation"]["dict"] = self._ocd2(cfg["segmentation"]["dict"])
        next_mark = [STAGE1_MARK, STAGE2_MARK]

        def build(stage: int, mode: str, with_project: bool) -> list[dict]:
            out = []
            srcs: list[tuple[str, list[tuple[str, str, str]], dict | None]] = []
            if with_project and project is not None:
                srcs.append((PROJECT_DICT, [(p.tw, p.cn, p.cn) for p in project], None))
            for d in self.stage_dicts[stage]:
                name = d["file"][: -len(".ocd2")]
                srcs.append((name, self.entries[name], d))
            for name, ents, d in srcs:
                if mode == "official" and d is not None:
                    out.append(self._ocd2(d))
                    continue
                path = self.tmp / f"{tag}-{stage}-{name}.txt"
                lines = []
                for i, (k, v0, vraw) in enumerate(ents, start=1):
                    if mode == "marker":
                        mk = chr(next_mark[stage])
                        next_mark[stage] += 1
                        idx = project[i - 1].row if name == PROJECT_DICT else i
                        markers[mk] = (name, idx, k, v0)
                        lines.append((k, mk))
                    else:
                        lines.append((k, vraw))
                lines.sort(key=lambda kv: kv[0].encode("utf-8"))
                path.write_text("".join(f"{k}\t{v}\n" for k, v in lines), encoding="utf-8")
                nd = {"type": "text", "file": str(path)}
                if d is not None and d.get("may_output_tofu"):
                    nd["may_output_tofu"] = True
                out.append(nd)
            return out

        cfg["conversion_chain"][0]["dict"]["dicts"] = build(0, s1, True)
        if s2 is None:
            cfg["conversion_chain"] = cfg["conversion_chain"][:1]
        else:
            cfg["conversion_chain"][1]["dict"]["dicts"] = build(1, s2, False)
        path = self.tmp / f"config-{tag}.json"
        path.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
        cc = self._opencc.OpenCC(str(path), include_tofu_risk_dictionaries=True)
        self._cc[ck] = cc
        self._markers[ck] = markers
        return cc, markers

    def stage2_only(self) -> object:
        ck = ("stage2-only",)
        if ck not in self._cc:
            cfg = json.loads(json.dumps(self.base))
            cfg["normalization"][0]["dict"] = self._ocd2(cfg["normalization"][0]["dict"])
            cfg["segmentation"]["dict"] = self._ocd2(cfg["segmentation"]["dict"])
            cfg["conversion_chain"] = cfg["conversion_chain"][1:]
            cfg["conversion_chain"][0]["dict"]["dicts"] = [self._ocd2(d) for d in cfg["conversion_chain"][0]["dict"]["dicts"]]
            path = self.tmp / "config-stage2.json"
            path.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
            self._cc[ck] = self._opencc.OpenCC(str(path), include_tofu_risk_dictionaries=True)
        return self._cc[ck]

    def formal(self, project: tuple[Phrase, ...] | None) -> object:
        return self.config(project, "official", "official")[0]

    # 追蹤 --------------------------------------------------------------------

    @staticmethod
    def walk(inp: str, marked: str, markers: dict) -> tuple[list[Match], str, dict[int, int]]:
        i = 0
        out: list[str] = []
        olen = 0
        matches: list[Match] = []
        pos = {0: 0}
        for ch in marked:
            m = markers.get(ch)
            if m is not None:
                name, idx, key, value = m
                if inp[i:i + len(key)] != key:
                    raise ConvertError(f"追蹤位置不符（{name}:{idx}）")
                matches.append(Match(i, i + len(key), name, idx, key, value, olen, olen + len(value)))
                out.append(value)
                i += len(key)
                olen += len(value)
            else:
                if i >= len(inp) or inp[i] != ch:
                    raise ConvertError("追蹤的直通字元與輸入不符")
                out.append(ch)
                i += 1
                olen += 1
            pos[i] = olen
        if i != len(inp):
            raise ConvertError("追蹤未消耗全部輸入")
        return matches, "".join(out), pos

    def track(self, text: str, project: tuple[Phrase, ...] | None) -> Track:
        cc1, mk1 = self.config(project, "marker", None)
        s1, out1, map1 = self.walk(text, cc1.convert(text), mk1)
        cc2, mk2 = self.config(project, "official", "marker")
        s2, out2, map2 = self.walk(out1, cc2.convert(text), mk2)
        return Track(s1, out1, map1, s2, out2, map2)


# ---------------------------------------------------------------- 讀入

def read_phrases(path: Path) -> tuple[list[Phrase], list[str]]:
    errors = []
    phrases = []
    seen: set[str] = set()
    for n, (tw, cn, kind, reason) in enumerate(read_tsv(path, PHRASE_HEADER), start=1):
        where = f"{path.name} 第 {n} 列"
        if not tw or not cn or any(c.isspace() for c in tw + cn):
            errors.append(f"{where}: tw／cn 不得為空或含空白、tab")
            continue
        if tw in seen:
            errors.append(f"{where}: 重複 tw「{tw}」")
            continue
        if kind not in KINDS:
            errors.append(f"{where}: kind 必須是 keep、map、guard 或 char")
            continue
        if kind == "char" and (len(tw) != 1 or len(cn) != 1 or not is_han(tw) or not is_han(cn) or tw == cn):
            errors.append(f"{where}: char 詞條的 tw、cn 必須各是單一且不同的漢字（改變字數者用 map）")
            continue
        if not reason.strip():
            errors.append(f"{where}: reason 不得為空")
        if kind == "keep" and len(tw) != len(cn):
            errors.append(f"{where}: keep 詞條不得改變字數")
        seen.add(tw)
        phrases.append(Phrase(n, tw, cn, kind, reason))
    return phrases, errors


def read_overrides(path: Path) -> tuple[list[Override], list[str]]:
    errors = []
    out = []
    seen = set()
    for n, (family, key, sha, translation, reason) in enumerate(read_tsv(path, OVERRIDE_HEADER, allow_missing=True), start=1):
        if (family, key) in seen:
            errors.append(f"{path.name} 第 {n} 列: 重複 {family}:{key}")
        seen.add((family, key))
        if not reason.strip() or not translation:
            errors.append(f"{path.name} 第 {n} 列: translation、reason 不得為空")
        out.append(Override(family, key, sha, translation, reason))
    return out, errors


def family_files(text_dir: Path) -> list[tuple[str, Path]]:
    out = []
    for p in sorted(text_dir.glob("*.zh-TW.tsv")):
        fam = p.name[: -len(".zh-TW.tsv")]
        if fam not in EXCLUDED_FAMILIES:
            out.append((fam, p))
    return out


# ---------------------------------------------------------------- 主流程

def run(root: Path, review: bool = False, tmp: Path | None = None) -> Result:
    res = Result()
    text = root / "text"
    phrases, perr = read_phrases(text / "zh-CN-phrases.tsv")
    res.errors += perr
    overrides, oerr = read_overrides(text / "zh-CN-overrides.tsv")
    res.errors += oerr
    chars = [p for p in phrases if p.kind == "char"]
    char_map = {p.tw: p for p in chars}
    phrases = [p for p in phrases if p.kind != "char"]  # 送進 OpenCC 的詞表
    ptuple = tuple(phrases)
    by_row = {p.row: p for p in phrases + chars}

    def apply_chars(text: str) -> str:
        """§3.2 char：OpenCC 轉換後逐字套用。"""
        return "".join(char_map[c].cn if c in char_map else c for c in text)

    with tempfile.TemporaryDirectory(dir=tmp) as td:
        eng = Engine(phrases, Path(td))
        sha_list = root / "tools" / "docker" / "opencc" / "opencc-dicts.sha256"
        if sha_list.exists():
            verify_official(eng.share, sha_list)
        else:
            res.errors.append("缺 tools/docker/opencc/opencc-dicts.sha256")

        # 讀全部列、追蹤兩種設定
        rows: list[Row] = []
        fams: dict[str, list[Row]] = {}
        for fam, path in family_files(text):
            fams[fam] = []
            for key, tw, source in read_tsv(path, CATALOG_HEADER):
                r = Row(fam, key, tw, source)
                rows.append(r)
                fams[fam].append(r)
        formal_raw = eng.formal(None)
        formal_proj = eng.formal(ptuple)
        text_proj = eng.config(ptuple, "text", "text")[0]
        text_raw = eng.config(None, "text", "text")[0]
        for r in rows:
            if any(is_private(c) for c in r.tw):
                res.errors.append(f"{r.where}: zh-TW 含私用區字元，無法追蹤")
                continue
            if any(c in eng.normalization_keys for c in r.tw):
                res.errors.append(f"{r.where}: zh-TW 含相容表意字（正規化會改變位置）")
                continue
            r.raw = eng.track(r.tw, None)
            r.proj = eng.track(r.tw, ptuple)
            opencc_out = formal_proj.convert(r.tw)
            r.cn = apply_chars(opencc_out)
            if r.raw.out2 != formal_raw.convert(r.tw) or r.proj.out2 != opencc_out:
                res.errors.append(f"{r.where}: 追蹤設定輸出與正式設定不同")
            if text_proj.convert(r.tw) != opencc_out or text_raw.convert(r.tw) != r.raw.out2:
                res.errors.append(f"{r.where}: 匯出 text 字典設定輸出與官方 ocd2 不同")
        rows = [r for r in rows if r.proj is not None]

        # §3.2 自檢
        stage2 = eng.stage2_only()
        matched_rows: dict[int, int] = {p.row: 0 for p in phrases}
        for r in rows:
            for m in r.proj.s1:
                if m.dict == PROJECT_DICT:
                    matched_rows[m.idx] += 1
        for p in phrases:
            if formal_proj.convert(p.tw) != p.cn:
                res.errors.append(f"詞表第 {p.row} 列「{p.tw}」單獨轉換不等於 cn")
            if stage2.convert(p.cn) != p.cn:
                res.errors.append(f"詞表第 {p.row} 列「{p.tw}」的 cn 經第二段不恆等")
            if matched_rows[p.row] == 0:
                res.errors.append(f"詞表第 {p.row} 列「{p.tw}」在正式譯文沒有實際匹配")
        # char 自檢：單獨轉換（OpenCC＋逐字）等於 cn、至少命中一次、cn 在字元清單中。
        char_hits: dict[int, int] = {p.row: 0 for p in chars}
        for r in rows:
            for c in r.proj.out2:
                if c in char_map:
                    char_hits[char_map[c].row] += 1
        font_list = root / "font" / f"characters.{LANG}.txt"
        font_chars = ({line.split("\t", 1)[1] for line in font_list.read_text(encoding="utf-8").splitlines() if "\t" in line}
                      if font_list.exists() else set())
        for p in chars:
            if apply_chars(formal_proj.convert(p.tw)) != p.cn:
                res.errors.append(f"詞表第 {p.row} 列 char「{p.tw}」單獨轉換不等於 cn")
            if char_hits[p.row] == 0:
                res.errors.append(f"詞表第 {p.row} 列 char「{p.tw}」在 OpenCC 輸出沒有命中")
            if p.cn not in font_chars:
                res.ledger_errors.append(f"詞表第 {p.row} 列 char 的 cn「{p.cn}」不在 {font_list.name}（重生字元清單後再檢查）")
        for r in rows:
            pm = [m for m in r.proj.s1 if m.dict == PROJECT_DICT]
            for p in phrases:
                for a in occurrences(r.tw, p.tw):
                    b = a + len(p.tw)
                    ok = any(m.start == a and m.idx == p.row for m in pm) or any(
                        by_row[m.idx].kind in ("guard", "map") and m.start <= a and b <= m.end and m.end - m.start > len(p.tw)
                        for m in pm)
                    if not ok:
                        res.errors.append(f"{r.where}: 詞表第 {p.row} 列「{p.tw}」在位置 {a} 未匹配也未被較長 guard／map 覆蓋")

        # §3.2 遮蔽偵測
        overridden = {(o.family, o.key) for o in overrides}
        without_cache: dict[int, object] = {}

        def same_without(r: Row, prow: int) -> bool:
            if prow not in without_cache:
                without_cache[prow] = eng.formal(tuple(p for p in phrases if p.row != prow))
            return without_cache[prow].convert(r.tw) == r.cn

        for r in rows:
            if (r.family, r.key) in overridden:
                continue
            raw_off = [m for m in r.raw.s1]
            for m in r.proj.s1:
                if m.dict != PROJECT_DICT or by_row[m.idx].kind == "guard":
                    continue
                cats = []
                if any(o.start == m.start and o.end > m.end for o in raw_off):
                    cats.append(1)
                if any(m.start < o.start < m.end for o in raw_off):
                    cats.append(2)
                if any(o.start < m.start < o.end for o in raw_off):
                    cats.append(3)
                if cats and not same_without(r, m.idx):
                    res.errors.append(f"{r.where}: 詞表第 {m.idx} 列「{m.key}」在位置 {m.start} 遮蔽官方匹配（類 {','.join(map(str, cats))}），需 guard 或覆寫")
            for p in phrases:
                if p.kind == "guard":
                    continue
                for a in occurrences(r.tw, p.tw):
                    if any(o.dict != PROJECT_DICT and o.start < a < o.end for o in r.proj.s1) and not same_without(r, p.row):
                        res.errors.append(f"{r.where}: 官方匹配覆蓋詞表第 {p.row} 列「{p.tw}」起點 {a}（類 3），需 guard 或覆寫")

        # §3.4 不變量與字數核算（產生結果）
        counted = lambda m: m.dict == PHRASES_REV or (m.dict == PROJECT_DICT and by_row[m.idx].kind in ("map", "guard"))  # noqa: E731
        for r in rows:
            res.errors += row_invariant_errors(r.where, r.tw, r.cn)
            want = sum(len(m.value) - len(m.key) for m in r.proj.s1 if counted(m))
            if han_count(r.cn) - han_count(r.tw) != want:
                res.errors.append(f"{r.where}: 漢字數改變 {han_count(r.cn) - han_count(r.tw)} 不等於套用詞條長度差 {want}")

        # §3.3 覆寫
        index = {(r.family, r.key): r for r in rows}
        for r in rows:
            r.final = r.cn
        for o in overrides:
            r = index.get((o.family, o.key))
            if r is None:
                res.errors.append(f"覆寫 {o.family}:{o.key}: 孤兒（key 不存在）")
                continue
            if sha256_text(r.tw) != o.sha:
                res.errors.append(f"覆寫 {o.family}:{o.key}: zh-TW 雜湊不符")
                continue
            errs = row_invariant_errors(f"覆寫 {o.family}:{o.key}", r.tw, o.translation)
            if errs:
                res.errors += errs
                continue
            r.final = o.translation
            r.override = o

        # §3.6 名字
        grows = read_tsv(text / "name-glossary.tsv", GLOSSARY_HEADER)
        gout = []
        name_map: list[tuple[str, str]] = []
        for g in grows:
            cn = apply_chars(formal_proj.convert(g[2]))
            gout.append([g[0], g[1], cn, g[3], g[4], g[5], g[6]])
            name_map.append((g[2], cn))
        seen_cn: dict[str, str] = {}
        for tw, cn in name_map:
            if cn in seen_cn and seen_cn[cn] != tw:
                res.errors.append(f"名字表 chinese 轉換後重複：「{seen_cn[cn]}」「{tw}」→「{cn}」")
            seen_cn[cn] = tw
        erows = read_tsv(text / "name-glossary-exclude.tsv", EXCLUDE_HEADER, allow_missing=True)
        eout = []
        phrase_map: list[tuple[str, str]] = []
        for e in erows:
            cn = apply_chars(formal_proj.convert(e[0]))
            eout.append([cn, e[1], e[2]])
            phrase_map.append((e[0], cn))
        for label, pairs in (("名字", name_map), ("例外片語", phrase_map)):
            for tw_name, cn_name in pairs:
                for r in rows:
                    occ = occurrences(r.tw, tw_name)
                    if not occ:
                        continue
                    if r.override is not None:
                        if r.final.count(cn_name) != len(occ):
                            res.errors.append(f"{r.where}: {label}「{tw_name}」在覆寫譯文中寫法不一致")
                        continue
                    for a in occ:
                        s, e = r.proj.align(a), r.proj.align(a + len(tw_name))
                        if s is None or e is None or r.final[s:e] != cn_name:
                            res.errors.append(f"{r.where}: {label}「{tw_name}」位置 {a} 轉換後與「{cn_name}」不一致")

        # 音譯對照
        trows = read_tsv(text / "translit-chars.zh-TW.tsv", CATALOG_HEADER)
        tmap = []
        seen_t: dict[str, str] = {}
        for _key, ch, _src in trows:
            cn = apply_chars(formal_proj.convert(ch))
            if len(ch) != 1 or len(cn) != 1:
                res.errors.append(f"音譯對照「{ch}」→「{cn}」不是單一字元")
                continue
            if cn in seen_t:
                res.errors.append(f"音譯對照碰撞：「{seen_t[cn]}」「{ch}」→「{cn}」")
            seen_t[cn] = ch
            tmap.append([ch, cn])

        # §3.7 跨家族一致性：整列只含漢字（可含 •）的詞，在其他家族對齊的出現處轉換結果須相同。
        terms: dict[str, tuple[str, Row]] = {}
        for r in rows:
            t = r.tw
            if 2 <= len(t) <= 12 and all(is_han(c) or c == "•" for c in t):
                prev = terms.get(t)
                if prev is not None and prev[0] != r.final:
                    res.errors.append(f"跨家族不一致：整列「{t}」在 {prev[1].where} 與 {r.where} 轉換結果不同")
                terms.setdefault(t, (r.final, r))
        for t, (cn_t, owner) in sorted(terms.items()):
            for r in rows:
                if r.family == owner.family or t not in r.tw or r.override is not None or r.tw == t:
                    continue
                for a in occurrences(r.tw, t):
                    s, e = r.proj.align(a), r.proj.align(a + len(t))
                    if s is None or e is None:
                        continue  # 此處不是同一個詞（詞條跨越邊界）
                    if r.final[s:e] != cn_t:
                        res.errors.append(f"跨家族不一致：「{t}」在 {owner.where} 為「{cn_t}」，在 {r.where} 位置 {a} 不同")

        # §3.5 帳本
        expected = []
        for r in rows:
            n = 0
            for m in r.proj.s1:
                if counted(m):
                    n += 1
                    expected.append((r, n, m))
            # char 套用處接在後面（依 OpenCC 輸出位置），位置為最終輸出座標。
            for i, c in enumerate(r.proj.out2):
                if c in char_map:
                    n += 1
                    p = char_map[c]
                    expected.append((r, n, Match(i, i + 1, PROJECT_DICT, p.row, p.tw, p.cn, i, i + 1)))
        ledger_path = text / "zh-CN-term-review.tsv"
        ledger = {}
        try:
            lrows = read_tsv(ledger_path, LEDGER_HEADER)
        except ConvertError as exc:
            lrows = []
            res.ledger_errors.append(str(exc))
        for fam, key, sha, occ, term, verdict, note in lrows:
            k = (fam, key, occ)
            if k in ledger:
                res.ledger_errors.append(f"帳本重複 {fam}:{key}#{occ}")
            ledger[k] = (sha, term, verdict, note)
            if verdict not in VERDICTS:
                res.ledger_errors.append(f"帳本 {fam}:{key}#{occ}: verdict 必須是 ok 或 override")
            if verdict == "override" and (fam, key) not in overridden:
                res.ledger_errors.append(f"帳本 {fam}:{key}#{occ}: verdict=override 但覆寫表沒有該列")
            if fam in MANUAL_FAMILIES and note:
                res.ledger_errors.append(f"帳本 {fam}:{key}#{occ}: 手冊家族 note 必須留空")
        want_keys = set()
        for r, n, m in expected:
            k = (r.family, r.key, str(n))
            want_keys.add(k)
            got = ledger.get(k)
            if got is None:
                res.ledger_errors.append(f"帳本缺項或新套用處：{r.family}:{r.key}#{n} {m.term_id}")
            elif got[0] != sha256_text(r.tw):
                res.ledger_errors.append(f"帳本 {r.family}:{r.key}#{n}: zh-TW 雜湊不符")
            elif got[1] != m.term_id:
                res.ledger_errors.append(f"帳本 {r.family}:{r.key}#{n}: 詞條不符（{got[1]} → {m.term_id}）")
        for k in sorted(set(ledger) - want_keys):
            res.ledger_errors.append(f"帳本多出不存在的套用處：{k[0]}:{k[1]}#{k[2]}")

        if review:
            for r, n, m in expected:
                if by_row.get(m.idx) is not None and m.dict == PROJECT_DICT and by_row[m.idx].kind == "char":
                    inv = {}
                    for a in range(len(r.tw) + 1):
                        o = r.proj.align(a)
                        if o is not None:
                            inv.setdefault(o, a)
                    a = inv.get(m.ostart, 0)
                    res.review.append({
                        "family": r.family, "key": r.key, "zh_tw_sha256": sha256_text(r.tw), "occurrence": n,
                        "term_id": m.term_id, "tw": m.key, "cn": m.value, "raw_same": 0,
                        "tw_context": r.tw[max(0, a - 12):a + 13], "cn_context": r.final[max(0, m.ostart - 12):m.ostart + 13],
                        "verdict": (ledger.get((r.family, r.key, str(n))) or ("", "", "", ""))[2],
                        "note": (ledger.get((r.family, r.key, str(n))) or ("", "", "", ""))[3],
                    })
                    continue
                s = r.proj.map2.get(m.ostart)
                e = r.proj.map2.get(m.oend)
                cn_term = r.cn[s:e] if s is not None and e is not None else "?"
                a0 = max(0, m.start - 12)
                b0 = min(len(r.tw), m.end + 12)
                ca, cb = r.proj.align(a0), r.proj.align(b0)
                cn_ctx = r.final[ca:cb] if ca is not None and cb is not None else r.final
                got = ledger.get((r.family, r.key, str(n)))
                res.review.append({
                    "family": r.family, "key": r.key, "zh_tw_sha256": sha256_text(r.tw), "occurrence": n,
                    "term_id": m.term_id, "tw": m.key, "cn": cn_term,
                    "raw_same": int(any(o.start == m.start and o.key == m.key for o in r.raw.s1)),
                    "tw_context": r.tw[a0:b0], "cn_context": cn_ctx,
                    "verdict": got[2] if got else "", "note": got[3] if got else "",
                })

        # 輸出
        for fam, frows in fams.items():
            res.outputs[f"text/{fam}.{LANG}.tsv"] = tsv_bytes(CATALOG_HEADER, [[r.key, r.final, r.source] for r in frows if r.proj is not None])
        res.outputs[f"text/name-glossary.{LANG}.tsv"] = tsv_bytes(GLOSSARY_HEADER, gout)
        res.outputs[f"text/name-glossary-exclude.{LANG}.tsv"] = tsv_bytes(EXCLUDE_HEADER, eout)
        res.outputs[f"text/translit-{LANG}-map.tsv"] = tsv_bytes(MAP_HEADER, tmap)

        # 統計（不含譯文）
        width = [(r.where, half_units(r.final) - half_units(r.tw)) for r in rows if half_units(r.final) != half_units(r.tw)]
        res.stats = {
            "rows": len(rows), "families": len(fams), "phrases": len(phrases), "overrides": len(overrides),
            "changed_rows": sum(1 for r in rows if r.final != r.tw),
            "raw_diff_rows": sum(1 for r in rows if r.final != r.raw.out2),
            "ledger_expected": len(expected),
            "ledger_by_dict": {d: sum(1 for _, _, m in expected if m.dict == d) for d in (PHRASES_REV, PROJECT_DICT)},
            "phrase_matches": {p.row: matched_rows[p.row] for p in phrases},
            "char_hits": {p.row: char_hits[p.row] for p in chars},
            "width_changed": width,
            "wider": [w for w in width if w[1] > 0],
        }
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--check", action="store_true", help="重新產生並比對，不寫檔")
    ap.add_argument("--review-dir", type=Path, help="輸出審閱清單（workplace，不進版控）")
    ap.add_argument("--stats-out", type=Path, help="輸出統計 JSON（不含譯文）")
    a = ap.parse_args(argv)
    try:
        res = run(a.root, review=a.review_dir is not None)
    except ConvertError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 1
    for e in res.errors:
        print(f"錯誤：{e}", file=sys.stderr)
    if a.review_dir is not None:
        a.review_dir.mkdir(parents=True, exist_ok=True)
        cols = ["family", "key", "zh_tw_sha256", "occurrence", "term_id", "tw", "cn", "raw_same",
                "tw_context", "cn_context", "verdict", "note"]
        body = "\t".join(cols) + "\n" + "".join(
            "\t".join(str(x[c]).replace("\t", " ") for c in cols) + "\n" for x in res.review)
        (a.review_dir / "review.tsv").write_text(body, encoding="utf-8")
    if a.stats_out is not None:
        a.stats_out.write_text(json.dumps(res.stats, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if a.check:
        bad = list(res.errors) + list(res.ledger_errors)
        for e in res.ledger_errors:
            print(f"錯誤：{e}", file=sys.stderr)
        for rel, data in sorted(res.outputs.items()):
            p = a.root / rel
            if not p.exists() or p.read_bytes() != data:
                bad.append(rel)
                print(f"錯誤：產生檔與重新產生結果不同：{rel}", file=sys.stderr)
        expected = set(res.outputs)
        for p in sorted((a.root / "text").glob(f"*.{LANG}.tsv")):
            rel = f"text/{p.name}"
            if rel not in expected:
                bad.append(rel)
                print(f"錯誤：多出的產生檔（不在產生範圍）：{rel}", file=sys.stderr)
        if bad:
            print(f"zh_cn_convert --check：{len(bad)} 項失敗", file=sys.stderr)
            return 1
        print(f"zh_cn_convert --check OK（{res.stats['rows']} 列、{len(res.outputs)} 檔、帳本 {res.stats['ledger_expected']} 處）")
        return 0
    if res.errors:
        print(f"zh_cn_convert：{len(res.errors)} 項錯誤，未寫檔", file=sys.stderr)
        return 1
    for rel, data in sorted(res.outputs.items()):
        p = a.root / rel
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
    for e in res.ledger_errors:
        print(f"警告（帳本）：{e}", file=sys.stderr)
    print(f"zh_cn_convert：寫出 {len(res.outputs)} 檔（{res.stats['rows']} 列）；帳本問題 {len(res.ledger_errors)} 項")
    return 0


if __name__ == "__main__":
    sys.exit(main())
