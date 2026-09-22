import tempfile
import unittest
from pathlib import Path

from story_opening_catalog import conservative_cells, validate


ROOT = Path(__file__).resolve().parents[1]


class StoryOpeningCatalogTest(unittest.TestCase):
    def test_formal_draft_pair(self):
        validate(ROOT / "text/story-opening-events.tsv", ROOT / "text/story-opening.zh-TW.tsv")

    def test_rejects_translation_trailing_space(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            events.write_bytes((ROOT / "text/story-opening-events.tsv").read_bytes())
            text = (ROOT / "text/story-opening.zh-TW.tsv").read_text(encoding="utf-8").replace("勢力。\t", "勢力。 \t")
            translations.write_text(text, encoding="utf-8")
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_rejects_translation_control_character(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            events.write_bytes((ROOT / "text/story-opening-events.tsv").read_bytes())
            text = (ROOT / "text/story-opening.zh-TW.tsv").read_text(encoding="utf-8").replace(
                "聽聞巴克羅吉斯與\t", "聽聞巴克羅吉斯\u0001與\t"
            )
            translations.write_text(text, encoding="utf-8")
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_rejects_translation_over_event_capacity(self):
        with tempfile.TemporaryDirectory() as temp:
            events = Path(temp) / "events.tsv"
            translations = Path(temp) / "translations.tsv"
            events.write_bytes((ROOT / "text/story-opening-events.tsv").read_bytes())
            text = (ROOT / "text/story-opening.zh-TW.tsv").read_text(encoding="utf-8").replace(
                "聽聞巴克羅吉斯與\t", "聽聞巴克羅吉斯與" + ("超" * 20) + "\t"
            )
            translations.write_text(text, encoding="utf-8")
            with self.assertRaises(ValueError):
                validate(events, translations)

    def test_conservative_fullwidth_advance_is_two_cells(self):
        self.assertEqual(conservative_cells("甲A（RAM）"), 2 + 1 + 2 + 3 + 2)
