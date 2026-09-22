#!/usr/bin/env python3
"""驗證手冊題庫與繁中掃描來源對照；不處理答案或 OCR 全文。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse


FIELDS = [
    "record_index", "page", "heading_ascii", "status", "source_scan",
    "archive_order", "source_sha256", "printed_page", "source_anchor_zh", "note",
]
STATUSES = {"confirmed", "strong-inference", "unknown"}
ENGLISH_FIELDS = [
    "record_index", "source_kind", "source_url", "source_locator", "source_sha256", "retrieved_on",
]
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"{path}: 缺少標頭")
        return list(reader)


def read_english_sources(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if reader.fieldnames != ENGLISH_FIELDS:
            raise ValueError(f"英文原書來源表標頭不符：{reader.fieldnames!r}")
        rows = list(reader)
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        record = row["record_index"]
        if not record or record in result:
            raise ValueError(f"英文原書來源 record_index 缺漏或重複：{record}")
        url = urlparse(row["source_url"])
        if (row["source_kind"] != "original-english-transcription" or url.scheme != "https" or not url.netloc
                or not row["source_locator"] or not SHA256_RE.fullmatch(row["source_sha256"])
                or not DATE_RE.fullmatch(row["retrieved_on"])):
            raise ValueError(f"第 {record} 筆英文原書來源不完整")
        result[record] = row
    return result


def validate(questions_path: Path, crosswalk_path: Path, manifest_path: Path | None,
             english_source_path: Path | None = None, english_snapshot_path: Path | None = None) -> None:
    questions = read_tsv(questions_path)
    crosswalk = read_tsv(crosswalk_path)
    with crosswalk_path.open(encoding="utf-8", newline="") as source:
        header = next(csv.reader(source, delimiter="\t"))
    if header != FIELDS:
        raise ValueError(f"對照表標頭不符：{header!r}")
    if len(questions) != 39 or len(crosswalk) != 39:
        raise ValueError("題庫與對照表都必須恰有 39 筆")
    english_sources = read_english_sources(english_source_path)
    if english_snapshot_path is not None:
        snapshot_hash = hashlib.sha256(english_snapshot_path.read_bytes()).hexdigest()
        if not english_sources or any(row["source_sha256"] != snapshot_hash for row in english_sources.values()):
            raise ValueError("英文原書來源 SHA-256 與本機快照不符")
    used_english: set[str] = set()

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
            if any(evidence) or not source["note"] or source["record_index"] in english_sources:
                raise ValueError(f"第 {question['record_index']} 筆 unknown 必須清空來源並說明原因")
            continue
        if not any(evidence):
            if status != "confirmed" or source["record_index"] not in english_sources or not source["note"]:
                raise ValueError(f"第 {question['record_index']} 筆有等級但來源欄位不完整")
            used_english.add(source["record_index"])
            continue
        if not all(evidence) or source["record_index"] in english_sources:
            raise ValueError(f"第 {question['record_index']} 筆掃描來源不完整或與英文來源重複")
        if manifest and manifest.get(source["source_scan"]) != source["source_sha256"]:
            raise ValueError(f"第 {question['record_index']} 筆掃描 SHA-256 與 manifest 不符")
    if set(english_sources) != used_english:
        raise ValueError(f"英文原書來源有孤兒 record：{sorted(set(english_sources) - used_english)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("questions", type=Path)
    parser.add_argument("crosswalk", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--english-sources", type=Path)
    parser.add_argument("--english-snapshot", type=Path)
    args = parser.parse_args()
    try:
        validate(args.questions, args.crosswalk, args.manifest, args.english_sources, args.english_snapshot)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
