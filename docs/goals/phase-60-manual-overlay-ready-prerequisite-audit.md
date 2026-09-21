# 第六十階段：手冊覆繪 READY 前置稽核

狀態：完成

## 目標

在不預選 2×／3× 的前提下，逐項查證手冊繁中段落覆繪規格的其餘 READY 前置，
將已完成、尚待決策與應屬於實作後 CONFORMED 驗收的項目分開，消除循環依賴。

## 範圍

- 驗證 39 筆原版題庫、22 筆已校訂 catalog、來源等級與未命中政策的權威關係。
- 核對 manual runtime watcher、collector、ordinal bridge、exact catalog lookup 的實作與測試現況。
- 確認未校訂、`strong-inference`、`unknown` 與 catalog miss 均明確失敗即關閉，不需為湊齊
  39 題而猜測補文。
- 訂正 `docs/spec/002-manual-paragraph-overlay-draft.md` 的關卡分類：READY 只放實作前契約；
  錯答重抽、安全矩形、原版輸入與同狀態 A/B 放到實作後 CONFORMED 驗收。
- 建立可追溯的 readiness matrix，但維持規格 DRAFT，直到使用者確認倍率。

## 不在本階段

- 不實作正式 manual renderer、分頁輸入或頁尾提示。
- 不選定倍率，不將 DRAFT 升為 READY。
- 不新增未經逐字校訂的手冊段落，不自動作答或改原版驗證。

## 完成條件

1. readiness matrix 對每個前置列出權威檔案、驗證命令、結果與剩餘阻擋。
2. 專案資料驗證與 dosgolem manual adapter／watcher 相關測試通過。
3. spec 002 不再把實作後收據當作 READY 前置，且明寫未校訂題目的失敗即關閉政策。
4. 專案 `main` 已提交推送，GitHub Issues 已更新；dosgolem 如無程式變更則不製造空提交。

## 退出條件

- 若查出 watcher 或 catalog 契約與既有收據矛盾，保留 DRAFT 並建立最小重播，不以文件宣告解決。
- 若只剩產品倍率決策，清楚標示為唯一 READY blocker，繼續等待使用者回答。

## 完成摘要

- 39 題來源分級、22 筆正式 catalog 與 17 筆未命中邊界已驗證並文件化。
- 正式譯文最長 236 字，全部落在單頁 612 字容量，本批不需分頁輸入決策。
- spec 002 已將 renderer 接線後的正常路徑、錯答重抽、containment 與 A/B 移到
  CONFORMED 驗收；唯一 READY blocker 為使用者尚未選定 2×／3×。
- 專案 101 項測試及 dosgolem 手冊 adapter／watcher 測試通過；本輪未修改 dosgolem。
