#!/usr/bin/env python3
"""規格 039 §3.4「欄名列」白名單 text/header-columns.tsv 的載入檢查與原版核對。

載入檢查（與 dosgolem apps/buckrogers/header_columns.go 一致）：
- 欄位 family、key、cols、evidence；family 為 menu 或 dispatcher；dispatcher 鍵不帶 .uc。
- cols 為非負整數、嚴格遞增。
- 譯文以 U+0020 切成 token，數目等於 cols 項數；不得有空 token（連續、前導、結尾空白）。
- 非最後一欄：token 單位 + 1 ≤ 2·(cols[i+1] − cols[i])；最後一欄：2·cols[末] + token 單位 ≤ 原文長度×2。
- key 須同時存在於 events 檔（原文長度取自此）與譯文 catalog。

原版核對（本機 workplace/ 有原文或證據畫面時；唯讀）：
- dispatcher：從 workplace/engine-l10n/fragments.tsv 取原文，驗 SHA-256 等於 events，
  以空白切分重算各欄名起點並與 cols 比對；evidence 的 trace 列另驗該步的字串雜湊與列欄。
- menu：evidence 的 screen 項（原版 baseline RGBA）重算資料欄起點（相對事件欄）並與 cols 比對。
- 原文或證據缺席時輸出「跳過原版驗證」，不視為失敗。

輸出只含 key、數字與結論，不輸出英文原文。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from halfwidth import half_units  # noqa: E402

HEADER = ["family", "key", "cols", "evidence"]
FAMILIES = ("menu", "dispatcher")

# 與 dosgolem live_menu_load.go 的 liveMenuSources 相同（events → 譯文）。
MENU_SOURCES = [
    ("menu-events.tsv", "menu.zh-TW.tsv"),
    ("gender-events.tsv", "gender.zh-TW.tsv"),
    ("class-events.tsv", "class.zh-TW.tsv"),
    ("save-roster-join-runtime-events.tsv", "save-roster-join.zh-TW.tsv"),
    ("character-sheet-events.tsv", "character-sheet.zh-TW.tsv"),
    ("name-prompt-events.tsv", "name-prompt.zh-TW.tsv"),
    ("career-skill-screen-events.tsv", "career-skill-screen.zh-TW.tsv"),
    ("technical-skill-screen-events.tsv", "technical-skill-screen.zh-TW.tsv"),
]
ENGINE_EVENTS = "engine-fragment-events.tsv"
ENGINE_TEXT = "engine-fragment.zh-TW.tsv"
SKIP = "跳過原版驗證"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t", quoting=csv.QUOTE_NONE))


def load_list(path: Path) -> list[dict]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path.name}: 不接受 BOM")
    lines = data.decode("utf-8").splitlines()
    if not lines or lines[0].split("\t") != HEADER:
        raise ValueError(f"{path.name}: 標頭不符")
    rows, seen = [], set()
    for number, line in enumerate(lines[1:], start=2):
        fields = line.split("\t")
        if len(fields) != len(HEADER) or any(f == "" for f in fields):
            raise ValueError(f"{path.name}:{number}: 欄數或空欄")
        family, key, cols_text, evidence = fields
        if family not in FAMILIES:
            raise ValueError(f"{path.name}:{number}: family 無效")
        if family == "dispatcher" and key.endswith(".uc"):
            raise ValueError(f"{key}: 須寫去掉 .uc 的片段鍵")
        if (family, key) in seen:
            raise ValueError(f"{key}: 重複鍵")
        seen.add((family, key))
        try:
            cols = [int(c) for c in cols_text.split(",")]
        except ValueError:
            raise ValueError(f"{key}: cols 無效") from None
        if any(c < 0 or c > 39 for c in cols) or any(b <= a for a, b in zip(cols, cols[1:])):
            raise ValueError(f"{key}: cols 必須為非負且嚴格遞增")
        rows.append({"family": family, "key": key, "cols": cols, "evidence": evidence})
    if not rows:
        raise ValueError(f"{path.name}: 名單不得為空")
    return rows


def anchor_columns(zh: str, cols: list[int], total: int) -> list[int]:
    """回傳各欄起畫單位；不成立時丟 ValueError（規格 039 §3.4 欄名列第 1–3 條）。"""
    tokens = zh.split(" ")
    if len(tokens) != len(cols):
        raise ValueError(f"欄名 {len(tokens)} 個，cols {len(cols)} 項")
    starts = []
    for i, token in enumerate(tokens):
        if token == "":
            raise ValueError("欄名有空 token（連續、前導或結尾空白）")
        start, units = 2 * cols[i], half_units(token)
        if i + 1 < len(cols):
            if units + 1 > 2 * (cols[i + 1] - cols[i]):
                raise ValueError(f"第 {i} 欄 {units} 單位，與下一欄之間不足 1 單位")
        elif start + units > total:
            raise ValueError(f"末欄止於 {start + units} 單位，超過 {total}")
        starts.append(start)
    return starts


def menu_identities(text_dir: Path, key: str) -> list[tuple[int, str, int, int]]:
    """(原文長度, 譯文, 事件列, 事件欄)。"""
    out = []
    for events_name, text_name in MENU_SOURCES:
        events = [r for r in read_tsv(text_dir / events_name) if r["event_key"] == key]
        if not events:
            continue
        texts = {r["key"]: r["translation"] for r in read_tsv(text_dir / text_name)}
        for event in events:
            zh = texts.get(event["text_key"])
            if not zh:
                raise ValueError(f"{key}: 譯文 catalog 缺 {event['text_key']}")
            out.append((int(event["original_length"]), zh, int(event["row"]), int(event["column"])))
    return out


def engine_identities(text_dir: Path, key: str) -> list[tuple[str, int, str]]:
    """(事件鍵, 原文長度, SHA-256)，含 .uc 變體。"""
    return [(r["event_key"], int(r["original_length"]), r["original_sha256"])
            for r in read_tsv(text_dir / ENGINE_EVENTS) if r["event_key"] in (key, key + ".uc")]


def check_load(text_dir: Path, rows: list[dict]) -> None:
    engine_text = {r["key"]: r["translation"] for r in read_tsv(text_dir / ENGINE_TEXT)}
    for row in rows:
        key, cols = row["key"], row["cols"]
        if row["family"] == "menu":
            ids = menu_identities(text_dir, key)
            if not ids:
                raise ValueError(f"{key}: 不在選單 events")
            for length, zh, _, _ in ids:
                try:
                    anchor_columns(zh, cols, 2 * length)
                except ValueError as error:
                    raise ValueError(f"{key}: {error}") from None
        else:
            ids = engine_identities(text_dir, key)
            if not any(k == key for k, _, _ in ids):
                raise ValueError(f"{key}: 不在引擎片段 events")
            zh = engine_text.get(key)
            if not zh:
                raise ValueError(f"{key}: 不在引擎片段譯文")
            for event_key, length, _ in ids:
                try:
                    anchor_columns(zh, cols, 2 * length)
                except ValueError as error:
                    raise ValueError(f"{event_key}: {error}") from None


def token_starts(original: str) -> list[int]:
    return [i for i, c in enumerate(original) if c != " " and (i == 0 or original[i - 1] == " ")]


def evidence_items(evidence: str) -> list[tuple[str, str]]:
    out = []
    for item in evidence.split(";"):
        name, _, value = item.partition("=")
        out.append((name, value))
    return out


def screen_data_starts(path: Path, scale: int, rows: list[int], column: int, length: int) -> list[int]:
    """原版畫面在 rows 各列、[column, column+length) 內有墨跡的格取聯集，回傳各連續段的起點（相對 column）。"""
    data = path.read_bytes()
    width = 320 * scale
    if len(data) != width * 200 * scale * 4:
        raise ValueError(f"{path.name}: RGBA 大小不符 {scale}×")
    ink = set()
    for row in rows:
        for cell in range(column, column + length):
            colours = set()
            for y in range(row * 8 * scale, (row + 1) * 8 * scale):
                base = (y * width + cell * 8 * scale) * 4
                for x in range(8 * scale):
                    colours.add(data[base + 4 * x: base + 4 * x + 3])
            if len(colours) > 1:
                ink.add(cell - column)
    return [c for c in sorted(ink) if c - 1 not in ink]


def verify_original(text_dir: Path, workplace: Path, rows: list[dict]) -> list[str]:
    report = []
    table_path = workplace / "engine-l10n" / "fragments.tsv"
    table = None
    if table_path.is_file():
        table = {r["key"]: r["original"] for r in read_tsv(table_path)}
    for row in rows:
        key, cols = row["key"], row["cols"]
        if row["family"] == "dispatcher":
            if table is None or key not in table:
                report.append(f"{key}: {SKIP}（原文表缺席）")
                continue
            original = table[key]
            ids = {k: (n, sha) for k, n, sha in engine_identities(text_dir, key)}
            n, sha = ids[key]
            if len(original) != n or hashlib.sha256(original.encode("latin-1")).hexdigest() != sha:
                raise ValueError(f"{key}: 原文表與 events 的長度／SHA 不符")
            starts = token_starts(original)
            if starts != cols:
                raise ValueError(f"{key}: 原文欄名起點 {starts} 與 cols {cols} 不符")
            report.append(f"{key}: 原文欄名起點 {starts} = cols")
            for name, value in evidence_items(row["evidence"]):
                if name != "trace":
                    continue
                path_text, _, step = value.rpartition(":")
                trace = workplace / path_text
                if not trace.is_file():
                    report.append(f"{key}: trace {SKIP}（檔案缺席）")
                    continue
                hit = None
                for line in trace.read_text(encoding="latin-1").splitlines():
                    f = line.split("\t")
                    if len(f) >= 8 and f[0] == "D" and f[1] == step:
                        hit = f
                        break
                if hit is None:
                    raise ValueError(f"{key}: trace 沒有步 {step}")
                text = "\t".join(hit[7:])
                if hashlib.sha256(text.encode("latin-1")).hexdigest() not in {s for _, s in ids.values()}:
                    raise ValueError(f"{key}: trace 步 {step} 的字串雜湊不符")
                report.append(f"{key}: trace 步 {step} 列 {hit[5]} 欄 {hit[6]}，字串雜湊相符")
        else:
            ids = menu_identities(text_dir, key)
            screens = [v for n, v in evidence_items(row["evidence"]) if n == "screen"]
            if not screens:
                report.append(f"{key}: {SKIP}（evidence 無畫面）")
            for value in screens:
                path_text, scale, span = value.rsplit(":", 2)
                path = workplace / path_text
                if not path.is_file():
                    report.append(f"{key}: {path_text} {SKIP}（證據畫面缺席）")
                    continue
                rows_used = []
                for part in span.split(","):
                    first, _, last = part.partition("-")
                    rows_used.extend(range(int(first), int(last or first) + 1))
                for length, _, _, column in ids:
                    starts = screen_data_starts(path, int(scale), rows_used, column, length)
                    if starts != cols:
                        raise ValueError(f"{key}: {path_text} 資料欄起點 {starts} 與 cols {cols} 不符")
                    report.append(f"{key}: {path_text} 列 {span} 資料欄起點 "
                                  f"{[column + c for c in starts]}（相對 {starts}）= cols")
    return report


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--text", type=Path, default=root / "text")
    parser.add_argument("--workplace", type=Path, default=root / "workplace")
    args = parser.parse_args(argv)
    rows = load_list(args.text / "header-columns.tsv")
    check_load(args.text, rows)
    print(f"載入檢查：{len(rows)} 列通過")
    for line in verify_original(args.text, args.workplace, rows):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
