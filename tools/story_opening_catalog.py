#!/usr/bin/env python3
"""驗證首屏劇情 READY exact identity 與繁中譯文的雙向覆蓋。"""

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
    ("story.opening.line.001", 37, "a989ceac7d0b25ad1a02fca8d158c5c47ab25aa28faa329f99016bcbd22d89d2", 17, 268686427, 270263541),
    ("story.opening.line.002", 38, "177bcfea0dd3bdba2390155791c7c48097736031d03e90eff9c1e594e7d24dc5", 18, 270307529, 271928281),
    ("story.opening.line.003", 33, "c6a67dbd38752114fcf6761f59a57ed0970d0c75ac63696466c8f99d658a963b", 19, 271971771, 273373887),
    ("story.opening.line.004", 29, "a0cb29721abfb85c6062169ef8d5c8a0d4e794570a007b472fc3f2c655dcd182", 20, 273417761, 274644543),
    ("story.opening.line.005", 23, "f686b3355b648d95981ec5c128fc4e07f0950c983e9543c49a258fbcd1ea5d74", 21, 274689101, 275652511),
]
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


def conservative_cells(text: str) -> int:
    """估算 16px ETen 字模在原版 8px 格中的佔用格數。

    這是資料層的保守上界：全形／寬字元佔兩格，其餘字元佔一格。
    實際 2×／3× 字模邊界另依 spec010 的本機原型收據審查；此函式不冒稱 runtime A/B。
    """
    return sum(2 if unicodedata.east_asian_width(ch) in {"W", "F"} else 1 for ch in text)


def _rows(path: Path, header: list[str]) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path}: 不得含 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: 不是有效 UTF-8") from exc
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != header:
            raise ValueError(f"{path}: 標頭不符")
        rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError(f"{path}: 欄數不符")
    if b"\r" in raw:
        raise ValueError(f"{path}: 不得含 CR 字元")
    return rows


def validate(events_path: Path, translations_path: Path) -> None:
    events = _rows(events_path, EVENT_HEADER)
    translations = _rows(translations_path, TRANSLATION_HEADER)
    if len(events) != 5 or len(translations) != 5:
        raise ValueError("READY 首屏劇情必須恰有五筆")
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
        if (int(row["row"]), int(row["entry_step"]), int(row["post_call_step"])) != (logical_row, entry, post):
            raise ValueError(f"步數／列不符：{key}")
        if row["evidence_level"] != "confirmed" or row["catalog_status"] != "READY":
            raise ValueError(f"READY 狀態或證據分級不符：{key}")
    keys = [row["event_key"] for row in events]
    translation_keys = [row["key"] for row in translations]
    if keys != translation_keys or len(set(keys)) != len(keys) or len(set(translation_keys)) != len(translation_keys):
        raise ValueError("事件與譯文 key 非雙向一對一")
    event_by_key = {row["event_key"]: row for row in events}
    for row in translations:
        if not row["translation"] or row["source"] not in {"runtime-editorial", "manual-term-editorial"}:
            raise ValueError(f"譯文來源或內容不符：{row['key']}")
        if row["translation"] != unicodedata.normalize("NFC", row["translation"]):
            raise ValueError(f"譯文非 NFC：{row['key']}")
        if any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in row["translation"]):
            raise ValueError(f"譯文不得含控制或格式字元：{row['key']}")
        cells = conservative_cells(row["translation"])
        if cells > STORY_CELL_CAPACITY:
            raise ValueError(f"譯文超過故事區 39 格安全矩形（資料層保守上界 {cells} 格）：{row['key']}")
        if row["translation"].endswith(" "):
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
    print("story-opening READY catalog OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
