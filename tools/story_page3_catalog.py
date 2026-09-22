#!/usr/bin/env python3
"""驗證第三頁固定劇情的 DRAFT exact identity 與繁中候選。"""

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
    ("story.page3.line.001", 34, "84c6fba5f613f52a02e935f0937bb66eea6632840d9465cf8fc9c3d7edd0dbff", 17, 291022040, 292467756),
    ("story.page3.line.002", 37, "6ea1adb513486d4687926d744f1d9ff22638ee3a9eaeef6fe6ff97282c361536", 18, 292511846, 294089001),
    ("story.page3.line.003", 31, "fd9dbc141cf71e523e4f8a45fe5ced142f55d5257f5801f4259142162bf5f37a", 19, 294132533, 295447194),
    ("story.page3.line.004", 37, "93c17e4396f05f1e17c659f42233369c205ae8f23280c796e0bf8b023873479d", 20, 295491296, 297068295),
    ("story.page3.line.005", 5, "8f0cfc1b387ddcad6870b6a960f67f71d044bd7163d01db49e753b6e71afb7d5", 21, 297111967, 297287594),
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
        raise ValueError("第三頁 DRAFT 必須恰有五筆固定劇情")
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
        if int(row["row"]) != logical_row or not (17 <= logical_row <= 21):
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
        if not text or row["source"] != "runtime-editorial":
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
    print("story-page3 DRAFT catalog OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
