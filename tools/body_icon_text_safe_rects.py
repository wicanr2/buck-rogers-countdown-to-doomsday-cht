#!/usr/bin/env python3
"""驗證身體圖示畫面固定文字的 logical 320x200 安全矩形。"""

from __future__ import annotations

import csv
from pathlib import Path

import body_icon_catalog
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name

HEADER = ["screen", "event_key", "x", "y", "width", "height", "draw_x", "draw_y",
          "capacity_cells", "line_count", "overflow_policy"]


def _rows(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path}: 不得含 UTF-8 BOM")
    try:
        rows = list(csv.reader(raw.decode("utf-8").splitlines(), delimiter="\t"))
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: 不是有效 UTF-8") from exc
    if not rows or rows[0] != HEADER or not rows[1:]:
        raise ValueError(f"{path}: schema 或內容不符")
    if any(len(row) != len(HEADER) or any(value == "" for value in row) for row in rows[1:]):
        raise ValueError(f"{path}: 欄位數錯誤或空欄")
    return [dict(zip(HEADER, row)) for row in rows[1:]]


def validate(rects_path: Path, events_path: Path, affixes_path: Path, translations_path: Path,
             inventory_dir: Path, lang: str = DEFAULT_LANG) -> None:
    body_icon_catalog.validate(events_path, affixes_path, translations_path, inventory_dir, lang=lang)
    rects = _rows(rects_path)
    events = body_icon_catalog.table(events_path, body_icon_catalog.EVENT_HEADER, "body-icon-events.tsv")
    catalog = body_icon_catalog.table(translations_path, body_icon_catalog.TEXT_HEADER, catalog_name("body-icon", lang))
    event_by_key = {row["event_key"]: row for row in events}
    text_by_key = {row["key"]: row for row in catalog}
    # 儲存詢問只有前綴矩形是靜態的；後綴矩形隨名字長度由 presenter 計算（規格 025）。
    affix = body_icon_catalog.table(affixes_path, body_icon_catalog.AFFIX_HEADER, "body-icon-affixes.tsv")[0]
    prefix_key = body_icon_catalog.SAVE_TEXT_KEYS[0]
    event_by_key[prefix_key] = {"column": affix["column"], "row": affix["row"],
                                "original_length": affix["prefix_length"], "text_key": prefix_key}
    if len(rects) != len(event_by_key) or {row["event_key"] for row in rects} != set(event_by_key):
        raise ValueError("身體圖示安全矩形必須與六筆事件及儲存詢問前綴一對一")
    by_screen: dict[str, list[tuple[int, int, int, int, str]]] = {}
    for rect in rects:
        key = rect["event_key"]
        if rect["screen"] not in {"confirmation", "save_prompt", "body_icon", "selection"}:
            raise ValueError(f"{key}: 未知畫面群組")
        event = event_by_key[key]
        try:
            values = [int(rect[name]) for name in HEADER[2:10]]
        except ValueError as exc:
            raise ValueError(f"{key}: 幾何欄必須是 ASCII 十進位整數") from exc
        if any(str(value) != rect[name] for value, name in zip(values, HEADER[2:10])):
            raise ValueError(f"{key}: 幾何欄必須是 canonical ASCII 十進位")
        x, y, width, height, draw_x, draw_y, capacity, lines = values
        expected = (int(event["column"]) * 8, int(event["row"]) * 8,
                    int(event["original_length"]) * 8, 8)
        if (x, y, width, height) != expected or (draw_x, draw_y) != (x, y):
            raise ValueError(f"{key}: 矩形不等於已證實原文事件幾何")
        if min(values) < 0 or x + width > 320 or y + height > 200:
            raise ValueError(f"{key}: 矩形超出 320×200 或含負值")
        if any(value % 8 for value in (x, y, width, height, draw_x, draw_y)):
            raise ValueError(f"{key}: 幾何必須對齊 8-pixel logical cell")
        if capacity != width // 8 or lines != 1 or rect["overflow_policy"] != "single-line-reject":
            raise ValueError(f"{key}: 容量、行數或 overflow policy 不符")
        if len(text_by_key[event["text_key"]]["translation"]) > capacity:
            raise ValueError(f"{key}: 繁中譯文超過單行容量")
        by_screen.setdefault(rect["screen"], []).append((x, y, x + width, y + height, key))
    for screen, items in by_screen.items():
        for index, first in enumerate(items):
            for second in items[index + 1:]:
                if (first[0] < second[2] and second[0] < first[2] and
                        first[1] < second[3] and second[1] < first[3]):
                    raise ValueError(f"{screen}: 安全矩形重疊：{first[4]}／{second[4]}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("rects_path", type=Path)
    parser.add_argument("events_path", type=Path)
    parser.add_argument("affixes_path", type=Path)
    parser.add_argument("translations_path", type=Path)
    parser.add_argument("inventory_dir", type=Path)
    add_lang_argument(parser)
    validate(**vars(parser.parse_args()))
