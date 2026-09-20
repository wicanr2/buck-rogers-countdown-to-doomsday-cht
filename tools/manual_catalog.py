#!/usr/bin/env python3
"""交叉驗證手冊事件、題庫、繁中來源與顯示 catalog。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re

from catalog_font import read_catalog


EVENT_FIELDS = ["event_key", "record_index", "page", "heading_ascii", "ordinal", "text_key"]
EVENT_PATTERN = re.compile(r"^manual\.page([0-9]+)\.[a-z0-9_]+\.word([0-9]+)$")


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"{path}: 缺少標頭")
        return reader.fieldnames, list(reader)


def validate(questions_path: Path, crosswalk_path: Path, events_path: Path, catalog_path: Path) -> None:
    _, questions = read_rows(questions_path)
    _, crosswalk = read_rows(crosswalk_path)
    event_header, events = read_rows(events_path)
    if event_header != EVENT_FIELDS:
        raise ValueError(f"事件表標頭不符：{event_header!r}")

    question_by_record = {row["record_index"]: row for row in questions}
    source_by_record = {row["record_index"]: row for row in crosswalk}
    catalog = {entry.key: entry for entry in read_catalog(catalog_path)}
    seen_events: set[str] = set()
    seen_text: set[str] = set()

    for event in events:
        record = event["record_index"]
        question = question_by_record.get(record)
        source = source_by_record.get(record)
        if question is None or source is None:
            raise ValueError(f"事件指向不存在的 record：{record}")
        for key in ("page", "heading_ascii", "ordinal"):
            if event[key] != question[key]:
                raise ValueError(f"record {record} 的 {key} 與題庫不符")
        if source["status"] != "confirmed":
            raise ValueError(f"record {record} 的來源不是 confirmed")
        match = EVENT_PATTERN.fullmatch(event["event_key"])
        if not match or match.groups() != (event["page"], event["ordinal"]):
            raise ValueError(f"record {record} 的 event_key 與頁碼／序數不符")
        if event["event_key"] in seen_events or event["text_key"] in seen_text:
            raise ValueError(f"record {record} 的事件鍵或文字鍵重複")
        seen_events.add(event["event_key"])
        seen_text.add(event["text_key"])
        if event["text_key"] not in catalog:
            raise ValueError(f"record {record} 的 text_key 不在 catalog")

    extras = sorted(catalog.keys() - seen_text)
    if extras:
        raise ValueError(f"catalog 有未映射文字鍵：{', '.join(extras)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("questions", type=Path)
    parser.add_argument("crosswalk", type=Path)
    parser.add_argument("events", type=Path)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    try:
        validate(args.questions, args.crosswalk, args.events, args.catalog)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
