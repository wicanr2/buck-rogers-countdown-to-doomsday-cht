# 第八十九階段：host 倍率預選與 Apply 純核心

狀態：完成（純核心；非 host frontend）

## 目標

依使用者已確認的 C 語意，建立 dosgolem 通用、無前端 backend 的倍率設定純核心：2×／3×
option 只能改變 `selectedScale`，唯有 Apply 可提交 `activeScale`。它必須可供未來 host presenter
使用，但不實作視窗、面板、命令列、持久化、DOS input forwarding 或 Buck Rogers adapter。

## 已確認前提

- 使用者已選擇「先選取，再按 Apply」，排除 option 點擊立即套用；Apply 後是否收合面板與
  跨重啟持久化均尚未決定。
- dosgolem 的現有 output overlay 已明示支援 2×／3×，但既有 runtime overlay 只有 constructor
  scale、沒有 setter；host frontend 目前仍是 DRAFT，且沒有視窗 backend。
- host hit event 必須在 DOS 座標轉換、mouse API、BIOS 與 IRQ 前被消費；倍率 state core 本身
  不得持有 machine、鍵盤、滑鼠、VRAM、檔案、存檔、catalog 或翻譯資料。

## 範圍

- 先建立 dosgolem DRAFT→READY 規格，定義 generic typed state、constructor、Select、Apply、
  防禦性 snapshot、2×／3×邊界與 C 的 state transition；所有未知 UI/backend 行為明列停止線。
- 在通用 host／presentation 層實作純 Go state core 與單元測試，證實 Select 不改 active、Apply
  原子提交、重複 Apply 無副作用、非法 scale／nil receiver 失敗即關閉，且回傳值不能污染內部 state。
- 對既有 320×200 output compositing 做最小 adapter-free verification，證明 core 只產生倍率值、
  不會啟動或重啟 DOS、送鍵、寫 machine、清除 overlays 或碰觸手冊／字型資料。

## 不在本階段

- 不實作視窗 backend、頂端按鈕、面板、hit test、host 文案、焦點、Apply 後收合或設定持久化。
- 不把倍率 core 接入 `cmd/probe`、`cmd/buckrogers-receipt`、`RuntimeManualOverlay`、DOS mouse／
  keyboard、BIOS、IRQ、VRAM、存檔或任何遊戲 adapter。
- 不選定產品預設 2×或3×，不下載字型，且不以純核心測試宣稱玩家可在遊戲中切換。

## 完成條件

1. dosgolem READY 規格完整描述 C 語意、typed boundary、狀態轉移、失敗模式、輸入隔離與
   同狀態／backend 停止線；production code 僅在 READY 後進入本機 dosgolem branch。
2. 通用 core 測試涵蓋所有合法／非法 transition、value isolation 與 2×／3×；並以 Go test、vet、
   race 驗證，沒有 DOS／遊戲專屬依賴。
3. 專案文件、main 推送與相關 GitHub Issue 回寫完成；規格 004 只更新已證實的 core，保持
   backend、面板收合與持久化為 DRAFT。

## 退出條件

- 若 C 語意需要依賴未決的 backend、收合或持久化行為才能定義 state transition，維持 DRAFT，
  不以預設值猜補。
- 若通用 core 需要引用 DOS 或 Buck Rogers 型別，退回 DRAFT 並重新分層；不得用遊戲 adapter
  冒充通用 host 能力。
