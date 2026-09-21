# 第九十階段：手冊 presentation queue consumer 純核心

狀態：完成（純核心）

## 目標

將 spec 216 已 CONFORM 的 append-only `ManualPresentationEvent` value queue，以 cursor 與歷史
一致性檢查交給 spec 217 的 `RuntimeManualOverlay`。consumer 必須只接受 value snapshot、只消費新事件，
不得由 `Observations()` 重建 lifecycle，也不接 command、正式字型、host frontend 或 DOS machine。

## 已確認前提

- `Watcher.PresentationEvents()` 對外回傳 value copy；正常玩家第一題已證實 begin → pending clear →
  request 的 generation 1 順序，且 request 不含答案、原文或 input reference。
- `RuntimeManualOverlay.Apply` 已對 begin／clear／request、generation、catalog identity 和字型缺口
  失敗即關閉，但目前沒有 queue cursor 或 runtime 接線。
- 同一 consumer 重複收到完整 queue snapshot 時，不得重複 Apply 已消費事件；任何先前事件內容被
  竄改、snapshot 縮短或新事件非法時都必須拒絕，不能把 controller cursor 悄悄跳過。

## 範圍

- 建立 dosgolem DRAFT→READY 規格，定義 consumer constructor、append-only snapshot contract、cursor、
  prefix identity、每事件提交、部分批次失敗與 defensive accessor；原版／玩家路徑證據只引用 spec 216。
- 新增 `apps/buckrogers` 純 Go consumer 與 synthetic tests，驗證新事件恰好一次 Apply、完整 snapshot
  replay 為 zero-op、prefix mutation／縮短 queue／非法事件拒絕、失敗事件不前進 cursor，以及回傳歷史
  不可污染內部狀態。
- 驗證 consumer 不 import machine／oracle／input 或 command，不繪製／重繪、載入字型檔、寫 VRAM、
  修改 watcher、送鍵、改答案或存檔。

## 不在本階段

- 不將 consumer 接到 `cmd/buckrogers-receipt`、正常遊戲 loop、host canvas、倍率 Apply 或任何前端。
- 不建置／採用正式字型；現有 fixture font 只用於純核心測試，不能聲稱玩家看見中文。
- 不重新量測原版題目、改動 lifecycle watcher、英文 identity、翻譯、手冊答案、DOS input、VRAM、
  memory、檔案或存檔。

## 完成條件

1. READY 規格定義 append-only value contract、state transition、partial-failure cursor、失敗模式、
   機器／輸入隔離及正常玩家 A/B 停止線；production code 僅在 READY 後進入本機 dosgolem branch。
2. consumer 單元、vet、race 測試覆蓋 append、replay、mutation、shrink、invalid event、partial failure
   與 defensive-copy；無 DOS／遊戲外輸入依賴，也不產生原作素材。
3. 專案資料驗證、main 推送與相關 GitHub Issue 回寫完成；spec 005 只回填 consumer core，不將
   正式字型或正常玩家 RGBA A/B 提前標完成。

## 退出條件

- 若 value snapshot 無法可靠區分 append 與 mutation，維持 DRAFT，不以 event count 或 generation
  單獨猜測歷史一致性。
- 若 consumer 必須修改 watcher 或從 machine 讀狀態才能運作，退回 DRAFT；不得讓 renderer 反向控制
  原版 lifecycle。

## 完成收據

- dosgolem 本機分支 `buck-rogers-cht-output-overlay` 的
  `b0721c605619a9e689c934994408e009e9231ff9` 已 CONFORM spec 220：consumer 只接受 event value
  snapshot，完整比對已消費 prefix，且僅在 presenter `Apply` 成功後推進 cursor。
- Docker 內 `go test ./apps/buckrogers`、`go vet ./apps/buckrogers` 與
  `go test -race ./apps/buckrogers` 都通過；測試覆蓋 append、replay、mutation、shrink、未知與非法
  event、partial failure、defensive-copy 與 nil。consumer 的唯一直接 import 是 `fmt`。
- 未接 watcher callback、command／遊戲 loop、正式字型、RGBA A/B 或正常玩家路徑；因此這不宣稱玩家
  已看見手冊中文。dosgolem 分支依專案規範未推送。
