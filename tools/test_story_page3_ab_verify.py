import hashlib
import unittest

from story_page3_ab_verify import pixels, verify


class StoryPage3ABVerifyTest(unittest.TestCase):
    def test_visible_and_cleared_at_both_scales(self):
        for scale in (2, 3):
            with self.subTest(scale=scale):
                baseline = bytearray(320 * scale * 200 * scale * 4)
                overlay = bytearray(baseline)
                pos = ((136 * scale) * 320 * scale + 8 * scale) * 4
                overlay[pos] = 255
                control = {"state_start": 1, "memory_sha256": "same"}
                info = {"scale": scale, "drew": True,
                        "active_keys": [f"story.page3.line.{n:03d}" for n in range(1, 6)],
                        "missing_glyphs": None, "diff_inside_story_rect": 1,
                        "diff_outside_story_rect": 0,
                        "baseline_rgba_sha256": hashlib.sha256(baseline).hexdigest(),
                        "overlay_rgba_sha256": hashlib.sha256(overlay).hexdigest()}
                receipt = dict(control, story_page3_overlay=info)
                self.assertEqual(verify(control, receipt, baseline, overlay, scale, True)["inside_changed_pixels"], 1)
                receipt["story_page3_overlay"] = dict(info, drew=False, active_keys=[],
                                                       diff_inside_story_rect=0,
                                                       overlay_rgba_sha256=hashlib.sha256(baseline).hexdigest())
                receipt["story_page3_invalidations"] = [{"instruction": {"segment": 0x0cf4, "offset": 0x1b3a},
                                                          "video_segment": 0xa000, "active_keys_before": 5}]
                self.assertEqual(verify(control, receipt, baseline, baseline, scale, False)["inside_changed_pixels"], 0)

    def test_outside_or_original_state_change_fails(self):
        baseline = bytearray(640 * 400 * 4)
        overlay = bytearray(baseline)
        overlay[0] = 255
        self.assertEqual(pixels(baseline, overlay, 2), (0, 1))
        control = {"memory_sha256": "same"}
        receipt = {"memory_sha256": "changed", "story_page3_overlay": {}}
        with self.assertRaises(ValueError):
            verify(control, receipt, baseline, baseline, 2, False)


if __name__ == "__main__":
    unittest.main()
