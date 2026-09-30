#!/usr/bin/env python3
"""驗證正式性別事件、繁中 catalog 與既有生命週期證據。"""

from __future__ import annotations

import csv
from pathlib import Path
import re

import gender_selection_receipt
import post_race_receipt
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name


EVENT_HEADER = [
    "event_key", "sequence", "text_key", "original_length", "original_sha256",
    "caller", "background", "foreground", "row", "column",
]
TEXT_HEADER = ["key", "translation", "source"]
IDENTITY_FIELDS = [
    "original_length", "original_sha256", "caller", "background", "foreground", "row", "column",
]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")
SOURCES = {"manual-and-runtime", "runtime-interface"}


def _table(path: Path, header: list[str], label: str) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{label}: 不得含 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label}: 不是有效 UTF-8") from exc
    rows = list(csv.reader(text.splitlines(), delimiter="\t"))
    if not rows or rows[0] != header or any(len(row) != len(header) for row in rows[1:]):
        raise ValueError(f"{label}: schema 不符")
    return [dict(zip(header, row)) for row in rows[1:]]


def _same_identity(left: dict[str, str], right: dict[str, str]) -> bool:
    return all(left[field] == right[field] for field in IDENTITY_FIELDS)


def validate(events_path: Path, translations_path: Path, post_path: Path, lifecycle_path: Path,
             lang: str = DEFAULT_LANG) -> None:
    events = _table(events_path, EVENT_HEADER, "gender-events.tsv")
    texts = _table(translations_path, TEXT_HEADER, catalog_name("gender", lang))
    if len(events) != 7 or [row["sequence"] for row in events] != [str(value) for value in range(1, 8)]:
        raise ValueError("gender-events.tsv: 必須恰有七筆連續事件")
    if len(texts) != 3:
        raise ValueError(f"{catalog_name('gender', lang)}: 必須恰有三筆譯文")
    event_keys = [row["event_key"] for row in events]
    text_keys = [row["key"] for row in texts]
    identities = [tuple(row[field] for field in IDENTITY_FIELDS) for row in events]
    if len(set(event_keys)) != 7 or len(set(identities)) != 7:
        raise ValueError("gender-events.tsv: event key 或 identity 不唯一")
    if len(set(text_keys)) != 3 or any(not row["translation"] or row["source"] not in SOURCES for row in texts):
        raise ValueError(f"{catalog_name('gender', lang)}: key、譯文或來源無效")
    if {row["text_key"] for row in events} != set(text_keys):
        raise ValueError("性別事件與譯文鍵必須雙向完整")
    for row in events:
        if not HASH_RE.fullmatch(row["original_sha256"]) or not CALLER_RE.fullmatch(row["caller"]):
            raise ValueError("gender-events.tsv: hash 或 caller 格式不符")
        for field in ("original_length", "background", "foreground", "row", "column"):
            if not row[field].isascii() or not row[field].isdigit() or not 0 <= int(row[field]) <= 255:
                raise ValueError(f"gender-events.tsv: {field} 無效")
    post = post_race_receipt._read_inventory(post_path)
    for index in range(4):
        if events[index]["event_key"] != post[index]["event_key"] or not _same_identity(events[index], post[index]):
            raise ValueError(f"gender-events.tsv: 初始事件 {index + 1} 不符 post-race 證據")
    lifecycle = gender_selection_receipt._read_lifecycle(lifecycle_path)
    links = ((4, 0), (5, 1), (6, 2), (3, 3))
    for event_index, lifecycle_index in links:
        if (events[event_index]["event_key"] != lifecycle[lifecycle_index]["event_key"] or
                not _same_identity(events[event_index], lifecycle[lifecycle_index])):
            raise ValueError("gender-events.tsv: selection variant 不符生命週期證據")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("events", type=Path)
    parser.add_argument("translations", type=Path)
    parser.add_argument("post", type=Path)
    parser.add_argument("lifecycle", type=Path)
    add_lang_argument(parser)
    args = parser.parse_args()
    validate(args.events, args.translations, args.post, args.lifecycle, lang=args.lang)
