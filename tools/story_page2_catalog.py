#!/usr/bin/env python3
"""驗證第二頁固定劇情的 DRAFT exact identity 與繁中候選。"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from pathlib import Path

EVENT_HEADER = ["event_key", "sequence", "original_length", "original_sha256", "caller", "glyph_guard", "background", "foreground", "row", "column", "entry_step", "post_call_step", "evidence_level", "catalog_status"]
TRANSLATION_HEADER = ["key", "translation", "source"]
STORY_CELL_CAPACITY = 39
EXPECTED = [
    ("story.page2.line.001", 37, "d5e1af5a30c6c4954aec9e63c0ab8454f5b451d333b9c58c0b66a89c43733364", 17, 281022067, 282599485),
    ("story.page2.line.002", 31, "8834f68a0a932af699b5f090e02a652184341ef8c107ca30d714097b6f9e91c7", 18, 282643017, 283957425),
    ("story.page2.line.003", 38, "57910b8786c4b13181ed37f12b273e7f43886747dbab9fb360f09071ae39c7bd", 19, 284002085, 285622608),
    ("story.page2.line.004", 37, "a114f1a715a848c0280677ab70d806145ae5e1991f6f570f5ace5d49c9dc85b4", 20, 285666098, 287243280),
]
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


def conservative_cells(text: str) -> int:
    """DRAFT 保守估算：ETen 全形／寬字元 2 格，其他字元 1 格。"""
    return sum(2 if unicodedata.east_asian_width(ch) in {"W", "F"} else 1 for ch in text)


def _rows(path: Path, header: list[str]) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        raise ValueError(f"{path}: BOM／CR 不合法")
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: 不是有效 UTF-8") from exc
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != header:
            raise ValueError(f"{path}: 標頭不符")
        rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError(f"{path}: 欄數不符")
    return rows


def validate(events_path: Path, translations_path: Path) -> None:
    events = _rows(events_path, EVENT_HEADER)
    translations = _rows(translations_path, TRANSLATION_HEADER)
    if len(events) != len(EXPECTED) or len(translations) != len(EXPECTED):
        raise ValueError("第二頁 DRAFT 必須恰有四筆固定劇情")
    for index, (row, expected) in enumerate(zip(events, EXPECTED), start=1):
        key, length, digest, logical_row, entry, post = expected
        if row["event_key"] != key or int(row["sequence"]) != index:
            raise ValueError(f"事件順序不符：{key}")
        if int(row["original_length"]) != length or row["original_sha256"] != digest:
            raise ValueError(f"原版 identity 不符：{key}")
        if not SHA256_RE.fullmatch(row["original_sha256"]):
            raise ValueError(f"hash 格式不符：{key}")
        if row["caller"] != "0763:04FF" or row["glyph_guard"] != "0763:026B":
            raise ValueError(f"位址不符：{key}")
        if (row["background"], row["foreground"], row["column"]) != ("0", "10", "1"):
            raise ValueError(f"顏色／欄位不符：{key}")
        if int(row["row"]) != logical_row or not (17 <= logical_row <= 20):
            raise ValueError(f"故事區列不符：{key}")
        if (int(row["entry_step"]), int(row["post_call_step"])) != (entry, post):
            raise ValueError(f"步數不符：{key}")
        if row["evidence_level"] != "confirmed" or row["catalog_status"] != "DRAFT":
            raise ValueError(f"DRAFT 狀態或證據分級不符：{key}")
    keys = [row["event_key"] for row in events]
    translation_keys = [row["key"] for row in translations]
    if keys != translation_keys or len(set(keys)) != len(keys) or len(set(translation_keys)) != len(translation_keys):
        raise ValueError("事件與譯文 key 非雙向一對一")
    for row in translations:
        text = row["translation"]
        if not text or row["source"] != "manual-and-runtime":
            raise ValueError(f"譯文來源或內容不符：{row['key']}")
        if text != unicodedata.normalize("NFC", text):
            raise ValueError(f"譯文非 NFC：{row['key']}")
        if any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text):
            raise ValueError(f"譯文不得含控制或格式字元：{row['key']}")
        if conservative_cells(text) > STORY_CELL_CAPACITY:
            raise ValueError(f"譯文超過故事區 39 格：{row['key']}")
        if text.endswith(" "):
            raise ValueError(f"譯文不得含尾端空白：{row['key']}")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"用法：{argv[0]} EVENTS.tsv TRANSLATIONS.tsv", file=sys.stderr)
        return 2
    try:
        validate(Path(argv[1]), Path(argv[2]))
    except (OSError, ValueError) as exc:
        print(f"失敗即關閉：{exc}", file=sys.stderr)
        return 1
    print("story-page2 DRAFT catalog OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
