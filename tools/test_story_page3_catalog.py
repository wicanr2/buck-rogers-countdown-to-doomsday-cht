import tempfile
import unittest
from pathlib import Path

from story_page3_catalog import conservative_cells, validate


ROOT = Path(__file__).resolve().parents[1]


class StoryPage3CatalogTest(unittest.TestCase):
    def test_formal_ready_pair(self):
        validate(ROOT / "text/story-page3-events.tsv", ROOT / "text/story-page3.zh-TW.tsv")

    def test_rejects_draft_catalog_status(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            text = (ROOT / "text/story-page3-events.tsv").read_text(encoding="utf-8").replace("\tconfirmed\tREADY", "\tconfirmed\tDRAFT", 1)
            events.write_text(text, encoding="utf-8")
            translations.write_bytes((ROOT / "text/story-page3.zh-TW.tsv").read_bytes())
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_rejects_row_24_status_event(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            text = (ROOT / "text/story-page3-events.tsv").read_text(encoding="utf-8").replace("\t21\t1\t297111967", "\t24\t1\t297111967")
            events.write_text(text, encoding="utf-8")
            translations.write_bytes((ROOT / "text/story-page3.zh-TW.tsv").read_bytes())
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_rejects_fullwidth_overflow(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            events.write_bytes((ROOT / "text/story-page3-events.tsv").read_bytes())
            text = (ROOT / "text/story-page3.zh-TW.tsv").read_text(encoding="utf-8").replace(
                "你們坐進不舒服的椅子，\t", "你們坐進不舒服的椅子，" + ("超" * 20) + "\t"
            )
            translations.write_text(text, encoding="utf-8")
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_conservative_mixed_advance(self):
        self.assertEqual(conservative_cells("甲A（NEO）"), 2 + 1 + 2 + 3 + 2)
