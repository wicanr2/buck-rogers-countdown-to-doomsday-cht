# 第九十一階段：手冊 watcher snapshot bridge 純核心

日期：2026-09-21
dosgolem 本機分支：`buck-rogers-cht-output-overlay`
dosgolem 本機提交：`bac3f3fafc3cc40b78eee66fdb1f756f21509e53`（未推送）
狀態：**CONFORMED（純核心）**

## 已證實轉送界線

spec 216 的 `Watcher.PresentationEvents()` 是唯一 lifecycle accessor，回傳不含答案的
`ManualPresentationEvent` value slice。spec 220 的 consumer 保存唯一的成功 prefix 與 cursor，會在
presenter `Apply` 成功後才提交 event。bridge 只持有兩個 reference，`Sync` 每次只將新的 watcher
snapshot 交給 consumer；它不讀 `Observations()`、collector、machine、oracle 或原版資料。

nil watcher 在 accessor 前拒絕；nil consumer 或 bridge 也拒絕。其餘錯誤由 consumer 原樣傳回：history
drift、非法 lifecycle 與 partial failure 都不被吞掉、重排或以第二份 cursor 修正。這是既有 serial
owner 的純核心契約，未新增 goroutine 或鎖語意。

## 合成驗證

Docker、無網路、唯讀程式輸入中通過：

```text
go test ./apps/buckrogers
go vet ./apps/buckrogers
go test -race ./apps/buckrogers
```

測試以 synthetic watcher presentation state 覆蓋 begin→clear→request 的分批 append、完整 replay
zero-op、合成 history drift、clear generation 不符造成的部分失敗、失敗 event 重試，以及 nil
watcher／consumer／bridge。bridge 的唯一直接 import 是標準庫 `fmt`；不依賴 machine、oracle、input、
`cmd`、renderer 或 font。

## 明確邊界

這份收據只證實 watcher value snapshot 至 consumer 的一次性轉送，不是原版正常玩家 runtime 收據。
它沒有接 command、遊戲 loop、frame／draw、正式 691 glyph 字型、host frontend 或 2×／3× RGBA A/B。
手冊中文仍未可見；不得把合成 bridge 測試當作原版驗證、答案不變或存讀檔相容性的證明。
