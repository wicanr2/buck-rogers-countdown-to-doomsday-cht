#!/usr/bin/env python3
"""規格 034：由本機英文手冊快照產生手冊查詢題的英文摘錄（只在 ignored workplace）。

答案只在本行程記憶體內解碼、只用來核對；不寫檔、不印出、不進例外訊息。
失敗只回報 event_key。輸出檔等同答案表，只能寫到 workplace/manual-english/。
"""
import argparse
import hashlib
import html
import re
import sys
from pathlib import Path

TOOL_VERSION = "034.1"
SNAPSHOT_SHA256 = "e8528a31b66d76e7162abe358bff1f27d7d5a5d4070914beee470867e59e728a"  # phase-112
DUMP_SHA256 = "28a0563b647ebe75a70e19648502e3fb9dc9379ada35bd397d99b104a4ce7c60"  # 0EC0:0000（phase-12）
RECORD_SIZE = 0x1E
BLOCK_TAGS = re.compile(r"<\s*/?\s*(p|br|div|h[1-6]|li|tr)\b[^>]*>", re.I)
EDGE_PUNCT = ".,;:!?\"()"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def snapshot_lines(raw: bytes) -> list[str]:
    """規格 034 §3.2 的純文字化程序（版本 TOOL_VERSION）。"""
    t = raw.decode("utf-8", errors="replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S | re.I)
    t = BLOCK_TAGS.sub("\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    lines = (re.sub(r"\s+", " ", line).strip() for line in t.split("\n"))
    return [line for line in lines if line]


def line_sha(line: str) -> str:
    return sha256(line.encode("utf-8"))[:16]


def read_tsv(path: Path) -> list[list[str]]:
    rows = [line.rstrip("\n").split("\t") for line in path.read_text(encoding="utf-8").splitlines()]
    return [r for r in rows[1:] if r and not r[0].startswith("#")]


def decode_field(record: bytes, length_at: int, capacity: int) -> str:
    n = record[length_at]
    if n > capacity:
        raise ValueError("長度超過容量")
    data = record[length_at + 1:length_at + 1 + n]
    return bytes((b - 6 + n) & 0xFF for b in data).decode("ascii")


def words_from(lines: list[str], line: int, word: int, count: int) -> list[str] | None:
    out: list[str] = []
    i, w = line, word
    carry = ""
    while i < len(lines) and len(out) < count:
        toks = lines[i].split(" ")[w:]
        for j, tok in enumerate(toks):
            last = j == len(toks) - 1
            if carry:
                tok, carry = carry + tok, ""
            if last and tok.endswith("-") and len(tok) > 1:
                carry = tok[:-1]
                continue
            out.append(tok)
            if len(out) == count:
                return out
        i, w = i + 1, 0
    return out if len(out) == count else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", type=Path, required=True)
    ap.add_argument("--dump", type=Path, required=True)
    ap.add_argument("--questions", type=Path, required=True)
    ap.add_argument("--events", type=Path, required=True)
    ap.add_argument("--anchors", type=Path, required=True)
    ap.add_argument("--fixes", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--start-exe", type=Path, required=True)
    ap.add_argument("--game-ovr", type=Path, required=True)
    a = ap.parse_args()
    if "workplace/manual-english" not in a.out.resolve().as_posix():
        print("錯誤：輸出只能在 workplace/manual-english/", file=sys.stderr)
        return 2
    snap = a.snapshot.read_bytes()
    dump = a.dump.read_bytes()
    if sha256(snap) != SNAPSHOT_SHA256 or sha256(dump) != DUMP_SHA256:
        print("錯誤：快照或傾印雜湊不符", file=sys.stderr)
        return 2
    lines = snapshot_lines(snap)
    events = {r[1]: r for r in read_tsv(a.events)}  # record_index -> row
    anchors = {r[0]: r for r in read_tsv(a.anchors)}
    fixes: dict[str, dict[int, str]] = {}
    if a.fixes and a.fixes.exists():
        for r in read_tsv(a.fixes):
            fixes.setdefault(r[0], {})[int(r[1])] = r[2]
    out_rows, excluded = [], []
    for q in read_tsv(a.questions):
        idx, off, page, heading, ordinal = q[0], int(q[1], 16), q[2], q[3], int(q[4])
        ev = events.get(idx)
        if ev is None:
            continue
        key = ev[0]
        rec = dump[off:off + RECORD_SIZE]
        try:
            if decode_field(rec, 0x01, 18) != heading or rec[0x14] != ordinal:
                print("錯誤：題庫解碼自我核對失敗", file=sys.stderr)
                return 2
        except (ValueError, UnicodeDecodeError):
            print("錯誤：題庫解碼自我核對失敗", file=sys.stderr)
            return 2
        an = anchors.get(key)
        if an is None:
            excluded.append((key, "no-anchor"))
            continue
        line, word, want_sha = int(an[3]), int(an[4]), an[5]
        if line >= len(lines) or line_sha(lines[line]) != want_sha:
            excluded.append((key, "anchor-sha"))
            continue
        ws = words_from(lines, line, word, ordinal)
        if ws is None:
            excluded.append((key, "short"))
            continue
        for i, w in fixes.get(key, {}).items():
            if 1 <= i <= ordinal:
                ws[i - 1] = w
        last = ws[-1].strip(EDGE_PUNCT).upper()
        try:
            ok = last == decode_field(rec, 0x15, 8).upper()
        except (ValueError, UnicodeDecodeError):
            ok = False
        if not ok or not last or not all(0x21 <= ord(c) <= 0x7E for w in ws for c in w):
            excluded.append((key, "mismatch"))
            continue
        ws[-1] = last
        out_rows.append(f"{key}\t{ordinal}\t{' '.join(ws)}")
    prov = (f"# tool={TOOL_VERSION} snapshot={sha256(snap)} dump={sha256(dump)} "
            f"start={sha256(a.start_exe.read_bytes())} game_ovr={sha256(a.game_ovr.read_bytes())} "
            f"anchors={sha256(a.anchors.read_bytes())} "
            f"fixes={sha256(a.fixes.read_bytes()) if a.fixes and a.fixes.exists() else '-'} "
            f"passed={len(out_rows)}")
    a.out.write_text(prov + "\nevent_key\tordinal\twords\n" + "".join(r + "\n" for r in out_rows), encoding="utf-8")
    print(f"通過 {len(out_rows)} 題，排除 {len(excluded)} 題")
    for key, why in excluded:
        print(f"排除\t{key}\t{why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
