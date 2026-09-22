#!/usr/bin/env python3
"""驗證第八頁 content-safe identity 與繁中 READY 譯文。"""
from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

EVENT_HEADER = ["event_key", "sequence", "original_length", "original_sha256", "caller", "glyph_guard", "background", "foreground", "row", "column", "entry_step", "post_call_step", "evidence_level", "catalog_status"]
TRANSLATION_HEADER = ["key", "translation", "source"]
EXPECTED = [
    ("story.page8.line.001", 38, "fe4920d51364241526b326e9dcb2a44100fa891298fdcbe00269af612c5f0cf3", 17, 341020346, 342641523),
    ("story.page8.line.002", 37, "93e4a1278b2e315c1a37c44c40be891519e0b2de988d6084a729f61209865932", 18, 342684953, 344262194),
    ("story.page8.line.003", 33, "a0a0128ae4b64bf9396830ca0150ace8a80ab9b0668486e311b8eea9b11e8845", 19, 344305840, 345708016),
    ("story.page8.line.004", 22, "b174b4ddd624675cd321067f2f0663d72fe82c55405f175b8348309596af6b1f", 20, 345752448, 346672243),
]


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
    if len(events) != len(EXPECTED) or len(translations) != len(EXPECTED):
        raise ValueError("第八頁 READY 必須恰有四筆")
    keys, translation_keys = [r["event_key"] for r in events], [r["key"] for r in translations]
    if keys != translation_keys or len(set(keys)) != len(EXPECTED) or len(set(translation_keys)) != len(EXPECTED):
        raise ValueError("事件與譯文 key 非雙向一對一")
    for i, (row, (key, length, digest, logical_row, entry, post)) in enumerate(zip(events, EXPECTED), 1):
        actual = (row["event_key"], int(row["sequence"]), int(row["original_length"]), row["original_sha256"], int(row["row"]), int(row["entry_step"]), int(row["post_call_step"]))
        if actual != (key, i, length, digest, logical_row, entry, post):
            raise ValueError(f"identity 不符：{key}")
        if row["caller"] != "0763:04FF" or row["glyph_guard"] != "0763:026B" or (row["background"], row["foreground"], row["column"], row["evidence_level"], row["catalog_status"]) != ("0", "10", "1", "confirmed", "READY") or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"metadata 不符：{key}")
    for row in translations:
        text = row["translation"]
        if not text or row["source"] != "runtime-editorial" or text != unicodedata.normalize("NFC", text) or text.endswith(" ") or conservative_cells(text) > 39 or any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text):
            raise ValueError(f"譯文格式或寬度不符：{row['key']}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        raise SystemExit(f"用法：{sys.argv[0]} EVENTS.tsv TRANSLATIONS.tsv")
    validate(Path(sys.argv[1]), Path(sys.argv[2]))
    print("story-page8 READY catalog OK")
