#!/usr/bin/env python3
"""驗證水平選單項目批次譯文並合併為 text/hmenu.zh-TW.tsv（規格 028）。"""
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ecl_translation_merge import read_tsv, check  # noqa: E402

SOURCE = 'ecl-batch-editorial'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--events', required=True, type=Path)
    ap.add_argument('--batches', required=True, type=Path)
    ap.add_argument('--done', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    catalog = {r[0] for r in read_tsv(a.events, ['event_key', 'original_length', 'original_sha256'])}
    merged, errors, noise = {}, [], 0
    for done in sorted(a.done.glob('batch-[0-9][0-9].tsv')):
        want = [r[0] for r in read_tsv(a.batches / done.name, ['key', 'original', 'from'])]
        got = read_tsv(done, ['key', 'translation'])
        if [r[0] for r in got] != want:
            errors.append(f'{done.name}：key 集合或順序不同')
            continue
        for r in got:
            k, t = r[0], (r[1] if len(r) > 1 else '')
            if t == '-':
                noise += 1
                continue
            if k not in catalog:
                errors.append(f'{done.name}：{k} 不在 catalog')
                continue
            e = check(t, f'{done.name}:{k}')
            if e:
                errors.extend(e)
                continue
            merged[k] = t
    for e in errors:
        print(e, file=sys.stderr)
    print(f'譯文 {len(merged)}，雜訊 {noise}，錯誤 {len(errors)}', file=sys.stderr)
    if errors:
        sys.exit(1)
    a.out.write_text('\n'.join(['key\ttranslation\tsource'] + [f'{k}\t{t}\t{SOURCE}' for k, t in sorted(merged.items())]) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
