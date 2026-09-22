import contextlib
import hashlib
import gzip
import io
import json
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
    candidate_validation_json,
    catalog_codepoints,
    character_list_bytes,
    main,
    read_catalog,
    read_catalogs,
    validate_font_candidate,
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

    def write_candidate(self, entries: list[Entry], glyphs: list[int] | None = None) -> tuple[Path, Path, Path, dict[str, object]]:
        glyphs = glyphs if glyphs is not None else catalog_codepoints(entries)
        source = self.root / "candidate.hex"
        source.write_text("".join(f"{codepoint:04X}:{'AA' * 32}\n" for codepoint in glyphs), encoding="ascii")
        license_path = self.root / "COPYING"
        license_path.write_text("Synthetic complete license text.\n", encoding="utf-8")
        manifest = self.root / "candidate-manifest.json"
        data: dict[str, object] = {
            "schema": "buck-rogers-manual-font-candidate/v1",
            "source_filename": source.name,
            "source_version": "synthetic-v1",
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "source_format": "unifont-hex",
            "conversion_rule": "unifont-8x16-or-16x16-to-golemfnt-16x16",
            "license_filename": license_path.name,
            "license_sha256": hashlib.sha256(license_path.read_bytes()).hexdigest(),
            "attribution_notice": "synthetic attribution",
            "embedding_notice": "synthetic embedding notice",
            "character_list_sha256": hashlib.sha256(character_list_bytes(entries)).hexdigest(),
            "validation_scope": "local-validation-only",
            "distribution_status": "undecided",
        }
        manifest.write_text(json.dumps(data), encoding="utf-8")
        return manifest, source, license_path, data

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

    def test_multiple_catalogs_merge_without_copying_translation_authority(self):
        first = self.root / "first.tsv"
        second = self.root / "second.tsv"
        first.write_text("key\ttranslation\tsource\na\t甲\truntime\n", encoding="utf-8")
        second.write_text("key\ttranslation\tsource\nb\t乙\truntime-interface\n", encoding="utf-8")
        self.assertEqual([entry.key for entry in read_catalogs([first, second])], ["a", "b"])
        second.write_text("key\ttranslation\tsource\na\t甲\truntime-interface\n", encoding="utf-8")
        with self.assertRaises(CatalogError):
            read_catalogs([first, second])

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

    def test_candidate_manifest_validates_metadata_without_building_or_leaking_input(self):
        entries = [Entry("a", "A甲", "runtime")]
        manifest, source, license_path, _ = self.write_candidate(entries)
        validation = validate_font_candidate(entries, manifest, source, license_path)
        metadata = json.loads(candidate_validation_json(validation))
        self.assertEqual(metadata["glyphs"], {"found": 2, "required": 2})
        self.assertEqual(metadata["source"]["filename"], source.name)
        self.assertEqual(metadata["license"]["filename"], license_path.name)
        encoded = candidate_validation_json(validation)
        self.assertNotIn("synthetic attribution", encoded)
        self.assertNotIn("Synthetic complete license text", encoded)
        self.assertNotIn("AA" * 16, encoded)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(
                main([
                    "validate-candidate", "--manifest", str(manifest), "--source", str(source), "--license", str(license_path),
                    str(self.write_catalog("key\ttranslation\tsource\na\tA甲\truntime\n".encode("utf-8"))),
                ]),
                0,
            )
        self.assertEqual(json.loads(output.getvalue()), metadata)
        self.assertFalse((self.root / "out.golemfnt").exists())

    def test_candidate_manifest_covers_the_formal_manual_catalog_with_synthetic_glyphs(self):
        manual_catalog = Path(__file__).resolve().parents[1] / "text" / "manual.zh-TW.tsv"
        entries = read_catalog(manual_catalog)
        manifest, source, license_path, _ = self.write_candidate(entries)
        validation = validate_font_candidate(entries, manifest, source, license_path)
        self.assertEqual(validation.required_glyphs, 845)
        self.assertEqual(validation.found_glyphs, 845)
        self.assertEqual(
            validation.character_list_sha256,
            "e6016c2473c87fcd2504652fabd0b069354b7abbd3c70281b67dfbaec18c7367",
        )
        self.assertFalse((self.root / "manual-synthetic.golemfnt").exists())

    def test_candidate_manifest_rejects_schema_hash_and_policy_drift(self):
        entries = [Entry("a", "甲", "runtime")]
        manifest, source, license_path, data = self.write_candidate(entries)
        cases: list[tuple[str, dict[str, object]]] = []
        missing = dict(data)
        del missing["source_version"]
        cases.append(("missing", missing))
        unknown = dict(data)
        unknown["unexpected"] = "x"
        cases.append(("unknown", unknown))
        for field, value in (
            ("source_sha256", "0" * 64),
            ("license_sha256", "1" * 64),
            ("character_list_sha256", "2" * 64),
            ("source_filename", "nested/candidate.hex"),
            ("source_format", "bdf"),
            ("conversion_rule", "other"),
            ("validation_scope", "adopted"),
            ("distribution_status", "distributable"),
        ):
            drift = dict(data)
            drift[field] = value
            cases.append((field, drift))
        for name, content in cases:
            with self.subTest(name=name):
                manifest.write_text(json.dumps(content), encoding="utf-8")
                with self.assertRaises(CatalogError):
                    validate_font_candidate(entries, manifest, source, license_path)

    def test_candidate_manifest_rejects_empty_license_missing_source_and_coverage_gap(self):
        entries = [Entry("a", "A甲", "runtime")]
        manifest, source, license_path, data = self.write_candidate(entries)
        license_path.write_text(" \n", encoding="utf-8")
        data["license_sha256"] = hashlib.sha256(license_path.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(CatalogError):
            validate_font_candidate(entries, manifest, source, license_path)

        manifest, source, license_path, _ = self.write_candidate(entries, [ord("A")])
        with self.assertRaises(CatalogError):
            validate_font_candidate(entries, manifest, self.root / "missing.hex", license_path)
        with self.assertRaises(CatalogError):
            validate_font_candidate(entries, manifest, source, license_path)


if __name__ == "__main__":
    unittest.main()
