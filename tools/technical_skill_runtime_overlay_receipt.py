#!/usr/bin/env python3
"""驗證技術技能 base／Down × 2×／3× 執行期繁中覆繪收據。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import technical_skill_screen_text_safe_rects

OVERLAY_FIELDS = {"overlay_scale", "overlay_actions", "active_overlay_keys",
                  "overlay_missing_glyphs", "overlay_drew"}
EXPECTED = {
    "font": "2a9c858becca4b65d30f1bc8f337d83aea7f2df8ad6cc7bebf4ddb43fadf7b99",
    "career_rects": "7cf61d8ccab1edbdffe908b84c296adb5acf7505480d04aceea760655c8f9287",
    "technical_rects": "2384c2eb065049936b0a85bc6bbd6875635596ed7cf4920ef3bfa03a2890f71c",
    "base_fb": "6bf7f9bb55720d24d2193bd1bffcc4abedd7278eb291db4d37398888c183432a",
    "down_fb": "8990a6cb2e7cb240f4e9aa3eb32e0f4fabfcedd0ec5bf994036c307bc1d0729e",
    "base_control": "db5a3b6758cbf82b7c176a2e494294d6ee3bde743000384d3a220413da31cbc7",
    "down_control": "5316175414d4223513389caf05ba8dc1e08b37d6648823f002aed2d9897bb5dc",
    "base_2": "33cbbed95b3c33ee8a002c21d851d7faf4d31dd293cb183746793729f92d85c4",
    "base_3": "18b8e2159395546c3349d33fc40ad35670d0095a96f4350a5cb1b7a6828bfea3",
    "down_2": "9fae9982a589dd2bf9e9691d16cacddc09999447ec149b77e81fed61d2a1225d",
    "down_3": "9e751416a47ad6242e68d599484da8022bf03671da4b49588d8807f79497eafe",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def project(receipt: dict) -> dict:
    return {key: value for key, value in receipt.items() if key not in OVERLAY_FIELDS}


def load_rects(*paths: Path) -> list[tuple[int, int, int, int]]:
    out = []
    for path in paths:
        with path.open(encoding="utf-8", newline="") as stream:
            out.extend((int(row["x"]), int(row["y"]), int(row["width"]), int(row["height"]))
                       for row in csv.DictReader(stream, delimiter="\t"))
    return out


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
        if source_x >= 184 and (source_y in range(8, 24) or source_y in range(48, 152)):
            dynamic += 1
    return inside, outside, dynamic


def expected_active(branch: str) -> list[str]:
    headers = ["technical.screen.general_points.heading", "career.screen.maximum_per_skill.heading",
               "technical.screen.skills.heading", "career.screen.columns.heading"]
    tail = [f"technical.screen.skill.{name}.normal" for name in (
        "repair_nuclear_engine", "repair_life_support", "repair_rocket_hull", "jury_rig",
        "bypass_security", "open_lock", "commo_operation", "sensor_operation", "demolitions",
        "first_aid", "repair_weapon")]
    if branch == "base":
        return headers + ["technical.screen.skill.repair_mechanical.normal"] + tail + [
            "technical.screen.skill.repair_electrical.selected"]
    return headers + tail + ["technical.screen.skill.repair_electrical.normal",
                             "technical.screen.skill.repair_mechanical.selected"]


def verify(args) -> dict:
    technical_skill_screen_text_safe_rects.validate(
        args.technical_rects, args.events, args.translations, args.entry, args.selection)
    for path, key in ((args.font, "font"), (args.career_rects, "career_rects"),
                      (args.technical_rects, "technical_rects")):
        if sha(path.read_bytes()) != EXPECTED[key]:
            raise ValueError(f"{key} SHA-256 不符")
    rects = load_rects(args.career_rects, args.technical_rects)
    result = {}
    for branch, stopped, count, requests, misses, inside in (
            ("base", 103_500_000, 289, 32, 257, {2: 16611, 3: 34423}),
            ("down", 103_800_000, 297, 34, 263, {2: 16611, 3: 34423})):
        control_a = getattr(args, f"control_{branch}_a").read_bytes()
        control_b = getattr(args, f"control_{branch}_b").read_bytes()
        control = json.loads(control_a)
        control_screen_a = getattr(args, f"control_{branch}_screen_a").read_bytes()
        control_screen_b = getattr(args, f"control_{branch}_screen_b").read_bytes()
        if (control_a != control_b or sha(control_a) != EXPECTED[f"{branch}_control"] or
                control_screen_a != control_screen_b or sha(control_screen_a) != EXPECTED[f"{branch}_fb"]):
            raise ValueError(f"{branch} control 不決定或固定雜湊不符")
        if (control["stopped_at"], len(control["events"]), len(control["requests"]),
                control["catalog_misses"]) != (stopped, count, requests, misses):
            raise ValueError(f"{branch} control 計數或穩定 frame 停止點不符")
        for scale in (2, 3):
            prefix = f"{branch}_{scale}"
            json_a = getattr(args, f"{prefix}_a_json").read_bytes()
            json_b = getattr(args, f"{prefix}_b_json").read_bytes()
            if json_a != json_b or sha(json_a) != EXPECTED[prefix]:
                raise ValueError(f"{branch} {scale}× JSON 不決定或固定雜湊不符")
            receipt = json.loads(json_a)
            if project(receipt) != control:
                raise ValueError(f"{branch} {scale}× 原版語意 projection 不等於 control")
            if (receipt.get("overlay_scale") != scale or receipt.get("overlay_drew") is not True or
                    receipt.get("active_overlay_keys") != expected_active(branch) or
                    receipt.get("overlay_actions") != receipt["requests"] or
                    receipt.get("overlay_missing_glyphs") not in (None, [])):
                raise ValueError(f"{branch} {scale}× presentation metadata 不符")
            for run in ("a", "b"):
                if getattr(args, f"{prefix}_{run}_screen").read_bytes() != control_screen_a:
                    raise ValueError(f"{branch} {scale}× 改動原版 framebuffer")
            rgba_a = getattr(args, f"{prefix}_a_rgba").read_bytes()
            rgba_b = getattr(args, f"{prefix}_b_rgba").read_bytes()
            baseline_a = getattr(args, f"{prefix}_a_baseline").read_bytes()
            baseline_b = getattr(args, f"{prefix}_b_baseline").read_bytes()
            if rgba_a != rgba_b or baseline_a != baseline_b:
                raise ValueError(f"{branch} {scale}× RGBA 或 baseline 不決定")
            counts = diff_counts(rgba_a, baseline_a, scale, rects)
            if counts != (inside[scale], 0, 0):
                raise ValueError(f"{branch} {scale}× containment 或動態欄不符：{counts}")
            result[prefix] = {"inside_diff_pixels": counts[0], "outside_diff_pixels": counts[1],
                              "dynamic_column_diff_pixels": counts[2]}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("technical-rects", "career-rects", "events", "translations", "entry", "selection", "font"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    for branch in ("base", "down"):
        for suffix in ("a", "b", "screen-a", "screen-b"):
            parser.add_argument(f"--control-{branch}-{suffix}", type=Path, required=True)
        for scale in (2, 3):
            for run in ("a", "b"):
                for kind in ("json", "rgba", "baseline", "screen"):
                    parser.add_argument(f"--{branch}-{scale}-{run}-{kind}", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args), ensure_ascii=False, sort_keys=True))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
