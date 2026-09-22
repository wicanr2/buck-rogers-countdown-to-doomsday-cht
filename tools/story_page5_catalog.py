#!/usr/bin/env python3
"""驗證第五頁低階 identity 與繁中候選；DRAFT，不授權 runtime。"""
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
    ("story.page5.line.001", 34, "03a272d4abbd18dec91119382124d6c884f0e3774282ea09da5d99398cf80198", 17, 310025410, 311471305),
    ("story.page5.line.002", 38, "db72900ffc61c01cb49f5a3919819c4069a2582a9177dcf57917399d3f39abe1", 18, 311515077, 313136143),
    ("story.page5.line.003", 35, "d688b262bd262f45a25d351f8b85c919af3254b41944086f1f595f15bbd3878a", 19, 313180017, 314669839),
    ("story.page5.line.004", 36, "0b9c76df8c266950d6fcf8cb4dea52c4f9ccf91e41a8248095e1649b874e0a16", 20, 314713839, 316247017),
    ("story.page5.line.005", 25, "1572bf767f5ecfe323e56db37bdd2d96051aecc186203677c4f5e4db75b222c9", 21, 316290891, 317342460),
]


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
        raise ValueError("第五頁 DRAFT 必須恰有五筆")
    keys = [row["event_key"] for row in events]
    translation_keys = [row["key"] for row in translations]
    if keys != translation_keys or len(set(keys)) != len(keys) or len(set(translation_keys)) != len(translation_keys):
        raise ValueError("事件與譯文 key 非雙向一對一")
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
        if int(row["row"]) != logical_row or not 17 <= logical_row <= 21:
            raise ValueError(f"故事區列不符：{key}")
        if (int(row["entry_step"]), int(row["post_call_step"])) != (entry, post):
            raise ValueError(f"步數不符：{key}")
        if row["evidence_level"] != "proven" or row["catalog_status"] != "DRAFT":
            raise ValueError(f"DRAFT 狀態或證據分級不符：{key}")
    for row in translations:
        text = row["translation"]
        if not text or row["source"] != "runtime-editorial":
            raise ValueError(f"譯文來源或內容不符：{row['key']}")
        if text != unicodedata.normalize("NFC", text):
            raise ValueError(f"譯文非 NFC：{row['key']}")
        if any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text):
            raise ValueError(f"譯文不得含控制或格式字元：{row['key']}")
        if text.endswith(" "):
            raise ValueError(f"譯文不得含尾端空白：{row['key']}")
        if conservative_cells(text) > STORY_CELL_CAPACITY:
            raise ValueError(f"譯文超過故事區 39 格：{row['key']}")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"用法：{argv[0]} EVENTS.tsv TRANSLATIONS.tsv", file=sys.stderr)
        return 2
    try:
        validate(Path(argv[1]), Path(argv[2]))
    except (OSError, ValueError) as exc:
        print(f"失敗即關閉：{exc}", file=sys.stderr)
        return 1
    print("story-page5 DRAFT catalog OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
