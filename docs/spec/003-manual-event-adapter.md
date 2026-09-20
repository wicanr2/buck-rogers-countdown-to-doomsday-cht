# 003 — 手冊事件 adapter 整合邊界

狀態：DRAFT（事件觀測子層 READY；玩家可見整合仍未核准）
日期：2026-09-20

## 目的

記錄《拯救地球》如何使用 dosgolem 的 Buck Rogers 手冊事件純核心，以及哪些玩家可見整合
仍未獲 READY 授權。本文件不是核心行為的第二份規格；唯一實作權威是 workplace dosgolem
分支的 `docs/spec/007-buck-rogers-manual-event-adapter.md`，對應本機 commit
`8ce092f29d000ea7e6765c4f3389fe484aefa555`。可版控的證據摘要見
[第 23 階段研究收據](../re/phase-23-manual-event-adapter.md)。

## 已可依賴的核心契約

- 題首精確命中才建立 generation 並使舊 visible 失效。
- 六筆 guarded post-call 須依已證實 caller 與順序收集；錯誤 generation 失敗即關閉。
- 原版序數詞只由正式 `manual-ordinals.tsv` 橋接，不內嵌一般英文推測。
- 題目身分只以 `(page, heading_ascii, ordinal)` 精確唯一匹配正式 TSV。
- 輸出只有 generation、event key、text key 與 translation，不含答案、輸入、原版狀態寫入、
  存檔或 renderer 欄位。

## 仍為 DRAFT 的整合

- 2×／3× 產品倍率選擇、字模偏移、手冊安全矩形與分頁控制。
- 中文 overlay 的建立、clear／新 generation 移除與正常玩家路徑同狀態 A/B。
- 玩家翻頁輸入與原版答題輸入如何共存；不得先假設按鍵語意。

在上述項目各自取得證據並升為 READY 前，不得把純核心接入正式 runtime。核心單元測試通過
只證明事件與資料契約的內部一致性，不證明中文已在遊戲畫面顯示。

## 已核准的 runtime 觀測子層

第 24 階段已把 `oracle.OnCall`、dispatcher entry、三重 guarded post-call 與 clear entry
審查並實作為 dosgolem READY 規格 `docs/spec/008-buck-rogers-manual-runtime-watcher.md`。
固定狀態重播已由真實原版第一題產生 `manual.page34.deimos_prison.word10` 顯示請求；收據見
[第 24 階段研究紀錄](../re/phase-24-manual-runtime-watcher.md)。此核准只到 typed request，
不包含 renderer、倍率、分頁或玩家輸入。
