#!/usr/bin/env python3
"""驗證角色資料靜態事件與繁中 catalog，並排除動態值。"""

from __future__ import annotations

import csv
from pathlib import Path
import re

EVENT_HEADER = ["event_key", "sequence", "text_key", "original_length", "original_sha256",
                "caller", "background", "foreground", "row", "column"]
TEXT_HEADER = ["key", "translation", "source"]
INVENTORY_HEADER = ["event_key", "sequence", "event_role", "inference_level", "entry_step",
                    "post_call_step", "original_length", "original_sha256", "caller", "background",
                    "foreground", "row", "column"]
IDENTITY = ["original_length", "original_sha256", "caller", "background", "foreground", "row", "column"]
STATIC_ROLES = {"static_label", "ability_label", "skill_label", "reroll_prompt"}
FORBIDDEN_DYNAMIC_ROLES = {"empty_dynamic_value", "identity_value", "ability_placeholder",
                           "summary_value", "skill_value", "ability_rerolled_value"}
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
    events = table(events_path, EVENT_HEADER, "character-sheet-events.tsv")
    texts = table(translations_path, TEXT_HEADER, "character-sheet.zh-TW.tsv")
    inventory = table(inventory_path, INVENTORY_HEADER, "post-class-events.tsv")
    static = [row for row in inventory if row["event_role"] in STATIC_ROLES]
    if len(events) != 35 or len(texts) != 35 or len(static) != 35:
        raise ValueError("角色資料靜態事件／譯文必須各有 35 筆")
    if [row["sequence"] for row in events] != [str(i) for i in range(1, 36)]:
        raise ValueError("事件 sequence 必須從 1 連續")
    if len({row["event_key"] for row in events}) != 35 or len({tuple(row[x] for x in IDENTITY) for row in events}) != 35:
        raise ValueError("event key 或 identity 不唯一")
    if len({row["key"] for row in texts}) != 35 or {row["text_key"] for row in events} != {row["key"] for row in texts}:
        raise ValueError("事件與譯文鍵必須唯一且雙向完整")
    if any(not row["translation"] or row["source"] not in {"manual-and-runtime", "runtime-interface"} for row in texts):
        raise ValueError("譯文或來源無效")
    for event, source in zip(events, static):
        if not HASH_RE.fullmatch(event["original_sha256"]) or not CALLER_RE.fullmatch(event["caller"]):
            raise ValueError("hash 或 caller 格式不符")
        if any(event[field] != source[field] for field in IDENTITY):
            raise ValueError(f"{event['event_key']}: identity 不符原始清冊")
    dynamic_ids = {tuple(row[x] for x in IDENTITY) for row in inventory
                   if row["event_role"] in FORBIDDEN_DYNAMIC_ROLES}
    if any(tuple(row[x] for x in IDENTITY) in dynamic_ids for row in events):
        raise ValueError("動態 identity 不得進入靜態 catalog")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("events", type=Path)
    parser.add_argument("translations", type=Path)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    validate(args.events, args.translations, args.inventory)
