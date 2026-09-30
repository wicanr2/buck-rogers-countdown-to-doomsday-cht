#!/usr/bin/env python3
"""規格 043 §3.3：韓文（ko）譯文檢查。共用邏輯在 tools/lang_check.py，本檔是薄包裝。

  python3 tools/ko_check.py                       檢查 text/*.ko.tsv
  python3 tools/ko_check.py --expect-rows 5414 --expect-keys 5406   加覆蓋斷言（規格 043 §3.1）
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lang_check as _lc  # noqa: E402

LANG = "ko"


def check(text_dir, font_dir, report, *, expect_rows=None, expect_keys=None):
    _lc.check(text_dir, font_dir, report, expect_rows=expect_rows, expect_keys=expect_keys, lang=LANG)


def main(argv=None):
    return _lc.main(argv, default_lang=LANG)


if __name__ == "__main__":
    sys.exit(main())
