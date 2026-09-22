#!/usr/bin/env python3
"""驗證第九頁 content-safe identity 與繁中 DRAFT 譯文。"""
from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

EVENT_HEADER = ["event_key", "sequence", "original_length", "original_sha256", "caller", "glyph_guard", "background", "foreground", "row", "column", "entry_step", "post_call_step", "evidence_level", "catalog_status"]
TRANSLATION_HEADER = ["key", "translation", "source"]
EXPECTED = ("story.page9.line.001", 20, "39a751ca9f384a77491b1e4399c0a72afb8b1ef146a77db2623394590ff1ca78", 17, 351155910, 351988536)


def conservative_cells(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in {"W", "F"} else 1 for ch in text)


def _rows(path: Path, header: list[str]) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        raise ValueError(f"{path}: BOM/CR 不合法")
    raw.decode("utf-8")
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != header:
            raise ValueError(f"{path}: 標頭不符")
        rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError(f"{path}: 欄數不符")
    return rows


def validate(events_path: Path, translations_path: Path) -> None:
    events, translations = _rows(events_path, EVENT_HEADER), _rows(translations_path, TRANSLATION_HEADER)
    if len(events) != 1 or len(translations) != 1:
        raise ValueError("第九頁 DRAFT 必須恰有一筆")
    row = events[0]
    key, length, digest, logical_row, entry, post = EXPECTED
    actual = (row["event_key"], int(row["sequence"]), int(row["original_length"]), row["original_sha256"], int(row["row"]), int(row["entry_step"]), int(row["post_call_step"]))
    if actual != (key, 1, length, digest, logical_row, entry, post):
        raise ValueError("identity 不符：story.page9.line.001")
    if row["caller"] != "0763:04FF" or row["glyph_guard"] != "0763:026B" or (row["background"], row["foreground"], row["column"], row["evidence_level"], row["catalog_status"]) != ("0", "10", "1", "confirmed", "DRAFT") or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("metadata 不符：story.page9.line.001")
    translation = translations[0]
    if translation["key"] != key:
        raise ValueError("事件與譯文 key 非雙向一對一")
    text = translation["translation"]
    if not text or translation["source"] != "runtime-editorial" or text != unicodedata.normalize("NFC", text) or text.endswith(" ") or conservative_cells(text) > 39 or any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text):
        raise ValueError("譯文格式或寬度不符")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        raise SystemExit(f"用法：{sys.argv[0]} EVENTS.tsv TRANSLATIONS.tsv")
    validate(Path(sys.argv[1]), Path(sys.argv[2]))
    print("story-page9 DRAFT catalog OK")
