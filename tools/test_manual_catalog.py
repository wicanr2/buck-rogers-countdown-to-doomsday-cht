import csv
from pathlib import Path
import tempfile
import unittest

import manual_catalog as subject


class ManualCatalogTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.questions = root / "questions.tsv"
        self.crosswalk = root / "crosswalk.tsv"
        self.events = root / "events.tsv"
        self.catalog = root / "catalog.tsv"
        self.questions.write_text(
            "record_index\tpage\theading_ascii\tordinal\n1\t24\tThe Elevator\t5\n", encoding="utf-8"
        )
        self.crosswalk.write_text(
            "record_index\tstatus\n1\tconfirmed\n", encoding="utf-8"
        )
        self.events.write_text(
            "event_key\trecord_index\tpage\theading_ascii\tordinal\ttext_key\n"
            "manual.page24.the_elevator.word5\t1\t24\tThe Elevator\t5\tmanual.log.11.the_elevator\n",
            encoding="utf-8",
        )
        self.catalog.write_text(
            "key\ttranslation\tsource\nmanual.log.11.the_elevator\t昇降機段落\tmanual-and-runtime\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_confirmed_exact_mapping(self):
        subject.validate(self.questions, self.crosswalk, self.events, self.catalog)

    def test_rejects_unconfirmed_source(self):
        self.crosswalk.write_text("record_index\tstatus\n1\tstrong-inference\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "不是 confirmed"):
            subject.validate(self.questions, self.crosswalk, self.events, self.catalog)

    def test_rejects_event_key_page_or_ordinal_mismatch(self):
        text = self.events.read_text(encoding="utf-8").replace("page24", "page25")
        self.events.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "event_key"):
            subject.validate(self.questions, self.crosswalk, self.events, self.catalog)

    def test_rejects_unmapped_catalog_entry(self):
        with self.catalog.open("a", encoding="utf-8") as out:
            out.write("manual.extra\t多餘\tmanual-and-runtime\n")
        with self.assertRaisesRegex(ValueError, "未映射"):
            subject.validate(self.questions, self.crosswalk, self.events, self.catalog)

    def test_accepts_translation_at_single_page_capacity(self):
        self.catalog.write_text(
            "key\ttranslation\tsource\n"
            f"manual.log.11.the_elevator\t{'字' * subject.MANUAL_PAGE_CAPACITY}\tmanual-and-runtime\n",
            encoding="utf-8",
        )
        subject.validate(self.questions, self.crosswalk, self.events, self.catalog)

    def test_rejects_translation_over_single_page_capacity(self):
        self.catalog.write_text(
            "key\ttranslation\tsource\n"
            f"manual.log.11.the_elevator\t{'字' * (subject.MANUAL_PAGE_CAPACITY + 1)}\tmanual-and-runtime\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "超過 14 列，超過單頁上限（504 個全形格）"):
            subject.validate(self.questions, self.crosswalk, self.events, self.catalog)


if __name__ == "__main__":
    unittest.main()
