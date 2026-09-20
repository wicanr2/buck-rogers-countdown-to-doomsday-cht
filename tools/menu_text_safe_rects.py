#!/usr/bin/env python3
"""Validate logical 320x200 menu text-safe rectangles and CJK capacity."""

from __future__ import annotations

import csv
from pathlib import Path

import menu_events


HEADER = [
    "event_key", "x", "y", "width", "height", "draw_x", "draw_y",
    "capacity_cells", "line_count", "overflow_policy",
]


def _rows(path: Path) -> list[dict[str, str]]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path}: 不得含 UTF-8 BOM")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: 不是有效 UTF-8") from exc
    raw = list(csv.reader(text.splitlines(), delimiter="\t"))
    if not raw or raw[0] != HEADER:
        raise ValueError(f"{path}: 標頭不符")
    if not raw[1:]:
        raise ValueError(f"{path}: 不得為空")
    for line, row in enumerate(raw[1:], 2):
        if len(row) != len(HEADER) or any(value == "" for value in row):
            raise ValueError(f"{path}:{line}: 欄位數錯誤或空欄")
    return [dict(zip(HEADER, row)) for row in raw[1:]]


def validate(rects_path: Path, events_path: Path, catalog_path: Path) -> None:
    menu_events.validate(events_path, catalog_path)
    rects = _rows(rects_path)
    with events_path.open(encoding="utf-8", newline="") as stream:
        events = {row["event_key"]: row for row in csv.DictReader(stream, delimiter="\t")}
    with catalog_path.open(encoding="utf-8", newline="") as stream:
        catalog = {row["key"]: row["translation"] for row in csv.DictReader(stream, delimiter="\t")}

    if len(rects) != len(events) or {row["event_key"] for row in rects} != set(events):
        raise ValueError("menu-text-safe-rects.tsv: event key 必須與事件表一對一")

    by_row: dict[int, list[tuple[int, int, str]]] = {}
    for row in rects:
        key = row["event_key"]
        event = events[key]
        try:
            x, y, width, height, draw_x, draw_y, capacity, lines = (
                int(row[name]) for name in HEADER[1:9]
            )
        except ValueError as exc:
            raise ValueError(f"{key}: 幾何欄必須是 ASCII 十進位整數") from exc
        values = (x, y, width, height, draw_x, draw_y, capacity, lines)
        if any(str(value) != row[name] for value, name in zip(values, HEADER[1:9])):
            raise ValueError(f"{key}: 幾何欄必須是 canonical ASCII 十進位")
        expected_x = int(event["column"]) * 8
        expected_y = int(event["row"]) * 8
        expected_width = int(event["original_length"]) * 8
        if (x, y, width, height) != (expected_x, expected_y, expected_width, 8):
            raise ValueError(f"{key}: 清除矩形不等於已證實原文矩形")
        if min(x, y, width, height, draw_x, draw_y, capacity, lines) < 0:
            raise ValueError(f"{key}: 不接受負數")
        if x + width > 320 or y + height > 200:
            raise ValueError(f"{key}: 矩形超出 320×200")
        if any(value % 8 for value in (x, y, width, height, draw_x, draw_y)):
            raise ValueError(f"{key}: 幾何必須對齊 8-pixel logical cell")
        if not (x <= draw_x < x + width) or draw_y != y:
            raise ValueError(f"{key}: draw anchor 不在清除矩形首列")
        if capacity != (x + width - draw_x) // 8 or lines != 1:
            raise ValueError(f"{key}: capacity 或 line_count 不符")
        if row["overflow_policy"] != "single-line-reject":
            raise ValueError(f"{key}: overflow policy 不符")
        if len(catalog[event["text_key"]]) > capacity:
            raise ValueError(f"{key}: 繁中譯文超過單行容量")
        by_row.setdefault(y, []).append((x, x + width, key))

    sorted_y = sorted(by_row)
    for first, second in zip(sorted_y, sorted_y[1:]):
        if first + 8 > second:
            raise ValueError(f"相鄰 logical row 垂直侵入：{first} → {second}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("rects", type=Path)
    parser.add_argument("events", type=Path)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    validate(args.rects, args.events, args.catalog)
