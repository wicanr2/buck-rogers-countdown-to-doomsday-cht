#!/usr/bin/env python3
"""驗證技能操作列事件與繁中顯示文字的雙向覆蓋。"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path

from catalog_lang import DEFAULT_LANG, add_lang_argument
from skill_action_bar_events import EXPECTED, validate as validate_events

TEXTS = {
    "action.add": "加點(A)",
    "action.subtract": "減點(S)",
    "action.prev": "上頁(P)",
    "action.next": "下頁(N)",
    "action.done": "完成(D)",
}


HOTKEY_RE = re.compile(r"\(([^()])\)")


def validate(events: Path, translations: Path, lang: str = DEFAULT_LANG) -> tuple[int, int]:
    """zh-TW 比對字面；其他語言（規格 041 §3.7）只查結構與恰一個 `(X)`、字母同 zh-TW。"""
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
        if unicodedata.normalize("NFC", text) != text:
            raise ValueError(f"{key}: 譯文或 NFC 漂移")
        if lang == DEFAULT_LANG:
            if text != expected:
                raise ValueError(f"{key}: 譯文或 NFC 漂移")
        elif HOTKEY_RE.findall(text) != HOTKEY_RE.findall(expected) or len(HOTKEY_RE.findall(text)) != 1:
            raise ValueError(f"{key}: (X) 熱鍵與 zh-TW 不同")
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
    add_lang_argument(parser)
    args = parser.parse_args()
    print("validated %d events and %d translations" % validate(args.events, args.translations, args.lang))


if __name__ == "__main__":
    main()
