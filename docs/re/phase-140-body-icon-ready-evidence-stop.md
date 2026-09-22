# 第一百四十階段：身體圖示 READY 前置證據停止線

狀態：DRAFT；未接 runtime，未升 READY。

本筆是對既有[第四十八階段](phase-48-body-icon-selection-lifecycle.md)與
`text/body-icon-events.tsv` 的證據稽核，**沒有產生新的原版重播收據**。引用的原版
`GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
下列 `segment:offset` 是 dosgolem 實模式位址，不是 IDA 線性位址。Phase 48 文件
沒有列出起始 state 檔名／雜湊與工具 commit；因此本筆不能取代正式重跑的完整 provenance，
這也是 READY 前需要補的條件。

## 已回查事實

Phase 48 的正常 BIOS 重播已可決定重生身體圖示畫面及其 Enter→N、Enter→Y 分支。正式 identity 對應的四個固定圖示文字 caller 為 `1C41:2708`、`1C41:2729`、`1C41:274A`、`1C41:276B`；其原始長度、SHA-256、色彩與格座標已由 `text/body-icon-events.tsv` 鎖定。確認與儲存詢問則是 `37F1:101E`。

這些僅證實高階 dispatcher 的 completed event，**不**證實低階 `0763:026B` glyph 的 return edge；不得把既有 event 的 `post_call_step` 當成 glyph return 收據。

## READY 前的最小剩餘量測

同一個 phase-48 正常玩家輸入排程至少要各雙重重播移動、Enter→N、Enter→Y 三條分支，並記錄：

- 每一筆四 caller 的 glyph entry、實際 `RETF imm16` 前一指令、返回 CS:IP、entry／return SS 與 SP 差；
- 每條 active body-icon、confirmation、save-prompt stamp 的轉場中，最早與該 stamp 安全矩形相交的原版 pre-write；
- 兩次收據的 content-safe metadata 與終態 indexed framebuffer 相同。

未同時取得上述兩類原版收據前，唯一安全策略是整組失效；這不是可升 READY 的專用清除契約，也不得接 production watcher。

## 本輪探針停止線與可用工具鏈訂正

本輪只嘗試在 Docker 的暫存 dosgolem 副本擴大既有 glyph-return trace 篩選；候選既有映像 `golang:1.24-alpine` 與 `fd2-go-test-local:20260909` 均不含 `go`。依 Docker-only 規則，未以主機替代執行，也未完成這份暫存探針。
訂正：同專案第三頁量測已實際以 `golang:1.26.7-bookworm` 在 Docker 內執行
`go run ./cmd/buckrogers-text-receipt` 並通過測試；因此**不存在全專案 Go 工具鏈阻塞**。
本階段未取得身體圖示低階收據，是這個暫存探針未完成，不是必須退回主機或
另建重複 image。下一輪應沿用該可用 image 與已驗證的唯讀原版掛載繼續量測。
