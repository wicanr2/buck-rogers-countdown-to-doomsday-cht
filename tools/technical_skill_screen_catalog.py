#!/usr/bin/env python3
"""驗證技術技能配置畫面的 exact 靜態文字 catalog。"""

from __future__ import annotations

import csv
import re
from pathlib import Path
import unicodedata

import name_prompt_catalog
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name

EVENT_HEADER = name_prompt_catalog.EVENT_HEADER
TEXT_HEADER = name_prompt_catalog.TEXT_HEADER
IDENTITY = name_prompt_catalog.IDENTITY
STATIC_SOURCE_SEQUENCES = [2, 6, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]
MANUAL_TERMS = {
    "technical.screen.skills": "技術性技能",
    "technical.skill.repair_electrical": "電器設備維修",
    "technical.skill.repair_mechanical": "維修機械設備",
    "technical.skill.repair_nuclear_engine": "核能引擎維修",
    "technical.skill.repair_life_support": "維生設備維修",
    "technical.skill.repair_rocket_hull": "船體維修",
    "technical.skill.jury_rig": "緊急維修",
    "technical.skill.bypass_security": "破解保安系統",
    "technical.skill.open_lock": "開鎖",
    "technical.skill.commo_operation": "通訊操作",
    "technical.skill.sensor_operation": "操作掃瞄器",
    "technical.skill.demolitions": "爆破",
    "technical.skill.first_aid": "緊急救護",
    "technical.skill.repair_weapon": "武器維修",
}


HOTKEY_RE = re.compile(r"\(([^()])\)")


def hotkeys(text: str) -> list[str]:
    """半形括號熱鍵字母序列；規格 041 §3.7 非 zh-TW 只比結構與這些字母。"""
    return HOTKEY_RE.findall(text)


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate(events_path: Path, translations_path: Path, entry_path: Path,
             selection_path: Path, lang: str = DEFAULT_LANG) -> None:
    events = name_prompt_catalog.table(events_path, EVENT_HEADER, "technical-skill-screen-events.tsv")
    texts = name_prompt_catalog.table(translations_path, TEXT_HEADER, catalog_name("technical-skill-screen", lang))
    entry, selection = read_dicts(entry_path), read_dicts(selection_path)
    if (len(events) != 17 or len({row["event_key"] for row in events}) != 17 or
            [row["sequence"] for row in events] != [str(i) for i in range(1, 18)]):
        raise ValueError("技術技能新增事件必須恰有 17 筆且 sequence 連續")
    sources = [entry[index - 1] for index in STATIC_SOURCE_SEQUENCES] + [selection[4]]
    for event, source in zip(events, sources):
        if any(event[field] != source[field] for field in IDENTITY):
            raise ValueError(f"{event['event_key']}: identity 不符來源清冊")
        if (not name_prompt_catalog.HASH_RE.fullmatch(event["original_sha256"]) or
                not name_prompt_catalog.CALLER_RE.fullmatch(event["caller"])):
            raise ValueError(f"{event['event_key']}: hash 或 caller 格式不符")
    text_map = {row["key"]: row for row in texts}
    if len(text_map) != len(texts) or {row["text_key"] for row in events} != set(text_map):
        raise ValueError("技術技能 text key 重複、缺漏或含孤兒")
    for key, row in text_map.items():
        if not row["translation"] or row["source"] not in {"runtime-interface", "manual-and-runtime"}:
            raise ValueError(f"{key}: 譯文或來源無效")
        if (unicodedata.normalize("NFC", row["translation"]) != row["translation"] or
                any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in row["translation"])):
            raise ValueError(f"{key}: 譯文必須是 NFC 且不得含控制／格式字元")
    if lang == DEFAULT_LANG:
        for key, translation in MANUAL_TERMS.items():
            if text_map.get(key, {}).get("translation") != translation or text_map[key]["source"] != "manual-and-runtime":
                raise ValueError(f"{key}: 譯名不符中文手冊 SCAN0352_012.jpg")
    else:
        # 規格 041 §3.7：字面由產生器 --check 保證（等於 zh-TW 經同一轉換）；這裡只查結構與 (X) 字母。
        reference = {row["key"]: row for row in name_prompt_catalog.table(
            translations_path.parent / catalog_name("technical-skill-screen", DEFAULT_LANG), TEXT_HEADER,
            catalog_name("technical-skill-screen", DEFAULT_LANG))}
        for key in MANUAL_TERMS:
            if key not in text_map or text_map[key]["source"] != "manual-and-runtime":
                raise ValueError(f"{key}: 缺手冊譯名或來源不是 manual-and-runtime")
        for key, row in text_map.items():
            if key not in reference or row["source"] != reference[key]["source"]:
                raise ValueError(f"{key}: 與 zh-TW 結構不符")
            if hotkeys(row["translation"]) != hotkeys(reference[key]["translation"]):
                raise ValueError(f"{key}: (X) 熱鍵字母與 zh-TW 不同")
    dynamic = {(int(row["row"]), int(row["column"])) for row in entry
               if row["event_role"] == "technical_skill_screen" and int(row["column"]) in {23, 29, 35}}
    if not ({(1, 23), (2, 23)} | {(row, col) for row in range(6, 19) for col in (23, 29, 35)}) <= dynamic:
        raise ValueError("缺少技術技能剩餘點數或 points／bonus／total 動態邊界")
    keyed = {row["event_key"]: row["text_key"] for row in events}
    for skill in ("repair_electrical", "repair_mechanical"):
        if keyed[f"technical.screen.skill.{skill}.normal"] != keyed[f"technical.screen.skill.{skill}.selected"]:
            raise ValueError(f"{skill}: normal／selected 必須共用 text key")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("events_path", "translations_path", "entry_path", "selection_path"):
        parser.add_argument(name, type=Path)
    add_lang_argument(parser)
    validate(**vars(parser.parse_args()))
