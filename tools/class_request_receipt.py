#!/usr/bin/env python3
"""驗證職業選擇繁中執行期顯示請求收據。"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import class_events
import class_selection_receipt
import post_gender_receipt
import post_race_receipt
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name

STATE_SHA = post_gender_receipt.STATE_SHA
START_SHA = post_gender_receipt.START_SHA
GAME_SHA = post_gender_receipt.GAME_SHA
COMMAND_SHA = "363fc8045519fe4b70184a756549e5eade8917320ae9eff65a5e78ff38538231"
STEADY_SHA = "e2ea55e875a3a74a4ff0be92da3ddc4cab3f992f6fbed7c76dece88e8b2c37e0"
DOWN_UP_SHA = "3f542218d0098103fd6249c8cccabab7d1869cd4860c81e0648995433d341399"
ESCAPE_SHA = "16033cc1e4f901d9857f8bc4f1ccb68e8455630d29a80333140acd28f3761f66"
TOP_FIELDS = {"state_start", "stopped_at", "bios_input", "events", "requests", "catalog_misses", "bios_keys"}
REQUEST_FIELDS = {"event_key", "text_key", "translation_runes"}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _request(row, texts):
    return {"event_key": row["event_key"], "text_key": row["text_key"],
            "translation_runes": len(texts[row["text_key"]])}


def _validate_requests(receipt, expected, misses):
    if set(receipt) != TOP_FIELDS or receipt["catalog_misses"] != misses:
        raise ValueError("class request receipt: 頂層 schema 或 miss 數不符")
    if receipt["requests"] != expected:
        raise ValueError("class request receipt: request 序列不符")
    if any(set(row) != REQUEST_FIELDS or row["translation_runes"] <= 0 for row in receipt["requests"]):
        raise ValueError("class request receipt: request schema 或譯文字數不符")


def verify(steady_a: Path, steady_b: Path, down_a: Path, down_b: Path, escape_a: Path, escape_b: Path,
           state: Path, start_exe: Path, game_ovr: Path, command: Path, menu_inventory: Path,
           menu_catalog: Path, post_inventory: Path, gender_inventory: Path, class_inventory: Path,
           class_catalog: Path, post_gender_inventory: Path, lifecycle_inventory: Path,
           lang: str = DEFAULT_LANG) -> None:
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command")):
        if _sha(path) != expected:
            raise ValueError(f"class request receipt: {label} SHA-256 不符")
    class_events.validate(class_inventory, class_catalog, post_gender_inventory, lifecycle_inventory, lang=lang)
    menu_rows, gender_rows, class_rows = _rows(menu_inventory), _rows(gender_inventory), _rows(class_inventory)
    post_rows = post_race_receipt._read_inventory(post_inventory)
    lifecycle = class_selection_receipt._read_lifecycle(lifecycle_inventory)
    menu_texts = {r["key"]: r["translation"] for r in _rows(menu_catalog)}
    gender_texts = {r["key"]: r["translation"] for r in _rows(Path(str(gender_inventory).replace("gender-events.tsv", catalog_name("gender", lang))))}
    class_texts = {r["key"]: r["translation"] for r in _rows(class_catalog)}
    receipts = []
    for first, second, expected in ((steady_a, steady_b, STEADY_SHA), (down_a, down_b, DOWN_UP_SHA),
                                    (escape_a, escape_b, ESCAPE_SHA)):
        raw = first.read_bytes()
        if raw != second.read_bytes() or hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError("class request receipt: JSON 重播或固定 SHA-256 不符")
        receipts.append(json.loads(raw))
    base_rows = menu_rows[:10] + post_rows + [gender_rows[4]] + class_rows[:7]
    steady_core = {key: receipts[0][key] for key in post_gender_receipt.TOP_FIELDS}
    post_gender_receipt._validate_receipt(steady_core, base_rows)
    common = [{"queued_at": 100010000, "scan": 28, "ascii": 13},
              {"queued_at": 100240000, "scan": 28, "ascii": 13},
              {"queued_at": 100400000, "scan": 28, "ascii": 13}]
    down_core = {key: receipts[1][key] for key in class_selection_receipt.TOP_FIELDS}
    class_selection_receipt._validate_path(
        down_core, base_rows + lifecycle[:4], post_gender_receipt.ENTRY_STEPS + class_selection_receipt.DOWN_UP_ENTRY,
        post_gender_receipt.POST_STEPS + class_selection_receipt.DOWN_UP_POST,
        common + [{"queued_at": 100650000, "scan": 80, "ascii": 0}, {"queued_at": 100720000, "scan": 72, "ascii": 0}])
    escape_core = {key: receipts[2][key] for key in class_selection_receipt.TOP_FIELDS}
    class_selection_receipt._validate_path(
        escape_core, base_rows + lifecycle[4:], post_gender_receipt.ENTRY_STEPS + class_selection_receipt.ESCAPE_ENTRY,
        post_gender_receipt.POST_STEPS + class_selection_receipt.ESCAPE_POST,
        common + [{"queued_at": 100650000, "scan": 1, "ascii": 27}])
    menu_requests = [_request(row, menu_texts) for row in menu_rows[:10]]
    gender_request = _request(gender_rows[4], gender_texts)
    initial_class = [_request(row, class_texts) for row in class_rows[:7]]
    base_requests = menu_requests + [_request(row, gender_texts) for row in post_rows] + [gender_request] + initial_class
    _validate_requests(receipts[0], base_requests, 0)
    _validate_requests(receipts[1], base_requests + [_request(class_rows[i], class_texts) for i in (7, 8, 9, 6)], 0)
    _validate_requests(receipts[2], base_requests + [_request(class_rows[7], class_texts)], 7)

