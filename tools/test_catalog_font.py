import gzip
import struct
import tempfile
import unittest
from pathlib import Path

from catalog_font import (
    CatalogError,
    Entry,
    MAGIC,
    SOURCE_UNIFONT,
    build_golemfnt,
    catalog_codepoints,
    character_list_bytes,
    read_catalog,
)


class CatalogFontTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write_catalog(self, content: bytes) -> Path:
        path = self.root / "catalog.tsv"
        path.write_bytes(content)
        return path

    def test_catalog_accepts_valid_utf8_and_sorts_unique_characters(self):
        path = self.write_catalog(
            "key\ttranslation\tsource\nmenu.one\t乙甲\truntime\nmenu.two\t甲人\tmanual-and-runtime\n".encode()
        )
        entries = read_catalog(path)
        self.assertEqual(catalog_codepoints(entries), sorted(map(ord, "乙甲人")))
        self.assertEqual(character_list_bytes(entries), "U+4E59\t乙\nU+4EBA\t人\nU+7532\t甲\n".encode())

    def test_catalog_accepts_runtime_interface_source(self):
        path = self.write_catalog(
            "key\ttranslation\tsource\ngender.male\t男性\truntime-interface\n".encode()
        )
        self.assertEqual(read_catalog(path)[0].source, "runtime-interface")

    def test_catalog_rejects_invalid_utf8(self):
        with self.assertRaises(CatalogError):
            read_catalog(self.write_catalog(b"key\ttranslation\tsource\nkey\t\xff\truntime\n"))

    def test_catalog_rejects_bom_wrong_header_columns_and_empty_translation(self):
        bad = [
            b"\xef\xbb\xbfkey\ttranslation\tsource\nkey\tx\truntime\n",
            b"key\ttranslation\nkey\tx\n",
            b"key\ttranslation\tsource\nkey\tx\truntime\textra\n",
            b"key\ttranslation\tsource\nkey\t\truntime\n",
        ]
        for index, content in enumerate(bad):
            with self.subTest(index=index), self.assertRaises(CatalogError):
                read_catalog(self.write_catalog(content))

    def test_catalog_rejects_duplicate_key_source_control_and_non_nfc(self):
        bad = [
            "key\ttranslation\tsource\na\t甲\truntime\na\t乙\truntime\n",
            "key\ttranslation\tsource\na\t甲\tmanual\n",
            "key\ttranslation\tsource\na\t甲\\u200b\truntime\n".replace("\\u200b", "\u200b"),
            "key\ttranslation\tsource\na\te\u0301\truntime\n",
        ]
        for index, content in enumerate(bad):
            with self.subTest(index=index), self.assertRaises(CatalogError):
                read_catalog(self.write_catalog(content.encode()))

    def test_build_golemfnt_centers_8x16_and_keeps_16x16(self):
        entries = [Entry("a", "A甲", "runtime")]
        narrow = bytes([0x81] * 16)
        wide = bytes(range(32))
        font = self.root / "font.hex.gz"
        with gzip.open(font, "wt", encoding="ascii", newline="") as stream:
            stream.write(f"0041:{narrow.hex().upper()}\n7532:{wide.hex().upper()}\n")
        output = build_golemfnt(entries, font)
        self.assertEqual(output[:8], MAGIC)
        self.assertEqual(struct.unpack_from("<HHI", output, 8), (16, 16, 2))
        offset = 16
        codepoint, source = struct.unpack_from("<IB", output, offset)
        self.assertEqual((codepoint, source), (ord("A"), SOURCE_UNIFONT))
        self.assertEqual(output[offset + 5 : offset + 37], b"\x08\x10" * 16)
        offset += 37
        self.assertEqual(struct.unpack_from("<IB", output, offset), (ord("甲"), SOURCE_UNIFONT))
        self.assertEqual(output[offset + 5 : offset + 37], wide)
        self.assertEqual(output, build_golemfnt(entries, font))

    def test_build_rejects_missing_and_unsupported_glyph(self):
        entries = [Entry("a", "甲", "runtime")]
        missing = self.root / "missing.hex"
        missing.write_text("0041:" + "00" * 16 + "\n", encoding="ascii")
        with self.assertRaises(CatalogError):
            build_golemfnt(entries, missing)
        unsupported = self.root / "unsupported.hex"
        unsupported.write_text("7532:" + "00" * 64 + "\n", encoding="ascii")
        with self.assertRaises(CatalogError):
            build_golemfnt(entries, unsupported)


if __name__ == "__main__":
    unittest.main()
