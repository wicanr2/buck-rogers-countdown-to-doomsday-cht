#!/usr/bin/env python3
"""規格 042 §3.3：日文（ja）譯文檢查。共用邏輯在 tools/lang_check.py（規格 043 §3.3），本檔是薄包裝：命令列與舊名稱不變。

  python3 tools/ja_check.py                       檢查 text/*.ja.tsv
  python3 tools/ja_check.py --expect-rows 5453 --expect-keys 5445   加覆蓋斷言（規格 042 §3.1）
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lang_check as _lc  # noqa: E402
from lang_check import (  # noqa: E402,F401  舊名稱原名轉出（test_ja_check.py 直接使用）
    ROOT, Report, cap_for, families, load_cap_sources, read_catalog_raw, units,
)

LANG = "ja"


def check(text_dir, font_dir, report, *, expect_rows=None, expect_keys=None):
    _lc.check(text_dir, font_dir, report, expect_rows=expect_rows, expect_keys=expect_keys, lang=LANG)


def main(argv=None):
    return _lc.main(argv, default_lang=LANG)


if __name__ == "__main__":
    sys.exit(main())
