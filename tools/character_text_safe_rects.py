#!/usr/bin/env python3
"""驗證性別／職業 logical 320×200 文字安全矩形與繁中容量。"""

from __future__ import annotations

import csv
from pathlib import Path

import class_events
import gender_events

HEADER = ["event_key", "x", "y", "width", "height", "draw_x", "draw_y",
          "capacity_cells", "line_count", "overflow_policy"]


def _rows(path: Path, header: list[str]) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path}: 不得含 BOM")
    try:
        table = list(csv.reader(raw.decode("utf-8").splitlines(), delimiter="\t"))
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: 不是有效 UTF-8") from exc
    if not table or table[0] != header or any(len(row) != len(header) for row in table[1:]):
        raise ValueError(f"{path}: schema 不符")
    return [dict(zip(header, row)) for row in table[1:]]


def validate(rects_path: Path, events_path: Path, catalog_path: Path, kind: str,
             post_path: Path, lifecycle_path: Path) -> None:
    if kind == "gender":
        gender_events.validate(events_path, catalog_path, post_path, lifecycle_path)
    elif kind == "class":
        class_events.validate(events_path, catalog_path, post_path, lifecycle_path)
    else:
        raise ValueError("kind 必須是 gender 或 class")
    rects = _rows(rects_path, HEADER)
    events = {row["event_key"]: row for row in _rows(events_path, class_events.EVENT_HEADER)}
    texts = {row["key"]: row["translation"] for row in _rows(catalog_path, class_events.TEXT_HEADER)}
    if len(rects) != len(events) or {r["event_key"] for r in rects} != set(events):
        raise ValueError("安全矩形與事件鍵必須一對一")
    for row in rects:
        key, event = row["event_key"], events[row["event_key"]]
        names = HEADER[1:9]
        try:
            values = tuple(int(row[name]) for name in names)
        except ValueError as exc:
            raise ValueError(f"{key}: 幾何必須為 ASCII 十進位整數") from exc
        if any(str(value) != row[name] for value, name in zip(values, names)):
            raise ValueError(f"{key}: 幾何不是 canonical ASCII 十進位")
        x, y, width, height, draw_x, draw_y, capacity, lines = values
        expected = (int(event["column"]) * 8, int(event["row"]) * 8,
                    int(event["original_length"]) * 8, 8)
        if (x, y, width, height) != expected:
            raise ValueError(f"{key}: 清除矩形不等於 exact identity 原文矩形")
        if min(values) < 0 or x + width > 320 or y + height > 200 or any(v % 8 for v in values[:6]):
            raise ValueError(f"{key}: 幾何越界或未對齊")
        if draw_x != x or draw_y != y or capacity != width // 8 or lines != 1:
            raise ValueError(f"{key}: anchor／capacity／line_count 不符")
        if row["overflow_policy"] != "single-line-reject" or len(texts[event["text_key"]]) > capacity:
            raise ValueError(f"{key}: overflow policy 或譯文容量不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("gender", "class"))
    for name in ("rects_path", "events_path", "catalog_path", "post_path", "lifecycle_path"):
        parser.add_argument(name, type=Path)
    validate(**vars(parser.parse_args()))
