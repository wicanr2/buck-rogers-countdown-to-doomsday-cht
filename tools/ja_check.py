#!/usr/bin/env python3
"""規格 042 §3.3：日文（ja）譯文檢查。不含英文原文；以 text/*.zh-TW.tsv 與事件檔、安全矩形檔為基準，逐列驗證。

  python3 tools/ja_check.py                       檢查 text/*.ja.tsv
  python3 tools/ja_check.py --expect-rows 5414 --expect-keys 5406   加覆蓋斷言（規格 042 §3.1）

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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
LANG = "ja"
BASE = "zh-TW"
CATALOG_HEADER = ["key", "translation", "source"]

# 不產生 ja 檔的家族（規格 042 §3.1）與只要求存在的家族。
NO_JA_FAMILIES = {"translit-chars", "host-ui", "manual-english-panel"}
HEADER_ONLY_FAMILIES = {"manual"}
NON_CATALOG_PREFIX = ("name-glossary",)

# 規格 042 §3.3 第 5 項。
STORY_CAP = {**{f"story-page{i}": 78 for i in range(2, 8)}, "story-opening": 78, "story-page8": 76, "story-page9": 40}
ECL_CAP = 456
ECL_RATIO_WARN = 1.6
LOGBOOK_TITLE_CAP = 76
FIXED_LINE_FAMILIES = ("hmenu", "story-opening", *(f"story-page{i}" for i in range(2, 10)))

# 規格 042 §3.2 禁用字元；§3.4 新增的列首禁則字元與開括號。
FORBIDDEN_RANGES = [(0xFF61, 0xFF9F), (0xFF10, 0xFF19), (0xFF21, 0xFF3A), (0xFF41, 0xFF5A)]
FORBIDDEN_CHARS = {"　", "～", "－", '"'}
NEW_LINE_START = set("ぁぃぅぇぉっゃゅょゎゕゖァィゥェォッャュョヮヵヶーゝゞヽヾ々〻・】〕］｝〉〙〗’”．")
OPENING = set("「『（【〔［｛〈《‘“")

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
          expect_keys: int | None = None) -> None:
    zh_fams = families(text_dir, BASE)
    ja_fams = families(text_dir, LANG)
    charset = None
    if (font_dir / "charset.ja.txt").exists():
        charset = set((font_dir / "charset.ja.txt").read_text(encoding="utf-8").rstrip("\n"))
    characters = None
    if (font_dir / "characters.ja.txt").exists():
        characters = set()
        for line in (font_dir / "characters.ja.txt").read_text(encoding="utf-8").splitlines():
            if "\t" in line and line.startswith("U+"):
                characters.add(chr(int(line.split("\t", 1)[0][2:], 16)))
    exemptions: set[str] = set()
    ex_path = text_dir / "ja-coverage-exemptions.tsv"
    if ex_path.exists():
        exemptions = {r["key"] for r in read_tsv_dicts(ex_path)}
    cap_src = load_cap_sources(text_dir)
    seen_used_exemptions: set[str] = set()
    shared: dict[str, dict[str, str]] = defaultdict(dict)  # key -> {檔: 譯文}
    total_rows = 0
    total_keys: set[str] = set()

    # 家族存在性
    for fam in zh_fams:
        if fam in NO_JA_FAMILIES:
            continue
        if fam not in ja_fams:
            report.err(f"{fam}.{LANG}.tsv", "缺檔（規格 042 §3.1）")
    for fam in ja_fams:
        if fam not in zh_fams:
            report.err(f"{fam}.{LANG}.tsv", "沒有對應的 zh-TW 檔")

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
            if fam in HEADER_ONLY_FAMILIES:
                report.err(where, "manual.ja.tsv 本期必須只有標頭（規格 042 §3.9）")
                continue
            if zh is None:
                report.err(where, f"key 不在 zh-TW 同家族：{key}")
                continue
            check_row(fam, key, text, source, zh[1], zh[2], where, report, charset, characters, cap_src, panel_title)
        if fam in HEADER_ONLY_FAMILIES:
            continue
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
        report.err("ja-coverage-exemptions.tsv", f"豁免 {k} 未被使用（多餘）")
    # 跨檔共用 key
    for key, per_file in shared.items():
        if len(set(per_file.values())) > 1:
            report.err(",".join(sorted(per_file)), f"共用 key 譯文不一致：{key}")
    # 覆蓋斷言
    if expect_rows is not None and total_rows != expect_rows:
        report.err("覆蓋", f"列數 {total_rows} ≠ 預期 {expect_rows}")
    if expect_keys is not None and len(total_keys) != expect_keys:
        report.err("覆蓋", f"不同 key 數 {len(total_keys)} ≠ 預期 {expect_keys}")


def quote_diff(s: str) -> int:
    return sum(s.count(c) for c in "「『") - sum(s.count(c) for c in "」』")


def check_row(fam: str, key: str, ja: str, source: str, zh: str, zh_source: str, where: str, report: Report,
              charset: set[str] | None, characters: set[str] | None, cap_src: dict[str, object],
              panel_title: str | None) -> None:
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
        if c in FORBIDDEN_CHARS or any(lo <= cp <= hi for lo, hi in FORBIDDEN_RANGES):
            report.err(where, f"禁用字元 U+{cp:04X}")
        elif charset is not None and c not in charset:
            report.err(where, f"字集外字元 U+{cp:04X}「{c}」")
        elif characters is not None and c not in characters and 0x21 <= cp:
            report.err(where, f"不在 characters.ja.txt：U+{cp:04X}「{c}」")
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
        if ja[0] in NEW_LINE_START:
            report.err(where, f"定行家族不得以列首禁則字元「{ja[0]}」開頭")
        if ja[-1] in OPENING:
            report.err(where, f"定行家族不得以開括號「{ja[-1]}」結尾")
    # 欄名列（單空白 token）在 header_columns.py 檢查；這裡只擋連續空白於 dispatcher 欄名列
    if "  " in ja and "  " not in zh and fam == "engine-fragment":
        report.warn(where, "含連續空白（若是欄名列會使 anchorColumns 失敗；header_columns.py 判定）")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--text", type=Path, default=ROOT / "text")
    p.add_argument("--font", type=Path, default=ROOT / "font")
    p.add_argument("--expect-rows", type=int)
    p.add_argument("--expect-keys", type=int)
    args = p.parse_args(argv)
    report = Report()
    check(args.text, args.font, report, expect_rows=args.expect_rows, expect_keys=args.expect_keys)
    for w in report.warnings:
        print(w)
    for e in report.errors:
        print(e)
    print(f"ja_check：錯誤 {len(report.errors)}，警告 {len(report.warnings)}")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
