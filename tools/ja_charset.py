#!/usr/bin/env python3
"""規格 042 §3.7：日文允許字集 font/charset.ja.txt 的產生與核對。

定義：ASCII（U+0020–U+007E）∪ JIS X 0208 中 Unifont 有 16 寬（16x16）字模的字元 ∪ 明列的 8 寬置中字元
{U+2014、U+2026、U+2190、U+2192}；不含全形英數（U+FF10–FF19、FF21–FF3A、FF41–FF5A）與 U+3000。
檔案格式：UTF-8 單行，字元依碼位遞增串接，結尾換行。

  python3 tools/ja_charset.py --font <unifont_all-17.0.05.hex.gz> --out font/charset.ja.txt
  python3 tools/ja_charset.py --font <hex> --check        重生後與 font/charset.ja.txt 逐位元組比對
"""
from __future__ import annotations

import argparse
import gzip
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARSET = ROOT / "font" / "charset.ja.txt"
EXTRA_HALF_WIDTH = (0x2014, 0x2026, 0x2190, 0x2192)
EXCLUDED = set(range(0xFF10, 0xFF1A)) | set(range(0xFF21, 0xFF3B)) | set(range(0xFF41, 0xFF5B)) | {0x3000}


def jis_x_0208() -> set[int]:
    out: set[int] = set()
    for row in range(0x21, 0x7F):
        for col in range(0x21, 0x7F):
            try:
                ch = bytes((row | 0x80, col | 0x80)).decode("euc_jp")
            except UnicodeDecodeError:
                continue
            if len(ch) == 1:
                out.add(ord(ch))
    return out


def wide_glyphs(path: Path) -> set[int]:
    opener = gzip.open if path.suffix == ".gz" else open
    wide: set[int] = set()
    with opener(path, "rt", encoding="ascii", newline="") as stream:
        for line in stream:
            code, _, bitmap = line.rstrip("\r\n").partition(":")
            if not bitmap:
                continue
            try:
                cp = int(code, 16)
            except ValueError:
                continue
            if len(bitmap) == 64:  # 16x16
                wide.add(cp)
    return wide


def build(font: Path) -> str:
    wide = wide_glyphs(font)
    points = {c for c in jis_x_0208() if c in wide} | set(range(0x20, 0x7F)) | set(EXTRA_HALF_WIDTH)
    points -= EXCLUDED
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
            print("font/charset.ja.txt 與重生結果不同", file=sys.stderr)
            return 1
        print(f"ja_charset OK（{len(text) - 1} 字）")
        return 0
    if args.out is None:
        p.error("需要 --out 或 --check")
    args.out.write_text(text, encoding="utf-8")
    print(f"寫出 {args.out}（{len(text) - 1} 字）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
