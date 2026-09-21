#!/usr/bin/env python3
"""驗證職業技能配置文字安全矩形與動態數值邊界。"""

from __future__ import annotations

import csv
from pathlib import Path

import career_skill_screen_catalog
import menu_text_safe_rects

HEADER = menu_text_safe_rects.HEADER


def validate(rects_path: Path, events_path: Path, translations_path: Path,
             confirm_path: Path, selection_path: Path, character_text_path: Path) -> None:
    career_skill_screen_catalog.validate(events_path, translations_path, confirm_path,
                                         selection_path, character_text_path)
    rects = menu_text_safe_rects._rows(rects_path)
    with events_path.open(encoding="utf-8", newline="") as stream:
        events = {row["event_key"]: row for row in csv.DictReader(stream, delimiter="\t")}
    with translations_path.open(encoding="utf-8", newline="") as stream:
        texts = {row["key"]: row["translation"] for row in csv.DictReader(stream, delimiter="\t")}
    if len(rects) != 14 or len({row["event_key"] for row in rects}) != 14 or {row["event_key"] for row in rects} != set(events):
        raise ValueError("職業技能矩形必須與 14 個 event keys 一對一")
    for row in rects:
        key, event = row["event_key"], events[row["event_key"]]
        try:
            values = [int(row[name]) for name in HEADER[1:9]]
        except ValueError as exc:
            raise ValueError(f"{key}: 幾何欄不是整數") from exc
        if any(str(value) != row[name] for value, name in zip(values, HEADER[1:9])):
            raise ValueError(f"{key}: 幾何欄不是 canonical 十進位")
        x, y, width, height, draw_x, draw_y, capacity, lines = values
        expected = (int(event["column"]) * 8, int(event["row"]) * 8,
                    int(event["original_length"]) * 8, 8)
        if (x, y, width, height) != expected or (draw_x, draw_y) != (x, y):
            raise ValueError(f"{key}: 矩形不符 exact event 幾何")
        if x + width > 320 or y + height > 200 or capacity != width // 8 or lines != 1:
            raise ValueError(f"{key}: 尺寸、容量或行數不符")
        if row["overflow_policy"] != "single-line-reject" or len(texts[event["text_key"]]) > capacity:
            raise ValueError(f"{key}: overflow policy 或譯文容量不符")
    with confirm_path.open(encoding="utf-8", newline="") as stream:
        source = list(csv.DictReader(stream, delimiter="\t"))
    dynamic = {(int(row["row"]), int(row["column"])) for row in source
               if row["event_role"] == "skill_allocation_screen" and int(row["column"]) in {23, 29, 35}}
    if not all((row, col) in dynamic for row in range(6, 14) for col in (23, 29, 35)):
        raise ValueError("技能 points／bonus／total 動態邊界不完整")
    for row in rects:
        y, right = int(row["y"]) // 8, int(row["x"]) + int(row["width"])
        same_row_dynamic = [column * 8 for dyn_row, column in dynamic if dyn_row == y]
        if same_row_dynamic and right > min(same_row_dynamic):
            raise ValueError(f"{row['event_key']}: 矩形侵入動態數值欄")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("rects_path", "events_path", "translations_path", "confirm_path", "selection_path",
                 "character_text_path"):
        parser.add_argument(name, type=Path)
    validate(**vars(parser.parse_args()))
