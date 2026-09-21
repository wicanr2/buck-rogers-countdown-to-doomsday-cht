import unittest

import name_prompt_runtime_overlay_receipt as subject


class NamePromptRuntimeOverlayReceiptTest(unittest.TestCase):
    def test_project_removes_only_presentation_fields(self):
        value = {"events": [1], "overlay_scale": 2, "overlay_drew": True,
                 "active_overlay_keys": ["x"], "overlay_actions": [1]}
        self.assertEqual(subject.project(value), {"events": [1]})

    def test_diff_counts_rejects_outside_and_input_column(self):
        scale = 2
        baseline = bytes(320 * scale * 200 * scale * 4)
        actual = bytearray(baseline)
        inside = ((192 * scale) * 320 * scale) * 4
        input_at = ((192 * scale) * 320 * scale + 136 * scale) * 4
        actual[inside] = 1
        actual[input_at] = 1
        self.assertEqual(subject.diff_counts(bytes(actual), baseline, scale), (1, 1, 1))


if __name__ == "__main__":
    unittest.main()
