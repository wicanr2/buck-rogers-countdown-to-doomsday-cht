# 002 — 手冊查詢繁中段落覆繪

狀態：DRAFT  
前置：[第十一階段事件證據](../re/phase-11-first-manual-check-event-map.md)、
[第十二階段題庫結構](../re/phase-12-manual-question-table-inventory.md)、
[第十三階段繁中來源對照](../re/phase-13-manual-source-crosswalk.md)、
[第十四階段短篇段落](../re/phase-14-manual-compact-paragraphs.md)、
[第十六階段第三批段落](../re/phase-16-manual-compact-paragraphs-3.md)、
[第十七階段分頁與倍率 prototype](../re/phase-17-manual-pagination-scale-prototype.md)、
[第十八階段題目世代與失效](../re/phase-18-manual-generation-invalidation.md)、
[第十九階段事件收集器 prototype](../re/phase-19-manual-event-collector-prototype.md)、
[第二十階段 catalog 顯示請求 prototype](../re/phase-20-manual-catalog-display-request-prototype.md)、
[第二十一階段序數詞橋接](../re/phase-21-manual-ordinal-bridge-evidence.md)、
[第二十二階段整數倍率 renderer](../re/phase-22-dosgolem-xlate-integer-scale.md)

## 目的

當原版已顯示一個手冊查詢時，dosgolem 可依「頁碼＋英文標題＋序數」找到對應的
繁中手冊段落，在輸出端覆繪顯示。原版的題目抽選、答案輸入、比對與錯答重試都不變。

## DRAFT 映射記錄

權威事件列位於 `text/manual-events.tsv`，目前有 22 筆；每筆保留 record、頁碼、英文標題、
序數及唯一文字鍵。來源定位在 `text/manual-source-crosswalk.tsv`，顯示文字在
`text/manual.zh-TW.tsv`。`show_when` 仍要求同一畫面 generation 已觀測到三個識別欄位；
`answer_input` 永遠由原版處理，不自動填入。版面仍待 2×／3× 與分頁 prototype 決策。

第十七階段由真實手冊畫面量得安全矩形 `[7,312)×[7,184)`；保留內距後的 prototype
正文為 36 欄×17 行、每頁 612 字。2×／3× 使用相同邏輯格，頁數一致；兩案均已驗證
安全矩形外 0 px 變更。這只證明靜態幾何可行，不證明分頁輸入、錯答重抽或 generation
失效。倍率仍待使用者決定，因此不得把任一候選寫入 production 路徑。

第十八階段證實錯答換題不會先把畫面整面清空：固定題首、頁碼與提示先逐筆覆寫，
`026F:029C` 的局部矩形清除才在中途出現。因此 DRAFT adapter 應以
`2A33:01ED → 0763:0424` 的精確題首 entry 開啟新 generation 並立即丟棄舊段落；累積
頁碼、標題與序數後，只在 `2A33:0309` 的 `word?` guarded post-call 才允許解析並覆繪。
不得等待空白畫面，也不得在第一筆或頁碼出現後提前畫中文。

第十九階段把上述事件收斂為 typed lifecycle：`idle → pending(generation, stage, page?,
heading?, ordinal?) → visible(key)`。pending frame 在 dispatcher entry 綁定 generation；只有同
generation、正確 caller、正確順序及合法內容的 guarded post-call 能推進。任何驗證失敗都
poison 該 generation，下一個精確題首才能復原。矩形清除可移除 visible，但不得提交或重設
pending。此模型已通過可丟棄 prototype，尚未授權 production 實作。

第二十階段將完整題目身分接到正式 TSV：只允許 `(page, heading_ascii, ordinal)` 精確唯一
命中，再由唯一 `text_key` 取得繁中段落。輸出型別只含 generation、event key、text key 與
translation，不得含答案、輸入或原版狀態寫入。

第二十一階段已由原版 consumer 證實 `record[+14] × 19 + DS:339B` 的 1–10 序數表，並以
`text/manual-ordinals.tsv` 保存每筆 runtime 位址與原始 19-byte slot。adapter 必須從這份
受驗資料做 ordinal word→number 精確橋接；表外、大小寫不同或 bytes 不符仍失敗即關閉。

第二十二階段已讓 dosgolem 通用 `xlate` renderer 接受正整數倍率，並以真實 16×16
GOLEMFNT 驗證 2×／3×；非法倍率失敗即關閉、目的緩衝區外安全裁切。這只移除 2× 的工具
限制，不等於選定正式倍率，也不構成遊戲 adapter 或正常玩家路徑完成證據。

## 失敗即關閉規則

1. 三個原版識別欄位任一缺失、超過同一 generation，或 catalog 沒有唯一命中，不顯示中文段落。
2. 映射只可選擇覆繪文字；不得送鍵、改寫 DOS 記憶體或修改原版程式返回值。
3. 錯答造成重新抽題時，舊段落必須在新題覆繪前失效；不得沿用上一題 metadata。
4. `manual-questions.tsv` 的 39 筆只證明原版 metadata；現階段只登記 22 筆繁中段落，
   未命中其他題目是預期行為，不可用標題模糊比對猜測。
5. `manual-source-crosswalk.tsv` 只證明來源定位；`strong-inference`、`unknown` 或未逐字校訂的
   OCR 內容一律不可當成顯示譯文。
6. 新題題首出現時須先清除上一 generation 的段落與 metadata；中途矩形清除只維持 pending，
   不可建立題目身分。到 `word?` guarded post-call 前，任何中文手冊段落都不得顯示。
7. pending frame 必須帶 generation；舊 generation 延遲返回、亂序、重複或未知 caller 不得
   推進目前題目。失敗後不可使用部分 metadata，須等下一個精確題首重新開始。
8. catalog lookup 不得做大小寫折疊、模糊標題、近似頁碼或相鄰條目 fallback。ordinal word
   未在已證實橋接表時，即使 page 與 heading 命中也不得顯示。
9. 翻譯只由 UTF-8 TSV catalog 取得；顯示請求不得攜帶答案或改變原版語意狀態。

## READY 前置

- 逐字校訂可用中文段落；解決 3 筆強推論與 `Roll.` 缺頁，或為它們訂出明確的失敗即關閉政策。
- 原版覆繪位置、分頁與輸入提示保留都有同狀態 A/B 收據；錯答重抽須在 adapter 實作後補
  「舊覆蓋先失效、新覆蓋只在完整題目後出現」的同狀態 A/B 收據。
- 通過未命中、重複標題、過期 generation 與 catalog 缺漏的失敗即關閉測試。
- 將第十九階段 prototype 的同世代、跨世代、亂序與 poisoned 復原案例轉成正式 adapter 測試。
- 正式 adapter 讀取並驗證 `manual-ordinals.tsv`，以全套 catalog lookup 測試證明沒有回退
  到程式碼內嵌序數或模糊比對。
- 使用者確認 2×／3×，並為選定倍率補齊正常玩家路徑、覆繪 containment 與分頁互動收據。
