from pathlib import Path
import tempfile
import unittest

import race_selection_receipt as subject


class RaceSelectionReceiptTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "selection.tsv"
        self.good = (
            "sequence\tinput_phase\tevent_role\ttext_key\toriginal_length\toriginal_sha256\tcaller\tbackground\tforeground\trow\tcolumn\n"
            "1\tdown\tunselect-old\trace.terran\t6\t" + "a" * 64 + "\t37F1:1856\t0\t10\t3\t3\n"
            "2\tdown\tselect-new\trace.martian\t7\t" + "b" * 64 + "\t37F1:175D\t15\t0\t4\t3\n"
            "3\tup\tunselect-old\trace.martian\t7\t" + "b" * 64 + "\t37F1:1856\t0\t10\t4\t3\n"
            "4\tup\tselect-new\trace.terran\t6\t" + "a" * 64 + "\t37F1:175D\t15\t0\t3\t3\n"
        )
        self.path.write_text(self.good, encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_four_event_lifecycle(self):
        rows = subject._selection_rows(self.path, {"race.terran", "race.martian"})
        self.assertEqual(len(rows), 4)

    def test_rejects_order_key_hash_caller_and_count(self):
        mutations = [
            ("sequence", "1\tdown", "2\tdown"),
            ("phase", "2\tdown", "2\tup"),
            ("role", "unselect-old", "unknown"),
            ("key", "race.terran", "race.unknown"),
            ("hash", "a" * 64, "A" * 64),
            ("caller", "37F1:1856", "37f1:1856"),
            ("count", self.good.splitlines()[-1] + "\n", ""),
        ]
        for name, old, new in mutations:
            with self.subTest(name=name):
                self.path.write_text(self.good.replace(old, new, 1), encoding="utf-8")
                with self.assertRaises(ValueError):
                    subject._selection_rows(self.path, {"race.terran", "race.martian"})


if __name__ == "__main__":
    unittest.main()
