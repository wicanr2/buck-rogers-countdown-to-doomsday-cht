#!/usr/bin/env python3
"""Validate localization catalogs and build deterministic GOLEMFNT subsets."""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import struct
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path


HEADER = ["key", "translation", "source"]
ALLOWED_SOURCES = {"runtime", "manual-and-runtime", "runtime-interface"}
MAGIC = b"GOLEMFNT"
WIDTH = 16
HEIGHT = 16
SOURCE_UNIFONT = 1


class CatalogError(ValueError):
    pass


@dataclass(frozen=True)
class Entry:
    key: str
    translation: str
    source: str


def read_catalog(path: Path) -> list[Entry]:
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CatalogError(f"{path}: 不是有效的 UTF-8：{exc}") from exc
    if text.startswith("\ufeff"):
        raise CatalogError(f"{path}: 不允許 UTF-8 BOM")

    rows = list(csv.reader(io.StringIO(text), delimiter="\t", strict=True))
    if not rows or rows[0] != HEADER:
        raise CatalogError(f"{path}: 標頭必須精確為 {'/'.join(HEADER)}")

    entries: list[Entry] = []
    seen: set[str] = set()
    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(HEADER):
            raise CatalogError(f"{path}:{line_number}: 必須恰有 {len(HEADER)} 欄")
        key, translation, source = row
        if not key:
            raise CatalogError(f"{path}:{line_number}: key 不得為空")
        if key in seen:
            raise CatalogError(f"{path}:{line_number}: 重複 key：{key}")
        seen.add(key)
        if not translation:
            raise CatalogError(f"{path}:{line_number}: translation 不得為空")
        if source not in ALLOWED_SOURCES:
            raise CatalogError(f"{path}:{line_number}: 不允許的 source：{source}")
        if any(unicodedata.category(ch).startswith("C") for ch in translation):
            raise CatalogError(f"{path}:{line_number}: translation 含控制或格式字元")
        if unicodedata.normalize("NFC", translation) != translation:
            raise CatalogError(f"{path}:{line_number}: translation 必須使用 NFC")
        entries.append(Entry(key, translation, source))
    return entries


def catalog_codepoints(entries: list[Entry]) -> list[int]:
    return sorted({ord(ch) for entry in entries for ch in entry.translation})


def character_list_bytes(entries: list[Entry]) -> bytes:
    return "".join(f"U+{codepoint:04X}\t{chr(codepoint)}\n" for codepoint in catalog_codepoints(entries)).encode("utf-8")


def _open_unifont(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="ascii", newline="")
    return path.open("rt", encoding="ascii", newline="")


def _glyph_16x16(raw: bytes, codepoint: int) -> bytes:
    if len(raw) == 32:
        return raw
    if len(raw) == 16:
        out = bytearray()
        for row in raw:
            out.extend(struct.pack(">H", row << 4))
        return bytes(out)
    raise CatalogError(f"U+{codepoint:04X}: 只支援 8x16 或 16x16 Unifont 字模")


def load_unifont_subset(path: Path, wanted: list[int]) -> dict[int, bytes]:
    wanted_set = set(wanted)
    found: dict[int, bytes] = {}
    with _open_unifont(path) as stream:
        for line_number, raw_line in enumerate(stream, start=1):
            line = raw_line.rstrip("\r\n")
            if not line or ":" not in line:
                continue
            code_text, bitmap_text = line.split(":", 1)
            try:
                codepoint = int(code_text, 16)
            except ValueError:
                continue
            if codepoint not in wanted_set:
                continue
            if codepoint in found:
                raise CatalogError(f"{path}:{line_number}: 重複字模 U+{codepoint:04X}")
            try:
                bitmap = bytes.fromhex(bitmap_text)
            except ValueError as exc:
                raise CatalogError(f"{path}:{line_number}: U+{codepoint:04X} 的字模不是十六進位") from exc
            found[codepoint] = _glyph_16x16(bitmap, codepoint)

    missing = sorted(wanted_set - found.keys())
    if missing:
        formatted = ", ".join(f"U+{codepoint:04X}" for codepoint in missing)
        raise CatalogError(f"{path}: 缺少字模：{formatted}")
    return found


def build_golemfnt(entries: list[Entry], unifont_path: Path) -> bytes:
    codepoints = catalog_codepoints(entries)
    glyphs = load_unifont_subset(unifont_path, codepoints)
    output = bytearray(MAGIC)
    output.extend(struct.pack("<HHI", WIDTH, HEIGHT, len(codepoints)))
    for codepoint in codepoints:
        output.extend(struct.pack("<IB", codepoint, SOURCE_UNIFONT))
        output.extend(glyphs[codepoint])
    return bytes(output)


def _write_if_changed(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == content:
        return
    path.write_bytes(content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    lint = subparsers.add_parser("lint", help="驗證 TSV catalog")
    lint.add_argument("catalog", type=Path)

    chars = subparsers.add_parser("chars", help="產生決定性的字元清單")
    chars.add_argument("catalog", type=Path)
    chars.add_argument("--out", required=True, type=Path)

    build = subparsers.add_parser("build", help="由 Unifont 建立 GOLEMFNT 子集")
    build.add_argument("catalog", type=Path)
    build.add_argument("--font", required=True, type=Path)
    build.add_argument("--out", required=True, type=Path)

    args = parser.parse_args(argv)
    try:
        entries = read_catalog(args.catalog)
        if args.command == "chars":
            _write_if_changed(args.out, character_list_bytes(entries))
        elif args.command == "build":
            _write_if_changed(args.out, build_golemfnt(entries, args.font))
    except (CatalogError, OSError, csv.Error) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
