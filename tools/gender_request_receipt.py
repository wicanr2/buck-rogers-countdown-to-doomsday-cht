#!/usr/bin/env python3
"""驗證性別選擇的繁中執行期顯示請求收據。"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import gender_events
import gender_selection_receipt
import post_race_receipt


STATE_SHA = post_race_receipt.STATE_SHA
START_SHA = post_race_receipt.START_SHA
GAME_SHA = post_race_receipt.GAME_SHA
COMMAND_SHA = "ed6e7b6537a9be3fe332f49821adee0d91c51a1f4510ca32648ed1b0f8fad5c9"
DOWN_UP_SHA = "d5bafaf03cd1fb3c5f54346239aab7754b7ceb828789436d73957cca9854faa4"
ESCAPE_SHA = "0b7518bc5ea5583954f33b153c77d900b77ca09f7584de9e21325f618890628b"
TOP_FIELDS = {
    "state_start", "stopped_at", "bios_input", "events", "requests", "catalog_misses", "bios_keys",
}
REQUEST_FIELDS = {"event_key", "text_key", "translation_runes"}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _request(row: dict[str, str], texts: dict[str, str]) -> dict:
    translation = texts[row["text_key"]]
    return {"event_key": row["event_key"], "text_key": row["text_key"],
            "translation_runes": len(translation)}


def _validate_request_contract(receipt: dict, expected: list[dict], misses: int) -> None:
    if set(receipt) != TOP_FIELDS:
        raise ValueError("gender request receipt: 頂層 schema 不符")
    if receipt["catalog_misses"] != misses:
        raise ValueError("gender request receipt: catalog miss 數不符")
    if receipt["requests"] != expected:
        raise ValueError("gender request receipt: request 序列不符")
    if any(set(row) != REQUEST_FIELDS or row["translation_runes"] <= 0 for row in receipt["requests"]):
        raise ValueError("gender request receipt: request schema 或譯文字數不符")


def verify(down_a: Path, down_b: Path, escape_a: Path, escape_b: Path,
           state: Path, start_exe: Path, game_ovr: Path, command: Path,
           menu_inventory: Path, menu_catalog: Path, post_inventory: Path,
           lifecycle_inventory: Path, gender_inventory: Path, gender_catalog: Path) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command")):
        if _sha(path) != expected:
            raise ValueError(f"gender request receipt: {label} SHA-256 不符")
    gender_events.validate(gender_inventory, gender_catalog, post_inventory, lifecycle_inventory)
    menu_rows, gender_rows = _rows(menu_inventory), _rows(gender_inventory)
    menu_texts = {row["key"]: row["translation"] for row in _rows(menu_catalog)}
    gender_texts = {row["key"]: row["translation"] for row in _rows(gender_catalog)}
    post_rows = post_race_receipt._read_inventory(post_inventory)
    lifecycle = gender_selection_receipt._read_lifecycle(lifecycle_inventory)
    receipts = []
    for first, second, expected_sha in ((down_a, down_b, DOWN_UP_SHA), (escape_a, escape_b, ESCAPE_SHA)):
        raw = first.read_bytes()
        if raw != second.read_bytes() or hashlib.sha256(raw).hexdigest() != expected_sha:
            raise ValueError("gender request receipt: JSON 重播或固定 SHA-256 不符")
        receipts.append(json.loads(raw))

    common = [{"queued_at": 100_010_000, "scan": 28, "ascii": 13},
              {"queued_at": 100_240_000, "scan": 28, "ascii": 13}]
    base = menu_rows[:10] + post_rows
    down_core = {key: receipts[0][key] for key in gender_selection_receipt.TOP_FIELDS}
    gender_selection_receipt._validate_path(
        down_core, base + lifecycle[:4],
        gender_selection_receipt.BASE_ENTRY + gender_selection_receipt.DOWN_UP_ENTRY,
        gender_selection_receipt.BASE_POST + gender_selection_receipt.DOWN_UP_POST,
        common + [{"queued_at": 100_400_000, "scan": 80, "ascii": 0},
                  {"queued_at": 100_460_000, "scan": 72, "ascii": 0}],
    )
    escape_core = {key: receipts[1][key] for key in gender_selection_receipt.TOP_FIELDS}
    gender_selection_receipt._validate_path(
        escape_core, base + lifecycle[4:],
        gender_selection_receipt.BASE_ENTRY + gender_selection_receipt.ESCAPE_ENTRY,
        gender_selection_receipt.BASE_POST + gender_selection_receipt.ESCAPE_POST,
        common + [{"queued_at": 100_400_000, "scan": 1, "ascii": 27}],
    )
    menu_requests = [_request(row, menu_texts) for row in menu_rows[:10]]
    down_gender = [gender_rows[index] for index in (0, 1, 2, 3, 4, 5, 6, 3)]
    escape_gender = [gender_rows[index] for index in (0, 1, 2, 3, 4)]
    _validate_request_contract(receipts[0], menu_requests + [_request(row, gender_texts) for row in down_gender], 0)
    _validate_request_contract(receipts[1], menu_requests + [_request(row, gender_texts) for row in escape_gender], 7)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("down_a", "down_b", "escape_a", "escape_b", "state", "start_exe", "game_ovr", "command",
                 "menu_inventory", "menu_catalog", "post_inventory", "lifecycle_inventory",
                 "gender_inventory", "gender_catalog"):
        parser.add_argument(name, type=Path)
    verify(**vars(parser.parse_args()))
