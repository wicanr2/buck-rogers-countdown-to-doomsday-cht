#!/usr/bin/env python3
"""Verify deterministic race-selection lifecycle and indexed framebuffer receipts."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re

import menu_events


SELECTION_HEADER = [
    "sequence", "input_phase", "event_role", "text_key", "original_length",
    "original_sha256", "caller", "background", "foreground", "row", "column",
]
EVENT_FIELDS = {
    "entry_step", "post_call_step", "caller", "original_length", "original_sha256",
    "background", "foreground", "row", "column",
}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")


def _selection_rows(path: Path, catalog_keys: set[str]) -> list[dict[str, str]]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("race-selection-events.tsv: 不得含 BOM")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("race-selection-events.tsv: 不是有效 UTF-8") from exc
    raw = list(csv.reader(text.splitlines(), delimiter="\t"))
    if not raw or raw[0] != SELECTION_HEADER:
        raise ValueError("race-selection-events.tsv: 標頭不符")
    rows = [dict(zip(SELECTION_HEADER, row)) for row in raw[1:] if len(row) == len(SELECTION_HEADER)]
    if len(rows) != 4 or len(raw) != 5:
        raise ValueError("race-selection-events.tsv: 必須恰有四筆完整事件")
    for index, row in enumerate(rows, 1):
        if row["sequence"] != str(index):
            raise ValueError("race-selection-events.tsv: sequence 不連續")
        expected_phase = "down" if index <= 2 else "up"
        expected_role = "unselect-old" if index % 2 else "select-new"
        if row["input_phase"] != expected_phase or row["event_role"] != expected_role:
            raise ValueError("race-selection-events.tsv: lifecycle 順序不符")
        if row["text_key"] not in catalog_keys:
            raise ValueError("race-selection-events.tsv: text key 不在 catalog")
        if not HASH_RE.fullmatch(row["original_sha256"]) or not CALLER_RE.fullmatch(row["caller"]):
            raise ValueError("race-selection-events.tsv: hash 或 caller 格式不符")
        for name in ("original_length", "background", "foreground", "row", "column"):
            if not row[name].isascii() or not row[name].isdigit() or not 0 <= int(row[name]) <= 255:
                raise ValueError(f"race-selection-events.tsv: {name} 無效")
    return rows


def _event_matches(event: dict, row: dict[str, str]) -> bool:
    if set(event) != EVENT_FIELDS or set(event["caller"]) != {"segment", "offset"}:
        return False
    caller = f'{event["caller"]["segment"]:04X}:{event["caller"]["offset"]:04X}'
    return (
        caller == row["caller"]
        and event["original_length"] == int(row["original_length"])
        and event["original_sha256"] == row["original_sha256"]
        and event["background"] == int(row["background"])
        and event["foreground"] == int(row["foreground"])
        and event["row"] == int(row["row"])
        and event["column"] == int(row["column"])
    )


def verify(
    receipt_a: Path, receipt_b: Path, selection_path: Path, menu_path: Path,
    catalog_path: Path, steady_screen: Path, down_screen: Path, up_screen: Path,
) -> None:
    menu_events.validate(menu_path, catalog_path)
    with catalog_path.open(encoding="utf-8", newline="") as stream:
        catalog_keys = {row["key"] for row in csv.DictReader(stream, delimiter="\t")}
    selection = _selection_rows(selection_path, catalog_keys)
    a = json.loads(receipt_a.read_text(encoding="utf-8"))
    b = json.loads(receipt_b.read_text(encoding="utf-8"))
    if a != b:
        raise ValueError("selection receipt: 兩次重播不一致")
    if set(a) != {"state_start", "stopped_at", "bios_input", "bios_keys", "events"}:
        raise ValueError("selection receipt: 頂層欄位不符")
    if a["state_start"] != 99_999_999 or a["stopped_at"] != 100_600_000:
        raise ValueError("selection receipt: 執行範圍不符")
    if a["bios_keys"] != [
        {"queued_at": 100_010_000, "scan": 0x1C, "ascii": 0x0D},
        {"queued_at": 100_240_000, "scan": 0x50, "ascii": 0},
        {"queued_at": 100_300_000, "scan": 0x48, "ascii": 0},
    ]:
        raise ValueError("selection receipt: BIOS 排程不符")
    events = a["events"]
    if len(events) != 13:
        raise ValueError("selection receipt: 必須是初始九筆加四筆 selection 事件")
    previous_post = events[8]["post_call_step"]
    for index, (event, row) in enumerate(zip(events[9:], selection), 10):
        if not _event_matches(event, row):
            raise ValueError(f"selection receipt: 第 {index} 筆 identity 不符")
        if not previous_post < event["entry_step"] < event["post_call_step"]:
            raise ValueError(f"selection receipt: 第 {index} 筆順序不符")
        previous_post = event["post_call_step"]

    steady, down, up = (path.read_bytes() for path in (steady_screen, down_screen, up_screen))
    if any(len(screen) != 320 * 200 for screen in (steady, down, up)):
        raise ValueError("selection receipt: framebuffer 必須是 64,000 bytes")
    if steady != up:
        raise ValueError("selection receipt: Down→Up 未逐位元回到 steady")
    changed = [index for index, (old, new) in enumerate(zip(steady, down)) if old != new]
    if len(changed) != 832:
        raise ValueError("selection receipt: steady／Down 像素差數不符")
    xs, ys = [index % 320 for index in changed], [index // 320 for index in changed]
    if (min(xs), min(ys), max(xs), max(ys)) != (24, 24, 79, 39):
        raise ValueError("selection receipt: steady／Down 差異矩形不符")
    expected_hashes = (
        "d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd",
        "efaa3d88ea3c1f05aff308b86f796c4634845304c63eb5c92cc7e1d0a1a278d0",
        "d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd",
    )
    actual_hashes = tuple(hashlib.sha256(screen).hexdigest() for screen in (steady, down, up))
    if actual_hashes != expected_hashes:
        raise ValueError("selection receipt: framebuffer SHA-256 不符")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    for name in ("receipt_a", "receipt_b", "selection", "menu", "catalog", "steady", "down", "up"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    verify(args.receipt_a, args.receipt_b, args.selection, args.menu, args.catalog, args.steady, args.down, args.up)
