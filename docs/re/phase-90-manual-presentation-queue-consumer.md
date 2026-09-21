# 第九十階段：手冊 presentation queue consumer 純核心

日期：2026-09-21
dosgolem 本機分支：`buck-rogers-cht-output-overlay`
dosgolem 本機提交：`b0721c605619a9e689c934994408e009e9231ff9`（未推送）
狀態：**CONFORMED（純核心）**

## 已證實輸入與提交界線

spec 216 的 `Watcher.PresentationEvents()` 回傳 answer-free `ManualPresentationEvent` value slice；每筆
包含 step、kind、generation 與僅 request 使用的 `DisplayRequest` value。spec 217 的
`RuntimeManualOverlay.Apply` 已驗證 begin、clear、request 的 lifecycle。第九十階段不重讀原版、
不由 `Observations()` 猜測 lifecycle，也不將英文原文、答案、輸入或手冊掃描內容帶入 consumer。

`ManualPresentationConsumer` 保存唯一私有的成功 prefix。每次 `Consume` 先要求新 snapshot 至少與
prefix 等長，並逐筆 value 比對已消費歷史；縮短或 mutation 一律在 presenter 前拒絕。其後只將尚未
消費的 event 依序交給 `Apply`，且僅在該筆成功後 append cursor。中段錯誤不假裝可 rollback 已提交的
presenter state：回傳成功筆數、保留已提交 prefix，下一次重試失敗位置而不重套舊事件。

## 合成驗證

Docker、無網路、唯讀程式輸入中通過：

```text
go test ./apps/buckrogers
go vet ./apps/buckrogers
go test -race ./apps/buckrogers
```

測試覆蓋 begin→pending clear→request 的分批 append、完整 snapshot replay zero-op、歷史 step mutation、
snapshot shrink、沒有 begin 的 request、未知 kind、clear generation 不符造成的部分失敗、history
defensive-copy 與 nil consumer／presenter。consumer 的唯一直接 import 是標準庫 `fmt`，沒有 machine、
oracle、input、`cmd` 或 renderer 依賴。

## 明確邊界

這份收據只證實 lifecycle value 的一次性消費；它不是 watcher callback、command／遊戲 loop、frame／draw
接線或玩家可見畫面。正式 691 glyph 字型仍受 spec 218 DRAFT 阻擋，原版／繁中 2×／3× same-state RGBA
A/B、答錯換題與存讀檔正常路徑收據均未做。不得因本純核心而聲稱手冊中文已顯示或原版驗證受保證。
