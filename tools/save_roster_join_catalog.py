#!/usr/bin/env python3
"""驗證保存→名冊→加入事件清冊與新增繁中 catalog。"""

from __future__ import annotations

import csv
import hashlib
import io
import re
from pathlib import Path

from catalog_font import CatalogError, read_catalog
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name


EVENT_HEADER = ["event_key", "sequence", "event_role", "translation_key", "inference_level",
                "entry_step", "post_call_step", "original_length", "original_sha256", "caller",
                "background", "foreground", "row", "column"]
ROLES = {"existing_static", "new_static", "dynamic_character_name"}
NEW_KEYS = {"roster.add_prompt", "roster.loading"}
EXISTING_KEYS = {"menu.create_new_character", "menu.add_character_to_team", "menu.load_saved_game",
                 "menu.joystick_mouse_initialize", "menu.exit_to_dos", "menu.choose_function"}
RUNTIME_HEADER = ["event_key", "sequence", "text_key", "original_length", "original_sha256",
                  "caller", "background", "foreground", "row", "column"]
EVENTS_SHA256 = "f178fae862f42eb6cc901251b97f2deea8dfa943ae17456f28208fee81adbcec"
CALLER = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _decode(path: Path) -> str:
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: 不是有效 UTF-8") from exc
    if text.startswith("\ufeff"):
        raise ValueError(f"{path}: 不允許 UTF-8 BOM")
    return text


def validate(events_path: Path, catalog_path: Path, menu_catalog_path: Path | None = None,
             runtime_events_path: Path | None = None, runtime_rects_path: Path | None = None) -> None:
    event_bytes = events_path.read_bytes()
    if hashlib.sha256(event_bytes).hexdigest() != EVENTS_SHA256:
        raise ValueError("事件清冊與第五十四階段 exact identity 基線不符")
    rows = list(csv.reader(io.StringIO(_decode(events_path)), delimiter="\t", strict=True))
    if not rows or rows[0] != EVENT_HEADER:
        raise ValueError("事件清冊標頭不符")
    if len(rows) != 19:
        raise ValueError("事件清冊必須恰有 18 筆事件")
    seen_events: set[str] = set()
    new_keys: set[str] = set()
    static_keys: set[str] = set()
    dynamic = 0
    for index, row in enumerate(rows[1:], 1):
        if len(row) != len(EVENT_HEADER):
            raise ValueError(f"事件第 {index} 筆欄數不符")
        key, sequence, role, translation_key, level, entry, post, length, digest, caller, bg, fg, y, x = row
        if key in seen_events:
            raise ValueError(f"重複事件 key：{key}")
        seen_events.add(key)
        if int(sequence) != index or role not in ROLES or level != "confirmed":
            raise ValueError(f"事件第 {index} 筆分類或序號不符")
        if int(entry) >= int(post) or int(length) < 1 or not SHA256.fullmatch(digest) or not CALLER.fullmatch(caller):
            raise ValueError(f"事件第 {index} 筆 identity 不合法")
        for value, maximum in ((bg, 15), (fg, 15), (y, 24), (x, 39)):
            if not 0 <= int(value) <= maximum:
                raise ValueError(f"事件第 {index} 筆幾何或色號越界")
        if role == "dynamic_character_name":
            dynamic += 1
            if translation_key:
                raise ValueError("動態角色名不得進入翻譯 catalog")
        elif not translation_key:
            raise ValueError("靜態事件缺少 translation_key")
        else:
            static_keys.add(translation_key)
        if role == "new_static":
            new_keys.add(translation_key)
    if dynamic != 4 or new_keys != NEW_KEYS:
        raise ValueError("動態事件數或新增靜態 key 集合不符")
    if static_keys != NEW_KEYS | EXISTING_KEYS:
        raise ValueError("完整路徑的靜態 key 集合不符")

    try:
        entries = read_catalog(catalog_path)
    except CatalogError as exc:
        raise ValueError(str(exc)) from exc
    catalog_keys = {entry.key for entry in entries}
    if catalog_keys != NEW_KEYS:
        raise ValueError("新增 catalog 有漏譯或孤兒 key")
    if any(entry.source != "runtime-interface" for entry in entries):
        raise ValueError("新增譯文來源必須是 runtime-interface")
    if menu_catalog_path is not None:
        try:
            menu_keys = {entry.key for entry in read_catalog(menu_catalog_path)}
        except CatalogError as exc:
            raise ValueError(str(exc)) from exc
        if not EXISTING_KEYS <= menu_keys:
            raise ValueError("既有功能選單 catalog 缺少本路徑靜態 key")
    if runtime_events_path is not None:
        runtime_rows = list(csv.reader(io.StringIO(_decode(runtime_events_path)), delimiter="\t", strict=True))
        if not runtime_rows or runtime_rows[0] != RUNTIME_HEADER or len(runtime_rows) != 3:
            raise ValueError("runtime 事件表必須是兩筆 exact identity")
        if [row[2] for row in runtime_rows[1:]] != ["roster.add_prompt", "roster.loading"]:
            raise ValueError("runtime 事件表 key 或順序不符")
        expected = {
            ("17", "adfe0feb6f39631e4b7b14a12d9407e0af2a1bc12fc72dad2c1b879ca781ef90", "37F1:101E", "0", "13", "24", "0"),
            ("21", "e920b38b45dd6a828b466a06f4c4c4f63645f1c6a82e488599dc3da46b5280f2", "0763:1307", "0", "10", "24", "0"),
        }
        actual = {(row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in runtime_rows[1:]}
        if actual != expected:
            raise ValueError("runtime 事件 identity 與完整清冊不符")
        if runtime_rects_path is not None:
            rects = list(csv.reader(io.StringIO(_decode(runtime_rects_path)), delimiter="\t", strict=True))
            want_header = ["event_key", "x", "y", "width", "height", "draw_x", "draw_y",
                           "capacity_cells", "line_count", "overflow_policy"]
            if not rects or rects[0] != want_header or len(rects) != 3:
                raise ValueError("runtime 安全矩形 schema 或筆數不符")
            event_by_key = {row[0]: row for row in runtime_rows[1:]}
            for row in rects[1:]:
                event = event_by_key.get(row[0])
                if event is None:
                    raise ValueError("安全矩形含孤兒 event_key")
                x, y, width, height, draw_x, draw_y, capacity, lines = map(int, row[1:9])
                if (x, y, width, height) != (int(event[9]) * 8, int(event[8]) * 8,
                                             int(event[3]) * 8, 8):
                    raise ValueError("安全矩形未由 dispatcher 幾何精確導出")
                if (draw_x, draw_y, capacity, lines, row[9]) != (x, y, int(event[3]), 1,
                                                                  "single-line-reject"):
                    raise ValueError("安全矩形 draw／容量契約不符")


def verify_known_dynamic_bytes() -> None:
    expected = {
        b"A" + b" " * 14: "f7872bdce8d40b314454ee51a0bbe13fe4c4ccb5d19d6b1299ac7d1a9ddab60c",
        b"A": "559aead08264d5795d3909718cdd05abd49572e84fe55590eef31a88a08fdffd",
        b"* A": "d60b849846dd57b81aeb8f3b6e545341c143750c10c36c6681532e25ad9edcfb",
    }
    for raw, digest in expected.items():
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError("動態角色名 fixture 雜湊不符")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    add_lang_argument(parser)
    lang = parser.parse_args().lang
    root = Path(__file__).resolve().parents[1]
    verify_known_dynamic_bytes()
    validate(root / "text/save-roster-join-events.tsv", root / "text" / catalog_name("save-roster-join", lang),
             root / "text" / catalog_name("menu", lang), root / "text/save-roster-join-runtime-events.tsv",
             root / "text/save-roster-join-text-safe-rects.tsv")
    print("保存→名冊→加入繁中 catalog：通過")
