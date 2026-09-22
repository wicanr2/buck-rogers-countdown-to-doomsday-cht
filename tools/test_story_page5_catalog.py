import csv
import tempfile
import unittest
from pathlib import Path

from story_page5_catalog import conservative_cells, validate

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "text/story-page5-events.tsv"
TRANSLATIONS = ROOT / "text/story-page5.zh-TW.tsv"


class StoryPage5CatalogTest(unittest.TestCase):
    def _copy_with(self, source: Path, mutator):
        with source.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        mutator(rows)
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".tsv", delete=False)
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        handle.close()
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return Path(handle.name)

    def test_valid_draft(self):
        validate(EVENTS, TRANSLATIONS)

    def test_rejects_identity_hash_drift(self):
        events = self._copy_with(EVENTS, lambda rows: rows[0].__setitem__("original_sha256", "0" * 64))
        with self.assertRaises(ValueError):
            validate(events, TRANSLATIONS)

    def test_rejects_non_draft_status(self):
        events = self._copy_with(EVENTS, lambda rows: rows[0].__setitem__("catalog_status", "READY"))
        with self.assertRaises(ValueError):
            validate(events, TRANSLATIONS)

    def test_rejects_translation_key_drift(self):
        translations = self._copy_with(TRANSLATIONS, lambda rows: rows[0].__setitem__("key", "story.page5.unknown"))
        with self.assertRaises(ValueError):
            validate(EVENTS, translations)

    def test_rejects_duplicate_event_key(self):
        events = self._copy_with(EVENTS, lambda rows: rows[1].__setitem__("event_key", rows[0]["event_key"]))
        with self.assertRaises(ValueError):
            validate(events, TRANSLATIONS)

    def test_rejects_control_or_format_character(self):
        translations = self._copy_with(TRANSLATIONS, lambda rows: rows[0].__setitem__("translation", rows[0]["translation"] + "\u200b"))
        with self.assertRaises(ValueError):
            validate(EVENTS, translations)

    def test_rejects_trailing_space(self):
        translations = self._copy_with(TRANSLATIONS, lambda rows: rows[0].__setitem__("translation", rows[0]["translation"] + " "))
        with self.assertRaises(ValueError):
            validate(EVENTS, translations)

    def test_conservative_mixed_advance(self):
        self.assertEqual(conservative_cells("甲A（NEO）"), 2 + 1 + 2 + 3 + 2)


if __name__ == "__main__":
    unittest.main()
