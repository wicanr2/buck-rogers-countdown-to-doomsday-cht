"""tools/lang_check.py 的韓文（ko）合成負例測試（規格 043 §5.1）與真實資料護欄。

  cd tools && python3 -m unittest test_lang_check.py
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lang_check  # noqa: E402

HEADER = "key\ttranslation\tsource\n"


def write(path: Path, rows: list[tuple[str, str, str]]) -> None:
    path.write_text(HEADER + "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")


class Fixture:
    """最小的 text/ 與 font/：menu（有熱鍵）、hmenu（大寫與數字）、ecl-text、story-page9（定行）。"""

    def __init__(self, root: Path) -> None:
        self.text = root / "text"
        self.font = root / "font"
        self.text.mkdir()
        self.font.mkdir()
        self.zh = {
            "menu": [("menu.a", "加點(A) 減點(S)", "runtime-interface"), ("menu.b", "{0}還需要{1}點", "runtime-interface")],
            "hmenu": [("hmenu.x", "RAM 3", "ecl-batch-editorial"), ("hmenu.y", "離開(E)", "ecl-batch-editorial")],
            "ecl-text": [("ecl.1", "NEO 部隊第一段\\n第二段「你好」", "ecl-batch-editorial")],
            "story-page9": [("story.page9.line.001", "一句話", "runtime-editorial")],
        }
        self.ko = {
            "menu": [("menu.a", "추가(A) 삭제(S)", "runtime-interface"), ("menu.b", "{1}점이 {0}만큼 필요하다", "runtime-interface")],
            "hmenu": [("hmenu.x", "RAM 3", "ecl-batch-editorial"), ("hmenu.y", "종료(E)", "ecl-batch-editorial")],
            "ecl-text": [("ecl.1", "NEO 부대의 첫 단락\\n둘째 단락「안녕」", "ecl-batch-editorial")],
            "story-page9": [("story.page9.line.001", "한마디", "runtime-editorial")],
        }
        self.charset = None

    def flush(self) -> None:
        for fam, rows in self.zh.items():
            write(self.text / f"{fam}.zh-TW.tsv", rows)
        for fam, rows in self.ko.items():
            write(self.text / f"{fam}.ko.tsv", rows)
        chars = set("".join(t for rows in self.ko.values() for _, t, _ in rows)) | set(map(chr, range(0x20, 0x7F)))
        (self.font / "charset.ko.txt").write_text("".join(sorted(chars)) + "\n", encoding="utf-8")
        if self.charset is not None:
            (self.font / "charset.ko.txt").write_text(self.charset + "\n", encoding="utf-8")

    def run(self, **kw) -> lang_check.Report:
        self.flush()
        report = lang_check.Report()
        lang_check.check(self.text, self.font, report, lang="ko", **kw)
        return report


class KoCheckNegatives(unittest.TestCase):
    def fixture(self) -> Fixture:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Fixture(Path(tmp.name))

    def assertHas(self, report: lang_check.Report, needle: str) -> None:
        self.assertTrue(any(needle in e for e in report.errors), f"沒有找到「{needle}」：{report.errors}")

    def test_clean(self) -> None:
        self.assertEqual(self.fixture().run().errors, [])

    def test_source_mismatch(self) -> None:
        f = self.fixture()
        f.ko["menu"][0] = ("menu.a", "추가(A) 삭제(S)", "runtime")
        self.assertHas(f.run(), "source 與 zh-TW 不同")

    def test_placeholder_missing(self) -> None:
        f = self.fixture()
        f.ko["menu"][1] = ("menu.b", "필요하다", "runtime-interface")
        self.assertHas(f.run(), "佔位符")

    def test_hotkey_mismatch(self) -> None:
        f = self.fixture()
        f.ko["menu"][0] = ("menu.a", "추가(B) 삭제(S)", "runtime-interface")
        self.assertHas(f.run(), "熱鍵序列")

    def test_extra_latin_word(self) -> None:
        f = self.fixture()
        f.ko["ecl-text"][0] = ("ecl.1", "NEO 부대의 첫 단락\\n둘째 Hello 단락「안녕」", "ecl-batch-editorial")
        self.assertHas(f.run(), "多出拉丁字母詞")

    def test_newline_count(self) -> None:
        f = self.fixture()
        f.ko["ecl-text"][0] = ("ecl.1", "NEO 부대의 단락「안녕」", "ecl-batch-editorial")
        self.assertHas(f.run(), "\\n 數量")

    def test_quote_imbalance(self) -> None:
        f = self.fixture()
        f.ko["ecl-text"][0] = ("ecl.1", "NEO 부대의 첫 단락\\n둘째 단락「안녕", "ecl-batch-editorial")
        self.assertHas(f.run(), "引號開閉差")

    def test_charset_violation(self) -> None:
        f = self.fixture()
        f.flush()
        f.charset = "abc"
        self.assertHas(f.run(), "字集外字元")

    def test_missing_and_extra_key(self) -> None:
        f = self.fixture()
        f.ko["menu"].pop()
        self.assertHas(f.run(), "缺列")
        f = self.fixture()
        f.ko["menu"].append(("menu.zzz", "여분", "runtime-interface"))
        self.assertHas(f.run(), "key 不在 zh-TW")

    def test_translit_files_are_not_a_family(self) -> None:
        """規格 044 §3.5：音譯允許字集 translit-chars.<lang>.tsv 與詞典 translit-<lang>-names.tsv 不是翻譯家族。"""
        f = self.fixture()
        base = f.run()
        write(f.text / "translit-chars.ko.tsv", [(f"translit.char.U+{0xAC00:04X}", "가", "translit-table")])
        write(f.text / "translit-chars.zh-TW.tsv", [(f"translit.char.U+{0x4E00:04X}", "一", "translit-table")])
        (f.text / "translit-ko-names.tsv").write_text("english\ttranslation\tbasis\nPIERRE\t피에르\tmachine-reviewed\n", encoding="utf-8")
        for lang in ("ko", "zh-TW"):
            self.assertNotIn("translit-chars", lang_check.families(f.text, lang))
        report = f.run()
        self.assertEqual(report.errors, base.errors)
        self.assertEqual(report.warnings, base.warnings)

    def test_missing_family_file(self) -> None:
        f = self.fixture()
        f.flush()
        (f.text / "menu.ko.tsv").unlink()
        report = lang_check.Report()
        lang_check.check(f.text, f.font, report, lang="ko")
        self.assertHas(report, "缺檔")

    def test_order(self) -> None:
        f = self.fixture()
        f.ko["hmenu"].reverse()
        self.assertHas(f.run(), "順序")

    def test_hmenu_caps_digits(self) -> None:
        f = self.fixture()
        f.ko["hmenu"][0] = ("hmenu.x", "RAM 4", "ecl-batch-editorial")
        self.assertHas(f.run(), "大寫 ASCII 與數字")

    def test_manual_must_be_header_only(self) -> None:
        f = self.fixture()
        f.zh["manual"] = [("manual.1", "段落", "manual-term-editorial")]
        f.ko["manual"] = [("manual.1", "단락", "manual-term-editorial")]
        self.assertHas(f.run(), "只有標頭")

    def test_row_count_assertion(self) -> None:
        f = self.fixture()
        self.assertHas(f.run(expect_rows=99), "列數")
        f = self.fixture()
        self.assertHas(f.run(expect_keys=99), "不同 key 數")

    def test_bom_and_crlf(self) -> None:
        f = self.fixture()
        f.flush()
        p = f.text / "menu.ko.tsv"
        p.write_bytes(b"\xef\xbb\xbf" + p.read_bytes())
        report = lang_check.Report()
        lang_check.check(f.text, f.font, report, lang="ko")
        self.assertHas(report, "BOM")
        p.write_bytes(p.read_bytes().replace(b"\xef\xbb\xbf", b"").replace(b"\n", b"\r\n"))
        report = lang_check.Report()
        lang_check.check(f.text, f.font, report, lang="ko")
        self.assertHas(report, "CR")

    # ---- 檢查項 12 至 14（規格 043 §3.3）

    def test_item12_space_runs(self) -> None:
        f = self.fixture()
        f.ko["ecl-text"][0] = ("ecl.1", "NEO 부대의  첫 단락\\n둘째 단락「안녕」", "ecl-batch-editorial")
        self.assertHas(f.run(), "連續空白段數")
        # zh-TW 本來就有一段連續空白者，ko 有一段即可
        f = self.fixture()
        f.zh["ecl-text"][0] = ("ecl.1", "NEO  部隊第一段\\n第二段「你好」", "ecl-batch-editorial")
        f.ko["ecl-text"][0] = ("ecl.1", "NEO    부대의 첫 단락\\n둘째 단락「안녕」", "ecl-batch-editorial")
        self.assertEqual(f.run().errors, [])

    def test_item13_latin_hangul(self) -> None:
        f = self.fixture()
        f.ko["ecl-text"][0] = ("ecl.1", "NEO부대의 첫 단락\\n둘째 단락「안녕」", "ecl-batch-editorial")
        self.assertHas(f.run(), "需加一個半形空白")
        f = self.fixture()
        f.ko["ecl-text"][0] = ("ecl.1", "NEO의 부대 첫 단락\\n둘째 단락「안녕」", "ecl-batch-editorial")
        self.assertEqual(f.run().errors, [])  # 助詞黏寫合法
        f = self.fixture()
        f.ko["ecl-text"][0] = ("ecl.1", "NEO 는 부대의 첫 단락\\n둘째 단락「안녕」", "ecl-batch-editorial")
        self.assertHas(f.run(), "多了空白才接助詞串")
        f = self.fixture()
        f.ko["ecl-text"][0] = ("ecl.1", "NEO로봇 첫 단락\\n둘째 단락「안녕」", "ecl-batch-editorial")
        self.assertHas(f.run(), "需加一個半形空白")  # 完整比對：名詞不被當助詞放行

    def test_item14_forbidden(self) -> None:
        for bad in ("ㅋㅋ", "漢", "~", "·", '"', "Ｈ", "　"):
            f = self.fixture()
            f.ko["story-page9"][0] = ("story.page9.line.001", f"한{bad}마디", "runtime-editorial")
            r = f.run()
            self.assertTrue(r.errors, f"禁用字元 {bad!r} 沒被擋")

    def test_fixed_line_space_edges(self) -> None:
        f = self.fixture()
        f.ko["story-page9"][0] = ("story.page9.line.001", " 한마디", "runtime-editorial")
        self.assertHas(f.run(), "半形空白開頭或結尾")
        f = self.fixture()
        f.ko["story-page9"][0] = ("story.page9.line.001", "한마디 ", "runtime-editorial")
        self.assertHas(f.run(), "半形空白開頭或結尾")


class KoCheckRealData(unittest.TestCase):
    """真實 text/ 的護欄：整套韓文資料通過，且寬度檢查沒有因缺事件檔而靜默略過。"""

    def test_real_data_clean(self) -> None:
        text = lang_check.ROOT / "text"
        if not (text / "hmenu-item-events.tsv").exists() or not (text / "ecl-text.ko.tsv").exists():
            self.skipTest("沒有真實 text/")
        report = lang_check.Report()
        lang_check.check(text, lang_check.ROOT / "font", report, lang="ko", expect_rows=5414, expect_keys=5406)
        self.assertEqual(report.errors, [])

    def test_caps_cover_most_rows(self) -> None:
        text = lang_check.ROOT / "text"
        if not (text / "hmenu-item-events.tsv").exists() or not (text / "hmenu.ko.tsv").exists():
            self.skipTest("沒有真實 text/")
        src = lang_check.load_cap_sources(text)
        covered = total = 0
        for fam, path in lang_check.families(text, "ko").items():
            if fam in ("ecl-text", "logbook", "logbook-panel", "engine-template", "manual"):
                continue
            for r in lang_check.read_catalog_raw(path, lang_check.Report()) or []:
                total += 1
                if lang_check.cap_for(fam, r[0], r[1], src) is not None:
                    covered += 1
        self.assertGreater(covered, 0.95 * total)


if __name__ == "__main__":
    unittest.main()
