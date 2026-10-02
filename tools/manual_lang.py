#!/usr/bin/env python3
"""規格 051：ja、ko 手冊段落的檢查（與 dosgolem `manualRows` 等價的換列、拉丁字母白名單、字集）。

函式供 tools/lang_check.py 與批次檢查使用；命令列：

  python3 tools/manual_lang.py check --lang ja --catalog text/manual.ja.tsv \\
      --zh text/manual.zh-TW.tsv --charset font/charset.ja.txt

錯誤讓結束碼非零。不含英文原文；白名單以同一列 zh-TW 譯文的拉丁字母詞為基準。
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

COLUMNS = 36
ROWS = 14
ROW_UNITS = 2 * COLUMNS  # 72
SAFE_UNITS = 960         # 規格 051 §3.4：總單位數上限（政策值，容量 1,008 的約 95%）
SAFE_ROWS = 13           # 規格 051 §3.4：逐字元換列後至多 13 列（硬上限 14 列留 1 列餘量）
_JA_SPACE = re.compile(r"[A-Za-z0-9] +[^\x00-\x7f]|[^\x00-\x7f] +[A-Za-z0-9]")

# 拉丁字母詞：以字母或數字起頭、由 ASCII 字母數字與內部的 . ' - 構成的連續串，且至少含一個字母。
_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_TOKEN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9.'\-]*[A-Za-z0-9])?")


def is_half(c: str) -> bool:
    """dosgolem halfwidth.go：ASCII 0x20 至 0x7E 與 U+2022 算半形。"""
    return 0x20 <= ord(c) <= 0x7E or ord(c) == 0x2022


def units(text: str) -> int:
    return sum(1 if is_half(c) else 2 for c in text)


def manual_rows(text: str, columns: int = COLUMNS, rows: int = ROWS) -> list[str] | None:
    """dosgolem manual_overlay_runtime.go 的 manualRows：逐字元換列，放不下的字整個移到下一列；超過 rows 列回 None。"""
    if not text:
        return None
    out: list[str] = [""] * rows
    row, used, start = 0, 0, 0
    for i, c in enumerate(text):
        u = 1 if is_half(c) else 2
        if used + u > 2 * columns:
            out[row] = text[start:i]
            row, used, start = row + 1, 0, i
            if row >= rows:
                return None
        used += u
    out[row] = text[start:]
    return out


def numbers(text: str) -> list[str]:
    """數字（阿拉伯數字串）的排序列表，用來核對譯文沒有改動、漏掉或新增數字。"""
    return sorted(_NUM.findall(text))


def latin_tokens(text: str) -> set[str]:
    """拉丁字母詞集合（至少含一個字母；純數字不算）。"""
    return {t for t in _TOKEN.findall(text) if any(c.isalpha() for c in t)}


def check_paragraph(key: str, text: str, zh_text: str, charset: set[str] | None, lang: str = "") -> list[str]:
    """回傳錯誤訊息列表（空表示通過）。lang 為 ja 時另查日文與拉丁字母之間不得有空白。"""
    errs: list[str] = []
    if not text:
        return [f"{key}: 譯文是空的"]
    if "\t" in text or "\n" in text or "\r" in text or "\\n" in text:
        errs.append(f"{key}: 不得含 tab、換行或 \\n（手冊段落是單一段）")
    if text != text.strip():
        errs.append(f"{key}: 首尾不得有空白")
    if charset is not None:
        bad = sorted({c for c in text if c not in charset})
        if bad:
            errs.append(f"{key}: 字集外的字 {''.join(bad)}")
    extra = sorted(latin_tokens(text) - latin_tokens(zh_text))
    if extra:
        errs.append(f"{key}: 新增的拉丁字母詞（不在 zh-TW 同列）：{'、'.join(extra)}")
    if numbers(text) != numbers(zh_text):
        errs.append(f"{key}: 數字與 zh-TW 同列不同（zh-TW {numbers(zh_text)}，譯文 {numbers(text)}）")
    u = units(text)
    if u > SAFE_UNITS:
        errs.append(f"{key}: {u} 單位，超過安全上限 {SAFE_UNITS}（容量 {ROWS * ROW_UNITS}）")
    rows = manual_rows(text)
    if rows is None:
        errs.append(f"{key}: 以 {COLUMNS} 欄逐字元換列後超過 {ROWS} 列")
    elif len([r for r in rows if r]) > SAFE_ROWS:
        errs.append(f"{key}: 換列後 {len([r for r in rows if r])} 列，超過安全上限 {SAFE_ROWS} 列（硬上限 {ROWS}）")
    if lang == "ja" and _JA_SPACE.search(text):
        errs.append(f"{key}: 日文與拉丁字母（或數字）之間不得有空白")
    return errs


def read_catalog(path: Path) -> list[tuple[str, str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
    if not rows or rows[0] != ["key", "translation", "source"]:
        raise ValueError(f"{path}: 表頭必須是 key、translation、source")
    out = []
    for n, r in enumerate(rows[1:], start=2):
        if len(r) != 3:
            raise ValueError(f"{path}:{n}: 必須恰有 3 欄")
        out.append((r[0], r[1], r[2]))
    return out


def check_catalog(lang: str, catalog: Path, zh: Path, charset: set[str] | None) -> list[str]:
    zh_rows = read_catalog(zh)
    rows = read_catalog(catalog)
    errs: list[str] = []
    zh_map = {k: (t, s) for k, t, s in zh_rows}
    keys = [k for k, _, _ in rows]
    if len(set(keys)) != len(keys):
        errs.append(f"{catalog.name}: 有重複 key")
    if keys != [k for k, _, _ in zh_rows]:
        errs.append(f"{catalog.name}: key 集合或順序與 {zh.name} 不同")
    for key, text, source in rows:
        if key not in zh_map:
            errs.append(f"{key}: 不在 zh-TW")
            continue
        if source != zh_map[key][1]:
            errs.append(f"{key}: source 欄與 zh-TW 不同")
        errs.extend(check_paragraph(key, text, zh_map[key][0], charset, lang))
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="檢查 text/manual.<lang>.tsv")
    c.add_argument("--lang", required=True)
    c.add_argument("--catalog", type=Path, required=True)
    c.add_argument("--zh", type=Path, required=True)
    c.add_argument("--charset", type=Path)
    c.add_argument("--stats", action="store_true", help="印出每段單位數與換列數")
    a = ap.parse_args(argv)
    charset = set(a.charset.read_text(encoding="utf-8").rstrip("\n")) if a.charset else None
    try:
        errs = check_catalog(a.lang, a.catalog, a.zh, charset)
    except (OSError, ValueError) as exc:
        print(f"manual_lang: {exc}", file=sys.stderr)
        return 2
    if a.stats:
        for key, text, _ in read_catalog(a.catalog):
            r = manual_rows(text)
            print(f"{key}\t{units(text)}\t{len([x for x in (r or []) if x])}")
    for e in errs:
        print(f"錯誤：{e}", file=sys.stderr)
    if errs:
        return 1
    print(f"manual_lang: {a.lang} {len(read_catalog(a.catalog))} 段通過")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
