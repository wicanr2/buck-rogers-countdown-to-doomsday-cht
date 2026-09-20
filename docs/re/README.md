# 原版觀測證據索引

此目錄保存 dosgolem 的原版行為收據與推論分級，不保存原版遊戲、手冊、可還原素材或
其完整輸出。所有位址均須標明使用的位址空間；不可把 IDA 線性位址與 dosgolem 執行期
段位址混用。

| 文件 | 職責 |
| --- | --- |
| [第一階段輸入與啟動收據](phase-1-input-and-startup.md) | 輸入雜湊、權利邊界、dosgolem 能力與正常重播 |
| [第一階段選單文字輸出追蹤](phase-1-menu-text-trace.md) | 一條可觀測文字像素輸出鏈、位址與未知項目 |
| [第二階段文字分派與生命週期追蹤](phase-2-text-dispatch-and-lifecycle.md) | 長度前綴 ASCII 字串、字元 renderer、glyph primitive 與生命週期邊界 |
| [第三階段中文手冊輸入清冊](phase-3-manual-input-inventory.md) | RAR 完整性、解壓成員雜湊與僅 metadata 的頁面定位 |
| [第四階段選單互動與失效生命週期](phase-4-menu-interaction-lifecycle.md) | BIOS Enter 正常路徑、轉場字串輸出與舊文字清除時機 |
| [第五階段種族選擇返回生命週期](phase-5-pick-race-return-lifecycle.md) | BIOS Escape 正常返回、逐位元功能選單重建與反向清除時機 |
| [第六階段清除路徑與失效 hook 證據](phase-6-clear-path-hook-evidence.md) | byte-fill 勘誤、Mode 13h 矩形清除例程、Enter／Escape 動態範圍與 hook 邊界 |
| [第七階段文字 post-call 與 generation 事件](phase-7-text-post-call-generation-event.md) | 末 glyph 完成證據、guarded return、自然落入反例與轉場事件順序 |
| [第八階段功能選單繁中字型與版面 prototype](phase-8-menu-font-layout-prototype.md) | 九筆來源、手冊譯名、字型授權邊界、2×／3× 整數覆繪與 containment |
| [第九階段 dosgolem 通用繁中覆繪基礎](phase-9-dosgolem-xlate-foundation.md) | `xlate` 來源、移植 commit、能力邊界、測試收據與倍率限制 |
| [第十階段繁中 catalog 與字型建置](phase-10-catalog-font-build-pipeline.md) | TSV 驗證、決定性字元清單、GOLEMFNT builder 與 dosgolem 回讀收據 |
| [第十一階段手冊查閱事件映射](phase-11-first-manual-check-event-map.md) | 正常進入路徑、動態題目、錯答重抽與中文掃描對應 |
| [第十二階段手冊題庫結構](phase-12-manual-question-table-inventory.md) | 39 筆定長 schema、解碼器、消費者、無答案 metadata 清冊與動態反向驗證 |
| [第十三階段繁中手冊來源對照](phase-13-manual-source-crosswalk.md) | 39 筆逐項來源、證據分級、OCR 搜尋收據與缺頁邊界 |
| [第十四階段首批短篇手冊段落](phase-14-manual-compact-paragraphs.md) | 八筆原圖校訂、事件鍵、繁中 catalog、長度與失敗即關閉驗證 |
| [第十五階段第二批短篇手冊段落](phase-15-manual-compact-paragraphs-2.md) | 第二批八筆原圖校訂、事件擴充、長度與回歸驗證 |
| [第十六階段第三批已證實手冊段落](phase-16-manual-compact-paragraphs-3.md) | 剩餘候選篩選、五筆原圖校訂、排除原因與回歸驗證 |
| [第十七階段手冊分頁與倍率 prototype](phase-17-manual-pagination-scale-prototype.md) | 真實安全矩形、2×／3× 容量、逐頁對照與 renderer 限制 |
| [第十八階段手冊題目世代與舊覆蓋失效](phase-18-manual-generation-invalidation.md) | 答錯換題時間線、局部清除反例與失敗即關閉世代契約 |
| [第十九階段手冊題目事件收集器 prototype](phase-19-manual-event-collector-prototype.md) | typed lifecycle、真實事件重建與跨世代／亂序負向測試 |
| [第二十階段手冊 catalog 顯示請求 prototype](phase-20-manual-catalog-display-request-prototype.md) | 正式 TSV 精確命中、ordinal bridge 缺口與顯示／語意隔離測試 |
| [第二十一階段手冊序數詞橋接證據](phase-21-manual-ordinal-bridge-evidence.md) | 原版 1–10 長度前綴表、索引 consumer、IDA 收據與可重生 TSV |
| [第二十二階段 dosgolem xlate 通用整數倍率](phase-22-dosgolem-xlate-integer-scale.md) | 2×／3× renderer、邊界安全、真實 GOLEMFNT 冒煙收據與本機 commit |
| [第二十三階段手冊事件 adapter](phase-23-manual-event-adapter.md) | READY 純核心、generation／catalog 正反向測試、正式 TSV 與本機 commit |
| [第二十四階段手冊 runtime watcher](phase-24-manual-runtime-watcher.md) | dispatcher entry／guarded post-call 正式接線、固定狀態 metadata 收據與失敗即關閉測試 |
| [第二十七階段功能選單文字事件清冊](phase-27-menu-event-inventory.md) | 九筆 content-free runtime identity、guarded post-call 收據與正式 TSV 雙向驗證 |
| [第二十八階段功能選單顯示請求純核心](phase-28-menu-display-request-core.md) | READY exact-match catalog、九事件顯示請求與失敗即關閉驗證 |
| [第二十九階段功能選單執行期顯示請求 watcher](phase-29-menu-runtime-request-watcher.md) | guarded post-call 直接產生九筆 request、content-free 收據與 CONFORMED 子規格 |
| [第三十階段種族選單反白與文字安全矩形](phase-30-race-selection-highlight-lifecycle.md) | Down／Up normal→selected 重畫、同終點 framebuffer 與 logical text-safe rectangle |
| [第三十一階段反白 variant 執行期繁中請求](phase-31-selection-variant-runtime-requests.md) | 12-identity exact catalog、13-request 固定重播與舊九事件相容性 |
| [第三十二階段功能選單覆繪倍率 A/B prototype](phase-32-menu-overlay-scale-ab-prototype.md) | 同一原版 framebuffer 的 2×／3× xlate 覆繪、幾何與決策收據 |
| [第三十三階段種族選取列閃爍與色盤生命週期](phase-33-selection-blink-lifecycle.md) | 978 點 palette／row 取樣、黑底黑字選取狀態與無週期重畫證據 |
| [第三十四階段倍率中立的功能選單覆繪核心](phase-34-scale-neutral-menu-overlay-core.md) | READY→CONFORMED 純核心、2×／3× 同 API 與四組逐位元回歸收據 |
| [第三十五階段選定種族後的文字路徑清冊](phase-35-post-race-text-path-inventory.md) | 正常雙 Enter 路徑、性別畫面四筆 content-safe identity 與決定性 framebuffer |
| [第三十六階段性別選擇生命週期](phase-36-gender-selection-lifecycle.md) | Down／Up normal→selected 重畫、Escape 返回功能選單與雙重決定性收據 |
| [第三十七階段性別選擇繁中執行期顯示請求](phase-37-gender-runtime-display-requests.md) | 七 identity 繁中 catalog、18-request 正常路徑與 Escape 失敗即關閉證據 |

`workplace/` 是被 Git 忽略的原始輸入與可重生收據存放處；其檔名與雜湊由上述文件引用。
