#!/usr/bin/env python3
"""核對第三頁 control／雙倍率收據與覆繪像素；只讀本機私有產物。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


OUTPUT_ONLY = frozenset(("story_page3_overlay", "story_page3_invalidations"))
RECT = (8, 136, 320, 176)


def pixels(baseline: bytes, overlay: bytes, scale: int) -> tuple[int, int]:
    if scale not in (2, 3):
        raise ValueError("倍率必須為 2 或 3")
    width, height = 320 * scale, 200 * scale
    if len(baseline) != width * height * 4 or len(overlay) != len(baseline):
        raise ValueError("RGBA 尺寸不符")
    left, top, right, bottom = RECT
    inside = outside = 0
    for pos in range(0, len(baseline), 4):
        if baseline[pos:pos + 4] == overlay[pos:pos + 4]:
            continue
        pixel = pos // 4
        x, y = pixel % width, pixel // width
        if left * scale <= x < right * scale and top * scale <= y < bottom * scale:
            inside += 1
        else:
            outside += 1
    return inside, outside


def verify(control: dict, receipt: dict, baseline: bytes, overlay: bytes,
           scale: int, expect_visible: bool) -> dict:
    if any(key in control for key in OUTPUT_ONLY):
        raise ValueError("控制組不得含第三頁覆繪欄位")
    original = {key: value for key, value in receipt.items() if key not in OUTPUT_ONLY}
    if original != control:
        differing = sorted(key for key in set(original) | set(control)
                           if original.get(key) != control.get(key))
        raise ValueError(f"{scale}× 改變原版收據：{differing[:8]}")
    info = receipt.get("story_page3_overlay")
    if not isinstance(info, dict):
        raise ValueError(f"{scale}× 缺少第三頁覆繪收據")
    inside, outside = pixels(baseline, overlay, scale)
    wanted = [f"story.page3.line.{n:03d}" for n in range(1, 6)] if expect_visible else []
    if info.get("scale") != scale or info.get("drew") is not expect_visible or info.get("active_keys") != wanted:
        raise ValueError(f"{scale}× 第三頁啟用狀態不符")
    if info.get("missing_glyphs") not in (None, []):
        raise ValueError(f"{scale}× 譯文有缺字")
    if info.get("baseline_rgba_sha256") != hashlib.sha256(baseline).hexdigest() or \
            info.get("overlay_rgba_sha256") != hashlib.sha256(overlay).hexdigest():
        raise ValueError(f"{scale}× 收據與 RGBA bytes 不符")
    if info.get("diff_inside_story_rect") != inside or info.get("diff_outside_story_rect") != outside:
        raise ValueError(f"{scale}× 收據像素數不符")
    invalidations = receipt.get("story_page3_invalidations", [])
    if expect_visible and invalidations:
        raise ValueError(f"{scale}× 尚可見時不應有離頁清除收據")
    if not expect_visible:
        if len(invalidations) != 1:
            raise ValueError(f"{scale}× 缺少唯一離頁清除收據")
        event = invalidations[0]
        if event.get("instruction") != {"segment": 0x0cf4, "offset": 0x1b3a} or \
                event.get("video_segment") != 0xa000 or event.get("active_keys_before") != 5:
            raise ValueError(f"{scale}× 清除不是已量原版 pre-write")
    if outside:
        raise ValueError(f"{scale}× 安全矩形外有 {outside} 像素差異")
    if expect_visible and not inside:
        raise ValueError(f"{scale}× 預期五行繁中可見")
    if not expect_visible and inside:
        raise ValueError(f"{scale}× 離頁後仍有 {inside} 像素殘留")
    return {"scale": scale, "inside_changed_pixels": inside,
            "outside_changed_pixels": outside,
            "baseline_sha256": hashlib.sha256(baseline).hexdigest(),
            "overlay_sha256": hashlib.sha256(overlay).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control", type=Path, required=True)
    parser.add_argument("--two", type=Path, required=True)
    parser.add_argument("--three", type=Path, required=True)
    parser.add_argument("--expect", choices=("visible", "cleared"), required=True)
    args = parser.parse_args()
    try:
        control = json.loads(args.control.read_text(encoding="utf-8"))
        report = []
        for scale, directory in ((2, args.two), (3, args.three)):
            receipt = json.loads((directory / "receipt.json").read_text(encoding="utf-8"))
            report.append(verify(control, receipt,
                                 (directory / "baseline.rgba").read_bytes(),
                                 (directory / "overlay.rgba").read_bytes(),
                                 scale, args.expect == "visible"))
        print(json.dumps({"expect": args.expect, "scales": report}, ensure_ascii=False, sort_keys=True))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
