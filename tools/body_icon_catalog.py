#!/usr/bin/env python3
"""驗證身體圖示畫面文字的 exact catalog、儲存詢問前後綴身分與既有正常路徑證據。"""

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
AFFIX_HEADER = ["event_key", "caller", "background", "foreground", "row", "column", "prefix_length",
                "prefix_sha256", "suffix_length", "suffix_sha256", "slot_min", "slot_max"]
SAVE_KEY = "body.icon.save_prompt"
SAVE_TEXT_KEYS = ("body.icon.save_prompt.prefix", "body.icon.save_prompt.suffix")
# 規格 025：儲存詢問的樣式須與既有正常路徑收據（名字 A 的 8 字版本）相同。
SAVE_SOURCE = ("body-icon-exit-events.tsv", "body.icon.exit.save_prompt.001")
# 規格 025／第二百四十四階段以四個名字的一手 dispatcher 證實的前後綴。
SAVE_PINNED = {"prefix_length": "5", "suffix_length": "2",
               "prefix_sha256": "f5f25c5769e6107d2cec7dec87265599a9af37156f30add96e2a6daa2d4a4658",
               "suffix_sha256": "23eeade931d8902dde575f26bb466a3c786484e46471efa7fa5b054636e7298b"}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")

SOURCES = {
    "body.icon.confirmation": [("body-icon-exit-events.tsv", "body.icon.exit.confirmation.001"),
                                ("body-icon-refusal-events.tsv", "body.icon.refuse.confirmation.001")],
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


def _check_text(key: str, text: dict[str, str], capacity: int) -> None:
    if text["source"] != "runtime-interface" or not text["translation"]:
        raise ValueError(f"{key}: 文字鍵或來源不符")
    if len(text["translation"]) > capacity:
        raise ValueError(f"{key}: 譯文超過原文字格容量")
    if unicodedata.normalize("NFC", text["translation"]) != text["translation"]:
        raise ValueError(f"{key}: 譯文必須是 NFC")
    if any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in text["translation"]):
        raise ValueError(f"{key}: 譯文不得含控制或格式字元")


def validate_affix(affixes_path: Path, text_by_key: dict[str, dict[str, str]], inventory_dir: Path) -> dict[str, str]:
    rows = table(affixes_path, AFFIX_HEADER, "body-icon-affixes.tsv")
    if len(rows) != 1 or rows[0]["event_key"] != SAVE_KEY:
        raise ValueError("前後綴 catalog 必須恰為儲存詢問一筆")
    affix = rows[0]
    if not CALLER_RE.fullmatch(affix["caller"]) or not HASH_RE.fullmatch(affix["prefix_sha256"]) or \
            not HASH_RE.fullmatch(affix["suffix_sha256"]) or affix["prefix_sha256"] == affix["suffix_sha256"]:
        raise ValueError(f"{SAVE_KEY}: caller 或前後綴 hash 格式不符")
    if any(affix[k] != v for k, v in SAVE_PINNED.items()):
        raise ValueError(f"{SAVE_KEY}: 前後綴身分與規格 025 已證實值不符")
    try:
        prefix, suffix, lo, hi, column = (int(affix[k]) for k in ("prefix_length", "suffix_length", "slot_min", "slot_max", "column"))
    except ValueError as exc:
        raise ValueError(f"{SAVE_KEY}: 長度欄必須是整數") from exc
    if prefix <= 0 or suffix <= 0 or lo < 1 or hi < lo or column + prefix + hi + suffix > 40:
        raise ValueError(f"{SAVE_KEY}: 前後綴或名字長度範圍不符")
    filename, source_key = SAVE_SOURCE
    matches = [row for row in table(inventory_dir / filename, INVENTORY_HEADER, filename) if row["event_key"] == source_key]
    if len(matches) != 1 or any(affix[f] != matches[0][f] for f in ("caller", "background", "foreground", "row", "column")) or \
            not lo <= int(matches[0]["original_length"]) - prefix - suffix <= hi:
        raise ValueError(f"{SAVE_KEY}: 未通過 {filename} 的樣式與長度對照")
    for key, capacity in zip(SAVE_TEXT_KEYS, (prefix, suffix)):
        _check_text(key, text_by_key[key], capacity)
    return affix


def validate(events_path: Path, affixes_path: Path, translations_path: Path, inventory_dir: Path) -> None:
    events = table(events_path, EVENT_HEADER, "body-icon-events.tsv")
    texts = table(translations_path, TEXT_HEADER, "body-icon.zh-TW.tsv")
    if len(events) != len(SOURCES) or len(texts) != len(SOURCES) + len(SAVE_TEXT_KEYS):
        raise ValueError("身體圖示事件須恰有六筆、譯文須恰有八筆")
    event_by_key = {row["event_key"]: row for row in events}
    text_by_key = {row["key"]: row for row in texts}
    if set(event_by_key) != set(SOURCES) or set(text_by_key) != set(SOURCES) | set(SAVE_TEXT_KEYS):
        raise ValueError("身體圖示事件／譯文鍵值不完整或重複")
    for index, row in enumerate(events):
        if row["sequence"] != str(index + 1):
            raise ValueError(f"{row['event_key']}: sequence 必須連號")
    validate_affix(affixes_path, text_by_key, inventory_dir)
    for key, source_refs in SOURCES.items():
        event = event_by_key[key]
        text = text_by_key[key]
        if event["text_key"] != key:
            raise ValueError(f"{key}: 文字鍵或來源不符")
        if not HASH_RE.fullmatch(event["original_sha256"]) or not CALLER_RE.fullmatch(event["caller"]):
            raise ValueError(f"{key}: hash 或 caller 格式不符")
        _check_text(key, text, int(event["original_length"]))
        for filename, source_key in source_refs:
            rows = table(inventory_dir / filename, INVENTORY_HEADER, filename)
            matches = [row for row in rows if row["event_key"] == source_key]
            if len(matches) != 1 or any(event[field] != matches[0][field] for field in IDENTITY):
                raise ValueError(f"{key}: 未通過 {filename} 的 exact identity")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("events", type=Path)
    parser.add_argument("affixes", type=Path)
    parser.add_argument("translations", type=Path)
    parser.add_argument("inventory_dir", type=Path)
    args = parser.parse_args()
    validate(args.events, args.affixes, args.translations, args.inventory_dir)
