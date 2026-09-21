#!/usr/bin/env python3
"""驗證技能操作列事件與繁中顯示文字的雙向覆蓋。"""

from __future__ import annotations

import argparse
import csv
import unicodedata
from pathlib import Path

from skill_action_bar_events import EXPECTED, validate as validate_events

TEXTS = {
    "action.add": "(A)加點",
    "action.subtract": "(S)減點",
    "action.prev": "(P)上頁",
    "action.next": "(N)下頁",
    "action.done": "(D)完成",
}


def validate(events: Path, translations: Path) -> tuple[int, int]:
    event_count = validate_events(events)
    with translations.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != ["key", "translation", "source"]:
            raise ValueError("譯文欄位不符合固定 schema")
        rows = list(reader)
    found = {row["key"]: row for row in rows}
    if len(found) != len(rows) or found.keys() != TEXTS.keys():
        raise ValueError("譯文 key 重複、缺漏或有孤兒")
    for key, expected in TEXTS.items():
        row = found[key]
        text = row["translation"]
        if text != expected or unicodedata.normalize("NFC", text) != text:
            raise ValueError(f"{key}: 譯文或 NFC 漂移")
        if row["source"] != "runtime-interface" or any(unicodedata.category(c) in {"Cc", "Cf"} for c in text):
            raise ValueError(f"{key}: 來源或控制字元漂移")
    event_keys = {key for _, key in EXPECTED}
    if event_keys != set(TEXTS):
        raise ValueError("事件與譯文未雙向覆蓋")
    return event_count, len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("events", type=Path)
    parser.add_argument("translations", type=Path)
    args = parser.parse_args()
    print("validated %d events and %d translations" % validate(args.events, args.translations))


if __name__ == "__main__":
    main()
