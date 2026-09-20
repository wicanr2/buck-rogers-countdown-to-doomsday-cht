#!/usr/bin/env python3
"""Verify a dosgolem menu text receipt against content-free identities."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import menu_events


EVENT_FIELDS = {
    "entry_step", "post_call_step", "caller", "original_length", "original_sha256",
    "background", "foreground", "row", "column",
}


def verify(receipt_path: Path, events_path: Path, catalog_path: Path) -> None:
    menu_events.validate(events_path, catalog_path)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if set(receipt) != {"state_start", "stopped_at", "bios_input", "events"}:
        raise ValueError("receipt: 頂層欄位不符")
    if receipt["bios_input"] != "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)":
        raise ValueError("receipt: BIOS 輸入不符")
    with events_path.open(encoding="utf-8", newline="") as stream:
        identities = list(csv.DictReader(stream, delimiter="\t"))
    actual = receipt["events"]
    if len(actual) != len(identities):
        raise ValueError("receipt: 事件數不符")
    previous_post = 0
    for index, (event, identity) in enumerate(zip(actual, identities), 1):
        if set(event) != EVENT_FIELDS:
            raise ValueError(f"receipt: 第 {index} 筆欄位不符")
        caller = event["caller"]
        if set(caller) != {"segment", "offset"}:
            raise ValueError(f"receipt: 第 {index} 筆 caller 欄位不符")
        caller_text = f'{caller["segment"]:04X}:{caller["offset"]:04X}'
        comparisons = {
            "original_length": int(identity["original_length"]),
            "original_sha256": identity["original_sha256"],
            "background": int(identity["background"]),
            "foreground": int(identity["foreground"]),
            "row": int(identity["row"]),
            "column": int(identity["column"]),
        }
        if caller_text != identity["caller"]:
            raise ValueError(f"receipt: 第 {index} 筆 caller 不符")
        for field, expected in comparisons.items():
            if event[field] != expected:
                raise ValueError(f"receipt: 第 {index} 筆 {field} 不符")
        if not previous_post < event["entry_step"] < event["post_call_step"]:
            raise ValueError(f"receipt: 第 {index} 筆 entry／post-call 順序不符")
        previous_post = event["post_call_step"]
    if not receipt["state_start"] < actual[0]["entry_step"] or receipt["stopped_at"] < previous_post:
        raise ValueError("receipt: 執行範圍不包含全部事件")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("events", type=Path)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    verify(args.receipt, args.events, args.catalog)
