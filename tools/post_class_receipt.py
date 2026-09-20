#!/usr/bin/env python3
"""驗證確認預設職業後角色資料畫面的決定性收據。"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re

import gender_events
import menu_events
import post_gender_receipt
import post_race_receipt


STATE_SHA = post_race_receipt.STATE_SHA
START_SHA = post_race_receipt.START_SHA
GAME_SHA = post_race_receipt.GAME_SHA
COMMAND_SHA = "363fc8045519fe4b70184a756549e5eade8917320ae9eff65a5e78ff38538231"
RECEIPT_SHA = "3c55e98804c752a817d80c66b20e0bac59992d32280582786790affc888b0a42"
SCREEN_SHA = "1f3b81946cc058d89a8ecfd9ca5aab8e7fb2aaa5d95c2c2ecbd49c219f51d4dd"
TOP_FIELDS = {"state_start", "stopped_at", "bios_input", "events", "bios_keys"}
HEADER = [
    "event_key", "sequence", "event_role", "inference_level", "entry_step", "post_call_step",
    "original_length", "original_sha256", "caller", "background", "foreground", "row", "column",
]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")
ROLES = {"selection_normal", "static_label", "empty_dynamic_value", "identity_value",
         "ability_label", "ability_placeholder", "summary_value", "skill_label", "skill_value",
         "ability_rerolled_value", "summary_or_skill_redraw", "reroll_prompt"}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_inventory(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("post-class-events.tsv: 不得含 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("post-class-events.tsv: 不是有效 UTF-8") from exc
    table = list(csv.reader(text.splitlines(), delimiter="\t"))
    if not table or table[0] != HEADER or len(table) != 97 or any(len(row) != len(HEADER) for row in table[1:]):
        raise ValueError("post-class-events.tsv: schema 或筆數不符")
    rows = [dict(zip(HEADER, row)) for row in table[1:]]
    if [row["sequence"] for row in rows] != [str(value) for value in range(1, 97)]:
        raise ValueError("post-class-events.tsv: sequence 不連續")
    if len({row["event_key"] for row in rows}) != 96:
        raise ValueError("post-class-events.tsv: event key 不唯一")
    previous = -1
    for row in rows:
        if row["event_role"] not in ROLES or row["inference_level"] != "confirmed":
            raise ValueError("post-class-events.tsv: role 或證據等級不符")
        if not HASH_RE.fullmatch(row["original_sha256"]) or not CALLER_RE.fullmatch(row["caller"]):
            raise ValueError("post-class-events.tsv: hash 或 caller 格式不符")
        for field in ("sequence", "entry_step", "post_call_step", "original_length", "background",
                      "foreground", "row", "column"):
            if not row[field].isascii() or not row[field].isdigit():
                raise ValueError(f"post-class-events.tsv: {field} 無效")
        entry, post = int(row["entry_step"]), int(row["post_call_step"])
        if not previous < entry < post:
            raise ValueError("post-class-events.tsv: step 次序不符")
        if any(not 0 <= int(row[field]) <= 255 for field in
               ("original_length", "background", "foreground", "row", "column")):
            raise ValueError("post-class-events.tsv: 數值越界")
        previous = post
    return rows


def _event_matches(event: dict, row: dict[str, str]) -> bool:
    segment, offset = (int(value, 16) for value in row["caller"].split(":"))
    return (event["caller"] == {"segment": segment, "offset": offset} and
            event["original_length"] == int(row["original_length"]) and
            event["original_sha256"] == row["original_sha256"] and
            all(event[field] == int(row[field]) for field in
                ("background", "foreground", "row", "column")))


def _validate_receipt(receipt: dict, prefix_rows: list[dict[str, str]], new_rows: list[dict[str, str]]) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 102_000_000:
        raise ValueError("post-class receipt: 頂層或執行範圍不符")
    if receipt["bios_input"] != "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)":
        raise ValueError("post-class receipt: 相容 Enter metadata 不符")
    if receipt["bios_keys"] != [
        {"queued_at": 100_010_000, "scan": 28, "ascii": 13},
        {"queued_at": 100_240_000, "scan": 28, "ascii": 13},
        {"queued_at": 100_400_000, "scan": 28, "ascii": 13},
        {"queued_at": 100_650_000, "scan": 28, "ascii": 13},
    ]:
        raise ValueError("post-class receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 118 or len(prefix_rows) != 22 or len(new_rows) != 96:
        raise ValueError("post-class receipt: 事件筆數不符")
    for index, (event, row) in enumerate(zip(events[:22], prefix_rows), 1):
        if not _event_matches(event, row):
            raise ValueError(f"post-class receipt: 前綴第 {index} 筆 identity 不符")
    for index, (event, row) in enumerate(zip(events[22:], new_rows), 1):
        if (event["entry_step"] != int(row["entry_step"]) or
                event["post_call_step"] != int(row["post_call_step"]) or
                not _event_matches(event, row)):
            raise ValueError(f"post-class receipt: 新事件第 {index} 筆 step／identity 不符")


def verify(receipt_a: Path, receipt_b: Path, screen_a: Path, screen_b: Path, state: Path,
           start_exe: Path, game_ovr: Path, command: Path, menu_inventory: Path,
           menu_catalog: Path, post_inventory: Path, lifecycle_inventory: Path,
           gender_inventory: Path, gender_catalog: Path, post_gender_inventory: Path,
           post_class_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command")):
        if _sha(path) != expected:
            raise ValueError(f"post-class receipt: {label} SHA-256 不符")
    menu_events.validate(menu_inventory, menu_catalog)
    gender_events.validate(gender_inventory, gender_catalog, post_inventory, lifecycle_inventory)
    with menu_inventory.open(encoding="utf-8", newline="") as stream:
        menu_rows = list(csv.DictReader(stream, delimiter="\t"))
    with gender_inventory.open(encoding="utf-8", newline="") as stream:
        gender_rows = list(csv.DictReader(stream, delimiter="\t"))
    prefix = menu_rows[:10] + post_race_receipt._read_inventory(post_inventory) + [gender_rows[4]]
    prefix += post_gender_receipt._read_inventory(post_gender_inventory)
    new_rows = _read_inventory(post_class_inventory)
    raw_a, raw_b = receipt_a.read_bytes(), receipt_b.read_bytes()
    if raw_a != raw_b or hashlib.sha256(raw_a).hexdigest() != RECEIPT_SHA:
        raise ValueError("post-class receipt: JSON 重播或固定 SHA-256 不符")
    try:
        receipt = json.loads(raw_a)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("post-class receipt: 不是有效 UTF-8 JSON") from exc
    _validate_receipt(receipt, prefix, new_rows)
    screen_raw_a, screen_raw_b = screen_a.read_bytes(), screen_b.read_bytes()
    if (len(screen_raw_a) != 64_000 or screen_raw_a != screen_raw_b or
            hashlib.sha256(screen_raw_a).hexdigest() != SCREEN_SHA):
        raise ValueError("post-class receipt: framebuffer 重播、尺寸或 SHA-256 不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("receipt_a", "receipt_b", "screen_a", "screen_b", "state", "start_exe", "game_ovr",
                 "command", "menu_inventory", "menu_catalog", "post_inventory", "lifecycle_inventory",
                 "gender_inventory", "gender_catalog", "post_gender_inventory", "post_class_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
