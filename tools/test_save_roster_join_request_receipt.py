import copy
import json
from pathlib import Path
import unittest

import save_roster_join_request_receipt as subject


ROOT = Path(__file__).resolve().parents[1]


class SaveRosterJoinRequestReceiptTests(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((ROOT / "workplace/phase56/c.json").read_bytes())
        self.baseline = json.loads((ROOT / "workplace/phase54/b-joined.json").read_bytes())
        self.paths = (
            ROOT / "text/save-roster-join-events.tsv",
            ROOT / "text/menu-events.tsv",
            ROOT / "text/save-roster-join-runtime-events.tsv",
            ROOT / "text/menu.zh-TW.tsv",
            ROOT / "text/save-roster-join.zh-TW.tsv",
        )

    def check(self, receipt):
        subject.validate(receipt, self.baseline, *self.paths)

    def test_accepts_exact_normal_player_path(self):
        self.check(self.receipt)

    def test_rejects_request_miss_identity_and_semantic_drift(self):
        variants = []
        bad = copy.deepcopy(self.receipt); bad["requests"].pop(); variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["catalog_misses"] = 3; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["events"][11]["original_sha256"] = "0" * 64; variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["file_ops"].pop(); variants.append(bad)
        bad = copy.deepcopy(self.receipt); bad["extra"] = 1; variants.append(bad)
        for value in variants:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.check(value)


if __name__ == "__main__":
    unittest.main()
