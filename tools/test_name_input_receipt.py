import copy
import json
from pathlib import Path
import tempfile
import unittest

import name_input_receipt as subject
import reroll_lifecycle_receipt


ROOT = Path(__file__).resolve().parents[1]


class NameInputReceiptTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads((ROOT / "workplace/phase43/n-a.json").read_bytes())["events"]
        self.edit = reroll_lifecycle_receipt._read_inventory(ROOT / "text/name-edit-events.tsv", 2,
                                                              subject.EDIT_ROLES)
        self.confirm = reroll_lifecycle_receipt._read_inventory(ROOT / "text/name-confirm-events.tsv", 43,
                                                                 subject.CONFIRM_ROLES)

    @staticmethod
    def event(row):
        segment, offset = (int(value, 16) for value in row["caller"].split(":"))
        return {"entry_step": int(row["entry_step"]), "post_call_step": int(row["post_call_step"]),
                "caller": {"segment": segment, "offset": offset},
                "original_length": int(row["original_length"]), "original_sha256": row["original_sha256"],
                "background": int(row["background"]), "foreground": int(row["foreground"]),
                "row": int(row["row"]), "column": int(row["column"])}

    def receipt(self, rows, keys):
        return {"state_start": 99_999_999, "stopped_at": 103_000_000,
                "events": copy.deepcopy(self.baseline) + [self.event(row) for row in rows],
                "bios_keys": subject.PREFIX_KEYS + keys}

    def test_accepts_edit_and_confirm(self):
        edit_keys = [{"queued_at": 102_050_000, "scan": 30, "ascii": 97},
                     {"queued_at": 102_150_000, "scan": 48, "ascii": 98},
                     {"queued_at": 102_250_000, "scan": 14, "ascii": 8}]
        confirm_keys = [{"queued_at": 102_050_000, "scan": 30, "ascii": 97},
                        {"queued_at": 102_150_000, "scan": 28, "ascii": 13}]
        subject._validate_branch(self.receipt(self.edit, edit_keys), self.baseline, self.edit, edit_keys)
        subject._validate_branch(self.receipt(self.confirm, confirm_keys), self.baseline, self.confirm, confirm_keys)

    def test_rejects_baseline_identity_step_schedule_count_and_schema(self):
        keys = [{"queued_at": 102_050_000, "scan": 30, "ascii": 97},
                {"queued_at": 102_150_000, "scan": 48, "ascii": 98},
                {"queued_at": 102_250_000, "scan": 14, "ascii": 8}]
        exact = self.receipt(self.edit, keys)
        variants = []
        bad = copy.deepcopy(exact); bad["events"][0]["original_length"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["bios_keys"][-1]["ascii"] += 1; variants.append(bad)
        bad = copy.deepcopy(exact); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(exact); bad["extra"] = 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_branch(value, self.baseline, self.edit, keys)

    def test_inventory_rejects_bom_duplicate_role_step_and_missing_row(self):
        original = (ROOT / "text/name-confirm-events.tsv").read_text(encoding="utf-8")
        first, second = original.splitlines()[1:3]
        variants = ["\ufeff" + original,
                    original.replace(second.split("\t")[0], first.split("\t")[0], 1),
                    original.replace("\tconfirmed\t", "\thypothesis\t", 1),
                    original.replace("\tinput_echo\t", "\tunknown_role\t", 1),
                    original.replace(first.split("\t")[4], first.split("\t")[5], 1),
                    "\n".join(original.splitlines()[:-1]) + "\n"]
        for value in variants:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "events.tsv"
                path.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    reroll_lifecycle_receipt._read_inventory(path, 43, subject.CONFIRM_ROLES)


if __name__ == "__main__":
    unittest.main()
