# 019 — Linux 前端失敗即關閉 session 回合邊界

狀態：**DRAFT；不授權 production 實作，不使規格 004 升 READY。**
日期：2026-09-24

同日 machine 收據：[第二百零六階段](../re/phase-206-linux-session-machine-step-delta-draft.md)
以合成 COM 及現行 dosgolem `Machine.RunUntil` 雙重播證實：
`TickReceipt.Steps` 若取前後 `Machine.Steps` 差分，量到的是含失敗
嘗試的 machine Step 次數，不是保證成功執行的指令數；提前停會小於
budget，`RunUntil` 的 `StopBudget` 遇非空 error 時不得解為預算用完。
正常 DOS 退出、觀測者／前端故障的映射仍未定，本規格維持 DRAFT。

同日 fake 補驗：[第二百零五階段](../re/phase-205-linux-session-failed-close-once-fake.md)
在既有可丟棄 typed session 中，固定 Deliver／Advance 注入故障後的後續輸入拒絕、
重試零步及 Close 計數一次。此結果不涵蓋 Snapshot／Draw／observer 故障或真實資源，
本規格仍為 DRAFT。

同日 fake 勘誤：[第二百零三階段](../re/phase-203-linux-session-mixed-batch-fake-review.md)
將 `InputBatch.DOSInputs` 從「已分類輸入」改為同批候選鍵，補驗
Open／Apply／Cancel＋Enter 的零 fake DOS 副作用、零步及下一關閉回合恢復。
這只補本規格輸入批次負例；實際 machine steps、其他 fault 與
cold-boot 前置仍未驗，本規格維持 DRAFT。

同日勘誤：[第一百九十六階段](../re/phase-196-ebiten-panel-batch-keyboard-gate.md)
已依本機 dosgolem spec 232 的獨立 READY 審查，修正正式 `Game.Update`
的 Apply／Cancel 同批鍵盤漏入 BIOS。下文「現行缺口」保存修正前基線，
不再代表目前程式；本規格其餘 typed Session、budget／step receipt、
phase、Snapshot 與 Close 仍是 DRAFT，未因鍵盤子契約升格。

本規格將正式 Linux／Ebitengine cold-boot 前端所需的最小「一回合」責任獨立出來。
它只界定 host 輸入分流、面板暫停、可量的 DOS 推進收據及失敗後收束；不是原版
冷開機、存讀檔、完整鍵盤映射、視窗 resize／DPI、多作用層聚合或玩家可玩完成規格。
除已確認的 host 操作語意外，本規格不引入遊戲規則、原版輸入或譯文。

## 證據、分級與停止線

| 項目 | 分級 | 可回查證據與限縮結論 |
| --- | --- | --- |
| 面板回合不呼叫 `Advance` | 已證實／限縮 CONFORMED | [第一百九十四階段](../re/phase-194-formal-ebiten-panel-pause-conformance.md)：本機 dosgolem `c273db6` 的正式 `frontend/ebiten.Game.Update`，Open／Select／Cancel／Apply、持續開啟及收合同回合均不呼叫 injected callback；下一關閉回合才恢復。這是 callback 排程，不是 DOS step receipt。 |
| fake session 回合與失敗模型 | 已證實／僅 DRAFT prototype | [第一百九十三階段](../re/phase-193-frontend-session-fake-draft.md)：Open／Select／Cancel／Apply 的零步、下一回合恢復、故障後拒絕推進、Close 一次；它未接真實 Ebitengine、machine 或原版。 |
| 現行正式 API 的缺口 | 已證實 | [第一百九十階段](../re/phase-190-linux-frontend-session-ready-prerequisites.md) 與本機 `workplace/dosgolem` `540a5228e5391ba245da27e04d4fa5f034e060fd`：`Config.Advance` 仍是 `func() error`，沒有 budget、實際 steps、epoch、停止原因、session phase 或 Close。 |
| 起點面板開啟的鍵盤隔離 | 已確認的使用者決定 | 規格 004：面板開啟時鍵盤只由 host 處理，不送 DOS；Cancel／Apply 收合的當回合仍暫停，下一關閉回合才恢復。 |

本規格沒有原版 EXE、手冊、存態、字型或畫面輸入；位址空間不適用。這些素材及其
衍生物不得加入版本控制、GitHub 或公開包。

未納入本子契約的缺口仍由規格 004 維持 DRAFT：cold-boot original/save root
preflight、第一個 instruction 前 observer 安裝、active presentation composite、完整
鍵盤／pointer／window-close 政策、正常玩家路徑、存讀檔和原文／繁中同狀態驗證。

## DRAFT typed contract

下列型別名稱可在 READY 審查時調整，但責任、單調 phase 與收據欄位不可省略：

```go
type InstructionBudget uint64

type SessionPhase uint8 // Booting, Running, Stopped, Failed, Closed
type StopReason uint8   // BudgetExhausted, ProgramStopped, OriginalFault, FrontendFault

type InputBatch struct {
    // 一次 Ebitengine Update 取得的事件；包含 batch 起點的 host state。
    StartedPanelOpen bool
    Events           []InputEvent
}

type InputReceipt struct {
    Epoch       uint64
    Phase       SessionPhase
    HostChanged bool
    DOSDelivered uint64
}

type TickReceipt struct {
    Epoch  uint64
    Steps  uint64
    Phase  SessionPhase
    Reason StopReason
}

type Session interface {
    Deliver(InputBatch) (InputReceipt, error)
    Advance(InstructionBudget) (TickReceipt, error)
    Snapshot(host.OutputScale) (presentation.LayerPresentationSnapshot, error)
    Close() error
}
```

`Session` 是唯一持有 session phase、machine step 與可關閉資源的 owner。`Deliver`、
`Advance`、已安裝 lifecycle owner 的 `Frame`、`Snapshot` 與其 error transition 必須在
同一 goroutine；frontend 只提交 batch／顯示 snapshot，不得持有 machine 或自行推進。
`Snapshot` 是純讀投影：不得 step、讀盤、消費 watcher、呼叫 `Layer.Frame`、清 stamp 或
猜測未登錄 layer。

## 一回合輸入與暫停契約

每個 Ebitengine Update 只建立一個 `InputBatch`，並固定下列順序：

```text
capture batch 起點 panel state → classify/Deliver 全批事件
→ 決定本回合 pause →（僅允許時）Advance(明示 budget)
→ lifecycle owner 更新既有 active layer → Snapshot → Draw
```

1. `StartedPanelOpen=true` 時，**整批 keyboard event 一律由 host 消費，DOSDelivered
   不得因同批 Cancel／Apply 收合而增加**。這是既定「面板開啟時鍵盤只給 host」在
   batch 邊界的直接解讀；特別是 Apply + Enter 同一批時 Enter 不得進 BIOS。
2. batch 起點雖關閉、但本批先命中 Open／host panel hit 而使面板開啟時，該 transition
   後的 keyboard event 同樣只交 host；不得因 event loop 的後續迭代繞過面板焦點。
3. Open、SelectScale、Cancel、Apply 或 batch 結束時 panel 仍開啟，該回合必須回傳
   `TickReceipt{Steps: 0}`，不得呼叫 machine step。Cancel／Apply 收合的當回合仍為零步；
   只有下一個起點與結束皆關閉的回合才可 `Advance`，且必須傳入非猜測的有界 budget。
4. 關閉面板的 DOS event 只有在 route 已明示允許後才可交付；未知鍵、未分類 event 或
   route error 一律拒絕，不得猜 mapping 或部分送入 BIOS／IRQ／mouse。
5. 每個成功 `Advance` 都回傳該 epoch 的**實際** `Steps` 和 `Reason`；callback 被呼叫
   次數不能取代 DOS 指令數或 machine／DOS 同狀態證據。

修正前的 `Game.Update` 曾在 Apply + Enter 同批時，於 pointer Apply 收合面板後，
讓 `key()` 透過 `KeyboardBridge.DeliverBIOSKey` 將 Enter 排入 BIOS；
`panelEventThisUpdate` 雖阻止當回合 `Advance`，卻未隔離整批鍵盤。
此缺口已由 [第一百九十六階段](../re/phase-196-ebiten-panel-batch-keyboard-gate.md)
限縮修正並驗證；本 DRAFT 的 typed session、實際 step receipt 與失敗模型仍未因此完成。

## 失敗即關閉與最小審查矩陣

`Deliver`、`Advance`、lifecycle owner、`Snapshot` 或 `Draw` 任一失敗，必須使 phase 單調
轉為 `Failed`，記錄 `FrontendFault` 或適用的 fault reason，停止本回合後續推進；之後
`Advance` 不得增加 steps。`Close` 必須最多執行一次並釋放 session 擁有的資源；呼叫端可
重複要求關閉，但不得重複副作用。`Closed` 或 `Failed` 後的新輸入不得復活 session。

READY 審查前至少以 ignored fake（不載原版／字型）固定：

1. Open、Select、Cancel、Apply、持續開啟、同回合 open→close 都是零 steps；下一個
   closed batch 才依傳入 budget 前進並有可判讀 receipt。
2. 起點開啟的 Apply + Enter 與 Cancel + Enter 都是零 BIOS／IRQ key delivery；起點關閉後
   Open + Enter 亦不可繞過 host focus。
3. host event 不改 fake DOS BIOS、IRQ、mouse、VRAM 或 save counters；已明示允許的 closed
   DOS event 才能改其對應 counter。
4. Deliver、Advance、Snapshot、Draw、observer 任一錯誤都單調進 Failed，後續 steps 恆定，
   Close 的副作用恰一次。
5. receipt epoch 單調，`Steps` 不超過 budget；`ProgramStopped`、`OriginalFault`、
   `FrontendFault` 與 budget 耗盡不得混稱。

通過上述 fake 與獨立規格審查，最多只可將**此 session-turn typed contract**升為 READY，
授權下一個 production 切片；它不代表 cold boot、Linux 玩家前端、中文多作用層、存讀檔或
原版同狀態 A/B 已完成，更不使規格 004 整體升級。production 完成後仍須依規格 004 的
正常 cold-boot／同狀態驗收另行決定 CONFORMED。
