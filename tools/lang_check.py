#!/usr/bin/env python3
"""規格 042 §3.3、043 §3.3：日文（ja）與韓文（ko）譯文檢查。不含英文原文；以 text/*.zh-TW.tsv 與事件檔、安全矩形檔為基準，逐列驗證。
共用邏輯依語言設定（LangConfig）取值；tools/ja_check.py 與 tools/ko_check.py 是薄包裝。

  python3 tools/lang_check.py --lang ko                    檢查 text/*.ko.tsv
  python3 tools/lang_check.py --lang ko --expect-rows 5453 --expect-keys 5445   加覆蓋斷言

錯誤讓結束碼非零；警告（ECL 寬度超過 zh-TW 1.6 倍等）只列出。單位：半形 1、其餘 2（規格 039）。
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
BASE = "zh-TW"
CATALOG_HEADER = ["key", "translation", "source"]
MANUAL_FAMILY = "manual"  # 規格 051：手冊段落由 tools/manual_lang.py 檢查（逐字元換列、拉丁字母白名單、字集）
NON_CATALOG_PREFIX = ("name-glossary", "translit-chars")

# 規格 042 §3.3 第 5 項。
STORY_CAP = {**{f"story-page{i}": 78 for i in range(2, 8)}, "story-opening": 78, "story-page8": 76, "story-page9": 40}
ECL_CAP = 456
ECL_RATIO_WARN = 1.6
LOGBOOK_TITLE_CAP = 76
FIXED_LINE_FAMILIES = ("hmenu", "story-opening", *(f"story-page{i}" for i in range(2, 10)))


@dataclass(frozen=True)
class LangConfig:
    """語言設定：規格 042（ja）、043（ko）。"""
    code: str
    spec: str                       # 訊息用，如「規格 042」
    no_files: frozenset[str]        # 不產生該語言檔的家族
    forbidden_ranges: tuple[tuple[int, int], ...]
    forbidden_chars: frozenset[str]
    new_line_start: frozenset[str]  # 定行家族不得以其開頭
    opening: frozenset[str]         # 定行家族不得以其結尾
    word_spacing: bool = False      # 韓文：空白規則（第 12 至 14 項）


_NO_FILES = frozenset({"translit-chars", "host-ui", "manual-english-panel"})
# 規格 042 §3.2 禁用字元；§3.4 新增的列首禁則字元與開括號。
JA = LangConfig(
    "ja", "規格 042", _NO_FILES,
    ((0xFF61, 0xFF9F), (0xFF10, 0xFF19), (0xFF21, 0xFF3A), (0xFF41, 0xFF5A)),
    frozenset({"　", "～", "－", '"'}),
    frozenset("ぁぃぅぇぉっゃゅょゎゕゖァィゥェォッャュョヮヵヶーゝゞヽヾ々〻・】〕］｝〉〙〗’”．"),
    frozenset("「『（【〔［｛〈《‘“"),
)
# 規格 043 §3.2：韓文用半形 ASCII 標點；禁用全形英數與相容字母、Hanja、`~`、`·`、ASCII 雙引號；無列首禁則集合。
KO = LangConfig(
    "ko", "規格 043", _NO_FILES,
    ((0xFF10, 0xFF19), (0xFF21, 0xFF3A), (0xFF41, 0xFF5A), (0x3130, 0x318F), (0x4E00, 0x9FFF)),
    frozenset({"　", "~", "·", '"'}),
    frozenset(),
    frozenset(),
    True,
)
CONFIGS: dict[str, LangConfig] = {"ja": JA, "ko": KO}

# 規格 043 §3.3 第 13 項：拉丁字母詞後緊接韓文時，整段連續韓文必須是下列助詞串之一（完整比對）。
KO_LATIN_SUFFIXES = frozenset(
    "의 이 가 은 는 을 를 과 와 로 으로 에 에서 에게 에게는 에게서 에는 에서의 까지 들 들이 들은 들을 들에게 입니다 이며 이다 이라면 이라는 이라고 이에요 형".split())

PLACEHOLDER_RE = re.compile(r"\{\d+\}")
HOTKEY_RE = re.compile(r"\(([A-Za-z0-9])\)")
LATIN_RE = re.compile(r"[A-Za-z][A-Za-z0-9'.\-]*")


def units(s: str) -> int:
    return sum(1 if (0x20 <= ord(c) <= 0x7E or c == "•") else 2 for c in s)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"錯誤 {where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"警告 {where}: {msg}")


def read_catalog_raw(path: Path, report: Report) -> list[list[str]] | None:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        report.err(path.name, "不允許 UTF-8 BOM")
    if b"\r" in data:
        report.err(path.name, "含 CR（CRLF）")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        report.err(path.name, f"不是有效的 UTF-8：{exc}")
        return None
    text = text.lstrip("﻿")
    rows = list(csv.reader(io.StringIO(text), delimiter="\t", quoting=csv.QUOTE_NONE))
    if not rows or rows[0] != CATALOG_HEADER:
        report.err(path.name, f"標頭必須精確為 {'/'.join(CATALOG_HEADER)}")
        return None
    return rows[1:]


def read_tsv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
    if not rows:
        return []
    return [dict(zip(rows[0], r)) for r in rows[1:] if r and any(r)]


def families(text_dir: Path, lang: str) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in sorted(text_dir.glob(f"*.{lang}.tsv")):
        if p.name.startswith(NON_CATALOG_PREFIX):
            continue
        out[p.name[: -len(f".{lang}.tsv")]] = p
    return out


# ------------------------------------------------------------ 寬度上限（規格 042 §3.3 第 5 項）

def load_cap_sources(text_dir: Path) -> dict[str, object]:
    """事件檔與安全矩形；缺檔時對應家族不做寬度檢查（合成測試用）。"""
    simple: dict[str, int] = {}
    for fn in ("hmenu-item-events.tsv", "engine-fragment-events.tsv", "item-word-events.tsv", "monster-name-events.tsv"):
        p = text_dir / fn
        if p.exists():
            for r in read_tsv_dicts(p):
                simple[r["event_key"]] = int(r["original_length"])
    ident: dict[str, set[int]] = defaultdict(set)
    rect: dict[str, int] = {}
    text_events: dict[str, set[str]] = defaultdict(set)
    for p in sorted(text_dir.glob("*.tsv")):
        if re.search(r"\.(zh-TW|zh-CN|ja|ko|en|zz)\.tsv$", p.name) or p.name.startswith("name-glossary"):
            continue
        try:
            rows = read_tsv_dicts(p)
        except (OSError, csv.Error, UnicodeDecodeError):
            continue
        if p.name.endswith("-text-safe-rects.tsv"):
            for r in rows:
                if r.get("event_key") and r.get("capacity_cells"):
                    rect[r["event_key"]] = int(r["capacity_cells"])
            continue
        if p.name.endswith("-events.tsv"):
            for r in rows:
                tk = r.get("text_key") or r.get("translation_key")
                if r.get("event_key") and tk:
                    text_events[tk].add(r["event_key"])
        if rows and "original_sha256" in rows[0]:
            for r in rows:
                for col in ("event_key", "text_key", "translation_key", "key"):
                    if r.get(col) and r.get("original_length", "").isdigit():
                        ident[r[col]].add(int(r["original_length"]))
    bar = text_dir / "skill-action-bar-events.tsv"
    if bar.exists():
        for r in read_tsv_dicts(bar):
            for v in ("normal", "focus"):
                text_events[r["key"]].add(f"{r['screen']}.{r['key']}.{v}")
    return {"simple": simple, "ident": ident, "rect": rect, "text_events": text_events}


def cap_for(family: str, key: str, zh: str, src: dict[str, object]) -> int | None:
    simple: dict[str, int] = src["simple"]  # type: ignore[assignment]
    ident: dict[str, set[int]] = src["ident"]  # type: ignore[assignment]
    rect: dict[str, int] = src["rect"]  # type: ignore[assignment]
    text_events: dict[str, set[str]] = src["text_events"]  # type: ignore[assignment]
    if family == "coordinate-line":
        return 2
    if family in ("ecl-text", "logbook", "logbook-panel", "engine-template"):
        return None
    if family in STORY_CAP:
        return STORY_CAP[family]
    if family in ("hmenu", "engine-fragment", "item-word", "monster-name"):
        n = simple.get(key)
        if n is None:
            return None
        return max(2 * n, units(zh)) if family == "hmenu" else 2 * n
    caps = [rect[e] for e in text_events.get(key, ()) if e in rect]
    if key in rect:
        caps.append(rect[key])
    if caps:
        return 2 * min(caps)
    lens = ident.get(key)
    if lens:
        return 2 * min(lens)
    return None


# ------------------------------------------------------------ 檢查本體

def check(text_dir: Path, font_dir: Path, report: Report, *, expect_rows: int | None = None,
          expect_keys: int | None = None, lang: str = "ja") -> None:
    cfg = CONFIGS[lang]
    zh_fams = families(text_dir, BASE)
    ja_fams = families(text_dir, lang)
    charset = None
    if (font_dir / f"charset.{lang}.txt").exists():
        charset = set((font_dir / f"charset.{lang}.txt").read_text(encoding="utf-8").rstrip("\n"))
    characters = None
    if (font_dir / f"characters.{lang}.txt").exists():
        characters = set()
        for line in (font_dir / f"characters.{lang}.txt").read_text(encoding="utf-8").splitlines():
            if "\t" in line and line.startswith("U+"):
                characters.add(chr(int(line.split("\t", 1)[0][2:], 16)))
    exemptions: set[str] = set()
    ex_path = text_dir / f"{lang}-coverage-exemptions.tsv"
    if ex_path.exists():
        exemptions = {r["key"] for r in read_tsv_dicts(ex_path)}
    cap_src = load_cap_sources(text_dir)
    seen_used_exemptions: set[str] = set()
    shared: dict[str, dict[str, str]] = defaultdict(dict)  # key -> {檔: 譯文}
    total_rows = 0
    total_keys: set[str] = set()

    # 家族存在性
    for fam in zh_fams:
        if fam in cfg.no_files:
            continue
        if fam not in ja_fams:
            report.err(f"{fam}.{lang}.tsv", f"缺檔（{cfg.spec} §3.1）")
    for fam in ja_fams:
        if fam not in zh_fams:
            report.err(f"{fam}.{lang}.tsv", "沒有對應的 zh-TW 檔")

    # 標題展開樣板（logbook-panel）
    panel_title = None
    if "logbook-panel" in ja_fams:
        rows = read_catalog_raw(ja_fams["logbook-panel"], Report()) or []
        for r in rows:
            if len(r) == 3 and r[0] == "logbook.panel.title":
                panel_title = r[1]

    for fam, ja_path in ja_fams.items():
        if fam not in zh_fams:
            continue
        ja_rows = read_catalog_raw(ja_path, report)
        zh_rows = read_catalog_raw(zh_fams[fam], Report())
        if ja_rows is None or zh_rows is None:
            continue
        name = ja_path.name
        if fam == MANUAL_FAMILY:
            import manual_lang
            for n, r in enumerate(ja_rows, start=2):
                if len(r) != 3:
                    report.err(f"{name}:{n}", "必須恰有 3 欄")
                    continue
                total_rows += 1
                total_keys.add(r[0])
                shared[r[0]][name] = r[1]
            try:
                for e in manual_lang.check_catalog(lang, ja_path, zh_fams[fam], charset):
                    report.err(name, e)
            except ValueError as exc:
                report.err(name, str(exc))
            continue
        zh_map = {r[0]: r for r in zh_rows if len(r) == 3}
        ja_keys: list[str] = []
        seen: set[str] = set()
        for n, r in enumerate(ja_rows, start=2):
            where = f"{name}:{n}"
            if len(r) != 3:
                report.err(where, "必須恰有 3 欄")
                continue
            key, text, source = r
            ja_keys.append(key)
            total_rows += 1
            total_keys.add(key)
            shared[key][name] = text
            if key in seen:
                report.err(where, f"重複 key：{key}")
            seen.add(key)
            zh = zh_map.get(key)
            if zh is None:
                report.err(where, f"key 不在 zh-TW 同家族：{key}")
                continue
            check_row(fam, key, text, source, zh[1], zh[2], where, report, charset, characters, cap_src, panel_title, cfg)
        # 順序與覆蓋
        zh_order = [k for k in zh_map if k in seen or k in exemptions]
        ja_order = [k for k in ja_keys if k in zh_map]
        if ja_order != [k for k in zh_map if k in seen]:
            report.err(name, "key 順序與 zh-TW 不同")
        for k in zh_map:
            if k not in seen:
                if k in exemptions:
                    seen_used_exemptions.add(k)
                else:
                    report.err(name, f"缺列（zh-TW 有）：{k}")
        del zh_order
    for k in exemptions - seen_used_exemptions:
        report.err(f"{lang}-coverage-exemptions.tsv", f"豁免 {k} 未被使用（多餘）")
    # 跨檔共用 key
    for key, per_file in shared.items():
        if len(set(per_file.values())) > 1:
            report.err(",".join(sorted(per_file)), f"共用 key 譯文不一致：{key}")
    # 覆蓋斷言
    if expect_rows is not None and total_rows != expect_rows:
        report.err("覆蓋", f"列數 {total_rows} ≠ 預期 {expect_rows}")
    if expect_keys is not None and len(total_keys) != expect_keys:
        report.err("覆蓋", f"不同 key 數 {len(total_keys)} ≠ 預期 {expect_keys}")


_LATIN_HANGUL_RE = re.compile(r"([A-Za-z][A-Za-z0-9'\-]*)( ?)([가-힣]+)")


def ko_word_checks(ko: str, zh: str, where: str, report: Report) -> None:
    """規格 043 §3.3 第 12 與 13 項（第 14 項的禁用字元由 LangConfig 處理，第 15 項在 name_glossary.py）。"""
    runs = lambda t: len(re.findall(r" {2,}", t))  # noqa: E731
    if runs(ko) > runs(zh):
        report.err(where, f"連續空白段數 {runs(ko)} 多於 zh-TW {runs(zh)}")
    body = PLACEHOLDER_RE.sub("\x00", ko.replace("\\n", "\x00"))  # `\n` 與佔位符不是拉丁字母詞
    for m in _LATIN_HANGUL_RE.finditer(body):
        word, space, run = m.groups()
        if not space and run not in KO_LATIN_SUFFIXES:
            report.err(where, f"拉丁字母詞「{word}」後直接接「{run}」：不是助詞串，需加一個半形空白")
        elif space and run in KO_LATIN_SUFFIXES:
            report.err(where, f"拉丁字母詞「{word}」後多了空白才接助詞串「{run}」")


def quote_diff(s: str) -> int:
    return sum(s.count(c) for c in "「『") - sum(s.count(c) for c in "」』")


def check_row(fam: str, key: str, ja: str, source: str, zh: str, zh_source: str, where: str, report: Report,
              charset: set[str] | None, characters: set[str] | None, cap_src: dict[str, object],
              panel_title: str | None, cfg: LangConfig = JA) -> None:
    if source != zh_source:
        report.err(where, f"source 與 zh-TW 不同：{source!r} ≠ {zh_source!r}")
    if not ja:
        report.err(where, "translation 為空")
        return
    if unicodedata.normalize("NFC", ja) != ja:
        report.err(where, "translation 必須使用 NFC")
    if any(unicodedata.category(c).startswith("C") for c in ja):
        report.err(where, "translation 含控制或格式字元")
    if "\t" in ja or "\n" in ja:
        report.err(where, "translation 含 tab 或換行")
    for c in ja:
        cp = ord(c)
        if c in cfg.forbidden_chars or any(lo <= cp <= hi for lo, hi in cfg.forbidden_ranges):
            report.err(where, f"禁用字元 U+{cp:04X}")
        elif charset is not None and c not in charset:
            report.err(where, f"字集外字元 U+{cp:04X}「{c}」")
        elif characters is not None and c not in characters and 0x21 <= cp:
            report.err(where, f"不在 characters.{cfg.code}.txt：U+{cp:04X}「{c}」")
    if Counter(PLACEHOLDER_RE.findall(ja)) != Counter(PLACEHOLDER_RE.findall(zh)):
        report.err(where, f"佔位符與 zh-TW 不同：{PLACEHOLDER_RE.findall(ja)} ≠ {PLACEHOLDER_RE.findall(zh)}")
    if ja.count("\\n") != zh.count("\\n"):
        report.err(where, f"\\n 數量 {ja.count(chr(92) + 'n')} ≠ zh-TW {zh.count(chr(92) + 'n')}")
    if HOTKEY_RE.findall(ja) != HOTKEY_RE.findall(zh):
        report.err(where, f"熱鍵序列 {HOTKEY_RE.findall(ja)} ≠ zh-TW {HOTKEY_RE.findall(zh)}")
    if fam == "hmenu":
        def caps_digits(s: str) -> Counter:
            return Counter(c for c in s if c.isascii() and (c.isupper() or c.isdigit()))
        if caps_digits(ja) != caps_digits(zh):
            report.err(where, "水平選單的大寫 ASCII 與數字集合與 zh-TW 不同")
    strip = lambda s: PLACEHOLDER_RE.sub(" ", s.replace("\\n", " "))  # noqa: E731
    ja_latin, zh_latin = set(LATIN_RE.findall(strip(ja))), set(LATIN_RE.findall(strip(zh)))
    if not ja_latin <= zh_latin:
        report.err(where, f"多出拉丁字母詞：{sorted(ja_latin - zh_latin)}")
    if quote_diff(ja) != quote_diff(zh):
        report.err(where, f"引號開閉差 {quote_diff(ja)} ≠ zh-TW {quote_diff(zh)}")
    # 寬度
    cap = cap_for(fam, key, zh, cap_src)
    if fam == "coordinate-line":
        if len(ja) != 1:
            report.err(where, "方位必須恰一字")
    elif cap is not None and units(ja) > cap:
        report.err(where, f"寬度 {units(ja)} 超過上限 {cap}")
    if fam == "ecl-text":
        if units(ja) > ECL_CAP:
            report.err(where, f"ECL 寬度 {units(ja)} 超過 {ECL_CAP}")
        elif units(zh) and units(ja) > ECL_RATIO_WARN * units(zh) and units(ja) > 20:
            report.warn(where, f"ECL 寬度為 zh-TW {units(ja) / units(zh):.1f} 倍")
    if fam == "logbook" and key.endswith(".title") and panel_title is not None:
        expanded = panel_title.replace("{0}", "99").replace("{1}", ja)
        if units(expanded) > LOGBOOK_TITLE_CAP:
            report.err(where, f"手札標題展開後 {units(expanded)} 超過 {LOGBOOK_TITLE_CAP}")
    # 定行家族首尾字元
    if fam in FIXED_LINE_FAMILIES:
        if ja[0] in cfg.new_line_start:
            report.err(where, f"定行家族不得以列首禁則字元「{ja[0]}」開頭")
        if ja[-1] in cfg.opening:
            report.err(where, f"定行家族不得以開括號「{ja[-1]}」結尾")
        if cfg.word_spacing and (ja[0] == " " or ja[-1] == " "):
            report.err(where, "定行家族不得以半形空白開頭或結尾")
    # 欄名列（單空白 token）在 header_columns.py 檢查；這裡只擋連續空白於 dispatcher 欄名列
    if not cfg.word_spacing and "  " in ja and "  " not in zh and fam == "engine-fragment":
        report.warn(where, "含連續空白（若是欄名列會使 anchorColumns 失敗；header_columns.py 判定）")
    if cfg.word_spacing:
        ko_word_checks(ja, zh, where, report)


def main(argv: list[str] | None = None, default_lang: str = "ja") -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--lang", default=default_lang, choices=sorted(CONFIGS))
    p.add_argument("--text", type=Path, default=ROOT / "text")
    p.add_argument("--font", type=Path, default=ROOT / "font")
    p.add_argument("--expect-rows", type=int)
    p.add_argument("--expect-keys", type=int)
    args = p.parse_args(argv)
    report = Report()
    check(args.text, args.font, report, expect_rows=args.expect_rows, expect_keys=args.expect_keys, lang=args.lang)
    for w in report.warnings:
        print(w)
    for e in report.errors:
        print(e)
    print(f"{args.lang}_check：錯誤 {len(report.errors)}，警告 {len(report.warnings)}")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
