#!/usr/bin/env python3
"""驗證第六頁 content-safe identity 與繁中 DRAFT 譯文。"""
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from pathlib import Path

EVENT_HEADER = ["event_key", "sequence", "original_length", "original_sha256", "caller", "glyph_guard", "background", "foreground", "row", "column", "entry_step", "post_call_step", "evidence_level", "catalog_status"]
TRANSLATION_HEADER = ["key", "translation", "source"]
STORY_CELL_CAPACITY = 39
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
EXPECTED = [
    ("story.page6.line.001", 37, "d053056eb6958d1b38d28ff193b8102c7eaa64fb6db0864582d9f060201f463e", 17, 321119958, 322697067),
    ("story.page6.line.002", 34, "fa20332aaf7be72ca4ba8b7b745a9691a5de12d3f917f07843657a48891f4d01", 18, 322740929, 324187017),
    ("story.page6.line.003", 36, "0f61c2ab249eed0ca1e8d89ac8f2a6ac0d2886fad2cd8f9312592d0cdf5bb3c1", 19, 324231131, 325764354),
    ("story.page6.line.004", 38, "2099600ba5c88af0aae899a1739eab8c791dfe1385ca8493c64aabdab27d2a65", 20, 325808798, 327429545),
    ("story.page6.line.005", 36, "beb4798b2f69f82186693d602ddcd76f30557d6797a45f4b506c797d4b4872cf", 21, 327473647, 329006868),
    ("story.page6.line.006", 19, "276a43ecca15ed7b57fe5b73f7e9bfefb04eec4a686ddb442fb0fc8712ceb48a", 22, 329050400, 329839410),
]


def conservative_cells(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in {"W", "F"} else 1 for ch in text)


def _rows(path: Path, header: list[str]) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        raise ValueError(f"{path}: BOM/CR 不合法")
    raw.decode("utf-8")
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
        raise ValueError("第六頁 DRAFT 必須恰有六筆")
    keys = [row["event_key"] for row in events]
    translation_keys = [row["key"] for row in translations]
    if keys != translation_keys or len(set(keys)) != len(keys) or len(set(translation_keys)) != len(translation_keys):
        raise ValueError("事件與譯文 key 非雙向一對一")
    for index, (row, expected) in enumerate(zip(events, EXPECTED), start=1):
        key, length, digest, logical_row, entry, post = expected
        if row["event_key"] != key or int(row["sequence"]) != index:
            raise ValueError(f"事件順序不符：{key}")
        if int(row["original_length"]) != length or row["original_sha256"] != digest or not SHA256_RE.fullmatch(row["original_sha256"]):
            raise ValueError(f"原版 identity 不符：{key}")
        if (row["caller"], row["glyph_guard"], row["background"], row["foreground"], row["column"], row["evidence_level"], row["catalog_status"]) != ("0763:04FF", "0763:026B", "0", "10", "1", "confirmed", "DRAFT"):
            raise ValueError(f"metadata 不符：{key}")
        if int(row["row"]) != logical_row or not 17 <= logical_row <= 22:
            raise ValueError(f"故事區列不符：{key}")
        if (int(row["entry_step"]), int(row["post_call_step"])) != (entry, post):
            raise ValueError(f"步數不符：{key}")
    for row in translations:
        text = row["translation"]
        if not text or row["source"] != "runtime-editorial":
            raise ValueError(f"譯文來源或內容不符：{row['key']}")
        if text != unicodedata.normalize("NFC", text) or any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text):
            raise ValueError(f"譯文 Unicode 不符：{row['key']}")
        if text.endswith(" ") or conservative_cells(text) > STORY_CELL_CAPACITY:
            raise ValueError(f"譯文格式或寬度不符：{row['key']}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(f"用法：{sys.argv[0]} EVENTS.tsv TRANSLATIONS.tsv")
    validate(Path(sys.argv[1]), Path(sys.argv[2]))
    print("story-page6 DRAFT catalog OK")
