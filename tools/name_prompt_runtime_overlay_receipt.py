#!/usr/bin/env python3
"""驗證姓名提示 base／A × 2×／3× 執行期覆繪收據。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import name_prompt_text_safe_rects

OVERLAY_FIELDS = {"overlay_scale", "overlay_actions", "active_overlay_keys",
                  "overlay_missing_glyphs", "overlay_drew"}
EXPECTED = {
    "font": "aa53cc31dd2a17fc5554792d3767c1cef757ecda69326c4d17643d211f4d0ea1",
    "base_fb": "55da7c0e296b882f99c7c8ba2550743debe93a8bc480d1a0fc8fbb1dc514a6bb",
    "a_fb": "bd3d779926df3b0e2979f5317f718480057bc01f36768610ac1378aa4c8feec6",
    "base_2_json": "343de86f4279a5f8b13b8443360991425d71b38e537bb9f0144424e30f5fb920",
    "base_3_json": "f50c5c2704286eb2fbd0536243f8817748c6742b43a4e8ffc3f0b9da03173a92",
    "a_2_json": "bee63ca2f523f27d425ee6faed07b5b3746477861c5493f1aae37863ff18d601",
    "a_3_json": "6a05c934e5110aeb07b7e5dbc79b81fbf6d364ce2cb7dfae60e7e2b9a8224b16",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def project(receipt: dict) -> dict:
    return {key: value for key, value in receipt.items() if key not in OVERLAY_FIELDS}


def diff_counts(actual: bytes, baseline: bytes, scale: int) -> tuple[int, int, int]:
    width = 320 * scale
    if len(actual) != width * 200 * scale * 4 or len(actual) != len(baseline):
        raise ValueError("RGBA 尺寸不符")
    inside = outside = input_column = 0
    for pixel in range(len(actual) // 4):
        offset = pixel * 4
        if actual[offset:offset + 4] == baseline[offset:offset + 4]:
            continue
        x, y = pixel % width, pixel // width
        if 0 <= x < 128 * scale and 192 * scale <= y < 200 * scale:
            inside += 1
        else:
            outside += 1
        if x >= 136 * scale and 192 * scale <= y < 200 * scale:
            input_column += 1
    return inside, outside, input_column


def verify(args) -> dict:
    name_prompt_text_safe_rects.validate(args.rects, args.events, args.translations,
                                         args.inventory, args.edit)
    if sha(args.font.read_bytes()) != EXPECTED["font"]:
        raise ValueError("GOLEMFNT SHA-256 不符")
    result = {}
    for branch, count, misses in (("base", 183, 182), ("a", 184, 183)):
        control_raw = getattr(args, f"control_{branch}").read_bytes()
        control = json.loads(control_raw)
        control_fb = getattr(args, f"control_{branch}_fb").read_bytes()
        if sha(control_fb) != EXPECTED[f"{branch}_fb"]:
            raise ValueError(f"{branch} control framebuffer SHA-256 不符")
        if (len(control["events"]), len(control["requests"]), control["catalog_misses"]) != (count, 1, misses):
            raise ValueError(f"{branch} control 計數不符")
        for scale in (2, 3):
            prefix = f"{branch}_{scale}"
            json_a = getattr(args, f"{prefix}_a_json").read_bytes()
            json_b = getattr(args, f"{prefix}_b_json").read_bytes()
            if json_a != json_b or sha(json_a) != EXPECTED[f"{branch}_{scale}_json"]:
                raise ValueError(f"{branch} {scale}× JSON 不決定或 SHA-256 不符")
            receipt = json.loads(json_a)
            if project(receipt) != control:
                raise ValueError(f"{branch} {scale}× 原版語意 projection 不等於 control")
            if (receipt.get("overlay_scale") != scale or receipt.get("overlay_drew") is not True or
                    receipt.get("active_overlay_keys") != ["character.name.prompt"] or
                    receipt.get("overlay_actions") != receipt["requests"] or
                    receipt.get("overlay_missing_glyphs") not in (None, [])):
                raise ValueError(f"{branch} {scale}× presentation metadata 不符")
            for run in ("a", "b"):
                if getattr(args, f"{prefix}_{run}_fb").read_bytes() != control_fb:
                    raise ValueError(f"{branch} {scale}× 改動原版 framebuffer")
            rgba_a = getattr(args, f"{prefix}_a_rgba").read_bytes()
            rgba_b = getattr(args, f"{prefix}_b_rgba").read_bytes()
            baseline_a = getattr(args, f"{prefix}_a_baseline").read_bytes()
            baseline_b = getattr(args, f"{prefix}_b_baseline").read_bytes()
            if rgba_a != rgba_b or baseline_a != baseline_b:
                raise ValueError(f"{branch} {scale}× RGBA 或 baseline 不決定")
            inside, outside, input_column = diff_counts(rgba_a, baseline_a, scale)
            if inside == 0 or outside != 0 or input_column != 0:
                raise ValueError(f"{branch} {scale}× containment 不符")
            result[f"{branch}_{scale}"] = {"inside_diff_pixels": inside,
                                            "outside_diff_pixels": outside,
                                            "input_column_diff_pixels": input_column}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("rects", "events", "translations", "inventory", "edit", "font",
                 "control-base", "control-base-fb", "control-a", "control-a-fb"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    for branch in ("base", "a"):
        for scale in (2, 3):
            for run in ("a", "b"):
                for kind in ("json", "rgba", "baseline", "fb"):
                    parser.add_argument(f"--{branch}-{scale}-{run}-{kind}", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args), ensure_ascii=False, sort_keys=True))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
