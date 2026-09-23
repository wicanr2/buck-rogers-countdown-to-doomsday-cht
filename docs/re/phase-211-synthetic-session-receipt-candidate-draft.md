# 第二百一十一階段：合成 typed session 收據候選與負例

日期：2026-09-24
狀態：**DRAFT；ignored 合成原型，不是正式 session 或原版同狀態收據。**

## 範圍與來源

[第二百一十階段](phase-210-session-stop-receipt-probe-draft.md)顯示現行
`Machine.RunUntil` 的 raw stop 無法單獨分辨 DOS 正常退出與 CPU error，
起點已退出時仍可能多嘗試一步。本階段只在 dosgolem fork 的 ignored
`workplace/phase211-session-receipt-candidate/` 新建 typed 原型，不動
phase206／phase210 已釘選探針，也不改 production 或規格狀態。

`session.go` SHA-256
`e5019b12587613a6c3828e80086c3714c28d96c21acda8c8a374de1a40615905`；
`session_test.go` SHA-256
`3562275ff06296f47a60b31279be18f26d191154ff43c517393d96d0d754434b`。
fork commit `674e3e3fcbf8e36d5ac115da9e9b5bf685564339`，Go 1.26.7，
沿用 image `eob-remake-go:1.26.7-ebiten2.9.9`。原型只載合成 COM：
NOP、未支援指令，以及 `MOV AX,4C03h; INT 21h` 正常 DOS 退出。
位址採合成 COM `PSPSeg:0100h`；沒有原版 EXE、手冊、字型、存態或畫面。

代理與主代理各自在唯讀、無網路 Docker 以目前 UID/GID、
`--rm --read-only --memory 2g --cpus 2 --pids-limit 256`、
可執行 `/tmp` tmpfs、`GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`，
執行 `go test -count=1 -v ./workplace/phase211-session-receipt-candidate`。
五組頂層測試及所有子案例通過；來源雜湊與 phase206／phase210
原有雜湊經主代理獨立核對。

## 候選收據的實測邊界

原型測試一種**候選**先後：在 `RunUntil` 前先查 `DOS.Exited`，
已退出就回零新步且不呼叫 machine；若有執行，從
`Machine.Steps` 前後差分記錄 Step **嘗試數**；判讀時非空 error
優先於 raw stop，無 error 才看 DOS 退出，再保留 predicate、breakpoint
與 budget 各自的原始區別。測試固定：

- 合成 DOS 退出不論 raw stop 是 `StopBudget` 或 `StopPredicate`，
  候選分類都能記為 `DOSExited`；再 `Advance` 時零步、零次 `RunUntil`。
- 未支援指令的 raw `StopBudget` 加非空 error，候選分類是
  `MachineError`，不冒稱預算耗盡。
- predicate 與 breakpoint 的 raw stop 仍分開保存，沒有一律混成
  `ProgramStopped`。
- 零預算同時測「先拒絕」和「直接傳給 `RunUntil`」兩條路，均標
  `ZeroBudgetUnresolved`；此測試**沒有**選定正式政策。
- `AttemptOrdinal` 測得 1、2，同時 `MachineStepsAfter` 測得 2、4。
  原型故意沒有 `Epoch` 欄位，以免用其中一個數字偷定正式語意。

**已證實（合成原型）**：這組固定輸入下，候選型別與流程能保留
足夠觀測欄位，且在退出後防止再 Step。**未證實**：正式輸入回合、
原版冷開機的停止分類、DOS／BIOS 狀態同一性、前端 Draw 錯誤 owner、
真實 Close，以及 `Epoch`／零預算的最終契約。規格
[019](../spec/019-linux-frontend-session-turn-boundary-draft.md) 與 Issue #18
仍維持 DRAFT／開啟。
