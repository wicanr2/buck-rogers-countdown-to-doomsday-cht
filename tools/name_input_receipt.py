#!/usr/bin/env python3
"""驗證角色姓名編輯與確認分支的決定性收據。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import post_class_receipt
import reroll_lifecycle_receipt


STATE_SHA = post_class_receipt.STATE_SHA
START_SHA = post_class_receipt.START_SHA
GAME_SHA = post_class_receipt.GAME_SHA
COMMAND_SHA = post_class_receipt.COMMAND_SHA
BASELINE_SHA = reroll_lifecycle_receipt.NO_RECEIPT_SHA
EDIT_RECEIPT_SHA = "863440bcee78552f70d86cc1d086ef5953d6f993ceaa3798cfc48170060ee9e3"
EDIT_SCREEN_SHA = "bd3d779926df3b0e2979f5317f718480057bc01f36768610ac1378aa4c8feec6"
CONFIRM_RECEIPT_SHA = "52e50460281115f677e0ab73dc94c206a8d7af5d6713977d912d28ecd4281d3d"
CONFIRM_SCREEN_SHA = "a1cd728cecaa720357f680f2be66e857f401ee5b0113f9959b23143e0fae95f7"
TOP_FIELDS = {"state_start", "stopped_at", "events", "bios_keys"}
EDIT_ROLES = {"input_echo"}
CONFIRM_ROLES = {"input_echo", "skill_allocation_screen"}
PREFIX_KEYS = reroll_lifecycle_receipt.PREFIX_KEYS + [
    {"queued_at": 101_400_000, "scan": 49, "ascii": 110},
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_branch(receipt: dict, baseline_events: list[dict], rows: list[dict[str, str]],
                     suffix_keys: list[dict[str, int]]) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 103_000_000:
        raise ValueError("name input receipt: 頂層或執行範圍不符")
    if receipt["bios_keys"] != PREFIX_KEYS + suffix_keys:
        raise ValueError("name input receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 183 + len(rows) or events[:183] != baseline_events:
        raise ValueError("name input receipt: 基線或事件數不符")
    for index, (event, row) in enumerate(zip(events[183:], rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not post_class_receipt._event_matches(event, row)):
            raise ValueError(f"name input receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(edit_a: Path, edit_b: Path, edit_screen_a: Path, edit_screen_b: Path,
           confirm_a: Path, confirm_b: Path, confirm_screen_a: Path, confirm_screen_b: Path,
           baseline: Path, state: Path, start_exe: Path, game_ovr: Path, command: Path,
           edit_inventory: Path, confirm_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command"),
                                  (baseline, BASELINE_SHA, "baseline")):
        if _sha(path) != expected:
            raise ValueError(f"name input receipt: {label} SHA-256 不符")
    baseline_events = json.loads(baseline.read_bytes())["events"]
    if len(baseline_events) != 183:
        raise ValueError("name input receipt: baseline 事件數不符")
    edit_rows = reroll_lifecycle_receipt._read_inventory(edit_inventory, 2, EDIT_ROLES)
    confirm_rows = reroll_lifecycle_receipt._read_inventory(confirm_inventory, 43, CONFIRM_ROLES)
    cases = [
        (edit_a, edit_b, edit_screen_a, edit_screen_b, EDIT_RECEIPT_SHA, EDIT_SCREEN_SHA, edit_rows,
         [{"queued_at": 102_050_000, "scan": 30, "ascii": 97},
          {"queued_at": 102_150_000, "scan": 48, "ascii": 98},
          {"queued_at": 102_250_000, "scan": 14, "ascii": 8}]),
        (confirm_a, confirm_b, confirm_screen_a, confirm_screen_b, CONFIRM_RECEIPT_SHA, CONFIRM_SCREEN_SHA,
         confirm_rows, [{"queued_at": 102_050_000, "scan": 30, "ascii": 97},
                        {"queued_at": 102_150_000, "scan": 28, "ascii": 13}]),
    ]
    for receipt_a, receipt_b, screen_a, screen_b, receipt_sha, screen_sha, rows, keys in cases:
        raw_a, raw_b = receipt_a.read_bytes(), receipt_b.read_bytes()
        if raw_a != raw_b or hashlib.sha256(raw_a).hexdigest() != receipt_sha:
            raise ValueError("name input receipt: JSON 重播或固定 SHA-256 不符")
        try:
            receipt = json.loads(raw_a)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("name input receipt: 不是有效 UTF-8 JSON") from exc
        _validate_branch(receipt, baseline_events, rows, keys)
        screen_raw_a, screen_raw_b = screen_a.read_bytes(), screen_b.read_bytes()
        if (len(screen_raw_a) != 64_000 or screen_raw_a != screen_raw_b or
                hashlib.sha256(screen_raw_a).hexdigest() != screen_sha):
            raise ValueError("name input receipt: framebuffer 重播、尺寸或 SHA-256 不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("edit_a", "edit_b", "edit_screen_a", "edit_screen_b", "confirm_a", "confirm_b",
                 "confirm_screen_a", "confirm_screen_b", "baseline", "state", "start_exe", "game_ovr",
                 "command", "edit_inventory", "confirm_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
