# 002 — 手冊查詢繁中段落覆繪

狀態：DRAFT  
前置：[第十一階段事件證據](../re/phase-11-first-manual-check-event-map.md)、
[第十二階段題庫結構](../re/phase-12-manual-question-table-inventory.md)、
[第十三階段繁中來源對照](../re/phase-13-manual-source-crosswalk.md)、
[第十四階段短篇段落](../re/phase-14-manual-compact-paragraphs.md)、
[第十六階段第三批段落](../re/phase-16-manual-compact-paragraphs-3.md)

## 目的

當原版已顯示一個手冊查詢時，dosgolem 可依「頁碼＋英文標題＋序數」找到對應的
繁中手冊段落，在輸出端覆繪顯示。原版的題目抽選、答案輸入、比對與錯答重試都不變。

## DRAFT 映射記錄

權威事件列位於 `text/manual-events.tsv`，目前有 22 筆；每筆保留 record、頁碼、英文標題、
序數及唯一文字鍵。來源定位在 `text/manual-source-crosswalk.tsv`，顯示文字在
`text/manual.zh-TW.tsv`。`show_when` 仍要求同一畫面 generation 已觀測到三個識別欄位；
`answer_input` 永遠由原版處理，不自動填入。版面仍待 2×／3× 與分頁 prototype 決策。

## 失敗即關閉規則

1. 三個原版識別欄位任一缺失、超過同一 generation，或 catalog 沒有唯一命中，不顯示中文段落。
2. 映射只可選擇覆繪文字；不得送鍵、改寫 DOS 記憶體或修改原版程式返回值。
3. 錯答造成重新抽題時，舊段落必須在新題覆繪前失效；不得沿用上一題 metadata。
4. `manual-questions.tsv` 的 39 筆只證明原版 metadata；現階段只登記 22 筆繁中段落，
   未命中其他題目是預期行為，不可用標題模糊比對猜測。
5. `manual-source-crosswalk.tsv` 只證明來源定位；`strong-inference`、`unknown` 或未逐字校訂的
   OCR 內容一律不可當成顯示譯文。

## READY 前置

- 逐字校訂可用中文段落；解決 3 筆強推論與 `Roll.` 缺頁，或為它們訂出明確的失敗即關閉政策。
- 原版覆繪位置、分頁、輸入提示保留與錯答重抽都有同狀態 A/B 收據。
- 通過未命中、重複標題、過期 generation 與 catalog 缺漏的失敗即關閉測試。
