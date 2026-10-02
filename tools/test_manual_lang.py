import tempfile
import unittest
from pathlib import Path

import manual_lang as m


class ManualRowsTest(unittest.TestCase):
    """案例對照 dosgolem halfwidth_part2_test.go 的 manualRows。"""

    def test_whole_character_wrap(self):
        rows = m.manual_rows("A" * 71 + "字B")
        self.assertEqual(rows[0], "A" * 71)
        self.assertEqual(rows[1], "字B")

    def test_capacity_boundaries(self):
        self.assertIsNotNone(m.manual_rows("字" * 504))
        self.assertIsNotNone(m.manual_rows("A" * 1008))
        self.assertIsNone(m.manual_rows("字" * 505))
        self.assertIsNone(m.manual_rows("A" * 1009))
        self.assertIsNone(m.manual_rows("A" * 71 + "字" * (36 * 13 + 1)))

    def test_empty(self):
        self.assertIsNone(m.manual_rows(""))

    def test_units(self):
        self.assertEqual(m.units("AB字"), 4)
        self.assertEqual(m.units("•"), 1)
        self.assertEqual(m.units("「」"), 4)


class LatinTokensTest(unittest.TestCase):
    def test_tokens(self):
        self.assertEqual(m.latin_tokens("NEO 的 RAM 與 Scot.dos 第 3 頁"), {"NEO", "RAM", "Scot.dos"})
        self.assertEqual(m.latin_tokens("20 CR 與 5.5"), {"CR"})
        self.assertEqual(m.latin_tokens("NEO部隊"), {"NEO"})
        self.assertEqual(m.latin_tokens("NEO는"), {"NEO"})


class ParagraphTest(unittest.TestCase):
    CS = set("あいうえおのは。 NEORAM")

    def ok(self, text, zh="NEO RAM 說明"):
        return m.check_paragraph("k", text, zh, self.CS)

    def test_pass(self):
        self.assertEqual(self.ok("NEOのRAMは。"), [])

    def test_new_latin_word(self):
        self.assertTrue(any("新增的拉丁字母詞" in e for e in self.ok("NEOのBUCKは。")))

    def test_charset(self):
        self.assertTrue(any("字集外" in e for e in self.ok("NEOの漢は。")))

    def test_tab_newline_and_backslash_n(self):
        for bad in ("あ\tい", "あ\nい", "あ\\nい"):
            self.assertTrue(any("tab" in e for e in self.ok(bad)), bad)

    def test_trim(self):
        self.assertTrue(any("首尾" in e for e in self.ok(" あい")))

    def test_over_safe_units(self):
        errs = m.check_paragraph("k", "あ" * 481, "", None)
        self.assertTrue(any("安全上限" in e for e in errs))
        self.assertEqual(m.check_paragraph("k", "あ" * 468, "", None), [])  # 936 單位、13 列

    def test_over_safe_rows(self):
        # 13 列剛好、14 列超過安全上限但沒超過硬上限
        self.assertEqual(m.check_paragraph("k", "あ" * (36 * 13), "", None), [])
        errs = m.check_paragraph("k", "あ" * (36 * 13 + 1), "", None)
        self.assertTrue(any("安全上限 13" in e for e in errs))

    def test_ja_latin_spacing(self):
        self.assertEqual(m.check_paragraph("k", "NEOの部隊", "NEO", None, "ja"), [])
        self.assertTrue(any("空白" in e for e in m.check_paragraph("k", "NEO の部隊", "NEO", None, "ja")))
        self.assertTrue(any("空白" in e for e in m.check_paragraph("k", "部隊 NEO", "NEO", None, "ja")))
        self.assertEqual(m.check_paragraph("k", "NEO 순찰대", "NEO", None, "ko"), [])

    def test_over_rows(self):
        errs = m.check_paragraph("k", "A" * 71 + "あ" * (36 * 13 + 1), "", None)
        self.assertTrue(any("超過" in e for e in errs))

    def test_empty(self):
        self.assertTrue(m.check_paragraph("k", "", "x", None))


class NumbersTest(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(m.numbers("第 7 頁 80 點 10% 1,000"), ["1,000", "10", "7", "80"])
        errs = m.check_paragraph("k", "あ 7", "二 8", None)
        self.assertTrue(any("數字" in e for e in errs))
        self.assertEqual(m.check_paragraph("k", "7あ 80", "第 80 頁 7", None), [])


class CatalogTest(unittest.TestCase):
    def write(self, d, name, rows):
        p = Path(d) / name
        p.write_text("key\ttranslation\tsource\n" + "".join(f"{k}\t{t}\t{s}\n" for k, t, s in rows), encoding="utf-8")
        return p

    def test_catalog(self):
        with tempfile.TemporaryDirectory() as d:
            zh = self.write(d, "zh.tsv", [("a", "NEO 一", "s1"), ("b", "二", "s2")])
            ok = self.write(d, "ok.tsv", [("a", "NEOあ", "s1"), ("b", "い", "s2")])
            self.assertEqual(m.check_catalog("ja", ok, zh, None), [])
            order = self.write(d, "order.tsv", [("b", "い", "s2"), ("a", "NEOあ", "s1")])
            self.assertTrue(any("順序" in e for e in m.check_catalog("ja", order, zh, None)))
            missing = self.write(d, "missing.tsv", [("a", "NEOあ", "s1")])
            self.assertTrue(any("集合" in e for e in m.check_catalog("ja", missing, zh, None)))
            src = self.write(d, "src.tsv", [("a", "NEOあ", "s9"), ("b", "い", "s2")])
            self.assertTrue(any("source" in e for e in m.check_catalog("ja", src, zh, None)))
            dup = self.write(d, "dup.tsv", [("a", "NEOあ", "s1"), ("a", "い", "s1")])
            self.assertTrue(any("重複" in e for e in m.check_catalog("ja", dup, zh, None)))

    def test_header_only_is_a_key_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            zh = self.write(d, "zh.tsv", [("a", "一", "s")])
            empty = self.write(d, "e.tsv", [])
            self.assertTrue(m.check_catalog("ko", empty, zh, None))


if __name__ == "__main__":
    unittest.main()
