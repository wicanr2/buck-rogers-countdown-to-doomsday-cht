#!/usr/bin/env python3
"""驗證性別／職業 2×／3× 覆繪 A/B 的決定性與幾何收據。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import character_text_safe_rects

TOP_FIELDS = {"tool", "screen", "scale", "canvas_width", "canvas_height", "inputs_sha256",
              "events", "missing_glyphs", "diff_outside_safe_rects", "overlapping_rects",
              "base_png_sha256", "output_png_sha256"}
EVENT_FIELDS = {"event_key", "text_key", "translation_runes", "background", "foreground",
                "clear_rect", "draw_anchor_x", "draw_anchor_y", "ink_rect", "contained"}
EXPECTED = {
    "gender-steady-2x": ("35ebd3a09d37d00c15080b0456b195aeb64e91bdd59c410699b12a09223d8d4e", "508bd19c16fc9e3880be78cdec83de0f4efa6606fa2eaced9f9ae82600fcb133", "88e58d9622b5a298c055123fa56406b6afbbea04f026ca5a578b7565d89190ce", 3),
    "gender-steady-3x": ("631895b6fa3163312de9e2df3a4c316acb407a8203c7559f3a6deb6fde46e6a3", "02a6e947bfb012eddb6b5fdf7d170bf78e6943ea01256e9ef580e61d024e3315", "fea746d6d1dad2be10b7ba6317d0629a45e2d6fc4b384fe956465949f6872c9c", 3),
    "gender-down-2x": ("61b502903f4d52140f772ea359dcecf39799e5291a0b74fe3049ace45e4025fa", "5a80dc0155303489a8d37e51b0d722a576bc825e152a8a02db2eedaee87ee87a", "9964e1986c04f99878c24885521058572410862798b97ab39c1162793475bab4", 3),
    "gender-down-3x": ("2c5c487077c681d9f05df73a5c0fdf355fa76f73c3b511b5b90548c666df6edc", "6eb7fb76dbaaaef811b63314492800a179ac1542fb166824d278752ed764be4d", "33d1364970424360c9502335d574db76f7ff13b344f7a4741ec974b13a15102b", 3),
    "class-steady-2x": ("1603e8398ac9110cc4071e20e7e1e2eaa0189b6cb4346ea506c809f0dbf628a2", "c0eff428f4125099b88cbc7d288b90dead436f8b4dea64a60a33b1ff37741309", "6efc1200dfa75134a0c914f18e3e459c22198369bdcc0de2e0a7b4147abf4ae4", 6),
    "class-steady-3x": ("d3edb3168648adb2d04885ab612b3a37a4ea5bcfe3ad6c8158538bd9220e3815", "c5461f92f6e31bd4c6acc8519fa48deafc1f5dc6168e0414b8b0725fea02b74e", "5412bb8502d9f4116969c20fbc7b940f45c534a5de36db066c3db44a43baba50", 6),
    "class-down-2x": ("b1bd589bf913f12e5d991962fc04f9fd76638604bf9066338554f8fa48edbce9", "04220ed98f774d38f37b12bb3ed382ec4744ebadd1f6fee559d5af8091f12569", "db0f2a855b330797269fde2ea99448895e0c95a4a52c128cd0f7433b5f6cc9c1", 6),
    "class-down-3x": ("33df44fea5170647ec0502ee76aaed58dcc6393c57e765b5ab56a90d7c580c73", "632885aa073efc186e4f3909643e8a9cf406e2ba437eb746b374971e90bfee1c", "42cff160673c60f06e91eed4f25e9a3e855e74243e3f64a8488205cdeb672de4", 6),
}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _validate_receipt(data: dict, screen: str, scale: int, count: int) -> None:
    if set(data) != TOP_FIELDS or data["tool"] != "dosgolem/cmd/buckrogers-overlay-prototype":
        raise ValueError("character overlay receipt: 頂層 schema 或工具不符")
    if data["screen"] != screen or data["scale"] != scale or (data["canvas_width"], data["canvas_height"]) != (320 * scale, 200 * scale):
        raise ValueError("character overlay receipt: 畫面或 canvas 不符")
    if len(data["events"]) != count or data["missing_glyphs"] != [] or data["diff_outside_safe_rects"] != 0 or data["overlapping_rects"] != 0:
        raise ValueError("character overlay receipt: 數量、缺字或幾何閘門不符")
    for event in data["events"]:
        if set(event) != EVENT_FIELDS or not event["contained"] or event["translation_runes"] <= 0:
            raise ValueError("character overlay receipt: event schema 或 containment 不符")
        clear, ink = event["clear_rect"], event["ink_rect"]
        if not (ink["X"] >= clear["X"] and ink["Y"] >= clear["Y"] and
                ink["X"] + ink["Width"] <= clear["X"] + clear["Width"] and
                ink["Y"] + ink["Height"] <= clear["Y"] + clear["Height"]):
            raise ValueError("character overlay receipt: ink 超出 clear rect")


def verify(root_a: Path, root_b: Path, gender_rects: Path, gender_events_path: Path,
           gender_catalog: Path, post_race: Path, gender_lifecycle: Path, class_rects: Path,
           class_events_path: Path, class_catalog: Path, post_gender: Path, class_lifecycle: Path) -> None:
    character_text_safe_rects.validate(gender_rects, gender_events_path, gender_catalog, "gender", post_race, gender_lifecycle)
    character_text_safe_rects.validate(class_rects, class_events_path, class_catalog, "class", post_gender, class_lifecycle)
    for stem, (json_sha, png_sha, base_sha, count) in EXPECTED.items():
        screen, scale_text = stem.rsplit("-", 1)
        scale = int(scale_text[0])
        raw_a, raw_b = (root_a / f"{stem}.json").read_bytes(), (root_b / f"{stem}.json").read_bytes()
        png_a, png_b = (root_a / f"{stem}.png").read_bytes(), (root_b / f"{stem}.png").read_bytes()
        base_name = f"{screen}-base-{scale}x.png"
        base_a, base_b = (root_a / base_name).read_bytes(), (root_b / base_name).read_bytes()
        if raw_a != raw_b or _sha(raw_a) != json_sha or png_a != png_b or _sha(png_a) != png_sha or base_a != base_b or _sha(base_a) != base_sha:
            raise ValueError(f"character overlay receipt: {stem} 重播或 SHA-256 不符")
        data = json.loads(raw_a)
        _validate_receipt(data, screen, scale, count)
        if data["output_png_sha256"] != png_sha or data["base_png_sha256"] != base_sha:
            raise ValueError(f"character overlay receipt: {stem} 內嵌 PNG SHA-256 不符")
