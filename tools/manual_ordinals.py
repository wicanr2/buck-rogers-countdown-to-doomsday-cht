#!/usr/bin/env python3
"""由原版 runtime data dump 重生手冊序數詞橋接表。"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import re


BASE = 0x339B
SLOT_SIZE = 0x13
MIN_ORDINAL = 1
MAX_ORDINAL = 10
FIELDS = ["number", "ordinal_ascii", "runtime_address", "slot_hex"]
WORD_PATTERN = re.compile(r"^[a-z]+$")


def parse(data: bytes) -> list[dict[str, str]]:
    end = BASE + (MAX_ORDINAL + 1) * SLOT_SIZE
    if len(data) < end:
        raise ValueError(f"runtime data 太短：需要至少 {end} bytes，實際 {len(data)}")

    rows: list[dict[str, str]] = []
    seen_words: set[str] = set()
    for number in range(MIN_ORDINAL, MAX_ORDINAL + 1):
        offset = BASE + number * SLOT_SIZE
        slot = data[offset : offset + SLOT_SIZE]
        length = slot[0]
        if not 1 <= length < SLOT_SIZE:
            raise ValueError(f"ordinal {number} 長度越界：{length}")
        raw = slot[1 : 1 + length]
        try:
            padded_word = raw.decode("ascii")
        except UnicodeDecodeError as error:
            raise ValueError(f"ordinal {number} 不是 ASCII") from error
        word = padded_word.rstrip(" ")
        if not WORD_PATTERN.fullmatch(word):
            raise ValueError(f"ordinal {number} 字串格式錯誤：{word!r}")
        if any(byte != 0 for byte in slot[1 + length :]):
            raise ValueError(f"ordinal {number} padding 非零")
        if word in seen_words:
            raise ValueError(f"ordinal 字串重複：{word}")
        seen_words.add(word)
        rows.append(
            {
                "number": str(number),
                "ordinal_ascii": word,
                "runtime_address": f"0EC0:{offset:04X}",
                "slot_hex": slot.hex(),
            }
        )
    return rows


def validate_events(rows: list[dict[str, str]], events_path: Path) -> None:
    available = {row["number"] for row in rows}
    with events_path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if reader.fieldnames is None or "ordinal" not in reader.fieldnames:
            raise ValueError("事件表缺少 ordinal 欄")
        missing = sorted({row["ordinal"] for row in reader if row["ordinal"] not in available})
    if missing:
        raise ValueError(f"事件表含未橋接 ordinal：{', '.join(missing)}")


def write_tsv(rows: list[dict[str, str]], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runtime_data", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--events", type=Path)
    args = parser.parse_args()
    try:
        data = args.runtime_data.read_bytes()
        rows = parse(data)
        if args.events is not None:
            validate_events(rows, args.events)
        write_tsv(rows, args.output)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))
    print(f"input_sha256={hashlib.sha256(data).hexdigest()} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
