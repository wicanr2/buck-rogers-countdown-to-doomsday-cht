#!/usr/bin/env python3
"""驗證 scratch-backed NO／YES 後的空角色名冊返回生命週期。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import post_class_receipt
import reroll_lifecycle_receipt
import save_prompt_receipt


STATE_SHA = save_prompt_receipt.STATE_SHA
START_SHA = save_prompt_receipt.START_SHA
GAME_SHA = save_prompt_receipt.GAME_SHA
COMMAND_SHA = "e3b07d66813ef90f1333c2d6f16e6b3e1870d4df43f11cbc7124e97bf221cd3a"
NO_BASELINE_SHA = save_prompt_receipt.NO_RECEIPT_SHA
YES_BASELINE_SHA = save_prompt_receipt.YES_RECEIPT_SHA
NO_RECEIPT_SHA = "996330589e35527482efca024af68e3d13dfd0a0a9f5328f87327655c96242b2"
YES_RECEIPT_SHA = "7c86c3ef0db049528e0fde85bc855da484983db52337398f01ce37c54a2bb7b0"
SCREEN_SHA = "a9171abc8464207e24377891d75097b290d74a455fad29dd92fa12cfe283ca00"
MANIFEST_SHA = "93018f5a710b1013d7c009a8b9c102714369f833fc0532659070a85846dc180a"
TOP_FIELDS = {"state_start", "stopped_at", "events", "bios_keys", "scratch"}
ROLES = {"previous_option_redraw", "current_option_redraw", "function_menu_instruction",
         "enter_option_redraw", "function_menu_return", "function_menu_return_selected"}
MENU_KEYS = [{"queued_at": 108_000_000, "scan": 80, "ascii": 0},
             {"queued_at": 108_200_000, "scan": 28, "ascii": 13}]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_branch(receipt: dict, baseline_events: list[dict], prefix_keys: list[dict[str, int]],
                     rows: list[dict[str, str]]) -> None:
    if (set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or
            receipt["stopped_at"] != 112_000_000 or receipt["scratch"] != "/tmp/scratch"):
        raise ValueError("character roster receipt: 頂層、執行範圍或 scratch 不符")
    if receipt["bios_keys"] != prefix_keys + MENU_KEYS:
        raise ValueError("character roster receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 305 + len(rows) or events[:305] != baseline_events:
        raise ValueError("character roster receipt: 基線或事件數不符")
    for index, (event, row) in enumerate(zip(events[305:], rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not post_class_receipt._event_matches(event, row)):
            raise ValueError(f"character roster receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(no_a: Path, no_b: Path, no_screen_a: Path, no_screen_b: Path,
           yes_a: Path, yes_b: Path, yes_screen_a: Path, yes_screen_b: Path,
           no_baseline: Path, yes_baseline: Path, state: Path, start_exe: Path, game_ovr: Path,
           command: Path, no_inventory: Path, yes_inventory: Path,
           no_manifest_a: Path, no_manifest_b: Path, yes_manifest_a: Path, yes_manifest_b: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command"),
                                  (no_baseline, NO_BASELINE_SHA, "NO baseline"),
                                  (yes_baseline, YES_BASELINE_SHA, "YES baseline")):
        if _sha(path) != expected:
            raise ValueError(f"character roster receipt: {label} SHA-256 不符")
    no_base = json.loads(no_baseline.read_bytes())
    yes_base = json.loads(yes_baseline.read_bytes())
    no_rows = reroll_lifecycle_receipt._read_inventory(no_inventory, 11, ROLES)
    yes_rows = reroll_lifecycle_receipt._read_inventory(yes_inventory, 11, ROLES)
    no_prefix = save_prompt_receipt.PREFIX_KEYS + [{"queued_at": 107_000_000, "scan": 49, "ascii": 110}]
    yes_prefix = save_prompt_receipt.PREFIX_KEYS + [
        {"queued_at": 107_000_000, "scan": 75, "ascii": 0},
        {"queued_at": 107_200_000, "scan": 28, "ascii": 13},
    ]
    cases = [(no_a, no_b, no_screen_a, no_screen_b, NO_RECEIPT_SHA, no_base["events"], no_prefix, no_rows),
             (yes_a, yes_b, yes_screen_a, yes_screen_b, YES_RECEIPT_SHA, yes_base["events"], yes_prefix, yes_rows)]
    for receipt_a, receipt_b, screen_a, screen_b, receipt_sha, baseline, keys, rows in cases:
        raw = receipt_a.read_bytes()
        if raw != receipt_b.read_bytes() or _sha(receipt_a) != receipt_sha:
            raise ValueError("character roster receipt: JSON 重播或固定 SHA-256 不符")
        _validate_branch(json.loads(raw), baseline, keys, rows)
        screen = screen_a.read_bytes()
        if len(screen) != 64_000 or screen != screen_b.read_bytes() or _sha(screen_a) != SCREEN_SHA:
            raise ValueError("character roster receipt: framebuffer 重播、尺寸或 SHA-256 不符")
    if no_screen_a.read_bytes() != yes_screen_a.read_bytes():
        raise ValueError("character roster receipt: NO／YES 終點畫面不同")
    manifests = [p.read_bytes() for p in (no_manifest_a, no_manifest_b, yes_manifest_a, yes_manifest_b)]
    if any(value != manifests[0] for value in manifests) or _sha(no_manifest_a) != MANIFEST_SHA:
        raise ValueError("character roster receipt: scratch manifest 不可重播")
    expected = f"{hashlib.sha256((Path(__file__).resolve().parents[1] / 'workplace/original/BRcdoom/CHARS.DAX').read_bytes()).hexdigest()}  CHARS.DAX\n".encode()
    if manifests[0] != expected:
        raise ValueError("character roster receipt: scratch 不是未變的 CHARS.DAX shadow")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("no_a", "no_b", "no_screen_a", "no_screen_b", "yes_a", "yes_b",
                 "yes_screen_a", "yes_screen_b", "no_baseline", "yes_baseline", "state",
                 "start_exe", "game_ovr", "command", "no_inventory", "yes_inventory",
                 "no_manifest_a", "no_manifest_b", "yes_manifest_a", "yes_manifest_b"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
