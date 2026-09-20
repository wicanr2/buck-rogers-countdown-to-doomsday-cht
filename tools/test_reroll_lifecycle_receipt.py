import copy
import json
from pathlib import Path
import tempfile
import unittest

import reroll_lifecycle_receipt as subject


ROOT = Path(__file__).resolve().parents[1]


class RerollLifecycleReceiptTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads((ROOT / "workplace/phase42/fourth-enter-b.json").read_bytes())["events"]
        self.yes_rows = subject._read_inventory(ROOT / "text/reroll-yes-events.tsv", 31, subject.YES_ROLES)
        self.no_rows = subject._read_inventory(ROOT / "text/reroll-no-events.tsv", 65, subject.NO_ROLES)

    @staticmethod
    def event(row):
        segment, offset = (int(value, 16) for value in row["caller"].split(":"))
        return {"entry_step": int(row["entry_step"]), "post_call_step": int(row["post_call_step"]),
                "caller": {"segment": segment, "offset": offset},
                "original_length": int(row["original_length"]), "original_sha256": row["original_sha256"],
                "background": int(row["background"]), "foreground": int(row["foreground"]),
                "row": int(row["row"]), "column": int(row["column"])}

    def receipt(self, rows, key):
        return {"state_start": 99_999_999, "stopped_at": 102_000_000,
                "events": copy.deepcopy(self.baseline) + [self.event(row) for row in rows],
                "bios_keys": subject.PREFIX_KEYS + [key]}

    def test_accepts_exact_yes_and_no_branches(self):
        subject._validate_branch(self.receipt(self.yes_rows, {"queued_at": 101_400_000, "scan": 21, "ascii": 121}),
                                 self.baseline, self.yes_rows,
                                 {"queued_at": 101_400_000, "scan": 21, "ascii": 121})
        subject._validate_branch(self.receipt(self.no_rows, {"queued_at": 101_400_000, "scan": 49, "ascii": 110}),
                                 self.baseline, self.no_rows,
                                 {"queued_at": 101_400_000, "scan": 49, "ascii": 110})

    def test_rejects_baseline_identity_step_schedule_count_and_schema(self):
        exact = self.receipt(self.yes_rows, {"queued_at": 101_400_000, "scan": 21, "ascii": 121})
        variants = []
        bad = copy.deepcopy(exact); bad["events"][0]["original_length"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["bios_keys"][-1]["ascii"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(exact); bad["extra"] = 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_branch(value, self.baseline, self.yes_rows,
                                         {"queued_at": 101_400_000, "scan": 21, "ascii": 121})

    def test_inventory_rejects_bom_duplicate_role_step_and_missing_row(self):
        original = (ROOT / "text/reroll-yes-events.tsv").read_text(encoding="utf-8")
        first, second = original.splitlines()[1:3]
        variants = ["\ufeff" + original,
                    original.replace(second.split("\t")[0], first.split("\t")[0], 1),
                    original.replace("\tconfirmed\t", "\thypothesis\t", 1),
                    original.replace("\tability_rerolled_value\t", "\tunknown_role\t", 1),
                    original.replace(first.split("\t")[4], first.split("\t")[5], 1),
                    "\n".join(original.splitlines()[:-1]) + "\n"]
        for value in variants:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "events.tsv"
                path.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    subject._read_inventory(path, 31, subject.YES_ROLES)


if __name__ == "__main__":
    unittest.main()
