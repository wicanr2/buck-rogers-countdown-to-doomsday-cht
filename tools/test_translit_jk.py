"""tools/translit_jk.py 的測試（規格 044、045）：真實資料護欄與合成負例。

  cd tools && python3 -m unittest test_translit_jk.py
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import translit_jk as tj  # noqa: E402

NAMES = "english\ttranslation\tbasis\n"
JA_DICT = {"AARON": "アーロン", "PIERRE": "ピエール"}
KO_DICT = {"AARON": "에런", "PIERRE": "피에르"}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class Tree:
    """合成的 text/、docs/re、font/、dosgolem testdata（zh 名字表只有 AARON，補充名 PIERRE）。"""

    def __init__(self, root: Path, lang: str) -> None:
        self.root, self.lang = root, lang
        self.text, self.docs, self.font, self.dg = root / "text", root / "docs" / "re", root / "font", root / "dg"
        self.dict = dict(JA_DICT if lang == "ja" else KO_DICT)
        self.basis = {k: "machine-reviewed" for k in self.dict}
        r1, r2 = ("J1.AA", "J1.IH") if lang == "ja" else ("K2.AA", "K2.IY")
        self.fixed = [(f"N{i:02d}", self.dict["AARON"], "cmudict", r1, "ok:甲,乙") for i in range(60)]
        self.regression = [("AARON", self.dict["AARON"], "cmudict", r1), ("PIERRE", self.dict["PIERRE"], "cmudict", r2)]
        self.examples = [("Kate", self.dict["AARON"], "J1.EY" if lang == "ja" else "K2.EY", "rule")]
        self.font_extra = ""
        self.with_dg = False
        self.dg_edit: dict[str, str] = {}

    def args(self, *cmd: str) -> list[str]:
        return ["--text", str(self.text), "--docs", str(self.docs), "--font", str(self.font), "--dosgolem", str(self.dg), *cmd, "--lang", self.lang]

    def flush(self) -> None:
        write(self.text / "translit-names.tsv", "english\tgender\tchinese\tbasis\nAARON\tM\t亞倫\treviewed\n")
        write(tj.dict_path(self.text, self.lang), NAMES + "".join(f"{k}\t{v}\t{self.basis[k]}\n" for k, v in self.dict.items()))
        # chars 先由規則字集（真實）與合成詞典產生，這裡只寫該語言用到的字與基底
        write(self.text / f"translit-chars.{self.lang}.tsv", tj.catalog_bytes(tj.allowed(self.text, self.lang)).decode("utf-8"))
        base = tj.ja_base() if self.lang == "ja" else tj.ko_base()
        write(self.font / f"charset.{self.lang}.txt", "".join(sorted(base | set(self.font_extra))) + "\n")
        write(tj.doc_path(self.docs, "translit-fixed-names", self.lang),
              "\t".join(tj.FIXED_HEADER) + "\n" + "".join("\t".join(r) + "\n" for r in self.fixed))
        write(tj.doc_path(self.docs, "translit-rule-regression", self.lang),
              "\t".join(tj.REGRESSION_HEADER) + "\n" + "".join("\t".join(r) + "\n" for r in self.regression))
        write(tj.doc_path(self.docs, "spec-examples", self.lang),
              "\t".join(tj.EXAMPLES_HEADER) + "\n" + "".join("\t".join(r) + "\n" for r in self.examples))
        write(self.text / "cmudict" / "LICENSE", "license\n")
        if self.with_dg:
            td = self.dg / "xlate" / "translitjk" / "testdata"
            for src, dst in tj.copy_pairs(self.text, self.docs, self.dg, self.lang, ("translit-fixed-names", "translit-rule-regression", "spec-examples")):
                write(dst, src.read_text(encoding="utf-8"))
            for rel, body in self.dg_edit.items():
                write(td / rel, body)

    def run(self, *cmd: str) -> tuple[int, str]:
        self.flush()
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            rc = tj.main(self.args(*cmd))
        return rc, err.getvalue() + out.getvalue()


class TranslitJkSynthetic(unittest.TestCase):
    def tree(self, lang: str) -> Tree:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Tree(Path(tmp.name), lang)

    def both(self):
        for lang in ("ja", "ko"):
            yield lang, self.tree(lang)

    def assertFails(self, t: Tree, cmd: tuple[str, ...], needle: str) -> None:
        rc, msg = t.run(*cmd)
        self.assertEqual(rc, 1, msg)
        self.assertIn(needle, msg)

    # ---- lint
    def test_lint_clean(self) -> None:
        for lang, t in self.both():
            rc, msg = t.run("lint")
            self.assertEqual(rc, 0, f"{lang}: {msg}")

    def test_lint_char_outside_allowed(self) -> None:
        for lang, t in self.both():
            t.dict["AARON"] = "漢"
            self.assertFails(t, ("lint",), "不在允許字集內")
        # 規則字集之外的字，字型字集有它才算允許（chars 把它併入允許字集檔）
        for lang, t in self.both():
            t.dict["AARON"] = "漢"
            t.font_extra = "漢"
            rc, msg = t.run("lint")
            self.assertEqual(rc, 0, msg)
            self.assertEqual(tj.main(t.args("chars", "--check")), 0)

    def test_lint_duplicate_english(self) -> None:
        for lang, t in self.both():
            t.flush()
            p = tj.dict_path(t.text, lang)
            p.write_text(p.read_text(encoding="utf-8") + f"AARON\t{t.dict['AARON']}\tmachine-reviewed\n", encoding="utf-8")
            rc = tj.main(t.args("lint"))  # 不經 run()：run 會重寫檔案
            self.assertEqual(rc, 1)

    def test_lint_basis_whitelist(self) -> None:
        for lang, t in self.both():
            t.basis["AARON"] = "guess"
            self.assertFails(t, ("lint",), "basis")

    def test_lint_english_set(self) -> None:
        for lang, t in self.both():
            del t.dict["PIERRE"]
            self.assertFails(t, ("lint",), "缺 english")
            t2 = self.tree(lang)
            t2.dict["EXTRA"] = t2.dict["AARON"]
            t2.basis["EXTRA"] = "reviewed"
            self.assertFails(t2, ("lint",), "多 english")

    def test_lint_ja_spaces(self) -> None:
        t = self.tree("ja")
        t.dict["AARON"] = "アー ロン"
        self.assertFails(t, ("lint",), "不得含空白或連字號")

    def test_lint_ko_spaces(self) -> None:
        for bad in (" 에런", "에런 ", "에  런", "에-런"):
            t = self.tree("ko")
            t.dict["AARON"] = bad
            self.assertFails(t, ("lint",), "首尾與連續空白、連字號都不行")
        t = self.tree("ko")
        t.dict["AARON"] = "에 런"
        rc, msg = t.run("lint")
        self.assertEqual(rc, 0, msg)

    def test_lint_font_charset(self) -> None:
        t = self.tree("ja")
        t.flush()
        (t.font / "charset.ja.txt").write_text("ア\n", encoding="utf-8")
        rc = tj.main(t.args("lint"))
        self.assertEqual(rc, 1)

    # ---- chars
    def test_chars_check(self) -> None:
        for lang, t in self.both():
            t.flush()
            self.assertEqual(tj.main(t.args("chars", "--check")), 0)
            p = t.text / f"translit-chars.{lang}.tsv"
            p.write_text(p.read_text(encoding="utf-8") + "translit.char.U+0041\tA\ttranslit-table\n", encoding="utf-8")
            self.assertEqual(tj.main(t.args("chars", "--check")), 1)

    # ---- verify-fixed
    def test_verify_fixed_clean(self) -> None:
        for lang, t in self.both():
            rc, msg = t.run("verify-fixed")
            self.assertEqual(rc, 0, f"{lang}: {msg}")
            self.assertIn("略過副本雜湊", msg)

    def test_verify_fixed_pending_fails(self) -> None:
        for lang, t in self.both():
            t.fixed[3] = t.fixed[3][:4] + ("pending",)
            self.assertFails(t, ("verify-fixed",), "pending")

    def test_verify_fixed_review_format(self) -> None:
        for bad, needle in (("ok:甲", "review"), ("ok:甲,甲", "不同的人"), ("done", "review"), ("ok:甲,乙,丙", "review")):
            t = self.tree("ja")
            t.fixed[0] = t.fixed[0][:4] + (bad,)
            self.assertFails(t, ("verify-fixed",), needle)

    def test_verify_fixed_columns(self) -> None:
        t = self.tree("ja")
        t.fixed[0] = ("N00", "", "cmudict", "", "ok:甲,乙")
        self.assertFails(t, ("verify-fixed",), "必須一致")
        t = self.tree("ja")
        t.fixed[0] = ("N00", "ア", "weird", "", "ok:甲,乙")
        self.assertFails(t, ("verify-fixed",), "tier")
        t = self.tree("ja")
        t.fixed[0] = ("N00", "漢", "cmudict", "", "ok:甲,乙")
        self.assertFails(t, ("verify-fixed",), "不在允許字集內")
        t = self.tree("ja")
        t.fixed[1] = t.fixed[0]
        self.assertFails(t, ("verify-fixed",), "重複")
        t = self.tree("ko")
        t.fixed[0] = ("N00", "에런", "cmudict", "J1.AA", "ok:甲,乙")
        self.assertFails(t, ("verify-fixed",), "規則編號")

    def test_verify_fixed_regression_set(self) -> None:
        t = self.tree("ko")
        t.regression.pop()
        self.assertFails(t, ("verify-fixed",), "規則回歸表的 name 集合")

    def test_verify_fixed_copy_hash(self) -> None:
        t = self.tree("ja")
        t.with_dg = True
        rc, msg = t.run("verify-fixed")
        self.assertEqual(rc, 0, msg)
        self.assertIn("副本雜湊", msg)
        t = self.tree("ja")
        t.with_dg = True
        t.dg_edit = {"fixed-names.ja.tsv": "tampered\n"}
        self.assertFails(t, ("verify-fixed",), "副本雜湊不符")
        t = self.tree("ko")
        t.with_dg = True
        t.dg_edit = {"text/translit-chars.ko.tsv": "tampered\n"}
        # text 的副本不在 flush 的 copy 清單內：缺檔時回報，有檔且不同時回報雜湊不符
        self.assertFails(t, ("verify-fixed",), "副本")

    # ---- examples
    def test_examples_clean(self) -> None:
        for lang, t in self.both():
            rc, msg = t.run("examples", "--check")
            self.assertEqual(rc, 0, f"{lang}: {msg}")

    def test_examples_negatives(self) -> None:
        cases = [
            (("Kate", "漢", "J1.EY", "rule"), "不在允許字集內"),
            (("Kate", "アー", "K2.EY", "rule"), "規則編號"),
            (("Kate", "アー", "J1.EY", "maybe"), "kind"),
            (("Ka7e", "アー", "J1.EY", "rule"), "name"),
            (("Kate", "", "J1.EY", "rule"), "空"),
        ]
        for row, needle in cases:
            t = self.tree("ja")
            t.examples = [row]
            self.assertFails(t, ("examples", "--check"), needle)
        t = self.tree("ja")
        t.examples = [("Kate", "ケ", "J1.EY", "rule"), ("Kate", "ケ", "J1.EY", "rule")]
        self.assertFails(t, ("examples", "--check"), "重複")
        t = self.tree("ko")
        t.examples = [("Kate", "에런", "!K5", "rule")]
        rc, msg = t.run("examples", "--check")
        self.assertEqual(rc, 0, msg)


class TranslitJkRealData(unittest.TestCase):
    """真實 text/、docs/re 的護欄：缺檔就略過，不靜默通過（以 skipTest 印出原因）。"""

    def setUp(self) -> None:
        if not (tj.DEFAULT_TEXT / "translit-ja-names.tsv").exists():
            self.skipTest("沒有真實 text/")

    def test_real_chars_and_lint(self) -> None:
        for lang in ("ja", "ko"):
            self.assertEqual(tj.cmd_chars(tj.DEFAULT_TEXT, lang, True), 0)
            self.assertEqual(tj.cmd_lint(tj.DEFAULT_TEXT, lang), 0)

    def test_real_examples(self) -> None:
        for lang in ("ja", "ko"):
            if not tj.doc_path(tj.DEFAULT_DOCS, "spec-examples", lang).exists():
                self.skipTest("沒有 docs/re 的例子表")
            self.assertEqual(tj.cmd_examples(tj.DEFAULT_TEXT, tj.DEFAULT_DOCS, tj.DEFAULT_DOSGOLEM, lang), 0)


if __name__ == "__main__":
    unittest.main()
