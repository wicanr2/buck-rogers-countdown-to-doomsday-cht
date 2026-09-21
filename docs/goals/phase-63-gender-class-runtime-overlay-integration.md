# 第六十三階段：性別與職業選單執行期繁中覆繪整合

狀態：完成

## 目標

沿用已 CONFORMED 的明示倍率 `RuntimeMenuOverlay`，把既有性別／職業 typed request 與
text-safe rectangles 納入同一正常角色建立 runtime receipt；以 2×／3× 驗證輸出端繁中覆繪，
不設定產品預設倍率。

## 範圍

- 盤點並驗證性別／職業正式事件、繁中 catalog、安全矩形與 Phase 41 A/B 證據。
- 先建立或補正獨立 READY 子規格，再擴充 receipt 的完整 overlay 輸入契約。
- 以正常 BIOS 路徑進入性別與職業畫面，分別驗證 selected／normal 重畫、返回／轉場清除、
  中文像素 containment 與原版語意隔離。
- 2×／3× 均採命令列明示，至少各兩次決定性重播。
- dosgolem 變更只提交本機 `buck-rogers-cht-output-overlay` branch，不推遠端；專案證據提交
  `main`、推送並更新 GitHub Issues。

## 不在本階段

- 不選定正式 2×／3×，不建立預設倍率。
- 不處理手冊版面、不替使用者回答 Phase 62 的保留題目決策。
- 不翻譯動態能力值、技能點或玩家姓名，不修改遊戲規則、輸入、記憶體與存檔。

## 完成條件

1. 性別／職業 overlay 輸入必須成對且完整，缺 rect、缺字、identity 漂移或非法倍率失敗即關閉。
2. 正常路徑的 request 與 overlay action 一一對應；選取重畫不殘留舊 variant，離開畫面後舊
   stamp 失效。
3. 2×／3× 各兩次輸出決定性，所有 ink 位於核准安全矩形且動態欄位不被覆蓋。
4. 原版 events、BIOS keys、raw framebuffer、記憶體／檔案副作用與無覆繪 baseline 一致。
5. dosgolem 正式 test／vet／race、專案回歸與收據 verifier 通過。
6. 兩個儲存庫依授權邊界提交，專案 `main` 已推送，相關 GitHub Issues 已更新。

## 退出條件

- 若既有矩形只屬離線 prototype、無法和 runtime event identity 一一對回，先補證據，不猜座標。
- 若長存 layer 暴露新失效生命週期缺口，規格退回 DRAFT，以 typed clear／replace 契約修正，
  不以終態 key 硬刪。
- 若工作開始依賴預設倍率或手冊版面，暫停該分支等待使用者。

## 完成摘要

- dosgolem spec 036 已依 READY→implementation→same-state verification 升為 CONFORMED。
- 正常三 Enter＋Down 路徑為 24 requests／24 actions；2×／3× 各兩次決定性，安全矩形外 0 px。
- 原版 raw framebuffer 與 baseline 相同；終態只有職業 keys，性別與舊 variant 均已失效。
- 專案 105 項測試及 dosgolem 正式 test／vet／race 通過；未設定預設倍率或觸碰手冊版面。
