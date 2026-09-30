#!/usr/bin/env python3
"""規格 043 §3.7：韓文允許字集 font/charset.ko.txt 的產生與核對。

定義：可見 ASCII（U+0020–U+007E）∪ 現代韓文音節（U+AC00–U+D7A3，Unifont 需有 16 寬（16x16）字模）∪ 「」『』（U+300C–U+300F，16 寬）
∪ 明列的 8 寬置中箭頭 {U+2190、U+2192}。檔案格式：UTF-8 單行，字元依碼位遞增串接，結尾換行。

  python3 tools/ko_charset.py --font <unifont_all-17.0.05.hex.gz> --out font/charset.ko.txt
  python3 tools/ko_charset.py --font <hex> --check        重生後與 font/charset.ko.txt 逐位元組比對
"""
from __future__ import annotations

import argparse
import gzip
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARSET = ROOT / "font" / "charset.ko.txt"
HANGUL = range(0xAC00, 0xD7A4)
BRACKETS = (0x300C, 0x300D, 0x300E, 0x300F)
EXTRA_HALF_WIDTH = (0x2190, 0x2192)


def glyph_widths(path: Path) -> dict[int, int]:
    """碼位 → 字模十六進位字元數（64＝16 寬、32＝8 寬）。"""
    opener = gzip.open if path.suffix == ".gz" else open
    widths: dict[int, int] = {}
    with opener(path, "rt", encoding="ascii", newline="") as stream:
        for line in stream:
            code, _, bitmap = line.rstrip("\r\n").partition(":")
            if not bitmap:
                continue
            try:
                widths[int(code, 16)] = len(bitmap)
            except ValueError:
                continue
    return widths


def build(font: Path) -> str:
    widths = glyph_widths(font)
    bad = [c for c in (*HANGUL, *BRACKETS) if widths.get(c) != 64]
    if bad:
        raise SystemExit(f"Unifont 缺 16 寬字模：{len(bad)} 個，例 U+{bad[0]:04X}")
    missing = [c for c in EXTRA_HALF_WIDTH if c not in widths]
    if missing:
        raise SystemExit(f"Unifont 缺字模：{[hex(c) for c in missing]}")
    points = set(range(0x20, 0x7F)) | set(HANGUL) | set(BRACKETS) | set(EXTRA_HALF_WIDTH)
    return "".join(chr(c) for c in sorted(points)) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--font", required=True, type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    text = build(args.font)
    if args.check:
        if not CHARSET.exists() or CHARSET.read_text(encoding="utf-8") != text:
            print("font/charset.ko.txt 與重生結果不同", file=sys.stderr)
            return 1
        print(f"ko_charset OK（{len(text) - 1} 字）")
        return 0
    if args.out is None:
        p.error("需要 --out 或 --check")
    args.out.write_text(text, encoding="utf-8")
    print(f"寫出 {args.out}（{len(text) - 1} 字）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
