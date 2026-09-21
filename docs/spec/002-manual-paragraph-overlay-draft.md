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
[第二十二階段整數倍率 renderer](../re/phase-22-dosgolem-xlate-integer-scale.md)、
[第二十三階段事件 adapter](../re/phase-23-manual-event-adapter.md)、
[第二十四階段 runtime watcher](../re/phase-24-manual-runtime-watcher.md)、
[第六十階段 READY 前置稽核](../re/phase-60-manual-overlay-ready-prerequisite-audit.md)

## 目的

當原版已顯示一個手冊查詢時，dosgolem 可依「頁碼＋英文標題＋序數」找到對應的
繁中手冊段落，在輸出端覆繪顯示。原版的題目抽選、答案輸入、比對與錯答重試都不變。

## DRAFT 映射記錄

權威事件列位於 `text/manual-events.tsv`，目前有 22 筆；每筆保留 record、頁碼、英文標題、
序數及唯一文字鍵。來源定位在 `text/manual-source-crosswalk.tsv`，顯示文字在
`text/manual.zh-TW.tsv`。`show_when` 仍要求同一畫面 generation 已觀測到三個識別欄位；
`answer_input` 永遠由原版處理，不自動填入。版面仍待 2×／3× 決策。

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

第二十三階段將事件收集、原版序數橋接與精確 catalog lookup 切成獨立 READY 子規格，並在
dosgolem `apps/buckrogers` 實作未接線純核心。正式 TSV 正向／未命中與失敗即關閉測試均通過；
核心不接 oracle、xlate、輸入或答案。總體規格仍須等 runtime hook、倍率、分頁與 A/B 收據，
因此維持 DRAFT。

第二十四階段已把純核心接上正式 runtime watcher；原版固定狀態能在
`#266,557,246` 對 `manual.page34.deimos_prison.word10` 產生唯一顯示請求，而正式 catalog
未收錄的 `41 / Technical Skills / second` 只完成題目事件、請求數維持 0。第六十階段再以
目前資料重驗：39 筆題庫中 35 筆來源已證實、3 筆為強推論、1 筆未知；正式事件與譯文各
22 筆，最長譯文 236 字，全部可放入 36×17＝612 字的單頁正文。故目前正式 catalog 不需要
新增分頁按鍵或頁尾提示；未來若新增超過單頁的譯文，須另開 DRAFT 規格，不能默認截斷、
送鍵或接管原版輸入。

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
10. 目前只顯示 22 筆已逐字校訂且來源為 `confirmed` 的單頁譯文；其餘 17 筆即使來源已
    證實，只要未列入正式事件與譯文 catalog，就維持原版英文。3 筆 `strong-inference`、
    1 筆 `unknown` 以及任何未校訂內容一律不得猜補。
11. 正式 catalog 的單筆譯文必須不超過 612 個 Unicode 字元；`tools/manual_catalog.py`
    已在載入／驗證時對 613 字以上資料失敗即關閉，不能靜默截斷。此界線不預先決定未來
    多頁內容的操作方式。

## READY 前置（實作前契約）

- [x] 22 筆可用中文段落均已逐字校訂、來源為 `confirmed`，且以 exact identity 接到 catalog。
- [x] 其餘 17 題已有明確失敗即關閉政策；不要求先解決 3 筆強推論與 `Roll.` 缺頁。
- [x] 未命中、重複標題、過期 generation、catalog 缺漏與 ordinal 異常均有負向測試。
- [x] READY 純核心已接上已驗證的 dispatcher entry／guarded post-call，並有真實固定狀態收據。
- [x] 目前 22 筆譯文都能單頁顯示；612 字通過、613 字失敗即關閉，本範圍不新增分頁輸入
  或頁尾提示。
- [ ] 使用者確認正式輸出倍率為 2× 或 3×，將所選倍率、像素原點與安全矩形寫成固定契約。

## CONFORMED 驗收（實作後收據）

- 正常玩家路徑只在完整題目 `word?` guarded post-call 後顯示中文，不誤收其他字串。
- 選定倍率下的中文 ink 完全落在 `[7,312)×[7,184)` 安全矩形，矩形外 0 px 差異。
- 錯答重抽時舊 generation 先失效，新段落只在新題身分完整後出現；舊段落不得殘留。
- catalog miss、未校訂題目與超限譯文不畫中文；原版英文與原版答案輸入仍可操作。
- 同資料、同初始狀態、同輸入與固定 seed（若涉及亂數）的原文／繁中 A/B，除核准覆繪像素
  外，事件、輸入、原版 framebuffer、記憶體、檔案操作與存檔不得改變。
