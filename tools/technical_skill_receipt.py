#!/usr/bin/env python3
"""驗證技術技能選取、可逆減點與離開分支的決定性收據。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import career_skill_action_receipt
import post_class_receipt
import reroll_lifecycle_receipt


STATE_SHA = career_skill_action_receipt.STATE_SHA
START_SHA = career_skill_action_receipt.START_SHA
GAME_SHA = career_skill_action_receipt.GAME_SHA
COMMAND_SHA = career_skill_action_receipt.COMMAND_SHA
BASELINE_SHA = career_skill_action_receipt.EXIT_RECEIPT_SHA
BASELINE_SCREEN_SHA = career_skill_action_receipt.EXIT_SCREEN_SHA
DOWN_RECEIPT_SHA = "bc00c32cef045468893aac497bf48e9ab5195627357572aa7dd3ec8e2e11df2f"
DOWN_SCREEN_SHA = "8990a6cb2e7cb240f4e9aa3eb32e0f4fabfcedd0ec5bf994036c307bc1d0729e"
SUBTRACT_RECEIPT_SHA = "f509896457e8a3e6a4bd330d954705a5e96c91c6ba871c8d02bb9e6547d1dc22"
SUBTRACT_SCREEN_SHA = "32d71c8d84bc4c711421eb5cfff0e6bfd086233db8bd9516b4d4152e962ed057"
REFUSAL_RECEIPT_SHA = "99fee634e3f7516bc14c80fa8e61efbc6667eaf27d5e4d91a2ffbcce7eb849de"
REFUSAL_SCREEN_SHA = BASELINE_SCREEN_SHA
EXIT_RECEIPT_SHA = "e28828f173a860a9f2d28721100805abf245082af615ab593f52498bfc3210b6"
EXIT_SCREEN_SHA = "d8c15be5805741ed45cfd42fc2211ec16664499c1895e3f840072cb13eb5296f"
TOP_FIELDS = {"state_start", "stopped_at", "events", "bios_keys"}
DOWN_ROLES = {"previous_row_redraw", "current_row_redraw"}
SUBTRACT_ROLES = {"add_redraw", "subtract_redraw"}
REFUSAL_ROLES = {"exit_confirmation_prompt"}
EXIT_ROLES = {"exit_confirmation_prompt", "body_icon_screen"}
PREFIX_KEYS = career_skill_action_receipt.PREFIX_KEYS + [
    {"queued_at": 102_700_000, "scan": 1, "ascii": 27},
    {"queued_at": 102_900_000, "scan": 21, "ascii": 121},
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_branch(receipt: dict, baseline_events: list[dict], rows: list[dict[str, str]],
                     suffix_keys: list[dict[str, int]], stopped_at: int) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != stopped_at:
        raise ValueError("technical skill receipt: 頂層或執行範圍不符")
    if receipt["bios_keys"] != PREFIX_KEYS + suffix_keys:
        raise ValueError("technical skill receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 289 + len(rows) or events[:289] != baseline_events:
        raise ValueError("technical skill receipt: 基線或事件數不符")
    for index, (event, row) in enumerate(zip(events[289:], rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not post_class_receipt._event_matches(event, row)):
            raise ValueError(f"technical skill receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(down_a: Path, down_b: Path, down_screen_a: Path, down_screen_b: Path,
           subtract_a: Path, subtract_b: Path, subtract_screen_a: Path, subtract_screen_b: Path,
           refusal_a: Path, refusal_b: Path, refusal_screen_a: Path, refusal_screen_b: Path,
           exit_a: Path, exit_b: Path, exit_screen_a: Path, exit_screen_b: Path,
           baseline: Path, baseline_screen: Path, right_reference: Path, state: Path,
           start_exe: Path, game_ovr: Path, command: Path, down_inventory: Path,
           subtract_inventory: Path, refusal_inventory: Path, exit_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command"),
                                  (baseline, BASELINE_SHA, "baseline"),
                                  (baseline_screen, BASELINE_SCREEN_SHA, "baseline screen"),
                                  (right_reference, SUBTRACT_SCREEN_SHA, "right reference")):
        if _sha(path) != expected:
            raise ValueError(f"technical skill receipt: {label} SHA-256 不符")
    baseline_events = json.loads(baseline.read_bytes())["events"]
    if len(baseline_events) != 289:
        raise ValueError("technical skill receipt: baseline 事件數不符")
    inventories = [
        reroll_lifecycle_receipt._read_inventory(down_inventory, 8, DOWN_ROLES),
        reroll_lifecycle_receipt._read_inventory(subtract_inventory, 10, SUBTRACT_ROLES),
        reroll_lifecycle_receipt._read_inventory(refusal_inventory, 1, REFUSAL_ROLES),
        reroll_lifecycle_receipt._read_inventory(exit_inventory, 7, EXIT_ROLES),
    ]
    cases = [
        (down_a, down_b, down_screen_a, down_screen_b, DOWN_RECEIPT_SHA, DOWN_SCREEN_SHA,
         inventories[0], [{"queued_at": 103_600_000, "scan": 80, "ascii": 0}], 105_000_000),
        (subtract_a, subtract_b, subtract_screen_a, subtract_screen_b, SUBTRACT_RECEIPT_SHA,
         SUBTRACT_SCREEN_SHA, inventories[1],
         [{"queued_at": 103_600_000, "scan": 28, "ascii": 13},
          {"queued_at": 103_700_000, "scan": 77, "ascii": 0},
          {"queued_at": 103_800_000, "scan": 28, "ascii": 13}], 105_000_000),
        (refusal_a, refusal_b, refusal_screen_a, refusal_screen_b, REFUSAL_RECEIPT_SHA,
         REFUSAL_SCREEN_SHA, inventories[2],
         [{"queued_at": 103_600_000, "scan": 1, "ascii": 27},
          {"queued_at": 103_800_000, "scan": 49, "ascii": 110}], 106_000_000),
        (exit_a, exit_b, exit_screen_a, exit_screen_b, EXIT_RECEIPT_SHA, EXIT_SCREEN_SHA,
         inventories[3], [{"queued_at": 103_600_000, "scan": 1, "ascii": 27},
                          {"queued_at": 103_800_000, "scan": 21, "ascii": 121}], 106_000_000),
    ]
    for receipt_a, receipt_b, screen_a, screen_b, receipt_sha, screen_sha, rows, keys, stopped_at in cases:
        raw_a, raw_b = receipt_a.read_bytes(), receipt_b.read_bytes()
        if raw_a != raw_b or hashlib.sha256(raw_a).hexdigest() != receipt_sha:
            raise ValueError("technical skill receipt: JSON 重播或固定 SHA-256 不符")
        try:
            receipt = json.loads(raw_a)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("technical skill receipt: 不是有效 UTF-8 JSON") from exc
        _validate_branch(receipt, baseline_events, rows, keys, stopped_at)
        screen_raw_a, screen_raw_b = screen_a.read_bytes(), screen_b.read_bytes()
        if (len(screen_raw_a) != 64_000 or screen_raw_a != screen_raw_b or
                hashlib.sha256(screen_raw_a).hexdigest() != screen_sha):
            raise ValueError("technical skill receipt: framebuffer 重播、尺寸或 SHA-256 不符")
        if receipt_a == subtract_a and screen_raw_a != right_reference.read_bytes():
            raise ValueError("technical skill receipt: 減點終點未回到零點／Right 選取畫面")
        if receipt_a == refusal_a and screen_raw_a != baseline_screen.read_bytes():
            raise ValueError("technical skill receipt: 拒絕離開未回到技術技能基線")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("down_a", "down_b", "down_screen_a", "down_screen_b", "subtract_a", "subtract_b",
                 "subtract_screen_a", "subtract_screen_b", "refusal_a", "refusal_b",
                 "refusal_screen_a", "refusal_screen_b", "exit_a", "exit_b", "exit_screen_a",
                 "exit_screen_b", "baseline", "baseline_screen", "right_reference", "state",
                 "start_exe", "game_ovr", "command", "down_inventory", "subtract_inventory",
                 "refusal_inventory", "exit_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
