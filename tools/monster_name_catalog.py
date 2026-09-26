#!/usr/bin/env python3
"""由 MON0CHA.DAX 抽出怪物名（規格 029 空位字典），輸出不含原文的 catalog。

每筆 263 位元組的怪物記錄開頭是 Pascal 字串名稱（長度 ≤ 15）。
"""
import argparse, hashlib, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ecl_text_catalog import dax_blocks  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--orig', required=True, type=Path)
    ap.add_argument('--events', required=True, type=Path)
    ap.add_argument('--source', required=True, type=Path)
    a = ap.parse_args()
    names = {}
    for bid, b in dax_blocks((a.orig / 'MON0CHA.DAX').read_bytes()):
        n = b[0]
        if len(b) != 263 or not 0 < n <= 15:
            sys.exit(f'block {bid} 格式不符')
        names.setdefault(b[1:1 + n].decode('ascii'), bid)
    ev, src = ['event_key\toriginal_length\toriginal_sha256'], ['key\toriginal']
    for t in sorted(names):
        h = hashlib.sha256(t.encode('ascii')).hexdigest()
        ev.append(f'monster.{h[:12]}\t{len(t)}\t{h}')
        src.append(f'monster.{h[:12]}\t{t}')
    a.events.write_text('\n'.join(ev) + '\n', encoding='utf-8')
    a.source.write_text('\n'.join(src) + '\n', encoding='utf-8')
    print(f'{len(names)} names', file=sys.stderr)


if __name__ == '__main__':
    main()
