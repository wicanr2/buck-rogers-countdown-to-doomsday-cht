import tempfile
import unittest
from pathlib import Path

from skill_action_bar_catalog import validate

ROOT = Path(__file__).resolve().parents[1]


class SkillActionBarCatalogTest(unittest.TestCase):
    def test_formal_catalog(self):
        self.assertEqual(validate(ROOT / "text/skill-action-bar-events.tsv", ROOT / "text/skill-action-bar.zh-TW.tsv"), (8, 5))

    def test_rejects_source_drift(self):
        source = (ROOT / "text/skill-action-bar.zh-TW.tsv").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.tsv"
            path.write_text(source.replace("runtime-interface", "manual", 1), encoding="utf-8")
            with self.assertRaises(ValueError):
                validate(ROOT / "text/skill-action-bar-events.tsv", path)


if __name__ == "__main__":
    unittest.main()
