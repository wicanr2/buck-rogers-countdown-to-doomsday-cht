from pathlib import Path
import tempfile
import unittest

import body_icon_catalog as subject

ROOT = Path(__file__).resolve().parents[1]


class BodyIconCatalogTests(unittest.TestCase):
    def validate(self, events=None, texts=None):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            event_path = base / "events.tsv"
            text_path = base / "texts.tsv"
            event_path.write_text(events or (ROOT / "text/body-icon-events.tsv").read_text(), encoding="utf-8")
            text_path.write_text(texts or (ROOT / "text/body-icon.zh-TW.tsv").read_text(), encoding="utf-8")
            subject.validate(event_path, ROOT / "text/body-icon-affixes.tsv", text_path, ROOT / "text")

    def test_accepts_exact_catalog(self):
        self.validate()

    def test_rejects_schema_identity_capacity_source_bom_and_control(self):
        events = (ROOT / "text/body-icon-events.tsv").read_text()
        texts = (ROOT / "text/body-icon.zh-TW.tsv").read_text()
        variants = [
            ("\ufeff" + events, texts),
            (events.replace("1C41:2708", "1C41:2709"), texts),
            (events, texts.replace("runtime-interface", "guess", 1)),
            (events, texts.replace("\t儲存\t", "\t儲存\x01\t")),
            (events, texts.replace("\t？\t", "\t？？？\t")),
            (events.replace("\t1\tbody.icon.confirmation", "\t2\tbody.icon.confirmation"), texts),
            (events, texts.replace("選擇身體圖示。", "選擇身體圖示。太長太長太長太長太長太長太長太長太長太長太長太長")),
            (events, "key\ttranslation\tsource\n"),
        ]
        for event_data, text_data in variants:
            with self.assertRaises(ValueError):
                self.validate(event_data, text_data)


    def test_rejects_affix_drift(self):
        good = (ROOT / "text/body-icon-affixes.tsv").read_text()
        bad_variants = [
            good.replace("\t13\t24\t", "\t15\t24\t"),
            good.replace("\t1\t15\n", "\t0\t15\n"),
            good.replace("\t1\t15\n", "\t1\t40\n"),
            good.replace("f5f25c57", "f5f25c58"),
            good + good.splitlines()[1] + "\n",
        ]
        for data in bad_variants:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "affixes.tsv"
                path.write_text(data, encoding="utf-8")
                with self.assertRaises(ValueError):
                    subject.validate(ROOT / "text/body-icon-events.tsv", path,
                                     ROOT / "text/body-icon.zh-TW.tsv", ROOT / "text")


if __name__ == "__main__":
    unittest.main()
