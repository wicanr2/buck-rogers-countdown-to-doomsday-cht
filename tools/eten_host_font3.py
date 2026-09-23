#!/usr/bin/env python3
"""由本機倚天原生 24 點來源建立僅供本機使用的 3× host 字型子集。"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import struct
import sys
from pathlib import Path

from catalog_font import CatalogError, read_catalog
from eten_font import _stage_bytes, _workplace_path, big5_raw


SOURCE_SHA256 = {
    "std": ("STD.24M", "347ae2655807fc250a18673e6634a363dfba7feee6c3355b886a0810d2d9c030"),
    "spc": ("SPCFONT.24", "da7574d2eee10b9d3b2a2d90bbc39e2ba482b9b2b73a9803f1e4dbefdd91a92a"),
    "ascii": ("ASCFONT.24", "7e69f74bfedf57579fad41a1bc2f0c3a6da873cba1734fd30a1c4afc64893ada"),
    "etunpack": ("etunpack.py", "738e491f65a52e6c716269b5e78b4937510547647615985c1d60b00ec2a4bac6"),
}
LABEL_KEYS = {
    "host.settings", "host.apply", "host.cancel", "host.scale2", "host.scale3"
}
OUTPUT_NAMES = (
    "host-wide24.golemfnt", "host-ascii16x24.golemfnt", "native-host-fonts-manifest.json"
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_locked(path: Path, key: str) -> bytes:
    name, expected = SOURCE_SHA256[key]
    if not path.is_file() or path.is_symlink() or path.name != name:
        raise CatalogError(f"{key}: 本機來源缺失、非一般檔案或檔名不是 {name}: {path}")
    data = path.read_bytes()
    if _sha256(data) != expected:
        raise CatalogError(f"{key}: 本機來源 SHA-256 不符: {path}")
    return data


def _host_codepoints(catalog: Path) -> list[int]:
    entries = read_catalog(catalog)
    by_key = {entry.key: entry.translation for entry in entries}
    if set(by_key) != LABEL_KEYS or any(not text for text in by_key.values()):
        raise CatalogError("host catalog 必須恰有五個非空 host 標籤")
    codepoints = sorted({ord(ch) for text in by_key.values() for ch in text})
    if not codepoints or any(not (ord("0") <= cp <= ord("9") or cp > 127) for cp in codepoints):
        raise CatalogError("3× host 標籤含不支援的 ASCII 字元")
    return codepoints


def _decode_std(std_path: Path, etunpack_path: Path) -> bytes:
    # The external decoder is a caller-supplied, SHA-locked local tool, never
    # imported from the ignored visual A/B prototype.
    spec = importlib.util.spec_from_file_location("eten_host24_locked_decoder", etunpack_path)
    if spec is None or spec.loader is None:
        raise CatalogError("ETUNPACK 解壓器無法載入")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.unpack(str(std_path))
    if not isinstance(result, tuple) or len(result) != 5:
        raise CatalogError("ETUNPACK 回傳格式不符")
    decoded, truncated = result[3], result[4]
    if truncated is not None or not isinstance(decoded, bytes) or len(decoded) != 13094 * 72:
        raise CatalogError("STD.24M 解壓失敗、截斷或長度不符")
    return decoded


def _glyph(codepoint: int, ascii_data: bytes, spc_data: bytes, std_data: bytes) -> tuple[int, bytes]:
    if ord("0") <= codepoint <= ord("9"):
        width, source, index = 16, ascii_data, codepoint
    else:
        raw = big5_raw(codepoint)
        if 0 <= raw <= 407:
            width, source, index = 24, spc_data, raw
        elif 471 <= raw <= 5871:
            width, source, index = 24, std_data, raw - 471
        elif 6280 <= raw <= 13972:
            width, source, index = 24, std_data, 5401 + raw - 6280
        else:
            raise CatalogError(f"U+{codepoint:04X}: Big5 索引落在未證實區段")
    size = 24 * ((width + 7) // 8)
    bitmap = source[index * size:(index + 1) * size]
    if len(bitmap) != size or not any(bitmap):
        raise CatalogError(f"U+{codepoint:04X}: 原生 24 點字模缺失或空白")
    return width, bitmap


def _encode_font(glyphs: dict[int, bytes], width: int) -> bytes:
    size = 24 * ((width + 7) // 8)
    out = bytearray(b"GOLEMFNT" + struct.pack("<HHI", width, 24, len(glyphs)))
    for codepoint, bitmap in sorted(glyphs.items()):
        if len(bitmap) != size or not any(bitmap):
            raise CatalogError(f"U+{codepoint:04X}: GOLEMFNT 字模損壞")
        out.extend(struct.pack("<IB", codepoint, 0))
        out.extend(bitmap)
    return bytes(out)


def _outputs(out_dir: Path, repository: Path, inputs: tuple[Path, ...]) -> tuple[Path, ...]:
    repository = repository.resolve()
    if not out_dir.is_dir() or out_dir.is_symlink():
        raise CatalogError("輸出目錄必須是已存在的一般目錄且不得為符號連結")
    paths = tuple(_workplace_path(out_dir / name, repository) for name in OUTPUT_NAMES)
    resolved_inputs = {path.resolve() for path in inputs}
    if any(path in resolved_inputs for path in paths):
        raise CatalogError("輸出不得覆寫來源或 catalog")
    if any(path.exists() and path.stat().st_nlink != 1 for path in paths):
        raise CatalogError("輸出不得是 hard link")
    return paths


def _publish_three(paths: tuple[Path, ...], payloads: tuple[bytes, ...]) -> None:
    # Validate and stage all three outputs before replacing any existing one.
    old = tuple(path.read_bytes() if path.exists() else None for path in paths)
    staged: list[Path] = []
    backups: list[Path | None] = []
    published: list[int] = []
    try:
        for path, data in zip(paths, payloads):
            staged.append(_stage_bytes(path, data))
        for path, data in zip(paths, old):
            backups.append(_stage_bytes(path, data) if data is not None else None)
        for index, path in enumerate(paths):
            os.replace(staged[index], path)
            published.append(index)
    except BaseException as exc:
        recovery_errors = []
        for index in reversed(published):
            try:
                if backups[index] is None:
                    paths[index].unlink()
                else:
                    os.replace(backups[index], paths[index])
                    backups[index] = None
            except BaseException as restore_exc:
                recovery_errors.append(str(restore_exc))
        if recovery_errors:
            raise CatalogError("三檔發布失敗且回復失敗：" + "; ".join(recovery_errors)) from exc
        raise
    finally:
        for path in (*staged, *(backup for backup in backups if backup is not None)):
            try:
                path.unlink()
            except FileNotFoundError:
                pass


def build(catalog: Path, std_path: Path, spc_path: Path, ascii_path: Path,
          etunpack_path: Path, out_dir: Path, repository: Path | None = None) -> dict[str, object]:
    repository = (repository or Path(__file__).resolve().parents[1]).resolve()
    inputs = (catalog, std_path, spc_path, ascii_path, etunpack_path)
    outputs = _outputs(out_dir, repository, inputs)
    codepoints = _host_codepoints(catalog)
    _read_locked(std_path, "std")
    spc_data = _read_locked(spc_path, "spc")
    ascii_data = _read_locked(ascii_path, "ascii")
    _read_locked(etunpack_path, "etunpack")
    if len(spc_data) != 408 * 72 or len(ascii_data) != 256 * 48:
        raise CatalogError("原生 24 點符號或 ASCII 來源長度不符")
    std_data = _decode_std(std_path, etunpack_path)
    wide: dict[int, bytes] = {}
    ascii_digits: dict[int, bytes] = {}
    for codepoint in codepoints:
        width, bitmap = _glyph(codepoint, ascii_data, spc_data, std_data)
        (ascii_digits if width == 16 else wide)[codepoint] = bitmap
    if not wide or not ascii_digits:
        raise CatalogError("3× host 字型缺少 Wide 或 ASCII 來源")
    font_data = (_encode_font(wide, 24), _encode_font(ascii_digits, 16))
    manifest: dict[str, object] = {
        "status": "local-only-not-for-distribution",
        "catalog": {"filename": catalog.name, "sha256": _sha256(catalog.read_bytes())},
        "source_sha256": {key: spec[1] for key, spec in sorted(SOURCE_SHA256.items())},
        "codepoints": [f"U+{codepoint:04X}" for codepoint in codepoints],
        "outputs": {
            OUTPUT_NAMES[0]: {"sha256": _sha256(font_data[0]), "glyph_count": len(wide), "width": 24, "height": 24},
            OUTPUT_NAMES[1]: {"sha256": _sha256(font_data[1]), "glyph_count": len(ascii_digits), "width": 16, "height": 24},
        },
    }
    manifest_data = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    _publish_three(outputs, (*font_data, manifest_data))
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--std", required=True, type=Path)
    parser.add_argument("--spc", required=True, type=Path)
    parser.add_argument("--ascii", required=True, type=Path)
    parser.add_argument("--etunpack", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        manifest = build(args.catalog, args.std, args.spc, args.ascii, args.etunpack, args.out_dir)
    except (CatalogError, OSError, SyntaxError, ValueError) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
