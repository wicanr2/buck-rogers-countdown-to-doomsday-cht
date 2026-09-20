#!/usr/bin/env python3
"""驗證角色能力重擲 Y／N 分支的決定性生命週期收據。"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re

import post_class_receipt


STATE_SHA = post_class_receipt.STATE_SHA
START_SHA = post_class_receipt.START_SHA
GAME_SHA = post_class_receipt.GAME_SHA
COMMAND_SHA = post_class_receipt.COMMAND_SHA
BASELINE_SHA = post_class_receipt.RECEIPT_SHA
YES_RECEIPT_SHA = "132cf0078289064e7ccba27a5dafe346df1b0e78c35e051afaa5461392ed5eb5"
YES_SCREEN_SHA = "03d9bf1fcdd871055949c5545eaf102fecb7aa6ef0f3b3e09a2dcf6e95050f97"
NO_RECEIPT_SHA = "f9ed6a8ef55bc3503d427a04f2788b55c959b35e3e1af31b0c52058d27117bff"
NO_SCREEN_SHA = "55da7c0e296b882f99c7c8ba2550743debe93a8bc480d1a0fc8fbb1dc514a6bb"
HEADER = post_class_receipt.HEADER
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")
YES_ROLES = {"ability_rerolled_value", "summary_redraw", "skill_label", "skill_value", "reroll_prompt"}
NO_ROLES = {"accept_transition_redraw", "name_prompt"}
TOP_FIELDS = {"state_start", "stopped_at", "events", "bios_keys"}
PREFIX_KEYS = [
    {"queued_at": 100_010_000, "scan": 28, "ascii": 13},
    {"queued_at": 100_240_000, "scan": 28, "ascii": 13},
    {"queued_at": 100_400_000, "scan": 28, "ascii": 13},
    {"queued_at": 100_650_000, "scan": 28, "ascii": 13},
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_inventory(path: Path, expected_count: int, roles: set[str]) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path.name}: 不得含 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path.name}: 不是有效 UTF-8") from exc
    table = list(csv.reader(text.splitlines(), delimiter="\t"))
    if (not table or table[0] != HEADER or len(table) != expected_count + 1 or
            any(len(row) != len(HEADER) for row in table[1:])):
        raise ValueError(f"{path.name}: schema 或筆數不符")
    rows = [dict(zip(HEADER, row)) for row in table[1:]]
    if [row["sequence"] for row in rows] != [str(value) for value in range(1, expected_count + 1)]:
        raise ValueError(f"{path.name}: sequence 不連續")
    if len({row["event_key"] for row in rows}) != expected_count:
        raise ValueError(f"{path.name}: event key 不唯一")
    previous = -1
    for row in rows:
        if row["event_role"] not in roles or row["inference_level"] != "confirmed":
            raise ValueError(f"{path.name}: role 或證據等級不符")
        if not HASH_RE.fullmatch(row["original_sha256"]) or not CALLER_RE.fullmatch(row["caller"]):
            raise ValueError(f"{path.name}: hash 或 caller 格式不符")
        for field in ("sequence", "entry_step", "post_call_step", "original_length", "background",
                      "foreground", "row", "column"):
            if not row[field].isascii() or not row[field].isdigit():
                raise ValueError(f"{path.name}: {field} 無效")
        entry, post = int(row["entry_step"]), int(row["post_call_step"])
        if not previous < entry < post:
            raise ValueError(f"{path.name}: step 次序不符")
        if any(not 0 <= int(row[field]) <= 255 for field in
               ("original_length", "background", "foreground", "row", "column")):
            raise ValueError(f"{path.name}: 數值越界")
        previous = post
    return rows


def _validate_branch(receipt: dict, baseline_events: list[dict], rows: list[dict[str, str]],
                     final_key: dict[str, int]) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 102_000_000:
        raise ValueError("reroll receipt: 頂層或執行範圍不符")
    if receipt["bios_keys"] != PREFIX_KEYS + [final_key]:
        raise ValueError("reroll receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 118 + len(rows) or events[:118] != baseline_events:
        raise ValueError("reroll receipt: 基線或事件數不符")
    for index, (event, row) in enumerate(zip(events[118:], rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not post_class_receipt._event_matches(event, row)):
            raise ValueError(f"reroll receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(yes_a: Path, yes_b: Path, yes_screen_a: Path, yes_screen_b: Path,
           no_a: Path, no_b: Path, no_screen_a: Path, no_screen_b: Path,
           baseline: Path, state: Path, start_exe: Path, game_ovr: Path, command: Path,
           yes_inventory: Path, no_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command"),
                                  (baseline, BASELINE_SHA, "baseline")):
        if _sha(path) != expected:
            raise ValueError(f"reroll receipt: {label} SHA-256 不符")
    baseline_events = json.loads(baseline.read_bytes())["events"]
    if len(baseline_events) != 118:
        raise ValueError("reroll receipt: baseline 事件數不符")
    yes_rows = _read_inventory(yes_inventory, 31, YES_ROLES)
    no_rows = _read_inventory(no_inventory, 65, NO_ROLES)
    cases = [
        (yes_a, yes_b, yes_screen_a, yes_screen_b, YES_RECEIPT_SHA, YES_SCREEN_SHA, yes_rows,
         {"queued_at": 101_400_000, "scan": 21, "ascii": 121}),
        (no_a, no_b, no_screen_a, no_screen_b, NO_RECEIPT_SHA, NO_SCREEN_SHA, no_rows,
         {"queued_at": 101_400_000, "scan": 49, "ascii": 110}),
    ]
    for receipt_a, receipt_b, screen_a, screen_b, receipt_sha, screen_sha, rows, key in cases:
        raw_a, raw_b = receipt_a.read_bytes(), receipt_b.read_bytes()
        if raw_a != raw_b or hashlib.sha256(raw_a).hexdigest() != receipt_sha:
            raise ValueError("reroll receipt: JSON 重播或固定 SHA-256 不符")
        try:
            receipt = json.loads(raw_a)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("reroll receipt: 不是有效 UTF-8 JSON") from exc
        _validate_branch(receipt, baseline_events, rows, key)
        screen_raw_a, screen_raw_b = screen_a.read_bytes(), screen_b.read_bytes()
        if (len(screen_raw_a) != 64_000 or screen_raw_a != screen_raw_b or
                hashlib.sha256(screen_raw_a).hexdigest() != screen_sha):
            raise ValueError("reroll receipt: framebuffer 重播、尺寸或 SHA-256 不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("yes_a", "yes_b", "yes_screen_a", "yes_screen_b", "no_a", "no_b", "no_screen_a",
                 "no_screen_b", "baseline", "state", "start_exe", "game_ovr", "command",
                 "yes_inventory", "no_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
