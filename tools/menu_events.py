#!/usr/bin/env python3
"""Validate content-free Buck Rogers menu event identities."""

from __future__ import annotations

import csv
from pathlib import Path
import re
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name


HEADER = [
    "event_key", "sequence", "text_key", "original_length", "original_sha256",
    "caller", "background", "foreground", "row", "column",
]
CATALOG_HEADER = ["key", "translation", "source"]
KEY_RE = re.compile(r"^[a-z0-9]+(?:[._][a-z0-9]+)*$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")


def _rows(path: Path, header: list[str]) -> list[list[str]]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path}: 不得含 UTF-8 BOM")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: 不是有效 UTF-8") from exc
    rows = list(csv.reader(text.splitlines(), delimiter="\t"))
    if not rows or rows[0] != header:
        raise ValueError(f"{path}: 標頭必須精確為 {header}")
    for line, row in enumerate(rows[1:], 2):
        if len(row) != len(header):
            raise ValueError(f"{path}:{line}: 欄位數錯誤")
    return rows[1:]


def validate(events_path: Path, catalog_path: Path, lang: str = DEFAULT_LANG) -> None:
    events = _rows(events_path, HEADER)
    catalog = _rows(catalog_path, CATALOG_HEADER)
    if not events:
        raise ValueError("menu-events.tsv: 不得為空")

    event_keys: set[str] = set()
    identities: set[tuple[str, ...]] = set()
    used_text_keys: set[str] = set()
    for expected_sequence, row in enumerate(events, 1):
        event_key, sequence, text_key, length, digest, caller, bg, fg, y, x = row
        if not KEY_RE.fullmatch(event_key) or event_key in event_keys:
            raise ValueError(f"menu-events.tsv: 無效或重複 event_key {event_key!r}")
        if sequence != str(expected_sequence):
            raise ValueError("menu-events.tsv: sequence 必須由 1 起連續")
        if not KEY_RE.fullmatch(text_key):
            raise ValueError(f"menu-events.tsv: 無效 text_key {text_key!r}")
        try:
            n, background, foreground, row_no, column = map(int, (length, bg, fg, y, x))
        except ValueError as exc:
            raise ValueError("menu-events.tsv: 數值欄必須為十進位整數") from exc
        if not 1 <= n <= 255 or not HASH_RE.fullmatch(digest):
            raise ValueError("menu-events.tsv: 原文長度或 SHA-256 無效")
        if not CALLER_RE.fullmatch(caller):
            raise ValueError("menu-events.tsv: caller 必須為大寫 4 位 segment:offset")
        if not (0 <= background <= 255 and 0 <= foreground <= 255):
            raise ValueError("menu-events.tsv: 色號超界")
        if not (0 <= row_no <= 24 and 0 <= column <= 39):
            raise ValueError("menu-events.tsv: 文字格座標超界")
        identity = (digest, length, caller, bg, fg, y, x)
        if identity in identities:
            raise ValueError("menu-events.tsv: 重複 runtime identity")
        event_keys.add(event_key)
        identities.add(identity)
        used_text_keys.add(text_key)

    catalog_keys = [row[0] for row in catalog]
    if len(set(catalog_keys)) != len(catalog_keys):
        raise ValueError(f"{catalog_name('menu', lang)}: 重複 key")
    missing = used_text_keys - set(catalog_keys)
    orphan = set(catalog_keys) - used_text_keys
    if missing or orphan:
        raise ValueError(f"選單事件／catalog 不完整：missing={sorted(missing)} orphan={sorted(orphan)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("events", type=Path)
    parser.add_argument("catalog", type=Path)
    add_lang_argument(parser)
    args = parser.parse_args()
    validate(args.events, args.catalog, lang=args.lang)
