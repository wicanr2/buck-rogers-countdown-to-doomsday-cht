"""規格 041 §5.1：zh_cn_convert 的正向與合成負例。

需要 OpenCC（buck-zhcn-opencc:1.4.2 image）；其他 image 內自動略過。
"""
from __future__ import annotations

import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

try:
    import opencc  # noqa: F401
    HAVE_OPENCC = True
except ImportError:  # pragma: no cover
    HAVE_OPENCC = False

import zh_cn_convert as z

ROOT = Path(__file__).resolve().parents[1]
SHA_LIST = ROOT / "tools" / "docker" / "opencc" / "opencc-dicts.sha256"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.write_text("\t".join(header) + "\n" + "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")


@unittest.skipUnless(HAVE_OPENCC, "需要 OpenCC（buck-zhcn-opencc image）")
class ZhCnConvertTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        (self.dir / "text").mkdir()
        (self.dir / "tools" / "docker" / "opencc").mkdir(parents=True)
        shutil.copy(SHA_LIST, self.dir / "tools" / "docker" / "opencc" / "opencc-dicts.sha256")
        self.families = {"alpha": [["a.1", "雷射開火了。"], ["a.2", "載入中"]],
                         "beta": [["b.1", "螢幕上出現巴克羅吉斯。"]]}
        self.phrases = [["載入", "读取", "map", "使用者定案"]]
        self.overrides: list[list[str]] | None = None
        self.names = [["BUCK ROGERS", "Buck Rogers", "巴克羅吉斯", "full", "buck-rogers", "xinhua", ""]]
        self.excludes: list[list[str]] = []
        self.translit = ["丁", "丘", "發"]

    def tearDown(self):
        shutil.rmtree(self.dir)

    def write(self):
        t = self.dir / "text"
        for p in t.glob("*.zh-TW.tsv"):
            p.unlink()
        for fam, rows in self.families.items():
            tsv(t / f"{fam}.zh-TW.tsv", z.CATALOG_HEADER, [[k, v, "runtime"] for k, v in rows])
        tsv(t / "zh-CN-phrases.tsv", z.PHRASE_HEADER, self.phrases)
        if self.overrides is not None:
            tsv(t / "zh-CN-overrides.tsv", z.OVERRIDE_HEADER, self.overrides)
        elif (t / "zh-CN-overrides.tsv").exists():
            (t / "zh-CN-overrides.tsv").unlink()
        tsv(t / "name-glossary.tsv", z.GLOSSARY_HEADER, self.names)
        tsv(t / "name-glossary-exclude.tsv", z.EXCLUDE_HEADER, self.excludes)
        tsv(t / "translit-chars.zh-TW.tsv", z.CATALOG_HEADER,
            [[f"translit.char.U+{ord(c):04X}", c, "translit-table"] for c in self.translit])

    def run_(self, review=True):
        self.write()
        return z.run(self.dir, review=review)

    def ledger_from(self, res):
        tsv(self.dir / "text" / "zh-CN-term-review.tsv", z.LEDGER_HEADER,
            [[r["family"], r["key"], r["zh_tw_sha256"], str(r["occurrence"]), r["term_id"], "ok", ""] for r in res.review])

    def assertError(self, res, needle):
        text = "\n".join(res.errors + res.ledger_errors)
        self.assertIn(needle, text)

    # ---------------------------------------------------------------- 正向

    def test_positive_tracking_determinism_and_check(self):
        res = self.run_()
        self.assertEqual(res.errors, [])
        self.ledger_from(res)
        res2 = self.run_()
        self.assertEqual(res2.errors, [])
        self.assertEqual(res2.ledger_errors, [])
        self.assertEqual(res.outputs, res2.outputs)  # 兩次產生位元組相同
        out = res.outputs["text/alpha.zh-CN.tsv"].decode()
        self.assertIn("激光开火了。", out)
        self.assertIn("读取中", out)
        self.assertIn("巴克罗吉斯", res.outputs["text/name-glossary.zh-CN.tsv"].decode())
        for rel, data in res2.outputs.items():
            (self.dir / rel).write_bytes(data)
        self.assertEqual(z.main(["--root", str(self.dir), "--check"]), 0)
        # 手工改動產生檔 → --check 失敗
        p = self.dir / "text" / "alpha.zh-CN.tsv"
        p.write_text(p.read_text(encoding="utf-8").replace("激光", "雷射"), encoding="utf-8")
        self.assertEqual(z.main(["--root", str(self.dir), "--check"]), 1)

    # ---------------------------------------------------------------- 負例

    def test_invariant_violation(self):
        self.phrases = [["載入", "读取X", "map", "t"]]
        self.assertError(self.run_(), "去掉漢字後的字元序列")

    def test_count_mismatch(self):
        self.families["alpha"].append(["a.3", "核心區"])
        self.phrases.append(["核心", "核", "keep", "t"])
        res = self.run_()
        self.assertError(res, "keep 詞條不得改變字數")
        self.assertError(res, "不等於套用詞條長度差")

    def test_override_hash_mismatch(self):
        self.overrides = [["alpha", "a.1", "0" * 64, "激光开火了。", "t"]]
        self.assertError(self.run_(), "zh-TW 雜湊不符")

    def test_orphan_override(self):
        self.overrides = [["alpha", "a.9", sha("x"), "x", "t"]]
        self.assertError(self.run_(), "孤兒")

    def test_override_invariant(self):
        self.overrides = [["alpha", "a.1", sha("雷射開火了。"), "激光开火了！", "t"]]
        self.assertError(self.run_(), "覆寫 alpha:a.1: 去掉漢字後")

    def test_phrase_whitespace(self):
        self.phrases.append(["雷 射", "雷射", "keep", "t"])
        self.assertError(self.run_(), "不得為空或含空白")

    def test_phrase_not_matched(self):
        self.phrases.append(["程序", "程序", "keep", "t"])
        self.assertError(self.run_(), "沒有實際匹配")

    def test_occurrence_not_matched_nor_covered_and_category3(self):
        # 同一列另有實際匹配，使「不套用該詞條」的輸出不同，類 3 不能豁免。
        self.families["alpha"] += [["a.3", "記憶體和憶體"]]
        self.phrases.append(["憶體", "内存", "map", "t"])
        res = self.run_()
        self.assertError(res, "未匹配也未被較長 guard／map 覆蓋")
        self.assertError(res, "（類 3）")

    def test_masking_category1(self):
        self.families["alpha"].append(["a.3", "無法載入執行檔"])
        self.phrases.append(["執行", "执行", "keep", "t"])
        self.assertError(self.run_(), "類 1")

    def test_masking_category1_fixed_by_guard(self):
        self.families["alpha"] += [["a.3", "無法載入執行檔"], ["a.4", "執行任務"]]
        self.phrases += [["執行", "执行", "keep", "t"], ["執行檔", "可执行文件", "guard", "t"]]
        self.assertEqual(self.run_().errors, [])

    def test_masking_category2(self):
        self.families["alpha"].append(["a.3", "許多工程師"])
        self.phrases.append(["許多", "许多", "keep", "t"])
        self.assertError(self.run_(), "類 2")

    def test_ledger_missing_and_new(self):
        res = self.run_()
        self.ledger_from(res)
        rows = (self.dir / "text" / "zh-CN-term-review.tsv").read_text(encoding="utf-8").splitlines()
        (self.dir / "text" / "zh-CN-term-review.tsv").write_text("\n".join(rows[:-1]) + "\n", encoding="utf-8")
        self.families["beta"].append(["b.2", "滑鼠"])
        res = self.run_()
        self.assertError(res, "帳本缺項或新套用處")
        self.assertIn("b.2", "\n".join(res.ledger_errors))

    def test_ledger_hash_and_stale(self):
        res = self.run_()
        self.ledger_from(res)
        self.families["alpha"][0][1] = "雷射再次開火了。"
        self.families["alpha"] = self.families["alpha"][:1]
        res = self.run_()
        self.assertError(res, "zh-TW 雜湊不符")
        self.assertError(res, "帳本多出不存在的套用處")

    def test_ledger_manual_note(self):
        self.families["manual"] = [["m.1", "雷射"]]
        res = self.run_()
        self.ledger_from(res)
        p = self.dir / "text" / "zh-CN-term-review.tsv"
        p.write_text(p.read_text(encoding="utf-8").replace("\tok\t\n", "\tok\tx\n"), encoding="utf-8")
        self.assertError(self.run_(), "手冊家族 note 必須留空")

    def test_name_inconsistent(self):
        self.names.append(["MEMORY", "", "記憶", "short", "memory", "xinhua", ""])
        self.families["alpha"].append(["a.3", "記憶體不足"])
        self.assertError(self.run_(), "名字「記憶」")

    def test_chinese_duplicate(self):
        self.names += [["AFA", "", "阿發", "short", "afa", "xinhua", ""], ["AFAA", "", "阿髮", "short", "afaa", "xinhua", ""]]
        self.assertError(self.run_(), "chinese 轉換後重複")

    def test_exclude_phrase_inconsistent(self):
        self.excludes = [["記憶", "*", "t"]]
        self.families["alpha"].append(["a.3", "記憶體不足"])
        self.assertError(self.run_(), "例外片語「記憶」")

    def test_cross_family_inconsistent(self):
        self.families["gamma"] = [["g.1", "資料"]]
        self.families["beta"].append(["b.2", "找到資料了"])
        self.overrides = [["gamma", "g.1", sha("資料"), "资料", "t"]]
        self.assertError(self.run_(), "跨家族不一致")

    def test_translit_collision(self):
        self.translit = ["丁", "發", "髮"]
        self.assertError(self.run_(), "音譯對照碰撞")


if __name__ == "__main__":
    unittest.main()
