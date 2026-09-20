import copy
import unittest

import gender_request_receipt as subject


class GenderRequestReceiptTests(unittest.TestCase):
    def setUp(self):
        self.expected = [
            {"event_key": "gender.screen.prompt", "text_key": "gender.prompt", "translation_runes": 4},
            {"event_key": "gender.option.male", "text_key": "gender.male", "translation_runes": 2},
        ]
        self.receipt = {
            "state_start": 99_999_999,
            "stopped_at": 101_000_000,
            "bios_input": "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)",
            "events": [],
            "requests": copy.deepcopy(self.expected),
            "catalog_misses": 0,
            "bios_keys": [],
        }

    def test_accepts_exact_request_contract(self):
        subject._validate_request_contract(self.receipt, self.expected, 0)

    def test_rejects_order_key_rune_miss_and_schema_mutations(self):
        variants = []
        bad = copy.deepcopy(self.receipt); bad["requests"].reverse(); variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["requests"][0]["text_key"] = "gender.unknown"; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["requests"][0]["translation_runes"] = 0; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["catalog_misses"] = 1; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["extra"] = 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_request_contract(value, self.expected, 0)


if __name__ == "__main__":
    unittest.main()
