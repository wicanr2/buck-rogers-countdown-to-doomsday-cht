#!/usr/bin/env python3
"""驗證姓名 Enter 清除與 Escape 原地重印的覆繪生命週期。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from name_prompt_runtime_overlay_receipt import OVERLAY_FIELDS, diff_counts, project

EXPECTED = {
    "confirm_control": "4e8eaec59fdf981e196c52aba494db698c21475576fb659ff7ccdd2e60df5468",
    "escape_control": "a3fb3bd40b283b93dbc78d1e5a1ba406edbb31f45ca14312017eaeed87c43556",
    "confirm_fb": "a1cd728cecaa720357f680f2be66e857f401ee5b0113f9959b23143e0fae95f7",
    "escape_fb": "55da7c0e296b882f99c7c8ba2550743debe93a8bc480d1a0fc8fbb1dc514a6bb",
    "confirm_2_json": "18be6427063c7e39b63cda71fd03d51c60c5155846230af2ca8917c7ead05f0a",
    "confirm_3_json": "d77d7e18f522f34747edfe6549eb1e2ca86f031eef6934aed9c05a27b2b73851",
    "escape_2_json": "220087a2c313460b19e6cb5807c3abdae10a4ea6c6571a117e4aaba10e82ddb1",
    "escape_3_json": "562afa6fa22579da574175cfc6ea65c0a131880872bf275c40506cd28c980442",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify(args) -> dict:
    result = {}
    for branch, count, requests, misses, active, drew in (
            ("confirm", 226, 1, 225, [], False),
            ("escape", 184, 2, 182, ["character.name.prompt"], True)):
        control_a = getattr(args, f"{branch}_control_a").read_bytes()
        control_b = getattr(args, f"{branch}_control_b").read_bytes()
        if control_a != control_b or sha(control_a) != EXPECTED[f"{branch}_control"]:
            raise ValueError(f"{branch} control JSON 不決定或 SHA-256 不符")
        control = json.loads(control_a)
        if (len(control["events"]), len(control["requests"]), control["catalog_misses"]) != (count, requests, misses):
            raise ValueError(f"{branch} control 計數不符")
        control_fb_a = getattr(args, f"{branch}_control_a_fb").read_bytes()
        control_fb_b = getattr(args, f"{branch}_control_b_fb").read_bytes()
        if control_fb_a != control_fb_b or sha(control_fb_a) != EXPECTED[f"{branch}_fb"]:
            raise ValueError(f"{branch} control framebuffer 不決定或 SHA-256 不符")
        for scale in (2, 3):
            prefix = f"{branch}_{scale}"
            json_a = getattr(args, f"{prefix}_a_json").read_bytes()
            json_b = getattr(args, f"{prefix}_b_json").read_bytes()
            if json_a != json_b or sha(json_a) != EXPECTED[f"{branch}_{scale}_json"]:
                raise ValueError(f"{branch} {scale}× JSON 不決定或 SHA-256 不符")
            receipt = json.loads(json_a)
            if project(receipt) != control:
                raise ValueError(f"{branch} {scale}× 原版語意 projection 不等於 control")
            if (receipt.get("overlay_scale") != scale or receipt.get("overlay_drew") is not drew or
                    receipt.get("active_overlay_keys", []) != active or
                    len(receipt.get("overlay_actions", [])) != requests or
                    receipt.get("overlay_actions") != receipt["requests"] or
                    receipt.get("overlay_missing_glyphs") not in (None, [])):
                raise ValueError(f"{branch} {scale}× presentation metadata 不符")
            for run in ("a", "b"):
                if getattr(args, f"{prefix}_{run}_fb").read_bytes() != control_fb_a:
                    raise ValueError(f"{branch} {scale}× 改動原版 framebuffer")
            rgba_a = getattr(args, f"{prefix}_a_rgba").read_bytes()
            rgba_b = getattr(args, f"{prefix}_b_rgba").read_bytes()
            baseline_a = getattr(args, f"{prefix}_a_baseline").read_bytes()
            baseline_b = getattr(args, f"{prefix}_b_baseline").read_bytes()
            if rgba_a != rgba_b or baseline_a != baseline_b:
                raise ValueError(f"{branch} {scale}× RGBA 或 baseline 不決定")
            inside, outside, input_column = diff_counts(rgba_a, baseline_a, scale)
            if branch == "confirm" and (inside, outside, input_column) != (0, 0, 0):
                raise ValueError(f"confirm {scale}× 空終態仍有覆繪差異")
            if branch == "escape" and (inside == 0 or outside != 0 or input_column != 0):
                raise ValueError(f"escape {scale}× containment 不符")
            result[prefix] = {"inside_diff_pixels": inside, "outside_diff_pixels": outside,
                              "input_column_diff_pixels": input_column, "active_keys": active,
                              "drew": drew}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for branch in ("confirm", "escape"):
        for run in ("a", "b"):
            parser.add_argument(f"--{branch}-control-{run}", type=Path, required=True)
            parser.add_argument(f"--{branch}-control-{run}-fb", type=Path, required=True)
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
