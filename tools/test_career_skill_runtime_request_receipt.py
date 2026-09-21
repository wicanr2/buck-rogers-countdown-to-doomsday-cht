import unittest

import career_skill_runtime_request_receipt as subject


class CareerSkillRuntimeRequestReceiptTest(unittest.TestCase):
    def test_semantic_removes_only_catalog_output(self):
        value = {"events": [1], "requests": [2], "catalog_misses": 3, "bios_keys": [4]}
        self.assertEqual(subject.semantic(value), {"events": [1], "bios_keys": [4]})

    def test_down_suffix_is_not_part_of_base(self):
        self.assertNotIn("career.screen.skill.maneuver_zero_g.selected", subject.BASE_KEYS)
        self.assertEqual(subject.BASE_KEYS[-1], "career.screen.skill.notice.selected")


if __name__ == "__main__":
    unittest.main()
