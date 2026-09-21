#!/usr/bin/env python3
"""驗證姓名提示 exact catalog，並以 reroll-no inventory 排除玩家輸入。"""

from __future__ import annotations

import csv
from pathlib import Path
import re
import unicodedata

EVENT_HEADER = ["event_key", "sequence", "text_key", "original_length", "original_sha256",
                "caller", "background", "foreground", "row", "column"]
TEXT_HEADER = ["key", "translation", "source"]
INVENTORY_HEADER = ["event_key", "sequence", "event_role", "inference_level", "entry_step",
                    "post_call_step", "original_length", "original_sha256", "caller", "background",
                    "foreground", "row", "column"]
IDENTITY = ["original_length", "original_sha256", "caller", "background", "foreground", "row", "column"]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")


def table(path: Path, header: list[str], label: str) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{label}: 不得含 BOM")
    try:
        rows = list(csv.reader(raw.decode("utf-8").splitlines(), delimiter="\t"))
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label}: 不是有效 UTF-8") from exc
    if not rows or rows[0] != header or any(len(row) != len(header) for row in rows[1:]):
        raise ValueError(f"{label}: schema 不符")
    return [dict(zip(header, row)) for row in rows[1:]]


def validate(events_path: Path, translations_path: Path, inventory_path: Path) -> None:
    events = table(events_path, EVENT_HEADER, "name-prompt-events.tsv")
    texts = table(translations_path, TEXT_HEADER, "name-prompt.zh-TW.tsv")
    inventory = table(inventory_path, INVENTORY_HEADER, "reroll-no-events.tsv")
    prompts = [row for row in inventory if row["event_role"] == "name_prompt"]
    if len(events) != 1 or len(texts) != 1 or len(prompts) != 1:
        raise ValueError("姓名提示事件、譯文與來源必須各恰有一筆")
    event, text, source = events[0], texts[0], prompts[0]
    if event["sequence"] != "1" or event["event_key"] != "character.name.prompt":
        raise ValueError("姓名提示 sequence 或 event key 不符")
    if event["text_key"] != text["key"] or text["key"] != "character.name.prompt":
        raise ValueError("姓名提示文字鍵未雙向對齊")
    if any(event[field] != source[field] for field in IDENTITY):
        raise ValueError("姓名提示 identity 不符原始清冊")
    if not HASH_RE.fullmatch(event["original_sha256"]) or not CALLER_RE.fullmatch(event["caller"]):
        raise ValueError("姓名提示 hash 或 caller 格式不符")
    if text["source"] != "runtime-interface" or not text["translation"]:
        raise ValueError("姓名提示譯文或來源無效")
    if unicodedata.normalize("NFC", text["translation"]) != text["translation"]:
        raise ValueError("姓名提示譯文必須是 NFC")
    if any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text["translation"]):
        raise ValueError("姓名提示譯文不得含控制或格式字元")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("events", type=Path)
    parser.add_argument("translations", type=Path)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    validate(args.events, args.translations, args.inventory)
