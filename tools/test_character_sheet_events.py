from pathlib import Path
import tempfile
import unittest

import character_sheet_events as subject

ROOT = Path(__file__).resolve().parents[1]


class CharacterSheetEventsTests(unittest.TestCase):
    def validate(self, events=None, texts=None, inventory=None):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            event_path, text_path, inventory_path = base / "events.tsv", base / "texts.tsv", base / "inventory.tsv"
            event_path.write_text(events or (ROOT / "text/character-sheet-events.tsv").read_text(), encoding="utf-8")
            text_path.write_text(texts or (ROOT / "text/character-sheet.zh-TW.tsv").read_text(), encoding="utf-8")
            inventory_path.write_text(inventory or (ROOT / "text/post-class-events.tsv").read_text(), encoding="utf-8")
            subject.validate(event_path, text_path, inventory_path)

    def test_accepts_formal_catalog(self):
        self.validate()

    def test_rejects_drift_bad_source_missing_text_and_dynamic_identity(self):
        events = (ROOT / "text/character-sheet-events.tsv").read_text()
        texts = (ROOT / "text/character-sheet.zh-TW.tsv").read_text()
        inventory = (ROOT / "text/post-class-events.tsv").read_text()
        variants = [
            (events.replace("2368:011D", "2368:011E", 1), texts, inventory),
            (events, texts.replace("manual-and-runtime", "guess", 1), inventory),
            (events, "\n".join(texts.splitlines()[:-1]) + "\n", inventory),
            (events.replace("1ecca1ebbc092c340ce2cfd58fa6d1767d8a20c8bcad420a614d4eb1240b731f",
                            "237c59a3b965d0787ce08d5afcd4ec80017f7de4b6d84021f2207f865345f419", 1), texts, inventory),
        ]
        for event_data, text_data, inventory_data in variants:
            with self.assertRaises(ValueError):
                self.validate(event_data, text_data, inventory_data)


if __name__ == "__main__":
    unittest.main()
