# 026 — 儲存詢問離頁交接

狀態：READY（2026-09-26 獨立審查後修訂）
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
   交接後收到的事件只計數。move、refuse 路徑維持原本的失敗即關閉。
2. **失效**：交接不改變 presenter。前後綴 stamp 保留到任何 A000 寫入與任一矩形
   相交為止，然後成對失效（規格 025）。
3. **不擴權**：交接後 `Transitions()` 與內部事件清單不得再成長，presenter 不會
   收到新 transition。主選單的覆繪屬於選單家族，不在本規格範圍。
4. 未完成就收到路徑外事件，行為不變，仍失敗即關閉。

5. **前提**：交接期間的失效只靠 A000 寫入觀察。`int 10h AH=00` 設定模式時，
   `VGA.resetMode` 直接清空顯示記憶體，不經寫入觀察。phase-246 的區間沒有模式切換；
   若發生，stamp 可能殘留。此缺口是所有覆繪家族共有的，另列 dosgolem 待辦；
   本規格的終態零差檢查會把這種殘留判為失敗。DOS 退出與狀態還原不在本規格範圍。

## 實作需要的介面變更

1. `BodyIconWatcher.Observe`：confirm 路徑且 `Complete()` 時，計數後直接回傳 nil。
2. `BodyIconWatcher.PostRouteEvents() int` 回傳交接後的事件數。
3. runner 收據新增 `body_icon_post_route_events`（int，僅在有 body icon route 時輸出）。

## 驗收（CONFORMED 條件）

`BUCK`，Y（全新 scratch）與 N 兩條，各做 control／2×／3×：

- 主選單已出現、第 24 列未改寫的時間點（510.6M）：前後綴 stamp 仍 active，
  差異只在兩個矩形內。
- 第 24 列改寫之後（驗收時在 511.0M 取終態；phase-246 只量到 510.65M，
  511.0M 由驗收重播本身產生）：active 為零，overlay 與 baseline 全畫面零差。
- control／2×／3× 的 indexed、共同收據欄位、FileOps 相等；Y 的 scratch 內容相等。
