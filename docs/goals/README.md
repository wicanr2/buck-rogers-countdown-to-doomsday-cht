# 分期目標索引

此目錄只保存每一階段的範圍、成功定義與退出條件；可執行工作與其遠端狀態以 GitHub
Issues 為唯一權威，研究證據則在 `docs/re/`。

| 階段 | 狀態 | 目標 |
| --- | --- | --- |
| [第一階段：可觀測的原版啟動與文字輸出基線](phase-1-observable-original.md) | 已完成 | 建立 dosgolem 原版啟動、重播與第一條文字輸出收據。 |
| [第二階段：文字分派與生命週期證據](phase-2-text-dispatch-and-lifecycle.md) | 已完成 | 追出可進入 DRAFT 覆繪規格的最小充分證據。 |
| [第三階段：中文手冊輸入清冊與頁面定位](phase-3-manual-input-inventory.md) | 已完成 | 建立不散布手冊內容的 RAR 清冊與可追溯頁面定位基線。 |
| [第四階段：選單互動與覆繪失效生命週期](phase-4-menu-interaction-lifecycle.md) | 已完成 | 量測正常選單互動後的重繪、轉場與覆繪失效時機。 |
| [第五階段：種族選擇畫面的離開與返回生命週期](phase-5-pick-race-return-lifecycle.md) | 已完成 | 量測 `PICK RACE` 的 Escape 離開、清除、重繪與返回證據。 |
| [第六階段：清除路徑與失效 hook 證據](phase-6-clear-path-hook-evidence.md) | 已完成 | 排除底層 byte-fill，證實帶參數的 Mode 13h 矩形清除 hook 候選。 |
| [第七階段：文字 post-call 與 generation 事件](phase-7-text-post-call-generation-event.md) | 已完成 | 證實 dispatcher 完成繪製後的事件與矩形失效之 generation 順序。 |
| [第八階段：功能選單繁中字型與版面 prototype](phase-8-menu-cht-font-layout-prototype.md) | 已完成 | 盤點參考實作、建立首批譯文與原生尺寸字型／版面對照。 |
| [第九階段：dosgolem 通用繁中覆繪基礎](phase-9-dosgolem-xlate-foundation.md) | 已完成 | 移植並驗證通用 `xlate` package；遠端分支待明確授權。 |
| [第十階段：繁中 catalog 與 GOLEMFNT 建置管線](phase-10-catalog-font-build-pipeline.md) | 已完成 | 建立 TSV lint、字元清單與可重生的 16×16 字型子集工具。 |
| [第十一階段：第一條手冊查閱事件與中文段落映射](phase-11-first-manual-check-event-map.md) | 已完成 | 定位原版手冊查閱事件並建立第一條中文來源映射。 |
| [第十二階段：手冊題庫結構與可抽題清冊](phase-12-manual-question-table-inventory.md) | 完成 | 證實原版題庫 schema、消費者與可抽題 metadata，再對回中文條目。 |
| [第十三階段：39 筆手冊題目與繁中來源對照](phase-13-manual-source-crosswalk.md) | 完成 | 逐筆核對中文掃描來源、證據等級與可用繁中段落。 |
| [第十四階段：首批短篇繁中手冊段落校訂](phase-14-manual-compact-paragraphs.md) | 完成 | 原圖校訂八筆短篇段落並建立題目鍵與繁中 catalog。 |
| [第十五階段：第二批短篇繁中手冊段落校訂](phase-15-manual-compact-paragraphs-2.md) | 完成 | 再校訂八筆單段內容並擴充事件與 catalog。 |
| [第十六階段：第三批已證實繁中手冊段落校訂](phase-16-manual-compact-paragraphs-3.md) | 完成 | 從剩餘已證實來源校訂五筆完整內容並分類排除其餘候選。 |
| [第十七階段：手冊查詢分頁與倍率對照 prototype](phase-17-manual-pagination-scale-prototype.md) | 完成 | 由真實查詢畫面建立 2×／3× 可丟棄分頁對照與決策證據。 |
| [第十八階段：手冊題目世代與舊覆蓋失效](phase-18-manual-generation-invalidation.md) | 完成 | 量測答錯換題事件順序，建立舊繁中覆蓋不得跨題沿用的失效契約。 |
| [第十九階段：手冊題目事件收集器 prototype](phase-19-manual-event-collector-prototype.md) | 完成 | 以真實事件及反例驗證世代收集器的 typed lifecycle 與失敗即關閉行為。 |
| [第二十階段：手冊 catalog 顯示請求 prototype](phase-20-manual-catalog-display-request-prototype.md) | 完成 | 以正式 TSV 驗證精確唯一命中與未命中失敗即關閉的顯示請求。 |
| [第二十一階段：手冊序數詞橋接證據](phase-21-manual-ordinal-bridge-evidence.md) | 完成 | 由原版資料與 consumer 建立 runtime 序數詞到題庫數字的可稽核橋接。 |
| [第二十二階段：dosgolem xlate 通用整數倍率](phase-22-dosgolem-xlate-integer-scale.md) | 完成 | 擴充通用 GOLEMFNT renderer 支援 2×／3×，不預先選定遊戲倍率。 |
| [第二十三階段：手冊事件 adapter 規格與正式核心](phase-23-manual-event-adapter.md) | 完成 | 將已證實事件與 catalog 流程審查成 READY 子規格，再實作未接線的正式核心。 |
| [第二十四階段：手冊 runtime watcher 與真實事件收據](phase-24-manual-runtime-watcher.md) | 完成 | 將已證實 dispatcher guard 接到正式核心，以原版固定狀態驗證顯示請求。 |
| [第二十五階段：手冊繁中覆繪倍率決策](phase-25-manual-overlay-scale-decision.md) | 進行中 | 以原生尺寸 prototype 與 Golden Box CJK 版面證據決定 2×／3×。 |
| [第二十六階段：README 遊戲歷史、保存價值與技術定位](phase-26-readme-history-positioning.md) | 完成 | 以可回查來源完成專案歷史介紹、保存理由、技術定位與權利邊界。 |
| [第二十七階段：功能選單文字事件清冊](phase-27-menu-event-inventory.md) | 完成 | 由正常 Enter 固定狀態重生九筆 typed dispatcher／post-call metadata。 |
| [第二十八階段：功能選單顯示請求純核心](phase-28-menu-display-request-core.md) | 完成 | 將 exact runtime identity 與正式繁中 TSV 接成失敗即關閉顯示請求。 |
| [第二十九階段：功能選單執行期顯示請求 watcher](phase-29-menu-runtime-request-watcher.md) | 完成 | 在 guarded post-call 直接產生精確繁中顯示請求，不接 renderer。 |
| [第三十階段：種族選單反白與文字安全矩形生命週期](phase-30-race-selection-highlight-lifecycle.md) | 完成 | 量測正常方向鍵反白重繪，建立 logical text-safe rectangle 證據。 |
| [第三十一階段：反白 variant 的執行期繁中請求](phase-31-selection-variant-runtime-requests.md) | 完成 | 將已證實 selection identity 納入 exact catalog，閉合 13-request 路徑。 |
| [第三十二階段：功能選單覆繪倍率 A/B prototype](phase-32-menu-overlay-scale-ab-prototype.md) | 完成 | 以同一原版 framebuffer 建立 2×／3× 繁中覆繪與幾何決策收據。 |
| [第三十三階段：種族選取列閃爍與色盤生命週期](phase-33-selection-blink-lifecycle.md) | 完成 | 量測 selected row 的連續幀可見性、palette 與像素重畫機制。 |
| [第三十四階段：倍率中立的功能選單覆繪核心](phase-34-scale-neutral-menu-overlay-core.md) | 完成 | 將已證實選單幾何移入明示倍率的正式純核心，不預先選定 2×／3×。 |
| [第三十五階段：選定種族後的下一畫面文字路徑清冊](phase-35-post-race-text-path-inventory.md) | 完成 | 由正常 Enter 路徑建立下一個玩家可見畫面的 content-safe 文字事件證據。 |
| [第三十六階段：性別選擇生命週期收據](phase-36-gender-selection-lifecycle.md) | 完成 | 量測性別選擇的上下移動、返回與 framebuffer 決定性收據。 |
| [第三十七階段：性別選擇繁中執行期顯示請求](phase-37-gender-runtime-display-requests.md) | 完成 | 將已證實性別事件接成正式繁中 catalog 與執行期顯示請求。 |
| [第三十八階段：確認性別後的下一畫面文字路徑清冊](phase-38-post-gender-text-path-inventory.md) | 完成 | 由正常第三次 Enter 量測下一個角色建立畫面的文字事件與 framebuffer。 |
| [第三十九階段：職業選擇生命週期收據](phase-39-class-selection-lifecycle.md) | 完成 | 量測職業選擇的上下移動、返回與 framebuffer 決定性收據。 |
