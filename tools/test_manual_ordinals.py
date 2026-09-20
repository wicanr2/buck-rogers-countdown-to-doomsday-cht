from pathlib import Path
import tempfile
import unittest

from manual_ordinals import BASE, MAX_ORDINAL, SLOT_SIZE, parse, validate_events


WORDS = ("first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth")


def fixture() -> bytearray:
    data = bytearray(BASE + (MAX_ORDINAL + 1) * SLOT_SIZE)
    for number, word in enumerate(WORDS, 1):
        padded = word.ljust(7).encode("ascii")
        offset = BASE + number * SLOT_SIZE
        data[offset] = len(padded)
        data[offset + 1 : offset + 1 + len(padded)] = padded
    return data


class ManualOrdinalsTest(unittest.TestCase):
    def test_parses_ten_length_prefixed_slots(self):
        rows = parse(bytes(fixture()))
        self.assertEqual([row["number"] for row in rows], [str(i) for i in range(1, 11)])
        self.assertEqual([row["ordinal_ascii"] for row in rows], list(WORDS))
        self.assertEqual(rows[0]["runtime_address"], "0EC0:33AE")
        self.assertEqual(rows[-1]["runtime_address"], "0EC0:3459")

    def test_rejects_truncated_data(self):
        with self.assertRaisesRegex(ValueError, "太短"):
            parse(bytes(fixture()[:-1]))

    def test_rejects_length_out_of_bounds(self):
        data = fixture()
        data[BASE + SLOT_SIZE] = SLOT_SIZE
        with self.assertRaisesRegex(ValueError, "長度越界"):
            parse(bytes(data))

    def test_rejects_non_ascii(self):
        data = fixture()
        data[BASE + SLOT_SIZE + 1] = 0xFF
        with self.assertRaisesRegex(ValueError, "不是 ASCII"):
            parse(bytes(data))

    def test_rejects_nonzero_padding(self):
        data = fixture()
        data[BASE + SLOT_SIZE + 18] = 1
        with self.assertRaisesRegex(ValueError, "padding 非零"):
            parse(bytes(data))

    def test_rejects_duplicate_word(self):
        data = fixture()
        first = BASE + SLOT_SIZE
        second = BASE + 2 * SLOT_SIZE
        data[second : second + SLOT_SIZE] = data[first : first + SLOT_SIZE]
        with self.assertRaisesRegex(ValueError, "字串重複"):
            parse(bytes(data))

    def test_event_ordinals_must_be_covered(self):
        rows = parse(bytes(fixture()))
        with tempfile.TemporaryDirectory() as directory:
            valid = Path(directory) / "valid.tsv"
            valid.write_text("event_key\tordinal\na\t1\nb\t10\n", encoding="utf-8")
            validate_events(rows, valid)
            invalid = Path(directory) / "invalid.tsv"
            invalid.write_text("event_key\tordinal\na\t11\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "未橋接 ordinal"):
                validate_events(rows, invalid)


if __name__ == "__main__":
    unittest.main()
