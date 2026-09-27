#!/usr/bin/env python3
"""Validate localization catalogs and build deterministic GOLEMFNT subsets."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import struct
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path


HEADER = ["key", "translation", "source"]
ALLOWED_SOURCES = {
    "runtime",
    "manual-and-runtime",
    "runtime-interface",
    "runtime-editorial",
    "manual-term-editorial",
    "ecl-batch-editorial",
    "frontend-help",  # dosgolem 規格 241 前端說明頁
}
MAGIC = b"GOLEMFNT"
WIDTH = 16
HEIGHT = 16
SOURCE_UNIFONT = 1
CANDIDATE_SCHEMA = "buck-rogers-manual-font-candidate/v1"
CANDIDATE_SOURCE_FORMAT = "unifont-hex"
CANDIDATE_CONVERSION_RULE = "unifont-8x16-or-16x16-to-golemfnt-16x16"
CANDIDATE_VALIDATION_SCOPE = "local-validation-only"
CANDIDATE_DISTRIBUTION_STATUS = "undecided"
CANDIDATE_FIELDS = frozenset(
    {
        "schema",
        "source_filename",
        "source_version",
        "source_sha256",
        "source_format",
        "conversion_rule",
        "license_filename",
        "license_sha256",
        "attribution_notice",
        "embedding_notice",
        "character_list_sha256",
        "validation_scope",
        "distribution_status",
    }
)
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


class CatalogError(ValueError):
    pass


@dataclass(frozen=True)
class Entry:
    key: str
    translation: str
    source: str


@dataclass(frozen=True)
class CandidateManifest:
    source_filename: str
    source_version: str
    source_sha256: str
    license_filename: str
    license_sha256: str
    character_list_sha256: str


@dataclass(frozen=True)
class CandidateValidation:
    source_filename: str
    source_version: str
    source_sha256: str
    license_filename: str
    license_sha256: str
    character_list_sha256: str
    required_glyphs: int
    found_glyphs: int

    def metadata(self) -> dict[str, object]:
        return {
            "character_list_sha256": self.character_list_sha256,
            "distribution_status": CANDIDATE_DISTRIBUTION_STATUS,
            "glyphs": {"found": self.found_glyphs, "required": self.required_glyphs},
            "license": {"filename": self.license_filename, "sha256": self.license_sha256},
            "schema": CANDIDATE_SCHEMA,
            "source": {
                "filename": self.source_filename,
                "format": CANDIDATE_SOURCE_FORMAT,
                "sha256": self.source_sha256,
                "version": self.source_version,
            },
            "validation_scope": CANDIDATE_VALIDATION_SCOPE,
        }


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


def read_catalogs(paths: list[Path]) -> list[Entry]:
    """合併多份 catalog；同一 key 即使譯文相同也拒絕，維持單一權威。"""
    entries: list[Entry] = []
    seen: set[str] = set()
    for path in paths:
        for entry in read_catalog(path):
            if entry.key in seen:
                raise CatalogError(f"多 catalog 重複 key：{entry.key}")
            seen.add(entry.key)
            entries.append(entry)
    return entries


# 規格 034 §3.3：手冊英文列用同一字型顯示本機英文摘錄，字型子集固定含全部可列印 ASCII。
FIXED_CODEPOINTS = frozenset(range(0x21, 0x7F))


def catalog_codepoints(entries: list[Entry], fixed: bool = False) -> list[int]:
    points = {ord(ch) for entry in entries for ch in entry.translation}
    return sorted(points | FIXED_CODEPOINTS if fixed else points)


def character_list_bytes(entries: list[Entry], fixed: bool = False) -> bytes:
    return "".join(f"U+{codepoint:04X}\t{chr(codepoint)}\n" for codepoint in catalog_codepoints(entries, fixed)).encode("utf-8")


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


def build_golemfnt(entries: list[Entry], unifont_path: Path, fixed: bool = False) -> bytes:
    codepoints = catalog_codepoints(entries, fixed)
    glyphs = load_unifont_subset(unifont_path, codepoints)
    output = bytearray(MAGIC)
    output.extend(struct.pack("<HHI", WIDTH, HEIGHT, len(codepoints)))
    for codepoint in codepoints:
        output.extend(struct.pack("<IB", codepoint, SOURCE_UNIFONT))
        output.extend(glyphs[codepoint])
    return bytes(output)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_regular_file(path: Path, label: str) -> bytes:
    if not path.is_file():
        raise CatalogError(f"{path}: {label} 必須是一般檔案")
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise CatalogError(f"{path}: 無法讀取 {label}") from exc
    if not data:
        raise CatalogError(f"{path}: {label} 不得為空")
    return data


def _strict_json_object(path: Path) -> dict[str, object]:
    data = _read_regular_file(path, "candidate manifest")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CatalogError(f"{path}: candidate manifest 必須是 UTF-8") from exc
    if text.startswith("\ufeff"):
        raise CatalogError(f"{path}: candidate manifest 不允許 UTF-8 BOM")

    def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
        out: dict[str, object] = {}
        for key, value in pairs:
            if key in out:
                raise CatalogError(f"{path}: candidate manifest 重複欄位 {key}")
            out[key] = value
        return out

    try:
        value = json.loads(text, object_pairs_hook=no_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise CatalogError(f"{path}: candidate manifest 不是有效 JSON") from exc
    if not isinstance(value, dict):
        raise CatalogError(f"{path}: candidate manifest 必須是 object")
    return value


def _manifest_text(data: dict[str, object], field: str) -> str:
    value = data[field]
    if not isinstance(value, str) or not value or value.strip() != value:
        raise CatalogError(f"candidate manifest: {field} 必須是非空字串")
    if "\n" in value or "\r" in value or "\x00" in value:
        raise CatalogError(f"candidate manifest: {field} 不得含換行或 NUL")
    return value


def _manifest_filename(data: dict[str, object], field: str) -> str:
    value = _manifest_text(data, field)
    if value in {".", ".."} or "/" in value or "\\" in value or Path(value).name != value:
        raise CatalogError(f"candidate manifest: {field} 必須是 basename")
    return value


def _manifest_sha256(data: dict[str, object], field: str) -> str:
    value = _manifest_text(data, field)
    if not SHA256_RE.fullmatch(value):
        raise CatalogError(f"candidate manifest: {field} 必須是 64 個小寫十六進位字元")
    return value


def read_candidate_manifest(path: Path) -> CandidateManifest:
    data = _strict_json_object(path)
    fields = frozenset(data)
    if fields != CANDIDATE_FIELDS:
        missing = sorted(CANDIDATE_FIELDS - fields)
        unknown = sorted(fields - CANDIDATE_FIELDS)
        detail = []
        if missing:
            detail.append(f"缺欄 {','.join(missing)}")
        if unknown:
            detail.append(f"未知欄 {','.join(unknown)}")
        raise CatalogError(f"{path}: candidate manifest schema 不符：{'；'.join(detail)}")
    if _manifest_text(data, "schema") != CANDIDATE_SCHEMA:
        raise CatalogError(f"{path}: candidate manifest schema 不支援")
    if _manifest_text(data, "source_format") != CANDIDATE_SOURCE_FORMAT:
        raise CatalogError(f"{path}: candidate source_format 不支援")
    if _manifest_text(data, "conversion_rule") != CANDIDATE_CONVERSION_RULE:
        raise CatalogError(f"{path}: candidate conversion_rule 不支援")
    if _manifest_text(data, "validation_scope") != CANDIDATE_VALIDATION_SCOPE:
        raise CatalogError(f"{path}: candidate validation_scope 必須是本機驗證")
    if _manifest_text(data, "distribution_status") != CANDIDATE_DISTRIBUTION_STATUS:
        raise CatalogError(f"{path}: candidate distribution_status 必須保持未定")
    for field in ("source_version", "attribution_notice", "embedding_notice"):
        _manifest_text(data, field)
    return CandidateManifest(
        source_filename=_manifest_filename(data, "source_filename"),
        source_version=_manifest_text(data, "source_version"),
        source_sha256=_manifest_sha256(data, "source_sha256"),
        license_filename=_manifest_filename(data, "license_filename"),
        license_sha256=_manifest_sha256(data, "license_sha256"),
        character_list_sha256=_manifest_sha256(data, "character_list_sha256"),
    )


def validate_font_candidate(entries: list[Entry], manifest_path: Path, source_path: Path, license_path: Path) -> CandidateValidation:
    manifest = read_candidate_manifest(manifest_path)
    if source_path.name != manifest.source_filename:
        raise CatalogError(f"{source_path}: source filename 與 candidate manifest 不符")
    if license_path.name != manifest.license_filename:
        raise CatalogError(f"{license_path}: license filename 與 candidate manifest 不符")
    source = _read_regular_file(source_path, "candidate source")
    if _sha256(source) != manifest.source_sha256:
        raise CatalogError(f"{source_path}: candidate source SHA-256 不符")
    license_text = _read_regular_file(license_path, "candidate license")
    try:
        if not license_text.decode("utf-8").strip():
            raise CatalogError(f"{license_path}: candidate license 不得為空白")
    except UnicodeDecodeError as exc:
        raise CatalogError(f"{license_path}: candidate license 必須是 UTF-8 文字") from exc
    if _sha256(license_text) != manifest.license_sha256:
        raise CatalogError(f"{license_path}: candidate license SHA-256 不符")
    character_sha256 = _sha256(character_list_bytes(entries))
    if character_sha256 != manifest.character_list_sha256:
        raise CatalogError("candidate manifest: character_list_sha256 與 catalog 不符")
    codepoints = catalog_codepoints(entries)
    glyphs = load_unifont_subset(source_path, codepoints)
    return CandidateValidation(
        source_filename=manifest.source_filename,
        source_version=manifest.source_version,
        source_sha256=manifest.source_sha256,
        license_filename=manifest.license_filename,
        license_sha256=manifest.license_sha256,
        character_list_sha256=manifest.character_list_sha256,
        required_glyphs=len(codepoints),
        found_glyphs=len(glyphs),
    )


def candidate_validation_json(validation: CandidateValidation) -> str:
    return json.dumps(validation.metadata(), ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _write_if_changed(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == content:
        return
    path.write_bytes(content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    lint = subparsers.add_parser("lint", help="驗證 TSV catalog")
    lint.add_argument("catalog", nargs="+", type=Path)

    chars = subparsers.add_parser("chars", help="產生決定性的字元清單")
    chars.add_argument("catalog", nargs="+", type=Path)
    chars.add_argument("--out", required=True, type=Path)

    build = subparsers.add_parser("build", help="由 Unifont 建立 GOLEMFNT 子集")
    build.add_argument("catalog", nargs="+", type=Path)
    build.add_argument("--font", required=True, type=Path)
    build.add_argument("--out", required=True, type=Path)

    candidate = subparsers.add_parser("validate-candidate", help="驗證本機字型候選 manifest，不建置字型")
    candidate.add_argument("catalog", nargs="+", type=Path)
    candidate.add_argument("--manifest", required=True, type=Path)
    candidate.add_argument("--source", required=True, type=Path)
    candidate.add_argument("--license", required=True, type=Path)

    args = parser.parse_args(argv)
    try:
        if args.command in ("chars", "build"):
            # 字型字元聯集不帶跨檔文字鍵語意；已接通的畫面可合法共用 key。
            # 每份檔案仍分別通過 read_catalog 的完整 schema／唯一鍵檢查（同 eten_font.py）。
            entries = [entry for path in args.catalog for entry in read_catalog(path)]
        else:
            entries = read_catalogs(args.catalog)
        if args.command == "chars":
            _write_if_changed(args.out, character_list_bytes(entries, fixed=True))
        elif args.command == "build":
            _write_if_changed(args.out, build_golemfnt(entries, args.font, fixed=True))
        elif args.command == "validate-candidate":
            print(candidate_validation_json(validate_font_candidate(entries, args.manifest, args.source, args.license)))
    except (CatalogError, OSError, csv.Error) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
