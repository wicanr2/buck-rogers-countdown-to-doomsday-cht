#!/usr/bin/env python3
"""驗證職業技能配置畫面的 exact 靜態文字 catalog。"""

from __future__ import annotations

import csv
from pathlib import Path
import unicodedata

import name_prompt_catalog
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name

EVENT_HEADER = name_prompt_catalog.EVENT_HEADER
TEXT_HEADER = name_prompt_catalog.TEXT_HEADER
IDENTITY = name_prompt_catalog.IDENTITY
STATIC_SOURCE_SEQUENCES = [2, 4, 6, 7, 8, 12, 16, 20, 24, 28, 32, 36, 40]


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate(events_path: Path, translations_path: Path, confirm_path: Path,
             selection_path: Path, character_text_path: Path, lang: str = DEFAULT_LANG) -> None:
    events = name_prompt_catalog.table(events_path, EVENT_HEADER, "career-skill-screen-events.tsv")
    texts = name_prompt_catalog.table(translations_path, TEXT_HEADER, catalog_name("career-skill-screen", lang))
    confirm = read_dicts(confirm_path)
    selection = read_dicts(selection_path)
    character_texts = {row["key"]: row for row in read_dicts(character_text_path)}
    if (len(events) != 14 or len({row["event_key"] for row in events}) != 14 or
            [row["sequence"] for row in events] != [str(i) for i in range(1, 15)]):
        raise ValueError("職業技能靜態事件必須恰有 14 筆且 sequence 連續")
    sources = [confirm[index - 1] for index in STATIC_SOURCE_SEQUENCES]
    sources.append(selection[4])
    if len(sources) != len(events):
        raise ValueError("職業技能來源事件數不符")
    for event, source in zip(events, sources):
        if any(event[field] != source[field] for field in IDENTITY):
            raise ValueError(f"{event['event_key']}: identity 不符來源清冊")
        if (not name_prompt_catalog.HASH_RE.fullmatch(event["original_sha256"]) or
                not name_prompt_catalog.CALLER_RE.fullmatch(event["caller"])):
            raise ValueError(f"{event['event_key']}: hash 或 caller 格式不符")
    text_map = {row["key"]: row for row in texts}
    if len(text_map) != len(texts) or {row["text_key"] for row in events} != set(text_map):
        raise ValueError("職業技能 text key 重複、缺漏或含孤兒")
    for key, row in text_map.items():
        if not row["translation"] or row["source"] not in {"runtime-interface", "manual-and-runtime"}:
            raise ValueError(f"{key}: 譯文或來源無效")
        if (unicodedata.normalize("NFC", row["translation"]) != row["translation"] or
                any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in row["translation"])):
            raise ValueError(f"{key}: 譯文必須是 NFC 且不得含控制／格式字元")
        if key.startswith("character.skill."):
            canonical = character_texts.get(key)
            if canonical is None or (row["translation"], row["source"]) != (
                    canonical["translation"], canonical["source"]):
                raise ValueError(f"{key}: 技能譯名不符既有正式 catalog")
    dynamic_positions = {(int(row["row"]), int(row["column"])) for row in confirm
                         if row["event_role"] == "skill_allocation_screen" and int(row["column"]) in {23, 29, 35}}
    if not {(1, 23), (2, 23), (6, 23), (6, 29), (6, 35)} <= dynamic_positions:
        raise ValueError("缺少剩餘點數或技能數值動態邊界")
    keyed = {row["event_key"]: row["text_key"] for row in events}
    if (keyed["career.screen.skill.notice.normal"] != keyed["career.screen.skill.notice.selected"] or
            keyed["career.screen.skill.maneuver_zero_g.normal"] !=
            keyed["career.screen.skill.maneuver_zero_g.selected"]):
        raise ValueError("normal／selected variant 必須共用技能 text key")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("events_path", "translations_path", "confirm_path", "selection_path", "character_text_path"):
        parser.add_argument(name, type=Path)
    add_lang_argument(parser)
    validate(**vars(parser.parse_args()))
