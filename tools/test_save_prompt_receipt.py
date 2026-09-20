import copy
import json
from pathlib import Path
import unittest

import save_prompt_receipt as subject


ROOT = Path(__file__).resolve().parents[1]


class SavePromptReceiptTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads((ROOT / "workplace/phase48/exit-a.json").read_bytes())["events"]

    def test_accepts_literal_y_noop(self):
        keys = [{"queued_at": 107_000_000, "scan": 21, "ascii": 121}]
        receipt = {"state_start": 99_999_999, "stopped_at": 113_000_000,
                   "events": copy.deepcopy(self.baseline), "bios_keys": subject.PREFIX_KEYS + keys}
        subject._validate_branch(receipt, self.baseline, [], keys)

    def test_rejects_baseline_schedule_count_schema_and_stop(self):
        keys = [{"queued_at": 107_000_000, "scan": 21, "ascii": 121}]
        exact = {"state_start": 99_999_999, "stopped_at": 113_000_000,
                 "events": copy.deepcopy(self.baseline), "bios_keys": subject.PREFIX_KEYS + keys}
        variants = []
        bad = copy.deepcopy(exact); bad["events"][0]["original_length"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["bios_keys"][-1]["scan"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(exact); bad["extra"] = 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["stopped_at"] += 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_branch(value, self.baseline, [], keys)


if __name__ == "__main__":
    unittest.main()
