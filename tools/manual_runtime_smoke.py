#!/usr/bin/env python3
"""在 Docker 內重播原版及雙倍率手冊覆繪，獨立驗證狀態與像素。"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from manual_rgba_verify import compare, png_bytes
from catalog_lang import DEFAULT_LANG, add_lang_argument, catalog_name


def run_case(command: Path, state_compare: Path, state: Path, font: Path, out: Path, until: int, keys: list[str], visible: bool,
             lang: str = DEFAULT_LANG) -> dict:
    project = Path(__file__).resolve().parents[1]
    common = [str(command.resolve()), "-state", str(state.resolve()), "-until", str(until),
              "-file-ops", "-unimplemented"]
    for key in keys:
        common += ["-bios-key-at", key]

    def run(name: str, extras: list[str]) -> dict:
        args = common + ["-receipt-out", str(out / (name + ".json")),
                         "-screen-out", str(out / (name + ".indexed")),
                         "-state-out", str(out / (name + ".state"))] + extras
        subprocess.run(args, check=True, stdout=subprocess.DEVNULL, timeout=180)
        return json.loads((out / (name + ".json")).read_text())

    control = run("control", [])
    state_bytes = (out / "control.state").read_bytes()
    indexed = (out / "control.indexed").read_bytes()
    for required in ("memory_sha256", "indexed_sha256", "palette_sha256", "events", "stopped_at"):
        if required not in control:
            raise ValueError(f"control 缺必要狀態欄位：{required}")
    if control["stopped_at"] != until:
        raise ValueError("重播未到達要求步數")
    result = {"state_sha256": hashlib.sha256(state.read_bytes()).hexdigest(),
              "font_sha256": hashlib.sha256(font.read_bytes()).hexdigest(),
              "start": control["state_start"], "until": until, "keys": keys, "scales": []}
    for scale in (2, 3):
        name = str(scale) + "x"
        extras = ["-manual-events", str(project / "text/manual-events.tsv"),
                  "-manual-ordinals", str(project / "text/manual-ordinals.tsv"),
                  "-manual-translations", str(project / "text" / catalog_name("manual", lang)),
                  "-manual-layout", str(project / "text/manual-overlay-layout.tsv"),
                  "-manual-overlay-font", str(font.resolve()), "-manual-overlay-scale", str(scale),
                  "-manual-overlay-rgba-out", str(out / (name + ".rgba")),
                  "-manual-baseline-rgba-out", str(out / (name + ".baseline")),
                  "-manual-overlay-png-out", str(out / (name + ".renderer.png")),
                  "-manual-baseline-png-out", str(out / (name + ".baseline.png"))]
        receipt = run(name, extras)
        for field, value in control.items():
            if receipt.get(field) != value:
                raise ValueError(f"{name} 改變原版收據：{field}")
        if (out / (name + ".state")).read_bytes() != state_bytes:
            # gob 對 map 的序列化順序不固定，需比較解碼後的完整持久化狀態。
            equality = subprocess.run([str(state_compare.resolve()), "-left", str(out / "control.state"),
                                       "-right", str(out / (name + ".state"))],
                                      check=True, capture_output=True, text=True, timeout=30)
            (out / (name + ".state-comparison.json")).write_text(equality.stdout)
        if (out / (name + ".indexed")).read_bytes() != indexed:
            raise ValueError(f"{name} 原版 indexed 畫面不同")
        baseline = (out / (name + ".baseline")).read_bytes()
        overlay = (out / (name + ".rgba")).read_bytes()
        comparison = compare(baseline, overlay, scale, visible)
        (out / (name + ".png")).write_bytes(png_bytes(overlay, scale))
        comparison["original_state_identical"] = True
        result["scales"].append(comparison)
    (out / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", type=Path, required=True)
    parser.add_argument("--state-compare", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--until", type=int, default=266557247)
    parser.add_argument("--bios-key-at", action="append", default=[])
    parser.add_argument("--expect", choices=("visible", "cleared"), default="visible")
    add_lang_argument(parser)
    args = parser.parse_args()
    try:
        workplace = Path(__file__).resolve().parents[1] / "workplace"
        output = args.out_dir.resolve()
        if output == workplace.resolve() or not output.is_relative_to(workplace.resolve()):
            raise ValueError("驗收產物必須位於 workplace 的專用子目錄")
        if output.exists():
            raise ValueError("驗收目錄已存在，請指定新目錄以保留先前收據")
        for path in (args.command, args.state_compare, args.state, args.font):
            if not path.is_file():
                raise ValueError(f"缺少本機輸入：{path}")
        output.mkdir(parents=True)
        result = run_case(args.command, args.state_compare, args.state, args.font, output, args.until,
                          args.bios_key_at, args.expect == "visible", lang=args.lang)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
