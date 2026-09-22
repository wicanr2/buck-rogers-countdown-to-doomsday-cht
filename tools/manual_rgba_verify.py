#!/usr/bin/env python3
"""獨立驗證手冊覆繪的原始 RGBA，並輸出本機 PNG 供目視檢查。"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path


def compare(baseline: bytes, overlay: bytes, scale: int, visible: bool) -> dict:
    if type(scale) is not int or scale not in (2, 3):
        raise ValueError("倍率必須是 2 或 3")
    width, height = 320 * scale, 200 * scale
    if len(baseline) != width * height * 4 or len(overlay) != len(baseline):
        raise ValueError("RGBA 長度與倍率不符")
    inside = outside = 0
    for y in range(height):
        for x in range(width):
            start = (y * width + x) * 4
            if baseline[start:start + 4] == overlay[start:start + 4]:
                continue
            if 7 * scale <= x < 312 * scale and 72 * scale <= y < 184 * scale:
                inside += 1
            else:
                outside += 1
    if outside:
        raise ValueError(f"正文區外有 {outside} 個像素變更")
    if visible and inside == 0:
        raise ValueError("要求中文可見，但覆繪與原版完全相同")
    if not visible and inside:
        raise ValueError("要求舊中文已清除，但正文仍有覆繪差異")
    return {"scale": scale, "visible": visible, "inside_changed_pixels": inside,
            "outside_changed_pixels": outside,
            "baseline_sha256": hashlib.sha256(baseline).hexdigest(),
            "overlay_sha256": hashlib.sha256(overlay).hexdigest()}


def png_bytes(rgba: bytes, scale: int) -> bytes:
    width, height = 320 * scale, 200 * scale
    if scale not in (2, 3) or len(rgba) != width * height * 4:
        raise ValueError("PNG 輸入尺寸無效")

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    rows = b"".join(b"\x00" + rgba[y * width * 4:(y + 1) * width * 4] for y in range(height))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--scale", type=int, choices=(2, 3), required=True)
    parser.add_argument("--expect", choices=("visible", "cleared"), required=True)
    parser.add_argument("--png", type=Path)
    args = parser.parse_args()
    try:
        baseline, overlay = args.baseline.read_bytes(), args.overlay.read_bytes()
        result = compare(baseline, overlay, args.scale, args.expect == "visible")
        if args.png:
            workplace = Path(__file__).resolve().parents[1] / "workplace"
            target = args.png.resolve()
            if not target.is_relative_to(workplace.resolve()):
                raise ValueError("原版及字型衍生 PNG 只可寫入 workplace")
            if target in (args.baseline.resolve(), args.overlay.resolve()):
                raise ValueError("PNG 不得覆寫驗證輸入")
            target.write_bytes(png_bytes(overlay, args.scale))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    except (ValueError, OSError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
