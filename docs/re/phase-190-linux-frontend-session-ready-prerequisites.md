# 第一百九十階段：Linux 前端正式 session 的 READY 前置 API 稽核

日期：2026-09-23
狀態：**DRAFT 證據；不授權修改正式 `frontend/ebiten`，不宣稱已可玩。**

## 問題與限定結論

[第一百八十六階段](phase-186-linux-ebiten-cold-boot-lifecycle-ready-gap-audit.md) 已定出冷開機 composition root 的最小 typed contract；[第一百八十九階段](phase-189-ebiten-panel-pause-resume-draft.md) 僅在 ignored caller 驗得面板暫停的實體 DRAFT 排程。本輪以目前 `workplace/dosgolem` API 做唯讀稽核，問題是：現有 Ebitengine 元件是否已有足夠的輸入與回合邊界，可以安全承接正式 cold-boot session？

結論是**否**。`frontend/ebiten.Game` 可重用為 Linux 視窗 backend，但尚不能當作 session composition root，也沒有一個可由外層實作該 root 的完整 typed seam。最小 READY 前缺口不是再做 checkpoint 視窗，而是先明定並以可丟棄 fake 驗證：誰擁有 session phase、每回合的 instruction budget／實際 step receipt、host route 後的暫停決定、active presentation 聚合、cold-boot preflight 與失敗後 teardown。

本文件沒有讀取、輸出或記錄原版 EXE、手冊、存檔、字型 bytes、譯文全文、畫面或 checkpoint；也沒有改動 dosgolem fork 或正式前端。

## 固定稽核輸入與方法

| 項目 | 值 |
| --- | --- |
| 稽核程式 | `workplace/dosgolem` commit `3092dade3aa5deaf86395864a6c539f4088bdf23` |
| 主要檔案 | `frontend/ebiten/game.go`、`presentation/{keyboard,machine,layer_snapshot}.go`、`host/{panel,mouse_bridge,presentation,scale}.go` |
| 方法 | Docker 唯讀掛載的靜態 API／測試稽核；沒有原版輸入或私有 state |
| 位址空間 | 不適用；本輪未提出原版位址、offset 或執行期記憶體結論 |

本輪在 `golang:1.24-bookworm`、`--network none`、目前 UID/GID、`--memory 3g --cpus 2 --pids-limit 512` 中執行 `go test ./frontend/ebiten ./host ./presentation ./apps/buckrogers`。由於該乾淨映像沒有 Ebitengine `v2.9.9` 離線模組快取，frontend 套件在禁止網路下嘗試連至 Go proxy 後失敗；`host`、`presentation` 與 `apps/buckrogers` 則通過。這是容器快取缺口，**不是** frontend 通過收據或產品缺陷結論。先前專用映像的 `PATH` 未含 `/usr/local/go/bin`；即使以絕對路徑啟動 Go，仍無法提供本次需要的 module cache。

本輪每個啟動命令均指定 `--rm`，且沒有建立輸出檔。收尾時發現兩個未標記、無法安全歸屬的 `golang:1.24-bookworm` 運行容器；它們不因映像名稱而可歸為本輪，故未停止或刪除。後續正式收據應為自身容器加上可追溯 label，再做只針對該 label 的清理核對。

## 已證實 API 與不足

| 現有 API／行為 | 分級 | 已能保證 | READY 前仍缺什麼 |
| --- | --- | --- | --- |
| `host.PanelController`／`ScaleController` | 已證實；純核心 CONFORMED 範圍另見既有證據 | 暫選、Apply 自動收合、Cancel 回 active；面板開啟時鍵盤 route 不進 DOS | 沒有回合排程、machine 或 session phase。 |
| `presentation.KeyboardBridge` | 已證實 | 以 `PanelEventKeyboard` route 後才將已明示 BIOS key／scan 送往 DOS；open panel 消費鍵盤 | 沒有 batch receipt、來源時間戳或 session 所屬檢查。 |
| `host.MouseBridge` | 已證實；限縮符合範圍另見第一百七十九階段 | 已接受 left press 的 Down／Up／focus-loss lifecycle 與已知 layout 邊界 | 不持有 machine，且沒有 cold boot、window close 或 session failure ownership。 |
| `MachineFrameSource` → `LayerSnapshotProvider` | 已證實為唯讀投影 | 同 goroutine 讀一份 indexed/palette；複製輸入並以單一既有 `xlate.Layer` 畫 RGBA，不 Step machine | layer owner 必須在外部先 `Frame`；無多 layer composite、generation ownership 或 discontinuity protocol。 |
| `frontend/ebiten.Game.Config` | 已證實為 backend 注入點 | 要求 Panel、Keyboard、Mouse、Snapshot 與 2×／3× host font；畫布固定 320×200 | 接受任意 closure；沒有原版 root、save root、catalog/font preflight、observer 安裝、session Close 或 cold boot。 |
| `Game.Update` | 已證實 | 讀取 Ebitengine input，先 route pointer／key，之後可呼叫 `Advance` | `Advance` 型別只是 `func() error`；無 budget、epoch、step count、停止原因或 phase，且不讀 panel state，故面板展開／Cancel／Apply 收合同回合仍可能 Advance。 |
| `Game.Draw` | 已證實 | 讀 Snapshot 並驗證 320×200、倍率及 RGBA 長度 | Draw/Snapshot 錯誤只寫入 `g.err`，不能使外部 session 立即進入 `Failed`、關閉資源或產生 failure receipt；下一次 Update 才回傳該錯誤。 |

「未找到公開 Buck Rogers cold-boot command／session builder」是**強推論**：本輪固定 commit 的 `apps/buckrogers/` 與 `cmd/` 檔案清冊沒有該遊戲專屬 command，且 `frontend/ebiten.Game` 的 package 註解明示 machine step 與 active overlay lifecycle 由 caller 負責。這不是對未讀程式或未來 branch 的全域否定。

## 必須在 READY 前補齊的 typed seam

下列是 DRAFT 候選，不能直接成為 production API。名稱可調整，但責任不可省略：

```go
type InstructionBudget uint64

type StopReason uint8 // BudgetExhausted, ProgramStopped, OriginalFault, FrontendFault

type TickReceipt struct {
	Epoch  uint64
	Steps  uint64
	Phase  SessionPhase // Booting, Running, Stopped, Failed
	Reason StopReason
}

type Session interface {
	Deliver(InputBatch) (InputReceipt, error)
	Advance(InstructionBudget) (TickReceipt, error)
	Snapshot(host.OutputScale) (presentation.LayerPresentationSnapshot, error)
	Close() error
}
```

候選 host loop 必須由 composition root（或其窄 adapter）**在同一 goroutine**依下列順序呼叫，frontend 不得自行猜補：

```text
preflight → 建 machine/DOS → 安裝全部宣稱 layer 的 observer → cold boot
→ 分類一個輸入 batch／Deliver
→ 若該回合是 Open、Select、Cancel 或 Apply：記錄 Steps=0
→ 僅下一個 closed-panel 回合 Advance(有界 budget)
→ lifecycle owner 更新 active composite → Snapshot → Draw
```

`Snapshot` 必須純讀；不得 step、重新讀盤、消費 watcher、呼叫 `Layer.Frame`、清除 stamp 或建立猜測的 layer。Snapshot／Draw／Deliver／Advance 任一錯誤都必須使 session 以單調 phase 轉入 `Failed`；之後不得再 Advance，並須由 `Close` 收束可關閉資源。

## READY 前必要的可丟棄測試

在未改 production 前，可於 ignored `workplace/` 建立 fake-only session 原型；不得載入原版或把 prototype import 到 `frontend/ebiten`。最小測試必須固定：

1. Open、Select、Cancel、Apply 各自的輸入回合回傳 `Steps=0`；下一 closed-panel 回合才以傳入 budget 前進，且 receipt 的 epoch／reason 可判讀。
2. `Deliver` 的 host 消費事件不改 fake DOS BIOS／IRQ／mouse／VRAM／save counters；closed-panel 已明示輸入才可改對應 counter。
3. `Snapshot`、`Draw`、`Advance`、observer fault 任一失敗均使 phase 成為 `Failed`；後續 Update/Advance 的 step counter 恆定，`Close` 恰好一次。
4. active composite 拒絕未登錄 font、重複 z-order、跨 generation、partial group 與 discontinuity 後殘留 stamp；失敗時保留原始 indexed 投影、不畫譯文。
5. cold-boot preflight 拒絕不存在／雜湊不符 original root、等同或不可寫 save root、catalog/font/hook 缺項；所有拒絕案例均不開窗、不寫 original root 或 save root。

上述 fake 測試只能把 session contract 推至 READY 候選；真正 READY 還需以已安裝的實際 observers、Linux/X11 Ebitengine callback、正常 cold boot 與至少一條玩家路徑補足第一百八十六階段矩陣。它們更不能替代原文／繁中同 state、存讀檔或所有 overlay lifecycle 驗收。

## 結論與停止線

本輪結論為 DRAFT：現有 frontend 是有價值的 backend 元件，卻缺少可審計的 session 回合擁有權與冷開機 composition root。暫停語意在第一百八十九階段已有 ignored 實體證據，但目前 `Game.Update` API 不足以保證該決定，故不可接成正式玩家前端。待上節 typed seam 與 fake failure matrix 被獨立審查為 READY 後，才可提出 production 實作；之後仍須以 dosgolem 正常 cold boot 的同狀態收據決定是否 CONFORMED。

## 同日工具環境勘誤

上述 `golang:1.24-bookworm` 的 Ebitengine cache 失敗及登入 shell 的 PATH
失敗，只是該次測試命令／映像的限制，**不能推論既有專用映像無法測試前端**。
主代理改用已存在的 `eob-remake-go:1.26.7-ebiten2.9.9`、非登入 shell、
`--network none` 與有界 Xvfb，在相同 dosgolem fork 上重跑
`go test ./frontend/ebiten ./host ./presentation ./apps/buckrogers -count=1`，
四套均通過。這訂正前段關於專用映像離線快取的外推；API／session 的
DRAFT 缺口仍由上列程式契約決定，綠色元件測試不構成冷開機玩家驗收。
