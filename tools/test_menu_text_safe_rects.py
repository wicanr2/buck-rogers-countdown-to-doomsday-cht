from pathlib import Path
import tempfile
import unittest

import menu_text_safe_rects as subject


class MenuTextSafeRectsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.events = root / "events.tsv"
        self.catalog = root / "catalog.tsv"
        self.rects = root / "rects.tsv"
        self.events.write_text(
            "event_key\tsequence\ttext_key\toriginal_length\toriginal_sha256\tcaller\tbackground\tforeground\trow\tcolumn\n"
            "race.option.terran\t1\trace.terran\t8\t"
            "28f962ee4f76bcaea2e7d195fccb11782ecb4aea3c8f78e342118d69968e5d69\t"
            "37F1:15BD\t0\t10\t3\t1\n",
            encoding="utf-8",
        )
        self.catalog.write_text("key\ttranslation\tsource\nrace.terran\t地球人\truntime\n", encoding="utf-8")
        self.good = (
            "event_key\tx\ty\twidth\theight\tdraw_x\tdraw_y\tcapacity_cells\tline_count\toverflow_policy\n"
            "race.option.terran\t8\t24\t64\t8\t24\t24\t6\t1\tsingle-line-reject\n"
        )
        self.rects.write_text(self.good, encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_exact_original_rect_and_inset_anchor(self):
        subject.validate(self.rects, self.events, self.catalog)

    def test_rejects_geometry_capacity_policy_and_missing_key(self):
        mutations = [
            ("x", "\t8\t24\t64\t", "\t16\t24\t64\t"),
            ("height", "\t64\t8\t24\t", "\t64\t16\t24\t"),
            ("anchor", "\t8\t24\t64\t8\t24\t24\t", "\t8\t24\t64\t8\t8\t24\t"),
            ("capacity", "\t6\t1\t", "\t5\t1\t"),
            ("policy", "single-line-reject", "clip"),
            ("key", "race.option.terran", "race.option.unknown"),
        ]
        for name, old, new in mutations:
            with self.subTest(name=name):
                self.rects.write_text(self.good.replace(old, new), encoding="utf-8")
                with self.assertRaises(ValueError):
                    subject.validate(self.rects, self.events, self.catalog)

    def test_rejects_translation_overflow(self):
        self.catalog.write_text("key\ttranslation\tsource\nrace.terran\t一二三四五六七\truntime\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            subject.validate(self.rects, self.events, self.catalog)


if __name__ == "__main__":
    unittest.main()
