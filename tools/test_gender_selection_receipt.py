import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest

import gender_selection_receipt as subject
import post_race_receipt


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def event(row, entry, post):
    segment, offset = (int(value, 16) for value in row["caller"].split(":"))
    return {"entry_step": entry, "post_call_step": post, "caller": {"segment": segment, "offset": offset},
            "original_length": int(row["original_length"]), "original_sha256": row["original_sha256"],
            "background": int(row["background"]), "foreground": int(row["foreground"]),
            "row": int(row["row"]), "column": int(row["column"])}


class GenderSelectionReceiptTests(unittest.TestCase):
    def setUp(self):
        self.lifecycle = subject._read_lifecycle(ROOT / "text/gender-selection-events.tsv")
        base = read_rows(ROOT / "text/menu-events.tsv")[:10] + post_race_receipt._read_inventory(ROOT / "text/post-race-events.tsv")
        rows = base + self.lifecycle[:4]
        self.keys = [{"queued_at": 100_010_000, "scan": 28, "ascii": 13},
                     {"queued_at": 100_240_000, "scan": 28, "ascii": 13},
                     {"queued_at": 100_400_000, "scan": 80, "ascii": 0},
                     {"queued_at": 100_460_000, "scan": 72, "ascii": 0}]
        self.receipt = {"state_start": 99_999_999, "stopped_at": 101_000_000,
                        "bios_input": "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)",
                        "events": [event(row, entry, post) for row, entry, post in zip(
                            rows, subject.BASE_ENTRY + subject.DOWN_UP_ENTRY, subject.BASE_POST + subject.DOWN_UP_POST)],
                        "bios_keys": self.keys}
        self.rows = rows

    def test_accepts_exact_down_up_path(self):
        subject._validate_path(self.receipt, self.rows, subject.BASE_ENTRY + subject.DOWN_UP_ENTRY,
                               subject.BASE_POST + subject.DOWN_UP_POST, self.keys)

    def test_rejects_schedule_identity_step_count_and_schema(self):
        variants = []
        bad = copy.deepcopy(self.receipt); bad["bios_keys"][2]["queued_at"] += 1; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"][-1]["original_sha256"] = "0" * 64; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["extra"] = 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_path(value, self.rows, subject.BASE_ENTRY + subject.DOWN_UP_ENTRY,
                                       subject.BASE_POST + subject.DOWN_UP_POST, self.keys)

    def test_inventory_rejects_bom_duplicate_key_and_missing_row(self):
        original = (ROOT / "text/gender-selection-events.tsv").read_text(encoding="utf-8")
        variants = ["\ufeff" + original, original.replace("menu.return.row2", "menu.return.row1", 1),
                    "\n".join(original.splitlines()[:-1]) + "\n"]
        for value in variants:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "events.tsv"
                path.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    subject._read_lifecycle(path)


if __name__ == "__main__":
    unittest.main()
