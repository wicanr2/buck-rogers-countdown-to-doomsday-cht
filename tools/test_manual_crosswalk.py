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

    def write_english(self, record="1", source_hash="a" * 64):
        path = self.root / "english.tsv"
        with path.open("w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=subject.ENGLISH_FIELDS, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerow({"record_index": record, "source_kind": "original-english-transcription",
                             "source_url": "https://example.org/manual", "source_locator": "Rule Book p.42 ROLL.",
                             "source_sha256": source_hash, "retrieved_on": "2026-09-22"})
        return path

    def test_accepts_confirmed_english_source_without_fake_scan(self):
        self.write_crosswalk(lambda rows: rows[0].update(source_scan="", archive_order="", source_sha256="",
                                                         printed_page="", source_anchor_zh="", note="原版英文原書直接翻譯"))
        subject.validate(self.questions, self.crosswalk, None, self.write_english())

    def test_rejects_missing_english_source_or_bad_digest(self):
        self.write_crosswalk(lambda rows: rows[0].update(source_scan="", archive_order="", source_sha256="",
                                                         printed_page="", source_anchor_zh="", note="原版英文原書直接翻譯"))
        with self.assertRaisesRegex(ValueError, "來源欄位不完整"):
            subject.validate(self.questions, self.crosswalk, None)
        with self.assertRaisesRegex(ValueError, "英文原書來源不完整"):
            subject.validate(self.questions, self.crosswalk, None, self.write_english(source_hash="bad"))

    def test_english_snapshot_hash_is_verified_when_supplied(self):
        self.write_crosswalk(lambda rows: rows[0].update(source_scan="", archive_order="", source_sha256="",
                                                         printed_page="", source_anchor_zh="", note="原版英文原書直接翻譯"))
        snapshot = self.root / "manual.html"
        snapshot.write_bytes(b"original manual transcription")
        import hashlib
        digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        subject.validate(self.questions, self.crosswalk, None, self.write_english(source_hash=digest), snapshot)
        snapshot.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            subject.validate(self.questions, self.crosswalk, None, self.write_english(source_hash=digest), snapshot)

    def test_formal_sources_have_exact_39_records(self):
        project = Path(__file__).resolve().parents[1]
        subject.validate(project / "text/manual-questions.tsv", project / "text/manual-source-crosswalk.tsv",
                         None, project / "text/manual-english-sources.tsv")


if __name__ == "__main__":
    unittest.main()
