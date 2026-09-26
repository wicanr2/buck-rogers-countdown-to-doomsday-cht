#!/usr/bin/env python3
"""由執行期記憶體傾印抽出物品名單字表（規格 029、phase-260），輸出不含原文的 catalog。

START.EXE 的資料段是壓縮的，單字表只能從執行期取得：以
`cmd/buckrogers-glyph-text -mem-out` 在任一遊戲中狀態傾印 1MB 記憶體，
表在線性 0x108E2 起，每筆 21 位元組（Pascal string[20]），54 筆。
表內容的 SHA-256 固定，傾印來自別的版本或位置時直接失敗。
"""
import argparse, hashlib, sys
from pathlib import Path

BASE, WIDTH, COUNT = 0x108E2, 21, 54
TABLE_SHA256 = '1ea4440a4a4f85be6fdd1fbb6a3355f00c321303818f47daf2104d9ce4dec0cb'


def read_table(mem):
    table = mem[BASE:BASE + WIDTH * COUNT]
    words = []
    for i in range(COUNT):
        rec = table[i * WIDTH:(i + 1) * WIDTH]
        n = rec[0]
        if n > 20 or any(rec[1 + n:]):
            sys.exit(f'第 {i} 筆格式不符')
        words.append(rec[1:1 + n].decode('ascii'))
    return table, words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mem', required=True, type=Path)
    ap.add_argument('--events', type=Path)
    ap.add_argument('--source', type=Path)
    ap.add_argument('--print-sha', action='store_true')
    a = ap.parse_args()
    table, words = read_table(a.mem.read_bytes())
    sha = hashlib.sha256(table).hexdigest()
    if a.print_sha:
        print(sha)
        return
    if TABLE_SHA256 and sha != TABLE_SHA256:
        sys.exit(f'單字表雜湊不符：{sha}')
    ev, src, seen = ['event_key\toriginal_length\toriginal_sha256'], ['key\toriginal'], set()
    for w in words:
        if w in seen:
            continue
        seen.add(w)
        h = hashlib.sha256(w.encode('ascii')).hexdigest()
        ev.append(f'item.{h[:12]}\t{len(w)}\t{h}')
        src.append(f'item.{h[:12]}\t{w}')
        u = w.upper()
        if u != w and u not in words:
            hu = hashlib.sha256(u.encode('ascii')).hexdigest()
            ev.append(f'item.{h[:12]}.uc\t{len(u)}\t{hu}')
    a.events.write_text('\n'.join(ev) + '\n', encoding='utf-8')
    a.source.write_text('\n'.join(src) + '\n', encoding='utf-8')
    print(f'{len(ev) - 1} words', file=sys.stderr)


if __name__ == '__main__':
    main()
