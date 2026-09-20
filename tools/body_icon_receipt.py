#!/usr/bin/env python3
"""驗證角色身體圖示移動、拒絕及確認分支的決定性收據。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import post_class_receipt
import reroll_lifecycle_receipt
import technical_skill_receipt


STATE_SHA = technical_skill_receipt.STATE_SHA
START_SHA = technical_skill_receipt.START_SHA
GAME_SHA = technical_skill_receipt.GAME_SHA
COMMAND_SHA = technical_skill_receipt.COMMAND_SHA
BASELINE_SHA = technical_skill_receipt.EXIT_RECEIPT_SHA
BASELINE_SCREEN_SHA = technical_skill_receipt.EXIT_SCREEN_SHA
MOVE_RECEIPT_SHA = "f81bbf6026743a34e38bede37cb3b7af9dc355d80fbb34a9e9a9a23905f982cb"
MOVE_SCREEN_SHA = "bf38b570cf63a978fe88d5cb3b30fb233675d6acec7d5847220a8db57e309d90"
REFUSAL_RECEIPT_SHA = "fe6ac40ff62e8e1e74c409529a9ec3a8243b20cb18eb4700c5a81576a01df019"
EXIT_RECEIPT_SHA = "56f36c319307be6560934141d805c9a575f660ba09ed93655122cc66dd4bcc19"
EXIT_SCREEN_SHA = "927ec313f9e5a10937c23735c843ef20f6d2fc9cf2b0ef2aec5fff9d8f303078"
TOP_FIELDS = {"state_start", "stopped_at", "events", "bios_keys"}
PREFIX_KEYS = technical_skill_receipt.PREFIX_KEYS + [
    {"queued_at": 103_600_000, "scan": 1, "ascii": 27},
    {"queued_at": 103_800_000, "scan": 21, "ascii": 121},
]
MOVE_ROLES = {"selection_instruction"}
REFUSAL_ROLES = {"icon_confirmation_prompt", "body_icon_screen", "selection_instruction"}
EXIT_ROLES = {"icon_confirmation_prompt", "save_prompt"}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_branch(receipt: dict, baseline_events: list[dict], rows: list[dict[str, str]],
                     suffix_keys: list[dict[str, int]], stopped_at: int) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != stopped_at:
        raise ValueError("body icon receipt: 頂層或執行範圍不符")
    if receipt["bios_keys"] != PREFIX_KEYS + suffix_keys:
        raise ValueError("body icon receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 296 + len(rows) or events[:296] != baseline_events:
        raise ValueError("body icon receipt: 基線或事件數不符")
    for index, (event, row) in enumerate(zip(events[296:], rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not post_class_receipt._event_matches(event, row)):
            raise ValueError(f"body icon receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(move_a: Path, move_b: Path, move_screen_a: Path, move_screen_b: Path,
           refusal_a: Path, refusal_b: Path, refusal_screen_a: Path, refusal_screen_b: Path,
           exit_a: Path, exit_b: Path, exit_screen_a: Path, exit_screen_b: Path,
           baseline: Path, baseline_screen: Path, state: Path, start_exe: Path, game_ovr: Path,
           command: Path, move_inventory: Path, refusal_inventory: Path, exit_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command"),
                                  (baseline, BASELINE_SHA, "baseline"),
                                  (baseline_screen, BASELINE_SCREEN_SHA, "baseline screen")):
        if _sha(path) != expected:
            raise ValueError(f"body icon receipt: {label} SHA-256 不符")
    baseline_events = json.loads(baseline.read_bytes())["events"]
    inventories = [
        reroll_lifecycle_receipt._read_inventory(move_inventory, 1, MOVE_ROLES),
        reroll_lifecycle_receipt._read_inventory(refusal_inventory, 6, REFUSAL_ROLES),
        reroll_lifecycle_receipt._read_inventory(exit_inventory, 2, EXIT_ROLES),
    ]
    cases = [
        (move_a, move_b, move_screen_a, move_screen_b, MOVE_RECEIPT_SHA, MOVE_SCREEN_SHA,
         inventories[0], [{"queued_at": 106_000_000, "scan": 77, "ascii": 0}], 108_000_000),
        (refusal_a, refusal_b, refusal_screen_a, refusal_screen_b, REFUSAL_RECEIPT_SHA,
         BASELINE_SCREEN_SHA, inventories[1], [{"queued_at": 106_000_000, "scan": 28, "ascii": 13},
         {"queued_at": 106_200_000, "scan": 49, "ascii": 110}], 109_000_000),
        (exit_a, exit_b, exit_screen_a, exit_screen_b, EXIT_RECEIPT_SHA, EXIT_SCREEN_SHA,
         inventories[2], [{"queued_at": 106_000_000, "scan": 28, "ascii": 13},
         {"queued_at": 106_200_000, "scan": 21, "ascii": 121}], 109_000_000),
    ]
    for receipt_a, receipt_b, screen_a, screen_b, receipt_sha, screen_sha, rows, keys, stop in cases:
        raw = receipt_a.read_bytes()
        if raw != receipt_b.read_bytes() or _sha(receipt_a) != receipt_sha:
            raise ValueError("body icon receipt: JSON 重播或固定 SHA-256 不符")
        receipt = json.loads(raw)
        _validate_branch(receipt, baseline_events, rows, keys, stop)
        screen = screen_a.read_bytes()
        if len(screen) != 64_000 or screen != screen_b.read_bytes() or _sha(screen_a) != screen_sha:
            raise ValueError("body icon receipt: framebuffer 重播、尺寸或 SHA-256 不符")
        if receipt_a == refusal_a and screen != baseline_screen.read_bytes():
            raise ValueError("body icon receipt: N 未回到圖示選擇基線")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("move_a", "move_b", "move_screen_a", "move_screen_b", "refusal_a", "refusal_b",
                 "refusal_screen_a", "refusal_screen_b", "exit_a", "exit_b", "exit_screen_a",
                 "exit_screen_b", "baseline", "baseline_screen", "state", "start_exe", "game_ovr",
                 "command", "move_inventory", "refusal_inventory", "exit_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
