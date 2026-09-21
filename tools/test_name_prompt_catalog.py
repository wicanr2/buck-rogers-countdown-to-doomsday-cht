from pathlib import Path
import tempfile
import unittest

import name_prompt_catalog as subject

ROOT = Path(__file__).resolve().parents[1]


class NamePromptCatalogTests(unittest.TestCase):
    def validate(self, events=None, texts=None, inventory=None):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            event_path, text_path, inventory_path = base / "events.tsv", base / "texts.tsv", base / "inventory.tsv"
            event_path.write_text(events or (ROOT / "text/name-prompt-events.tsv").read_text(), encoding="utf-8")
            text_path.write_text(texts or (ROOT / "text/name-prompt.zh-TW.tsv").read_text(), encoding="utf-8")
            inventory_path.write_text(inventory or (ROOT / "text/reroll-no-events.tsv").read_text(), encoding="utf-8")
            subject.validate(event_path, text_path, inventory_path)

    def test_accepts_exact_prompt(self):
        self.validate()

    def test_rejects_schema_identity_source_control_nfc_and_missing_rows(self):
        events = (ROOT / "text/name-prompt-events.tsv").read_text()
        texts = (ROOT / "text/name-prompt.zh-TW.tsv").read_text()
        inventory = (ROOT / "text/reroll-no-events.tsv").read_text()
        variants = [
            ("\ufeff" + events, texts, inventory),
            (events.replace("0763:0826", "0763:0827"), texts, inventory),
            (events, texts.replace("runtime-interface", "guess"), inventory),
            (events, texts.replace("角色姓名：", "角色\x01姓名："), inventory),
            (events, texts.replace("角色姓名：", "e\u0301"), inventory),
            (events, "key\ttranslation\tsource\n", inventory),
            (events, texts, "\n".join(inventory.splitlines()[:-1]) + "\n"),
        ]
        for event_data, text_data, inventory_data in variants:
            with self.assertRaises(ValueError):
                self.validate(event_data, text_data, inventory_data)


if __name__ == "__main__":
    unittest.main()
