#!/usr/bin/env python3
"""驗證職業技能 base／Down × 2×／3× 執行期繁中覆繪收據。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import career_skill_screen_text_safe_rects

OVERLAY_FIELDS = {"overlay_scale", "overlay_actions", "active_overlay_keys",
                  "overlay_missing_glyphs", "overlay_drew"}
EXPECTED = {
    "font": "63bbc98f9397e5e866fec8b0b135d85b6f9ad245586b60550dca9ab4d7789975",
    "base_fb": "a1cd728cecaa720357f680f2be66e857f401ee5b0113f9959b23143e0fae95f7",
    "down_fb": "ddf66e0c914953ee369e93c73acdeb51d01a84e37d73cb31582ab7c77b4d6cbd",
    "base_2_json": "47360f636419442d0dbc421b24f798ca590cf0e6453bfa69e013d4b893ec2d92",
    "base_3_json": "fb6498127ddfc8264de3e958489aa55d5c4f82d05c57d369af6ffcfa126d81c8",
    "down_2_json": "0a28030fdf30213a72490dd407a80e5090d50b5cb46d82a28f27a1ffa22ba111",
    "down_3_json": "e5975ebed014b298363923c278a0f7e332927bc26c93a6e0bbe3b6785dd2accb",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def project(receipt: dict) -> dict:
    return {key: value for key, value in receipt.items() if key not in OVERLAY_FIELDS}


def load_rects(path: Path) -> list[tuple[int, int, int, int]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return [(int(row["x"]), int(row["y"]), int(row["width"]), int(row["height"]))
                for row in csv.DictReader(stream, delimiter="\t")]


def diff_counts(actual: bytes, baseline: bytes, scale: int,
                rects: list[tuple[int, int, int, int]]) -> tuple[int, int, int]:
    width, height = 320 * scale, 200 * scale
    if len(actual) != width * height * 4 or len(actual) != len(baseline):
        raise ValueError("RGBA 尺寸不符")
    inside = outside = dynamic = 0
    for pixel in range(len(actual) // 4):
        offset = pixel * 4
        if actual[offset:offset + 4] == baseline[offset:offset + 4]:
            continue
        x, y = pixel % width, pixel // width
        if any(rx * scale <= x < (rx + rw) * scale and
               ry * scale <= y < (ry + rh) * scale for rx, ry, rw, rh in rects):
            inside += 1
        else:
            outside += 1
        source_x, source_y = x // scale, y // scale
        if source_x >= 184 and (source_y in range(8, 24) or source_y in range(48, 112)):
            dynamic += 1
    return inside, outside, dynamic


def expected_active(branch: str) -> list[str]:
    headers = ["career.screen.remaining_points.heading", "career.screen.maximum_per_skill.heading",
               "career.screen.skills.heading", "career.screen.columns.heading"]
    common = ["career.screen.skill.use_jetpack.normal", "career.screen.skill.pilot_rocket.normal",
              "career.screen.skill.pilot_fixed_wing.normal", "career.screen.skill.drive_ground_car.normal",
              "career.screen.skill.pilot_rotorwing.normal", "career.screen.skill.drive_jetcar.normal"]
    if branch == "base":
        return headers + ["career.screen.skill.maneuver_zero_g.normal"] + common + ["career.screen.skill.notice.selected"]
    return headers + common + ["career.screen.skill.notice.normal", "career.screen.skill.maneuver_zero_g.selected"]


def verify(args) -> dict:
    career_skill_screen_text_safe_rects.validate(
        args.rects, args.events, args.translations, args.confirm, args.selection, args.character_text)
    if sha(args.font.read_bytes()) != EXPECTED["font"]:
        raise ValueError("GOLEMFNT SHA-256 不符")
    rects = load_rects(args.rects)
    result = {}
    for branch, count, requests, misses in (("base", 226, 14, 212), ("down", 234, 16, 218)):
        control_raw = getattr(args, f"control_{branch}").read_bytes()
        control = json.loads(control_raw)
        control_fb = getattr(args, f"control_{branch}_fb").read_bytes()
        if sha(control_fb) != EXPECTED[f"{branch}_fb"]:
            raise ValueError(f"{branch} control framebuffer SHA-256 不符")
        if (len(control["events"]), len(control["requests"]), control["catalog_misses"]) != (count, requests, misses):
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
                    receipt.get("active_overlay_keys") != expected_active(branch) or
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
            inside, outside, dynamic = diff_counts(rgba_a, baseline_a, scale, rects)
            if inside == 0 or outside != 0 or dynamic != 0:
                raise ValueError(f"{branch} {scale}× containment 或動態數值邊界不符")
            result[prefix] = {"inside_diff_pixels": inside, "outside_diff_pixels": outside,
                              "dynamic_column_diff_pixels": dynamic}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("rects", "events", "translations", "confirm", "selection", "character-text", "font",
                 "control-base", "control-base-fb", "control-down", "control-down-fb"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    for branch in ("base", "down"):
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
