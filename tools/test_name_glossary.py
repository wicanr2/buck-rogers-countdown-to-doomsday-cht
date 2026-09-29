import io
import tempfile
import unittest
from pathlib import Path

import name_glossary as ng

ROOT = Path(__file__).resolve().parents[1]
HEADER = "english\tenglish_mixed\tchinese\tkind\tperson\tbasis\tnote\n"
ROWS = [
    "BUCK ROGERS\tBuck Rogers\t巴克羅吉斯\tfull\tbuck-rogers\tprinted:SCAN#1\t",
    "BUCK\tBuck\t巴克\tshort\tbuck-rogers\tprinted:SCAN#2\t",
    "WILMA DEERING\tWilma Deering\t威瑪•狄琳\tfull\twilma-deering\tprinted:SCAN#3\told=威瑪•迪林",
    "LANDON\tLandon\t南敦\tfull\tlandon\tprinted:SCAN#4\told=蘭登",
    "SCOT.DOS\tScot.dos\t斯科特\tfull\tscot\txinhua\told=史考特|Scot.dos|Scot",
    "WILLIAMS\tWilliams\t威廉\tshort\twilliams\tprinted:SCAN#5\told=威廉斯",
    "ALEXANDER WILLIAMS\tAlexander Williams\t亞歷山大•威廉\tfull\twilliams\tprinted:SCAN#6\talias=Alexander William",
    "HOLZERHEIN\tHolzerhein\t何茲漢\tfull\tholzerhein\tprinted:SCAN#7\told=何茲漢（HOLZERHEIN.DOS）；alias=Holzerhein.dos",
]
EXCLUDE = "phrase\tscope\tnote\n史考特海鮮坊\tecl.*\t店名\n史考特的\thmenu.x\t店名\n"


def glossary(rows=ROWS, exclude=EXCLUDE):
    tmp = tempfile.TemporaryDirectory()
    g = Path(tmp.name) / "g.tsv"
    e = Path(tmp.name) / "e.tsv"
    g.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    e.write_text(exclude, encoding="utf-8")
    try:
        return ng.read_glossary(g, e)
    finally:
        tmp.cleanup()


def catalog(tmp, name, rows):
    path = Path(tmp) / name
    path.write_text("key\ttranslation\tsource\n" + "".join(f"{k}\t{t}\truntime\n" for k, t in rows), encoding="utf-8")
    return path


class ConvergeTest(unittest.TestCase):
    def setUp(self):
        self.g = glossary()

    def test_longest_match_keeps_full_name(self):
        hits, _ = ng.scan("巴克羅吉斯與巴克", "k", self.g)
        self.assertEqual([h.matched for h in hits], ["巴克羅吉斯", "巴克"])

    def test_old_name_replaced(self):
        text, changes, _ = ng.converge("告知已與蘭登會面，威瑪•迪林也在", "k", self.g)
        self.assertEqual(text, "告知已與南敦會面，威瑪•狄琳也在")
        self.assertEqual([(o, n) for o, n, _ in changes], [("蘭登", "南敦"), ("威瑪•迪林", "威瑪•狄琳")])

    def test_dot_variants_are_old(self):
        for variant in ("威瑪·狄琳", "威瑪．狄琳", "威瑪狄琳"):
            text, _, _ = ng.converge(variant, "k", self.g)
            self.assertEqual(text, "威瑪•狄琳")

    def test_exclusion_skips_phrase_in_scope_only(self):
        text, changes, skipped = ng.converge("史考特海鮮坊與史考特", "ecl.1", self.g)
        self.assertEqual(text, "史考特海鮮坊與斯科特")
        self.assertEqual(len(changes), 1)
        self.assertEqual(skipped, [(0, "史考特海鮮坊")])
        text, _, _ = ng.converge("史考特的(S)", "hmenu.x", self.g)
        self.assertEqual(text, "史考特的(S)")
        text, _, _ = ng.converge("史考特的資料", "ecl.2", self.g)
        self.assertEqual(text, "斯科特的資料")

    def test_ascii_old_name_eats_space_before_cjk(self):
        text, _, _ = ng.converge("Scot.dos 出現在你面前，」Scot.dos 說", "k", self.g)
        self.assertEqual(text, "斯科特出現在你面前，」斯科特說")

    def test_ascii_old_name_needs_word_boundary(self):
        text, _, _ = ng.converge("Scott's 與 Scotland", "k", self.g)
        self.assertEqual(text, "Scott's 與 Scotland")

    def test_manual_keeps_ascii(self):
        text, changes, _ = ng.converge("Scot.dos 的聲音，蘭登", "manual.x", self.g, skip_ascii_old=True)
        self.assertEqual(text, "Scot.dos 的聲音，南敦")
        self.assertEqual(len(changes), 1)

    def test_old_name_with_parenthesis_collapses(self):
        text, _, _ = ng.converge("驚動何茲漢（HOLZERHEIN.DOS）了", "k", self.g)
        self.assertEqual(text, "驚動何茲漢了")

    def test_paren_follow_listed(self):
        self.assertEqual(ng.paren_follow("巴克(B)與南敦（Landon）", "k", self.g), [("巴克", "巴克(B)"), ("南敦", "南敦（Landon）")])


class StripNotesTest(unittest.TestCase):
    def setUp(self):
        self.g = glossary()

    def test_strips_person_notes_with_titles(self):
        text, removed = ng.strip_notes(
            "巴克羅吉斯上校（Captain Buck Rogers）說，亞歷山大威廉博士（Dr. Alexander William）與何茲漢（Holzerhein.dos）", self.g
        )
        self.assertEqual(text, "巴克羅吉斯上校說，亞歷山大威廉博士與何茲漢")
        self.assertEqual(len(removed), 3)

    def test_keeps_non_person_and_mismatched_notes(self):
        src = "低地人（Lowlander）與太陽王（Sun King），南敦（Wilma）"
        text, removed = ng.strip_notes(src, self.g)
        self.assertEqual(text, src)
        self.assertEqual(removed, [])


class LintTest(unittest.TestCase):
    def test_reports_old_names_and_font(self):
        g = glossary()
        with tempfile.TemporaryDirectory() as tmp:
            ok = catalog(tmp, "ok.zh-TW.tsv", [("a", "南敦與斯科特")])
            bad = catalog(tmp, "bad.zh-TW.tsv", [("b", "蘭登與史考特")])
            manual = catalog(tmp, "manual.zh-TW.tsv", [("c", "Scot.dos 在此")])
            self.assertEqual(ng.lint(g, [ok, manual], None), [])
            errors = ng.lint(g, [bad], None)
            self.assertEqual(len(errors), 2)
            font = set("南敦與斯科特巴克羅吉斯威瑪•狄琳威廉亞歷山大何茲漢")
            self.assertEqual(ng.lint(g, [], font), [])
            font.discard("敦")
            self.assertEqual(len(ng.lint(g, [], font)), 1)

    def test_glossary_rejects_bad_rows(self):
        cases = [
            ROWS + ["ZANE\t\t贊恩·甲\tfull\tzane\txinhua\t"],  # 錯誤間隔號
            ROWS + ["ZANE\t\t贊恩\tlong\tzane\txinhua\t"],  # kind
            ROWS + ["ZANE\t\t贊恩\tfull\tzane\tguess\t"],  # basis
            ROWS + ["Zane\t\t贊恩\tfull\tzane\txinhua\t"],  # english 非全大寫
            ROWS + ["ZANE\tZain\t贊恩\tfull\tzane\txinhua\t"],  # mixed 拼法不同
            ROWS + ["ZANE\t\t南敦\tfull\tzane\txinhua\t"],  # chinese 重複
            ROWS + ["ZANE\t\t贊恩\tfull\tzane\txinhua\told=南敦"],  # 舊譯名等於正式譯名
        ]
        for rows in cases:
            with self.subTest(row=rows[-1]):
                with self.assertRaises(ng.GlossaryError):
                    glossary(rows)


class ApplyTest(unittest.TestCase):
    def test_apply_dry_run_and_write(self):
        g = glossary()
        with tempfile.TemporaryDirectory() as tmp:
            path = catalog(tmp, "ecl.zh-TW.tsv", [("ecl.1", "史考特與蘭登"), ("ecl.2", "無人名\"引號")])
            before = path.read_bytes()
            out = io.StringIO()
            self.assertEqual(ng.apply(g, [path], True, out), 2)
            self.assertEqual(path.read_bytes(), before)
            self.assertIn("REPLACE\tecl.zh-TW.tsv\tecl.1\t史考特\t斯科特", out.getvalue())
            ng.apply(g, [path], False, io.StringIO())
            self.assertEqual(path.read_text(encoding="utf-8").splitlines()[1:], ["ecl.1\t斯科特與南敦\truntime", "ecl.2\t無人名\"引號\truntime"])


class FormalGlossaryTest(unittest.TestCase):
    def test_formal_glossary_loads_and_catalogs_converged(self):
        g = ng.read_glossary()
        self.assertGreater(len(g.names), 30)
        errors = ng.lint(g, sorted((ROOT / "text").glob("*.zh-TW.tsv")), None)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
