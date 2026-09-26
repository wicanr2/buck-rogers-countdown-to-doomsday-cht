#!/usr/bin/env python3
"""合併手札意譯（規格 030）為 text/logbook.zh-TW.tsv，並以與執行期相同的排版檢查頁數。

排版規則同 dosgolem apps/buckrogers/ecl_text.go 的 layoutEclText：每字一格、
拉丁字母數字（含 . ' -）連續不拆、收尾標點黏在前一個 token；段落以兩個字元 `\\n` 分隔。
"""
import argparse, csv, sys, unicodedata
from pathlib import Path

COLS, ROWS, MAX_PAGES = 36, 19, 3
CLOSING = set('，。！？：；、」）……》』,.!?:;)')


def is_latin(c):
    return ord(c) < 0x80 and (c.isalnum() or c in ".'-")


def wrap(text):
    toks, i = [], 0
    while i < len(text):
        j = i + 1
        if is_latin(text[i]):
            while j < len(text) and is_latin(text[j]):
                j += 1
        while j < len(text) and text[j] in CLOSING:
            j += 1
        toks.append(text[i:j])
        i = j
    lines, cur = [], ''
    for t in toks:
        if len(cur) + len(t) > COLS and cur:
            lines.append(cur.rstrip(' '))
            cur = t.lstrip(' ') if t.startswith(' ') else t
        else:
            cur += t
        if len(t) > COLS:
            raise ValueError('token 超寬')
    if cur:
        lines.append(cur)
    return lines


def pages(body):
    lines = []
    for para in body.split('\\n'):
        para = para.strip()
        if para:
            lines += wrap(para)
    return (len(lines) + ROWS - 1) // ROWS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--done', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    got, errors = {}, []
    for f in sorted(a.done.glob('logbook-*.tsv')):
        rows = list(csv.reader(f.open(encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
        if rows[0] != ['entry', 'title', 'translation']:
            errors.append(f'{f.name}：表頭不符')
            continue
        for r in rows[1:]:
            if len(r) != 3:
                errors.append(f'{f.name}：欄數 {r[:1]}')
                continue
            n = int(r[0])
            if n in got:
                errors.append(f'第 {n} 則重複')
            got[n] = (r[1], r[2])
    for n in range(1, 72):
        if n not in got:
            errors.append(f'缺第 {n} 則')
            continue
        title, body = got[n]
        for label, t in (('標題', title), ('正文', body)):
            try:
                t.encode('big5')
            except UnicodeEncodeError as e:
                errors.append(f'第 {n} 則{label}非 Big5：{t[e.start:e.end]!r}')
            if t != t.strip(' ') or '　' in t or unicodedata.normalize('NFC', t) != t or not t:
                errors.append(f'第 {n} 則{label}有空白、全形空白、非 NFC 或為空')
        try:
            p = pages(body)
        except ValueError as e:
            errors.append(f'第 {n} 則：{e}')
            continue
        if p > MAX_PAGES:
            errors.append(f'第 {n} 則排版 {p} 頁，超過 {MAX_PAGES}')
    for e in errors:
        print(e, file=sys.stderr)
    if errors:
        sys.exit(1)
    out = ['key\ttranslation\tsource']
    for n in range(1, 72):
        title, body = got[n]
        out.append(f'logbook.{n}\t{body}\tecl-batch-editorial')
        out.append(f'logbook.{n}.title\t{title}\tecl-batch-editorial')
    a.out.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'71 則，最多 {max(pages(got[n][1]) for n in got)} 頁', file=sys.stderr)


if __name__ == '__main__':
    main()
