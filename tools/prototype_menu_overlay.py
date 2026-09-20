#!/usr/bin/env python3
"""以 GNU Unifont 在 dosgolem 原始色號畫面上製作可丟棄的整數縮放覆繪。"""

import argparse
import gzip
import struct
import zlib


def png(path, width, height, rgb):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    rows = b"".join(b"\0" + rgb[y * width * 3:(y + 1) * width * 3] for y in range(height))
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


def load_unifont(path, wanted):
    glyphs = {}
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="ascii") as f:
        for line in f:
            cp, bits = line.strip().split(":", 1)
            ch = chr(int(cp, 16))
            if ch in wanted:
                raw = bytes.fromhex(bits)
                width = 8 if len(raw) == 16 else 16
                glyphs[ch] = (width, raw)
    missing = sorted(wanted - glyphs.keys())
    if missing:
        raise SystemExit("Unifont 缺字：" + "".join(missing))
    return glyphs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--vram", required=True)
    p.add_argument("--palette", required=True)
    p.add_argument("--font", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--scale", type=int, choices=(2, 3), required=True)
    p.add_argument("--text", default="建立新角色")
    args = p.parse_args()
    vram = open(args.vram, "rb").read()
    pal = open(args.palette, "rb").read()
    if len(vram) != 64000 or len(pal) < 48:
        raise SystemExit("預期 320x200 色號與至少 16 色 RGB 調色盤")
    # dosgolem 的 DAC 值為 0..63；轉為 0..255。
    colors = [tuple(min(255, pal[i * 3 + j] * 4) for j in range(3)) for i in range(len(pal) // 3)]
    scale = args.scale
    w, h = 320 * scale, 200 * scale
    out = bytearray(w * h * 3)
    for y in range(200):
        for x in range(320):
            c = colors[vram[y * 320 + x]]
            for yy in range(y * scale, (y + 1) * scale):
                for xx in range(x * scale, (x + 1) * scale):
                    q = (yy * w + xx) * 3
                    out[q:q + 3] = bytes(c)
    glyphs = load_unifont(args.font, set(args.text))
    # 已證實原文矩形：column 9、row 12、20 個 8x8 格。
    x0, y0, cells = 9 * 8 * scale, 12 * 8 * scale, 20
    bg, fg = colors[0], colors[10]
    for y in range(y0, y0 + 8 * scale):
        for x in range(x0, x0 + cells * 8 * scale):
            q = (y * w + x) * 3
            out[q:q + 3] = bytes(bg)
    # scale=2：16x16 填滿一格；scale=3：16x16 置中於 24x24 格。
    ox = 0 if scale == 2 else 4
    oy = 0 if scale == 2 else 4
    for i, ch in enumerate(args.text):
        gw, bits = glyphs[ch]
        gx = x0 + i * 8 * scale + ox + (16 - gw) // 2
        gy = y0 + oy
        rowbytes = gw // 8
        for yy in range(16):
            for xx in range(gw):
                if bits[yy * rowbytes + xx // 8] & (0x80 >> (xx & 7)):
                    q = ((gy + yy) * w + gx + xx) * 3
                    out[q:q + 3] = bytes(fg)
    png(args.out, w, h, out)


if __name__ == "__main__":
    main()
