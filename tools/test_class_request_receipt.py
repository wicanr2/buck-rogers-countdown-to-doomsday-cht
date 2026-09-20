import copy
import unittest

import class_request_receipt as subject


class ClassRequestReceiptTests(unittest.TestCase):
    def test_accepts_exact_request_contract(self):
        receipt = {"state_start": 1, "stopped_at": 2, "bios_input": "x", "events": [],
                   "requests": [{"event_key": "e", "text_key": "t", "translation_runes": 2}],
                   "catalog_misses": 0, "bios_keys": []}
        subject._validate_requests(receipt, receipt["requests"], 0)

    def test_rejects_schema_sequence_miss_and_empty_translation(self):
        base = {"state_start": 1, "stopped_at": 2, "bios_input": "x", "events": [],
                "requests": [{"event_key": "e", "text_key": "t", "translation_runes": 2}],
                "catalog_misses": 0, "bios_keys": []}
        variants = []
        bad = copy.deepcopy(base); bad["extra"] = 1; variants.append((bad, base["requests"], 0))
        bad = copy.deepcopy(base); bad["catalog_misses"] = 1; variants.append((bad, base["requests"], 0))
        bad = copy.deepcopy(base); bad["requests"][0]["event_key"] = "wrong"; variants.append((bad, base["requests"], 0))
        bad = copy.deepcopy(base); bad["requests"][0]["translation_runes"] = 0; variants.append((bad, bad["requests"], 0))
        for receipt, expected, misses in variants:
            with self.assertRaises(ValueError): subject._validate_requests(receipt, expected, misses)


if __name__ == "__main__":
    unittest.main()
