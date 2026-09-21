import unittest

import name_prompt_transition_overlay_receipt as subject


class NamePromptTransitionOverlayReceiptTest(unittest.TestCase):
    def test_expected_branches_are_locked(self):
        self.assertIn("confirm_control", subject.EXPECTED)
        self.assertIn("escape_control", subject.EXPECTED)
        self.assertNotEqual(subject.EXPECTED["confirm_fb"], subject.EXPECTED["escape_fb"])

    def test_projection_contract_covers_all_presentation_fields(self):
        self.assertIn("overlay_drew", subject.OVERLAY_FIELDS)
        self.assertIn("active_overlay_keys", subject.OVERLAY_FIELDS)


if __name__ == "__main__":
    unittest.main()
