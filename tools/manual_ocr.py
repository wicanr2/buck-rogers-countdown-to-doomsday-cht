#!/usr/bin/env python3
"""以 RapidOCR 建立本機掃描搜尋線索；輸出不是語意配對證據。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, nargs="+")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    engine = RapidOCR()
    pages = []
    for path in args.input:
        result, elapsed = engine(str(path))
        lines = []
        for box, text, score in result or []:
            lines.append({"box": box, "text": text, "score": score})
        pages.append({"file": path.name, "elapsed": elapsed, "lines": lines})

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"schema": 1, "engine": "rapidocr-onnxruntime 1.4.4", "pages": pages},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
