import unittest

from logbook_merge import pages, wrap


class LogbookMergeUnitsTest(unittest.TestCase):
    """規格 039 §3.4：手札本文每列 72 半形單位、每頁 19 列（與 dosgolem layoutEclText 同規則）。"""

    def test_line_width_in_half_units(self):
        self.assertEqual(wrap("中" * 36), ["中" * 36])
        self.assertEqual(wrap("中" * 35 + "AB"), ["中" * 35 + "AB"])
        self.assertEqual(wrap("中" * 36 + "A"), ["中" * 36, "A"])
        # 拉丁字詞不拆：RAM 放不下時整個移到下一列。
        self.assertEqual(wrap("中" * 35 + "RAM"), ["中" * 35, "RAM"])
        # 內容空白是 1 單位，換行處的前導空白去掉。
        self.assertEqual(wrap("中" * 35 + "A B"), ["中" * 35 + "A", "B"])

    def test_token_wider_than_line_fails(self):
        with self.assertRaises(ValueError):
            wrap("A" * 73)
        self.assertEqual(wrap("A" * 72), ["A" * 72])

    def test_pages_of_19_lines(self):
        self.assertEqual(pages("中" * 36 * 19), 1)
        self.assertEqual(pages("中" * (36 * 19 + 1)), 2)


if __name__ == "__main__":
    unittest.main()
