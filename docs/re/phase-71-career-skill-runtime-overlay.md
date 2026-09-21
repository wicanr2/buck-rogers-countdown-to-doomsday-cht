# 第七十一階段：職業技能配置執行期繁中覆繪

日期：2026-09-21  
狀態：完成

## 結論

14 個已證實的標題／技能 identities 已以原文起點與長度建立安全矩形，並接入
dosgolem 長存 runtime overlay。base 與 Down 的 2×／3× 收據均只改動輸出 RGBA；原版
framebuffer、events、BIOS keys 與動態技能點數不變。

## 幾何與生命週期

- 四個標題右界最遠 x=168；技能列右界最遠 x=136。數值欄從 x=184 開始。
- base 終態是注意力 selected／無重力行動 normal；Down 後改為注意力 normal／
  無重力行動 selected。同一位置沒有 normal 與 selected stamp 並存。
- 姓名提示的 stamp 在 Enter 轉場後已由通用清除 hook 失效，技能頁無殘字。

## 正式收據

| 路徑 | requests／misses | 2× 矩形內差異 | 3× 矩形內差異 | 矩形外／動態欄 |
|---|---:|---:|---:|---:|
| base | 14／212 | 11,280 px | 22,791 px | 0／0 px |
| Down | 16／218 | 11,280 px | 22,791 px | 0／0 px |

八組 JSON、RGBA、baseline 與 raw framebuffer 由
`tools/career_skill_runtime_overlay_receipt.py` 對照 Phase 70 control。字型 SHA-256 為
`63bbc98f9397e5e866fec8b0b135d85b6f9ad245586b60550dca9ab4d7789975`。每組 A／B 逐位元一致。

## 邊界

本階段沒有翻譯 ADD／SUBTRACT／DONE，沒有新增未實測 selected variants，也沒有選定
產品預設倍率或手冊版面。
