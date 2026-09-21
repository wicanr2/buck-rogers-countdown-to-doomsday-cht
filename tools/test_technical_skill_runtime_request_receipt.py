import unittest

import technical_skill_runtime_request_receipt as subject


class TechnicalSkillRuntimeRequestReceiptTest(unittest.TestCase):
    def test_semantic_removes_only_presentation_counts(self):
        value = {"events": [1], "requests": [2], "catalog_misses": 3, "bios_keys": [4]}
        self.assertEqual(subject.semantic(value), {"events": [1], "bios_keys": [4]})

    def test_screen_keys_include_shared_career_identities(self):
        self.assertEqual(subject.SCREEN_KEYS[1], "career.screen.maximum_per_skill.heading")
        self.assertEqual(subject.SCREEN_KEYS[3], "career.screen.columns.heading")
        self.assertEqual(len(subject.SCREEN_KEYS), 18)


if __name__ == "__main__":
    unittest.main()
