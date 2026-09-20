#!/usr/bin/env python3
"""Verify deterministic Buck Rogers selected-row palette and pixel lifecycle receipts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import menu_events
import race_selection_receipt


TOP_FIELDS = {
    "tool", "state_sha256", "menu_events_sha256", "state_start", "stopped_at", "enter_at",
    "down_at", "sample_from", "sample_every",
    "samples", "events", "pending", "drops",
}
SAMPLE_FIELDS = {
    "step", "palette_sha256", "palette", "selected_contrast", "row3", "row4",
    "completed_events",
}
REGION_FIELDS = {"sha256", "counts"}
RGB_FIELDS = {"r", "g", "b"}
PALETTE_KEYS = {"0", "10", "13", "15"}

NORMAL_TERRAN = "0b66513fdfef40c4ec181a909b268e81b8c9e2086500b4828f4c8c4d2051334a"
SELECTED_TERRAN = "75ed8459bc4858aecf6ce82f2d9ddb91ca0597fec353a4146b62b3ac103462c7"
NORMAL_MARTIAN = "7f09284d2d5c6b62227bff167f080d0ba1ac70ff1ff0d503d3539164b00b9ba7"
SELECTED_MARTIAN = "5d6fe02f8c78a90bd883730f61aa0bcfde5531bd7dfcf82bcea626de5a53443f"


def _load_pair(path_a: Path, path_b: Path) -> dict:
    raw_a, raw_b = path_a.read_bytes(), path_b.read_bytes()
    if raw_a != raw_b:
        raise ValueError("blink receipt: 兩次重播不是逐 byte 相同")
    try:
        value = json.loads(raw_a)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("blink receipt: 不是有效 UTF-8 JSON") from exc
    if set(value) != TOP_FIELDS:
        raise ValueError("blink receipt: 頂層欄位不符")
    return value


def _validate_samples(receipt: dict, mode: str) -> None:
    if receipt["tool"] != "dosgolem/cmd/buckrogers-selection-blink-receipt":
        raise ValueError("blink receipt: tool 識別不符")
    if receipt["state_sha256"] != "cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164":
        raise ValueError("blink receipt: state SHA-256 不符")
    if receipt["menu_events_sha256"] != "973a6a1e247e7d9e16518a1a66266f340666d32e785f3f6f6652a890e830da2e":
        raise ValueError("blink receipt: menu events SHA-256 不符")
    if receipt["state_start"] != 99_999_999 or receipt["stopped_at"] != 110_000_000:
        raise ValueError("blink receipt: 執行範圍不符")
    if receipt["enter_at"] != 100_010_000 or receipt["sample_from"] != 100_220_000 or receipt["sample_every"] != 10_000:
        raise ValueError("blink receipt: Enter 或取樣排程不符")
    expected_down = 0 if mode == "steady" else 100_240_000
    if receipt["down_at"] != expected_down:
        raise ValueError("blink receipt: Down 排程不符")
    if receipt["pending"] is not False or receipt["drops"] != 0:
        raise ValueError("blink receipt: recorder pending／drop 不為零")
    samples = receipt["samples"]
    expected_steps = list(range(100_220_000, 110_000_000, 10_000))
    if len(samples) != 978 or [sample.get("step") for sample in samples] != expected_steps:
        raise ValueError("blink receipt: 取樣數或絕對 step 不符")
    palette_hashes: set[str] = set()
    for sample in samples:
        if set(sample) != SAMPLE_FIELDS or set(sample["palette"]) != PALETTE_KEYS:
            raise ValueError("blink receipt: sample schema 不符")
        if any(set(rgb) != RGB_FIELDS for rgb in sample["palette"].values()):
            raise ValueError("blink receipt: RGB schema 不符")
        if set(sample["row3"]) != REGION_FIELDS or set(sample["row4"]) != REGION_FIELDS:
            raise ValueError("blink receipt: region schema 不符")
        if sample["palette"]["0"] != {"r": 0, "g": 0, "b": 0} or sample["palette"]["15"] != {"r": 0, "g": 0, "b": 0}:
            raise ValueError("blink receipt: palette 0／15 不再同為黑色")
        if sample["palette"]["10"] != {"r": 85, "g": 255, "b": 85} or sample["palette"]["13"] != {"r": 255, "g": 85, "b": 255}:
            raise ValueError("blink receipt: normal／prompt 色彩不符")
        if sample["selected_contrast"] is not False:
            raise ValueError("blink receipt: selected palette 出現未核准 contrast")
        palette_hashes.add(sample["palette_sha256"])
    if len(palette_hashes) != 1:
        raise ValueError("blink receipt: 長窗口 palette 發生變化")

    if mode == "steady":
        if len(receipt["events"]) != 9:
            raise ValueError("blink receipt: steady 必須恰有九事件")
        stable = [sample for sample in samples if sample["step"] >= 100_230_000]
        want3, want4, completed = SELECTED_TERRAN, NORMAL_MARTIAN, 9
    else:
        if len(receipt["events"]) != 11:
            raise ValueError("blink receipt: Down 必須恰有十一事件")
        stable = [sample for sample in samples if sample["step"] >= 100_260_000]
        want3, want4, completed = NORMAL_TERRAN, SELECTED_MARTIAN, 11
    if not stable or any(
        sample["row3"]["sha256"] != want3
        or sample["row4"]["sha256"] != want4
        or sample["completed_events"] != completed
        for sample in stable
    ):
        raise ValueError("blink receipt: 選取後穩定區域或事件數發生變化")


def _validate_events(receipt: dict, menu_path: Path, catalog_path: Path, mode: str) -> None:
    menu_events.validate(menu_path, catalog_path)
    with menu_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    inventory = {row["event_key"]: row for row in rows}
    expected = rows[:9]
    if mode == "down":
        expected += [
            inventory["race.selection.normal.terran"],
            inventory["race.selection.selected.martian"],
        ]
    if len(receipt["events"]) != len(expected):
        raise ValueError("blink receipt: event 數不符")
    previous = -1
    for index, (event, row) in enumerate(zip(receipt["events"], expected), 1):
        if not race_selection_receipt._event_matches(event, row):
            raise ValueError(f"blink receipt: 第 {index} 筆 event identity 不符")
        if not previous < event["entry_step"] < event["post_call_step"]:
            raise ValueError(f"blink receipt: 第 {index} 筆 event 時序不符")
        previous = event["post_call_step"]


def verify(
    steady_a: Path, steady_b: Path, down_a: Path, down_b: Path,
    menu_path: Path, catalog_path: Path,
) -> None:
    steady = _load_pair(steady_a, steady_b)
    down = _load_pair(down_a, down_b)
    _validate_samples(steady, "steady")
    _validate_samples(down, "down")
    _validate_events(steady, menu_path, catalog_path, "steady")
    _validate_events(down, menu_path, catalog_path, "down")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    for name in ("steady_a", "steady_b", "down_a", "down_b", "menu", "catalog"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    verify(args.steady_a, args.steady_b, args.down_a, args.down_b, args.menu, args.catalog)
