from pathlib import Path
import tempfile
import unittest

import class_events as subject

ROOT = Path(__file__).resolve().parents[1]


class ClassEventsTests(unittest.TestCase):
    def validate(self, events=None, texts=None):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            event_path, text_path = base / "events.tsv", base / "texts.tsv"
            event_path.write_text(events or (ROOT / "text/class-events.tsv").read_text(), encoding="utf-8")
            text_path.write_text(texts or (ROOT / "text/class.zh-TW.tsv").read_text(), encoding="utf-8")
            subject.validate(event_path, text_path, ROOT / "text/post-gender-events.tsv", ROOT / "text/class-selection-events.tsv")

    def test_accepts_formal_catalog(self):
        self.validate()

    def test_rejects_malformed_or_cross_evidence_drift(self):
        events = (ROOT / "text/class-events.tsv").read_text()
        texts = (ROOT / "text/class.zh-TW.tsv").read_text()
        variants = [("\ufeff" + events, texts), (events.replace("37F1:1856", "37F1:1857", 1), texts),
                    (events.replace("class.selection.normal.medic", "class.selection.selected.medic", 1), texts),
                    (events, texts.replace("manual-and-runtime", "guess", 1)),
                    (events, "\n".join(texts.splitlines()[:-1]) + "\n")]
        for event_data, text_data in variants:
            with self.assertRaises(ValueError):
                self.validate(event_data, text_data)


if __name__ == "__main__":
    unittest.main()
