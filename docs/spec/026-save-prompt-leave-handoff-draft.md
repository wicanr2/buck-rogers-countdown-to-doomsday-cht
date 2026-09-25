# 026 — 儲存詢問離頁交接

狀態：DRAFT
範圍：身體圖示 confirm 路徑完成後，回答儲存詢問 Y／N 並回到主選單
更新：2026-09-26

證據：[第二百四十六階段：儲存詢問離頁時序](../re/phase-246-save-prompt-leave-timing.md)。
相關：[規格 009](009-body-icon-overlay-draft.md)、[規格 025](025-save-prompt-name-affix-overlay-draft.md)。

## 問題

confirm 路徑在儲存詢問出現時就完成。之後的主選單事件不屬於此路徑，watcher
失敗即關閉，runner 停止，無法驗證離頁。

## 契約

1. **交接**：只有 confirm 路徑、且 watcher 已完成（七筆事件依序全到）時，
   之後的 dispatcher 事件一律不再比對、不建立新 transition，也不讓 watcher 失敗。
   交接後收到的事件數記入收據。move、refuse 路徑維持原本的失敗即關閉。
2. **失效**：交接不改變 presenter。前後綴 stamp 保留到任何 A000 寫入與任一矩形
   相交為止，然後成對失效（規格 025）。
3. **不擴權**：交接後 watcher 不再授權任何覆繪；主選單的覆繪屬於選單家族，
   不在本規格範圍。
4. 未完成就收到路徑外事件，行為不變，仍失敗即關閉。

## 驗收（CONFORMED 條件）

`BUCK`，Y（全新 scratch）與 N 兩條，各做 control／2×／3×：

- 主選單已出現、第 24 列未改寫的時間點（510.6M）：前後綴 stamp 仍 active，
  差異只在兩個矩形內。
- 第 24 列改寫之後（511.0M）：active 為零，overlay 與 baseline 全畫面零差。
- control／2×／3× 的 indexed、共同收據欄位、FileOps 相等；Y 的 scratch 內容相等。
