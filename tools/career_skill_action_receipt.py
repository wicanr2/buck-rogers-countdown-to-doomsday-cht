#!/usr/bin/env python3
"""驗證職業技能點可逆減點與確認離開分支的決定性收據。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import career_skill_receipt
import post_class_receipt
import reroll_lifecycle_receipt


STATE_SHA = career_skill_receipt.STATE_SHA
START_SHA = career_skill_receipt.START_SHA
GAME_SHA = career_skill_receipt.GAME_SHA
COMMAND_SHA = career_skill_receipt.COMMAND_SHA
BASELINE_SHA = career_skill_receipt.BASELINE_SHA
SUBTRACT_RECEIPT_SHA = "b513aae816eb49fbd42d912451a22860e6a27f9fdb0dc3e8e4056f6e60783cd3"
SUBTRACT_SCREEN_SHA = "5dc661e499e1b37fbcadf5241e162b8747ebf9b0899d2dc3d8ff531e3153c195"
EXIT_RECEIPT_SHA = "68c586e4e4f47e14adf440d92c1fefcdaa60181e2deb8001a381978679cbf5b1"
EXIT_SCREEN_SHA = "6bf7f9bb55720d24d2193bd1bffcc4abedd7278eb291db4d37398888c183432a"
TOP_FIELDS = {"state_start", "stopped_at", "events", "bios_keys"}
SUBTRACT_ROLES = {"add_redraw", "subtract_redraw"}
EXIT_ROLES = {"exit_confirmation_prompt", "technical_skill_screen"}
PREFIX_KEYS = career_skill_receipt.PREFIX_KEYS


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_branch(receipt: dict, baseline_events: list[dict], rows: list[dict[str, str]],
                     suffix_keys: list[dict[str, int]], stopped_at: int) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != stopped_at:
        raise ValueError("career skill action receipt: 頂層或執行範圍不符")
    if receipt["bios_keys"] != PREFIX_KEYS + suffix_keys:
        raise ValueError("career skill action receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 226 + len(rows) or events[:226] != baseline_events:
        raise ValueError("career skill action receipt: 基線或事件數不符")
    for index, (event, row) in enumerate(zip(events[226:], rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not post_class_receipt._event_matches(event, row)):
            raise ValueError(f"career skill action receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(subtract_a: Path, subtract_b: Path, subtract_screen_a: Path, subtract_screen_b: Path,
           exit_a: Path, exit_b: Path, exit_screen_a: Path, exit_screen_b: Path,
           baseline: Path, right_reference: Path, state: Path, start_exe: Path, game_ovr: Path,
           command: Path, subtract_inventory: Path, exit_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command"),
                                  (baseline, BASELINE_SHA, "baseline"),
                                  (right_reference, SUBTRACT_SCREEN_SHA, "right reference")):
        if _sha(path) != expected:
            raise ValueError(f"career skill action receipt: {label} SHA-256 不符")
    baseline_events = json.loads(baseline.read_bytes())["events"]
    if len(baseline_events) != 226:
        raise ValueError("career skill action receipt: baseline 事件數不符")
    subtract_rows = reroll_lifecycle_receipt._read_inventory(
        subtract_inventory, 10, SUBTRACT_ROLES)
    exit_rows = reroll_lifecycle_receipt._read_inventory(exit_inventory, 63, EXIT_ROLES)
    cases = [
        (subtract_a, subtract_b, subtract_screen_a, subtract_screen_b, SUBTRACT_RECEIPT_SHA,
         SUBTRACT_SCREEN_SHA, subtract_rows,
         [{"queued_at": 102_700_000, "scan": 28, "ascii": 13},
          {"queued_at": 102_800_000, "scan": 77, "ascii": 0},
          {"queued_at": 102_900_000, "scan": 28, "ascii": 13}], 104_000_000),
        (exit_a, exit_b, exit_screen_a, exit_screen_b, EXIT_RECEIPT_SHA, EXIT_SCREEN_SHA, exit_rows,
         [{"queued_at": 102_700_000, "scan": 1, "ascii": 27},
          {"queued_at": 102_900_000, "scan": 21, "ascii": 121}], 105_000_000),
    ]
    for receipt_a, receipt_b, screen_a, screen_b, receipt_sha, screen_sha, rows, keys, stopped_at in cases:
        raw_a, raw_b = receipt_a.read_bytes(), receipt_b.read_bytes()
        if raw_a != raw_b or hashlib.sha256(raw_a).hexdigest() != receipt_sha:
            raise ValueError("career skill action receipt: JSON 重播或固定 SHA-256 不符")
        try:
            receipt = json.loads(raw_a)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("career skill action receipt: 不是有效 UTF-8 JSON") from exc
        _validate_branch(receipt, baseline_events, rows, keys, stopped_at)
        screen_raw_a, screen_raw_b = screen_a.read_bytes(), screen_b.read_bytes()
        if (len(screen_raw_a) != 64_000 or screen_raw_a != screen_raw_b or
                hashlib.sha256(screen_raw_a).hexdigest() != screen_sha):
            raise ValueError("career skill action receipt: framebuffer 重播、尺寸或 SHA-256 不符")
        if receipt_a == subtract_a and screen_raw_a != right_reference.read_bytes():
            raise ValueError("career skill action receipt: 減點終點未回到零點／Right 選取畫面")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("subtract_a", "subtract_b", "subtract_screen_a", "subtract_screen_b",
                 "exit_a", "exit_b", "exit_screen_a", "exit_screen_b", "baseline",
                 "right_reference", "state", "start_exe", "game_ovr", "command",
                 "subtract_inventory", "exit_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
