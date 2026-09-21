#!/usr/bin/env python3
"""驗證姓名固定提示命中、玩家輸入未命中，以及兩次重播決定性。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PROMPT_HASH = "246a64eabf869f90773d848870a32766bc838b7e766d88fce33dfa4e99d06676"
ECHO_HASH = "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: 收據根節點必須是物件")
    return value


def validate_pair(first_path: Path, second_path: Path, *, events: int, misses: int,
                  stopped_at: int, expect_echo: bool) -> None:
    first, second = load(first_path), load(second_path)
    if first != second:
        raise ValueError("相同輸入重播的 JSON 收據不一致")
    if first.get("stopped_at") != stopped_at or len(first.get("events", [])) != events:
        raise ValueError("停止步數或事件數不符")
    if first.get("catalog_misses") != misses:
        raise ValueError("catalog miss 數不符")
    if first.get("requests") != [{
        "event_key": "character.name.prompt",
        "text_key": "character.name.prompt",
        "translation_runes": 5,
    }]:
        raise ValueError("姓名提示顯示請求不符")
    prompts = [event for event in first["events"] if event["original_sha256"] == PROMPT_HASH]
    if len(prompts) != 1 or prompts[0] != {
        "entry_step": 101919217,
        "post_call_step": 101931640,
        "caller": {"segment": 1891, "offset": 2086},
        "original_length": 16,
        "original_sha256": PROMPT_HASH,
        "background": 0,
        "foreground": 13,
        "row": 24,
        "column": 0,
    }:
        raise ValueError("姓名提示事件 identity 不符")
    echoes = [event for event in first["events"] if event["original_sha256"] == ECHO_HASH]
    if bool(echoes) != expect_echo:
        raise ValueError("玩家輸入 echo 的存在性不符")
    if expect_echo and (len(echoes) != 1 or echoes[0]["original_length"] != 1
                        or echoes[0]["caller"] != {"segment": 1891, "offset": 2479}):
        raise ValueError("玩家輸入 echo identity 不符")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n_first", type=Path)
    parser.add_argument("n_second", type=Path)
    parser.add_argument("a_first", type=Path)
    parser.add_argument("a_second", type=Path)
    args = parser.parse_args()
    validate_pair(args.n_first, args.n_second, events=183, misses=182,
                  stopped_at=102000000, expect_echo=False)
    validate_pair(args.a_first, args.a_second, events=184, misses=183,
                  stopped_at=102100000, expect_echo=True)


if __name__ == "__main__":
    main()
