import unittest

import character_runtime_overlay_receipt as subject


class CharacterRuntimeOverlayReceiptTest(unittest.TestCase):
    def test_projection_removes_only_presentation_fields(self):
        receipt = {"events": [1], "requests": [2], "overlay_scale": 2,
                   "overlay_actions": [2], "overlay_drew": True}
        self.assertEqual(subject._project(receipt), {"events": [1], "requests": [2]})

    def test_outside_diff_classifies_pixels(self):
        baseline = bytes(4 * 4 * 2)
        actual = bytearray(baseline)
        actual[(0 * 4 + 1) * 4] = 1
        actual[(1 * 4 + 3) * 4] = 1
        self.assertEqual(subject._outside_diff(bytes(actual), baseline, 4, [(1, 0, 1, 1)]), (1, 1))


if __name__ == "__main__":
    unittest.main()
