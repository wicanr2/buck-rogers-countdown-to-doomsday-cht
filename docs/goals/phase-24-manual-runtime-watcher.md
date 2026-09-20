# 第 24 階段：手冊 runtime watcher 與真實事件收據

## 狀態

完成

## 本輪目標

以第 7、18 階段已證實的 dispatcher entry／guarded post-call 契約，為 dosgolem
`apps/buckrogers` 建立只觀測、不繪圖的 runtime watcher；在固定原版狀態重播已知手冊路徑，
證明真實執行事件可經第 23 階段正式核心產生或失敗即關閉顯示請求。

## 範圍

- 回讀 dosgolem `oracle.OnCall`、caller／return guard、記憶體與 observer API，以及既有 app
  watcher 實作方式。
- 回讀第 7、18 階段原始收據；建立 watcher 獨立規格，完成證據審查達 READY 後才實作。
- watcher 只擷取已證實的長度前綴顯示字串、caller、entry stack token 與 guarded return；
  把事件送入第 23 階段 Collector／Catalog。
- 由既有固定 state 重播至少一條已收錄題目與一條未收錄／錯答換題結果，保存只含 metadata
  的決定性收據，不保存答案或完整手冊內容。
- dosgolem 建立本機 commit、不推送其遠端；專案 main 推送並更新 Issues #6、#8。

## 不在本輪範圍

- 不選定 2× 或 3×，不建立 `xlate.Stamp`，不改畫面、分頁或字型。
- 不送入新的玩家答案、不自動作答、不改寫 DOS 記憶體、返回值或存檔。
- 不把 observer 收據宣稱為中文畫面 A/B 或完整玩家可見功能。
- 不以 direct-entry 取代既有正常玩家路徑；固定 state 只能縮短已由正常路徑建立的重播。

## 驗收條件

- READY watcher 規格記錄 entry／post-call guard、typed event、位址空間、失敗模式與測試矩陣。
- 單元測試涵蓋正確 return、自然 fall-through、錯誤 caller／SS／SP、巢狀或 stale pending。
- 真實原版固定狀態重播可決定性產生已知題目 metadata；正式 catalog 命中與未命中均符合預期。
- watcher 不產生鍵盤輸入、答案資料、記憶體寫入或 renderer 副作用。
- dosgolem 全部正式 packages、專案測試與資料重生通過；兩個工作樹乾淨。
- 推送專案 `main`，更新 GitHub Issues #6 與 #8。

## 預定交付物

- workplace dosgolem watcher READY 規格、`apps/buckrogers` 程式／測試與本機 commit
- `docs/spec/003-manual-event-adapter.md` 整合邊界回填
- `docs/re/phase-24-manual-runtime-watcher.md`
- `CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

已完成。真實第一題固定狀態由 #266,399,999 重播，在 #266,557,246 經六個 guarded
post-call 產生 `manual.page34.deimos_prison.word10` 顯示請求；正式 watcher、READY 規格、
metadata-only 收據工具、正反向測試與正式 packages 驗證均已完成。未選定 2×／3×，也未
接入 renderer 或玩家輸入。
