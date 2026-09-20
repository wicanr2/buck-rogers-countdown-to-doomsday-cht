# 第二十階段：手冊 catalog 顯示請求 prototype

日期：2026-09-20  
狀態：可丟棄 prototype 已通過正式 TSV 與負向測試；規格仍為 DRAFT。

## 目的與語意邊界

本階段把第十九階段的完整 runtime 題目身分接到正式 `manual-events.tsv` 與
`manual.zh-TW.tsv`。輸出只是一筆顯示請求；原版英文題目、答案、輸入、比較與存檔均不讀寫。
翻譯只存在 UTF-8 TSV，prototype 程式碼不內嵌繁中段落。

## 輸入與收據

- `text/manual-events.tsv` SHA-256：
  `bbf9c9058363b475858171b66048be6e2bb388eb73fa0fc7134e7092963efb6f`
- `text/manual.zh-TW.tsv` SHA-256：
  `cea5474ebcf41eab7a8c64c5d2ca7639c871931fd4cd18ba3fa85549fc97d1bb`
- `workplace/phase20/manual_display_request.py` SHA-256：
  `bd8eae504126d028f358cf0eb81b2314db888b0a81a3cbc0a5d91aa9dc5e9e95`
- `workplace/phase20/test_manual_display_request.py` SHA-256：
  `5ffe96fa896e82a063923cbff6e45ceda0df24d9b2d3e2efb79f55ae2fd66d4c`
- 執行環境：`python:3.13-bookworm`，無網路、一次性容器。

prototype 與測試留在被 Git 忽略的 `workplace/phase20/`，不屬於 production 實作。

## 發現的 ordinal 介面缺口

runtime 題目顯示的是英文序數詞；正式事件 TSV 保存數字。dosgolem 目前動態證實兩筆：

| runtime 字串 | 數字 | 題目 | 等級 |
| --- | ---: | --- | --- |
| `tenth` | 10 | `Deimos Prison` | 已證實 |
| `second` | 2 | `Technical Skills` | 已證實 |

prototype 只接受這兩筆對照。其餘 `first`、`third` 等雖屬常見英文，尚未由本遊戲的輸出事件
逐項證實，故不批次寫入正式資料；遇到未登記序數詞即不顯示。完整 22 筆 catalog 要進正式
runtime 前，仍須由原版資料或可重播事件建立完整、可稽核的序數橋接。

## Typed lookup 契約

輸入為 `generation + RuntimeQuestion(page, heading, ordinal_word)`，輸出最多一筆：

`DisplayRequest(generation, event_key, text_key, translation)`。

解析順序如下：

1. generation 必須為正值且等於目前 generation。
2. ordinal word 必須存在於已證實對照；否則不顯示。
3. `(page, heading_ascii, ordinal)` 必須精確命中唯一事件；不做大小寫折疊、相近標題、頁碼
   fallback 或模糊搜尋。
4. event 的 `text_key` 必須唯一存在於繁中 catalog；translation 與 source 不得為空。
5. event identity、event key、event text key、catalog key 均須唯一，catalog 不得有孤兒鍵。
6. TSV 必須是無 BOM 的嚴格 UTF-8，標頭與欄數須符合契約。

顯示請求沒有 answer、input、record mutation 或 save 欄位。這是顯示／語意隔離的 prototype
證據，不代表尚未實作的 dosgolem adapter 已符合。

## 正向與未命中收據

已收錄且動態 ordinal 已證實的 `34 / Deimos Prison / tenth` 唯一命中：

- event key：`manual.page34.deimos_prison.word10`
- text key：`manual.log.49.deimos_prison`
- translation：73 個 Unicode 字元（全文只由正式 TSV 讀入，不複製到收據）

第十九階段真實鍵 `41 / Technical Skills / second` 的來源雖已確認，但沒有完整校訂段落及事件
列，因此回傳未命中。prototype 沒有借用相近技能條目、只顯示標題或臨時加入譯文。

## 負向測試

12 項測試全部通過，涵蓋：

- stale generation；
- heading 大小寫差異、未證實 ordinal 拼法及未登記 ordinal；
- 重複題目身分、事件鍵、事件文字鍵與 catalog key；
- catalog 孤兒鍵；
- 無效 UTF-8；
- ordinal 對照多對一歧義；
- 未收錄的 `Technical Skills` 不顯示；
- 顯示請求欄位不含答案。

## 結論與下一步

從 runtime 題目身分到正式繁中 catalog 的精確、唯一、失敗即關閉路徑已由 prototype 證實。
新增的實質缺口是完整 ordinal bridge；在它、倍率決策、正式 adapter、畫面 A/B 與分頁輸入
完成前，spec 不升 READY，prototype 不進 production。
