#!/usr/bin/env python3
"""Verify direct runtime menu display-request metadata without text leakage."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import menu_events


TOP_FIELDS = {
    "state_start", "stopped_at", "bios_input", "events", "requests", "catalog_misses",
}
EVENT_FIELDS = {
    "entry_step", "post_call_step", "caller", "original_length", "original_sha256",
    "background", "foreground", "row", "column",
}
REQUEST_FIELDS = {"event_key", "text_key", "translation_runes"}


def verify(receipt_path: Path, events_path: Path, catalog_path: Path) -> None:
    menu_events.validate(events_path, catalog_path)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if set(receipt) != TOP_FIELDS:
        raise ValueError("request receipt: 頂層欄位不符")
    if receipt["bios_input"] != "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)":
        raise ValueError("request receipt: BIOS 輸入不符")
    if receipt["catalog_misses"] != 0:
        raise ValueError("request receipt: catalog miss 必須為 0")

    with events_path.open(encoding="utf-8", newline="") as stream:
        identities = list(csv.DictReader(stream, delimiter="\t"))
    with catalog_path.open(encoding="utf-8", newline="") as stream:
        translations = {row["key"]: row["translation"] for row in csv.DictReader(stream, delimiter="\t")}
    events, requests = receipt["events"], receipt["requests"]
    if len(events) != len(identities) or len(requests) != len(identities):
        raise ValueError("request receipt: 事件或請求數不符")

    previous_post = 0
    for index, (event, request, identity) in enumerate(zip(events, requests, identities), 1):
        if set(event) != EVENT_FIELDS or set(request) != REQUEST_FIELDS:
            raise ValueError(f"request receipt: 第 {index} 筆欄位不符")
        caller = event["caller"]
        if set(caller) != {"segment", "offset"}:
            raise ValueError(f"request receipt: 第 {index} 筆 caller 欄位不符")
        expected_event = {
            "original_length": int(identity["original_length"]),
            "original_sha256": identity["original_sha256"],
            "background": int(identity["background"]),
            "foreground": int(identity["foreground"]),
            "row": int(identity["row"]),
            "column": int(identity["column"]),
        }
        if f'{caller["segment"]:04X}:{caller["offset"]:04X}' != identity["caller"]:
            raise ValueError(f"request receipt: 第 {index} 筆 caller 不符")
        for field, expected in expected_event.items():
            if event[field] != expected:
                raise ValueError(f"request receipt: 第 {index} 筆 {field} 不符")
        if not previous_post < event["entry_step"] < event["post_call_step"]:
            raise ValueError(f"request receipt: 第 {index} 筆 guarded post-call 順序不符")
        previous_post = event["post_call_step"]

        if request["event_key"] != identity["event_key"] or request["text_key"] != identity["text_key"]:
            raise ValueError(f"request receipt: 第 {index} 筆 key 不符")
        if request["translation_runes"] != len(translations[identity["text_key"]]):
            raise ValueError(f"request receipt: 第 {index} 筆譯文字數不符")

    if not receipt["state_start"] < events[0]["entry_step"] or receipt["stopped_at"] < previous_post:
        raise ValueError("request receipt: 執行範圍不包含全部事件")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("events", type=Path)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    verify(args.receipt, args.events, args.catalog)
