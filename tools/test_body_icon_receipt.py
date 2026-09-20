import copy
import json
from pathlib import Path
import unittest

import body_icon_receipt as subject
import reroll_lifecycle_receipt


ROOT = Path(__file__).resolve().parents[1]


class BodyIconReceiptTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads((ROOT / "workplace/phase47/exit-a.json").read_bytes())["events"]
        self.move = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/body-icon-move-events.tsv", 1, subject.MOVE_ROLES)

    @staticmethod
    def event(row):
        segment, offset = (int(value, 16) for value in row["caller"].split(":"))
        return {"entry_step": int(row["entry_step"]), "post_call_step": int(row["post_call_step"]),
                "caller": {"segment": segment, "offset": offset},
                "original_length": int(row["original_length"]), "original_sha256": row["original_sha256"],
                "background": int(row["background"]), "foreground": int(row["foreground"]),
                "row": int(row["row"]), "column": int(row["column"])}

    def test_accepts_exact_move(self):
        keys = [{"queued_at": 106_000_000, "scan": 77, "ascii": 0}]
        receipt = {"state_start": 99_999_999, "stopped_at": 108_000_000,
                   "events": copy.deepcopy(self.baseline) + [self.event(self.move[0])],
                   "bios_keys": subject.PREFIX_KEYS + keys}
        subject._validate_branch(receipt, self.baseline, self.move, keys, 108_000_000)

    def test_rejects_identity_step_schedule_count_schema_and_stop(self):
        keys = [{"queued_at": 106_000_000, "scan": 77, "ascii": 0}]
        exact = {"state_start": 99_999_999, "stopped_at": 108_000_000,
                 "events": copy.deepcopy(self.baseline) + [self.event(self.move[0])],
                 "bios_keys": subject.PREFIX_KEYS + keys}
        variants = []
        bad = copy.deepcopy(exact); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["bios_keys"][-1]["scan"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(exact); bad["extra"] = 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["stopped_at"] += 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_branch(value, self.baseline, self.move, keys, 108_000_000)


if __name__ == "__main__":
    unittest.main()
