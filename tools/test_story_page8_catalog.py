import csv
import tempfile
import unittest
from pathlib import Path

from story_page8_catalog import half_units, validate

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "text/story-page8-events.tsv"
TRANSLATIONS = ROOT / "text/story-page8.zh-TW.tsv"


class StoryPage8CatalogTest(unittest.TestCase):
    def _copy_with(self, source, mutator):
        with source.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        mutator(rows)
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".tsv", delete=False)
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows); handle.close()
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return Path(handle.name)

    def test_valid_ready(self):
        validate(EVENTS, TRANSLATIONS)

    def test_rejects_draft_status(self):
        events = self._copy_with(EVENTS, lambda rows: rows[0].__setitem__("catalog_status", "DRAFT"))
        with self.assertRaises(ValueError): validate(events, TRANSLATIONS)

    def test_rejects_hash_drift(self):
        events = self._copy_with(EVENTS, lambda rows: rows[0].__setitem__("original_sha256", "0" * 64))
        with self.assertRaises(ValueError): validate(events, TRANSLATIONS)

    def test_rejects_key_drift(self):
        translations = self._copy_with(TRANSLATIONS, lambda rows: rows[0].__setitem__("key", "story.page8.unknown"))
        with self.assertRaises(ValueError): validate(EVENTS, translations)

    def test_rejects_control_character(self):
        translations = self._copy_with(TRANSLATIONS, lambda rows: rows[0].__setitem__("translation", rows[0]["translation"] + "\u200b"))
        with self.assertRaises(ValueError): validate(EVENTS, translations)

    def test_conservative_mixed_advance(self):
        self.assertEqual(half_units("甲A（NEO）"), 2 + 1 + 2 + 3 + 2)


if __name__ == "__main__":
    unittest.main()
