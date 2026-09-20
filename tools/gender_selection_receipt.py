#!/usr/bin/env python3
"""驗證性別選擇 Down／Up 與 Escape 的決定性收據。"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re

import menu_events
import post_race_receipt
import race_selection_receipt


STATE_SHA = post_race_receipt.STATE_SHA
START_SHA = post_race_receipt.START_SHA
GAME_SHA = post_race_receipt.GAME_SHA
COMMAND_SHA = post_race_receipt.COMMAND_SHA
DOWN_UP_RECEIPT_SHA = "e5d58d61cc74cb464343692355f68d5f4d54f3ecdd0f57f6e832f6d2de8cbd52"
DOWN_UP_SCREEN_SHA = "dcf947d18c85b051ec85e1bc968f30cec5c315a9158d598055d14ebfe82a715c"
ESCAPE_RECEIPT_SHA = "333960a20c5699ece5430e93a1fd3f7b04f0b5bd02a45c39a5e1050a0e96198a"
ESCAPE_SCREEN_SHA = "b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3"
HEADER = [
    "sequence", "input_path", "event_role", "event_key", "original_length",
    "original_sha256", "caller", "background", "foreground", "row", "column",
]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")
TOP_FIELDS = {"state_start", "stopped_at", "bios_input", "events", "bios_keys"}
BASE_ENTRY = post_race_receipt.ENTRY_STEPS
BASE_POST = post_race_receipt.POST_STEPS
DOWN_UP_ENTRY = [100400478, 100404132, 100460432, 100465577]
DOWN_UP_POST = [100403733, 100408910, 100465210, 100468832]
ESCAPE_ENTRY = [100400428, 100505151, 100527501, 100549953, 100571866, 100594672, 100616533, 100632796]
ESCAPE_POST = [100403683, 100520604, 100543731, 100561594, 100591150, 100603285, 100631986, 100646735]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_lifecycle(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("gender-selection-events.tsv: 不得含 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("gender-selection-events.tsv: 不是有效 UTF-8") from exc
    table = list(csv.reader(text.splitlines(), delimiter="\t"))
    if not table or table[0] != HEADER or len(table) != 13 or any(len(row) != len(HEADER) for row in table[1:]):
        raise ValueError("gender-selection-events.tsv: schema 或筆數不符")
    rows = [dict(zip(HEADER, row)) for row in table[1:]]
    if [row["sequence"] for row in rows] != [str(value) for value in range(1, 13)]:
        raise ValueError("gender-selection-events.tsv: sequence 不連續")
    if [row["input_path"] for row in rows] != ["down-up"] * 4 + ["escape"] * 8:
        raise ValueError("gender-selection-events.tsv: 路徑次序不符")
    if len({row["event_key"] for row in rows}) != 12:
        raise ValueError("gender-selection-events.tsv: event key 不唯一")
    for row in rows:
        if not HASH_RE.fullmatch(row["original_sha256"]) or not CALLER_RE.fullmatch(row["caller"]):
            raise ValueError("gender-selection-events.tsv: hash 或 caller 格式不符")
        for field in ("original_length", "background", "foreground", "row", "column"):
            if not row[field].isascii() or not row[field].isdigit() or not 0 <= int(row[field]) <= 255:
                raise ValueError(f"gender-selection-events.tsv: {field} 無效")
    return rows


def _validate_path(receipt: dict, expected_rows: list[dict[str, str]], entries: list[int], posts: list[int], keys: list[dict]) -> None:
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 101_000_000:
        raise ValueError("gender selection receipt: 頂層或執行範圍不符")
    if receipt["bios_input"] != "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)" or receipt["bios_keys"] != keys:
        raise ValueError("gender selection receipt: BIOS 排程不符")
    events = receipt["events"]
    if len(events) != len(expected_rows) or len(entries) != len(events) or len(posts) != len(events):
        raise ValueError("gender selection receipt: 事件數不符")
    previous = -1
    for index, (event, row, entry, post) in enumerate(zip(events, expected_rows, entries, posts), 1):
        if event["entry_step"] != entry or event["post_call_step"] != post or not previous < entry < post:
            raise ValueError(f"gender selection receipt: 第 {index} 筆 step 不符")
        if not race_selection_receipt._event_matches(event, row):
            raise ValueError(f"gender selection receipt: 第 {index} 筆 identity 不符")
        previous = post


def verify(down_a: Path, down_b: Path, down_screen_a: Path, down_screen_b: Path,
           escape_a: Path, escape_b: Path, escape_screen_a: Path, escape_screen_b: Path,
           state: Path, start_exe: Path, game_ovr: Path, command: Path,
           menu_inventory: Path, menu_catalog: Path, post_inventory: Path, lifecycle_inventory: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command")):
        if _sha(path) != expected:
            raise ValueError(f"gender selection receipt: {label} SHA-256 不符")
    menu_events.validate(menu_inventory, menu_catalog)
    with menu_inventory.open(encoding="utf-8", newline="") as stream:
        menu_rows = list(csv.DictReader(stream, delimiter="\t"))
    post_rows = post_race_receipt._read_inventory(post_inventory)
    lifecycle = _read_lifecycle(lifecycle_inventory)
    base = menu_rows[:10] + post_rows
    pairs = ((down_a, down_b, DOWN_UP_RECEIPT_SHA), (escape_a, escape_b, ESCAPE_RECEIPT_SHA))
    receipts = []
    for first, second, expected_hash in pairs:
        raw = first.read_bytes()
        if raw != second.read_bytes() or hashlib.sha256(raw).hexdigest() != expected_hash:
            raise ValueError("gender selection receipt: JSON 重播或 SHA-256 不符")
        receipts.append(json.loads(raw))
    common = [{"queued_at": 100_010_000, "scan": 28, "ascii": 13}, {"queued_at": 100_240_000, "scan": 28, "ascii": 13}]
    _validate_path(receipts[0], base + lifecycle[:4], BASE_ENTRY + DOWN_UP_ENTRY, BASE_POST + DOWN_UP_POST,
                   common + [{"queued_at": 100_400_000, "scan": 80, "ascii": 0}, {"queued_at": 100_460_000, "scan": 72, "ascii": 0}])
    _validate_path(receipts[1], base + lifecycle[4:], BASE_ENTRY + ESCAPE_ENTRY, BASE_POST + ESCAPE_POST,
                   common + [{"queued_at": 100_400_000, "scan": 1, "ascii": 27}])
    for first, second, expected in ((down_screen_a, down_screen_b, DOWN_UP_SCREEN_SHA),
                                    (escape_screen_a, escape_screen_b, ESCAPE_SCREEN_SHA)):
        raw = first.read_bytes()
        if len(raw) != 64_000 or raw != second.read_bytes() or hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError("gender selection receipt: framebuffer 重播、尺寸或 SHA-256 不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("down_a", "down_b", "down_screen_a", "down_screen_b", "escape_a", "escape_b",
                 "escape_screen_a", "escape_screen_b", "state", "start_exe", "game_ovr", "command",
                 "menu_inventory", "menu_catalog", "post_inventory", "lifecycle_inventory"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))

