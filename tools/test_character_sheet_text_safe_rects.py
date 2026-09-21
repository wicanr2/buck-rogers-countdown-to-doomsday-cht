from pathlib import Path
import tempfile
import unittest

import character_sheet_text_safe_rects as subject

ROOT = Path(__file__).resolve().parents[1]


class CharacterSheetTextSafeRectsTests(unittest.TestCase):
    def validate(self, rects=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rects.tsv"
            path.write_text(rects or (ROOT / "text/character-sheet-text-safe-rects.tsv").read_text(), encoding="utf-8")
            subject.validate(path, ROOT / "text/character-sheet-events.tsv",
                             ROOT / "text/character-sheet.zh-TW.tsv", ROOT / "text/post-class-events.tsv")

    def test_accepts_formal_rects(self):
        self.validate()

    def test_rejects_dynamic_overlap_capacity_policy_and_missing_key(self):
        good = (ROOT / "text/character-sheet-text-safe-rects.tsv").read_text()
        variants = [
            good.replace("character.sheet.label.ac\t224\t16\t56", "character.sheet.label.ac\t224\t16\t64", 1),
            good.replace("character.sheet.label.hp\t224\t8\t24", "character.sheet.label.hp\t224\t8\t32", 1),
            good.replace("character.sheet.label.name\t8\t8\t56\t8\t8\t8\t7", "character.sheet.label.name\t8\t8\t56\t8\t8\t8\t6", 1),
            good.replace("single-line-reject", "clip", 1),
            "\n".join(good.splitlines()[:-1]) + "\n",
        ]
        for data in variants:
            with self.assertRaises(ValueError):
                self.validate(data)


if __name__ == "__main__":
    unittest.main()
