import csv
import tempfile
import unittest
from pathlib import Path

from story_page4_catalog import validate


ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "text/story-page4-events.tsv"
TRANSLATIONS = ROOT / "text/story-page4.zh-TW.tsv"


class StoryPage4CatalogTest(unittest.TestCase):
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

    def test_rejects_post_call_step_drift(self):
        events = self._copy_with(EVENTS, lambda rows: rows[0].__setitem__("post_call_step", "302556030"))
        with self.assertRaises(ValueError):
            validate(events, TRANSLATIONS)

    def test_rejects_visual_transcription_evidence_level(self):
        events = self._copy_with(EVENTS, lambda rows: rows[0].__setitem__("evidence_level", "visual-transcription"))
        with self.assertRaises(ValueError):
            validate(events, TRANSLATIONS)

    def test_rejects_overlong_translation(self):
        translations = self._copy_with(TRANSLATIONS, lambda rows: rows[0].__setitem__("translation", "字" * 20))
        with self.assertRaises(ValueError):
            validate(EVENTS, translations)

    def test_rejects_translation_key_drift(self):
        translations = self._copy_with(TRANSLATIONS, lambda rows: rows[0].__setitem__("key", "story.page4.unknown"))
        with self.assertRaises(ValueError):
            validate(EVENTS, translations)


if __name__ == "__main__":
    unittest.main()
