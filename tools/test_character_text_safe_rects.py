from pathlib import Path
import tempfile
import unittest

import character_text_safe_rects as subject

ROOT = Path(__file__).resolve().parents[1]


class CharacterTextSafeRectsTests(unittest.TestCase):
    def validate(self, kind, rects=None):
        if kind == "gender":
            names = ("gender-text-safe-rects.tsv", "gender-events.tsv", "gender.zh-TW.tsv",
                     "post-race-events.tsv", "gender-selection-events.tsv")
        else:
            names = ("class-text-safe-rects.tsv", "class-events.tsv", "class.zh-TW.tsv",
                     "post-gender-events.tsv", "class-selection-events.tsv")
        if rects is None:
            subject.validate(ROOT / "text" / names[0], ROOT / "text" / names[1],
                             ROOT / "text" / names[2], kind, ROOT / "text" / names[3],
                             ROOT / "text" / names[4])
            return
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rects.tsv"; path.write_text(rects, encoding="utf-8")
            subject.validate(path, ROOT / "text" / names[1], ROOT / "text" / names[2], kind,
                             ROOT / "text" / names[3], ROOT / "text" / names[4])

    def test_accepts_gender_and_class(self):
        self.validate("gender"); self.validate("class")

    def test_rejects_bom_geometry_capacity_and_missing_key(self):
        original = (ROOT / "text/class-text-safe-rects.tsv").read_text()
        variants = ["\ufeff" + original, original.replace("\t80\t8\t", "\t88\t8\t", 1),
                    original.replace("\t10\t1\tsingle", "\t9\t1\tsingle", 1),
                    "\n".join(original.splitlines()[:-1]) + "\n"]
        for value in variants:
            with self.assertRaises(ValueError): self.validate("class", value)


if __name__ == "__main__":
    unittest.main()
