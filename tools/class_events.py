#!/usr/bin/env python3
"""驗證正式職業事件、繁中 catalog 與既有生命週期證據。"""

from __future__ import annotations

import csv
from pathlib import Path
import re

import class_selection_receipt
import post_gender_receipt

EVENT_HEADER = ["event_key", "sequence", "text_key", "original_length", "original_sha256",
                "caller", "background", "foreground", "row", "column"]
TEXT_HEADER = ["key", "translation", "source"]
IDENTITY_FIELDS = ["original_length", "original_sha256", "caller", "background", "foreground", "row", "column"]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_RE = re.compile(r"^[0-9A-F]{4}:[0-9A-F]{4}$")


def _table(path: Path, header: list[str], label: str) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{label}: 不得含 BOM")
    try:
        rows = list(csv.reader(raw.decode("utf-8").splitlines(), delimiter="\t"))
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label}: 不是有效 UTF-8") from exc
    if not rows or rows[0] != header or any(len(row) != len(header) for row in rows[1:]):
        raise ValueError(f"{label}: schema 不符")
    return [dict(zip(header, row)) for row in rows[1:]]


def _same(left, right):
    return all(left[field] == right[field] for field in IDENTITY_FIELDS)


def validate(events_path: Path, translations_path: Path, post_path: Path, lifecycle_path: Path) -> None:
    events = _table(events_path, EVENT_HEADER, "class-events.tsv")
    texts = _table(translations_path, TEXT_HEADER, "class.zh-TW.tsv")
    if len(events) != 12 or [r["sequence"] for r in events] != [str(i) for i in range(1, 13)]:
        raise ValueError("class-events.tsv: 必須恰有十二筆連續事件")
    if len(texts) != 6:
        raise ValueError("class.zh-TW.tsv: 必須恰有六筆譯文")
    if len({r["event_key"] for r in events}) != 12 or len({tuple(r[f] for f in IDENTITY_FIELDS) for r in events}) != 12:
        raise ValueError("class-events.tsv: event key 或 identity 不唯一")
    if len({r["key"] for r in texts}) != 6 or any(not r["translation"] or r["source"] != "manual-and-runtime" for r in texts):
        raise ValueError("class.zh-TW.tsv: key、譯文或來源無效")
    if {r["text_key"] for r in events} != {r["key"] for r in texts}:
        raise ValueError("職業事件與譯文鍵必須雙向完整")
    for row in events:
        if not HASH_RE.fullmatch(row["original_sha256"]) or not CALLER_RE.fullmatch(row["caller"]):
            raise ValueError("class-events.tsv: hash 或 caller 格式不符")
        for field in ("original_length", "background", "foreground", "row", "column"):
            if not row[field].isascii() or not row[field].isdigit() or not 0 <= int(row[field]) <= 255:
                raise ValueError(f"class-events.tsv: {field} 無效")
    post = post_gender_receipt._read_inventory(post_path)
    for index in range(7):
        if events[index]["event_key"] != post[index]["event_key"] or not _same(events[index], post[index]):
            raise ValueError(f"class-events.tsv: 初始事件 {index + 1} 不符 post-gender 證據")
    lifecycle = class_selection_receipt._read_lifecycle(lifecycle_path)
    for event_index, lifecycle_index in ((7, 0), (8, 1), (9, 2), (6, 3)):
        if events[event_index]["event_key"] != lifecycle[lifecycle_index]["event_key"] or not _same(events[event_index], lifecycle[lifecycle_index]):
            raise ValueError("class-events.tsv: selection variant 不符生命週期證據")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    for name in ("events", "translations", "post", "lifecycle"):
        parser.add_argument(name, type=Path)
    validate(**dict(zip(("events_path", "translations_path", "post_path", "lifecycle_path"), vars(parser.parse_args()).values())))
