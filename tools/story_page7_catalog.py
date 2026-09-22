#!/usr/bin/env python3
"""驗證第七頁 content-safe identity 與繁中 DRAFT 譯文。"""
from __future__ import annotations
import csv
import re
import sys
import unicodedata
from pathlib import Path

EVENT_HEADER = ["event_key", "sequence", "original_length", "original_sha256", "caller", "glyph_guard", "background", "foreground", "row", "column", "entry_step", "post_call_step", "evidence_level", "catalog_status"]
TRANSLATION_HEADER = ["key", "translation", "source"]
EXPECTED = [
    ("story.page7.line.001", 36, "aab9b4e77e5b9084aeb3c71af6e986373153552d689e0ed1a04f019ea094fb80", 17, 331028417, 332561826),
    ("story.page7.line.002", 36, "286012ec11f1bc1eddcbf52a62ef47b50edcb19a764235e9655b2c5ea71f0354", 18, 332606156, 334139066),
    ("story.page7.line.003", 37, "367a5f1a691a589cd87deecab045512cf1a99a540c798170522747130e2848e1", 19, 334182712, 335760142),
    ("story.page7.line.004", 38, "3c1411ce5cb9e9665cce5d643d090cb085ac8904d8ea77e25e5879ae20c876d5", 20, 335804016, 337424908),
    ("story.page7.line.005", 38, "c56c5c9e8f6f627d7209170bbec80a08d184101a44b81fd2938e433dd6efacd6", 21, 337468554, 339089573),
    ("story.page7.line.006", 5, "3566467963c88d979218b9230a14086b61d4bc146492ea5ed15a3b5855a7fb03", 22, 339133245, 339308875),
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
    if len(events) != 6 or len(translations) != 6:
        raise ValueError("第七頁 DRAFT 必須恰有六筆")
    keys, translation_keys = [r["event_key"] for r in events], [r["key"] for r in translations]
    if keys != translation_keys or len(set(keys)) != 6 or len(set(translation_keys)) != 6:
        raise ValueError("事件與譯文 key 非雙向一對一")
    for i, (row, (key, length, digest, logical_row, entry, post)) in enumerate(zip(events, EXPECTED), 1):
        if (row["event_key"], int(row["sequence"]), int(row["original_length"]), row["original_sha256"], int(row["row"]), int(row["entry_step"]), int(row["post_call_step"])) != (key, i, length, digest, logical_row, entry, post):
            raise ValueError(f"identity 不符：{key}")
        if row["caller"] != "0763:04FF" or row["glyph_guard"] != "0763:026B" or (row["background"], row["foreground"], row["column"], row["evidence_level"], row["catalog_status"]) != ("0", "10", "1", "confirmed", "DRAFT") or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"metadata 不符：{key}")
    for row in translations:
        text = row["translation"]
        if not text or row["source"] != "runtime-editorial" or text != unicodedata.normalize("NFC", text) or text.endswith(" ") or conservative_cells(text) > 39 or any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text):
            raise ValueError(f"譯文格式或寬度不符：{row['key']}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(f"用法：{sys.argv[0]} EVENTS.tsv TRANSLATIONS.tsv")
    validate(Path(sys.argv[1]), Path(sys.argv[2]))
    print("story-page7 DRAFT catalog OK")
