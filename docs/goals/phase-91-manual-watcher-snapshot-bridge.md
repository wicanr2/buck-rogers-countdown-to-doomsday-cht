# 第九十一階段：手冊 watcher snapshot bridge 純核心

狀態：完成（純核心）

## 目標

在 `apps/buckrogers` 建立最小的手冊 presentation bridge，將既有 `Watcher.PresentationEvents()` 的
防禦性 value snapshot 交給第九十階段已 CONFORM 的 `ManualPresentationConsumer`。bridge 只負責取得
snapshot 與呼叫 `Consume`；不自行保存第二份 cursor、不由 `Observations()` 重建事件，亦不取代
consumer 的 prefix 驗證。

## 已確認前提

- spec 216 已 CONFORM：watcher 的 `PresentationEvents()` 回傳 answer-free、append-only
  `ManualPresentationEvent` value slice；正常第一題 lifecycle 已有 begin → pending clear → request
  的原版 metadata 收據。
- spec 220 已 CONFORM：consumer 對同一 snapshot 完整重播回傳 zero，並拒絕歷史漂移、縮短與非法新
  event；唯一提交點是 presenter `Apply` 成功後。
- 目前尚無正式字型，也尚未決定／實作 host frontend；故本階段不能建立正式 presenter、不能接 command
  或聲稱玩家已看見中文。

## 範圍

- 建立 dosgolem DRAFT→READY 規格，定義 bridge constructor、watcher／consumer ownership、每次 Sync 的
  exact snapshot forwarding、nil／consumer error 邊界與停止線。
- 實作只持有 `*Watcher` 與 `*ManualPresentationConsumer` 的純核心 bridge；`Sync` 只能呼叫
  `PresentationEvents()` 與 `Consume`，回傳 consumer 的新 event 數／錯誤。
- 新增 synthetic tests，覆蓋 begin→clear→request 一次性 consumption、完整 snapshot replay、watcher
  history 漂移、consumer 拒絕、nil constructor／receiver 與 bridge 不重複 action。

## 不在本階段

- 不修改 watcher lifecycle、原始位址、machine、oracle、DOS／BIOS input、答案、英文 identity、檔案、
  存檔、catalog、手冊內容或正式字型。
- 不呼叫 `Frame`／`Draw`、不建立 RGBA、不可接 `cmd/buckrogers-receipt`、遊戲 loop、host frontend 或倍率
  Apply；不以 synthetic bridge 測試取代正常玩家原版／繁中 A/B。

## 完成條件

1. READY 規格明定 bridge 僅轉送 watcher defensive snapshot，consumer 是 cursor 的唯一權威，並記錄
   nil／history-drift／partial-failure 的 fail-closed 邊界。
2. Go unit、vet、race 通過，且新檔案沒有 direct import machine、oracle、input、command、renderer 或
   font；測試證實完整 replay 不會重複 presenter action。
3. 專案規格 005 只回填 bridge pure core；goal、證據、現況、工作歷程、main 推送及相關 GitHub Issue
   回寫完成，dosgolem 分支保持本機未推送。

## 退出條件

- 若 bridge 必須讀 `Observations()`、原版機器狀態或改寫 watcher 才能保持 lifecycle，維持 DRAFT；不得
  猜測事件或讓 presentation 反向控制原版。
- 若 consumer 必須因 bridge 而重複保存／比較 cursor，停止實作並回到 spec；不得建立兩份可分歧的歷史。

## 完成收據

- dosgolem 本機分支 `buck-rogers-cht-output-overlay` 的
  `bac3f3fafc3cc40b78eee66fdb1f756f21509e53` 已 CONFORM spec 221：bridge 僅取得 watcher 的
  `PresentationEvents()` value snapshot，並將它原樣交給既有 consumer；沒有第二份 cursor 或事件重建。
- Docker 內 `go test ./apps/buckrogers`、`go vet ./apps/buckrogers` 與
  `go test -race ./apps/buckrogers` 都通過；測試覆蓋分批 append、完整 replay、合成 history drift、
  partial failure、重試失敗 event 與 nil。
- 本階段也更正 spec 220 文件頂端的舊 DRAFT 標示為 CONFORMED。未接 command、遊戲 loop、正式字型、
  RGBA A/B 或正常玩家路徑；dosgolem 分支依專案規範未推送。
