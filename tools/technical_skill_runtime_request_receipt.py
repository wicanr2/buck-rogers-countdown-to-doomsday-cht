#!/usr/bin/env python3
"""驗證技術技能 base／Down 正常路徑的繁中顯示請求。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "base_control": "ee1ee6c8373ee545451866ca8c31fc849a8c02203ef35d6e934f135ca6f47cf0",
    "base_catalog": "9444cea5b0a846221bc1c3c1c4959be5825e1dde76a4799247083fd8cd0832c8",
    "base_fb": "6bf7f9bb55720d24d2193bd1bffcc4abedd7278eb291db4d37398888c183432a",
    "down_control": "a2dfcbd2be5a65a52f10846962994f8b430b9b24eb7540654ed28d40698959ba",
    "down_catalog": "46e9947fbca5bde2b188785700b06b5767672c1af1e00c206d610ef0694d34f9",
    "down_fb": "8990a6cb2e7cb240f4e9aa3eb32e0f4fabfcedd0ec5bf994036c307bc1d0729e",
}
SCREEN_KEYS = [
    "technical.screen.general_points.heading",
    "career.screen.maximum_per_skill.heading",
    "technical.screen.skills.heading",
    "career.screen.columns.heading",
    "technical.screen.skill.repair_electrical.normal",
    "technical.screen.skill.repair_mechanical.normal",
    "technical.screen.skill.repair_nuclear_engine.normal",
    "technical.screen.skill.repair_life_support.normal",
    "technical.screen.skill.repair_rocket_hull.normal",
    "technical.screen.skill.jury_rig.normal",
    "technical.screen.skill.bypass_security.normal",
    "technical.screen.skill.open_lock.normal",
    "technical.screen.skill.commo_operation.normal",
    "technical.screen.skill.sensor_operation.normal",
    "technical.screen.skill.demolitions.normal",
    "technical.screen.skill.first_aid.normal",
    "technical.screen.skill.repair_weapon.normal",
    "technical.screen.skill.repair_electrical.selected",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def semantic(receipt: dict) -> dict:
    return {key: value for key, value in receipt.items() if key not in {"requests", "catalog_misses"}}


def verify(args) -> dict:
    result = {}
    for branch, events, control_requests, catalog_requests, control_misses, catalog_misses, suffix in (
            ("base", 289, 16, 32, 273, 257, []),
            ("down", 297, 16, 34, 281, 263,
             ["technical.screen.skill.repair_electrical.normal",
              "technical.screen.skill.repair_mechanical.selected"])):
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
        if (len(control["events"]), len(control["requests"]), control["catalog_misses"]) != (
                events, control_requests, control_misses):
            raise ValueError(f"{branch} control 計數不符")
        if (len(catalog["events"]), len(catalog["requests"]), catalog["catalog_misses"]) != (
                events, catalog_requests, catalog_misses):
            raise ValueError(f"{branch} catalog 計數不符")
        keys = [row["event_key"] for row in catalog["requests"]]
        if keys[-len(SCREEN_KEYS + suffix):] != SCREEN_KEYS + suffix:
            raise ValueError(f"{branch} 技術技能畫面 request 順序不符")
        for mode in ("control", "catalog"):
            fb_a = getattr(args, f"{branch}_{mode}_a_fb").read_bytes()
            fb_b = getattr(args, f"{branch}_{mode}_b_fb").read_bytes()
            if fb_a != fb_b or sha(fb_a) != EXPECTED[f"{branch}_fb"]:
                raise ValueError(f"{branch} {mode} framebuffer 不決定或 SHA-256 不符")
        if getattr(args, f"{branch}_control_a_fb").read_bytes() != getattr(
                args, f"{branch}_catalog_a_fb").read_bytes():
            raise ValueError(f"{branch} catalog 改動原版 framebuffer")
        result[branch] = {"events": events, "requests": catalog_requests, "misses": catalog_misses}
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
