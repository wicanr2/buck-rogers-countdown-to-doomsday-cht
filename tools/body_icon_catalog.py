#!/usr/bin/env python3
"""驗證身體圖示畫面靜態文字的 exact catalog 與既有正常路徑證據。"""

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

SOURCES = {
    "body.icon.confirmation": [("body-icon-exit-events.tsv", "body.icon.exit.confirmation.001"),
                                ("body-icon-refusal-events.tsv", "body.icon.refuse.confirmation.001")],
    "body.icon.save_prompt": [("body-icon-exit-events.tsv", "body.icon.exit.save_prompt.001")],
    "body.icon.old.label": [("body-icon-refusal-events.tsv", "body.icon.refuse.old_label.001")],
    "body.icon.old.action": [("body-icon-refusal-events.tsv", "body.icon.refuse.old_action.001")],
    "body.icon.new.label": [("body-icon-refusal-events.tsv", "body.icon.refuse.new_label.001")],
    "body.icon.new.action": [("body-icon-refusal-events.tsv", "body.icon.refuse.new_action.001")],
    "body.icon.selection.instruction": [("body-icon-move-events.tsv", "body.icon.move.instruction.001"),
                                         ("body-icon-refusal-events.tsv", "body.icon.refuse.instruction.001")],
}


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


def validate(events_path: Path, translations_path: Path, inventory_dir: Path) -> None:
    events = table(events_path, EVENT_HEADER, "body-icon-events.tsv")
    texts = table(translations_path, TEXT_HEADER, "body-icon.zh-TW.tsv")
    if len(events) != len(SOURCES) or len(texts) != len(SOURCES):
        raise ValueError("身體圖示事件與譯文必須各恰有七筆")
    event_by_key = {row["event_key"]: row for row in events}
    text_by_key = {row["key"]: row for row in texts}
    if set(event_by_key) != set(SOURCES) or set(text_by_key) != set(SOURCES):
        raise ValueError("身體圖示事件／譯文鍵值不完整或重複")
    for key, source_refs in SOURCES.items():
        event = event_by_key[key]
        text = text_by_key[key]
        if event["text_key"] != key or text["source"] != "runtime-interface" or not text["translation"]:
            raise ValueError(f"{key}: 文字鍵或來源不符")
        if not HASH_RE.fullmatch(event["original_sha256"]) or not CALLER_RE.fullmatch(event["caller"]):
            raise ValueError(f"{key}: hash 或 caller 格式不符")
        if len(text["translation"]) > int(event["original_length"]):
            raise ValueError(f"{key}: 譯文超過原文字格容量")
        if unicodedata.normalize("NFC", text["translation"]) != text["translation"]:
            raise ValueError(f"{key}: 譯文必須是 NFC")
        if any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text["translation"]):
            raise ValueError(f"{key}: 譯文不得含控制或格式字元")
        for filename, source_key in source_refs:
            rows = table(inventory_dir / filename, INVENTORY_HEADER, filename)
            matches = [row for row in rows if row["event_key"] == source_key]
            if len(matches) != 1 or any(event[field] != matches[0][field] for field in IDENTITY):
                raise ValueError(f"{key}: 未通過 {filename} 的 exact identity")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("events", type=Path)
    parser.add_argument("translations", type=Path)
    parser.add_argument("inventory_dir", type=Path)
    args = parser.parse_args()
    validate(args.events, args.translations, args.inventory_dir)
