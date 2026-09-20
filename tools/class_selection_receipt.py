#!/usr/bin/env python3
"""驗證職業選擇 Down／Up 與 Escape 的決定性收據。"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re

import post_gender_receipt
import race_selection_receipt

STATE_SHA = post_gender_receipt.STATE_SHA
START_SHA = post_gender_receipt.START_SHA
GAME_SHA = post_gender_receipt.GAME_SHA
COMMAND_SHA = post_gender_receipt.COMMAND_SHA
DOWN_UP_RECEIPT_SHA = "650ad5b143c6a1382396289fcf9fc94105acd45f6fbc891bee3c6549d2876696"
DOWN_UP_SCREEN_SHA = post_gender_receipt.SCREEN_SHA
ESCAPE_RECEIPT_SHA = "653fc53dca4a971ba639f24c9f61cad79614b6718330367b5fdd395cd3bd6c51"
ESCAPE_SCREEN_SHA = "b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3"
HEADER = ["sequence", "input_path", "event_role", "event_key", "original_length",
          "original_sha256", "caller", "background", "foreground", "row", "column"]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")
TOP_FIELDS = {"state_start", "stopped_at", "bios_input", "events", "bios_keys"}
BASE_ENTRY = post_gender_receipt.ENTRY_STEPS
BASE_POST = post_gender_receipt.POST_STEPS
DOWN_UP_ENTRY = [100650515, 100659520, 100720463, 100724843]
DOWN_UP_POST = [100659121, 100663533, 100724476, 100733449]
ESCAPE_ENTRY = [100650465, 100760834, 100783184, 100805636, 100827549, 100850355, 100872216, 100888479]
ESCAPE_POST = [100659071, 100776287, 100799414, 100817277, 100846833, 100858968, 100887669, 100902418]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_lifecycle(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("class-selection-events.tsv: 不得含 BOM")
    try:
        table = list(csv.reader(raw.decode("utf-8").splitlines(), delimiter="\t"))
    except UnicodeDecodeError as exc:
        raise ValueError("class-selection-events.tsv: 不是有效 UTF-8") from exc
    if not table or table[0] != HEADER or len(table) != 13 or any(len(row) != len(HEADER) for row in table[1:]):
        raise ValueError("class-selection-events.tsv: schema 或筆數不符")
    rows = [dict(zip(HEADER, row)) for row in table[1:]]
    if [r["sequence"] for r in rows] != [str(i) for i in range(1, 13)]:
        raise ValueError("class-selection-events.tsv: sequence 不連續")
    if [r["input_path"] for r in rows] != ["down-up"] * 4 + ["escape"] * 8:
        raise ValueError("class-selection-events.tsv: 路徑次序不符")
    if len({r["event_key"] for r in rows}) != 12:
        raise ValueError("class-selection-events.tsv: event key 不唯一")
    for row in rows:
        if not HASH_RE.fullmatch(row["original_sha256"]) or not CALLER_RE.fullmatch(row["caller"]):
            raise ValueError("class-selection-events.tsv: hash 或 caller 格式不符")
        for field in ("original_length", "background", "foreground", "row", "column"):
            if not row[field].isascii() or not row[field].isdigit() or not 0 <= int(row[field]) <= 255:
                raise ValueError(f"class-selection-events.tsv: {field} 無效")
    return rows


def _validate_path(receipt, rows, entries, posts, keys):
    if set(receipt) != TOP_FIELDS or receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 102_000_000:
        raise ValueError("class selection receipt: 頂層或執行範圍不符")
    if receipt["bios_input"] != "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)" or receipt["bios_keys"] != keys:
        raise ValueError("class selection receipt: BIOS 排程不符")
    if len(receipt["events"]) != len(rows):
        raise ValueError("class selection receipt: 事件數不符")
    previous = -1
    for index, (event, row, entry, post) in enumerate(zip(receipt["events"], rows, entries, posts), 1):
        if event["entry_step"] != entry or event["post_call_step"] != post or not previous < entry < post:
            raise ValueError(f"class selection receipt: 第 {index} 筆 step 不符")
        if not race_selection_receipt._event_matches(event, row):
            raise ValueError(f"class selection receipt: 第 {index} 筆 identity 不符")
        previous = post


def verify(down_a, down_b, down_screen_a, down_screen_b, escape_a, escape_b, escape_screen_a,
           escape_screen_b, state, start_exe, game_ovr, command, post_gender_inventory,
           lifecycle_inventory):
    for path, expected, label in ((state, STATE_SHA, "state"), (start_exe, START_SHA, "START.EXE"),
                                  (game_ovr, GAME_SHA, "GAME.OVR"), (command, COMMAND_SHA, "command")):
        if _sha(path) != expected:
            raise ValueError(f"class selection receipt: {label} SHA-256 不符")
    base_rows = post_gender_receipt._read_inventory(post_gender_inventory)
    # 正式前綴由 post-gender verifier 的完整 22 筆收據提供；呼叫端傳入 JSON 後直接取前 22 筆。
    lifecycle = _read_lifecycle(lifecycle_inventory)
    paths = ((down_a, down_b, DOWN_UP_RECEIPT_SHA, lifecycle[:4]),
             (escape_a, escape_b, ESCAPE_RECEIPT_SHA, lifecycle[4:]))
    receipts = []
    for first, second, expected, _ in paths:
        raw = first.read_bytes()
        if raw != second.read_bytes() or hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError("class selection receipt: JSON 重播或 SHA-256 不符")
        receipts.append(json.loads(raw))
    # 前 22 筆另以既有固定 steps 自身 identity 鎖定；新 inventory 只描述本階段事件。
    prefix = receipts[0]["events"][:22]
    if receipts[1]["events"][:22] != prefix or len(base_rows) != 7:
        raise ValueError("class selection receipt: 既有前綴不符")
    prefix_rows = [{"original_length": str(e["original_length"]), "original_sha256": e["original_sha256"],
                    "caller": f'{e["caller"]["segment"]:04X}:{e["caller"]["offset"]:04X}',
                    "background": str(e["background"]), "foreground": str(e["foreground"]),
                    "row": str(e["row"]), "column": str(e["column"])} for e in prefix]
    common = [{"queued_at": 100010000, "scan": 28, "ascii": 13}, {"queued_at": 100240000, "scan": 28, "ascii": 13},
              {"queued_at": 100400000, "scan": 28, "ascii": 13}]
    _validate_path(receipts[0], prefix_rows + lifecycle[:4], BASE_ENTRY + DOWN_UP_ENTRY, BASE_POST + DOWN_UP_POST,
                   common + [{"queued_at": 100650000, "scan": 80, "ascii": 0}, {"queued_at": 100720000, "scan": 72, "ascii": 0}])
    _validate_path(receipts[1], prefix_rows + lifecycle[4:], BASE_ENTRY + ESCAPE_ENTRY, BASE_POST + ESCAPE_POST,
                   common + [{"queued_at": 100650000, "scan": 1, "ascii": 27}])
    for first, second, expected in ((down_screen_a, down_screen_b, DOWN_UP_SCREEN_SHA),
                                    (escape_screen_a, escape_screen_b, ESCAPE_SCREEN_SHA)):
        raw = first.read_bytes()
        if len(raw) != 64000 or raw != second.read_bytes() or hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError("class selection receipt: framebuffer 重播、尺寸或 SHA-256 不符")
