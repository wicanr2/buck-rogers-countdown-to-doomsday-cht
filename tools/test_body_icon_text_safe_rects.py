from pathlib import Path
import tempfile
import unittest

import body_icon_text_safe_rects as subject

ROOT = Path(__file__).resolve().parents[1]


class BodyIconTextSafeRectTests(unittest.TestCase):
    def validate(self, rects=None, events=None, texts=None):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            rect_path, event_path, text_path = base / "rects.tsv", base / "events.tsv", base / "texts.tsv"
            rect_path.write_text(rects or (ROOT / "text/body-icon-text-safe-rects.tsv").read_text(), encoding="utf-8")
            event_path.write_text(events or (ROOT / "text/body-icon-events.tsv").read_text(), encoding="utf-8")
            text_path.write_text(texts or (ROOT / "text/body-icon.zh-TW.tsv").read_text(), encoding="utf-8")
            subject.validate(rect_path, event_path, ROOT / "text/body-icon-affixes.tsv", text_path, ROOT / "text")

    def test_accepts_exact_rectangles(self):
        self.validate()

    def test_rejects_schema_geometry_overlap_capacity_and_bom(self):
        rects = (ROOT / "text/body-icon-text-safe-rects.tsv").read_text()
        events = (ROOT / "text/body-icon-events.tsv").read_text()
        texts = (ROOT / "text/body-icon.zh-TW.tsv").read_text()
        variants = [
            ("\ufeff" + rects, events, texts),
            (rects.replace("64\t48\t24", "64\t48\t32", 1), events, texts),
            (rects.replace("save_prompt\tbody.icon.save_prompt.prefix", "confirmation\tbody.icon.save_prompt.prefix"), events, texts),
            (rects.replace("0\t192\t40\t8\t0\t192\t5", "0\t192\t64\t8\t0\t192\t8"), events, texts),
            (rects.replace("17\t1\tsingle-line-reject", "1\t1\tsingle-line-reject", 1), events, texts),
            (rects.replace("single-line-reject", "clip", 1), events, texts),
        ]
        for rect_data, event_data, text_data in variants:
            with self.assertRaises(ValueError):
                self.validate(rect_data, event_data, text_data)


if __name__ == "__main__":
    unittest.main()
