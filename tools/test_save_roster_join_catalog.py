import tempfile
import unittest
from pathlib import Path

import save_roster_join_catalog as subject


ROOT = Path(__file__).resolve().parents[1]


class SaveRosterJoinCatalogTests(unittest.TestCase):
    def setUp(self):
        self.events = (ROOT / "text/save-roster-join-events.tsv").read_bytes()
        self.catalog = (ROOT / "text/save-roster-join.zh-TW.tsv").read_bytes()

    def check(self, events=None, catalog=None):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            ep, cp = root / "events.tsv", root / "catalog.tsv"
            ep.write_bytes(self.events if events is None else events)
            cp.write_bytes(self.catalog if catalog is None else catalog)
            subject.validate(ep, cp)

    def test_accepts_exact_catalog_and_dynamic_fixtures(self):
        self.check()
        subject.verify_known_dynamic_bytes()

    def test_repository_runtime_projection_matches_full_inventory(self):
        subject.validate(
            ROOT / "text/save-roster-join-events.tsv",
            ROOT / "text/save-roster-join.zh-TW.tsv",
            ROOT / "text/menu.zh-TW.tsv",
            ROOT / "text/save-roster-join-runtime-events.tsv",
        )

    def test_rejects_identity_drift_and_dynamic_translation(self):
        drift = self.events.replace(b"121227787", b"121227788", 1)
        with self.assertRaises(ValueError):
            self.check(events=drift)
        translated = self.events.replace(b"dynamic_character_name\t\tconfirmed", b"dynamic_character_name\troster.loading\tconfirmed", 1)
        with self.assertRaises(ValueError):
            self.check(events=translated)

    def test_rejects_missing_or_orphan_catalog_key_bom_control_and_non_nfc(self):
        variants = [
            b"key\ttranslation\tsource\nroster.add_prompt\t\xe5\x8a\xa0\xe5\x85\xa5\xe8\xa7\x92\xe8\x89\xb2\xef\xbc\x9a\truntime-interface\n",
            self.catalog + "roster.orphan\t孤兒\truntime-interface\n".encode(),
            b"\xef\xbb\xbf" + self.catalog,
            self.catalog.replace("載入中……請稍候".encode(), "載入中\u200b……請稍候".encode()),
            self.catalog.replace("載入中……請稍候".encode(), "e\u0301".encode()),
        ]
        for value in variants:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.check(catalog=value)


if __name__ == "__main__":
    unittest.main()
