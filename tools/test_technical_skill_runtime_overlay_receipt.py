import unittest

import technical_skill_runtime_overlay_receipt as subject


class TechnicalSkillRuntimeOverlayReceiptTest(unittest.TestCase):
    def test_project_removes_only_presentation_fields(self):
        value = {"events": [1], "overlay_scale": 2, "overlay_drew": True,
                 "active_overlay_keys": ["x"], "overlay_actions": [1]}
        self.assertEqual(subject.project(value), {"events": [1]})

    def test_diff_counts_separates_authorized_outside_and_dynamic(self):
        scale = 2
        baseline = bytes(320 * scale * 200 * scale * 4)
        actual = bytearray(baseline)
        for x, y in ((8, 48), (180, 48), (184, 48)):
            actual[(y * scale * 320 * scale + x * scale) * 4] = 1
        self.assertEqual(subject.diff_counts(bytes(actual), baseline, scale, [(8, 48, 136, 8)]),
                         (1, 2, 1))

    def test_expected_active_replaces_selected_row(self):
        base = subject.expected_active("base")
        down = subject.expected_active("down")
        self.assertIn("technical.screen.skill.repair_electrical.selected", base)
        self.assertNotIn("technical.screen.skill.repair_electrical.normal", base)
        self.assertIn("technical.screen.skill.repair_mechanical.selected", down)
        self.assertNotIn("technical.screen.skill.repair_mechanical.normal", down)


if __name__ == "__main__":
    unittest.main()
