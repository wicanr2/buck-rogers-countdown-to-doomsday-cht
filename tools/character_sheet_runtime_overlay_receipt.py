#!/usr/bin/env python3
"""驗證角色資料頁 base／Y × 2×／3× runtime overlay 收據。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import character_sheet_text_safe_rects

EXPECTED = {
    "base_control": "e34747b8668b795c554ec4e4903302ad9b42d94986e1b2229fcc24318e669be2",
    "y_control": "6cde56ed72e0a42547f0ec3f400e282f4605cab279c60b7fea6482319d63ea15",
    "base_fb": "1f3b81946cc058d89a8ecfd9ca5aab8e7fb2aaa5d95c2c2ecbd49c219f51d4dd",
    "y_fb": "03d9bf1fcdd871055949c5545eaf102fecb7aa6ef0f3b3e09a2dcf6e95050f97",
    "base_2_json": "bd22f043ff7fce34e43019f5d47ace5b03115d46c84d2232a4c6772eead7e8f5",
    "base_3_json": "017754308975b79c338043762a8650355e28810d8b56819d7e7d611a41ca7c67",
    "y_2_json": "9e91f7009c07c346c2d46133a417658b37ac83b1fc1e1c831ca88b20ffe0422e",
    "y_3_json": "ed7357171bf5f23eb5953b5bf1fe15ec228e2667068463f0b920e952dcf46717",
    "2_baseline": "3403cae25a7c7b0618242f8df0be549dbb7f7a56a854749cd4791c253c6c44b4",
    "3_baseline": "5a357214bfea4c2b782dd61d109701d8956ffe9404a9e77e433ef54d8e7fd980",
    "2_rgba": "e140f2492321dceca7edcd040a1ad0b8ae916353a6f342300628f7e788cd3def",
    "3_rgba": "5706ef26c94b08fdd58c54c2143c58e976629351f21e56ebfea3c2a52c59aa4b",
    "font": "5949e5b26268f2d469004888bbbba291a4e50b2a58ca24938e0a669eb171b2dc",
}
OVERLAY_FIELDS = {"overlay_scale", "overlay_actions", "active_overlay_keys",
                  "overlay_missing_glyphs", "overlay_drew"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def project(receipt: dict) -> dict:
    return {key: value for key, value in receipt.items() if key not in OVERLAY_FIELDS}


def outside_diff(actual: bytes, baseline: bytes, width: int,
                 rects: list[tuple[int, int, int, int]]) -> tuple[int, int]:
    if len(actual) != len(baseline) or len(actual) % (width * 4):
        raise ValueError("RGBA 尺寸不符")
    inside = outside = 0
    for pixel in range(len(actual) // 4):
        at = pixel * 4
        if actual[at:at + 4] == baseline[at:at + 4]:
            continue
        x, y = pixel % width, pixel // width
        if any(rx <= x < rx + rw and ry <= y < ry + rh for rx, ry, rw, rh in rects):
            inside += 1
        else:
            outside += 1
    return inside, outside


def verify(args) -> dict:
    character_sheet_text_safe_rects.validate(args.rects, args.events, args.translations, args.inventory)
    if sha(args.font.read_bytes()) != EXPECTED["font"]:
        raise ValueError("GOLEMFNT SHA-256 不符")
    with args.rects.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    active = [row["event_key"] for row in rows]
    logical_rects = [tuple(int(row[field]) for field in ("x", "y", "width", "height")) for row in rows]
    result = {}
    for branch, expected_events, expected_requests, expected_misses in (("base", 118, 43, 75), ("y", 149, 52, 97)):
        control_path = getattr(args, f"control_{branch}")
        control_raw = control_path.read_bytes()
        if sha(control_raw) != EXPECTED[f"{branch}_control"]:
            raise ValueError(f"{branch} control JSON SHA-256 不符")
        control = json.loads(control_raw)
        control_fb = getattr(args, f"control_{branch}_fb").read_bytes()
        if sha(control_fb) != EXPECTED[f"{branch}_fb"]:
            raise ValueError(f"{branch} control framebuffer SHA-256 不符")
        if (len(control["events"]), len(control["requests"]), control["catalog_misses"]) != (
                expected_events, expected_requests, expected_misses):
            raise ValueError(f"{branch} control 計數不符")
        for scale in (2, 3):
            first_json = getattr(args, f"{branch}_{scale}_a_json")
            second_json = getattr(args, f"{branch}_{scale}_b_json")
            first_raw, second_raw = first_json.read_bytes(), second_json.read_bytes()
            if first_raw != second_raw or sha(first_raw) != EXPECTED[f"{branch}_{scale}_json"]:
                raise ValueError(f"{branch} {scale}× JSON 不決定或 SHA-256 不符")
            receipt = json.loads(first_raw)
            if project(receipt) != control:
                raise ValueError(f"{branch} {scale}× 原版語意 projection 不等於 control")
            if (receipt.get("overlay_scale") != scale or receipt.get("overlay_drew") is not True or
                    receipt.get("active_overlay_keys") != active or
                    receipt.get("overlay_actions") != receipt["requests"] or
                    receipt.get("overlay_missing_glyphs") not in (None, [])):
                raise ValueError(f"{branch} {scale}× presentation metadata 不符")
            for fb_path in (getattr(args, f"{branch}_{scale}_a_fb"), getattr(args, f"{branch}_{scale}_b_fb")):
                if fb_path.read_bytes() != control_fb:
                    raise ValueError(f"{branch} {scale}× 改動原版 framebuffer")
            baseline_a = getattr(args, f"{branch}_{scale}_a_baseline").read_bytes()
            baseline_b = getattr(args, f"{branch}_{scale}_b_baseline").read_bytes()
            rgba_a = getattr(args, f"{branch}_{scale}_a_rgba").read_bytes()
            rgba_b = getattr(args, f"{branch}_{scale}_b_rgba").read_bytes()
            if baseline_a != baseline_b or sha(baseline_a) != EXPECTED[f"{scale}_baseline"]:
                raise ValueError(f"{branch} {scale}× baseline 不決定")
            if rgba_a != rgba_b or sha(rgba_a) != EXPECTED[f"{scale}_rgba"]:
                raise ValueError(f"{branch} {scale}× RGBA 不決定")
            scaled = [(x * scale, y * scale, w * scale, h * scale) for x, y, w, h in logical_rects]
            inside, outside = outside_diff(rgba_a, baseline_a, 320 * scale, scaled)
            if inside == 0 or outside != 0:
                raise ValueError(f"{branch} {scale}× containment 不符：inside={inside} outside={outside}")
            result[f"{branch}_{scale}"] = {"inside_diff_pixels": inside, "outside_diff_pixels": outside}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("rects", "events", "translations", "inventory", "font", "control-base", "control-base-fb",
                 "control-y", "control-y-fb"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    for branch in ("base", "y"):
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
