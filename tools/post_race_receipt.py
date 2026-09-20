#!/usr/bin/env python3
"""Verify deterministic, content-safe text receipts after selecting the default race."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import menu_events
import race_selection_receipt


STATE_SHA = "cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164"
START_SHA = "58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1"
GAME_SHA = "3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0"
COMMAND_SHA = "8ce3a79a791659f72f4fa4190274155462ce701431bf11c8d7da7ee8ae291506"
RECEIPT_SHA = "0c24a9fa56f5815bfed35b9ebff1ca219d10931beafaed16ed57a99eabbb7dab"
SCREEN_SHA = "dcf947d18c85b051ec85e1bc968f30cec5c315a9158d598055d14ebfe82a715c"

TOP_FIELDS = {"state_start", "stopped_at", "bios_input", "events", "bios_keys"}
EVENT_FIELDS = {
    "entry_step", "post_call_step", "caller", "original_length", "original_sha256",
    "background", "foreground", "row", "column",
}
INVENTORY_HEADER = [
    "event_key", "sequence", "text_key", "original_length", "original_sha256",
    "caller", "background", "foreground", "row", "column",
]
ENTRY_STEPS = [
    100010490, 100033190, 100059989, 100086713, 100113524, 100140424, 100167402,
    100194132, 100221773, 100240522, 100250787, 100277753, 100304303, 100331347,
]
POST_STEPS = [
    100025943, 100040266, 100066316, 100093802, 100121377, 100149030, 100173735,
    100205792, 100226552, 100245301, 100259380, 100282556, 100310629, 100334602,
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_inventory(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("post-race inventory: 不得含 UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("post-race inventory: 不是有效 UTF-8") from exc
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    if reader.fieldnames != INVENTORY_HEADER:
        raise ValueError("post-race inventory: header 不符")
    rows = list(reader)
    if len(rows) != 4 or any(set(row) != set(INVENTORY_HEADER) for row in rows):
        raise ValueError("post-race inventory: 必須恰有四筆完整事件")
    if [row["sequence"] for row in rows] != ["1", "2", "3", "4"]:
        raise ValueError("post-race inventory: sequence 不連續")
    if len({row["event_key"] for row in rows}) != 4:
        raise ValueError("post-race inventory: event key 不唯一")
    return rows


def _validate_receipt(receipt: dict, menu_rows: list[dict[str, str]], post_rows: list[dict[str, str]]) -> None:
    if set(receipt) != TOP_FIELDS:
        raise ValueError("post-race receipt: 頂層欄位不符")
    if receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 101_000_000:
        raise ValueError("post-race receipt: 執行範圍不符")
    if receipt["bios_input"] != "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)":
        raise ValueError("post-race receipt: 相容 Enter metadata 不符")
    if receipt["bios_keys"] != [
        {"queued_at": 100_010_000, "scan": 0x1C, "ascii": 0x0D},
        {"queued_at": 100_240_000, "scan": 0x1C, "ascii": 0x0D},
    ]:
        raise ValueError("post-race receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 14:
        raise ValueError("post-race receipt: 必須恰有十四事件")
    expected_rows = menu_rows[:10] + post_rows
    previous = -1
    for index, (event, row, entry, post) in enumerate(
        zip(events, expected_rows, ENTRY_STEPS, POST_STEPS), 1
    ):
        if set(event) != EVENT_FIELDS:
            raise ValueError(f"post-race receipt: 第 {index} 筆 schema 不符")
        if event["entry_step"] != entry or event["post_call_step"] != post:
            raise ValueError(f"post-race receipt: 第 {index} 筆絕對 step 不符")
        if not previous < entry < post:
            raise ValueError(f"post-race receipt: 第 {index} 筆時序不遞增")
        if not race_selection_receipt._event_matches(event, row):
            raise ValueError(f"post-race receipt: 第 {index} 筆 identity 不符")
        previous = post


def verify(
    receipt_a: Path, receipt_b: Path, screen_a: Path, screen_b: Path,
    state: Path, start_exe: Path, game_ovr: Path, command: Path,
    menu_inventory: Path, menu_catalog: Path, post_inventory: Path,
) -> None:
    expected_hashes = [
        (state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
        (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "receipt command"),
    ]
    for path, expected, label in expected_hashes:
        if _sha(path) != expected:
            raise ValueError(f"post-race receipt: {label} SHA-256 不符")
    raw_a, raw_b = receipt_a.read_bytes(), receipt_b.read_bytes()
    if raw_a != raw_b or hashlib.sha256(raw_a).hexdigest() != RECEIPT_SHA:
        raise ValueError("post-race receipt: JSON 重播或固定 SHA-256 不符")
    screen_raw_a, screen_raw_b = screen_a.read_bytes(), screen_b.read_bytes()
    if len(screen_raw_a) != 320 * 200 or screen_raw_a != screen_raw_b or hashlib.sha256(screen_raw_a).hexdigest() != SCREEN_SHA:
        raise ValueError("post-race receipt: framebuffer 重播、尺寸或 SHA-256 不符")
    menu_events.validate(menu_inventory, menu_catalog)
    with menu_inventory.open(encoding="utf-8", newline="") as stream:
        menu_rows = list(csv.DictReader(stream, delimiter="\t"))
    post_rows = _read_inventory(post_inventory)
    try:
        receipt = json.loads(raw_a)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("post-race receipt: 不是有效 UTF-8 JSON") from exc
    _validate_receipt(receipt, menu_rows, post_rows)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    for name in (
        "receipt_a", "receipt_b", "screen_a", "screen_b", "state", "start_exe", "game_ovr",
        "command", "menu_inventory", "menu_catalog", "post_inventory",
    ):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    verify(**vars(args))
