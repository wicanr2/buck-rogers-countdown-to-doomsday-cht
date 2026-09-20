import copy
import json
from pathlib import Path
import tempfile
import unittest

import career_skill_receipt as subject
import reroll_lifecycle_receipt


ROOT = Path(__file__).resolve().parents[1]


class CareerSkillReceiptTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads((ROOT / "workplace/phase44/confirm-a.json").read_bytes())["events"]
        self.selection = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/career-skill-selection-events.tsv", 8, subject.SELECTION_ROLES)
        self.add = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/career-skill-add-events.tsv", 5, subject.ADD_ROLES)
        self.refusal = reroll_lifecycle_receipt._read_inventory(
            ROOT / "text/career-skill-refusal-events.tsv", 1, subject.REFUSAL_ROLES)

    @staticmethod
    def event(row):
        segment, offset = (int(value, 16) for value in row["caller"].split(":"))
        return {"entry_step": int(row["entry_step"]), "post_call_step": int(row["post_call_step"]),
                "caller": {"segment": segment, "offset": offset},
                "original_length": int(row["original_length"]), "original_sha256": row["original_sha256"],
                "background": int(row["background"]), "foreground": int(row["foreground"]),
                "row": int(row["row"]), "column": int(row["column"])}

    def receipt(self, rows, keys, stopped_at=103_000_000):
        return {"state_start": 99_999_999, "stopped_at": stopped_at,
                "events": copy.deepcopy(self.baseline) + [self.event(row) for row in rows],
                "bios_keys": subject.PREFIX_KEYS + keys}

    def test_accepts_selection_add_and_refusal(self):
        down = [{"queued_at": 102_700_000, "scan": 80, "ascii": 0}]
        enter = [{"queued_at": 102_700_000, "scan": 28, "ascii": 13}]
        refusal = [{"queued_at": 102_700_000, "scan": 1, "ascii": 27},
                   {"queued_at": 102_900_000, "scan": 49, "ascii": 110}]
        subject._validate_branch(self.receipt(self.selection, down), self.baseline, self.selection, down,
                                 103_000_000)
        subject._validate_branch(self.receipt(self.add, enter), self.baseline, self.add, enter, 103_000_000)
        subject._validate_branch(self.receipt(self.refusal, refusal, 104_000_000), self.baseline,
                                 self.refusal, refusal, 104_000_000)

    def test_rejects_baseline_identity_step_schedule_count_schema_and_stop(self):
        keys = [{"queued_at": 102_700_000, "scan": 80, "ascii": 0}]
        exact = self.receipt(self.selection, keys)
        variants = []
        bad = copy.deepcopy(exact); bad["events"][0]["original_length"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["bios_keys"][-1]["scan"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(exact); bad["extra"] = 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["stopped_at"] += 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_branch(value, self.baseline, self.selection, keys, 103_000_000)

    def test_inventory_rejects_bom_duplicate_role_step_and_missing_row(self):
        original = (ROOT / "text/career-skill-selection-events.tsv").read_text(encoding="utf-8")
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
                    reroll_lifecycle_receipt._read_inventory(path, 8, subject.SELECTION_ROLES)


if __name__ == "__main__":
    unittest.main()
