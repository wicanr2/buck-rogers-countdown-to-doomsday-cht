# 第二百零七階段：Linux session 六階段故障矩陣 fake

日期：2026-09-24
狀態：**DRAFT；僅為被 Git 忽略的可丟棄模型，不授權正式前端接線。**

## 範圍與輸入

[規格 019](../spec/019-linux-frontend-session-turn-boundary-draft.md)要求前端回合在
`Deliver → Advance → Observer → Frame → Snapshot → Draw` 中任一階段失敗後，
拒絕後續輸入、停止推進並只關閉一次。沿用
`workplace/phase193-frontend-session-fake/`，新增獨立的 `TurnFake` 與測試，
不改既有 `Session` fake 或 dosgolem production。模型沒有載入原版遊戲、
手冊、字型、存態或畫面；沒有原版位址空間。

新增來源 SHA-256：`lifecycle_fake.go` 為
`8295e6d6ffecdf2a04826da4d9488e1334d4bc237486880144bc488012531339`；
`lifecycle_fake_test.go` 為
`73d9ec631c4ebe35c2a898b7fc543ba53d5e60bcb11870f69349f48e6dfb4079`。
沿用 `session.go` SHA-256
`70e1dbc01da452e62a7cf35543b84a6c38674f3623da51c493b0af8a6fdd0070`、
`session_test.go` SHA-256
`70a8babfde8697393299c11160ea6bad082d98062bf2e818e23df33e5149bb2d`，
以及 `go.mod` SHA-256
`f846467461a6a3baba222db69eddb7efecf1120a0b3ca93dc282b42dd0bf9e44`。

使用既有 `eob-remake-go:1.26.7-ebiten2.9.9`、Go 1.26.7；以目前 UID/GID、
`docker run --rm --network none --read-only --memory 2g --cpus 2 --pids-limit 256`、
可執行 `/tmp` tmpfs、唯讀掛載本專案 `workplace/`，設定
`GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`，在
`/workplace/phase193-frontend-session-fake` 執行
`/usr/local/go/bin/go test -count=1 -v ./...`。八組頂層測試全部通過；
其中新增測試包含六個逐階段故障子案例。

## 觀測

- 單獨 `Snapshot()` 只回傳 fake epoch 與計數器投影；沒有推進、繪圖或改動
  fake DOS 計數器。
- 面板開啟回合的 fake `Steps=0`、`Epoch=0`，仍依序走觀測、畫面與繪圖；
  故「暫停 DOS」不等於停止顯示 host 面板。
- 每個故障子案例先成功前進七個 fake steps，再於下一回合指定階段注入故障。
  `Deliver`／`Advance` 故障回報零新步；其餘四階段故障已完成該回合的
  三個 fake steps，但不執行任何後續階段。故障後再次送鍵、要求 99 步或
  重複 `Close()`，epoch 與 fake DOS 計數器不再變動，Close 副作用計數維持一。
- 這些是可丟棄模型的控制流程結果；`Draw` 在模型中能回傳 error，正式
  `Ebitengine.Game.Draw` 並無相同的回傳介面，不能由此推定正式畫面故障如何傳回 owner。

## 分級與待解邊界

**已證實（fake 範圍）**：上述固定序列的純讀 Snapshot、開面板零步而持續
繪圖、六階段故障後拒絕復活與 Close 一次。

**未知（正式執行期）**：觀測者實際錯誤、Ebitengine 繪圖故障回報邊界、
真實資源釋放、冷開機與原版同狀態。fake `Epoch += budget` 仍不是實際
machine steps；真實差分僅另由[第二百零六階段](phase-206-linux-session-machine-step-delta-draft.md)
的合成 COM 探針限縮證實。規格 019／004 與 Issue #18 保持 DRAFT／未完成。
