#!/usr/bin/env python3
"""Verify catalog-backed requests across the Enter→Down→Up runtime path."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import menu_events
import race_selection_receipt


TOP_FIELDS = {
    "state_start", "stopped_at", "bios_input", "bios_keys", "events", "requests",
    "catalog_misses",
}
REQUEST_FIELDS = {"event_key", "text_key", "translation_runes"}


def _verify_request(request: dict, identity: dict[str, str], translations: dict[str, str], index: int) -> None:
    if set(request) != REQUEST_FIELDS:
        raise ValueError(f"selection request: 第 {index} 筆欄位不符")
    if request["event_key"] != identity["event_key"] or request["text_key"] != identity["text_key"]:
        raise ValueError(f"selection request: 第 {index} 筆 key 不符")
    if request["translation_runes"] != len(translations[identity["text_key"]]):
        raise ValueError(f"selection request: 第 {index} 筆譯文字數不符")


def verify(receipt_a: Path, receipt_b: Path, menu_path: Path, selection_path: Path, catalog_path: Path) -> None:
    menu_events.validate(menu_path, catalog_path)
    with menu_path.open(encoding="utf-8", newline="") as stream:
        menu = list(csv.DictReader(stream, delimiter="\t"))
    with catalog_path.open(encoding="utf-8", newline="") as stream:
        translations = {row["key"]: row["translation"] for row in csv.DictReader(stream, delimiter="\t")}
    if len(menu) != 12:
        raise ValueError("selection request: 正式 inventory 必須恰有 12 個 identity")
    inventory = {row["event_key"]: row for row in menu}
    selection = race_selection_receipt._selection_rows(selection_path, set(translations), set(inventory))
    for row in selection:
        item = inventory[row["event_key"]]
        for name in ("text_key", "original_length", "original_sha256", "caller", "background", "foreground", "row", "column"):
            if row[name] != item[name]:
                raise ValueError(f"selection request: {row['event_key']} 不符正式 inventory")

    a = json.loads(receipt_a.read_text(encoding="utf-8"))
    b = json.loads(receipt_b.read_text(encoding="utf-8"))
    if a != b:
        raise ValueError("selection request: 兩次收據不一致")
    if set(a) != TOP_FIELDS or a["catalog_misses"] != 0:
        raise ValueError("selection request: 頂層欄位或 catalog miss 不符")
    if a["state_start"] != 99_999_999 or a["stopped_at"] != 100_600_000:
        raise ValueError("selection request: 執行範圍不符")
    if a["bios_keys"] != [
        {"queued_at": 100_010_000, "scan": 0x1C, "ascii": 0x0D},
        {"queued_at": 100_240_000, "scan": 0x50, "ascii": 0},
        {"queued_at": 100_300_000, "scan": 0x48, "ascii": 0},
    ]:
        raise ValueError("selection request: BIOS 排程不符")
    events, requests = a["events"], a["requests"]
    if len(events) != 13 or len(requests) != 13:
        raise ValueError("selection request: 必須恰有 13 events／requests")

    expected = menu[:9] + [inventory[row["event_key"]] for row in selection]
    previous_post = 0
    for index, (event, request, identity) in enumerate(zip(events, requests, expected), 1):
        if not race_selection_receipt._event_matches(event, identity):
            raise ValueError(f"selection request: 第 {index} 筆 event identity 不符")
        if not previous_post < event["entry_step"] < event["post_call_step"]:
            raise ValueError(f"selection request: 第 {index} 筆 guarded post-call 順序不符")
        previous_post = event["post_call_step"]
        _verify_request(request, identity, translations, index)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("receipt_a", type=Path)
    parser.add_argument("receipt_b", type=Path)
    parser.add_argument("menu", type=Path)
    parser.add_argument("selection", type=Path)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    verify(args.receipt_a, args.receipt_b, args.menu, args.selection, args.catalog)
