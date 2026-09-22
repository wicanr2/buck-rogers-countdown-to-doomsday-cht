import unittest

from manual_rgba_verify import compare


class ManualRGBACompareTests(unittest.TestCase):
    def test_both_scales_and_boundary_pixels(self):
        for scale in (2, 3):
            baseline = bytes(320 * 200 * scale * scale * 4)
            for x, y in ((7 * scale, 72 * scale), (312 * scale - 1, 184 * scale - 1)):
                overlay = bytearray(baseline)
                overlay[(y * 320 * scale + x) * 4] = 255
                result = compare(baseline, overlay, scale, True)
                self.assertEqual(result["inside_changed_pixels"], 1)
            for x, y in ((7 * scale - 1, 72 * scale), (312 * scale, 72 * scale),
                         (7 * scale, 72 * scale - 1), (7 * scale, 184 * scale)):
                overlay = bytearray(baseline)
                overlay[(y * 320 * scale + x) * 4] = 255
                with self.assertRaises(ValueError):
                    compare(baseline, overlay, scale, True)

    def test_cleared_visible_and_invalid_lengths(self):
        baseline = bytes(640 * 400 * 4)
        self.assertEqual(compare(baseline, baseline, 2, False)["inside_changed_pixels"], 0)
        with self.assertRaises(ValueError):
            compare(baseline, baseline, 2, True)
        with self.assertRaises(ValueError):
            compare(baseline, baseline[:-1], 2, False)
        with self.assertRaises(ValueError):
            compare(baseline, baseline, 4, False)
        overlay = bytearray(baseline)
        overlay[(144 * 640 + 14) * 4] = 255
        with self.assertRaises(ValueError):
            compare(baseline, overlay, 2, False)


if __name__ == "__main__":
    unittest.main()
