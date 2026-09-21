from pathlib import Path
import tempfile
import unittest

import career_skill_screen_text_safe_rects as subject


ROOT = Path(__file__).resolve().parents[1]


class CareerSkillScreenTextSafeRectsTest(unittest.TestCase):
    def validate(self, rects: Path) -> None:
        subject.validate(rects, ROOT / "text/career-skill-screen-events.tsv",
                         ROOT / "text/career-skill-screen.zh-TW.tsv",
                         ROOT / "text/name-confirm-events.tsv",
                         ROOT / "text/career-skill-selection-events.tsv",
                         ROOT / "text/character-sheet.zh-TW.tsv")

    def test_formal_rects(self):
        self.validate(ROOT / "text/career-skill-screen-text-safe-rects.tsv")

    def test_rejects_dynamic_column_overlap(self):
        source = (ROOT / "text/career-skill-screen-text-safe-rects.tsv").read_text(encoding="utf-8")
        bad = source.replace("\t8\t80\t128\t8\t8\t80\t16\t", "\t8\t80\t184\t8\t8\t80\t23\t", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(path)


if __name__ == "__main__":
    unittest.main()
