# 025 — 儲存詢問的名字前後綴覆繪

狀態：DRAFT
範圍：身體圖示確認 Y 之後的 `Save <角色名>? ` 儲存詢問
更新：2026-09-26

本規格取代[規格 009](009-body-icon-overlay-draft.md) 中 `body.icon.save_prompt`
那一列的固定 SHA 身分。009 的其他六筆、群組、失效與零污染契約不變。

證據入口：

- [第二百四十四階段：儲存詢問名字模板證據](../re/phase-244-save-prompt-name-template.md)
- [第二百四十三階段：正常命名直播鏈](../re/phase-243-named-live-chain-ab.md)
- [第四十九階段：儲存詢問與角色完成生命週期](../re/phase-49-save-prompt-and-character-completion-lifecycle.md)

## 問題

儲存詢問由 `37F1:101E` 一次送出，內容是固定前綴、玩家輸入的名字、固定後綴。
現行 catalog 鎖定名字 `A` 的 8 字版本；其他名字的長度與 SHA 都不同，正式
watcher 會失敗即關閉，confirm 路徑無法覆繪。

## 已證實事實

| 項目 | 事實 | 等級 |
|---|---|---|
| 名字長度 | 1–15 字；第 16 字起不回顯也不寫入 | 已證實 |
| 名字字元 | 接受字母、數字、空白、`.`、`?`；小寫存成大寫 | 已證實（抽樣） |
| 詢問組成 | 前綴 5 bytes、名字 n bytes、後綴 2 bytes，總長 `7+n` | 已證實（n=1、4、5、15） |
| 前綴 SHA-256 | `f5f25c5769e6107d2cec7dec87265599a9af37156f30add96e2a6daa2d4a4658` | 已證實 |
| 後綴 SHA-256 | `23eeade931d8902dde575f26bb466a3c786484e46471efa7fa5b054636e7298b` | 已證實 |
| 呼叫與樣式 | caller `37F1:101E`、背景 0、前景 13、row 24、column 0 | 已證實 |

名字本身可含 `?`，所以後綴一律取最後 2 bytes，不搜尋分隔字元。

## DRAFT 契約

1. **身分**：事件符合 caller、背景、前景、row、column，且
   `8 ≤ 長度 ≤ 22`、前 5 bytes 與後 2 bytes 的 SHA-256 分別等於上表，才算
   `body.icon.save_prompt`。記錄器只保存前後綴 SHA 與名字長度 n，
   **不保存名字 bytes**。
2. **譯文**：`text/body-icon.zh-TW.tsv` 分成兩筆：
   `body.icon.save_prompt.prefix`（「儲存」）與
   `body.icon.save_prompt.suffix`（「？」）。舊的單筆 `body.icon.save_prompt`
   譯文移除。
3. **幾何**：兩個 stamp，名字格不覆繪。
   - 前綴矩形 `[0,40)×[192,200)`，5 格，「儲存」兩字佔 4 格，第 5 格留底色。
   - 後綴矩形 `[(5+n)·8, (7+n)·8)×[192,200)`，2 格，「？」佔滿。
   - 名字格 `[40, (5+n)·8)` 保留原版墨跡，overlay 在此區必須零差。
4. **生命週期**：兩個 stamp 屬同一群組 `save_prompt`，同一 generation 建立；
   任何 A000 寫入與任一矩形相交時，兩個 stamp 一起失效。其餘沿用規格 009。
5. **失敗即關閉**：caller 與樣式相符但前後綴 SHA 不符、長度越界，都視為身分
   不符並停止 watcher，不退回固定 SHA 比對。

## READY 前待補

- 獨立審查本規格與第二百四十四階段證據。
- 確認 dispatcher 在單次呼叫內依序繪出整串，名字格不會被其他寫入者先寫。
- 確認「？」在倚天 2×／3× 的 2 格內 containment 零越界。

## 驗收（CONFORMED 條件）

名字 `Z`、`BUCK`、`A 1.?`、`ABCDEFGHIJKLMNO` 四條 confirm 路徑，各做
control／2×／3×：原版狀態、indexed、FileOps 相等；差異只在兩個矩形內；
名字格零差；離頁無殘層。
