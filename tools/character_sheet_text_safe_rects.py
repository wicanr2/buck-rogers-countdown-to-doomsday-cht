#!/usr/bin/env python3
"""驗證角色資料頁靜態繁中安全矩形及動態值邊界。"""

from __future__ import annotations

import csv
from pathlib import Path

import character_sheet_events
import menu_text_safe_rects

HEADER = menu_text_safe_rects.HEADER
EXTENDED_RIGHT = {
    "character.sheet.label.ac": 35 * 8,
    "character.sheet.label.thac0": 35 * 8,
}


def validate(rects_path: Path, events_path: Path, catalog_path: Path, inventory_path: Path) -> None:
    character_sheet_events.validate(events_path, catalog_path, inventory_path)
    rects = menu_text_safe_rects._rows(rects_path)
    with events_path.open(encoding="utf-8", newline="") as stream:
        events = {row["event_key"]: row for row in csv.DictReader(stream, delimiter="\t")}
    with catalog_path.open(encoding="utf-8", newline="") as stream:
        texts = {row["key"]: row["translation"] for row in csv.DictReader(stream, delimiter="\t")}
    if len(rects) != 35 or len({row["event_key"] for row in rects}) != 35 or {row["event_key"] for row in rects} != set(events):
        raise ValueError("角色資料安全矩形必須與 35 個事件一對一")

    occupied: dict[int, list[tuple[int, int, str]]] = {}
    for row in rects:
        key, event = row["event_key"], events[row["event_key"]]
        try:
            values = [int(row[name]) for name in HEADER[1:9]]
        except ValueError as exc:
            raise ValueError(f"{key}: 幾何欄不是整數") from exc
        if any(str(value) != row[name] for value, name in zip(values, HEADER[1:9])):
            raise ValueError(f"{key}: 幾何欄不是 canonical 十進位")
        x, y, width, height, draw_x, draw_y, capacity, lines = values
        source_x, source_y = int(event["column"]) * 8, int(event["row"]) * 8
        source_right = source_x + int(event["original_length"]) * 8
        expected_right = EXTENDED_RIGHT.get(key, source_right)
        if (x, y, x + width, height, draw_x, draw_y) != (source_x, source_y, expected_right, 8, source_x, source_y):
            raise ValueError(f"{key}: 矩形不符原文起點或已證實動態右界")
        if any(value < 0 for value in values) or any(value % 8 for value in (x, y, width, height, draw_x, draw_y)):
            raise ValueError(f"{key}: 幾何越界或未對齊")
        if x + width > 320 or y + height > 200 or capacity != width // 8 or lines != 1:
            raise ValueError(f"{key}: 尺寸、容量或行數不符")
        if row["overflow_policy"] != "single-line-reject" or len(texts[event["text_key"]]) > capacity:
            raise ValueError(f"{key}: overflow policy 或譯文容量不符")
        for left, right, other in occupied.setdefault(y, []):
            if x < right and left < x + width:
                raise ValueError(f"{key}: 與 {other} 的安全矩形重疊")
        occupied[y].append((x, x + width, key))

    # AC／THAC0 的擴張右界由同列 col 35 動態值證實；不得越過該值。
    with inventory_path.open(encoding="utf-8", newline="") as stream:
        inventory = list(csv.DictReader(stream, delimiter="\t"))
    dynamic_points = {(int(row["row"]), int(row["column"])) for row in inventory
                      if row["event_role"] in {"identity_value", "summary_value"}}
    if (2, 35) not in dynamic_points or (3, 35) not in dynamic_points:
        raise ValueError("缺少 AC／THAC0 同列動態值邊界證據")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("rects_path", "events_path", "catalog_path", "inventory_path"):
        parser.add_argument(name, type=Path)
    validate(**vars(parser.parse_args()))
