import copy
import unittest

import character_overlay_receipt as subject


def receipt():
    return {"tool": "dosgolem/cmd/buckrogers-overlay-prototype", "screen": "gender-steady",
            "scale": 2, "canvas_width": 640, "canvas_height": 400, "inputs_sha256": {},
            "events": [{"event_key": "e", "text_key": "t", "translation_runes": 2,
                        "background": 0, "foreground": 10,
                        "clear_rect": {"X": 0, "Y": 0, "Width": 32, "Height": 16},
                        "draw_anchor_x": 0, "draw_anchor_y": 0,
                        "ink_rect": {"X": 0, "Y": 0, "Width": 16, "Height": 16},
                        "contained": True}], "missing_glyphs": [], "diff_outside_safe_rects": 0,
            "overlapping_rects": 0, "base_png_sha256": "0" * 64, "output_png_sha256": "1" * 64}


class CharacterOverlayReceiptTests(unittest.TestCase):
    def test_accepts_exact_geometry(self):
        subject._validate_receipt(receipt(), "gender-steady", 2, 1)

    def test_rejects_schema_canvas_count_missing_overlap_outside_and_escape(self):
        variants = []
        bad = copy.deepcopy(receipt()); bad["extra"] = 1; variants.append(bad)
        bad = copy.deepcopy(receipt()); bad["canvas_width"] += 1; variants.append(bad)
        bad = copy.deepcopy(receipt()); bad["events"] = []; variants.append(bad)
        bad = copy.deepcopy(receipt()); bad["missing_glyphs"] = ["缺"]; variants.append(bad)
        bad = copy.deepcopy(receipt()); bad["overlapping_rects"] = 1; variants.append(bad)
        bad = copy.deepcopy(receipt()); bad["diff_outside_safe_rects"] = 1; variants.append(bad)
        bad = copy.deepcopy(receipt()); bad["events"][0]["ink_rect"]["Width"] = 33; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError): subject._validate_receipt(value, "gender-steady", 2, 1)


if __name__ == "__main__":
    unittest.main()
