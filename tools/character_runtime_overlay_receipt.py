#!/usr/bin/env python3
"""驗證性別／職業正常路徑的明示倍率 runtime overlay 收據。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


EXPECTED = {
    "control_json": "7e2cc671620231022f8cc5d477804aaac1aa727a7d0bf469cd46ed99cd01742f",
    "framebuffer": "49d8b036f2c6f0d7fe2d897b8ffcac46db15a5e8386fa0eb4d9c30ae8cccc81c",
    "2_json": "0978effcd3abae7e6e21cf0d0cbd7194c2f38439a60e6b08a599abce1b3844b2",
    "2_rgba": "cd62698f26df1c93d527a17addaf043ba8a0342926c1688b65b89663935cc8c2",
    "3_json": "74d3cac8d987af166e8b936fed5ce08f53c5260c6c7f1eb4dedcd704329d0208",
    "3_rgba": "b769435f2f79bd32b810db7ad51d865351cdd6f2dc2819c46226108f80be6725",
    "font": "3714d47c12f900f7e1f96d73e510d162d46685b78b9ec595d9a7bf3a7e7545ae",
    "palette": "045796505f7ec3115cec8632ca7a29e6391687a2a013198e38dd68dd5b3564eb",
}
OVERLAY_FIELDS = {
    "overlay_scale", "overlay_actions", "active_overlay_keys",
    "overlay_missing_glyphs", "overlay_drew",
}
ACTIVE = [
    "class.screen.prompt", "class.option.rocket_jock", "class.option.medic",
    "class.option.warrior", "class.option.engineer", "class.option.rogue",
    "class.selection.normal.rocket_jock", "class.selection.selected.medic",
]


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _project(receipt: dict) -> dict:
    return {key: value for key, value in receipt.items() if key not in OVERLAY_FIELDS}


def _rects(paths: list[Path]) -> dict[str, tuple[int, int, int, int]]:
    out = {}
    for path in paths:
        with path.open(encoding="utf-8", newline="") as source:
            for row in csv.DictReader(source, delimiter="\t"):
                key = row["event_key"]
                if key in out:
                    raise ValueError(f"重複安全矩形：{key}")
                out[key] = tuple(int(row[field]) for field in ("x", "y", "width", "height"))
    return out


def _baseline_rgba(framebuffer: bytes, palette: bytes, scale: int) -> bytes:
    if len(framebuffer) != 320 * 200 or len(palette) != 256 * 3:
        raise ValueError("framebuffer 或 palette 尺寸不符")
    width = 320 * scale
    out = bytearray(width * 200 * scale * 4)
    for y in range(200):
        for x in range(320):
            color = palette[framebuffer[y * 320 + x] * 3:][:3] + b"\xff"
            for dy in range(scale):
                for dx in range(scale):
                    at = ((y * scale + dy) * width + x * scale + dx) * 4
                    out[at:at + 4] = color
    return bytes(out)


def _outside_diff(actual: bytes, baseline: bytes, width: int,
                  rects: list[tuple[int, int, int, int]]) -> tuple[int, int]:
    if len(actual) != len(baseline) or len(actual) % (width * 4):
        raise ValueError("RGBA 尺寸不符")
    inside = outside = 0
    for pixel in range(len(actual) // 4):
        at = pixel * 4
        if actual[at:at + 4] == baseline[at:at + 4]:
            continue
        x, y = pixel % width, pixel // width
        contained = any(rx <= x < rx + rw and ry <= y < ry + rh for rx, ry, rw, rh in rects)
        if contained:
            inside += 1
        else:
            outside += 1
    return inside, outside


def verify(args) -> dict:
    control_raw = args.control_json.read_bytes()
    if _sha(control_raw) != EXPECTED["control_json"]:
        raise ValueError("control JSON SHA-256 不符")
    control = json.loads(control_raw)
    if len(control["events"]) != 24 or len(control["requests"]) != 24 or control["catalog_misses"] != 0:
        raise ValueError("control 事件／請求／miss 不符")

    framebuffer = args.control_fb.read_bytes()
    if _sha(framebuffer) != EXPECTED["framebuffer"]:
        raise ValueError("control framebuffer SHA-256 不符")
    for path in args.overlay_fb:
        if path.read_bytes() != framebuffer:
            raise ValueError(f"原版 framebuffer 被覆繪改變：{path}")
    if _sha(args.font.read_bytes()) != EXPECTED["font"]:
        raise ValueError("合併 GOLEMFNT SHA-256 不符")
    palette = args.palette.read_bytes()
    if _sha(palette) != EXPECTED["palette"]:
        raise ValueError("palette SHA-256 不符")

    rect_catalog = _rects(args.rects)
    results = {}
    for scale, first_json, second_json, first_rgba, second_rgba in (
        (2, args.a2_json, args.b2_json, args.a2_rgba, args.b2_rgba),
        (3, args.a3_json, args.b3_json, args.a3_rgba, args.b3_rgba),
    ):
        first_raw, second_raw = first_json.read_bytes(), second_json.read_bytes()
        if first_raw != second_raw or _sha(first_raw) != EXPECTED[f"{scale}_json"]:
            raise ValueError(f"{scale}× JSON 不決定或 SHA-256 不符")
        receipt = json.loads(first_raw)
        if _project(receipt) != control:
            raise ValueError(f"{scale}× 原版語意 projection 不等於 control")
        if receipt.get("overlay_scale") != scale or receipt.get("overlay_drew") is not True:
            raise ValueError(f"{scale}× 覆繪旗標不符")
        if receipt.get("active_overlay_keys") != ACTIVE:
            raise ValueError(f"{scale}× 終態 active keys 不符")
        if receipt.get("overlay_actions") != receipt["requests"]:
            raise ValueError(f"{scale}× request／action 不是一一對應")
        if receipt.get("overlay_missing_glyphs") not in (None, []):
            raise ValueError(f"{scale}× 有缺字")

        rgba_a, rgba_b = first_rgba.read_bytes(), second_rgba.read_bytes()
        if rgba_a != rgba_b or _sha(rgba_a) != EXPECTED[f"{scale}_rgba"]:
            raise ValueError(f"{scale}× RGBA 不決定或 SHA-256 不符")
        baseline = _baseline_rgba(framebuffer, palette, scale)
        scaled_rects = []
        for key in ACTIVE:
            if key not in rect_catalog:
                raise ValueError(f"active key 缺安全矩形：{key}")
            x, y, width, height = rect_catalog[key]
            scaled_rects.append((x * scale, y * scale, width * scale, height * scale))
        inside, outside = _outside_diff(rgba_a, baseline, 320 * scale, scaled_rects)
        if inside == 0 or outside != 0:
            raise ValueError(f"{scale}× 像素 containment 不符：inside={inside} outside={outside}")
        results[str(scale)] = {"inside_diff_pixels": inside, "outside_diff_pixels": outside}
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-json", type=Path, required=True)
    parser.add_argument("--control-fb", type=Path, required=True)
    parser.add_argument("--overlay-fb", type=Path, action="append", required=True)
    for name in ("a2-json", "b2-json", "a3-json", "b3-json", "a2-rgba", "b2-rgba", "a3-rgba", "b3-rgba"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--palette", type=Path, required=True)
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--rects", type=Path, action="append", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args), ensure_ascii=False, sort_keys=True))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
