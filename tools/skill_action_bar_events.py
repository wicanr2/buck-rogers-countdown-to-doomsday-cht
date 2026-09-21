#!/usr/bin/env python3
"""驗證技能配置底部操作列的 content-safe 事件清冊。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


HEADER = [
    "screen", "key", "original_length", "original_sha256", "row", "column",
    "x0", "y0", "x1", "y1", "normal_first_caller", "normal_rest_caller",
    "normal_bg", "normal_first_fg", "normal_rest_fg", "focus_caller",
    "focus_bg", "focus_fg", "evidence_level", "disabled_state",
]
EXPECTED = {
    ("career", "action.add"): (3, 0, 24),
    ("career", "action.subtract"): (8, 4, 96),
    ("career", "action.done"): (4, 13, 136),
    ("technical", "action.add"): (3, 0, 24),
    ("technical", "action.subtract"): (8, 4, 96),
    ("technical", "action.prev"): (4, 13, 136),
    ("technical", "action.next"): (4, 18, 176),
    ("technical", "action.done"): (4, 23, 216),
}


def validate(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != HEADER:
            raise ValueError("欄位不符合固定 schema")
        rows = list(reader)
    found = {(row["screen"], row["key"]): row for row in rows}
    if set(found) != set(EXPECTED) or len(rows) != len(found):
        raise ValueError("畫面與 key 覆蓋不完整或重複")
    for identity, (length, column, x1) in EXPECTED.items():
        row = found[identity]
        numbers = {name: int(row[name]) for name in (
            "original_length", "row", "column", "x0", "y0", "x1", "y1",
            "normal_bg", "normal_first_fg", "normal_rest_fg", "focus_bg", "focus_fg",
        )}
        if len(row["original_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in row["original_sha256"]):
            raise ValueError(f"{identity}: SHA-256 格式錯誤")
        if (numbers["original_length"], numbers["column"], numbers["x1"]) != (length, column, x1):
            raise ValueError(f"{identity}: 長度或定位漂移")
        if (numbers["row"], numbers["x0"], numbers["y0"], numbers["y1"]) != (24, column * 8, 192, 200):
            raise ValueError(f"{identity}: 安全矩形漂移")
        if row["normal_first_caller"] != "37F1:0391" or row["normal_rest_caller"] != "37F1:03CE":
            raise ValueError(f"{identity}: 一般狀態 caller 漂移")
        if row["focus_caller"] != "37F1:0337":
            raise ValueError(f"{identity}: 焦點 caller 漂移")
        if (numbers["normal_bg"], numbers["normal_first_fg"], numbers["normal_rest_fg"]) != (0, 15, 10):
            raise ValueError(f"{identity}: 一般狀態色彩漂移")
        if (numbers["focus_bg"], numbers["focus_fg"]) != (15, 0):
            raise ValueError(f"{identity}: 焦點色彩漂移")
        if row["evidence_level"] != "confirmed" or row["disabled_state"] != "unknown":
            raise ValueError(f"{identity}: 證據分級漂移")
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    print(f"validated {validate(args.catalog)} skill action-bar events")


if __name__ == "__main__":
    main()
