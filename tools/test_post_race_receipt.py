import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest

import post_race_receipt


ROOT = Path(__file__).resolve().parents[1]


def rows(path: Path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def event(row, entry, post):
    segment, offset = (int(part, 16) for part in row["caller"].split(":"))
    return {
        "entry_step": entry, "post_call_step": post,
        "caller": {"segment": segment, "offset": offset},
        "original_length": int(row["original_length"]),
        "original_sha256": row["original_sha256"],
        "background": int(row["background"]), "foreground": int(row["foreground"]),
        "row": int(row["row"]), "column": int(row["column"]),
    }


class PostRaceReceiptTests(unittest.TestCase):
    def setUp(self):
        self.menu = rows(ROOT / "text/menu-events.tsv")
        self.post = post_race_receipt._read_inventory(ROOT / "text/post-race-events.tsv")
        expected = self.menu[:10] + self.post
        self.receipt = {
            "state_start": 99_999_999,
            "stopped_at": 101_000_000,
            "bios_input": "Enter(scan=0x1c,ascii=0x0d,queued_at=100010000)",
            "events": [event(row, entry, post) for row, entry, post in zip(
                expected, post_race_receipt.ENTRY_STEPS, post_race_receipt.POST_STEPS
            )],
            "bios_keys": [
                {"queued_at": 100_010_000, "scan": 28, "ascii": 13},
                {"queued_at": 100_240_000, "scan": 28, "ascii": 13},
            ],
        }

    def test_exact_receipt(self):
        post_race_receipt._validate_receipt(self.receipt, self.menu, self.post)

    def test_rejects_identity_step_schedule_and_schema_mutations(self):
        mutations = []
        bad = copy.deepcopy(self.receipt); bad["events"][10]["original_length"] += 1; mutations.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"][13]["entry_step"] += 1; mutations.append(bad)
        bad = copy.deepcopy(self.receipt); bad["bios_keys"][1]["queued_at"] += 1; mutations.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"].pop(); mutations.append(bad)
        bad = copy.deepcopy(self.receipt); bad["extra"] = 1; mutations.append(bad)
        for value in mutations:
            with self.assertRaises(ValueError):
                post_race_receipt._validate_receipt(value, self.menu, self.post)

    def test_inventory_rejects_bom_duplicate_and_missing_row(self):
        original = (ROOT / "text/post-race-events.tsv").read_text(encoding="utf-8")
        variants = ["\ufeff" + original, original + original.splitlines()[1] + "\n", "\n".join(original.splitlines()[:-1]) + "\n"]
        for data in variants:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "events.tsv"
                path.write_text(data, encoding="utf-8")
                with self.assertRaises(ValueError):
                    post_race_receipt._read_inventory(path)


if __name__ == "__main__":
    unittest.main()
