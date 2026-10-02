#!/usr/bin/env python3
"""驗證保留原題的手冊正文覆繪版面與正式 catalog 容量。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from catalog_font import read_catalog
from manual_lang import manual_rows


HEADER = [
    "layout_key", "clear_x", "clear_y", "clear_width", "clear_height", "text_x", "text_y",
    "columns", "rows", "capacity", "line_height", "line_spacing", "overflow_policy", "evidence_level",
]
EXPECTED = {
    "layout_key": "manual.paragraph.body",
    "clear_x": 7,
    "clear_y": 72,
    "clear_width": 305,
    "clear_height": 112,
    "text_x": 16,
    "text_y": 72,
    "columns": 36,
    "rows": 14,
    "capacity": 504,
    "line_height": 8,
    "line_spacing": 0,
    "overflow_policy": "single-page-reject",
    "evidence_level": "confirmed",
}


def validate(layout_path: Path, catalog_path: Path) -> int:
    with layout_path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if reader.fieldnames != HEADER:
            raise ValueError("手冊 layout 欄位不符合固定 schema")
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError("手冊 layout 必須恰有一筆正文矩形")
    row = rows[0]
    for key, expected in EXPECTED.items():
        value = row[key]
        if isinstance(expected, int):
            try:
                value = int(value)
            except ValueError as exc:
                raise ValueError(f"{key}: 不是整數") from exc
        if value != expected:
            raise ValueError(f"{key}: 與已確認保留原題版面不符")

    text_right = EXPECTED["text_x"] + EXPECTED["columns"] * 8
    text_bottom = EXPECTED["text_y"] + EXPECTED["rows"] * (EXPECTED["line_height"] + EXPECTED["line_spacing"])
    clear_right = EXPECTED["clear_x"] + EXPECTED["clear_width"]
    clear_bottom = EXPECTED["clear_y"] + EXPECTED["clear_height"]
    if text_right > clear_right or text_bottom > clear_bottom:
        raise ValueError("正文格線超出已確認清除矩形")
    if EXPECTED["capacity"] != EXPECTED["columns"] * EXPECTED["rows"]:
        raise ValueError("正文容量未由欄列導出")

    catalog = read_catalog(catalog_path)
    for entry in catalog:
        if manual_rows(entry.translation, EXPECTED["columns"], EXPECTED["rows"]) is None:  # 規格 051：半形算半格、逐字元換列，與 dosgolem manualRows 等價
            raise ValueError(f"{entry.key}: 以 36 欄逐字元換列後超過 14 列（單頁上限 504 個全形格）")
    return len(catalog)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layout", type=Path)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    try:
        print(f"validated {validate(args.layout, args.catalog)} manual paragraphs at 504 characters")
    except (OSError, ValueError, csv.Error) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
