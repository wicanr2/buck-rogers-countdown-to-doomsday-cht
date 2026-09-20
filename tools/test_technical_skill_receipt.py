import copy
import json
from pathlib import Path
import tempfile
import unittest

import reroll_lifecycle_receipt
import technical_skill_receipt as subject


ROOT = Path(__file__).resolve().parents[1]


class TechnicalSkillReceiptTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads((ROOT / "workplace/phase46/exit-a.json").read_bytes())["events"]
        self.down = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/technical-skill-selection-events.tsv", 8, subject.DOWN_ROLES)
        self.subtract = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/technical-skill-subtract-events.tsv", 10, subject.SUBTRACT_ROLES)
        self.refusal = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/technical-skill-refusal-events.tsv", 1, subject.REFUSAL_ROLES)
        self.exit = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/technical-skill-exit-events.tsv", 7, subject.EXIT_ROLES)

    @staticmethod
    def event(row):
        segment, offset = (int(value, 16) for value in row["caller"].split(":"))
        return {"entry_step": int(row["entry_step"]), "post_call_step": int(row["post_call_step"]),
                "caller": {"segment": segment, "offset": offset},
                "original_length": int(row["original_length"]), "original_sha256": row["original_sha256"],
                "background": int(row["background"]), "foreground": int(row["foreground"]),
                "row": int(row["row"]), "column": int(row["column"])}

    def receipt(self, rows, keys, stopped_at):
        return {"state_start": 99_999_999, "stopped_at": stopped_at,
                "events": copy.deepcopy(self.baseline) + [self.event(row) for row in rows],
                "bios_keys": subject.PREFIX_KEYS + keys}

    def test_accepts_all_four_branches(self):
        cases = [
            (self.down, [{"queued_at": 103_600_000, "scan": 80, "ascii": 0}], 105_000_000),
            (self.subtract, [{"queued_at": 103_600_000, "scan": 28, "ascii": 13},
                             {"queued_at": 103_700_000, "scan": 77, "ascii": 0},
                             {"queued_at": 103_800_000, "scan": 28, "ascii": 13}], 105_000_000),
            (self.refusal, [{"queued_at": 103_600_000, "scan": 1, "ascii": 27},
                            {"queued_at": 103_800_000, "scan": 49, "ascii": 110}], 106_000_000),
            (self.exit, [{"queued_at": 103_600_000, "scan": 1, "ascii": 27},
                         {"queued_at": 103_800_000, "scan": 21, "ascii": 121}], 106_000_000),
        ]
        for rows, keys, stop in cases:
            subject._validate_branch(self.receipt(rows, keys, stop), self.baseline, rows, keys, stop)

    def test_rejects_baseline_identity_step_schedule_count_schema_and_stop(self):
        keys = [{"queued_at": 103_600_000, "scan": 80, "ascii": 0}]
        exact = self.receipt(self.down, keys, 105_000_000)
        variants = []
        bad = copy.deepcopy(exact); bad["events"][0]["original_length"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["bios_keys"][-1]["scan"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(exact); bad["extra"] = 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["stopped_at"] += 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_branch(value, self.baseline, self.down, keys, 105_000_000)

    def test_inventory_rejects_bom_duplicate_role_step_and_missing_row(self):
        original = (ROOT / "text/technical-skill-selection-events.tsv").read_text(encoding="utf-8")
        first, second = original.splitlines()[1:3]
        variants = ["\ufeff" + original,
                    original.replace(second.split("\t")[0], first.split("\t")[0], 1),
                    original.replace("\tconfirmed\t", "\thypothesis\t", 1),
                    original.replace("\tprevious_row_redraw\t", "\tunknown_role\t", 1),
                    original.replace(first.split("\t")[4], first.split("\t")[5], 1),
                    "\n".join(original.splitlines()[:-1]) + "\n"]
        for value in variants:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "events.tsv"
                path.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    reroll_lifecycle_receipt._read_inventory(path, 8, subject.DOWN_ROLES)


if __name__ == "__main__":
    unittest.main()
