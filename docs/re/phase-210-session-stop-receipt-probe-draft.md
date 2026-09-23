# 第二百一十階段：session 停止收據與 DOS 退出的合成探針

日期：2026-09-24
狀態：**DRAFT；只量 dosgolem 合成 COM 的現行 API，不是原版玩家路徑。**

## 問題與可重生輸入

[第二百零六階段](phase-206-linux-session-machine-step-delta-draft.md)已證明
`Machine.Steps` 差分計入失敗的 Step 嘗試，且 `StopBudget` 可與非空
error 並存。規格 [019](../spec/019-linux-frontend-session-turn-boundary-draft.md)
仍需區分 DOS 正常退出、起點已終止、零預算、條件／斷點與 CPU error；
本次另存新探針，不修改舊探針釘選的來源。

來源是 ignored `workplace/dosgolem/workplace/phase210-session-stop-receipt-probe/main.go`，
SHA-256 `77de1304e32d304722ca5fa8e5403405a1f6a219cb9ec9bc12e8b00c1d4ae89a`。
合成 COM 僅含 `90h` NOP、`90h 63h` 未支援指令案例，或
`B8 03 4C CD 21`（`MOV AX,4C03h; INT 21h`）正常 DOS 退出案例。
位址空間為合成 COM `PSPSeg:0100h` 起；`0102h` 條件／斷點不是
《拯救地球》位址。原版 EXE、手冊、字型、存態與畫面均未載入。

本機 dosgolem fork commit
`674e3e3fcbf8e36d5ac115da9e9b5bf685564339`；Go 1.26.7，
既有 image `eob-remake-go:1.26.7-ebiten2.9.9` ID
`sha256:39d6e05c9abc60a566e376cde6afd29c24aa21c30eeec1e1fd92c8b16e62aa60`。
以目前 UID/GID、`timeout 90s docker run --rm --network none --read-only
--memory 2g --cpus 2 --pids-limit 256`、唯讀掛載 fork、可執行 `/tmp`
tmpfs 與 `GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`，在 fork 根目錄
執行 `go run ./workplace/phase210-session-stop-receipt-probe`。代理從新路徑
重跑，主代理另以相同無網路容器獨立重跑；下表數值一致。

## API 觀測

| 合成案例 | budget | `Machine.Steps` 前→後 | 原始 `RunUntil` 停止碼／error | 額外狀態 |
| --- | ---: | ---: | --- | --- |
| 零預算，無條件 | 0 | 0→0 | `StopBudget`／無 | 無 |
| 零預算，起點 true 條件 | 0 | 0→0 | `StopPredicate`／無 | 無 |
| 正預算，起點 true 條件 | 8 | 0→1 | `StopPredicate`／無 | 起點成立仍先嘗試一步 |
| 一般預算 | 2 | 0→2 | `StopBudget`／無 | 無 |
| `IP=0102h` 條件 | 8 | 0→2 | `StopPredicate`／無 | 提前停 |
| `IP=0102h` 斷點 | 8 | 0→2 | `StopBreakpoint`／無 | 提前停 |
| DOS 正常退出、無條件 | 2 | 0→2 | `StopBudget`／無 | `DOS.Exited=true`，`CPU.Halted=true`，exit code 3 |
| DOS 正常退出、Halted 條件 | 8 | 0→2 | `StopPredicate`／無 | 同上 |
| 未支援 `63h` | 8 | 0→2 | `StopBudget`／**有** | 第二次失敗嘗試計入 |
| 同一 machine 退出後再呼叫，Exited 條件 | 8 | 2→3 | `StopPredicate`／無 | 已退出仍多嘗試一步 |

**已證實（此合成 API）**：`Machine.Steps` 是累積 Step 嘗試，前後差分
可作本次嘗試數；原始停止碼無法單獨辨識 DOS 正常退出或 CPU error。
正預算 `RunUntil` 對起點已成立的 predicate 仍會先執行一次 Step，
所以未來 session 在呼叫它以前須自檢 terminal phase，不能只交給
predicate 避免退出後多跑。error 必須優先於原始 `StopBudget` 判讀。

**尚未定案（正式契約）**：零預算由 session 接受或拒絕、`Epoch` 應記
machine 累積嘗試數或另一種單調序號、`StopPredicate`／`StopBreakpoint`
如何映射 `ProgramStopped`、以及前端故障與真實資源 Close 的責任。
此探針不自行替規格 019 決定上述政策，也不使其 READY。

建立新探針時曾短暫覆寫既有 phase206 ignored 來源；發現後已將新內容
移到本階段獨立路徑，並以 SHA-256 核對舊 `main.go` **精確恢復**為
`4edf58d7cd13aef2bca7c9a686b523c844680730e69b4efd1f70e69b1d935bda`。
兩份來源與目錄均由目前 UID/GID 持有，沒有 root-owned 或誤建 `.md`
目錄；本輪專用 Docker 容器已清理。
