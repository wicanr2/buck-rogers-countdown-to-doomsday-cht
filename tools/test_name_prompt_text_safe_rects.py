from pathlib import Path
import tempfile
import unittest

import name_prompt_text_safe_rects as subject


ROOT = Path(__file__).resolve().parents[1]


class NamePromptTextSafeRectsTest(unittest.TestCase):
    def validate(self, rects: Path) -> None:
        subject.validate(rects, ROOT / "text/name-prompt-events.tsv",
                         ROOT / "text/name-prompt.zh-TW.tsv",
                         ROOT / "text/reroll-no-events.tsv",
                         ROOT / "text/name-edit-events.tsv")

    def test_formal_rect(self):
        self.validate(ROOT / "text/name-prompt-text-safe-rects.tsv")

    def test_rejects_rect_crossing_input(self):
        source = (ROOT / "text/name-prompt-text-safe-rects.tsv").read_text(encoding="utf-8")
        bad = source.replace("\t128\t8\t", "\t144\t8\t").replace("\t16\t1\t", "\t18\t1\t")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(path)


if __name__ == "__main__":
    unittest.main()
