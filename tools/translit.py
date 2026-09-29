#!/usr/bin/env python3
"""英文姓名音譯資料工具（規格 037）。

子命令：
  table  從中文維基「Wikipedia:外語譯音表/英語」wikitext 轉錄人名表，輸出 text/translit-table.tsv
  chars  由譯音表、附註用字與專案詞典產生字型 catalog text/translit-chars.zh-TW.tsv
  lint   檢查 text/translit-names.tsv 的格式與用字都在允許字集內

只用 Python 標準庫。簡轉繁使用內建對照表 S2T；每個轉換都列在表中，未列入的簡體字
由 `table` 的 opencc 交叉檢查（有安裝 opencc 時）或人工審查攔下。
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEXT = ROOT / "text"
DEFAULT_SRC = ROOT / "workplace" / "translit-src" / "wiki-english.wikitext"

TABLE_HEADER = ["vowel_row", "consonant", "zh", "zh_female", "zh_initial", "note"]
NAMES_HEADER = ["english", "gender", "chinese", "basis"]
CATALOG_HEADER = ["key", "translation", "source"]
CATALOG_SOURCE = "translit-table"

STANDALONE_ROW = "單獨輔音"
NO_CONSONANT = "無輔音"

# 頁面「說明」段落的附註用字：th 在輔音前或詞尾譯「思」；女名「西」音作「茜」。
# 它們不在表格內，但規格 037 §3.3 規則 8、10 會輸出，所以固定進允許字集。
RULE_CHARS = "思茜"

# 人名表內出現的簡體字 → 繁體（逐字核對 OpenCC s2t 的結果後固定於此）。
S2T = {
    "贝": "貝",
    "盖": "蓋",
    "凯": "凱",
    "韦": "韋",
    "费": "費",
    "泽": "澤",
    "谢": "謝",
    "杰": "傑",
    "内": "內",
    "莱": "萊",
}

NAME_BASIS = {"reviewed", "wikidata-cc0"}
NAME_GENDER = {"", "M", "F"}
NAME_RE = re.compile(r"^[A-Z][A-Z'\-]*[A-Z]$")


class TranslitError(Exception):
    pass


# ---------------------------------------------------------------- wikitext

def split_cells(line: str) -> list[str]:
    """以深度 0 的 `||` 切儲存格；模板內的 `|` 不影響。"""
    cells: list[str] = []
    depth = 0
    start = 0
    i = 0
    while i < len(line):
        if line.startswith("{{", i):
            depth += 1
            i += 2
            continue
        if line.startswith("}}", i):
            depth -= 1
            i += 2
            continue
        if depth == 0 and line.startswith("||", i):
            cells.append(line[start:i])
            i += 2
            start = i
            continue
        i += 1
    cells.append(line[start:])
    if depth != 0:
        raise TranslitError(f"模板括號不平衡：{line[:60]}")
    return cells


TEMPLATE_UNWRAP = ("IPA", "Nowrap", "nowrap", "no2")


def _find_template(text: str, name: str) -> tuple[int, int, str] | None:
    """回傳第一個 {{name|...}} 的 (起, 迄, 內容)，內容可含巢狀模板。"""
    m = re.search(r"\{\{" + re.escape(name) + r"\|", text)
    if not m:
        return None
    depth = 1
    i = m.end()
    while i < len(text):
        if text.startswith("{{", i):
            depth += 1
            i += 2
            continue
        if text.startswith("}}", i):
            depth -= 1
            if depth == 0:
                return m.start(), i + 2, text[m.end():i]
            i += 2
            continue
        i += 1
    raise TranslitError(f"模板未閉合：{text[:60]}")


@dataclass
class Cell:
    zh: str = ""
    variant: str = ""
    notes: list[str] = field(default_factory=list)
    rowspan: int = 1


def parse_content(raw: str) -> Cell:
    cell = Cell()
    text = raw.strip()
    m = re.match(r'^rowspan="(\d+)"\s*\|?', text)
    if m:
        cell.rowspan = int(m.group(1))
        text = text[m.end():]
    for m in re.finditer(r"\{\{efn(?:-lr)?\|name=([^}|]+)\}\}", text):
        if m.group(1) not in cell.notes:
            cell.notes.append(m.group(1))
    text = re.sub(r"\{\{efn(?:-lr)?\|name=[^}|]+\}\}", "", text)
    found = _find_template(text, "换行夹注")
    if found:
        s, e, inner = found
        cell.variant = inner.strip()
        text = text[:s] + text[e:]
        if _find_template(text, "换行夹注"):
            raise TranslitError(f"一格有兩個夾注：{raw}")
    changed = True
    while changed:
        changed = False
        for name in TEMPLATE_UNWRAP:
            found = _find_template(text, name)
            if found:
                s, e, inner = found
                text = text[:s] + inner + text[e:]
                changed = True
    text = text.replace("&ZeroWidthSpace;", "")
    text = re.sub(r"<br\s*/?>", " ", text)
    if "{{" in text or "}}" in text or "|" in text:
        raise TranslitError(f"無法解析的儲存格：{raw}")
    cell.zh = " ".join(text.split())
    return cell


def to_traditional(text: str) -> str:
    return "".join(S2T.get(ch, ch) for ch in text)


def person_table_lines(wikitext: str) -> list[str]:
    start = wikitext.find("== 人名 ==")
    if start < 0:
        raise TranslitError("找不到「== 人名 ==」段落")
    end = wikitext.find("\n|}", start)
    if end < 0:
        raise TranslitError("人名表未閉合")
    return wikitext[start:end].splitlines()


@dataclass
class TableRow:
    vowel_row: str
    consonant: str
    zh: str
    zh_female: str
    zh_initial: str
    note: str


def parse_person_table(wikitext: str, ncols: int = 26) -> list[TableRow]:
    lines = person_table_lines(wikitext)
    columns: list[str] | None = None
    col_notes: list[list[str]] = []
    data_lines: list[str] = []
    for line in lines:
        if columns is None and line.startswith("! ||"):
            heads = split_cells(line[1:])
            columns = []
            for h in heads:
                c = parse_content(h)
                columns.append(c.zh or NO_CONSONANT)
                col_notes.append(c.notes)
        elif line.startswith("| {{rh}}|"):
            data_lines.append(line[2:])
    if columns is None:
        raise TranslitError("找不到輔音標頭列")
    if len(columns) != ncols:
        raise TranslitError(f"輔音欄數應為 {ncols}，實得 {len(columns)}")

    pending: dict[int, tuple[int, Cell]] = {}
    out: list[TableRow] = []
    for line in data_lines:
        raw = split_cells(line)
        if not raw[0].startswith("{{rh}}|") or not raw[-1].strip().startswith("{{rh}}|"):
            raise TranslitError(f"列首尾不是列標頭：{line[:60]}")
        head = parse_content(raw[0][len("{{rh}}|"):])
        vowel = head.zh or STANDALONE_ROW
        given = [parse_content(c) for c in raw[1:-1]]
        cells: list[Cell] = []
        it = iter(given)
        for col in range(ncols):
            if col in pending:
                left, cell = pending[col]
                cells.append(cell)
                if left <= 1:
                    del pending[col]
                else:
                    pending[col] = (left - 1, cell)
                continue
            try:
                cell = next(it)
            except StopIteration as exc:
                raise TranslitError(f"{vowel} 列儲存格不足") from exc
            if cell.rowspan > 1:
                pending[col] = (cell.rowspan - 1, cell)
            cells.append(cell)
        rest = list(it)
        if rest:
            raise TranslitError(f"{vowel} 列多出 {len(rest)} 格")
        for col, cell in enumerate(cells):
            if not cell.zh:
                if cell.variant:
                    raise TranslitError(f"{vowel}/{columns[col]} 只有夾注沒有本字")
                continue
            notes = list(cell.notes)
            for n in head.notes + col_notes[col]:
                if n not in notes:
                    notes.append(n)
            female = initial = ""
            if cell.variant:
                if "female" in cell.notes:
                    female = cell.variant
                elif "pre" in cell.notes:
                    initial = cell.variant
                else:
                    raise TranslitError(f"{vowel}/{columns[col]} 夾注沒有對應註腳")
            out.append(
                TableRow(
                    vowel_row=vowel,
                    consonant=columns[col],
                    zh=to_traditional(cell.zh),
                    zh_female=to_traditional(female),
                    zh_initial=to_traditional(initial),
                    note=",".join(notes),
                )
            )
    if pending:
        raise TranslitError("表格結束時仍有未消化的 rowspan")
    for row in out:
        for text in (row.zh, row.zh_female, row.zh_initial):
            if " " in text:
                raise TranslitError(f"{row.vowel_row}/{row.consonant} 一格多個用字：{text}")
    return out


def table_tsv(rows: list[TableRow]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, delimiter="\t", lineterminator="\n")
    w.writerow(TABLE_HEADER)
    for r in rows:
        w.writerow([r.vowel_row, r.consonant, r.zh, r.zh_female, r.zh_initial, r.note])
    return buf.getvalue()


def read_table(path: Path) -> list[TableRow]:
    rows = list(csv.reader(io.StringIO(path.read_text("utf-8")), delimiter="\t", strict=True))
    if not rows or rows[0] != TABLE_HEADER:
        raise TranslitError(f"{path}: 標頭必須為 {'/'.join(TABLE_HEADER)}")
    out = []
    for n, r in enumerate(rows[1:], start=2):
        if len(r) != len(TABLE_HEADER):
            raise TranslitError(f"{path}:{n}: 欄數錯誤")
        out.append(TableRow(*r))
    return out


# ---------------------------------------------------------------- names

@dataclass
class NameEntry:
    english: str
    gender: str
    chinese: str
    basis: str


def read_names(path: Path) -> list[NameEntry]:
    text = path.read_text("utf-8")
    rows = list(csv.reader(io.StringIO(text), delimiter="\t", strict=True))
    if not rows or rows[0] != NAMES_HEADER:
        raise TranslitError(f"{path}: 標頭必須為 {'/'.join(NAMES_HEADER)}")
    out: list[NameEntry] = []
    seen: set[tuple[str, str]] = set()
    for n, r in enumerate(rows[1:], start=2):
        if len(r) != len(NAMES_HEADER):
            raise TranslitError(f"{path}:{n}: 必須恰有 {len(NAMES_HEADER)} 欄")
        e = NameEntry(*r)
        if not NAME_RE.match(e.english):
            raise TranslitError(f"{path}:{n}: english 必須是大寫 A–Z（可含 ' -），至少兩字母：{e.english}")
        if e.gender not in NAME_GENDER:
            raise TranslitError(f"{path}:{n}: gender 只能是 M、F 或空白")
        if (e.english, e.gender) in seen:
            raise TranslitError(f"{path}:{n}: 重複條目 {e.english}/{e.gender}")
        seen.add((e.english, e.gender))
        if e.basis not in NAME_BASIS:
            raise TranslitError(f"{path}:{n}: basis 不在白名單：{e.basis}")
        if not e.chinese or unicodedata.normalize("NFC", e.chinese) != e.chinese:
            raise TranslitError(f"{path}:{n}: chinese 不得為空且須 NFC")
        out.append(e)
    return out


def table_chars(rows: list[TableRow]) -> set[str]:
    chars: set[str] = set()
    for r in rows:
        chars.update(r.zh + r.zh_female + r.zh_initial)
    chars.update(RULE_CHARS)
    return chars


def lint_names(names: list[NameEntry], allowed: set[str]) -> list[str]:
    errors = []
    for e in names:
        bad = sorted({ch for ch in e.chinese if ch not in allowed and ch != "•"})
        if bad:
            errors.append(f"{e.english}: 不在允許字集的字 {''.join(bad)}")
    return errors


def chars_catalog(chars: set[str]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, delimiter="\t", lineterminator="\n")
    w.writerow(CATALOG_HEADER)
    for ch in sorted(chars):
        w.writerow([f"translit.char.U+{ord(ch):04X}", ch, CATALOG_SOURCE])
    return buf.getvalue()


# ---------------------------------------------------------------- CLI

def cmd_table(args: argparse.Namespace) -> int:
    rows = parse_person_table(Path(args.src).read_text("utf-8"))
    out = table_tsv(rows)
    target = Path(args.text) / "translit-table.tsv"
    if args.check:
        current = target.read_text("utf-8")
        if current != out:
            print(f"{target}: 與 {args.src} 重新轉錄的結果不一致", file=sys.stderr)
            return 1
        print(f"{target}: 與來源一致（{len(rows)} 格）")
        return 0
    target.write_text(out, "utf-8")
    print(f"寫入 {target}：{len(rows)} 格，{len(table_chars(rows)) - len(RULE_CHARS)} 個表內用字")
    return 0


def _allowed(text_dir: Path) -> tuple[set[str], list[NameEntry]]:
    rows = read_table(text_dir / "translit-table.tsv")
    names = read_names(text_dir / "translit-names.tsv")
    return table_chars(rows), names


def cmd_chars(args: argparse.Namespace) -> int:
    text_dir = Path(args.text)
    allowed, names = _allowed(text_dir)
    for e in names:
        allowed.update(ch for ch in e.chinese if ch != "•")
    out = chars_catalog(allowed)
    target = text_dir / "translit-chars.zh-TW.tsv"
    if args.check:
        if target.read_text("utf-8") != out:
            print(f"{target}: 過期，請重跑 chars", file=sys.stderr)
            return 1
        print(f"{target}: 最新（{len(allowed)} 字）")
        return 0
    target.write_text(out, "utf-8")
    print(f"寫入 {target}：{len(allowed)} 字")
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    text_dir = Path(args.text)
    allowed, names = _allowed(text_dir)
    catalog = text_dir / "translit-chars.zh-TW.tsv"
    if catalog.exists():
        rows = list(csv.reader(io.StringIO(catalog.read_text("utf-8")), delimiter="\t"))
        allowed |= {r[1] for r in rows[1:]}
    errors = lint_names(names, allowed)
    for e in errors:
        print(e, file=sys.stderr)
    if errors:
        print("新增字請先重跑 chars 並重建字型", file=sys.stderr)
        return 1
    print(f"translit-names.tsv：{len(names)} 條，用字全在允許字集")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--text", default=str(DEFAULT_TEXT), help="text/ 目錄")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("table", help="轉錄人名表")
    t.add_argument("--src", default=str(DEFAULT_SRC), help="wikitext 路徑")
    t.add_argument("--check", action="store_true", help="只比對，不寫檔")
    c = sub.add_parser("chars", help="產生字型 catalog")
    c.add_argument("--check", action="store_true", help="只比對，不寫檔")
    sub.add_parser("lint", help="檢查專案詞典")
    args = p.parse_args(argv)
    try:
        return {"table": cmd_table, "chars": cmd_chars, "lint": cmd_lint}[args.cmd](args)
    except (TranslitError, OSError) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
