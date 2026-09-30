"""規格 041 §3.7：各工具的 --lang zh-CN 行為；zh-TW 行為不變。"""
from __future__ import annotations

import io
import contextlib
import tempfile
import unittest
from pathlib import Path

import catalog_font
import name_glossary
import skill_action_bar_catalog
import technical_skill_screen_catalog

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "text"
HAVE_CN = (T / "skill-action-bar.zh-CN.tsv").exists()


def quiet(fn, *a):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*a)


class ZhCnToolsTest(unittest.TestCase):
    def test_zh_tw_literal_validators_unchanged(self):
        self.assertEqual(skill_action_bar_catalog.validate(T / "skill-action-bar-events.tsv", T / "skill-action-bar.zh-TW.tsv"), (8, 5))
        technical_skill_screen_catalog.validate(T / "technical-skill-screen-events.tsv", T / "technical-skill-screen.zh-TW.tsv",
                                                T / "career-skill-exit-events.tsv", T / "technical-skill-selection-events.tsv")

    def _action_copy(self, directory: Path, text: str) -> Path:
        path = directory / "skill-action-bar.zh-CN.tsv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_action_bar_non_zh_tw_checks_hotkey_only(self):
        src = (T / "skill-action-bar.zh-TW.tsv").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as d:
            ok = self._action_copy(Path(d), src.replace("加點", "加点"))
            self.assertEqual(skill_action_bar_catalog.validate(T / "skill-action-bar-events.tsv", ok, "zh-CN"), (8, 5))
            with self.assertRaises(ValueError):  # zh-TW 仍比字面
                skill_action_bar_catalog.validate(T / "skill-action-bar-events.tsv", ok)
            bad = self._action_copy(Path(d), src.replace("(A)", "(X)"))
            with self.assertRaises(ValueError):
                skill_action_bar_catalog.validate(T / "skill-action-bar-events.tsv", bad, "zh-CN")

    def test_technical_non_zh_tw_hotkey_and_structure(self):
        src = (T / "technical-skill-screen.zh-TW.tsv").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "technical-skill-screen.zh-TW.tsv").write_text(src, encoding="utf-8")
            cn = Path(d) / "technical-skill-screen.zh-CN.tsv"
            cn.write_text(src.replace("技術性技能", "技术性技能"), encoding="utf-8")
            args = (T / "technical-skill-screen-events.tsv", cn, T / "career-skill-exit-events.tsv",
                    T / "technical-skill-selection-events.tsv")
            technical_skill_screen_catalog.validate(*args, lang="zh-CN")
            with self.assertRaises(ValueError):
                technical_skill_screen_catalog.validate(*args)  # zh-TW 字面釘選
            cn.write_text(src.replace("manual-and-runtime", "runtime-interface", 1), encoding="utf-8")
            with self.assertRaises(ValueError):
                technical_skill_screen_catalog.validate(*args, lang="zh-CN")

    def test_name_glossary_lang_paths_and_glob(self):
        g, e, f = name_glossary.lang_paths(T, "zh-CN")
        self.assertEqual((g.name, e.name, f.name), ("name-glossary.zh-CN.tsv", "name-glossary-exclude.zh-CN.tsv", "characters.zh-CN.txt"))
        self.assertEqual(name_glossary.lang_paths(T, "zh-TW")[0].name, "name-glossary.tsv")
        paths = name_glossary.catalog_paths(None, None, T, "zh-CN")
        self.assertFalse(any(p.name.startswith("name-glossary") for p in paths))

    @unittest.skipUnless(HAVE_CN, "需要產生後的 zh-CN 檔")
    def test_name_glossary_zh_cn_lint_and_no_apply(self):
        self.assertEqual(quiet(name_glossary.main, ["--lang", "zh-CN", "lint"]), 0)
        self.assertEqual(quiet(name_glossary.main, ["--lang", "zh-CN", "apply", "--dry-run"]), 2)
        glossary = name_glossary.read_glossary(*name_glossary.lang_paths(T, "zh-CN")[:2], use_old=False)
        self.assertTrue(all(n.old == () for n in glossary.names))

    @unittest.skipUnless(HAVE_CN, "需要產生後的 zh-CN 檔")
    def test_catalog_font_lang(self):
        paths = catalog_font.lang_catalogs(T, "zh-CN")
        self.assertFalse(any(p.name.startswith("name-glossary") for p in paths))
        self.assertEqual(quiet(catalog_font.main, ["lint", "--lang", "zh-CN"]), 0)
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "c.txt"
            self.assertEqual(quiet(catalog_font.main, ["chars", "--lang", "zh-CN", "--out", str(out)]), 0)
            chars = {line.split("\t")[1] for line in out.read_text(encoding="utf-8").splitlines()}
            translit = [r.split("\t")[1] for r in (T / "translit-zh-CN-map.tsv").read_text(encoding="utf-8").splitlines()[1:]]
            self.assertTrue(set(translit) <= chars)
            self.assertEqual(out.read_bytes(), (ROOT / "font" / "characters.zh-CN.txt").read_bytes())

    def test_catalog_font_zh_tw_explicit_paths_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "c.txt"
            self.assertEqual(quiet(catalog_font.main, ["chars", *map(str, sorted(T.glob("*.zh-TW.tsv"))), "--out", str(out)]), 0)
            self.assertEqual(out.read_bytes(), (ROOT / "font" / "characters.txt").read_bytes())


if __name__ == "__main__":
    unittest.main()
