#!/usr/bin/env python3
"""驗證儲存詢問字母鍵、NO 與 YES 選取分支的決定性收據。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import body_icon_receipt
import post_class_receipt
import reroll_lifecycle_receipt


STATE_SHA = body_icon_receipt.STATE_SHA
START_SHA = body_icon_receipt.START_SHA
GAME_SHA = body_icon_receipt.GAME_SHA
COMMAND_SHA = body_icon_receipt.COMMAND_SHA
BASELINE_SHA = body_icon_receipt.EXIT_RECEIPT_SHA
BASELINE_SCREEN_SHA = body_icon_receipt.EXIT_SCREEN_SHA
MANIFEST_SHA = "4bd93ba65ec2489bf4273346a62a521a9e401c3dd511b373b15e6e10d15819ff"
LITERAL_Y_RECEIPT_SHA = "60fef20825de9a60ded6e14157a8df8353cb0aa41fd1ed412caeea735095ca4a"
NO_RECEIPT_SHA = "1ccd699e2812e7b0d09f1975abb2b7d0f7e57a6a52816de4fb65763c28bb6fba"
YES_RECEIPT_SHA = "73469dff179ab79606b335d9cf3bbc1d4751319eace3e19dc3aacae3ed413a71"
MENU_SCREEN_SHA = "b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3"
TOP_FIELDS = {"state_start", "stopped_at", "events", "bios_keys"}
MENU_ROLES = {"function_menu", "function_menu_selected", "function_menu_instruction"}
PREFIX_KEYS = body_icon_receipt.PREFIX_KEYS + [
    {"queued_at": 106_000_000, "scan": 28, "ascii": 13},
    {"queued_at": 106_200_000, "scan": 21, "ascii": 121},
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_branch(receipt: dict, baseline_events: list[dict], rows: list[dict[str, str]],
                     suffix_keys: list[dict[str, int]]) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 113_000_000:
        raise ValueError("save prompt receipt: 頂層或執行範圍不符")
    if receipt["bios_keys"] != PREFIX_KEYS + suffix_keys:
        raise ValueError("save prompt receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 298 + len(rows) or events[:298] != baseline_events:
        raise ValueError("save prompt receipt: 基線或事件數不符")
    for index, (event, row) in enumerate(zip(events[298:], rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not post_class_receipt._event_matches(event, row)):
            raise ValueError(f"save prompt receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(literal_a: Path, literal_b: Path, literal_screen_a: Path, literal_screen_b: Path,
           no_a: Path, no_b: Path, no_screen_a: Path, no_screen_b: Path,
           yes_a: Path, yes_b: Path, yes_screen_a: Path, yes_screen_b: Path,
           baseline: Path, baseline_screen: Path, state: Path, start_exe: Path, game_ovr: Path,
           command: Path, no_inventory: Path, yes_inventory: Path, pristine_manifest: Path,
           no_manifest_a: Path, no_manifest_b: Path, yes_manifest_a: Path, yes_manifest_b: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command"),
                                  (baseline, BASELINE_SHA, "baseline"),
                                  (baseline_screen, BASELINE_SCREEN_SHA, "baseline screen")):
        if _sha(path) != expected:
            raise ValueError(f"save prompt receipt: {label} SHA-256 不符")
    manifest = pristine_manifest.read_bytes()
    if _sha(pristine_manifest) != MANIFEST_SHA:
        raise ValueError("save prompt receipt: pristine manifest SHA-256 不符")
    for path in (no_manifest_a, no_manifest_b, yes_manifest_a, yes_manifest_b):
        if path.read_bytes() != manifest:
            raise ValueError("save prompt receipt: overlay 檔案有非預期變動")
    baseline_events = json.loads(baseline.read_bytes())["events"]
    no_rows = reroll_lifecycle_receipt._read_inventory(no_inventory, 7, MENU_ROLES)
    yes_rows = reroll_lifecycle_receipt._read_inventory(yes_inventory, 7, MENU_ROLES)
    cases = [
        (literal_a, literal_b, literal_screen_a, literal_screen_b, LITERAL_Y_RECEIPT_SHA,
         BASELINE_SCREEN_SHA, [], [{"queued_at": 107_000_000, "scan": 21, "ascii": 121}]),
        (no_a, no_b, no_screen_a, no_screen_b, NO_RECEIPT_SHA, MENU_SCREEN_SHA, no_rows,
         [{"queued_at": 107_000_000, "scan": 49, "ascii": 110}]),
        (yes_a, yes_b, yes_screen_a, yes_screen_b, YES_RECEIPT_SHA, MENU_SCREEN_SHA, yes_rows,
         [{"queued_at": 107_000_000, "scan": 75, "ascii": 0},
          {"queued_at": 107_200_000, "scan": 28, "ascii": 13}]),
    ]
    for receipt_a, receipt_b, screen_a, screen_b, receipt_sha, screen_sha, rows, keys in cases:
        raw = receipt_a.read_bytes()
        if raw != receipt_b.read_bytes() or _sha(receipt_a) != receipt_sha:
            raise ValueError("save prompt receipt: JSON 重播或固定 SHA-256 不符")
        _validate_branch(json.loads(raw), baseline_events, rows, keys)
        screen = screen_a.read_bytes()
        if len(screen) != 64_000 or screen != screen_b.read_bytes() or _sha(screen_a) != screen_sha:
            raise ValueError("save prompt receipt: framebuffer 重播、尺寸或 SHA-256 不符")
    if no_screen_a.read_bytes() != yes_screen_a.read_bytes():
        raise ValueError("save prompt receipt: NO 與 YES 未回到相同功能選單")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("literal_a", "literal_b", "literal_screen_a", "literal_screen_b", "no_a", "no_b",
                 "no_screen_a", "no_screen_b", "yes_a", "yes_b", "yes_screen_a", "yes_screen_b",
                 "baseline", "baseline_screen", "state", "start_exe", "game_ovr", "command",
                 "no_inventory", "yes_inventory", "pristine_manifest", "no_manifest_a",
                 "no_manifest_b", "yes_manifest_a", "yes_manifest_b"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
