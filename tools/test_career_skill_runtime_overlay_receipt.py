import unittest

import career_skill_runtime_overlay_receipt as subject


class CareerSkillRuntimeOverlayReceiptTest(unittest.TestCase):
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
        self.assertEqual(subject.diff_counts(bytes(actual), baseline, scale, [(8, 48, 48, 8)]),
                         (1, 2, 1))


if __name__ == "__main__":
    unittest.main()
