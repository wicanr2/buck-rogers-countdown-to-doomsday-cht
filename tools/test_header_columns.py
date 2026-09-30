from pathlib import Path
import shutil
import tempfile
import unittest

import header_columns as subject


ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "text/header-columns.tsv"


class HeaderColumnsTest(unittest.TestCase):
    def check(self, content: str, edit=None) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = Path(directory) / "text"
            shutil.copytree(ROOT / "text", text, ignore=shutil.ignore_patterns("cmudict"))
            (text / "header-columns.tsv").write_text(content, encoding="utf-8")
            if edit:
                edit(text)
            rows = subject.load_list(text / "header-columns.tsv")
            subject.check_load(text, rows)

    def formal(self) -> str:
        return FORMAL.read_text(encoding="utf-8")

    def test_formal_list(self):
        rows = subject.load_list(FORMAL)
        subject.check_load(ROOT / "text", rows)
        self.assertEqual({r["key"]: r["cols"] for r in rows}, {
            "career.screen.columns.heading": [2, 8, 14],
            "frag.442e07fe93c9": [0, 17, 32],
            "frag.0ddcc5022a9c": [0, 17, 32],
        })

    def test_anchor_units(self):
        # 點數 加值 總計：各欄起於 4、16、28 單位，末欄止於 32 ≤ 36。
        self.assertEqual(subject.anchor_columns("點數 加值 總計", [2, 8, 14], 36), [4, 16, 28])

    def test_rejects_not_increasing(self):
        with self.assertRaises(ValueError):
            self.check(self.formal().replace("2,8,14", "2,8,8"))

    def test_rejects_column_width(self):
        # 第一欄 4 單位 + 1 > 2·(4−2)。
        with self.assertRaises(ValueError):
            self.check(self.formal().replace("2,8,14", "2,4,14"))

    def test_rejects_last_column(self):
        # 2·17 + 4 > 18×2。
        with self.assertRaises(ValueError):
            self.check(self.formal().replace("2,8,14", "2,8,17"))

    def test_rejects_token_count(self):
        with self.assertRaises(ValueError):
            self.check(self.formal().replace("2,8,14", "2,8"))

    def test_rejects_blank_rules(self):
        for bad in ("點數  加值 總計", " 點數 加值 總計", "點數 加值 總計 "):
            def edit(text: Path, bad=bad) -> None:
                path = text / "career-skill-screen.zh-TW.tsv"
                path.write_text(path.read_text(encoding="utf-8").replace("點數 加值 總計", bad), encoding="utf-8")
            with self.subTest(bad=repr(bad)), self.assertRaises(ValueError):
                self.check(self.formal(), edit)

    def test_rejects_unknown_keys(self):
        with self.assertRaises(ValueError):
            self.check(self.formal().replace("career.screen.columns.heading", "career.screen.missing"))
        with self.assertRaises(ValueError):
            self.check(self.formal().replace("frag.442e07fe93c9", "frag.000000000000"))
        with self.assertRaises(ValueError):
            self.check(self.formal().replace("dispatcher\tfrag.442e07fe93c9", "dispatcher\tfrag.442e07fe93c9.uc"))

    def test_rejects_missing_translation(self):
        def edit(text: Path) -> None:
            path = text / "engine-fragment.zh-TW.tsv"
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
            path.write_text("".join(l for l in lines if not l.startswith("frag.442e07fe93c9\t")), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.check(self.formal(), edit)

    def test_token_starts(self):
        self.assertEqual(subject.token_starts("ab   cd e"), [0, 5, 8])

    def test_skip_without_original(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = subject.load_list(FORMAL)
            report = subject.verify_original(ROOT / "text", Path(directory), rows)
        self.assertEqual(len(report), 3 + 1)  # 兩條 dispatcher、選單兩張畫面
        self.assertTrue(all(subject.SKIP in line for line in report))


if __name__ == "__main__":
    unittest.main()
