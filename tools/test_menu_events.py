from pathlib import Path
import tempfile
import unittest

import menu_events as subject


VALID_EVENTS = (
    "event_key\tsequence\ttext_key\toriginal_length\toriginal_sha256\tcaller\tbackground\tforeground\trow\tcolumn\n"
    "race.screen.prompt\t1\tmenu.pick_race\t9\t"
    "e932f4664fa9d32f95c406fe026368eb2e88dcbdadab01fc684d95abddef0c93\t"
    "37F1:158C\t0\t13\t2\t1\n"
)
VALID_CATALOG = "key\ttranslation\tsource\nmenu.pick_race\t選擇種族\truntime\n"


class MenuEventsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.events = root / "events.tsv"
        self.catalog = root / "catalog.tsv"
        self.events.write_text(VALID_EVENTS, encoding="utf-8")
        self.catalog.write_text(VALID_CATALOG, encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_exact_identity(self):
        subject.validate(self.events, self.catalog)

    def test_rejects_schema_sequence_hash_caller_and_bounds(self):
        replacements = [
            ("event_key\t", "wrong\t"),
            ("\t1\tmenu", "\t2\tmenu"),
            ("e932f466", "E932f466"),
            ("37F1:158C", "37f1:158c"),
            ("\t2\t1\n", "\t25\t1\n"),
        ]
        for old, new in replacements:
            with self.subTest(new=new):
                self.events.write_text(VALID_EVENTS.replace(old, new), encoding="utf-8")
                with self.assertRaises(ValueError):
                    subject.validate(self.events, self.catalog)

    def test_rejects_missing_and_orphan_catalog_keys(self):
        self.catalog.write_text("key\ttranslation\tsource\nmenu.other\t其他\truntime\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "不完整"):
            subject.validate(self.events, self.catalog)

    def test_repository_inventory_matches_catalog(self):
        root = Path(__file__).resolve().parents[1]
        subject.validate(root / "text/menu-events.tsv", root / "text/menu.zh-TW.tsv")


if __name__ == "__main__":
    unittest.main()
