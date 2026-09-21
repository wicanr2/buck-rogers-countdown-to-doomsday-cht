# 第七十九階段：技能操作列配色中立 runtime 生命週期

日期：2026-09-21

## 結論

Phase 78 builder 已包成 `RuntimeActionBarOverlay`，但 constructor 仍強制 caller 注入 normal
逐 rune 配色，沒有預設值，也尚未接正式 CLI。runtime owner 只持有 presentation layer；
`Apply` 重驗 Phase 76 exact event/request，沒有 screen anchor、identity drift 或非法 clear 都拒絕。

## 生命週期證據

- `Pending` 首幀原本會依原版像素重新定色；runtime owner 在 `xlate.Frame` 完成指紋與錨點後，
  重新套用 caller 指定的 palette RGB，因此全綠 `[10,10]` 不會被原版首字 15 覆寫。
- normal→focus→normal 以 action exact rectangle 整組取代；同畫面其他 action group 保留。
- 清除只碰到 multi-color group 的部分 stamp 時，reconcile 會清掉整組，避免留下半個繁中文字。
- career↔technical exact anchor 切換和 unrelated event 清空 groups；technical 的兩個已證實共享
  career heading 仍保留，與 Phase 75 watcher 契約一致。
- `Actions()` 只輸出 event key、text key、rune 數及 palette indices，不輸出譯文正文。

## 驗證與限制

兩候選、2×／3×、frame／draw、取代、clear、anchor、非法輸入及 deep-copy 測試通過。
dosgolem 正式 package `go test`、排除未版控 `workplace/` probes 的 `go vet`，以及 Buck Rogers
race detector 通過。全域 `go vet ./...` 會掃入既有 `workplace/fd2-input-parity-20260907/`
三個獨立 `main` probes 而失敗，已明確分類為研究工作區掃描問題，沒有刪改該資料。

spec 215 仍是 DRAFT；正式 CLI、正常玩家路徑 overlay 收據與 CONFORMED 狀態仍等待 normal
配色決策。dosgolem 本機分支提交為 `6d230a1`，未推送遠端。
