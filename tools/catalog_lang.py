"""規格 040 §3.1：catalog 語言代碼與檔名 `<family>.<lang>.tsv`（預設 zh-TW，行為不變）。"""
from __future__ import annotations

DEFAULT_LANG = "zh-TW"
# F4 循環的語言；zz 是測試專用假語言（只在 workplace 測試資料，不進 text/ 與發行包）。
KNOWN_LANGS = ("zh-TW", "zh-CN", "en", "ja", "ko", "zz")


def check_lang(lang: str) -> str:
    if lang not in KNOWN_LANGS:
        raise ValueError(f"不認得的語言代碼 {lang!r}")
    return lang


def catalog_name(family: str, lang: str = DEFAULT_LANG) -> str:
    """家族譯文檔名，例如 catalog_name("menu") == "menu.zh-TW.tsv"。"""
    return f"{family}.{check_lang(lang)}.tsv"


def catalog_glob(lang: str = DEFAULT_LANG) -> str:
    return f"*.{check_lang(lang)}.tsv"


def add_lang_argument(parser) -> None:
    parser.add_argument("--lang", default=DEFAULT_LANG, choices=KNOWN_LANGS,
                        help="譯文語言（規格 040；預設 zh-TW）")
