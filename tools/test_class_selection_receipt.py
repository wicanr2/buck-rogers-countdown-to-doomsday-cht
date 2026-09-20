import copy
import csv
from pathlib import Path
import tempfile
import unittest

import class_selection_receipt as subject

ROOT = Path(__file__).resolve().parents[1]


def event(row, entry, post):
    segment, offset = (int(v, 16) for v in row["caller"].split(":"))
    return {"entry_step": entry, "post_call_step": post, "caller": {"segment": segment, "offset": offset},
            "original_length": int(row["original_length"]), "original_sha256": row["original_sha256"],
            "background": int(row["background"]), "foreground": int(row["foreground"]),
            "row": int(row["row"]), "column": int(row["column"])}


class ClassSelectionReceiptTests(unittest.TestCase):
    def setUp(self):
        self.rows = subject._read_lifecycle(ROOT / "text/class-selection-events.tsv")[:4]
        self.keys = [{"queued_at": 100010000, "scan": 28, "ascii": 13},
                     {"queued_at": 100240000, "scan": 28, "ascii": 13},
                     {"queued_at": 100400000, "scan": 28, "ascii": 13},
                     {"queued_at": 100650000, "scan": 80, "ascii": 0},
                     {"queued_at": 100720000, "scan": 72, "ascii": 0}]
        entries, posts = subject.DOWN_UP_ENTRY, subject.DOWN_UP_POST
        self.receipt = {"state_start": 99999999, "stopped_at": 102000000,
                        "bios_input": "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)",
                        "events": [event(r, e, p) for r, e, p in zip(self.rows, entries, posts)],
                        "bios_keys": self.keys}

    def test_accepts_exact_lifecycle(self):
        subject._validate_path(self.receipt, self.rows, subject.DOWN_UP_ENTRY, subject.DOWN_UP_POST, self.keys)

    def test_rejects_schedule_identity_step_count_and_schema(self):
        variants = []
        bad = copy.deepcopy(self.receipt); bad["bios_keys"][-1]["queued_at"] += 1; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"][-1]["original_sha256"] = "0" * 64; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["extra"] = 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_path(value, self.rows, subject.DOWN_UP_ENTRY, subject.DOWN_UP_POST, self.keys)

    def test_inventory_rejects_bom_duplicate_and_missing_row(self):
        original = (ROOT / "text/class-selection-events.tsv").read_text(encoding="utf-8")
        variants = ["\ufeff" + original, original.replace("menu.return.row2", "menu.return.row1", 1),
                    "\n".join(original.splitlines()[:-1]) + "\n"]
        for value in variants:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "events.tsv"; path.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError): subject._read_lifecycle(path)


if __name__ == "__main__":
    unittest.main()
