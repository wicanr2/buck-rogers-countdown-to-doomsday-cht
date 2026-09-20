from copy import deepcopy
import unittest

import selection_blink_receipt as subject


def sample(step: int, row3: str, row4: str, events: int) -> dict:
    return {
        "step": step,
        "palette_sha256": "a" * 64,
        "palette": {
            "0": {"r": 0, "g": 0, "b": 0},
            "10": {"r": 85, "g": 255, "b": 85},
            "13": {"r": 255, "g": 85, "b": 255},
            "15": {"r": 0, "g": 0, "b": 0},
        },
        "selected_contrast": False,
        "row3": {"sha256": row3, "counts": {"0": 1}},
        "row4": {"sha256": row4, "counts": {"0": 1}},
        "completed_events": events,
    }


def receipt(mode: str) -> dict:
    samples = []
    for step in range(100_220_000, 110_000_000, 10_000):
        if mode == "steady":
            r3 = subject.NORMAL_TERRAN if step == 100_220_000 else subject.SELECTED_TERRAN
            r4, events = subject.NORMAL_MARTIAN, 8 if step == 100_220_000 else 9
        else:
            if step < 100_230_000:
                r3, r4, events = subject.NORMAL_TERRAN, subject.NORMAL_MARTIAN, 8
            elif step < 100_260_000:
                r3, r4, events = subject.SELECTED_TERRAN, subject.NORMAL_MARTIAN, 9
            else:
                r3, r4, events = subject.NORMAL_TERRAN, subject.SELECTED_MARTIAN, 11
        samples.append(sample(step, r3, r4, events))
    return {
        "tool": "dosgolem/cmd/buckrogers-selection-blink-receipt",
        "state_sha256": "cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164",
        "menu_events_sha256": "973a6a1e247e7d9e16518a1a66266f340666d32e785f3f6f6652a890e830da2e",
        "state_start": 99_999_999, "stopped_at": 110_000_000,
        "enter_at": 100_010_000, "down_at": 0 if mode == "steady" else 100_240_000,
        "sample_from": 100_220_000, "sample_every": 10_000,
        "samples": samples, "events": [{}] * (9 if mode == "steady" else 11),
        "pending": False, "drops": 0,
    }


class SelectionBlinkReceiptTest(unittest.TestCase):
    def test_accepts_steady_and_down_sample_contract(self):
        subject._validate_samples(receipt("steady"), "steady")
        subject._validate_samples(receipt("down"), "down")

    def test_rejects_palette_contrast_or_late_pixel_change(self):
        cases = []
        contrasted = receipt("steady")
        contrasted["samples"][4]["palette"]["15"] = {"r": 255, "g": 255, "b": 255}
        contrasted["samples"][4]["selected_contrast"] = True
        cases.append(contrasted)
        changed = receipt("down")
        changed["samples"][-1]["row4"]["sha256"] = "f" * 64
        cases.append(changed)
        for value in cases:
            with self.subTest():
                with self.assertRaises(ValueError):
                    subject._validate_samples(value, "steady" if value["down_at"] == 0 else "down")

    def test_rejects_sample_gap(self):
        value = receipt("steady")
        del value["samples"][10]
        with self.assertRaises(ValueError):
            subject._validate_samples(value, "steady")


if __name__ == "__main__":
    unittest.main()
