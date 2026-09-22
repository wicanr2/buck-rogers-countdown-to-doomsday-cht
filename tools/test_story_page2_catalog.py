import tempfile
import unittest
from pathlib import Path

from story_page2_catalog import conservative_cells, validate


ROOT = Path(__file__).resolve().parents[1]


class StoryPage2CatalogTest(unittest.TestCase):
    def test_formal_ready_pair(self):
        validate(ROOT / "text/story-page2-events.tsv", ROOT / "text/story-page2.zh-TW.tsv")

    def test_rejects_row_24_status_event(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            text = (ROOT / "text/story-page2-events.tsv").read_text(encoding="utf-8").replace("\t20\t1\t285666098", "\t24\t1\t285666098")
            events.write_text(text, encoding="utf-8")
            translations.write_bytes((ROOT / "text/story-page2.zh-TW.tsv").read_bytes())
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_rejects_unreviewed_draft_status(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            events.write_text(
                (ROOT / "text/story-page2-events.tsv").read_text(encoding="utf-8").replace("\tREADY\n", "\tDRAFT\n", 1),
                encoding="utf-8",
            )
            translations.write_bytes((ROOT / "text/story-page2.zh-TW.tsv").read_bytes())
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_rejects_fullwidth_overflow(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            events.write_bytes((ROOT / "text/story-page2-events.tsv").read_bytes())
            text = (ROOT / "text/story-page2.zh-TW.tsv").read_text(encoding="utf-8").replace(
                "作為新進隊員，NEO 已帶你們前往\t", "作為新進隊員，NEO 已帶你們前往" + ("超" * 20) + "\t"
            )
            translations.write_text(text, encoding="utf-8")
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_conservative_mixed_advance(self):
        self.assertEqual(conservative_cells("甲A（NEO）"), 2 + 1 + 2 + 3 + 2)
