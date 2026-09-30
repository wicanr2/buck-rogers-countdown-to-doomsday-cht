#!/usr/bin/env python3
"""具名人物譯名表工具（規格 036 §3.1、§3.2）。

子命令：
  lint                 檢查譯名表、例外清單格式，並掃描 text/*.zh-TW.tsv 不得殘留舊譯名；
                       譯名用字須在字型字元清單內。
  apply [--dry-run]    以譯名表把 catalog 內的舊譯名收斂成正式中文，列出每筆替換
                       （檔案、key、舊、新），以及正式譯名緊接括號（執行期不加註）的位置。
  strip-logbook-notes [--dry-run]
                       移除手札譯文中緊接人名的全形「（English）」註記，只移除人名的。

譯名表欄位：english、english_mixed、chinese、kind、person、basis、note。
note 以全形分號「；」分段，其中 `old=甲|乙` 列出要收斂的舊譯名，`alias=X|Y` 列出手札
註記裡可能出現的其他英文寫法。含間隔號的正式譯名自動把「·」「．」「・」與無間隔寫法
視為舊譯名。

例外清單欄位：phrase、scope、note。phrase 為含人名字樣但不是人名的中文片語；scope 為
key 的 fnmatch 樣式（`*` 表示全部）。比對時該片語整段跳過。

只用 Python 標準庫。
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import io
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from catalog_lang import DEFAULT_LANG, KNOWN_LANGS, catalog_glob, catalog_name

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"
GLOSSARY = TEXT / "name-glossary.tsv"
EXCLUDE = TEXT / "name-glossary-exclude.tsv"
FONT_CHARS = ROOT / "font" / "characters.txt"

GLOSSARY_HEADER = ["english", "english_mixed", "chinese", "kind", "person", "basis", "note"]
EXCLUDE_HEADER = ["phrase", "scope", "note"]
CATALOG_HEADER = ["key", "translation", "source"]
KINDS = {"full", "short"}
BASIS_RE = re.compile(r"^(printed:\S.*|xinhua|nickname)$")
PERSON_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ENGLISH_RE = re.compile(r"^[A-Z0-9][A-Z0-9 .'\-]*[A-Z0-9]$")
SEPARATOR = "•"  # •
OTHER_SEPARATORS = ("·", "．", "・")  # · ． ・
# 手冊段落只做中文收斂；既有英文（例如印刷本保留的 Scot.dos）不動。
MANUAL_CATALOGS = {catalog_name("manual", lang) for lang in KNOWN_LANGS}
LOGBOOK_CATALOG = catalog_name("logbook")
APPLY_FAMILIES = ["ecl-text", "logbook", "monster-name", "hmenu", "engine-fragment", "manual"]
DEFAULT_APPLY = [catalog_name(f) for f in APPLY_FAMILIES]


def default_apply(lang: str = DEFAULT_LANG) -> list[str]:
    """規格 040：apply 的預設 catalog 依語言命名（預設 zh-TW）。"""
    return [catalog_name(f, lang) for f in APPLY_FAMILIES]
# 手札註記前可緊接的稱謂（中文）與註記內可前置的英文稱謂。
ZH_TITLES = ("博士", "醫生", "船長", "上校", "指揮官", "主任", "行政官")
EN_TITLE_RE = re.compile(
    r"^(?:(?:Captain|Capt|Commander|Colonel|Col|Security Officer|Dr|Mrs|Mr|Ms)\b\.?[\s,]*)+", re.IGNORECASE
)
NOTE_RE = re.compile(r"（([^（）]*)）")


class GlossaryError(ValueError):
    pass


@dataclass(frozen=True)
class Name:
    english: str
    english_mixed: str
    chinese: str
    kind: str
    person: str
    basis: str
    note: str
    old: tuple[str, ...] = ()
    alias: tuple[str, ...] = ()


@dataclass(frozen=True)
class Exclusion:
    phrase: str
    scope: str

    def applies(self, key: str) -> bool:
        return fnmatch.fnmatchcase(key, self.scope)


@dataclass
class Glossary:
    names: list[Name]
    exclusions: list[Exclusion] = field(default_factory=list)

    def replacements(self) -> dict[str, Name]:
        """舊譯名 → 正式譯名（含自動間隔號變體）。"""
        out: dict[str, Name] = {}
        for name in self.names:
            for old in name.old + dot_variants(name.chinese):
                if old != name.chinese:
                    out.setdefault(old, name)
        return out

    def current(self) -> dict[str, Name]:
        return {name.chinese: name for name in self.names}


# ---------------------------------------------------------------- 讀檔

def _read_tsv(path: Path, header: list[str]) -> list[list[str]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        raise GlossaryError(f"{path}: 不允許 BOM 或 CR")
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8")), delimiter="\t", quoting=csv.QUOTE_NONE, strict=True))
    if not rows or rows[0] != header:
        raise GlossaryError(f"{path}: 標頭必須精確為 {'/'.join(header)}")
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            raise GlossaryError(f"{path}:{number}: 必須恰有 {len(header)} 欄")
        for value in row:
            if unicodedata.normalize("NFC", value) != value:
                raise GlossaryError(f"{path}:{number}: 必須使用 NFC")
            if any(unicodedata.category(ch).startswith("C") for ch in value):
                raise GlossaryError(f"{path}:{number}: 含控制或格式字元")
    return rows[1:]


def _note_field(note: str, name: str) -> tuple[str, ...]:
    values: list[str] = []
    for part in note.split("；"):
        part = part.strip()
        if part.startswith(name + "="):
            values.extend(v for v in part[len(name) + 1:].split("|"))
    if any(not v for v in values):
        raise GlossaryError(f"note 的 {name}= 含空值：{note}")
    return tuple(values)


def dot_variants(chinese: str) -> tuple[str, ...]:
    if SEPARATOR not in chinese:
        return ()
    return tuple(chinese.replace(SEPARATOR, sep) for sep in OTHER_SEPARATORS + ("",))


def read_glossary(path: Path = GLOSSARY, exclude_path: Path | None = EXCLUDE) -> Glossary:
    names: list[Name] = []
    for number, row in enumerate(_read_tsv(path, GLOSSARY_HEADER), start=2):
        english, mixed, chinese, kind, person, basis, note = row
        where = f"{path}:{number}"
        if not ENGLISH_RE.match(english):
            raise GlossaryError(f"{where}: english 必須是原版全大寫：{english!r}")
        if mixed and mixed.upper() != english:
            raise GlossaryError(f"{where}: english_mixed 與 english 不是同一拼法：{mixed!r}")
        if not chinese or chinese.strip() != chinese or " " in chinese:
            raise GlossaryError(f"{where}: chinese 不得為空或含空白")
        if any(sep in chinese for sep in OTHER_SEPARATORS):
            raise GlossaryError(f"{where}: 間隔號必須是 U+2022：{chinese}")
        if kind not in KINDS:
            raise GlossaryError(f"{where}: kind 必須是 full 或 short")
        if not PERSON_RE.match(person):
            raise GlossaryError(f"{where}: person 格式不符：{person!r}")
        if not BASIS_RE.match(basis):
            raise GlossaryError(f"{where}: basis 必須是 printed:<位置>、xinhua 或 nickname")
        try:
            old = _note_field(note, "old")
            alias = _note_field(note, "alias")
        except GlossaryError as exc:
            raise GlossaryError(f"{where}: {exc}") from exc
        names.append(Name(english, mixed, chinese, kind, person, basis, note, old, alias))

    seen_en: set[str] = set()
    seen_zh: set[str] = set()
    for name in names:
        if name.english in seen_en:
            raise GlossaryError(f"{path}: english 重複：{name.english}")
        if name.chinese in seen_zh:
            raise GlossaryError(f"{path}: chinese 重複：{name.chinese}")
        seen_en.add(name.english)
        seen_zh.add(name.chinese)
    glossary = Glossary(names)
    olds: dict[str, str] = {}
    for name in names:
        for old in name.old:
            if old in seen_zh:
                raise GlossaryError(f"{path}: 舊譯名「{old}」同時是正式譯名")
            if old in olds and olds[old] != name.person:
                raise GlossaryError(f"{path}: 舊譯名「{old}」屬於兩個人物")
            olds[old] = name.person
    if exclude_path is not None and exclude_path.exists():
        glossary.exclusions = read_exclusions(exclude_path)
    return glossary


def read_exclusions(path: Path) -> list[Exclusion]:
    out: list[Exclusion] = []
    seen: set[tuple[str, str]] = set()
    for number, (phrase, scope, _note) in enumerate(_read_tsv(path, EXCLUDE_HEADER), start=2):
        if not phrase or not scope:
            raise GlossaryError(f"{path}:{number}: phrase、scope 不得為空")
        if (phrase, scope) in seen:
            raise GlossaryError(f"{path}:{number}: 重複：{phrase} {scope}")
        seen.add((phrase, scope))
        out.append(Exclusion(phrase, scope))
    return out


def read_catalog(path: Path) -> tuple[list[list[str]], str]:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    rows = list(csv.reader(io.StringIO(text), delimiter="\t", quoting=csv.QUOTE_NONE, strict=True))
    if not rows or rows[0] != CATALOG_HEADER:
        raise GlossaryError(f"{path}: 不是 key/translation/source catalog")
    return rows, text


def write_catalog(path: Path, rows: list[list[str]]) -> None:
    body = "".join("\t".join(row) + "\n" for row in rows)
    path.write_bytes(body.encode("utf-8"))


# ---------------------------------------------------------------- 比對

def _is_ascii(s: str) -> bool:
    return all(ord(c) < 0x80 for c in s)


def _ascii_alnum(c: str) -> bool:
    return ord(c) < 0x80 and c.isalnum()


@dataclass(frozen=True)
class Hit:
    start: int
    end: int
    matched: str
    name: Name
    is_old: bool


def excluded_spans(text: str, key: str, exclusions: list[Exclusion]) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    for ex in exclusions:
        if not ex.applies(key):
            continue
        for m in re.finditer(re.escape(ex.phrase), text):
            spans.append((m.start(), m.end(), ex.phrase))
    return spans


def _after_escape(text: str, i: int) -> bool:
    """TSV 以 `\\n` 表示換行；跳脫序列後的字母不算與前字相連。"""
    return i >= 2 and text[i - 2] == "\\" and text[i - 1] in "nt"


def scan(text: str, key: str, glossary: Glossary, *, skip_ascii_old: bool = False) -> tuple[list[Hit], list[tuple[int, str]]]:
    """由左至右最長優先比對正式譯名與舊譯名；回傳命中與因例外跳過的位置。"""
    candidates: dict[str, tuple[Name, bool]] = {zh: (n, False) for zh, n in glossary.current().items()}
    for old, name in glossary.replacements().items():
        if skip_ascii_old and _is_ascii(old):
            continue
        candidates.setdefault(old, (name, True))
    ordered = sorted(candidates, key=len, reverse=True)
    spans = excluded_spans(text, key, glossary.exclusions)
    hits: list[Hit] = []
    skipped: list[tuple[int, str]] = []
    i = 0
    while i < len(text):
        span = next((s for s in spans if s[0] <= i < s[1]), None)
        if span is not None:
            if span[0] == i:
                skipped.append((i, span[2]))
            i = span[1]
            continue
        for cand in ordered:
            if not text.startswith(cand, i):
                continue
            end = i + len(cand)
            if _is_ascii(cand) and (
                (i > 0 and _ascii_alnum(text[i - 1]) and not _after_escape(text, i))
                or (end < len(text) and _ascii_alnum(text[end]))
            ):
                continue
            name, is_old = candidates[cand]
            hits.append(Hit(i, end, cand, name, is_old))
            i = end
            break
        else:
            i += 1
    return hits, skipped


def converge(text: str, key: str, glossary: Glossary, *, skip_ascii_old: bool = False) -> tuple[str, list[tuple[str, str, int]], list[tuple[int, str]]]:
    hits, skipped = scan(text, key, glossary, skip_ascii_old=skip_ascii_old)
    out: list[str] = []
    changes: list[tuple[str, str, int]] = []
    pos = 0
    for hit in hits:
        if not hit.is_old:
            continue
        start, end = hit.start, hit.end
        new = hit.name.chinese
        if _is_ascii(hit.matched) and not _is_ascii(new):
            # 英文舊譯名改成中文時，吃掉它與中文之間的一個半形空白。
            if end < len(text) and text[end] == " " and end + 1 < len(text) and not _is_ascii(text[end + 1]):
                end += 1
            if start > pos and text[start - 1] == " " and start >= 2 and not _is_ascii(text[start - 2]):
                start -= 1
        out.append(text[pos:start])
        out.append(new)
        changes.append((text[start:end], new, start))
        pos = end
    out.append(text[pos:])
    return "".join(out), changes, skipped


def paren_follow(text: str, key: str, glossary: Glossary) -> list[tuple[str, str]]:
    """正式譯名後緊接 ( 或 （ 的位置（執行期不再加註）。"""
    hits, _ = scan(text, key, glossary)
    out: list[tuple[str, str]] = []
    for hit in hits:
        if not hit.is_old and hit.end < len(text) and text[hit.end] in "(（":
            close = text.find(")" if text[hit.end] == "(" else "）", hit.end)
            out.append((hit.matched, text[hit.start:(close + 1 if close >= 0 else hit.end + 1)]))
    return out


def context(text: str, start: int, end: int, width: int = 8) -> str:
    return text[max(0, start - width):end + width].replace("\t", " ")


# ---------------------------------------------------------------- 子命令

def catalog_paths(args_paths: list[str] | None, default: list[str] | None, text_dir: Path,
                  lang: str = DEFAULT_LANG) -> list[Path]:
    if args_paths:
        return [Path(p) for p in args_paths]
    if default is None:
        return sorted(text_dir.glob(catalog_glob(lang)))
    return [text_dir / name for name in default]


def load_font_chars(path: Path) -> set[str]:
    chars: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            code = line.split("\t", 1)[0]
            if code.startswith("U+"):
                chars.add(chr(int(code[2:], 16)))
    return chars


def lint(glossary: Glossary, paths: list[Path], font_chars: set[str] | None) -> list[str]:
    errors: list[str] = []
    if font_chars is not None:
        for name in glossary.names:
            missing = sorted({c for c in name.chinese if c not in font_chars})
            if missing:
                errors.append(f"字型缺字：{name.chinese} 缺 {''.join(missing)}")
    for path in paths:
        rows, _ = read_catalog(path)
        manual = path.name in MANUAL_CATALOGS
        for row in rows[1:]:
            key, text = row[0], row[1]
            hits, _ = scan(text, key, glossary, skip_ascii_old=manual)
            for hit in hits:
                if hit.is_old:
                    errors.append(
                        f"{path.name}\t{key}\t舊譯名「{hit.matched}」應為「{hit.name.chinese}」\t{context(text, hit.start, hit.end)}"
                    )
    return errors


def apply(glossary: Glossary, paths: list[Path], dry_run: bool, out) -> int:
    total = 0
    for path in paths:
        rows, _ = read_catalog(path)
        manual = path.name in MANUAL_CATALOGS
        changed = False
        for row in rows[1:]:
            key, text = row[0], row[1]
            new, changes, skipped = converge(text, key, glossary, skip_ascii_old=manual)
            for old, rep, start in changes:
                print(f"REPLACE\t{path.name}\t{key}\t{old}\t{rep}\t{context(text, start, start + len(old))}", file=out)
                total += 1
            for pos, phrase in skipped:
                print(f"EXCLUDED\t{path.name}\t{key}\t{phrase}\t{context(text, pos, pos + len(phrase))}", file=out)
            for name, ctx in paren_follow(new, key, glossary):
                print(f"PAREN\t{path.name}\t{key}\t{name}\t{ctx}", file=out)
            if new != text:
                row[1] = new
                changed = True
        if changed and not dry_run:
            write_catalog(path, rows)
    print(f"# 替換 {total} 筆{'（dry-run，未寫回）' if dry_run else ''}", file=out)
    return total


def _note_person(note: str, glossary: Glossary) -> Name | None:
    bare = EN_TITLE_RE.sub("", note.strip())
    bare = re.sub(r"\s+", " ", bare).strip().lower()
    if not bare:
        return None
    for name in glossary.names:
        forms = {name.english, name.english_mixed, *name.alias}
        if bare in {f.lower() for f in forms if f}:
            return name
    return None


def _preceding_person(text: str, end: int, glossary: Glossary) -> Name | None:
    head = text[:end]
    for title in ZH_TITLES:
        if head.endswith(title):
            head = head[: -len(title)]
            break
    forms: list[tuple[str, Name]] = [(n.chinese, n) for n in glossary.names]
    forms += [(old, n) for old, n in glossary.replacements().items()]
    forms.sort(key=lambda item: len(item[0]), reverse=True)
    for form, name in forms:
        if head.endswith(form):
            return name
    return None


def strip_notes(text: str, glossary: Glossary) -> tuple[str, list[str]]:
    removed: list[str] = []
    out: list[str] = []
    pos = 0
    for m in NOTE_RE.finditer(text):
        noted = _note_person(m.group(1), glossary)
        before = _preceding_person(text, m.start(), glossary)
        if noted is None or before is None or noted.person != before.person:
            continue
        out.append(text[pos:m.start()])
        removed.append(m.group(0))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), removed


def strip_logbook(glossary: Glossary, path: Path, dry_run: bool, out) -> int:
    rows, _ = read_catalog(path)
    total = 0
    for row in rows[1:]:
        new, removed = strip_notes(row[1], glossary)
        for note in removed:
            print(f"STRIP\t{path.name}\t{row[0]}\t{note}", file=out)
            total += 1
        row[1] = new
    if total and not dry_run:
        write_catalog(path, rows)
    print(f"# 移除註記 {total} 筆{'（dry-run，未寫回）' if dry_run else ''}", file=out)
    return total


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--glossary", type=Path, default=GLOSSARY)
    p.add_argument("--exclude", type=Path, default=EXCLUDE)
    p.add_argument("--text", type=Path, default=TEXT, help="text/ 目錄")
    p.add_argument("--lang", default=DEFAULT_LANG, choices=KNOWN_LANGS, help="譯文語言（規格 040；預設 zh-TW）")
    sub = p.add_subparsers(dest="cmd", required=True)
    lp = sub.add_parser("lint")
    lp.add_argument("catalog", nargs="*")
    lp.add_argument("--font-chars", type=Path, default=FONT_CHARS)
    lp.add_argument("--no-font", action="store_true", help="略過字型缺字檢查")
    ap = sub.add_parser("apply")
    ap.add_argument("catalog", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    sp = sub.add_parser("strip-logbook-notes")
    sp.add_argument("catalog", nargs="?")
    sp.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)
    try:
        glossary = read_glossary(args.glossary, args.exclude)
        if args.cmd == "lint":
            font = None if args.no_font else load_font_chars(args.font_chars)
            errors = lint(glossary, catalog_paths(args.catalog, None, args.text, args.lang), font)
            for e in errors:
                print(e)
            if errors:
                print(f"name-glossary lint：{len(errors)} 項錯誤", file=sys.stderr)
                return 1
            print(f"name-glossary lint OK（{len(glossary.names)} 條、例外 {len(glossary.exclusions)} 條）")
            return 0
        if args.cmd == "apply":
            apply(glossary, catalog_paths(args.catalog, default_apply(args.lang), args.text, args.lang), args.dry_run, sys.stdout)
            return 0
        if args.cmd == "strip-logbook-notes":
            path = Path(args.catalog) if args.catalog else args.text / catalog_name("logbook", args.lang)
            strip_logbook(glossary, path, args.dry_run, sys.stdout)
            return 0
    except GlossaryError as exc:
        print(exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
