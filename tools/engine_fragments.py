#!/usr/bin/env python3
"""規格 029：引擎片段 catalog 與參考分解器。

片段 = GAME.OVR、START.EXE 內可列印、含兩個以上連續英文字母的 Pascal 字串（長度 1–80），
另加規格 029 §2.1 明列的短片段（EXPLICIT，逐條附檔案位移，不產生全大寫變體）。
decompose() 是 Go 實作（apps/buckrogers/engine_text.go）的參考版本，兩者要對同一批
測試向量給出相同 signature。
"""
import argparse, hashlib, re, sys
from pathlib import Path


# 規格 029 §2.1（2026-09-27 修訂）：明列短片段 -> (檔名, 長度位元組的檔案位移)。
EXPLICIT = {"'s": ('GAME.OVR', 187675)}


def fragments(orig, with_pos=False):
    out = {}
    for name in ('GAME.OVR', 'START.EXE'):
        d = (orig / name).read_bytes()
        for i in range(len(d) - 1):
            n = d[i]
            if 1 <= n <= 80 and i + 1 + n <= len(d):
                s = d[i + 1:i + 1 + n]
                if all(32 <= c < 127 for c in s) and re.search(rb'[A-Za-z]{2}', s):
                    out.setdefault(s.decode('ascii'), f'{name}:{i}')
    for t, (name, i) in EXPLICIT.items():
        d = (orig / name).read_bytes()
        if d[i] != len(t) or d[i + 1:i + 1 + len(t)] != t.encode('ascii'):
            sys.exit(f'明列片段 {t!r} 不在 {name}:{i}')
        out.setdefault(t, f'{name}:{i}')
    return out if with_pos else set(out)


def key_of(text, prefix):
    return f'{prefix}.{hashlib.sha256(text.encode("ascii")).hexdigest()[:12]}'


def is_alpha(c):
    return ('A' <= c <= 'Z') or ('a' <= c <= 'z')


def boundary(s, p):
    return p == 0 or p == len(s) or not (is_alpha(s[p - 1]) and is_alpha(s[p]))


def all_caps(t):
    return not re.search(r'[a-z]', t)


def item_runs(s, words):
    """回傳物品空位 [(i, j)]：最長連串，單位間恰一個空白。"""
    units = sorted(words, key=len, reverse=True)
    runs, p = [], 0
    while p < len(s):
        if not boundary(s, p):
            p += 1
            continue
        q, n = p, 0
        while True:
            hit = next((u for u in units if s.startswith(u, q) and boundary(s, q + len(u))), None)
            if not hit:
                break
            q += len(hit)
            n += 1
            if s.startswith(' ', q) and q + 1 < len(s) and any(s.startswith(u, q + 1) and boundary(s, q + 1 + len(u)) for u in units):
                q += 1
                continue
            break
        if n >= 2 or (n == 1 and re.match(r' \(\d', s[q:])):
            runs.append((p, q))
            p = q
        else:
            p += 1
    return runs


def decompose(s, frags, words):
    """回傳 [(kind, text)]，kind 為 'F'、'_'、'I'。"""
    if s in frags:
        return [('F', s)]
    parts, last = [], 0
    for i, j in item_runs(s, words):
        parts.append(('T', s[last:i]))
        parts.append(('I', s[i:j]))
        last = j
    parts.append(('T', s[last:]))
    out = []
    for kind, t in parts:
        if kind == 'I':
            out.append(('I', t))
        elif t:
            out.extend(_segment(t, frags))
    merged = []
    for kind, t in out:
        if kind == '_' and merged and merged[-1][0] == '_':
            merged[-1] = ('_', merged[-1][1] + t)
        else:
            merged.append((kind, t))
    return merged


def _segment(s, frags):
    n = len(s)
    best = [None] * (n + 1)
    best[0] = (0, 0, None)  # (-covered, pieces, back)
    for i in range(n):
        if best[i] is None:
            continue
        for j in range(i + 1, n + 1):
            t = s[i:j]
            isf = t in frags and len(t) >= 3 and not all_caps(t) and boundary(s, i) and boundary(s, j)
            cov = best[i][0] - (len(t) if isf else 0)
            cand = (cov, best[i][1] + 1, (i, isf))
            if best[j] is None or cand[:2] < best[j][:2]:
                best[j] = cand
    out, j = [], n
    while j > 0:
        i, isf = best[j][2]
        out.append(('F' if isf else '_', s[i:j]))
        j = i
    out.reverse()
    return out


def signature(parts, fkey):
    return '|'.join(fkey[t] if k == 'F' else k for k, t in parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--orig', required=True, type=Path)
    ap.add_argument('--events', required=True, type=Path)
    ap.add_argument('--source', required=True, type=Path)
    a = ap.parse_args()
    pos = fragments(a.orig, with_pos=True)
    frags = sorted(pos)
    ev = ['event_key\toriginal_length\toriginal_sha256']
    src = ['key\toriginal\tfirst_seen']
    seen, seen_upper = set(), set()
    for t in frags:
        k = key_of(t, 'frag')
        if k in seen:
            sys.exit('key 碰撞')
        seen.add(k)
        ev.append(f'{k}\t{len(t)}\t{hashlib.sha256(t.encode("ascii")).hexdigest()}')
        src.append(f'{k}\t{t}\t{pos[t]}')
        # 遊戲部分畫面把片段轉成全大寫顯示；全大寫變體共用同一譯文（key 加 .uc）。
        u = t.upper()
        if t not in EXPLICIT and u != t and u not in pos and u not in seen_upper:
            seen_upper.add(u)
            ev.append(f'{k}.uc\t{len(u)}\t{hashlib.sha256(u.encode("ascii")).hexdigest()}')
    a.events.write_text('\n'.join(ev) + '\n', encoding='utf-8')
    a.source.write_text('\n'.join(src) + '\n', encoding='utf-8')
    print(f'{len(frags)} fragments', file=sys.stderr)


if __name__ == '__main__':
    main()
