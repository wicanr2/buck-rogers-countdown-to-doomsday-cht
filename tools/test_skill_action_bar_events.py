import tempfile
import unittest
from pathlib import Path

import skill_action_bar_events


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "text" / "skill-action-bar-events.tsv"


class SkillActionBarEventsTest(unittest.TestCase):
    def test_catalog(self):
        self.assertEqual(skill_action_bar_events.validate(CATALOG), 8)

    def test_rejects_geometry_drift(self):
        text = CATALOG.read_text(encoding="utf-8").replace("\t184\t192\t216\t200", "\t184\t192\t224\t200")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.tsv"
            path.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "漂移"):
                skill_action_bar_events.validate(path)

    def test_rejects_unknown_promoted_without_evidence(self):
        text = CATALOG.read_text(encoding="utf-8").replace("\tunknown\n", "\tdisabled\n", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.tsv"
            path.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "證據分級"):
                skill_action_bar_events.validate(path)


if __name__ == "__main__":
    unittest.main()
