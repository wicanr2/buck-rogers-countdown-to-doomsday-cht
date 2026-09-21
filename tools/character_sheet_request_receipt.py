#!/usr/bin/env python3
"""驗證角色資料靜態繁中 request 的雙重決定性與非干擾收據。"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import character_sheet_events

BASE_JSON_SHA = "8a9759ef0337cc9dbbef8b6dd7ad21572dda1a4d3d033ca5b8a086615193e7fc"
BASE_SCREEN_SHA = "1f3b81946cc058d89a8ecfd9ca5aab8e7fb2aaa5d95c2c2ecbd49c219f51d4dd"
Y_JSON_SHA = "19702fb12197e91673189153bf5354e7eaa733002ba5796e0ee98d5b11f96f41"
Y_SCREEN_SHA = "03d9bf1fcdd871055949c5545eaf102fecb7aa6ef0f3b3e09a2dcf6e95050f97"
EVENT_FIELDS = {"entry_step", "post_call_step", "caller", "original_length", "original_sha256",
                "background", "foreground", "row", "column"}
REQUEST_FIELDS = {"event_key", "text_key", "translation_runes"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(row):
    return (int(row["original_length"]), row["original_sha256"], row["caller"],
            int(row["background"]), int(row["foreground"]), int(row["row"]), int(row["column"]))


def event_identity(event):
    caller = event["caller"]
    return (event["original_length"], event["original_sha256"],
            f'{caller["segment"]:04X}:{caller["offset"]:04X}', event["background"],
            event["foreground"], event["row"], event["column"])


def verify(receipt_a: Path, receipt_b: Path, screen_a: Path, screen_b: Path,
           events_path: Path, translations_path: Path, inventory_path: Path, branch: str) -> None:
    character_sheet_events.validate(events_path, translations_path, inventory_path)
    if branch not in {"base", "y"}:
        raise ValueError("branch 必須是 base 或 y")
    expected_json = BASE_JSON_SHA if branch == "base" else Y_JSON_SHA
    expected_screen = BASE_SCREEN_SHA if branch == "base" else Y_SCREEN_SHA
    expected_counts = (118, 43, 75, 4) if branch == "base" else (149, 52, 97, 5)
    if receipt_a.read_bytes() != receipt_b.read_bytes() or sha(receipt_a) != expected_json:
        raise ValueError("JSON 收據不決定或固定雜湊不符")
    if screen_a.read_bytes() != screen_b.read_bytes() or sha(screen_a) != expected_screen:
        raise ValueError("framebuffer 不決定或原版固定雜湊不符")
    data = json.loads(receipt_a.read_text(encoding="utf-8"))
    if set(data) != {"state_start", "stopped_at", "events", "requests", "catalog_misses", "bios_keys"}:
        raise ValueError("頂層欄位不符")
    events_n, requests_n, misses_n, keys_n = expected_counts
    if (data["state_start"], data["stopped_at"], len(data["events"]), len(data["requests"]),
            data["catalog_misses"], len(data["bios_keys"])) != (99_999_999, 102_000_000,
                                                               events_n, requests_n, misses_n, keys_n):
        raise ValueError("執行範圍或計數不符")
    with events_path.open(encoding="utf-8", newline="") as stream:
        catalog = {identity(row): row for row in csv.DictReader(stream, delimiter="\t")}
    with translations_path.open(encoding="utf-8", newline="") as stream:
        translations = {row["key"]: row["translation"] for row in csv.DictReader(stream, delimiter="\t")}
    expected = []
    for event in data["events"]:
        if set(event) != EVENT_FIELDS:
            raise ValueError("事件欄位不符")
        row = catalog.get(event_identity(event))
        if row:
            expected.append({"event_key": row["event_key"], "text_key": row["text_key"],
                             "translation_runes": len(translations[row["text_key"]])})
    if data["requests"] != expected or any(set(row) != REQUEST_FIELDS for row in data["requests"]):
        raise ValueError("request 與 exact event 順序不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("receipt_a", "receipt_b", "screen_a", "screen_b", "events_path", "translations_path",
                 "inventory_path"):
        parser.add_argument(name, type=Path)
    parser.add_argument("branch", choices=("base", "y"))
    verify(**vars(parser.parse_args()))
