"""tools/ja_check.py 的合成負例測試（規格 042 §3.3 第 11 項）與真實資料的護欄。

  python3 -m unittest tools/test_ja_check.py
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ja_check  # noqa: E402

HEADER = "key\ttranslation\tsource\n"


def write(path: Path, rows: list[tuple[str, str, str]]) -> None:
    path.write_text(HEADER + "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")


class Fixture:
    """一個最小的 text/ 與 font/：menu（有熱鍵）、hmenu（大寫與數字）、ecl-text、story-page9（定行）。"""

    def __init__(self, root: Path) -> None:
        self.text = root / "text"
        self.font = root / "font"
        self.text.mkdir()
        self.font.mkdir()
        self.zh = {
            "menu": [("menu.a", "加點(A) 減點(S)", "runtime-interface"), ("menu.b", "{0}還需要{1}點", "runtime-interface")],
            "hmenu": [("hmenu.x", "RAM 3", "ecl-batch-editorial"), ("hmenu.y", "離開(E)", "ecl-batch-editorial")],
            "ecl-text": [("ecl.1", "第一段\\n第二段「你好」", "ecl-batch-editorial")],
            "story-page9": [("story.page9.line.001", "一句話", "runtime-editorial")],
        }
        self.ja = {
            "menu": [("menu.a", "追加(A) 削減(S)", "runtime-interface"), ("menu.b", "{1}は{0}点必要だ", "runtime-interface")],
            "hmenu": [("hmenu.x", "RAM 3", "ecl-batch-editorial"), ("hmenu.y", "終了(E)", "ecl-batch-editorial")],
            "ecl-text": [("ecl.1", "一段落\\n二段落「こんにちは」", "ecl-batch-editorial")],
            "story-page9": [("story.page9.line.001", "一言だ", "runtime-editorial")],
        }
        self.charset = None

    def flush(self) -> None:
        for fam, rows in self.zh.items():
            write(self.text / f"{fam}.zh-TW.tsv", rows)
        for fam, rows in self.ja.items():
            write(self.text / f"{fam}.ja.tsv", rows)
        chars = set("".join(t for rows in self.ja.values() for _, t, _ in rows)) | set(map(chr, range(0x20, 0x7F)))
        (self.font / "charset.ja.txt").write_text("".join(sorted(chars)) + "\n", encoding="utf-8")
        if self.charset is not None:
            (self.font / "charset.ja.txt").write_text(self.charset + "\n", encoding="utf-8")

    def run(self, **kw) -> ja_check.Report:
        self.flush()
        report = ja_check.Report()
        ja_check.check(self.text, self.font, report, **kw)
        return report


class JaCheckNegatives(unittest.TestCase):
    def fixture(self) -> Fixture:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Fixture(Path(tmp.name))

    def assertHas(self, report: ja_check.Report, needle: str) -> None:
        self.assertTrue(any(needle in e for e in report.errors), f"沒有找到「{needle}」：{report.errors}")

    def test_clean(self) -> None:
        self.assertEqual(self.fixture().run().errors, [])

    def test_source_mismatch(self) -> None:
        f = self.fixture()
        f.ja["menu"][0] = ("menu.a", "追加(A) 削減(S)", "runtime")
        self.assertHas(f.run(), "source 與 zh-TW 不同")

    def test_placeholder_missing(self) -> None:
        f = self.fixture()
        f.ja["menu"][1] = ("menu.b", "必要だ", "runtime-interface")
        self.assertHas(f.run(), "佔位符")

    def test_hotkey_letter_mismatch(self) -> None:
        f = self.fixture()
        f.ja["menu"][0] = ("menu.a", "追加(B) 削減(S)", "runtime-interface")
        self.assertHas(f.run(), "熱鍵序列")

    def test_hotkey_count_mismatch(self) -> None:
        f = self.fixture()
        f.ja["menu"][0] = ("menu.a", "追加(A) 削減", "runtime-interface")
        self.assertHas(f.run(), "熱鍵序列")

    def test_extra_latin_word(self) -> None:
        f = self.fixture()
        f.ja["ecl-text"][0] = ("ecl.1", "一段落\\n二段落 Hello「こんにちは」", "ecl-batch-editorial")
        self.assertHas(f.run(), "多出拉丁字母詞")

    def test_newline_count(self) -> None:
        f = self.fixture()
        f.ja["ecl-text"][0] = ("ecl.1", "一段落二段落「こんにちは」", "ecl-batch-editorial")
        self.assertHas(f.run(), "\\n 數量")

    def test_quote_imbalance(self) -> None:
        f = self.fixture()
        f.ja["ecl-text"][0] = ("ecl.1", "一段落\\n二段落「こんにちは", "ecl-batch-editorial")
        self.assertHas(f.run(), "引號開閉差")

    def test_forbidden_chars(self) -> None:
        for bad in ("　", "ｱ", "ＡＢ", "～", '"'):
            f = self.fixture()
            f.ja["story-page9"][0] = ("story.page9.line.001", f"一言{bad}だ", "runtime-editorial")
            r = f.run()
            self.assertTrue(r.errors, f"禁用字元 {bad!r} 沒被擋")

    def test_charset_violation(self) -> None:
        f = self.fixture()
        f.flush()
        f.charset = "abc"
        self.assertHas(f.run(), "字集外字元")

    def test_missing_key_and_extra_key(self) -> None:
        f = self.fixture()
        f.ja["menu"].pop()
        self.assertHas(f.run(), "缺列")
        f = self.fixture()
        f.ja["menu"].append(("menu.zzz", "余分", "runtime-interface"))
        self.assertHas(f.run(), "key 不在 zh-TW")

    def test_missing_family_file(self) -> None:
        f = self.fixture()
        f.flush()
        (f.text / "menu.ja.tsv").unlink()
        report = ja_check.Report()
        ja_check.check(f.text, f.font, report)
        self.assertHas(report, "缺檔")

    def test_order(self) -> None:
        f = self.fixture()
        f.ja["hmenu"].reverse()
        self.assertHas(f.run(), "順序")

    def test_hmenu_caps_digits(self) -> None:
        f = self.fixture()
        f.ja["hmenu"][0] = ("hmenu.x", "RAM 4", "ecl-batch-editorial")
        self.assertHas(f.run(), "大寫 ASCII 與數字")

    def test_fixed_line_edges(self) -> None:
        f = self.fixture()
        f.ja["story-page9"][0] = ("story.page9.line.001", "ーした", "runtime-editorial")
        self.assertHas(f.run(), "列首禁則")
        f = self.fixture()
        f.ja["story-page9"][0] = ("story.page9.line.001", "彼は「", "runtime-editorial")
        f.zh["story-page9"][0] = ("story.page9.line.001", "他說「", "runtime-editorial")
        self.assertHas(f.run(), "開括號")

    def test_duplicate_key_and_shared_key(self) -> None:
        f = self.fixture()
        f.ja["menu"].append(("menu.a", "追加(A) 削減(S)", "runtime-interface"))
        self.assertHas(f.run(), "重複 key")

    def test_manual_rows_pass_and_are_checked(self) -> None:
        # 規格 051：manual 家族不再只准標頭，改由 manual_lang 檢查
        f = self.fixture()
        f.zh["manual"] = [("manual.1", "NEO 段落 7", "manual-and-runtime")]
        f.ja["manual"] = [("manual.1", "NEOの段落7", "manual-and-runtime")]
        self.assertEqual(f.run().errors, [])
        f.ja["manual"] = [("manual.1", "NEOとBUCKの段落7", "manual-and-runtime")]
        self.assertHas(f.run(), "新增的拉丁字母詞")
        f.ja["manual"] = [("manual.1", "NEOの段落8", "manual-and-runtime")]
        self.assertHas(f.run(), "數字")
        f.ja["manual"] = []
        self.assertHas(f.run(), "key 集合或順序")


    def test_row_count_assertion(self) -> None:
        f = self.fixture()
        self.assertHas(f.run(expect_rows=99), "列數")
        f = self.fixture()
        self.assertHas(f.run(expect_keys=99), "不同 key 數")

    def test_bom_and_crlf(self) -> None:
        f = self.fixture()
        f.flush()
        p = f.text / "menu.ja.tsv"
        p.write_bytes(b"\xef\xbb\xbf" + p.read_bytes())
        report = ja_check.Report()
        ja_check.check(f.text, f.font, report)
        self.assertHas(report, "BOM")
        p.write_bytes(p.read_bytes().replace(b"\xef\xbb\xbf", b"").replace(b"\n", b"\r\n"))
        report = ja_check.Report()
        ja_check.check(f.text, f.font, report)
        self.assertHas(report, "CR")


class JaCheckRealData(unittest.TestCase):
    """真實 text/ 的護欄：寬度檢查沒有因為缺事件檔而靜默略過。"""

    def test_caps_cover_most_rows(self) -> None:
        text = ja_check.ROOT / "text"
        if not (text / "hmenu-item-events.tsv").exists():
            self.skipTest("沒有真實 text/")
        src = ja_check.load_cap_sources(text)
        covered = total = 0
        for fam, path in ja_check.families(text, "ja").items():
            if fam in ("ecl-text", "logbook", "logbook-panel", "engine-template", "manual"):
                continue  # 這些家族的寬度另有檢查（ECL 上界、手札標題展開），不走 cap_for
            report = ja_check.Report()
            for r in ja_check.read_catalog_raw(path, report) or []:
                total += 1
                if ja_check.cap_for(fam, r[0], r[1], src) is not None:
                    covered += 1
        self.assertGreater(covered, 0.95 * total)


if __name__ == "__main__":
    unittest.main()
