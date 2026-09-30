#!/usr/bin/env python3
"""用本機 dosgolem 重播角色建立頁，驗證共用倚天字庫的 2×／3× 覆繪。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from manual_rgba_verify import png_bytes
from catalog_lang import add_lang_argument, catalog_name


CATALOGS = (
    ("menu", "menu", "menu"),
    ("gender", "gender", "gender"),
    ("class", "class", "class"),
    ("character-sheet", "character-sheet", "character-sheet"),
    ("name-prompt", "name-prompt", "name-prompt"),
    ("career-skill", "career-skill-screen", "career-skill-screen"),
    ("technical-skill", "technical-skill-screen", "technical-skill-screen"),
)
KEYS = (
    "100010000:1c:0d", "100240000:1c:0d", "100400000:1c:0d",
    "100650000:1c:0d", "101400000:31:6e", "102050000:1e:61",
    "102150000:1c:0d", "102700000:01:1b", "102900000:15:79",
)
OVERLAY_FIELDS = {
    "overlay_scale", "overlay_actions", "active_overlay_keys", "overlay_missing_glyphs", "overlay_drew",
}


def rects(project: Path) -> list[tuple[int, int, int, int]]:
    result = []
    for _, _, stem in CATALOGS:
        with (project / "text" / f"{stem}-text-safe-rects.tsv").open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream, delimiter="\t"):
                result.append(tuple(int(row[key]) for key in ("x", "y", "width", "height")))
    return result


def pixel_counts(before: bytes, after: bytes, scale: int, safe_rects: list[tuple[int, int, int, int]]) -> tuple[int, int]:
    width, height = 320 * scale, 200 * scale
    if len(before) != width * height * 4 or len(after) != len(before):
        raise ValueError("RGBA 輸出尺寸不符")
    inside = outside = 0
    for offset in range(0, len(before), 4):
        if before[offset:offset + 4] == after[offset:offset + 4]:
            continue
        pixel = offset // 4
        x, y = pixel % width, pixel // width
        if any(rx * scale <= x < (rx + rw) * scale and ry * scale <= y < (ry + rh) * scale
               for rx, ry, rw, rh in safe_rects):
            inside += 1
        else:
            outside += 1
    return inside, outside


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", type=Path, required=True)
    parser.add_argument("--state-compare", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    add_lang_argument(parser)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    workplace = project / "workplace"
    output = args.out_dir.resolve()
    if not output.is_relative_to(workplace.resolve()) or output == workplace.resolve() or output.exists():
        parser.error("輸出必須是 workplace 下尚不存在的專用目錄")
    for path in (args.command, args.state_compare, args.state, args.font):
        if not path.is_file():
            parser.error(f"缺少本機輸入：{path}")
    output.mkdir(parents=True)
    common = [str(args.command.resolve()), "-state", str(args.state.resolve()), "-until", "103500000"]
    for key in KEYS:
        common += ["-bios-key-at", key]
    for flag, stem, _ in CATALOGS:
        common += [f"-{flag}-events", str(project / "text" / f"{stem}-events.tsv"),
                   f"-{flag}-translations", str(project / "text" / catalog_name(stem, args.lang))]
    safe_rects = rects(project)

    def run(name: str, scale: int | None) -> dict:
        flags = common + ["-receipt-out", str(output / f"{name}.json"),
                          "-state-out", str(output / f"{name}.state"),
                          "-screen-out", str(output / f"{name}.indexed")]
        if scale is not None:
            for flag, _, stem in CATALOGS:
                flags += [f"-{flag}-rects", str(project / "text" / f"{stem}-text-safe-rects.tsv")]
            flags += ["-overlay-font", str(args.font.resolve()), "-overlay-scale", str(scale),
                      "-overlay-rgba-out", str(output / f"{name}.rgba"),
                      "-baseline-rgba-out", str(output / f"{name}.baseline")]
        subprocess.run(flags, check=True, stdout=subprocess.DEVNULL, timeout=180)
        return json.loads((output / f"{name}.json").read_text())

    control = run("control", None)
    if control.get("stopped_at") != 103500000:
        raise ValueError("控制組未到達指定指令點")
    results = []
    for scale in (2, 3):
        name = f"{scale}x"
        receipt = run(name, scale)
        if {key: value for key, value in receipt.items() if key not in OVERLAY_FIELDS} != control:
            raise ValueError(f"{name} 改變原版收據")
        if (output / f"{name}.indexed").read_bytes() != (output / "control.indexed").read_bytes():
            raise ValueError(f"{name} 改變原始 indexed 畫面")
        compared = subprocess.run([str(args.state_compare.resolve()), "-left", str(output / "control.state"),
                                   "-right", str(output / f"{name}.state")],
                                  check=True, capture_output=True, text=True, timeout=30)
        (output / f"{name}.state-comparison.json").write_text(compared.stdout)
        before = (output / f"{name}.baseline").read_bytes()
        after = (output / f"{name}.rgba").read_bytes()
        inside, outside = pixel_counts(before, after, scale, safe_rects)
        if inside == 0 or outside != 0 or receipt.get("overlay_missing_glyphs") or not receipt.get("overlay_drew"):
            raise ValueError(f"{name} 字模或安全矩形驗收失敗：inside={inside}, outside={outside}")
        (output / f"{name}.png").write_bytes(png_bytes(after, scale))
        results.append({"scale": scale, "inside_changed_pixels": inside, "outside_changed_pixels": outside,
                        "active_keys": len(receipt.get("active_overlay_keys", []))})
    summary = {"state_start": control["state_start"], "stopped_at": control["stopped_at"],
               "input_state_sha256": hashlib.sha256(args.state.read_bytes()).hexdigest(),
               "font_sha256": hashlib.sha256(args.font.read_bytes()).hexdigest(), "results": results}
    (output / "verification.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
