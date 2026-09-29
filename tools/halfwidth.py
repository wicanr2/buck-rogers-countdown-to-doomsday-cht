#!/usr/bin/env python3
"""規格 039：覆繪半形英數字的單位與字模墨跡規則（與 dosgolem apps/buckrogers/halfwidth.go 一致）。

- 半形單位＝4 邏輯像素；U+0020–U+007E 與 U+2022（•）各 1 單位，其他字元 2 單位。
- 16×16 GOLEMFNT 內的半形字模墨跡必須完全落在第 4–11 欄（執行期取這 8 欄為 8×16 半形字模）。
"""

from __future__ import annotations

HALFWIDTH_CODEPOINTS = frozenset(range(0x20, 0x7F)) | {0x2022}
HALF_INK_MASK = 0x0FF0  # 16 像素一列中的第 4–11 欄（MSB 為第 0 欄）


def is_halfwidth(ch: str) -> bool:
    return ord(ch) in HALFWIDTH_CODEPOINTS


def half_units(text: str) -> int:
    """文字寬度（半形單位）。"""
    return sum(1 if is_halfwidth(ch) else 2 for ch in text)


def halfwidth_ink_error(codepoint: int, bitmap: bytes) -> str | None:
    """16×16 字模（32 bytes）若為半形字且墨跡超出第 4–11 欄，回傳錯誤訊息。"""
    if codepoint not in HALFWIDTH_CODEPOINTS:
        return None
    if len(bitmap) != 32:
        return f"U+{codepoint:04X}: 半形字模必須為 16×16（32 bytes）"
    for y in range(16):
        row = bitmap[2 * y] << 8 | bitmap[2 * y + 1]
        if row & ~HALF_INK_MASK & 0xFFFF:
            return f"U+{codepoint:04X}: 半形字墨跡超出第 4–11 欄（規格 039 §3.2，第 {y} 列）"
    return None
