import tempfile
import unittest
from pathlib import Path

import manual_overlay_layout as subject


ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "text/manual-overlay-layout.tsv"
CATALOG = ROOT / "text/manual.zh-TW.tsv"


class ManualOverlayLayoutTest(unittest.TestCase):
    def test_formal_layout_and_catalog(self):
        self.assertEqual(subject.validate(LAYOUT, CATALOG), 31)

    def test_rejects_geometry_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            layout = Path(directory) / "layout.tsv"
            layout.write_text(LAYOUT.read_text(encoding="utf-8").replace("\t72\t305\t112", "\t71\t305\t112", 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "clear_y"):
                subject.validate(layout, CATALOG)

    def test_rejects_schema_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            layout = Path(directory) / "layout.tsv"
            layout.write_text(
                LAYOUT.read_text(encoding="utf-8").replace("overflow_policy", "overflow", 1),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "固定 schema"):
                subject.validate(layout, CATALOG)

    def test_rejects_505_character_paragraph(self):
        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / "catalog.tsv"
            catalog.write_text(
                "key\ttranslation\tsource\nmanual.log.11.the_elevator\t" + "字" * 505 + "\tmanual-and-runtime\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "505 字，超過單頁上限 504 字"):
                subject.validate(LAYOUT, catalog)

    def test_accepts_504_character_paragraph(self):
        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / "catalog.tsv"
            catalog.write_text(
                "key\ttranslation\tsource\nmanual.log.11.the_elevator\t" + "字" * 504 + "\tmanual-and-runtime\n",
                encoding="utf-8",
            )
            self.assertEqual(subject.validate(LAYOUT, catalog), 1)


if __name__ == "__main__":
    unittest.main()
