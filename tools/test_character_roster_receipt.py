import copy
import json
from pathlib import Path
import unittest

import character_roster_receipt as subject
import reroll_lifecycle_receipt
import save_prompt_receipt


ROOT = Path(__file__).resolve().parents[1]


class CharacterRosterReceiptTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads((ROOT / "workplace/phase49/no-a.json").read_bytes())["events"]
        self.rows = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/character-roster-no-events.tsv", 11, subject.ROLES)

    def test_accepts_exact_no_branch(self):
        prefix = save_prompt_receipt.PREFIX_KEYS + [{"queued_at": 107_000_000, "scan": 49, "ascii": 110}]
        receipt = json.loads((ROOT / "workplace/phase50/no-a.json").read_bytes())
        subject._validate_branch(receipt, self.baseline, prefix, self.rows)

    def test_rejects_event_schedule_schema_scratch_and_stop(self):
        prefix = save_prompt_receipt.PREFIX_KEYS + [{"queued_at": 107_000_000, "scan": 49, "ascii": 110}]
        exact = json.loads((ROOT / "workplace/phase50/no-a.json").read_bytes())
        variants = []
        bad = copy.deepcopy(exact); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["bios_keys"][-1]["scan"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(exact); bad["extra"] = 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["scratch"] = "/wrong"; variants.append(bad)
        bad = copy.deepcopy(exact); bad["stopped_at"] += 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_branch(value, self.baseline, prefix, self.rows)


if __name__ == "__main__":
    unittest.main()
