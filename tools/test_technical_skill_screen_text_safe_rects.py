from pathlib import Path
import tempfile
import unittest

import technical_skill_screen_text_safe_rects as subject


ROOT = Path(__file__).resolve().parents[1]


class TechnicalSkillScreenTextSafeRectsTest(unittest.TestCase):
    def validate(self, rects: Path) -> None:
        subject.validate(rects, ROOT / "text/technical-skill-screen-events.tsv",
                         ROOT / "text/technical-skill-screen.zh-TW.tsv",
                         ROOT / "text/career-skill-exit-events.tsv",
                         ROOT / "text/technical-skill-selection-events.tsv")

    def test_formal_rects(self):
        self.validate(ROOT / "text/technical-skill-screen-text-safe-rects.tsv")

    def test_rejects_dynamic_column_overlap(self):
        source = (ROOT / "text/technical-skill-screen-text-safe-rects.tsv").read_text(encoding="utf-8")
        bad = source.replace("\t8\t64\t168\t8\t8\t64\t21\t", "\t8\t64\t184\t8\t8\t64\t23\t", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(path)


if __name__ == "__main__":
    unittest.main()
