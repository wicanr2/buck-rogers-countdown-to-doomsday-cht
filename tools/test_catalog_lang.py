"""規格 040 §3.1：Python 工具的語言參數（預設 zh-TW，行為不變）。"""
from pathlib import Path
import tempfile
import unittest

import catalog_lang
import ecl_translation_merge
import header_columns
import name_glossary

ROOT = Path(__file__).resolve().parents[1]


class CatalogLangTests(unittest.TestCase):
    def test_default_names_are_unchanged(self):
        self.assertEqual(catalog_lang.catalog_name("menu"), "menu.zh-TW.tsv")
        self.assertEqual(catalog_lang.catalog_name("ecl-text", "ja"), "ecl-text.ja.tsv")
        self.assertEqual(catalog_lang.catalog_glob(), "*.zh-TW.tsv")
        with self.assertRaises(ValueError):
            catalog_lang.catalog_name("menu", "fr")

    def test_tool_defaults_keep_zh_tw_files(self):
        self.assertEqual(header_columns.MENU_SOURCES[0], ("menu-events.tsv", "menu.zh-TW.tsv"))
        self.assertEqual(header_columns.ENGINE_TEXT, "engine-fragment.zh-TW.tsv")
        self.assertEqual(name_glossary.DEFAULT_APPLY, name_glossary.default_apply())
        self.assertIn("manual.zh-TW.tsv", name_glossary.DEFAULT_APPLY)
        self.assertEqual(name_glossary.default_apply("ko")[0], "ecl-text.ko.tsv")
        self.assertEqual(name_glossary.LOGBOOK_CATALOG, "logbook.zh-TW.tsv")

    def test_big5_check_is_zh_tw_only(self):
        self.assertTrue(ecl_translation_merge.check("한국어", "x"))
        self.assertEqual(ecl_translation_merge.check("한국어", "x", "ko"), [])

    def test_header_columns_other_language_falls_back(self):
        rows = header_columns.load_list(ROOT / "text/header-columns.tsv")
        self.assertEqual(header_columns.check_load(ROOT / "text", rows), [])
        with tempfile.TemporaryDirectory() as directory:
            lang_dir = Path(directory)
            # 沒有任何 ja 譯文：每一列都退回一般排版，不讓語言失效。
            notes = header_columns.check_lang_load(ROOT / "text", lang_dir, rows, "ja")
            self.assertEqual(len(notes), len(rows))
            self.assertTrue(all("退回一般排版" in n for n in notes))


if __name__ == "__main__":
    unittest.main()
