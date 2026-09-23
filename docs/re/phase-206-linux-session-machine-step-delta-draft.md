# 第二百零六階段：Linux session 的 machine 步數差分與錯誤優先序

日期：2026-09-24
狀態：**DRAFT；只驗 dosgolem 合成 COM 的 machine 計數，不是 Buck Rogers 玩家前端。**

## 問題與輸入

[規格 019](../spec/019-linux-frontend-session-turn-boundary-draft.md)要求
`Advance` 回報實際 `Steps` 與停止原因，但目前正式 Ebitengine 前端只注入
`func() error`，可丟棄 session fake 則直接令 `epoch += budget`。
這兩者都不能證明 DOS machine 真正前進多少。獨立審查後，本輪只針對
`Machine.RunUntil` 的可量邊界寫可丟棄探針，不改 production。

輸入是探針內明列的合成 COM bytes：三個 `90h` NOP，或 `90h 63h`
並把 CPU model 設為 80186；後者的 `63h` 在此 dosgolem 版本未實作。
沒有載入原版遊戲、手冊、字型、存態或玩家資料；位址空間為合成 COM
`PSPSeg:0100h` 起，`0102h` 是條件／斷點的停止位址，不是原版遊戲位址。

可丟棄來源在 ignored
`workplace/dosgolem/workplace/phase206-step-count-probe/main.go`，SHA-256
`4edf58d7cd13aef2bca7c9a686b523c844680730e69b4efd1f70e69b1d935bda`；
本機 dosgolem fork commit
`674e3e3fcbf8e36d5ac115da9e9b5bf685564339`。
使用既有 `eob-remake-go:1.26.7-ebiten2.9.9` image ID
`sha256:39d6e05c9abc60a566e376cde6afd29c24aa21c30eeec1e1fd92c8b16e62aa60`，
Go 1.26.7。工作樹唯讀掛載，`--rm --network none --read-only --memory 2g
--cpus 2 --pids-limit 256`，目前 UID/GID，只有 `/tmp` tmpfs 可寫，
`GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`。兩次從相同來源執行
`go run ./workplace/phase206-step-count-probe`，輸出逐位元組相同。

## 觀測與解釋

| 案例 | budget | 前後 `m.Steps` 差 | 原始 `RunUntil` 停止碼 | error |
| --- | ---: | ---: | --- | --- |
| 零預算 | 0 | 0 | `StopBudget` | 無 |
| 預算耗盡 | 2 | 2 | `StopBudget` | 無 |
| `IP=0102h` 條件成立 | 8 | 2 | `StopPredicate` | 無 |
| `IP=0102h` 斷點 | 8 | 2 | `StopBreakpoint` | 無 |
| 第二次 Step 遇未實作 `63h` | 8 | 2 | `StopBudget` | **有** |

已證實（此合成輸入）：以前後 `m.Steps` 相減可取得 machine 的實際
**Step 嘗試次數**；條件與斷點可以少於 budget 提前停止。`Machine.Step`
在呼叫 `CPU.Step` 前就增加 `m.Steps`，所以故障案例的第二次嘗試也計入
差分；不可把它稱為「成功執行的指令數」。`RunUntil` 在 `Step` 回錯時仍
回傳 `StopBudget` 加非空 error；因此正式 receipt 的原因映射必須**先看
error**，不能把這筆誤報為預算用完。

未知：DOS 正常退出、HLT、observer 故障、前端 `Draw` 故障及
Buck Rogers 真實冷開機的停止分類；合成 `StopPredicate` 也不等於
`ProgramStopped`。零預算目前是 machine API 的可觀測行為，正式
session 要接受或拒絕仍屬 DRAFT 契約，不能由此實驗偷偷定案。
此收據只補 Issue #18 的步數與 error 優先證據，不使規格 019 READY。
