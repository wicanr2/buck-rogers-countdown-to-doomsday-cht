#!/usr/bin/env python3
"""由本機倚天 15 點字型建立不可散布的 top-pad GOLEMFNT 子集。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from catalog_font import CatalogError, Entry, character_list_bytes, catalog_codepoints, read_catalog
from halfwidth import halfwidth_ink_error
from catalog_lang import DEFAULT_LANG, KNOWN_LANGS, catalog_glob


MAGIC = b"GOLEMFNT"
WIDTH = HEIGHT = 16
GLYPH_BYTES = 32
MANUAL_CHARACTER_LIST_SHA256 = "dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f"
MANUAL_GLYPHS = 691
MANUAL_OUTPUT_SHA256 = "78c10dec8055110764013007899c4455b91256a78f94e212294ac9c51c01364e"
SOURCE_ASCII = 1
SOURCE_SPC = 2
SOURCE_STD_COMMON = 3
SOURCE_STD_SECONDARY = 4
SOURCE_SPECS = {
    "asc": ("ASCFONT.15", 3840, "1d0cf09d0a319a9e7039190688c6a905ba4370bd369fbfcfa43b2078480d6918"),
    "spc": ("SPCFONT.15", 12240, "f32049ba2a7a21db908878a488a2c1d93c389d17398cf46db1390ba89e247605"),
    "std": ("STDFONT.15", 392820, "39ba9c8519d75fe11d5988a8a27e6daa5794ad2ea215108390b0d7e9e53ff701"),
}


@dataclass(frozen=True)
class Glyph:
    codepoint: int
    source: int
    bitmap: bytes


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_source(path: Path, name: str) -> bytes:
    filename, length, digest = SOURCE_SPECS[name]
    if not path.is_file() or path.is_symlink():
        raise CatalogError(f"{path}: {name} 必須是一般檔案")
    if path.name != filename:
        raise CatalogError(f"{path}: {name} 檔名必須是 {filename}")
    data = path.read_bytes()
    if len(data) != length:
        raise CatalogError(f"{path}: {name} byte length 不符")
    if _sha256(data) != digest:
        raise CatalogError(f"{path}: {name} SHA-256 不符")
    return data


def _column(lo: int) -> int:
    if 0x40 <= lo <= 0x7E:
        return lo - 0x40
    if 0xA1 <= lo <= 0xFE:
        return lo - 0x62
    raise CatalogError(f"Big5 trail 0x{lo:02X} 不在已證實範圍")


def big5_raw(codepoint: int) -> int:
    try:
        encoded = chr(codepoint).encode("big5", "strict")
    except UnicodeEncodeError as exc:
        raise CatalogError(f"U+{codepoint:04X}: 無法以 Big5 編碼") from exc
    if len(encoded) != 2:
        raise CatalogError(f"U+{codepoint:04X}: Big5 必須恰為兩 bytes")
    hi, lo = encoded
    if not 0xA1 <= hi <= 0xF9:
        raise CatalogError(f"U+{codepoint:04X}: Big5 lead 0x{hi:02X} 不在已證實範圍")
    return (hi - 0xA1) * 157 + _column(lo)


def _top_pad_wide(raw: bytes) -> bytes:
    if len(raw) != 30:
        raise CatalogError("倚天全形字模必須恰為 30 bytes")
    return b"\0\0" + raw


def _top_pad_ascii(raw: bytes) -> bytes:
    if len(raw) != 15:
        raise CatalogError("倚天半形字模必須恰為 15 bytes")
    return b"\0\0" + b"".join(struct.pack(">H", row << 4) for row in raw)


def glyph_for(codepoint: int, asc: bytes, spc: bytes, std: bytes) -> Glyph:
    if 0 <= codepoint <= 0xFF:
        start = codepoint * 15
        return Glyph(codepoint, SOURCE_ASCII, _top_pad_ascii(asc[start : start + 15]))
    raw = big5_raw(codepoint)
    if 0 <= raw <= 407:
        start = raw * 30
        return Glyph(codepoint, SOURCE_SPC, _top_pad_wide(spc[start : start + 30]))
    if 471 <= raw <= 5871:
        start = (raw - 471) * 30
        return Glyph(codepoint, SOURCE_STD_COMMON, _top_pad_wide(std[start : start + 30]))
    if 6280 <= raw <= 13972:
        start = (5401 + raw - 6280) * 30
        return Glyph(codepoint, SOURCE_STD_SECONDARY, _top_pad_wide(std[start : start + 30]))
    raise CatalogError(f"U+{codepoint:04X}: Big5 raw {raw} 位於保留或未證實分區")


def _valid_scalar(codepoint: int) -> bool:
    return 0 <= codepoint <= 0x10FFFF and not 0xD800 <= codepoint <= 0xDFFF


def encode_golemfnt(glyphs: list[Glyph]) -> bytes:
    if [glyph.codepoint for glyph in glyphs] != sorted({glyph.codepoint for glyph in glyphs}):
        raise CatalogError("glyph codepoint 必須唯一且遞增")
    out = bytearray(MAGIC + struct.pack("<HHI", WIDTH, HEIGHT, len(glyphs)))
    for glyph in glyphs:
        if not _valid_scalar(glyph.codepoint):
            raise CatalogError(f"U+{glyph.codepoint:X}: 非法 Unicode scalar")
        if glyph.source not in {SOURCE_ASCII, SOURCE_SPC, SOURCE_STD_COMMON, SOURCE_STD_SECONDARY}:
            raise CatalogError(f"U+{glyph.codepoint:04X}: 未知 source tag")
        if len(glyph.bitmap) != GLYPH_BYTES:
            raise CatalogError(f"U+{glyph.codepoint:04X}: bitmap 長度不符")
        if glyph.bitmap[:2] != b"\0\0":
            raise CatalogError(f"U+{glyph.codepoint:04X}: top-pad row 0 必須為零")
        if glyph.codepoint != 0x20 and not any(glyph.bitmap):
            raise CatalogError(f"U+{glyph.codepoint:04X}: 非空白 glyph 不得全零")
        # 規格 039 §3.2：半形字墨跡必須在第 4–11 欄，否則建置失敗。
        ink_error = halfwidth_ink_error(glyph.codepoint, glyph.bitmap)
        if ink_error:
            raise CatalogError(ink_error)
        out.extend(struct.pack("<IB", glyph.codepoint, glyph.source))
        out.extend(glyph.bitmap)
    return bytes(out)


def decode_golemfnt(data: bytes) -> list[Glyph]:
    if len(data) < 16 or data[:8] != MAGIC:
        raise CatalogError("GOLEMFNT magic 不符")
    width, height, count = struct.unpack_from("<HHI", data, 8)
    if (width, height) != (WIDTH, HEIGHT):
        raise CatalogError("GOLEMFNT 必須為 16x16")
    expected = 16 + count * 37
    if len(data) != expected:
        raise CatalogError("GOLEMFNT 長度不符")
    glyphs: list[Glyph] = []
    cursor = 16
    for _ in range(count):
        codepoint, source = struct.unpack_from("<IB", data, cursor)
        bitmap = data[cursor + 5 : cursor + 37]
        if not _valid_scalar(codepoint):
            raise CatalogError("GOLEMFNT 含非法 Unicode scalar")
        if source not in {SOURCE_ASCII, SOURCE_SPC, SOURCE_STD_COMMON, SOURCE_STD_SECONDARY}:
            raise CatalogError("GOLEMFNT 有未知 source tag")
        if bitmap[:2] != b"\0\0":
            raise CatalogError("GOLEMFNT 不符合 top-pad row 0 契約")
        glyphs.append(Glyph(codepoint, source, bitmap))
        cursor += 37
    if [g.codepoint for g in glyphs] != sorted({g.codepoint for g in glyphs}):
        raise CatalogError("GOLEMFNT codepoint 順序或唯一性不符")
    if any(g.codepoint != 0x20 and not any(g.bitmap) for g in glyphs):
        raise CatalogError("GOLEMFNT 含非空白全零 glyph")
    for g in glyphs:
        ink_error = halfwidth_ink_error(g.codepoint, g.bitmap)
        if ink_error:
            raise CatalogError(f"GOLEMFNT {ink_error}")
    return glyphs


def _workplace_path(path: Path, repository: Path) -> Path:
    workplace = (repository / "workplace").resolve()
    if path.is_symlink():
        raise CatalogError(f"{path}: 輸出目標不得是符號連結")
    candidate = path.resolve()
    try:
        candidate.relative_to(workplace)
    except ValueError as exc:
        raise CatalogError(f"{path}: 輸出必須位於 repository/workplace/") from exc
    if candidate == workplace:
        raise CatalogError(f"{path}: 輸出不得是 workplace 根目錄")
    if path.exists() and not path.is_file():
        raise CatalogError(f"{path}: 輸出目標不得是目錄或特殊檔")
    return candidate


def _stage_bytes(path: Path, data: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        staged = Path(temp_name)
        if staged.read_bytes() != data:
            raise CatalogError(f"{path}: 暫存回讀不符")
        return staged
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def _publish_pair(font_path: Path, font_data: bytes, manifest_path: Path, manifest_data: bytes) -> None:
    """替換本 builder 擁有的兩檔；第二次替換失敗時回復既有 font。"""
    old_font = font_path.read_bytes() if font_path.exists() else None
    font_stage = _stage_bytes(font_path, font_data)
    manifest_stage = _stage_bytes(manifest_path, manifest_data)
    font_backup = _stage_bytes(font_path, old_font) if old_font is not None else None
    font_published = False
    try:
        os.replace(font_stage, font_path)
        font_published = True
        os.replace(manifest_stage, manifest_path)
    except BaseException as exc:
        recovery_error: BaseException | None = None
        if font_published:
            try:
                if font_backup is not None:
                    os.replace(font_backup, font_path)
                    font_backup = None
                else:
                    # 此檔由本次 publish 建立，並非使用者原有檔案。
                    font_path.unlink()
            except BaseException as restore_exc:
                recovery_error = restore_exc
        if recovery_error is not None:
            raise CatalogError(f"雙檔發布失敗且 font 回復失敗：{recovery_error}") from exc
        raise
    finally:
        for staged in (font_stage, manifest_stage, font_backup):
            if staged is not None:
                try:
                    staged.unlink()
                except FileNotFoundError:
                    pass


def _read_catalog_glyph_entries(paths: list[Path]) -> list[Entry]:
    """逐檔採既有 strict TSV 驗證，再對 glyph 而不是文字 key 合併。"""
    if not paths:
        raise CatalogError("至少需要一份正式 catalog")
    entries: list[Entry] = []
    for path in paths:
        # 已接通 UI catalog 可共享同一 text key；read_catalogs 的跨檔 key
        # 唯一性規則不適用於純字型 coverage。
        entries.extend(read_catalog(path))
    return entries


def _catalog_metadata(paths: list[Path]) -> list[dict[str, str]]:
    return sorted(
        ({"filename": path.name, "sha256": _sha256(path.read_bytes())} for path in paths),
        key=lambda item: (item["filename"], item["sha256"]),
    )


def _bundle_bytes(catalogs: list[Path], asc_path: Path, spc_path: Path, std_path: Path) -> tuple[bytes, bytes, dict[str, object]]:
    """以同一份嚴格規則產生 build 與唯讀 verify 的預期內容。"""
    entries = _read_catalog_glyph_entries(catalogs)
    character_sha = _sha256(character_list_bytes(entries, fixed=True))
    codepoints = catalog_codepoints(entries, fixed=True)
    asc = _read_source(asc_path, "asc")
    spc = _read_source(spc_path, "spc")
    std = _read_source(std_path, "std")
    glyphs = [glyph_for(codepoint, asc, spc, std) for codepoint in codepoints]
    font_data = encode_golemfnt(glyphs)
    reread = decode_golemfnt(font_data)
    if reread != glyphs or len(reread) != len(codepoints):
        raise CatalogError("GOLEMFNT 回讀不符")
    output_sha = _sha256(font_data)
    if character_sha == MANUAL_CHARACTER_LIST_SHA256 and len(codepoints) == MANUAL_GLYPHS and output_sha != MANUAL_OUTPUT_SHA256:
        raise CatalogError("手冊 GOLEMFNT SHA-256 不符合已驗證的 top-pad 收據")
    manifest: dict[str, object] = {
        "catalogs": _catalog_metadata(catalogs),
        "character_list_sha256": character_sha,
        "distribution_status": "local-only-not-for-distribution",
        "format": {"glyphs": len(glyphs), "height": HEIGHT, "magic": MAGIC.decode("ascii"), "width": WIDTH},
        "output_sha256": output_sha,
        "sources": {name: {"bytes": spec[1], "filename": spec[0], "sha256": spec[2]} for name, spec in sorted(SOURCE_SPECS.items())},
        "top_pad": {"ascii_x": [4, 11], "source_rows": [0, 14], "output_rows": [1, 15]},
    }
    manifest_data = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return font_data, manifest_data, manifest


def build(catalogs: list[Path], asc_path: Path, spc_path: Path, std_path: Path, out: Path, manifest_out: Path, repository: Path | None = None) -> dict[str, object]:
    repository = (repository or Path(__file__).resolve().parents[1]).resolve()
    safe_out = _workplace_path(out, repository)
    safe_manifest = _workplace_path(manifest_out, repository)
    if safe_out == safe_manifest:
        raise CatalogError("字型與 manifest 輸出不得相同")
    if safe_out.exists() and safe_manifest.exists() and os.path.samefile(safe_out, safe_manifest):
        raise CatalogError("字型與 manifest 輸出不得是同一檔案或 hard link")
    inputs = [*catalogs, asc_path, spc_path, std_path]
    input_paths = {path.resolve() for path in inputs}
    if safe_out in input_paths or safe_manifest in input_paths:
        raise CatalogError("輸出不得與 catalog 或字型來源重疊")
    font_data, manifest_data, manifest = _bundle_bytes(catalogs, asc_path, spc_path, std_path)
    _publish_pair(safe_out, font_data, safe_manifest, manifest_data)
    return manifest


def verify(asc_path: Path, spc_path: Path, std_path: Path, font_path: Path, manifest_path: Path, repository: Path | None = None,
           lang: str = DEFAULT_LANG) -> dict[str, object]:
    """不寫入任何檔案，核對完整正式譯文、原始字型與本機產物。"""
    repository = (repository or Path(__file__).resolve().parents[1]).resolve()
    catalog_dir = repository / "text"
    if not catalog_dir.is_dir():
        raise CatalogError("缺少正式 text/ 目錄")
    catalogs = sorted(catalog_dir.glob(catalog_glob(lang)))
    if not catalogs or any(not path.is_file() or path.is_symlink() for path in catalogs):
        raise CatalogError("正式 catalog 集合為空或含非一般檔案")
    safe_font = _workplace_path(font_path, repository)
    safe_manifest = _workplace_path(manifest_path, repository)
    if safe_font == safe_manifest or not safe_font.is_file() or not safe_manifest.is_file():
        raise CatalogError("本機字型與 manifest 必須是兩個現有檔案")
    expected_font, expected_manifest, manifest = _bundle_bytes(catalogs, asc_path, spc_path, std_path)
    if safe_font.read_bytes() != expected_font:
        raise CatalogError("本機 GOLEMFNT 與正式譯文／倚天來源不符")
    if safe_manifest.read_bytes() != expected_manifest:
        raise CatalogError("本機 manifest 與正式 catalog／來源／字型不符")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("build", help="由一份或多份正式 catalog 建立本機倚天 top-pad 字型")
    command.add_argument("catalog", nargs="+", type=Path)
    command.add_argument("--asc", required=True, type=Path)
    command.add_argument("--spc", required=True, type=Path)
    command.add_argument("--std", required=True, type=Path)
    command.add_argument("--out", required=True, type=Path)
    command.add_argument("--manifest-out", required=True, type=Path)
    command = subparsers.add_parser("verify", help="唯讀核對 text/ 全部正式繁中 catalog、本機來源與既有字型／manifest")
    command.add_argument("--asc", required=True, type=Path)
    command.add_argument("--spc", required=True, type=Path)
    command.add_argument("--std", required=True, type=Path)
    command.add_argument("--font", required=True, type=Path)
    command.add_argument("--manifest", required=True, type=Path)
    command.add_argument("--lang", default=DEFAULT_LANG, choices=KNOWN_LANGS, help="核對的譯文語言（規格 040；預設 zh-TW）")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            manifest = build(args.catalog, args.asc, args.spc, args.std, args.out, args.manifest_out)
        else:
            manifest = verify(args.asc, args.spc, args.std, args.font, args.manifest, lang=args.lang)
    except (CatalogError, OSError) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
