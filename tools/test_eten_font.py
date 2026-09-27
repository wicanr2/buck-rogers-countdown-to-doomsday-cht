import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from catalog_font import CatalogError, Entry, character_list_bytes
from eten_font import (
    SOURCE_ASCII, SOURCE_SPC, SOURCE_STD_COMMON, SOURCE_STD_SECONDARY,
    Glyph, _read_source, _top_pad_ascii, _top_pad_wide, big5_raw, build, decode_golemfnt,
    encode_golemfnt, glyph_for, verify, SOURCE_SPECS,
)


class EtenFontTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        (self.repo / "workplace").mkdir(parents=True)
        self.asc = self.root / "ASCFONT.15"
        self.spc = self.root / "SPCFONT.15"
        self.std = self.root / "STDFONT.15"
        self.asc.write_bytes(b"".join(bytes([(index % 255) + 1]) * 15 for index in range(256)))
        self.spc.write_bytes(b"".join(bytes([(index % 255) + 1]) * 30 for index in range(408)))
        self.std.write_bytes(b"".join(bytes([(index % 255) + 1]) * 30 for index in range(13094)))

    def tearDown(self):
        self.temp.cleanup()

    def specs(self):
        return {name: (path.name, path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()) for name, path in (("asc", self.asc), ("spc", self.spc), ("std", self.std))}

    def test_top_pad_and_ascii_centering(self):
        self.assertEqual(_top_pad_wide(bytes(range(30))), b"\0\0" + bytes(range(30)))
        glyph = _top_pad_ascii(bytes([0x81]) * 15)
        self.assertEqual(glyph[:2], b"\0\0")
        self.assertEqual(glyph[2:], b"\x08\x10" * 15)

    def test_big5_and_all_four_source_regions(self):
        self.assertEqual(big5_raw(ord("一")), 471)
        self.assertEqual(big5_raw(ord("中")), 537)
        asc, spc, std = self.asc.read_bytes(), self.spc.read_bytes(), self.std.read_bytes()
        self.assertEqual(glyph_for(ord("A"), asc, spc, std).source, SOURCE_ASCII)
        self.assertEqual(glyph_for(ord("，"), asc, spc, std).source, SOURCE_SPC)
        self.assertEqual(glyph_for(ord("一"), asc, spc, std).source, SOURCE_STD_COMMON)
        self.assertEqual(glyph_for(ord("伎"), asc, spc, std).source, SOURCE_STD_SECONDARY)

    def test_all_six_eten_region_endpoints_choose_exact_entries(self):
        asc, spc, std = self.asc.read_bytes(), self.spc.read_bytes(), self.std.read_bytes()
        cases = ((0, SOURCE_SPC, spc, 0), (407, SOURCE_SPC, spc, 407), (471, SOURCE_STD_COMMON, std, 0), (5871, SOURCE_STD_COMMON, std, 5400), (6280, SOURCE_STD_SECONDARY, std, 5401), (13972, SOURCE_STD_SECONDARY, std, 13093))
        for raw, tag, source, entry in cases:
            with self.subTest(raw=raw):
                with patch("eten_font.big5_raw", return_value=raw):
                    glyph = glyph_for(ord("甲"), asc, spc, std)
                self.assertEqual(glyph.source, tag)
                self.assertEqual(glyph.bitmap, b"\0\0" + source[entry * 30 : (entry + 1) * 30])

    def test_rejects_reserved_raw_ranges(self):
        with patch("eten_font.big5_raw", return_value=408):
            with self.assertRaises(CatalogError):
                glyph_for(ord("甲"), self.asc.read_bytes(), self.spc.read_bytes(), self.std.read_bytes())

    def test_codec_non_two_bytes_and_unencodable_are_rejected(self):
        with self.assertRaises(CatalogError):
            big5_raw(ord("A"))
        with self.assertRaises(CatalogError):
            big5_raw(ord("😀"))

    def test_source_identity_rejects_wrong_name_size_hash_and_short_data(self):
        specs = self.specs()
        with patch("eten_font.SOURCE_SPECS", specs):
            self.assertEqual(_read_source(self.asc, "asc"), self.asc.read_bytes())
            wrong_name = self.root / "wrong.15"
            wrong_name.write_bytes(self.asc.read_bytes())
            with self.assertRaises(CatalogError):
                _read_source(wrong_name, "asc")
            wrong_size = self.root / "ASCFONT.15"
            wrong_size.write_bytes(b"short")
            with self.assertRaises(CatalogError):
                _read_source(wrong_size, "asc")
            wrong_hash = self.root / "other" / "ASCFONT.15"
            wrong_hash.parent.mkdir()
            wrong_hash.write_bytes(b"\x00" * self.asc.stat().st_size)
            with self.assertRaises(CatalogError):
                _read_source(wrong_hash, "asc")
        with self.assertRaises(CatalogError):
            glyph_for(ord("A"), b"short", self.spc.read_bytes(), self.std.read_bytes())
        with patch("eten_font.big5_raw", return_value=5872):
            with self.assertRaises(CatalogError):
                glyph_for(ord("甲"), self.asc.read_bytes(), self.spc.read_bytes(), self.std.read_bytes())
        with patch("eten_font.big5_raw", return_value=6279):
            with self.assertRaises(CatalogError):
                glyph_for(ord("甲"), self.asc.read_bytes(), self.spc.read_bytes(), self.std.read_bytes())

    def test_golemfnt_round_trip_and_nonblank_rejection(self):
        glyphs = [Glyph(0x20, 1, b"\0" * 32), Glyph(ord("A"), 1, b"\0\0\x80" + b"\0" * 29)]
        self.assertEqual(decode_golemfnt(encode_golemfnt(glyphs)), glyphs)
        with self.assertRaises(CatalogError):
            encode_golemfnt([Glyph(ord("A"), 1, b"\0" * 32)])
        with self.assertRaises(CatalogError):
            encode_golemfnt([Glyph(ord("A"), 99, b"\0\0\x80" + b"\0" * 29)])

    def test_build_rejects_path_escape_before_source_access(self):
        with self.assertRaises(CatalogError):
            build([], self.asc, self.spc, self.std, self.root / "outside.bin", self.repo / "workplace/m.json", self.repo)
        with self.assertRaises(CatalogError):
            build([], self.asc, self.spc, self.std, self.repo / "workplace", self.repo / "workplace/m.json", self.repo)
        target_dir = self.repo / "workplace/target-dir"
        target_dir.mkdir()
        with self.assertRaises(CatalogError):
            build([], self.asc, self.spc, self.std, target_dir, self.repo / "workplace/m.json", self.repo)
        catalog = self.repo / "workplace/input.tsv"
        catalog.write_text("key\ttranslation\tsource\na\t甲\truntime\n", encoding="utf-8")
        with self.assertRaises(CatalogError):
            build([catalog], self.asc, self.spc, self.std, catalog, self.repo / "workplace/m.json", self.repo)

    def test_build_atomic_failure_preserves_old_output(self):
        out = self.repo / "workplace/font.golemfnt"
        manifest = self.repo / "workplace/font.json"
        out.write_bytes(b"old")
        manifest.write_bytes(b"old-manifest")
        with patch("eten_font.SOURCE_SPECS", self.specs()), patch("eten_font._read_source", side_effect=CatalogError("synthetic source failure")):
            with self.assertRaises(CatalogError):
                build([], self.asc, self.spc, self.std, out, manifest, self.repo)
        self.assertEqual(out.read_bytes(), b"old")
        self.assertEqual(manifest.read_bytes(), b"old-manifest")

    def test_second_replace_failure_restores_existing_pair(self):
        catalog = Path(__file__).resolve().parents[1] / "text/manual.zh-TW.tsv"
        out = self.repo / "workplace/font.golemfnt"
        manifest = self.repo / "workplace/font.json"
        out.write_bytes(b"old-font")
        manifest.write_bytes(b"old-manifest")
        import eten_font
        entries = __import__("catalog_font").read_catalog(catalog)
        glyphs = [glyph_for(codepoint, self.asc.read_bytes(), self.spc.read_bytes(), self.std.read_bytes()) for codepoint in sorted({ord(ch) for entry in entries for ch in entry.translation})]
        expected = hashlib.sha256(encode_golemfnt(glyphs)).hexdigest()
        real_replace = os.replace
        calls = 0
        def fail_second(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic second replace failure")
            return real_replace(source, destination)
        with patch("eten_font.SOURCE_SPECS", self.specs()), patch("eten_font.MANUAL_OUTPUT_SHA256", expected), patch("eten_font.os.replace", side_effect=fail_second):
            with self.assertRaises(OSError):
                build([catalog], self.asc, self.spc, self.std, out, manifest, self.repo)
        self.assertEqual(out.read_bytes(), b"old-font")
        self.assertEqual(manifest.read_bytes(), b"old-manifest")

    def test_multiple_catalogs_merge_glyphs_despite_shared_text_key(self):
        first = self.repo / "workplace/first.tsv"
        second = self.repo / "workplace/second.tsv"
        first.write_text("key\ttranslation\tsource\nshared\t甲\truntime\n", encoding="utf-8")
        second.write_text("key\ttranslation\tsource\nshared\t乙\truntime-interface\n", encoding="utf-8")
        out = self.repo / "workplace/union.golemfnt"
        manifest_out = self.repo / "workplace/union.json"
        with patch("eten_font.SOURCE_SPECS", self.specs()):
            manifest = build([first, second], self.asc, self.spc, self.std, out, manifest_out, self.repo)
        # 規格 034：正式建置固定併入可列印 ASCII。
        self.assertEqual(manifest["format"]["glyphs"], 2 + 94)
        self.assertEqual([glyph.codepoint for glyph in decode_golemfnt(out.read_bytes())], sorted(set(map(ord, "甲乙")) | set(range(0x21, 0x7F))))
        self.assertEqual([entry["filename"] for entry in manifest["catalogs"]], ["first.tsv", "second.tsv"])

    def test_verify_recomputes_complete_formal_bundle_without_writing(self):
        text_dir = self.repo / "text"
        text_dir.mkdir()
        first = text_dir / "first.zh-TW.tsv"
        second = text_dir / "second.zh-TW.tsv"
        first.write_text("key\ttranslation\tsource\na\t甲\truntime\n", encoding="utf-8")
        second.write_text("key\ttranslation\tsource\nb\t乙\truntime-interface\n", encoding="utf-8")
        out = self.repo / "workplace/font.golemfnt"
        sidecar = self.repo / "workplace/font.json"
        with patch("eten_font.SOURCE_SPECS", self.specs()):
            expected = build([first, second], self.asc, self.spc, self.std, out, sidecar, self.repo)
            before = (out.read_bytes(), sidecar.read_bytes())
            self.assertEqual(verify(self.asc, self.spc, self.std, out, sidecar, self.repo), expected)
            self.assertEqual((out.read_bytes(), sidecar.read_bytes()), before)

            second.write_text("key\ttranslation\tsource\nb\t丙\truntime-interface\n", encoding="utf-8")
            with self.assertRaises(CatalogError):
                verify(self.asc, self.spc, self.std, out, sidecar, self.repo)
            second.write_text("key\ttranslation\tsource\nb\t乙\truntime-interface\n", encoding="utf-8")

            out.write_bytes(before[0][:-1] + bytes([before[0][-1] ^ 1]))
            with self.assertRaises(CatalogError):
                verify(self.asc, self.spc, self.std, out, sidecar, self.repo)
            self.assertNotEqual(out.read_bytes(), before[0])
            out.write_bytes(before[0])

            sidecar.write_bytes(before[1] + b" ")
            with self.assertRaises(CatalogError):
                verify(self.asc, self.spc, self.std, out, sidecar, self.repo)
            self.assertEqual(sidecar.read_bytes(), before[1] + b" ")
            sidecar.write_bytes(before[1])

            third = text_dir / "new.zh-TW.tsv"
            third.write_text("key\ttranslation\tsource\nc\t丁\truntime\n", encoding="utf-8")
            with self.assertRaises(CatalogError):
                verify(self.asc, self.spc, self.std, out, sidecar, self.repo)
            third.unlink()

            self.asc.write_bytes(b"\0" * self.asc.stat().st_size)
            with self.assertRaises(CatalogError):
                verify(self.asc, self.spc, self.std, out, sidecar, self.repo)

    def test_verify_rejects_missing_bundle_before_reading_sources(self):
        (self.repo / "text").mkdir()
        (self.repo / "text/one.zh-TW.tsv").write_text("key\ttranslation\tsource\na\t甲\truntime\n", encoding="utf-8")
        with self.assertRaises(CatalogError):
            verify(self.asc, self.spc, self.std, self.repo / "workplace/missing.golemfnt", self.repo / "workplace/missing.json", self.repo)

    def test_rejects_symlink_and_hardlink_alias_outputs(self):
        out = self.repo / "workplace/font.golemfnt"
        manifest = self.repo / "workplace/font.json"
        out.write_bytes(b"old")
        manifest.hardlink_to(out)
        with patch("eten_font.SOURCE_SPECS", self.specs()):
            with self.assertRaises(CatalogError):
                build([], self.asc, self.spc, self.std, out, manifest, self.repo)
        alias = self.repo / "workplace/alias.golemfnt"
        alias.symlink_to(out)
        with patch("eten_font.SOURCE_SPECS", self.specs()):
            with self.assertRaises(CatalogError):
                build([], self.asc, self.spc, self.std, alias, manifest, self.repo)

    def test_formal_catalog_character_list_is_fixed(self):
        catalog = Path(__file__).resolve().parents[1] / "text/manual.zh-TW.tsv"
        from catalog_font import read_catalog
        self.assertEqual(hashlib.sha256(character_list_bytes(read_catalog(catalog))).hexdigest(), "f48517bc3e754a312382b542489f50031fa346b255015dc0b82e30852a48617c")


if __name__ == "__main__":
    unittest.main()
