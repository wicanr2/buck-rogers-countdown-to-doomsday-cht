# 第二百零五階段：Linux session 故障後拒絕推進與單次關閉 fake

日期：2026-09-24
狀態：**DRAFT 負例；只驗可丟棄 typed fake，不授權正式前端實作。**

## 問題與範圍

[第二百零三階段](phase-203-linux-session-mixed-batch-fake-review.md)已驗同批面板轉移與候選鍵隔離；
原有故障測試只在故障後嘗試一次 `Advance`。本階段沿用被 Git 忽略的
`workplace/phase193-frontend-session-fake/`，不新增 session 操作或正式 API，
補驗先成功推進一回合後發生 `Deliver` 或 `Advance` 故障時，後續輸入與重試均不能復活 session。

兩個子案例各從新建 fake session 開始：先交付一筆已允許的候選 DOS 鍵，再以明示 budget 7
取得 `Steps=7`、`Epoch=7`。其後分別注入下一次 `Deliver` 與下一次 `Advance` 故障。
故障後送入含面板 Open 與 DOS 候選鍵的 batch 必須遭拒；兩次 `Advance(99)` 均回錯，
`Steps=0`、`Epoch=7`、`Phase=Failed`、`Reason=Failed`。兩次明示 `Close()` 後，
phase 仍為 Failed、Close 計數仍為 1，fake BIOS／IRQ／mouse／VRAM／save 計數保持故障前值。
這些是 fake 計數器與回傳值，不是原版 DOS 指令、資源釋放或持久化狀態收據。

## 可重生輸入與結果

- fake `session.go` SHA-256：`70e1dbc01da452e62a7cf35543b84a6c38674f3623da51c493b0af8a6fdd0070`；
  `session_test.go` SHA-256：`70a8babfde8697393299c11160ea6bad082d98062bf2e818e23df33e5149bb2d`；
  `go.mod` SHA-256：`f846467461a6a3baba222db69eddb7efecf1120a0b3ca93dc282b42dd0bf9e44`。
- 沿用已存在的 `eob-remake-go:1.26.7-ebiten2.9.9` 映像；以目前 UID/GID、
  `--rm --network none --read-only --memory 2g --cpus 2 --pids-limit 256`、
  可執行的 `/tmp` tmpfs，唯讀掛載專案 `workplace/`。
- 容器內設定 `GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`，在
  `/workplace/phase193-frontend-session-fake` 執行
  `/usr/local/go/bin/go test -count=1 ./...`：全部五組頂層測試通過，包含新增的
  `TestFailedSessionRejectsLaterInputAndStepsWithOneClose` 兩個故障子案例。

## 證據等級與停止線

**已證實（fake 範圍）**：既有 `Session` 的兩個可注入故障路徑，於上述固定操作序列
拒絕後續輸入與步進，且 Close 副作用計數恰一次。
**未知（正式執行期）**：`Snapshot`、`Draw`、observer 故障，實際 machine 指令數、
真實資源釋放、冷開機、原版狀態、實體視窗與多作用層。既有 fake 沒有這些操作，
本階段不替它猜介面，也不把 `Epoch=7` 說成真實 DOS 步數。
規格 [019](../spec/019-linux-frontend-session-turn-boundary-draft.md) 與
[004](../spec/004-dosgolem-host-frontend-draft.md) 均維持 DRAFT；Issue #18 尚未完成。
本實驗未載入原版遊戲、掃描手冊、字型、存態或畫面，沒有可公開散布的第三方素材。
