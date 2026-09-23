"""3× host 字型 builder 的合成測試；不含倚天字模或原版素材。"""

import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import eten_host_font3 as host24
from catalog_font import CatalogError


class EtenHostFont3Test(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.out = self.repo / "workplace" / "host-font3"
        self.out.mkdir(parents=True)
        self.catalog = self.repo / "text" / "host-ui.zh-TW.tsv"
        self.catalog.parent.mkdir()
        self.catalog.write_text(
            "key\ttranslation\tsource\n"
            "host.settings\t設定\truntime-interface\n"
            "host.apply\t套用\truntime-interface\n"
            "host.cancel\t取消\truntime-interface\n"
            "host.scale2\t2×\truntime-interface\n"
            "host.scale3\t3×\truntime-interface\n",
            encoding="utf-8",
        )
        self.std = self.root / "STD.24M"
        self.spc = self.root / "SPCFONT.24"
        self.ascii = self.root / "ASCFONT.24"
        self.etunpack = self.root / "etunpack.py"
        self.std.write_bytes(b"synthetic compressed source")
        self.spc.write_bytes(b"\x80" * (408 * 72))
        self.ascii.write_bytes(b"\x80" * (256 * 48))
        self.etunpack.write_text("# synthetic decoder identity only\n", encoding="utf-8")
        self.decoded = b"\x80" * (13094 * 72)
        self.locked = {
            key: (path.name, hashlib.sha256(path.read_bytes()).hexdigest())
            for key, path in (
                ("std", self.std), ("spc", self.spc),
                ("ascii", self.ascii), ("etunpack", self.etunpack)
            )
        }

    def tearDown(self):
        self.temp.cleanup()

    def build(self):
        with patch.object(host24, "SOURCE_SHA256", self.locked), patch.object(
            host24, "_decode_std", return_value=self.decoded
        ):
            return host24.build(
                self.catalog, self.std, self.spc, self.ascii,
                self.etunpack, self.out, self.repo,
            )

    def old_outputs(self):
        old = (b"old-wide", b"old-ascii", b"old-manifest")
        for name, data in zip(host24.OUTPUT_NAMES, old):
            (self.out / name).write_bytes(data)
        return old

    def assert_old_outputs(self, old):
        self.assertEqual(
            tuple((self.out / name).read_bytes() for name in host24.OUTPUT_NAMES), old
        )

    def test_synthetic_build_has_seven_wide_and_two_ascii_glyphs(self):
        manifest = self.build()
        wide, ascii_digits, receipt = (
            (self.out / name).read_bytes() for name in host24.OUTPUT_NAMES
        )
        self.assertEqual(wide[:12], b"GOLEMFNT\x18\x00\x18\x00")
        self.assertEqual(ascii_digits[:12], b"GOLEMFNT\x10\x00\x18\x00")
        self.assertEqual(int.from_bytes(wide[12:16], "little"), 7)
        self.assertEqual(int.from_bytes(ascii_digits[12:16], "little"), 2)
        self.assertEqual(manifest["outputs"][host24.OUTPUT_NAMES[0]]["sha256"], hashlib.sha256(wide).hexdigest())
        self.assertIn(b"local-only-not-for-distribution", receipt)

    def test_missing_source_preserves_old_outputs(self):
        old = self.old_outputs()
        self.ascii.unlink()
        with self.assertRaises(CatalogError):
            self.build()
        self.assert_old_outputs(old)

    def test_source_sha_mismatch_preserves_old_outputs(self):
        old = self.old_outputs()
        self.spc.write_bytes(self.spc.read_bytes()[:-1] + b"\x81")
        with self.assertRaises(CatalogError):
            self.build()
        self.assert_old_outputs(old)

    def test_blank_native_glyph_preserves_old_outputs(self):
        old = self.old_outputs()
        self.decoded = b"\0" * (13094 * 72)
        with self.assertRaises(CatalogError):
            self.build()
        self.assert_old_outputs(old)

    def test_second_publish_error_restores_all_old_outputs(self):
        old = self.old_outputs()
        original_replace = os.replace
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic second replace failure")
            return original_replace(source, target)

        with patch.object(host24, "SOURCE_SHA256", self.locked), patch.object(
            host24, "_decode_std", return_value=self.decoded
        ), patch.object(host24.os, "replace", side_effect=fail_second):
            with self.assertRaises(OSError):
                host24.build(
                    self.catalog, self.std, self.spc, self.ascii,
                    self.etunpack, self.out, self.repo,
                )
        self.assert_old_outputs(old)


if __name__ == "__main__":
    unittest.main()
