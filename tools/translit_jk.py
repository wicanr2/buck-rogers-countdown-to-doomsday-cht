#!/usr/bin/env python3
"""日文、韓文玩家名音譯資料工具（規格 044、045）。

子命令：
  chars  --lang ja|ko [--check]   由規則的允許字集與專案詞典產生 text/translit-chars.<lang>.tsv
                                  （--check 只比對版控檔，不寫檔）
  lint   --lang ja|ko             檢查 text/translit-<lang>-names.tsv 的格式、集合與用字
  verify-fixed --lang ja|ko       檢查固定名單與規則回歸表的欄位、review 欄與 dosgolem testdata 副本雜湊；
                                  含 pending 的列使它失敗
  examples --check --lang ja|ko   檢查規格例子表的欄位、規則編號、kind 與用字，與 testdata 副本雜湊

只用 Python 標準庫。固定名單與例子表由 dosgolem 的測試產生候選與逐列比對（規格 044 §5：
TestFixedNames、TestSpecExamples，規則模式需要 Go），這裡只驗檔案本身與副本是否互鎖。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEXT = ROOT / "text"
DEFAULT_DOCS = ROOT / "docs" / "re"
DEFAULT_DOSGOLEM = ROOT / "workplace" / "dosgolem"
PHASE = "phase-308"
FIXED_HEADER = ["name", "expected", "tier", "rules", "review"]
REGRESSION_HEADER = ["name", "expected", "tier", "rules"]
EXAMPLES_HEADER = ["name", "expected", "rule", "kind"]
TIERS = {"dict", "cmudict", "spelling", "none"}
REVIEW_OK = re.compile(r"^ok:([^,\s:]+),([^,\s:]+)$")
RULE_ID = {"ja": re.compile(r"^J[1-9]([.][A-Za-z0-9.]+)?$"), "ko": re.compile(r"^K([1-9]|10)([.][A-Za-z0-9.]+)?$")}
NAME_CHARS = re.compile(r"^[A-Za-z' -]+$")
KINDS = {"rule", "idiom"}
CATALOG_HEADER = ["key", "translation", "source"]
NAMES_HEADER = ["english", "translation", "basis"]
CATALOG_SOURCE = "translit-table"
BASIS = {"machine-reviewed", "reviewed"}
# 規格 044 §3.5：詞典 english 集合 = translit-names.tsv 的名字加補充名。
SUPPLEMENT = {"PIERRE"}


class JkError(Exception):
    pass


def ja_base() -> set[str]:
    return {chr(c) for c in range(0x30A1, 0x30F7)} | {"ー", "・"}


# 規格 045 §3.3：頭子音 14 × 中聲 19 × 尾 8。
KO_ONSET = [0, 2, 3, 5, 6, 7, 9, 11, 12, 14, 15, 16, 17, 18]  # ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ
KO_NUCLEUS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20]  # 19 個，不含 ㅚ ㅢ
KO_CODA = [0, 1, 4, 8, 16, 17, 19, 21]  # 無 ㄱ ㄴ ㄹ ㅁ ㅂ ㅅ ㅇ


def ko_base() -> set[str]:
    return {chr(0xAC00 + (o * 21 + n) * 28 + c) for o in KO_ONSET for n in KO_NUCLEUS for c in KO_CODA}


def read_tsv(path: Path, header: list[str]) -> list[list[str]]:
    if not path.exists():
        raise JkError(f"缺檔：{path}")
    text = path.read_text(encoding="utf-8")
    if text.startswith("﻿"):
        raise JkError(f"{path.name}：不接受 BOM")
    rows = list(csv.reader(text.splitlines(), delimiter="\t", quoting=csv.QUOTE_NONE))
    if not rows or rows[0] != header:
        raise JkError(f"{path.name}：標頭必須為 {'/'.join(header)}")
    for i, r in enumerate(rows[1:], 2):
        if len(r) != len(header):
            raise JkError(f"{path.name}:{i}：欄數 {len(r)}，應為 {len(header)}")
    return rows[1:]


def dict_path(text: Path, lang: str) -> Path:
    return text / f"translit-{lang}-names.tsv"


def dict_chars(text: Path, lang: str) -> set[str]:
    rows = read_tsv(dict_path(text, lang), NAMES_HEADER)
    return {ch for r in rows for ch in r[1] if ch not in " -"}


def allowed(text: Path, lang: str) -> set[str]:
    base = ja_base() if lang == "ja" else ko_base()
    return base | dict_chars(text, lang)


def catalog_bytes(chars: set[str]) -> bytes:
    lines = ["\t".join(CATALOG_HEADER)]
    for ch in sorted(chars):
        lines.append(f"translit.char.U+{ord(ch):04X}\t{ch}\t{CATALOG_SOURCE}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def cmd_chars(text: Path, lang: str, check: bool) -> int:
    want = catalog_bytes(allowed(text, lang))
    path = text / f"translit-chars.{lang}.tsv"
    if check:
        if not path.exists() or path.read_bytes() != want:
            print(f"translit_jk chars --check：{path.name} 與規則字集不符（重新產生：tools/translit_jk.py chars --lang {lang}）", file=sys.stderr)
            return 1
        print(f"translit_jk chars --check OK（{lang}，{want.count(b'translit.char.')} 字）")
        return 0
    path.write_bytes(want)
    print(f"translit_jk chars：寫出 {path.name}（{want.count(b'translit.char.')} 字）")
    return 0


def cmd_lint(text: Path, lang: str, font: Path | None = None) -> int:
    errors: list[str] = []
    base_chars = ja_base() if lang == "ja" else ko_base()
    rows = read_tsv(dict_path(text, lang), NAMES_HEADER)
    zh = {r[0] for r in read_tsv(text / "translit-names.tsv", ["english", "gender", "chinese", "basis"])}
    want = zh | SUPPLEMENT
    seen: set[str] = set()
    font = font or ROOT / "font"
    charset = set((font / f"charset.{lang}.txt").read_text(encoding="utf-8")) if (font / f"charset.{lang}.txt").exists() else None
    for i, (en, tr, basis) in enumerate(rows, 2):
        if en in seen:
            errors.append(f"第 {i} 列：english {en} 重複")
        seen.add(en)
        if basis not in BASIS:
            errors.append(f"第 {i} 列：basis {basis!r} 不在 {sorted(BASIS)}")
        if tr != unicodedata.normalize("NFC", tr) or not tr:
            errors.append(f"第 {i} 列：translation 空或不是 NFC")
        if lang == "ja" and (" " in tr or "-" in tr):
            errors.append(f"第 {i} 列：ja 的 translation 不得含空白或連字號")
        if lang == "ko" and ("-" in tr or tr != tr.strip() or "  " in tr):
            errors.append(f"第 {i} 列：ko 的 translation 首尾與連續空白、連字號都不行")
        for ch in tr:
            if ch == " ":
                continue
            # 規則字集之外的字只有在字型字集（charset.<lang>.txt）有它時才算允許字集的成員（規格 044 §3.5）
            if ch not in base_chars and not (charset is not None and ch in charset):
                errors.append(f"第 {i} 列：{en} 的字 U+{ord(ch):04X} 不在允許字集內")
            if charset is not None and ch not in charset:
                errors.append(f"第 {i} 列：{en} 的字 U+{ord(ch):04X} 不在字型字集 charset.{lang}.txt 內")
    if seen != want:
        miss, extra = sorted(want - seen), sorted(seen - want)
        if miss:
            errors.append(f"缺 english：{', '.join(miss[:10])}（共 {len(miss)}）")
        if extra:
            errors.append(f"多 english：{', '.join(extra[:10])}（共 {len(extra)}）")
    if errors:
        for e in errors[:50]:
            print(f"translit_jk lint {lang}：{e}", file=sys.stderr)
        print(f"translit_jk lint {lang}：{len(errors)} 項失敗", file=sys.stderr)
        return 1
    print(f"translit_jk lint OK（{lang}，{len(rows)} 列）")
    return 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def doc_path(docs: Path, kind: str, lang: str) -> Path:
    return docs / f"{PHASE}-{kind}.{lang}.tsv"


# Buck repo 的檔 -> dosgolem xlate/translitjk/testdata 的逐字副本（TestFixedNamesAgainstBuck 也檢查同一組）
def copy_pairs(text: Path, docs: Path, dosgolem: Path, lang: str, kinds: tuple[str, ...]) -> list[tuple[Path, Path]]:
    td = dosgolem / "xlate" / "translitjk" / "testdata"
    names = {"translit-fixed-names": "fixed-names", "translit-rule-regression": "rule-regression", "spec-examples": "spec-examples"}
    pairs = [(doc_path(docs, k, lang), td / f"{names[k]}.{lang}.tsv") for k in kinds]
    if "translit-fixed-names" in kinds:
        pairs += [
            (text / f"translit-{lang}-names.tsv", td / "text" / f"translit-{lang}-names.tsv"),
            (text / f"translit-chars.{lang}.tsv", td / "text" / f"translit-chars.{lang}.tsv"),
            (text / "cmudict" / "LICENSE", td / "text" / "cmudict" / "LICENSE"),
        ]
    return pairs


def check_copies(pairs: list[tuple[Path, Path]], dosgolem: Path, errors: list[str]) -> str:
    if not (dosgolem / "xlate" / "translitjk" / "testdata").is_dir():
        return f"略過副本雜湊（沒有 {dosgolem}/xlate/translitjk/testdata；Go 測試 TestFixedNamesAgainstBuck 另行檢查）"
    for src, dst in pairs:
        if not src.exists():
            errors.append(f"缺 {src}")
        elif not dst.exists():
            errors.append(f"dosgolem 缺副本 {dst.relative_to(dosgolem)}")
        elif sha256(src) != sha256(dst):
            errors.append(f"副本雜湊不符：{src.name} 與 dosgolem {dst.relative_to(dosgolem)}")
    return f"副本雜湊 {len(pairs)} 個比對"


def report(tag: str, errors: list[str], ok_msg: str) -> int:
    if errors:
        for e in errors[:50]:
            print(f"{tag}：{e}", file=sys.stderr)
        print(f"{tag}：{len(errors)} 項失敗", file=sys.stderr)
        return 1
    print(f"{tag} OK（{ok_msg}）")
    return 0


def cmd_verify_fixed(text: Path, docs: Path, dosgolem: Path, lang: str) -> int:
    errors: list[str] = []
    ok_chars = allowed(text, lang) | {" ", "-"}
    rows = read_tsv(doc_path(docs, "translit-fixed-names", lang), FIXED_HEADER)
    names: set[str] = set()
    pending = 0
    for i, (name, expected, tier, rules, review) in enumerate(rows, 2):
        if name in names:
            errors.append(f"固定名單第 {i} 列：name {name!r} 重複")
        names.add(name)
        if tier not in TIERS:
            errors.append(f"固定名單第 {i} 列：tier {tier!r} 不在 {sorted(TIERS)}")
        if (expected == "") != (tier == "none"):
            errors.append(f"固定名單第 {i} 列：expected 為空與 tier=none 必須一致")
        if expected != unicodedata.normalize("NFC", expected):
            errors.append(f"固定名單第 {i} 列：expected 不是 NFC")
        for ch in expected:
            if ch not in ok_chars:
                errors.append(f"固定名單第 {i} 列：{name!r} 的字 U+{ord(ch):04X} 不在允許字集內")
        for r in filter(None, rules.split(",")):
            if not RULE_ID[lang].match(r):
                errors.append(f"固定名單第 {i} 列：規則編號 {r!r} 格式不符")
        if review == "pending":
            pending += 1
        else:
            m = REVIEW_OK.match(review)
            if not m:
                errors.append(f"固定名單第 {i} 列：review {review!r} 必須是 pending 或 ok:<審查者1>,<審查者2>")
            elif m.group(1) == m.group(2):
                errors.append(f"固定名單第 {i} 列：兩位審查者必須是不同的人（{m.group(1)}）")
    if pending:
        errors.append(f"固定名單有 {pending} 列 review 仍是 pending")
    if len(rows) < 50:
        errors.append(f"固定名單只有 {len(rows)} 列")
    # 規則回歸表：詞典的每個名字恰一列，規則模式的輸出
    reg = read_tsv(doc_path(docs, "translit-rule-regression", lang), REGRESSION_HEADER)
    reg_names = [r[0] for r in reg]
    dict_names = [r[0] for r in read_tsv(dict_path(text, lang), NAMES_HEADER)]
    if sorted(reg_names) != sorted(dict_names):
        errors.append("規則回歸表的 name 集合與專案詞典的 english 集合不同")
    for i, (name, expected, tier, rules) in enumerate(reg, 2):
        if tier not in TIERS - {"dict"}:
            errors.append(f"規則回歸表第 {i} 列：規則模式的 tier 不得是 {tier!r}")
        if (expected == "") != (tier == "none"):
            errors.append(f"規則回歸表第 {i} 列：expected 為空與 tier=none 必須一致")
        for ch in expected:
            if ch not in ok_chars:
                errors.append(f"規則回歸表第 {i} 列：{name!r} 的字 U+{ord(ch):04X} 不在允許字集內")
    note = check_copies(copy_pairs(text, docs, dosgolem, lang, ("translit-fixed-names", "translit-rule-regression")), dosgolem, errors)
    return report(f"translit_jk verify-fixed {lang}", errors, f"固定名單 {len(rows)} 列、規則回歸表 {len(reg)} 列；{note}")


def cmd_examples(text: Path, docs: Path, dosgolem: Path, lang: str) -> int:
    errors: list[str] = []
    ok_chars = allowed(text, lang) | {" ", "-"}
    rows = read_tsv(doc_path(docs, "spec-examples", lang), EXAMPLES_HEADER)
    seen: set[tuple[str, str, str]] = set()
    for i, (name, expected, rule, kind) in enumerate(rows, 2):
        if not NAME_CHARS.match(name):
            errors.append(f"第 {i} 列：name {name!r} 只能含英文字母、撇號、連字號與空白")
        if not expected or expected != unicodedata.normalize("NFC", expected):
            errors.append(f"第 {i} 列：expected 空或不是 NFC")
        for ch in expected:
            if ch not in ok_chars:
                errors.append(f"第 {i} 列：{name!r} 的字 U+{ord(ch):04X} 不在允許字集內")
        if not RULE_ID[lang].match(rule.removeprefix("!")):
            errors.append(f"第 {i} 列：規則編號 {rule!r} 格式不符（{lang}）")
        if kind not in KINDS:
            errors.append(f"第 {i} 列：kind {kind!r} 不在 {sorted(KINDS)}")
        key = (name, rule, kind)
        if key in seen:
            errors.append(f"第 {i} 列：{name!r}／{rule}／{kind} 重複")
        seen.add(key)
    note = check_copies(copy_pairs(text, docs, dosgolem, lang, ("spec-examples",)), dosgolem, errors)
    return report(f"translit_jk examples --check {lang}", errors, f"{len(rows)} 列；{note}；逐列比對規則模式輸出由 dosgolem TestSpecExamples 執行")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--text", type=Path, default=DEFAULT_TEXT)
    ap.add_argument("--docs", type=Path, default=DEFAULT_DOCS, help="docs/re（固定名單與例子表所在）")
    ap.add_argument("--dosgolem", type=Path, default=DEFAULT_DOSGOLEM, help="dosgolem 工作樹（testdata 副本互鎖；沒有就略過）")
    ap.add_argument("--font", type=Path, default=None, help="font/（lint 對 charset.<lang>.txt）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("chars")
    c.add_argument("--lang", required=True, choices=["ja", "ko"])
    c.add_argument("--check", action="store_true")
    l = sub.add_parser("lint")
    l.add_argument("--lang", required=True, choices=["ja", "ko"])
    v = sub.add_parser("verify-fixed")
    v.add_argument("--lang", required=True, choices=["ja", "ko"])
    e = sub.add_parser("examples")
    e.add_argument("--lang", required=True, choices=["ja", "ko"])
    e.add_argument("--check", action="store_true", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "chars":
            return cmd_chars(args.text, args.lang, args.check)
        if args.cmd == "verify-fixed":
            return cmd_verify_fixed(args.text, args.docs, args.dosgolem, args.lang)
        if args.cmd == "examples":
            return cmd_examples(args.text, args.docs, args.dosgolem, args.lang)
        return cmd_lint(args.text, args.lang, args.font)
    except JkError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
