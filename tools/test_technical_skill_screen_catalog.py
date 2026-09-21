from pathlib import Path
import tempfile
import unittest

import technical_skill_screen_catalog as subject


ROOT = Path(__file__).resolve().parents[1]


class TechnicalSkillScreenCatalogTest(unittest.TestCase):
    def validate(self, events: Path, translations: Path) -> None:
        subject.validate(events, translations, ROOT / "text/career-skill-exit-events.tsv",
                         ROOT / "text/technical-skill-selection-events.tsv")

    def test_formal_catalog(self):
        self.validate(ROOT / "text/technical-skill-screen-events.tsv",
                      ROOT / "text/technical-skill-screen.zh-TW.tsv")

    def test_rejects_manual_term_drift(self):
        source = (ROOT / "text/technical-skill-screen.zh-TW.tsv").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(source.replace("緊急救護", "急救", 1), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.validate(ROOT / "text/technical-skill-screen-events.tsv", path)


if __name__ == "__main__":
    unittest.main()
