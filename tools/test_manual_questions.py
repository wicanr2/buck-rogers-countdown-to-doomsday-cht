import unittest

import manual_questions as subject


def encoded(text: str) -> bytes:
    size = len(text)
    return bytes((byte + 6 - size) & 0xFF for byte in text.encode("ascii"))


class ManualQuestionsTest(unittest.TestCase):
    def make_data(self) -> bytearray:
        data = bytearray(subject.RECORD_BASE + subject.RECORD_COUNT * subject.RECORD_SIZE)
        for index in range(subject.RECORD_COUNT):
            offset = subject.RECORD_BASE + index * subject.RECORD_SIZE
            heading = f"Title{index + 1}"
            answer = "word"
            data[offset] = index + 1
            data[offset + 1] = len(heading)
            data[offset + 2 : offset + 2 + len(heading)] = encoded(heading)
            data[offset + 20] = index % 10 + 1
            data[offset + 21] = len(answer)
            data[offset + 22 : offset + 22 + len(answer)] = encoded(answer)
        return data

    def test_exports_metadata_without_answer(self):
        rows = subject.read_metadata(self.make_data())
        self.assertEqual(39, len(rows))
        self.assertEqual("Title1", rows[0]["heading_ascii"])
        self.assertEqual("0x00C2", rows[0]["data_offset_hex"])
        self.assertNotIn("answer", rows[0])

    def test_rejects_truncated_segment(self):
        with self.assertRaisesRegex(ValueError, "資料段過短"):
            subject.read_metadata(b"")

    def test_rejects_heading_over_capacity(self):
        data = self.make_data()
        data[subject.RECORD_BASE + 1] = subject.HEADING_CAPACITY + 1
        with self.assertRaisesRegex(ValueError, "標題長度超界"):
            subject.read_metadata(data)

    def test_rejects_answer_over_capacity_without_exporting_it(self):
        data = self.make_data()
        data[subject.RECORD_BASE + 21] = subject.ANSWER_CAPACITY + 1
        with self.assertRaisesRegex(ValueError, "答案長度超界"):
            subject.read_metadata(data)

    def test_rejects_ordinal_out_of_range(self):
        data = self.make_data()
        data[subject.RECORD_BASE + 20] = 0
        with self.assertRaisesRegex(ValueError, "序數超界"):
            subject.read_metadata(data)


if __name__ == "__main__":
    unittest.main()
