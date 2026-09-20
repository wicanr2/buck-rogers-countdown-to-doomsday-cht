#!/usr/bin/env python3
"""驗證職業技能點選取、加點與拒絕離開的決定性收據。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import name_input_receipt
import post_class_receipt
import reroll_lifecycle_receipt


STATE_SHA = name_input_receipt.STATE_SHA
START_SHA = name_input_receipt.START_SHA
GAME_SHA = name_input_receipt.GAME_SHA
COMMAND_SHA = name_input_receipt.COMMAND_SHA
BASELINE_SHA = name_input_receipt.CONFIRM_RECEIPT_SHA
BASELINE_SCREEN_SHA = name_input_receipt.CONFIRM_SCREEN_SHA
SELECTION_RECEIPT_SHA = "655984fa3a47ad2290373d84b94dab8c16819ab8e9bf4fd6bddb002256005487"
SELECTION_SCREEN_SHA = "ddf66e0c914953ee369e93c73acdeb51d01a84e37d73cb31582ab7c77b4d6cbd"
ADD_RECEIPT_SHA = "559023d66003f9e351bcae9526b0db884fde60d007117b8da55ee79dfcd82898"
ADD_SCREEN_SHA = "3428db0d72954a4a0a3dee45b486ea0fb0cf0f505eb668429c4f7e2cc9f8c808"
REFUSAL_RECEIPT_SHA = "cd76a0e84cbccfe59e23f8766863579dae829ace53e57e71707b970567110af3"
REFUSAL_SCREEN_SHA = BASELINE_SCREEN_SHA
TOP_FIELDS = {"state_start", "stopped_at", "events", "bios_keys"}
SELECTION_ROLES = {"previous_row_redraw", "current_row_redraw"}
ADD_ROLES = {"selected_row_redraw", "remaining_points_redraw"}
REFUSAL_ROLES = {"bottom_prompt_redraw"}
PREFIX_KEYS = name_input_receipt.PREFIX_KEYS + [
    {"queued_at": 102_050_000, "scan": 30, "ascii": 97},
    {"queued_at": 102_150_000, "scan": 28, "ascii": 13},
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_branch(receipt: dict, baseline_events: list[dict], rows: list[dict[str, str]],
                     suffix_keys: list[dict[str, int]], stopped_at: int) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != stopped_at:
        raise ValueError("career skill receipt: 頂層或執行範圍不符")
    if receipt["bios_keys"] != PREFIX_KEYS + suffix_keys:
        raise ValueError("career skill receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 226 + len(rows) or events[:226] != baseline_events:
        raise ValueError("career skill receipt: 基線或事件數不符")
    for index, (event, row) in enumerate(zip(events[226:], rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not post_class_receipt._event_matches(event, row)):
            raise ValueError(f"career skill receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(selection_a: Path, selection_b: Path, selection_screen_a: Path, selection_screen_b: Path,
           add_a: Path, add_b: Path, add_screen_a: Path, add_screen_b: Path,
           refusal_a: Path, refusal_b: Path, refusal_screen_a: Path, refusal_screen_b: Path,
           baseline: Path, baseline_screen: Path, state: Path, start_exe: Path, game_ovr: Path,
           command: Path, selection_inventory: Path, add_inventory: Path, refusal_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command"),
                                  (baseline, BASELINE_SHA, "baseline"),
                                  (baseline_screen, BASELINE_SCREEN_SHA, "baseline screen")):
        if _sha(path) != expected:
            raise ValueError(f"career skill receipt: {label} SHA-256 不符")
    baseline_events = json.loads(baseline.read_bytes())["events"]
    if len(baseline_events) != 226:
        raise ValueError("career skill receipt: baseline 事件數不符")
    selection_rows = reroll_lifecycle_receipt._read_inventory(selection_inventory, 8, SELECTION_ROLES)
    add_rows = reroll_lifecycle_receipt._read_inventory(add_inventory, 5, ADD_ROLES)
    refusal_rows = reroll_lifecycle_receipt._read_inventory(refusal_inventory, 1, REFUSAL_ROLES)
    cases = [
        (selection_a, selection_b, selection_screen_a, selection_screen_b, SELECTION_RECEIPT_SHA,
         SELECTION_SCREEN_SHA, selection_rows, [{"queued_at": 102_700_000, "scan": 80, "ascii": 0}],
         103_000_000),
        (add_a, add_b, add_screen_a, add_screen_b, ADD_RECEIPT_SHA, ADD_SCREEN_SHA, add_rows,
         [{"queued_at": 102_700_000, "scan": 28, "ascii": 13}], 103_000_000),
        (refusal_a, refusal_b, refusal_screen_a, refusal_screen_b, REFUSAL_RECEIPT_SHA,
         REFUSAL_SCREEN_SHA, refusal_rows,
         [{"queued_at": 102_700_000, "scan": 1, "ascii": 27},
          {"queued_at": 102_900_000, "scan": 49, "ascii": 110}], 104_000_000),
    ]
    for receipt_a, receipt_b, screen_a, screen_b, receipt_sha, screen_sha, rows, keys, stopped_at in cases:
        raw_a, raw_b = receipt_a.read_bytes(), receipt_b.read_bytes()
        if raw_a != raw_b or hashlib.sha256(raw_a).hexdigest() != receipt_sha:
            raise ValueError("career skill receipt: JSON 重播或固定 SHA-256 不符")
        try:
            receipt = json.loads(raw_a)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("career skill receipt: 不是有效 UTF-8 JSON") from exc
        _validate_branch(receipt, baseline_events, rows, keys, stopped_at)
        screen_raw_a, screen_raw_b = screen_a.read_bytes(), screen_b.read_bytes()
        if (len(screen_raw_a) != 64_000 or screen_raw_a != screen_raw_b or
                hashlib.sha256(screen_raw_a).hexdigest() != screen_sha):
            raise ValueError("career skill receipt: framebuffer 重播、尺寸或 SHA-256 不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("selection_a", "selection_b", "selection_screen_a", "selection_screen_b",
                 "add_a", "add_b", "add_screen_a", "add_screen_b", "refusal_a", "refusal_b",
                 "refusal_screen_a", "refusal_screen_b", "baseline", "baseline_screen", "state",
                 "start_exe", "game_ovr", "command", "selection_inventory", "add_inventory",
                 "refusal_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
