# 002 — 手冊查詢繁中段落覆繪

狀態：DRAFT  
前置：[第十一階段事件證據](../re/phase-11-first-manual-check-event-map.md)、
[第十二階段題庫結構](../re/phase-12-manual-question-table-inventory.md)

## 目的

當原版已顯示一個手冊查詢時，dosgolem 可依「頁碼＋英文標題＋序數」找到對應的
繁中手冊段落，在輸出端覆繪顯示。原版的題目抽選、答案輸入、比對與錯答重試都不變。

## DRAFT 映射記錄

| 欄位 | 本題值 |
| --- | --- |
| `event_key` | `manual.page34.deimos_prison.word10` |
| `page` | `34` |
| `heading_ascii` | `Deimos Prison` |
| `ordinal_ascii` | `tenth` |
| `text_key` | `manual.log.49.deimos_prison` |
| `source_scan` | archive-order 66 / `SCAN0352_039.jpg` / 印刷頁 73 |
| `show_when` | 同一畫面 generation 已觀測到頁碼、標題與序數後 |
| `answer_input` | 原版英文輸入與判定；不自動填入 |
| `layout` | 待定；須依使用者選定 2×／3× 後做分頁 prototype |

## 失敗即關閉規則

1. 三個原版識別欄位任一缺失、超過同一 generation，或 catalog 沒有唯一命中，不顯示中文段落。
2. 映射只可選擇覆繪文字；不得送鍵、改寫 DOS 記憶體或修改原版程式返回值。
3. 錯答造成重新抽題時，舊段落必須在新題覆繪前失效；不得沿用上一題 metadata。
4. `manual-questions.tsv` 的 39 筆只證明原版 metadata；現階段仍只登記一筆繁中段落，
   未命中其他題目是預期行為，不可用標題模糊比對猜測。

## READY 前置

- 盤點並反向驗證所有可抽題的頁碼與標題，每筆有獨立中文掃描來源。
- 原版覆繪位置、分頁、輸入提示保留與錯答重抽都有同狀態 A/B 收據。
- 通過未命中、重複標題、過期 generation 與 catalog 缺漏的失敗即關閉測試。
