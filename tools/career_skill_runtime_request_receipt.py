#!/usr/bin/env python3
"""驗證職業技能 base／Down 正常路徑的繁中顯示請求。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "base_control": "4e8eaec59fdf981e196c52aba494db698c21475576fb659ff7ccdd2e60df5468",
    "base_catalog": "488261912e585c5458f44e8f0e15c1fd89de276cd9a35c7fa08185f48adb1c6b",
    "base_fb": "a1cd728cecaa720357f680f2be66e857f401ee5b0113f9959b23143e0fae95f7",
    "down_control": "da4a0aedd90db566dacd07273d98902e8f25aacbb2b707ac009a51570fe7750b",
    "down_catalog": "2d99e5b56beaf7c7c4e29bd91ed3ec56530bd4cefdd690eee7a29d1506db73e6",
    "down_fb": "ddf66e0c914953ee369e93c73acdeb51d01a84e37d73cb31582ab7c77b4d6cbd",
}
BASE_KEYS = [
    "character.name.prompt",
    "career.screen.remaining_points.heading",
    "career.screen.maximum_per_skill.heading",
    "career.screen.skills.heading",
    "career.screen.columns.heading",
    "career.screen.skill.notice.normal",
    "career.screen.skill.maneuver_zero_g.normal",
    "career.screen.skill.use_jetpack.normal",
    "career.screen.skill.pilot_rocket.normal",
    "career.screen.skill.pilot_fixed_wing.normal",
    "career.screen.skill.drive_ground_car.normal",
    "career.screen.skill.pilot_rotorwing.normal",
    "career.screen.skill.drive_jetcar.normal",
    "career.screen.skill.notice.selected",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def semantic(receipt: dict) -> dict:
    return {key: value for key, value in receipt.items() if key not in {"requests", "catalog_misses"}}


def verify(args) -> dict:
    result = {}
    for branch, events, requests, misses, suffix in (
            ("base", 226, 14, 212, []),
            ("down", 234, 16, 218,
             ["career.screen.skill.notice.normal", "career.screen.skill.maneuver_zero_g.selected"])):
        control_a = getattr(args, f"{branch}_control_a").read_bytes()
        control_b = getattr(args, f"{branch}_control_b").read_bytes()
        catalog_a = getattr(args, f"{branch}_catalog_a").read_bytes()
        catalog_b = getattr(args, f"{branch}_catalog_b").read_bytes()
        if control_a != control_b or sha(control_a) != EXPECTED[f"{branch}_control"]:
            raise ValueError(f"{branch} control 不決定或 SHA-256 不符")
        if catalog_a != catalog_b or sha(catalog_a) != EXPECTED[f"{branch}_catalog"]:
            raise ValueError(f"{branch} catalog 不決定或 SHA-256 不符")
        control, catalog = json.loads(control_a), json.loads(catalog_a)
        if semantic(control) != semantic(catalog):
            raise ValueError(f"{branch} catalog 改動原版語意")
        if (len(catalog["events"]), len(catalog["requests"]), catalog["catalog_misses"]) != (
                events, requests, misses):
            raise ValueError(f"{branch} 計數不符")
        if [row["event_key"] for row in catalog["requests"]] != BASE_KEYS + suffix:
            raise ValueError(f"{branch} request 順序不符")
        for mode in ("control", "catalog"):
            fb_a = getattr(args, f"{branch}_{mode}_a_fb").read_bytes()
            fb_b = getattr(args, f"{branch}_{mode}_b_fb").read_bytes()
            if fb_a != fb_b or sha(fb_a) != EXPECTED[f"{branch}_fb"]:
                raise ValueError(f"{branch} {mode} framebuffer 不決定或 SHA-256 不符")
        if getattr(args, f"{branch}_control_a_fb").read_bytes() != getattr(
                args, f"{branch}_catalog_a_fb").read_bytes():
            raise ValueError(f"{branch} catalog 改動原版 framebuffer")
        result[branch] = {"events": events, "requests": requests, "misses": misses}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for branch in ("base", "down"):
        for mode in ("control", "catalog"):
            for run in ("a", "b"):
                parser.add_argument(f"--{branch}-{mode}-{run}", type=Path, required=True)
                parser.add_argument(f"--{branch}-{mode}-{run}-fb", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args), ensure_ascii=False, sort_keys=True))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
