#!/usr/bin/env python3
"""驗證姓名提示安全矩形及玩家輸入欄邊界。"""

from __future__ import annotations

import csv
from pathlib import Path

import menu_text_safe_rects
import name_prompt_catalog

HEADER = menu_text_safe_rects.HEADER


def validate(rects_path: Path, events_path: Path, translations_path: Path,
             inventory_path: Path, edit_path: Path) -> None:
    name_prompt_catalog.validate(events_path, translations_path, inventory_path)
    rects = menu_text_safe_rects._rows(rects_path)
    if len(rects) != 1 or rects[0]["event_key"] != "character.name.prompt":
        raise ValueError("姓名提示安全矩形必須與唯一事件一對一")
    with events_path.open(encoding="utf-8", newline="") as stream:
        event = next(csv.DictReader(stream, delimiter="\t"))
    with translations_path.open(encoding="utf-8", newline="") as stream:
        translation = next(csv.DictReader(stream, delimiter="\t"))["translation"]
    row = rects[0]
    try:
        values = [int(row[name]) for name in HEADER[1:9]]
    except ValueError as exc:
        raise ValueError("姓名提示幾何欄不是整數") from exc
    if any(str(value) != row[name] for value, name in zip(values, HEADER[1:9])):
        raise ValueError("姓名提示幾何欄不是 canonical 十進位")
    x, y, width, height, draw_x, draw_y, capacity, lines = values
    expected = (int(event["column"]) * 8, int(event["row"]) * 8,
                int(event["original_length"]) * 8, 8)
    if (x, y, width, height) != expected or (draw_x, draw_y) != (x, y):
        raise ValueError("姓名提示矩形不符原文事件幾何")
    if x + width > 320 or y + height > 200 or capacity != width // 8 or lines != 1:
        raise ValueError("姓名提示尺寸、容量或行數不符")
    if row["overflow_policy"] != "single-line-reject" or len(translation) > capacity:
        raise ValueError("姓名提示 overflow policy 或譯文容量不符")
    with edit_path.open(encoding="utf-8", newline="") as stream:
        echoes = [record for record in csv.DictReader(stream, delimiter="\t")
                  if record["event_role"] == "input_echo"]
    if not echoes or any(record["row"] != event["row"] for record in echoes):
        raise ValueError("缺少同列玩家姓名回顯邊界")
    input_left = min(int(record["column"]) * 8 for record in echoes)
    if x + width > input_left:
        raise ValueError("姓名提示矩形覆蓋玩家輸入欄")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("rects_path", "events_path", "translations_path", "inventory_path", "edit_path"):
        parser.add_argument(name, type=Path)
    validate(**vars(parser.parse_args()))
