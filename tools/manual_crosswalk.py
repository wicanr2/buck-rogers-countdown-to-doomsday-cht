#!/usr/bin/env python3
"""驗證手冊題庫與繁中掃描來源對照；不處理答案或 OCR 全文。"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FIELDS = [
    "record_index", "page", "heading_ascii", "status", "source_scan",
    "archive_order", "source_sha256", "printed_page", "source_anchor_zh", "note",
]
STATUSES = {"confirmed", "strong-inference", "unknown"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"{path}: 缺少標頭")
        return list(reader)


def validate(questions_path: Path, crosswalk_path: Path, manifest_path: Path | None) -> None:
    questions = read_tsv(questions_path)
    crosswalk = read_tsv(crosswalk_path)
    with crosswalk_path.open(encoding="utf-8", newline="") as source:
        header = next(csv.reader(source, delimiter="\t"))
    if header != FIELDS:
        raise ValueError(f"對照表標頭不符：{header!r}")
    if len(questions) != 39 or len(crosswalk) != 39:
        raise ValueError("題庫與對照表都必須恰有 39 筆")

    manifest: dict[str, str] = {}
    if manifest_path:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest = {Path(row["path"]).name: row["sha256"] for row in data["entries"]}

    for question, source in zip(questions, crosswalk, strict=True):
        for key in ("record_index", "page", "heading_ascii"):
            if source[key] != question[key]:
                raise ValueError(f"第 {question['record_index']} 筆 {key} 與題庫不符")
        status = source["status"]
        if status not in STATUSES:
            raise ValueError(f"第 {question['record_index']} 筆狀態無效：{status}")
        evidence = [source[key] for key in FIELDS[4:9]]
        if status == "unknown":
            if any(evidence) or not source["note"]:
                raise ValueError(f"第 {question['record_index']} 筆 unknown 必須清空來源並說明原因")
            continue
        if not all(evidence):
            raise ValueError(f"第 {question['record_index']} 筆有等級但來源欄位不完整")
        if manifest and manifest.get(source["source_scan"]) != source["source_sha256"]:
            raise ValueError(f"第 {question['record_index']} 筆掃描 SHA-256 與 manifest 不符")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("questions", type=Path)
    parser.add_argument("crosswalk", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        validate(args.questions, args.crosswalk, args.manifest)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
