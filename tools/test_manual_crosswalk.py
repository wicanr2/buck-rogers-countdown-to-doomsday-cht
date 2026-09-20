import csv
import json
from pathlib import Path
import tempfile
import unittest

import manual_crosswalk as subject


class ManualCrosswalkTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.questions = self.root / "questions.tsv"
        self.crosswalk = self.root / "crosswalk.tsv"
        with self.questions.open("w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(
                out,
                fieldnames=["record_index", "data_offset_hex", "page", "heading_ascii", "ordinal"],
                delimiter="\t", lineterminator="\n",
            )
            writer.writeheader()
            for index in range(1, 40):
                writer.writerow({"record_index": index, "data_offset_hex": "0x0000", "page": index,
                                 "heading_ascii": f"Title {index}", "ordinal": 1})

    def tearDown(self):
        self.temp.cleanup()

    def write_crosswalk(self, mutate=None):
        rows = []
        for index in range(1, 40):
            row = {key: "" for key in subject.FIELDS}
            row.update(record_index=str(index), page=str(index), heading_ascii=f"Title {index}",
                       status="confirmed", source_scan="scan.jpg", archive_order="1",
                       source_sha256="abc", printed_page="1", source_anchor_zh="標題")
            rows.append(row)
        if mutate:
            mutate(rows)
        with self.crosswalk.open("w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=subject.FIELDS, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def test_accepts_complete_rows_and_manifest(self):
        self.write_crosswalk()
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps({"entries": [{"path": "x/scan.jpg", "sha256": "abc"}]}))
        subject.validate(self.questions, self.crosswalk, manifest)

    def test_rejects_mismatched_question_identity(self):
        self.write_crosswalk(lambda rows: rows[0].update(page="2"))
        with self.assertRaisesRegex(ValueError, "與題庫不符"):
            subject.validate(self.questions, self.crosswalk, None)

    def test_unknown_requires_reason_and_no_fake_source(self):
        self.write_crosswalk(lambda rows: rows[0].update(status="unknown", note="", source_scan="x"))
        with self.assertRaisesRegex(ValueError, "unknown"):
            subject.validate(self.questions, self.crosswalk, None)

    def test_rejects_manifest_hash_mismatch(self):
        self.write_crosswalk()
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps({"entries": [{"path": "x/scan.jpg", "sha256": "wrong"}]}))
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            subject.validate(self.questions, self.crosswalk, manifest)


if __name__ == "__main__":
    unittest.main()
