#!/usr/bin/env python3
"""驗證確認預設性別後職業選擇畫面的決定性收據。"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re

import gender_events
import menu_events
import post_race_receipt
import race_selection_receipt


STATE_SHA = post_race_receipt.STATE_SHA
START_SHA = post_race_receipt.START_SHA
GAME_SHA = post_race_receipt.GAME_SHA
COMMAND_SHA = "ed6e7b6537a9be3fe332f49821adee0d91c51a1f4510ca32648ed1b0f8fad5c9"
RECEIPT_SHA = "a3e195ebe6f43ffa2d9fdcfaeb92c8f68323da9bb487dc9c468095c3b012570b"
SCREEN_SHA = "3a61cb542625bdb0fd353f1d337e87c68091bd2dd2185e9b2ba34dad7558012c"
TOP_FIELDS = {"state_start", "stopped_at", "bios_input", "events", "bios_keys"}
HEADER = [
    "event_key", "sequence", "text_key", "original_length", "original_sha256",
    "caller", "background", "foreground", "row", "column",
]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")
ENTRY_STEPS = post_race_receipt.ENTRY_STEPS + [
    100400451, 100410301, 100437195, 100464371, 100491004, 100517807, 100544697, 100571639,
]
POST_STEPS = post_race_receipt.POST_STEPS + [
    100403706, 100418147, 100447349, 100469932, 100498085, 100525650, 100550258, 100580245,
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_inventory(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("post-gender-events.tsv: 不得含 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("post-gender-events.tsv: 不是有效 UTF-8") from exc
    table = list(csv.reader(text.splitlines(), delimiter="\t"))
    if not table or table[0] != HEADER or len(table) != 8 or any(len(row) != len(HEADER) for row in table[1:]):
        raise ValueError("post-gender-events.tsv: schema 或筆數不符")
    rows = [dict(zip(HEADER, row)) for row in table[1:]]
    if [row["sequence"] for row in rows] != [str(value) for value in range(1, 8)]:
        raise ValueError("post-gender-events.tsv: sequence 不連續")
    if len({row["event_key"] for row in rows}) != 7:
        raise ValueError("post-gender-events.tsv: event key 不唯一")
    identities = [tuple(row[field] for field in HEADER[3:]) for row in rows]
    if len(set(identities)) != 7:
        raise ValueError("post-gender-events.tsv: identity 不唯一")
    for row in rows:
        if not HASH_RE.fullmatch(row["original_sha256"]) or not CALLER_RE.fullmatch(row["caller"]):
            raise ValueError("post-gender-events.tsv: hash 或 caller 格式不符")
        for field in ("original_length", "background", "foreground", "row", "column"):
            if not row[field].isascii() or not row[field].isdigit() or not 0 <= int(row[field]) <= 255:
                raise ValueError(f"post-gender-events.tsv: {field} 無效")
    return rows


def _validate_receipt(receipt: dict, expected_rows: list[dict[str, str]]) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 101_000_000:
        raise ValueError("post-gender receipt: 頂層或執行範圍不符")
    if receipt["bios_input"] != "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)":
        raise ValueError("post-gender receipt: 相容 Enter metadata 不符")
    if receipt["bios_keys"] != [
        {"queued_at": 100_010_000, "scan": 28, "ascii": 13},
        {"queued_at": 100_240_000, "scan": 28, "ascii": 13},
        {"queued_at": 100_400_000, "scan": 28, "ascii": 13},
    ]:
        raise ValueError("post-gender receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != 22 or len(expected_rows) != 22:
        raise ValueError("post-gender receipt: 必須恰有二十二事件")
    previous = -1
    for index, (event, row, entry, post) in enumerate(zip(events, expected_rows, ENTRY_STEPS, POST_STEPS), 1):
        if event["entry_step"] != entry or event["post_call_step"] != post or not previous < entry < post:
            raise ValueError(f"post-gender receipt: 第 {index} 筆 step 不符")
        if not race_selection_receipt._event_matches(event, row):
            raise ValueError(f"post-gender receipt: 第 {index} 筆 identity 不符")
        previous = post


def verify(receipt_a: Path, receipt_b: Path, screen_a: Path, screen_b: Path,
           state: Path, start_exe: Path, game_ovr: Path, command: Path,
           menu_inventory: Path, menu_catalog: Path, post_inventory: Path,
           lifecycle_inventory: Path, gender_inventory: Path, gender_catalog: Path,
           post_gender_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command")):
        if _sha(path) != expected:
            raise ValueError(f"post-gender receipt: {label} SHA-256 不符")
    menu_events.validate(menu_inventory, menu_catalog)
    gender_events.validate(gender_inventory, gender_catalog, post_inventory, lifecycle_inventory)
    with menu_inventory.open(encoding="utf-8", newline="") as stream:
        menu_rows = list(csv.DictReader(stream, delimiter="\t"))
    with gender_inventory.open(encoding="utf-8", newline="") as stream:
        gender_rows = list(csv.DictReader(stream, delimiter="\t"))
    post_rows = post_race_receipt._read_inventory(post_inventory)
    new_rows = _read_inventory(post_gender_inventory)
    expected_rows = menu_rows[:10] + post_rows + [gender_rows[4]] + new_rows
    raw_a, raw_b = receipt_a.read_bytes(), receipt_b.read_bytes()
    if raw_a != raw_b or hashlib.sha256(raw_a).hexdigest() != RECEIPT_SHA:
        raise ValueError("post-gender receipt: JSON 重播或固定 SHA-256 不符")
    try:
        receipt = json.loads(raw_a)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("post-gender receipt: 不是有效 UTF-8 JSON") from exc
    _validate_receipt(receipt, expected_rows)
    screen_raw_a, screen_raw_b = screen_a.read_bytes(), screen_b.read_bytes()
    if (len(screen_raw_a) != 64_000 or screen_raw_a != screen_raw_b or
            hashlib.sha256(screen_raw_a).hexdigest() != SCREEN_SHA):
        raise ValueError("post-gender receipt: framebuffer 重播、尺寸或 SHA-256 不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("receipt_a", "receipt_b", "screen_a", "screen_b", "state", "start_exe", "game_ovr",
                 "command", "menu_inventory", "menu_catalog", "post_inventory", "lifecycle_inventory",
                 "gender_inventory", "gender_catalog", "post_gender_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
