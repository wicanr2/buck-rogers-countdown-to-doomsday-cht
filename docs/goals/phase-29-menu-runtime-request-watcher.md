# 第二十九階段：功能選單執行期顯示請求 watcher

## 狀態

完成

## 本輪目標

將第 27 階段 `TextRecorder` 與第 28 階段 `MenuCatalog` 以一個未繪圖、無副作用的 dosgolem
runtime watcher 接合，使正常 Enter 固定狀態在原版每筆 guarded post-call 完成時直接產生繁中
`DisplayRequest`，而不是先匯出 JSON 再離線解析。

## 範圍

- 先建立獨立 READY 子規格，明定 entry／post-call、pending frame、request 提交順序、失敗
  模式、輸出語意隔離與固定狀態驗收，再實作 watcher。
- watcher 只組合既有 `TextRecorder` 與 `MenuCatalog`；不重做事件 identity、不接受模糊匹配。
- 每筆完整事件最多提交一筆 request；catalog miss、guard 失敗、重疊 entry 或未完成事件均不
  產生 request，且不得洩漏前一筆結果。
- 擴充或新增 dosgolem receipt command，以正式兩份 TSV 與正常 Enter 固定狀態直接輸出九筆
  content-free request metadata；不得輸出英文原文或繁中全文。
- dosgolem 建立本機 commit、不推送其遠端；專案 main 推送並更新 Issues #5、#8。

## 不在本輪範圍

- 不選 2×／3×、不載入 GOLEMFNT、不建立 `xlate.Stamp`、不清除或繪製畫面。
- 不加入鍵盤／滑鼠控制，不改原版記憶體、輸入、規則、手冊判定、存檔或 dispatcher。
- 不把九筆已證實事件外推到未盤點文字，不宣稱玩家可見中文化完成。

## 驗收條件

- READY 規格在 implementation 前完成，且只授權 request watcher 子層。
- 正常 Enter 固定狀態直接產生依序九筆 request；event key／text key 與第 27 階段正式 TSV
  一致，兩個 Terran request 保有不同 event key。
- entry 當下、錯誤 return address／SS／SP、未知 identity、catalog miss、pending overlap 與重播
  結束仍 pending 均失敗即關閉。
- request receipt 不含英文原文、繁中全文、原版 pointer、輸入、答案、renderer 或記憶體寫入。
- dosgolem 全部正式 packages test／vet、Buck Rogers race detector與專案資料測試通過。
- 兩個工作樹乾淨，專案 main 已推送，Issues #5、#8 已更新。

## 預定交付物

- dosgolem READY runtime request watcher 規格、實作與正反向測試
- 正常 Enter 固定狀態九筆 request metadata receipt
- `docs/re/phase-29-menu-runtime-request-watcher.md`
- DRAFT 整合邊界、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

- implementation 前建立 READY 規格；固定狀態與全部驗收通過後標為 CONFORMED。
- 正常 Enter 固定狀態直接產生九筆事件與九筆 request，零 drop、pending、catalog miss；
  Terran 選項／標題保有不同 event key 並共用 text key。
- request receipt 只含 event／text key 與譯文字數；正式 verifier 拒絕英／中文全文欄位。
- dosgolem 全部正式 packages test／vet、兩個相關 packages race detector，以及專案 34 項
  資料測試全數通過。
- dosgolem 本機 commit 為 `c6a963dafaf3f060a43816f8a6acbda90aa8b7a0`，未推送其遠端。
