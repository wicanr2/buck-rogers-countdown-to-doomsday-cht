# 第七十六階段：技能操作列繁中 catalog 與顯示請求

狀態：完成

## 目標

以 Phase 75 已 CONFORMED 的 `ActionBarEvent` 為唯一 runtime 輸入，建立技能頁底部五個
操作標籤的 UTF-8 繁體中文 catalog 與 exact display-request resolver。正常玩家路徑只將
已證實的 normal／focus events 轉成輸出端請求，不讓譯文進入原版控制流。

## 範圍

- 優先查找本專案既有中文手冊、譯名表及畫面 catalog 的用詞；無對應原文時，
  以標準繁中介面詞建立可追溯的 editorial 來源，不冒稱手冊逐字譯名。
- 新增唯一正式譯文 TSV，五個穩定 text key 由 career／technical 與 normal／focus 共用。
- 新增 dosgolem exact catalog loader／resolver，要求事件清冊與譯文雙向覆蓋。
- 將 `ActionBarWatcher` 完成事件接成 `DisplayRequest`，只輸出 event key、text key
  與譯文長度 metadata。
- 重生 Phase 75 八條正常玩家路徑，每條雙重播並與無 request 對照組比較。

## 不在本階段

- 不新增安全矩形、字型子集或 runtime overlay，不宣稱操作列已繪出中文。
- 不修改原版鍵盤輸入、技能點、焦點、離開判定、存檔或文字記憶體。
- 不新增 disabled identity；正式清冊仍只有已證實的 normal／focus。
- 不選定產品預設 2×／3×，不改手冊版面。

## 完成條件

1. 五個譯文的來源分級、穩定 text key、UTF-8／NFC、控制字元、孤兒 key 及雙向
   event coverage 由失敗即關閉 verifier 固定。
2. dosgolem spec 在實作前由 DRAFT 通過證據審查為 READY，明寫 typed resolver、
   失敗模式、語意隔離及驗收。
3. 純核心測試覆蓋八個畫面配置的 normal／focus exact hit，並拒絕未知雜湊、
   畫面／key／variant／幾何漂移、重複 identity、漏譯與孤兒譯文。
4. 八條 runtime 路徑的 request 數與 action event 數相同，0 miss／drop；A/B JSON 決定性一致，
   移除 request metadata 後與 control 的原版語意與 framebuffer 一致。
5. spec 限定範圍升為 CONFORMED；專案與 dosgolem 測試通過，專案 `main`
   推送並回寫相關 GitHub Issues。

## 退出條件

- 若中文手冊與現有 catalog 的用詞衝突，保留兩個來源並將詞彙決策列為 pending，
  不在程式碼內寫死未審查譯文。
- 若 request 接線需要改變 Phase 75 事件 identity，退回 spec 213／RE 補證據，
  不以模糊對應迴避。

## 完成收據

- 五筆正式譯文、八筆事件與 16 個 normal／focus resolver identities 已雙向驗證。
- 八條正常路徑 event／request 數為 3／6／9／8／13／18／23／28，零 miss／drop；
  雙重播、control 語意與 framebuffer 非干擾均通過。
- 專案 144 項 Python 測試及 dosgolem 全套 test／vet／相關 race 通過；spec 214 已 CONFORMED。
