import unittest

import selection_request_receipt as subject


class SelectionRequestReceiptTest(unittest.TestCase):
    def setUp(self):
        self.identity = {"event_key": "race.selection.normal.terran", "text_key": "race.terran"}
        self.translations = {"race.terran": "地球人"}

    def test_accepts_content_free_exact_request(self):
        subject._verify_request({
            "event_key": "race.selection.normal.terran",
            "text_key": "race.terran",
            "translation_runes": 3,
        }, self.identity, self.translations, 1)

    def test_rejects_key_count_and_translation_leak(self):
        requests = [
            {"event_key": "wrong", "text_key": "race.terran", "translation_runes": 3},
            {"event_key": "race.selection.normal.terran", "text_key": "wrong", "translation_runes": 3},
            {"event_key": "race.selection.normal.terran", "text_key": "race.terran", "translation_runes": 4},
            {"event_key": "race.selection.normal.terran", "text_key": "race.terran", "translation_runes": 3,
             "translation": "地球人"},
        ]
        for request in requests:
            with self.subTest(request=request):
                with self.assertRaises(ValueError):
                    subject._verify_request(request, self.identity, self.translations, 1)


if __name__ == "__main__":
    unittest.main()
