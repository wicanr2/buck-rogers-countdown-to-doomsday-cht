#!/usr/bin/env python3
"""驗證批次譯文並合併為 text/ecl-text.zh-TW.tsv。

每個 done/batch-NN.tsv 必須與 batches/batch-NN.tsv 的 key 集合、順序完全相同；
譯文須為單行、NFC、Big5 可編碼、非空。`-` 表示該列是雜訊，不進正式檔。
正式檔只收 catalog（text/ecl-text-events.tsv）內的 key。已存在正式檔的譯文，
除非批次檔有新值，否則保留。
"""
import argparse, csv, sys, unicodedata
from pathlib import Path

SOURCE = 'ecl-batch-editorial'


def read_tsv(path, header):
    rows = list(csv.reader(path.open(encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
    if not rows or rows[0][:len(header)] != header:
        raise SystemExit(f'{path}: 表頭應為 {header}')
    return rows[1:]


def check(text, where):
    errs = []
    if not text:
        errs.append('空白')
    if any(c in text for c in '\t\r\n'):
        errs.append('含 tab／換行')
    if unicodedata.normalize('NFC', text) != text:
        errs.append('非 NFC')
    if any(unicodedata.category(c) == 'Cc' for c in text):
        errs.append('控制字元')
    try:
        text.encode('big5')
    except UnicodeEncodeError as e:
        errs.append(f'非 Big5：{text[e.start:e.end]!r}')
    return [f'{where}：{e}' for e in errs]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--events', required=True, type=Path)
    ap.add_argument('--batches', required=True, type=Path)
    ap.add_argument('--done', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--exclude', type=Path, help='不進正式檔的 key（規格 027 §4）')
    ap.add_argument('--check-only', action='store_true')
    a = ap.parse_args()
    catalog = {r[0] for r in read_tsv(a.events, ['event_key', 'original_length', 'original_sha256', 'sources'])}
    excluded = set()
    if a.exclude:
        excluded = {r[0] for r in read_tsv(a.exclude, ['key', 'reason'])}
    merged = {}
    if a.out.exists():
        for k, t, s in read_tsv(a.out, ['key', 'translation', 'source']):
            merged[k] = (t, s)
    errors, garbage, done_batches = [], 0, 0
    for done in sorted(a.done.glob('batch-[0-9][0-9].tsv')):
        src = a.batches / done.name
        want = [r[0] for r in read_tsv(src, ['key', 'original'])]
        got = read_tsv(done, ['key', 'translation'])
        if [r[0] for r in got] != want:
            errors.append(f'{done.name}：key 集合或順序與輸入不同（{len(got)}／{len(want)}）')
            continue
        done_batches += 1
        for k, t in ((r[0], r[1] if len(r) > 1 else '') for r in got):
            if t == '-':
                garbage += 1
                merged.pop(k, None)
                continue
            if k in excluded:
                merged.pop(k, None)
                continue
            if k not in catalog:
                errors.append(f'{done.name}：{k} 不在 catalog')
                continue
            e = check(t, f'{done.name}:{k}')
            if e:
                errors.extend(e)
                continue
            merged[k] = (t, SOURCE)
    for e in errors:
        print(e, file=sys.stderr)
    print(f'批次 {done_batches}，譯文 {len(merged)}，雜訊 {garbage}，錯誤 {len(errors)}', file=sys.stderr)
    if errors:
        sys.exit(1)
    if not a.check_only:
        lines = ['key\ttranslation\tsource'] + [f'{k}\t{t}\t{s}' for k, (t, s) in sorted(merged.items())]
        a.out.write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
