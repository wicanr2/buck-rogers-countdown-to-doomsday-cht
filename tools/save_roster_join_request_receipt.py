#!/usr/bin/env python3
"""驗證保存→名冊→加入隊伍的執行期繁中顯示請求收據。"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name


ROOT_KEYS = {"state_start", "stopped_at", "events", "requests", "catalog_misses", "bios_keys",
             "scratch", "writes", "file_ops"}
EVENT_KEYS = {"entry_step", "post_call_step", "caller", "original_length", "original_sha256",
              "background", "foreground", "row", "column"}
REQUEST_KEYS = {"event_key", "text_key", "translation_runes"}


def _tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _identity(row: dict) -> tuple:
    caller = row["caller"]
    if isinstance(caller, dict):
        caller = f'{caller["segment"]:04X}:{caller["offset"]:04X}'
    return (int(row["original_length"]), row["original_sha256"], caller,
            int(row["background"]), int(row["foreground"]), int(row["row"]), int(row["column"]))


def validate(receipt: dict, baseline: dict, full_events: Path, menu_events: Path,
             roster_events: Path, menu_catalog: Path, roster_catalog: Path) -> None:
    if set(receipt) != ROOT_KEYS:
        raise ValueError("收據頂層 schema 不符")
    if receipt["state_start"] != 119_800_000 or receipt["stopped_at"] != 122_400_000:
        raise ValueError("收據起訖步數不符")
    if receipt["catalog_misses"] != 4 or len(receipt["events"]) != 18 or len(receipt["requests"]) != 14:
        raise ValueError("事件／請求／miss 數量不符")
    if any(set(event) != EVENT_KEYS for event in receipt["events"]):
        raise ValueError("事件 schema 不符")
    if any(set(request) != REQUEST_KEYS for request in receipt["requests"]):
        raise ValueError("請求 schema 不符")

    inventory = _tsv(full_events)
    if [_identity(event) for event in receipt["events"]] != [_identity(row) for row in inventory]:
        raise ValueError("18 筆事件 identity 或順序漂移")

    translations = {}
    for path in (menu_catalog, roster_catalog):
        for row in _tsv(path):
            translations[row["key"]] = row["translation"]
    resolver = {}
    for path in (menu_events, roster_events):
        for row in _tsv(path):
            resolver[_identity(row)] = (row["event_key"], row["text_key"])

    expected = []
    dynamic = 0
    for event, row in zip(receipt["events"], inventory, strict=True):
        resolved = resolver.get(_identity(event))
        if row["event_role"] == "dynamic_character_name":
            dynamic += 1
            if resolved is not None:
                raise ValueError("動態角色名不得被 catalog 解析")
            continue
        if resolved is None:
            raise ValueError("靜態事件沒有顯示請求 mapping")
        event_key, text_key = resolved
        expected.append({"event_key": event_key, "text_key": text_key,
                         "translation_runes": len(translations[text_key])})
    if dynamic != 4 or receipt["requests"] != expected:
        raise ValueError("動態隔離或顯示請求序列不符")

    for key in ("state_start", "stopped_at", "events", "bios_keys", "writes", "file_ops"):
        if receipt[key] != baseline[key]:
            raise ValueError(f"catalog 模式改變原版語意欄位：{key}")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("baseline", type=Path)
    add_lang_argument(parser)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    validate(json.loads(args.receipt.read_bytes()), json.loads(args.baseline.read_bytes()),
             root / "text/save-roster-join-events.tsv", root / "text/menu-events.tsv",
             root / "text/save-roster-join-runtime-events.tsv", root / "text" / catalog_name("menu", args.lang),
             root / "text" / catalog_name("save-roster-join", args.lang))
    print("保存→名冊→加入顯示請求收據：通過")


if __name__ == "__main__":
    main()
