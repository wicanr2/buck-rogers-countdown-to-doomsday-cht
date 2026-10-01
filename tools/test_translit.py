import tempfile
import unittest
from pathlib import Path

import translit
from catalog_font import read_catalog

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"
SRC = ROOT / "workplace" / "translit-src" / "wiki-english.wikitext"

MINI = """== 人名 ==
{| class="wikitable"
|-
! || {{IPA|b}} || {{IPA|p}}&ZeroWidthSpace;{{efn|name=tr_dr}} || {{IPA|z}}<br />{{IPA|{{Nowrap|dz}}}}
|-
| {{rh}}| || || 布 || 夫{{efn-lr|name=pre}}{{换行夹注|弗}} || 茲 || {{rh}}|
|-
| {{rh}}|{{IPA|e}}&ZeroWidthSpace;{{efn|name=ai-}} || rowspan="2"|埃 || rowspan="2" {{no2|贝}} || 特 || 泽 || {{rh}}|{{IPA|e}}
|-
| {{rh}}|{{IPA|eɪ}} || 泰 || {{no2|馬{{efn-lr|name=female}}{{换行夹注|瑪}}}} || {{rh}}|{{IPA|eɪ}}
|}
"""


class ParseTest(unittest.TestCase):
    def test_split_cells_ignores_template_pipes(self):
        self.assertEqual(translit.split_cells("a || {{x|y||z}} || b"), ["a ", " {{x|y||z}} ", " b"])

    def test_parse_content(self):
        c = translit.parse_content('rowspan="2" {{no2|雷{{efn-lr|name=female}}{{换行夹注|蕾}}}}')
        self.assertEqual((c.zh, c.variant, c.notes, c.rowspan), ("雷", "蕾", ["female"], 2))

    def test_mini_table_rowspan_and_variants(self):
        rows = translit.parse_person_table(MINI, ncols=4)
        got = {(r.vowel_row, r.consonant): (r.zh, r.zh_female, r.zh_initial, r.note) for r in rows}
        self.assertEqual(got[("單獨輔音", "p")], ("夫", "", "弗", "pre,tr_dr"))
        self.assertEqual(got[("e", "無輔音")], ("埃", "", "", "ai-"))
        self.assertEqual(got[("eɪ", "無輔音")], ("埃", "", "", ""))
        self.assertEqual(got[("eɪ", "b")], ("貝", "", "", ""))  # rowspan 無豎線寫法 + 轉繁
        self.assertEqual(got[("eɪ", "p")], ("泰", "", "", "tr_dr"))
        self.assertEqual(got[("eɪ", "z dz")], ("馬", "瑪", "", "female"))
        self.assertEqual(got[("e", "z dz")], ("澤", "", "", "ai-"))
        self.assertNotIn(("單獨輔音", "無輔音"), got)

    def test_bad_row_count_rejected(self):
        bad = MINI.replace("| {{rh}}|{{IPA|eɪ}} || 泰 ||", "| {{rh}}|{{IPA|eɪ}} || 泰 || 多 ||")
        with self.assertRaises(translit.TranslitError):
            translit.parse_person_table(bad, ncols=4)


@unittest.skipUnless(SRC.exists(), "本機未下載 wikitext")
class RealTableTest(unittest.TestCase):
    def test_committed_table_matches_source(self):
        rows = translit.parse_person_table(SRC.read_text("utf-8"))
        self.assertEqual(translit.table_tsv(rows), (TEXT / "translit-table.tsv").read_text("utf-8"))

    def test_shape(self):
        rows = translit.parse_person_table(SRC.read_text("utf-8"))
        vowels = {r.vowel_row for r in rows}
        self.assertEqual(len(vowels), 18)  # 17 元音列 + 單獨輔音
        self.assertEqual(len({r.consonant for r in rows}), 26)
        chars = translit.table_chars(rows) - set(translit.RULE_CHARS)
        self.assertEqual(len(chars), 290)
        cell = {(r.vowel_row, r.consonant): r for r in rows}
        self.assertEqual(cell[("eɪ", "t")].zh, "泰")
        self.assertEqual(cell[("eɪ", "d")].zh, "德")
        self.assertEqual(cell[("iː ɪ (j)", "ɹ")].zh_female, "麗")
        self.assertEqual(cell[("單獨輔音", "f")].zh_initial, "弗")


class NamesTest(unittest.TestCase):
    def write(self, text: str) -> Path:
        d = tempfile.mkdtemp()
        p = Path(d) / "n.tsv"
        p.write_text(text, "utf-8")
        return p

    def test_committed_names_lint(self):
        rows = translit.read_table(TEXT / "translit-table.tsv")
        names = translit.read_names(TEXT / "translit-names.tsv")
        allowed = translit.table_chars(rows)
        for e in names:
            allowed.update(e.chinese)
        self.assertEqual(translit.lint_names(names, allowed), [])

    def test_lint_reports_foreign_char(self):
        names = [translit.NameEntry("ABC", "", "阿龘", "reviewed")]
        self.assertEqual(len(translit.lint_names(names, {"阿"})), 1)

    def test_bad_rows(self):
        head = "english\tgender\tchinese\tbasis\n"
        for row in ("abc\t\t阿\treviewed\n", "A\t\t阿\treviewed\n", "ABC\tX\t阿\treviewed\n",
                    "ABC\t\t阿\tguess\n", "ABC\t\t阿\treviewed\nABC\t\t巴\treviewed\n"):
            with self.subTest(row=row), self.assertRaises(translit.TranslitError):
                translit.read_names(self.write(head + row))

    def test_chars_catalog_is_valid_font_catalog(self):
        text = translit.chars_catalog({"阿", "思", "茜"})
        p = self.write(text)
        entries = read_catalog(p)
        self.assertEqual([e.translation for e in entries], sorted("阿思茜"))
        self.assertTrue(all(e.source == "translit-table" for e in entries))

    def test_committed_chars_catalog_current(self):
        self.assertEqual(translit.main(["--text", str(TEXT), "chars", "--check"]), 0)
        read_catalog(TEXT / "translit-chars.zh-TW.tsv")

    def test_lang_is_zh_tw_only(self):
        """規格 044 §3.5：--lang ja|ko|zh-CN 會用 zh 譯音表寫出內容錯誤的字集檔，所以不接受。"""
        import contextlib
        import io
        for lang in ("ja", "ko", "zh-CN"):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
                translit.main(["--text", str(TEXT), "--lang", lang, "chars", "--check"])
            self.assertEqual(cm.exception.code, 2)
        self.assertEqual(translit.main(["--text", str(TEXT), "--lang", "zh-TW", "chars", "--check"]), 0)


if __name__ == "__main__":
    unittest.main()
