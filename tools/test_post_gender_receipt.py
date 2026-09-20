import copy
import csv
from pathlib import Path
import tempfile
import unittest

import post_gender_receipt as subject
import post_race_receipt


ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def event(row, entry, post):
    segment, offset = (int(value, 16) for value in row["caller"].split(":"))
    return {"entry_step": entry, "post_call_step": post, "caller": {"segment": segment, "offset": offset},
            "original_length": int(row["original_length"]), "original_sha256": row["original_sha256"],
            "background": int(row["background"]), "foreground": int(row["foreground"]),
            "row": int(row["row"]), "column": int(row["column"])}


class PostGenderReceiptTests(unittest.TestCase):
    def setUp(self):
        menu = rows(ROOT / "text/menu-events.tsv")[:10]
        post = post_race_receipt._read_inventory(ROOT / "text/post-race-events.tsv")
        gender = rows(ROOT / "text/gender-events.tsv")
        new = subject._read_inventory(ROOT / "text/post-gender-events.tsv")
        self.expected = menu + post + [gender[4]] + new
        self.receipt = {
            "state_start": 99_999_999, "stopped_at": 101_000_000,
            "bios_input": "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)",
            "events": [event(row, entry, post_step) for row, entry, post_step in zip(
                self.expected, subject.ENTRY_STEPS, subject.POST_STEPS)],
            "bios_keys": [
                {"queued_at": 100_010_000, "scan": 28, "ascii": 13},
                {"queued_at": 100_240_000, "scan": 28, "ascii": 13},
                {"queued_at": 100_400_000, "scan": 28, "ascii": 13},
            ],
        }

    def test_accepts_exact_receipt(self):
        subject._validate_receipt(self.receipt, self.expected)

    def test_rejects_identity_step_schedule_count_and_schema(self):
        variants = []
        bad = copy.deepcopy(self.receipt); bad["events"][-1]["original_length"] += 1; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"][-1]["entry_step"] += 1; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["bios_keys"][2]["queued_at"] += 1; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"].pop(); variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["extra"] = 1; variants.append(bad)
        for value in variants:
            with self.assertRaises(ValueError):
                subject._validate_receipt(value, self.expected)

    def test_inventory_rejects_bom_duplicate_and_missing_row(self):
        original = (ROOT / "text/post-gender-events.tsv").read_text(encoding="utf-8")
        variants = ["\ufeff" + original,
                    original.replace("class.option.warrior", "class.option.rocket_jock", 1),
                    original.replace("ba7e", "BA7e", 1),
                    original.replace("37F1:158C", "37f1:158C", 1),
                    original.replace("\t10\tba7e", "\t256\tba7e", 1),
                    "\n".join(original.splitlines()[:-1]) + "\n"]
        for value in variants:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "events.tsv"
                path.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    subject._read_inventory(path)


if __name__ == "__main__":
    unittest.main()
