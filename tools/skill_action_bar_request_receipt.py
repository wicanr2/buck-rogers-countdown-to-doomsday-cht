#!/usr/bin/env python3
"""驗證 Phase 76 技能操作列顯示請求與非干擾收據。"""
from __future__ import annotations
import argparse, json
from pathlib import Path

RUNES = {"action.add": 2, "action.subtract": 2, "action.prev": 2, "action.next": 2, "action.done": 2}
PATHS = ["career-base", "career-subtract", "career-done", "technical-base", "technical-subtract", "technical-prev", "technical-next", "technical-done"]

def without_requests(receipt: dict) -> dict:
    result = dict(receipt)
    for key in ("action_bar_requests", "action_bar_catalog_misses"):
        result.pop(key, None)
    return result

def validate(root: Path) -> int:
    for name in PATHS:
        a_path, b_path = root / f"{name}-a.json", root / f"{name}-b.json"
        if a_path.read_bytes() != b_path.read_bytes(): raise ValueError(f"{name}: A/B JSON 不一致")
        a = json.loads(a_path.read_text()); control = json.loads((root / f"{name}-control.json").read_text())
        if without_requests(a) != control: raise ValueError(f"{name}: request 改變原版語意收據")
        if a.get("action_bar_catalog_misses") != 0: raise ValueError(f"{name}: catalog miss")
        events, requests = a.get("action_bar_events", []), a.get("action_bar_requests", [])
        if len(events) != len(requests): raise ValueError(f"{name}: event/request 數不一致")
        for event, request in zip(events, requests, strict=True):
            text_key = event["event_key"].split(".", 1)[1].rsplit(".", 1)[0]
            if request != {"event_key": event["event_key"], "text_key": text_key, "translation_runes": RUNES[text_key]}:
                raise ValueError(f"{name}: request identity 漂移")
        for suffix in ("a", "b", "control"):
            if (root / f"{name}-{suffix}.screen").stat().st_size != 64000: raise ValueError(f"{name}: framebuffer 大小錯誤")
        if (root / f"{name}-a.screen").read_bytes() != (root / f"{name}-b.screen").read_bytes() or (root / f"{name}-a.screen").read_bytes() != (root / f"{name}-control.screen").read_bytes():
            raise ValueError(f"{name}: framebuffer 漂移")
    return len(PATHS)

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("receipt_root", type=Path); args = parser.parse_args()
    print(f"validated {validate(args.receipt_root)} action-bar request paths")
if __name__ == "__main__": main()
