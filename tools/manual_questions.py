#!/usr/bin/env python3
"""從原版執行期資料段匯出不含答案的手冊題目中繼資料。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys


RECORD_BASE = 0x00C2
RECORD_COUNT = 39
RECORD_SIZE = 30
HEADING_CAPACITY = 18
ANSWER_CAPACITY = 8


def decode_field(encoded: bytes, length: int) -> str:
    if length > len(encoded):
        raise ValueError(f"欄位長度 {length} 超過容量 {len(encoded)}")
    raw = bytes((byte - 6 + length) & 0xFF for byte in encoded[:length])
    try:
        return raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("解碼結果不是 ASCII") from error


def read_metadata(data: bytes) -> list[dict[str, str | int]]:
    end = RECORD_BASE + RECORD_COUNT * RECORD_SIZE
    if len(data) < end:
        raise ValueError(f"資料段過短：需要至少 0x{end:04X} bytes")

    rows: list[dict[str, str | int]] = []
    for index in range(1, RECORD_COUNT + 1):
        offset = RECORD_BASE + (index - 1) * RECORD_SIZE
        record = data[offset : offset + RECORD_SIZE]
        heading_length = record[1]
        answer_length = record[21]
        if heading_length > HEADING_CAPACITY:
            raise ValueError(f"第 {index} 筆標題長度超界：{heading_length}")
        if answer_length > ANSWER_CAPACITY:
            raise ValueError(f"第 {index} 筆答案長度超界：{answer_length}")
        if not 1 <= record[20] <= 10:
            raise ValueError(f"第 {index} 筆序數超界：{record[20]}")
        rows.append(
            {
                "record_index": index,
                "data_offset_hex": f"0x{offset:04X}",
                "page": record[0],
                "heading_ascii": decode_field(record[2:20], heading_length),
                "ordinal": record[20],
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_segment", type=Path, help="0EC0:0000 起算的 64 KiB 執行期資料段")
    parser.add_argument("--out", type=Path, help="輸出 TSV；未指定時寫到標準輸出")
    args = parser.parse_args()

    try:
        rows = read_metadata(args.data_segment.read_bytes())
    except (OSError, ValueError) as error:
        parser.error(str(error))

    output = args.out.open("w", encoding="utf-8", newline="") if args.out else sys.stdout
    try:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if args.out:
            output.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
