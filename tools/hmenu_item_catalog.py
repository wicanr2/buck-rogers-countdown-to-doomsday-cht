#!/usr/bin/env python3
"""由原版 GAME.OVR、START.EXE 與 ECL*.DAX 抽出水平選單項目候選（規格 028）。

選單在執行期由逐項字串組成，項目範圍只在執行期知道；這裡收集可能的項目：
可執行檔內的短 Pascal 字串（整串與逐字），以及 ECL 的短字串。
輸出不含原文的 events 與 ignored 工作區的 key→原文對照。
"""
import argparse, hashlib, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ecl_text_catalog import dax_blocks, decode6  # noqa: E402

TOKEN = re.compile(r"^[A-Za-z][A-Za-z'\-]*[A-Za-z]?[.?!]?$|^[0-9]+$")
ITEM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 '\-.,?!/]*$")


def pascal_strings(data):
    for i in range(len(data) - 2):
        n = data[i]
        if 2 <= n <= 40 and i + 1 + n <= len(data):
            s = data[i + 1:i + 1 + n]
            if all(32 <= c < 127 for c in s):
                yield s.decode('ascii')


def items_from(text):
    t = text.strip()
    if not t or len(t) > 40 or not ITEM.match(t) or not any(c.isalpha() for c in t):
        return []
    out = [t]
    toks = t.split()
    if len(toks) > 1 and all(TOKEN.match(x) for x in toks):
        out += toks
    return [x for x in out if len(x) >= 2 or x.isalnum()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--orig', required=True, type=Path)
    ap.add_argument('--events', required=True, type=Path)
    ap.add_argument('--source', required=True, type=Path)
    a = ap.parse_args()
    found = {}
    for name in ('GAME.OVR', 'START.EXE'):
        for s in pascal_strings((a.orig / name).read_bytes()):
            if re.search(r'[a-z]', s) and ' ' in s or re.fullmatch(r'[A-Z][a-z]+ ?', s):
                for it in items_from(s):
                    found.setdefault(it, name)
    for n in range(1, 7):
        for bid, blk in dax_blocks((a.orig / f'ECL{n}.DAX').read_bytes()):
            for i in range(len(blk) - 2):
                if blk[i] == 0x80 and 1 <= blk[i + 1] <= 30 and i + 2 + blk[i + 1] <= len(blk):
                    t = decode6(blk[i + 2:i + 2 + blk[i + 1]]).strip()
                    if re.fullmatch(r"[A-Z][A-Z '\-]*[A-Z]", t) and len(t) <= 30:
                        for it in items_from(t):
                            found.setdefault(it, f'ECL{n}')
    ev = ['event_key\toriginal_length\toriginal_sha256']
    src = ['key\toriginal\tfrom']
    seen = set()
    for t, where in sorted(found.items()):
        h = hashlib.sha256(t.encode('ascii')).hexdigest()
        key = f'hmenu.{h[:12]}'
        if key in seen:
            sys.exit('key 碰撞')
        seen.add(key)
        ev.append(f'{key}\t{len(t)}\t{h}')
        src.append(f'{key}\t{t}\t{where}')
    a.events.write_text('\n'.join(ev) + '\n', encoding='utf-8')
    a.source.write_text('\n'.join(src) + '\n', encoding='utf-8')
    print(f'{len(ev) - 1} items', file=sys.stderr)


if __name__ == '__main__':
    main()
