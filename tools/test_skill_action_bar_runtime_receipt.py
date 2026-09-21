import json
import tempfile
import unittest
from pathlib import Path

import skill_action_bar_runtime_receipt as receipt


class SkillActionBarRuntimeReceiptTest(unittest.TestCase):
    def test_formal_receipts_when_present(self):
        root = Path(__file__).resolve().parents[1]
        receipts = root / "workplace" / "phase75"
        if not (receipts / "technical-done-a.json").exists():
            self.skipTest("Phase 75 local receipts are absent")
        self.assertEqual(receipt.validate(receipts, root / "text" / "skill-action-bar-events.tsv"), 8)

    def test_without_action_removes_only_watcher_fields(self):
        source = {"events": [1], "action_bar_events": [2], "action_bar_misses": 0, "action_bar_drops": 0}
        self.assertEqual(receipt.without_action(source), {"events": [1]})
        self.assertIn("action_bar_events", source)

    def test_rejects_nondeterministic_json(self):
        project = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "career-base-a.json").write_text(json.dumps({"x": 1}))
            (root / "career-base-b.json").write_text(json.dumps({"x": 2}))
            with self.assertRaisesRegex(ValueError, "A/B JSON"):
                receipt.validate(root, project / "text" / "skill-action-bar-events.tsv")


if __name__ == "__main__":
    unittest.main()
