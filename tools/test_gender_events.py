from pathlib import Path
import tempfile
import unittest

import gender_events


ROOT = Path(__file__).resolve().parents[1]


class GenderEventsTests(unittest.TestCase):
    def setUp(self):
        self.events = (ROOT / "text/gender-events.tsv").read_text(encoding="utf-8")
        self.texts = (ROOT / "text/gender.zh-TW.tsv").read_text(encoding="utf-8")

    def validate(self, events=None, texts=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event_path, text_path = root / "events.tsv", root / "texts.tsv"
            event_path.write_text(self.events if events is None else events, encoding="utf-8")
            text_path.write_text(self.texts if texts is None else texts, encoding="utf-8")
            gender_events.validate(event_path, text_path, ROOT / "text/post-race-events.tsv",
                                   ROOT / "text/gender-selection-events.tsv")

    def test_formal_catalog_matches_both_evidence_tables(self):
        self.validate()

    def test_rejects_schema_sequence_duplicate_identity_missing_translation_and_evidence_drift(self):
        variants = [
            (self.events.replace("event_key\tsequence", "sequence\tevent_key", 1), self.texts),
            (self.events.replace("\t7\tgender.female", "\t8\tgender.female", 1), self.texts),
            (self.events.replace("gender.selection.normal.female", "gender.selection.selected.female", 1), self.texts),
            (self.events, "\n".join(self.texts.splitlines()[:-1]) + "\n"),
            (self.events.replace("37F1:1856", "37F1:1857", 1), self.texts),
        ]
        for events, texts in variants:
            with self.assertRaises(ValueError):
                self.validate(events, texts)

    def test_rejects_bom_and_unknown_source(self):
        with self.assertRaises(ValueError):
            self.validate("\ufeff" + self.events, self.texts)
        with self.assertRaises(ValueError):
            self.validate(self.events, self.texts.replace("runtime-interface", "guess", 1))


if __name__ == "__main__":
    unittest.main()
