#!/usr/bin/env python3
"""驗證 Phase 75 技能底部操作列 watcher 的雙重播與非干擾收據。"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


PATHS = {
    "career-base": [("career", "action.add", "focus"), ("career", "action.subtract", "normal"), ("career", "action.done", "normal")],
    "career-subtract": [("career", "action.add", "normal"), ("career", "action.subtract", "focus"), ("career", "action.done", "normal")],
    "career-done": [("career", "action.add", "normal"), ("career", "action.subtract", "normal"), ("career", "action.done", "focus")],
    "technical-base": [("technical", "action.add", "focus"), ("technical", "action.subtract", "normal"), ("technical", "action.prev", "normal"), ("technical", "action.next", "normal"), ("technical", "action.done", "normal")],
    "technical-subtract": [("technical", "action.add", "normal"), ("technical", "action.subtract", "focus"), ("technical", "action.prev", "normal"), ("technical", "action.next", "normal"), ("technical", "action.done", "normal")],
    "technical-prev": [("technical", "action.add", "normal"), ("technical", "action.subtract", "normal"), ("technical", "action.prev", "focus"), ("technical", "action.next", "normal"), ("technical", "action.done", "normal")],
    "technical-next": [("technical", "action.add", "normal"), ("technical", "action.subtract", "normal"), ("technical", "action.prev", "normal"), ("technical", "action.next", "focus"), ("technical", "action.done", "normal")],
    "technical-done": [("technical", "action.add", "normal"), ("technical", "action.subtract", "normal"), ("technical", "action.prev", "normal"), ("technical", "action.next", "normal"), ("technical", "action.done", "focus")],
}


def load_catalog(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return {(row["screen"], row["key"]): row for row in rows}


def without_action(receipt: dict) -> dict:
    copy = dict(receipt)
    for key in ("action_bar_events", "action_bar_misses", "action_bar_drops"):
        copy.pop(key, None)
    return copy


def validate(root: Path, catalog_path: Path) -> int:
    catalog = load_catalog(catalog_path)
    career_initial = PATHS["career-base"]
    checked = 0
    for name, terminal in PATHS.items():
        a_path, b_path = root / f"{name}-a.json", root / f"{name}-b.json"
        control_path = root / f"{name}-control.json"
        if a_path.read_bytes() != b_path.read_bytes():
            raise ValueError(f"{name}: watcher A/B JSON 不一致")
        a, control = json.loads(a_path.read_text()), json.loads(control_path.read_text())
        if without_action(a) != without_action(control):
            raise ValueError(f"{name}: watcher 改變原版語意收據")
        for suffix in ("a", "b", "control"):
            screen = root / f"{name}-{suffix}.screen"
            if screen.stat().st_size != 64000:
                raise ValueError(f"{name}-{suffix}: framebuffer 大小錯誤")
        if (root / f"{name}-a.screen").read_bytes() != (root / f"{name}-b.screen").read_bytes() or (root / f"{name}-a.screen").read_bytes() != (root / f"{name}-control.screen").read_bytes():
            raise ValueError(f"{name}: watcher/control framebuffer 不一致")
        if a.get("action_bar_misses") != 0 or a.get("action_bar_drops") != 0:
            raise ValueError(f"{name}: 不允許 miss/drop")

        expected_groups = [career_initial]
        if name.startswith("career-"):
            order = ["career-base", "career-subtract", "career-done"]
            expected_groups = [PATHS[item] for item in order[: order.index(name) + 1]]
        else:
            order = ["technical-base", "technical-subtract", "technical-prev", "technical-next", "technical-done"]
            expected_groups += [PATHS[item] for item in order[: order.index(name) + 1]]
        expected = [item for group in expected_groups for item in group]
        events = a.get("action_bar_events", [])
        if len(events) != len(expected):
            raise ValueError(f"{name}: events={len(events)} want={len(expected)}")
        for i, (event, identity) in enumerate(zip(events, expected, strict=True)):
            screen, key, variant = identity
            row = catalog[(screen, key)]
            want_key = f"{screen}.{key}.{variant}"
            numeric = (int(row["original_length"]), int(row["row"]), int(row["column"]), int(row["x0"]), int(row["y0"]), int(row["x1"]), int(row["y1"]))
            got_numeric = (event["original_length"], event["row"], event["column"], event["x0"], event["y0"], event["x1"], event["y1"])
            if event["screen"] != screen or event["event_key"] != want_key or event["variant"] != variant:
                raise ValueError(f"{name}: event {i} identity 漂移")
            if event["original_sha256"] != row["original_sha256"] or got_numeric != numeric:
                raise ValueError(f"{name}: event {i} hash/geometry 漂移")
            if event["post_call_step"] <= event["entry_step"]:
                raise ValueError(f"{name}: event {i} 沒有 guarded post-call")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt_root", type=Path)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    print(f"validated {validate(args.receipt_root, args.catalog)} action-bar runtime paths")


if __name__ == "__main__":
    main()
