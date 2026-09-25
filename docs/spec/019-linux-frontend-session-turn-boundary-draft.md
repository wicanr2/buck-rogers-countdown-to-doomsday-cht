# 019 — Linux 前端失敗即關閉 session 回合邊界

狀態：**READY（限新建封閉 owner 的 session-turn 與值型 View 子契約）；View 已限縮接入正式 owner，畫面 Snapshot、正式前端及原版 cold boot 尚未實作，規格 004 仍 DRAFT，且本規格尚未 CONFORMED。**
日期：2026-09-24

本檔較早的 DRAFT／「READY 候選」段落保存阻塞如何被發現；現行裁決以末節
〈2026-09-24 獨立審查定案：封閉 session owner 限縮 READY〉及本文末節的
值型 View 限縮 READY 為準。不得把既有可注入任意 bridge 的
`Game.New(Config)`、現有 frontend，或任一 ignored 原型誤稱已符合此契約。

implementation 起點：本機 dosgolem fork `b062c5b` 已加入不呼叫 DOS 的
`host.PlanMouseRoute` 單事件純值計畫，以及 `Game.Draw` 首次可檢查
故障的同步 `OnDrawFault` 通知。二者各有正式程式定向測試，
後續 `6e85c32` 使首次故障後不再重讀 snapshot；`117e0cc` 新建
私有 machine／DOS／panel／bridge 的 `session.Owner` 生命週期外殼，
先完成 Booting、首次 fault→Failed、單次 Close 與 Close error 保存。
後續本機 fork `b8c6bca` 的實作切片已加入合成 COM 的 typed `Advance` 收據與
私有 `startLoadedMachine`／`acceptTurn`；這些測試只在無觀測者的
`Machine.RunUntil` 成立，沒有遊戲文字 Watcher。後續 `329d816`／
`0546e2a` 已加入合成回合的純 Prepare／封閉 Commit、2×／3× 面板
版面私有投影與矛盾輸入的首動作前拒絕；`3b8688e`／`2901c98`
使現有 Ebitengine 前端共用純命中／版面投影；`a7cb0eb` 將同源
值型 View 與整批版本核對接入正式 owner。這些是**限縮的
無觀測者元件收據**，不涵蓋實體前端回合全矩陣。Booting 仍未載入
原版 EXE，故不得提前呼叫 `DOS.Install()` 或推進。原版冷開機、
observer-aware runner、畫面 Snapshot、正式前端交界、
`Game.OnDrawFault` 的真正 owner 接線及正常玩家路徑仍未完成；
本規格仍未 CONFORMED。

同日獨立路由複核：現行正式 `Game.Update` 在合成 DOS／真實 bridge
矩陣中，對未映射 F1、畫布外 Down、普通 unmatched Up、重複 Down
均維持既有無動作政策；混合批次仍只送出合法 Enter／Up。
因此候選 session 不需擅自改成「遇任何非命中輸入整批拒絕」。
證據見[Issue #18 審查末節](../re/issue-18-session-turn-ready-candidate-review.md#2026-09-24-現行非命中輸入的無動作矩陣)。
這只消除輸入政策的候選歧義；封閉 owner、排他提交與同步故障收束
仍未證實，本規格不升 READY。

現況追加：dosgolem fork `7ff0581` 的 `MouseBridge.Snapshot()` 已
提供含 `PressedEpoch` 的唯讀純值狀態；ignored 私有批次 v2 以此
在 `prepare` 前擋下跨 epoch 狀態漂移，並有完整快照／純計畫
終態等價測試。這只勘誤下文較早「公開 getter 缺 pressedEpoch」
的**觀測 API 缺口**，不是正式 session 已有 revision token 或
排他提交。ABA／直接 mutator 仍可繞過舊 plan；READY 判定不變。
收據見[Issue #18 審查末節](../re/issue-18-session-turn-ready-candidate-review.md#2026-09-24-完整滑鼠快照原型複驗)。

目前供審查的收斂契約見本文末〈限縮 READY 候選〉；上方 DRAFT 型別與
未決敘述保留當時的研究歷程，不作為現行實作依據。候選證據與未驗範圍見
[Issue #18 session-turn 審查紀錄](../re/issue-18-session-turn-ready-candidate-review.md)。

同日合成 typed 原型：[第二百一十一階段](../re/phase-211-synthetic-session-receipt-candidate-draft.md)
以退出前置檢查、machine Step 差分及 error 優先組成候選收據，
五組合成測試通過。它不決定零預算與 Epoch 語意，不處理正式
Draw 故障或真實 session owner，故本規格仍為 DRAFT。

同日合成退出探針：[第二百一十階段](../re/phase-210-session-stop-receipt-probe-draft.md)
證明正常 DOS 退出時原始 `RunUntil` 仍可回 `StopBudget`，起點已退出
卻以正預算再次呼叫時還會多嘗試一步。正式 session 必須在呼叫前
自檢終止狀態，error 判讀優先於 raw stop；零預算、Epoch 與
停止原因的完整映射仍屬 DRAFT。

同日獨立 READY 前審查：本限縮子契約仍有三個未閉合邊界：
`InputBatch` 內 DOS 鍵與 Open 的先後交付、`Steps`／`Epoch`／停止原因對
真實 machine 早停與 error 的映射，以及正式 `Draw` 故障回報 owner 的路徑。
因此下列 fake 與合成 machine 結果只授權繼續補證，不可將本規格升 READY。
規格 004 的完整冷開機／玩家路徑是後續 production 驗收，不應冒充本
限縮子契約的 READY 前置。

正式程式唯讀核對：本機 dosgolem fork `frontend/ebiten/game.go` 的
`Draw` 在 `Panel.Snapshot`、presentation `Snapshot` 或
`validateSnapshot` 回錯時只把 error 存入 `Game.err`，下一次 `Update`
於任何 `Advance` 前回傳該 error；這能擋住**下一次**推進，卻沒有通知
session owner 轉 `Failed` 或執行 Close。正式 `Draw` 不能回傳 error，故
READY 前須明定可實作的同步故障通知／收束邊界，且把 Ebitengine 本身
無 error 回傳的繪圖呼叫與可檢查的 snapshot／validation 故障分開。

同日補充一個 ignored、僅測試用的同步通知原型：
`workplace/dosgolem/frontend/ebiten/draw_fault_owner_draft_test.go`（SHA-256
`e451ae11ee950d7b3dab76f4df484455e823c5dd97bb9b245d96ff55f73f553a`）。
它用 wrapper 在正式 `Game.Draw` 返回後、下一次 `Update` 前立即讀取
`Game.err`，把 snapshot 故障及 3× host 字型缺字各送達合成 owner，
兩組測試皆只關閉一次、下一次 Update 零步。追加 typed fake 也驗了
故障後拒絕 batch／Advance、保留首次錯誤、Close 只一次，並另存
Close error。主代理在 Go 1.26.7／Ebitengine 2.9.9 的 Docker／Xvfb
重跑定向測試、`go vet` 與競態測試通過。wrapper 沒有真正 session／
資源 Close、Close error 對外政策，亦未解決整批輸入原子性；
正式 `Game` 未修改。本規格仍是 READY 候選，不能因此升 READY。

同日六階段 fake：[第二百零七階段](../re/phase-207-linux-session-six-stage-fault-fake.md)
補上 Observer、Frame、Snapshot、Draw 的可丟棄故障注入，並驗面板暫停仍可畫
host 面板、Snapshot 純讀。這只驗 fake；正式 `Ebitengine.Game.Draw` 無 error
回傳，故障如何通報 session owner 尚未解決，本規格仍為 DRAFT。

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

`InputBatch.Events` 目前仍是 DRAFT 型別佔位，**不是**實體事件的時間戳序列。
現有 Ebitengine `readFrameInput` 一次取回 pointer edge 與鍵盤候選清單，
`Game.Update` 依 pointer Down、Up 再到鍵盤的固定程序順序處理，無法還原
同一 Update 內「鍵先於點擊」的實際時間順序。沿用[第一百九十六階段](../re/phase-196-ebiten-panel-batch-keyboard-gate.md)
已驗的 host 優先批次政策：只要起點面板開啟、pointer 路由中有任一
面板轉移，或批次結束仍開啟，**整批**鍵盤候選都不送 DOS；起終皆
關閉且無 host 面板轉移時，才可依鍵盤候選清單順序送已明示映射的鍵。
若 host 路由失敗，立即停止，不可先交付部分 DOS 鍵。正式 typed
事件型別仍須把 pointer 候選與鍵盤候選分開表達並以負例驗證；本段
只釘住現行正式 frontend 與 fake 一致的可觀測語意，不宣稱 READY。

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

## 限縮 READY 候選：一回合的可實作責任

本節是待獨立審查的規範候選，覆蓋上文尚未決定的同批交付、epoch、
停止分類與 `Draw` 故障通報。它只接通通用 session-turn 邊界；原版冷開機
前置、多作用層、玩家路徑與存讀檔仍由規格 004 維持 DRAFT。
正式型別至少須能分別表達 pointer 候選、焦點與有序鍵盤候選；
`TickReceipt` 除 epoch／phase／reason 外須包含 budget、machine 前後
steps、實際差分、原始 stop 及錯誤來源。停止原因須明示
`PanelPaused`、`BudgetExhausted`、`ProgramStopped`、
`PredicateStopped`、`BreakpointStopped`、`OriginalFault`、
`ObserverFault` 與 `FrontendFault`，不能沿用上文四值 DRAFT enum
而把不同停止條件合併。對外 API 是否以欄位或附屬 detail struct
承載原始 stop 可由實作決定，但收據資訊不得遺失。

### 批次輸入與交付順序

`InputBatch` 必須分別攜帶本次 `Update` 擷取的 `PointerDown`、`PointerUp`、
焦點狀態及有序鍵盤候選清單，並記錄擷取前的面板狀態。候選清單不是
跨設備時間戳；前端不得聲稱知道鍵盤與 pointer 的物理先後。對現有
`readFrameInput`，規範順序固定為 pointer Down → pointer Up → 焦點失去
清理 → 鍵盤候選。先分類並完成整批 host 路由，才交付任何 DOS 鍵。

只要起點面板開啟、批次中出現 Open／Select／Cancel／Apply 面板轉移，
或終點面板仍開啟，整批鍵盤候選都由 host 消費，`DOSDelivered=0`。
因此 Apply／Cancel＋Enter 及 Open＋Enter 都不會把 Enter 送入 BIOS。
起終皆關閉且沒有面板轉移時，僅依現有明示映射按鍵盤候選清單順序
交付 DOS；任何未分類輸入或 route error 必須在交付前拒絕整批。
pointer 對 DOS 的已定案路由沿用規格 004 與 MouseBridge 契約；本節
不推定未支援滑鼠按鍵或鍵盤映射。已交付的 DOS pointer 動作無法在
後續 route error 時回滾，故正式實作須先對整批 route 做可失敗預檢，
再按固定順序提交；預檢不得改 DOS 狀態。現行
`PanelController.Route` 會改 host state，`MouseBridge.Handle` 可能立即
呼叫 DOS mouse，不能拿這兩個正式物件「試跑再回滾」。需用純資料
route plan 或等價的獨立暫態完成預檢，確認所有 payload、layout epoch、
focus、host transition 與 keyboard transport 後才提交；若提交階段的
既有無錯誤回傳 DOS queue／mouse 呼叫之外仍可能失敗，必須另證明
不會造成部分送入，否則這批交付不能宣稱原子拒絕。

#### 整批純路由預檢與單次 DOS 提交：待審 typed 契約

此段是 READY 前的**待審契約**，不是現行 API 已有的能力。「單次提交」
指同一個 `Update` 只有一個通過完整預檢的提交階段；`MoveMouse`、
`PressMouse`、`ReleaseMouse` 與 `DOS.PushKey` 仍是數個既有呼叫，
不宣稱 DOS 提供交易或回滾。原型中的 canvas Down → 關閉面板時
`PanelEventApply` 已實測：逐事件提交在後段回錯時留下 DOS 左鍵；
證據見[審查紀錄](../re/issue-18-session-turn-ready-candidate-review.md)。

建議型別的**必要資訊**如下；實際名稱、欄位歸屬與封裝可於 READY
審查調整，但不可遺失其狀態或憑空重算跨設備時間順序：

```go
type CapturedUpdate struct {
    StartedPanel host.PanelState
    Layout host.MouseLayout // 本批擷取所用的完整值，含 Epoch
    PointerDown, PointerUp *host.MouseEvent
    Focused bool
    Keys []MappedKeyCandidate // 原始順序、明示 transport、payload／未映射結果
}
type MouseRouteState struct {
    HasCurrent, Pressed, HostCaptured bool
    Current host.MouseLayout
    PressedEpoch uint64
}
type RouteBase struct {
    Panel host.PanelState
    Mouse MouseRouteState
    FrontendLayout host.MouseLayout
    OwnerPhase SessionPhase
    PendingUpdate bool
    SourceGeneration uint64 // 唯一 owner 的單調版本；不可由值狀態雜湊替代
}
type PreparedUpdate struct {
    Base RouteBase
    FinalPanel host.PanelState
    FinalMouse MouseRouteState
    Pause bool
    HostTransition bool
    DOSActions []PreparedDOSAction // 已定序的 mouse 操作與 BIOS／IRQ transport
}
```

`MappedKeyCandidate` 不可只保留 `dos.Key`：需保留來源候選是否受現有
`mapKey` 支援、選定的 BIOS／IRQ transport 及已驗 payload。現行
`Game.key` 對未映射鍵直接略過；此契約不得默默把它猜成 BIOS key。
若正式政策仍允許略過，plan 要明列為「不交付」並加測；要改為整批
拒絕則先審其玩家可見影響。`PreparedDOSAction` 只記已驗的參數與順序，
不持有可於提交時重新分類的原始 pointer 或視窗座標。

`SourceGeneration` 必須覆蓋 panel、mouse、frontend layout／phase／pending
的所有成功變更，並由同一 owner 擷取與核對。單憑完整值快照仍不夠：
Open→Cancel 及 canvas Down→Up 可回到逐欄相同的值，卻已發生來源變動
及 DOS 動作（ABA）。若外部仍可繞過 owner 直接呼叫 `PanelController.Route`、
`MouseBridge.Handle` 或 `ApplyLayout`，僅由 owner 包裝方法增加版本也無效；
正式 API 須把這些 mutator 納入共同版本管理，或限制來源生命週期內
只能透過 owner 寫入。`MouseRouteState` 的私有欄位必須由 host 層一次
取得，不得由 frontend 用公開 getter 拼湊。

預檢在唯一 session owner 的同一 goroutine 讀取 `RouteBase`，對獨立
值狀態依 `Game.Update` 的 Down → Up → focus loss → 鍵盤候選順序
模擬整批。pointer hit test 使用擷取當下的 layout；每個 host transition
使後續事件使用的 panel／layout 狀態變化必須按正式 `refreshLayout`
語意預先算出，不可把舊 epoch 當新 layout。`MouseBridge.Handle` 的
pressed、pressedEpoch、hostCaptured 與 current layout 必須由其內部
狀態的唯讀快照或同一純 evaluator 取得；公開 `Pressed()`、
`HostCaptured()` 和 `Layout()` 仍缺 pressedEpoch，不能完整重建 Up
的 epoch-changed-release 分支。預檢不得碰正式 `PanelController`、
正式 `MouseBridge`、DOS mouse／keyboard queue、`Machine.Steps`、
視窗尺寸或 session epoch。

路由結果須分辨「轉送」、「host 消費」、「依既有語意可接受的無動作」
與「拒絕整批」。例如 `MouseBridge` 對既有 pressed 的 Up、非 canvas Up
或失焦會釋放；沒有 pressed 的 focus loss 仍會清除 host capture，
不可因其回傳 `unmatched-up-rejected` 就跳過清理。沒有 pressed 的
普通 Up、重複 Down、畫布外 Down 目前由正式 `Game.routePointer`
忽略其 route reason；是否保留無動作或改為拒絕，須在 READY 審查
列舉理由並固定測試，不得靠字尾 `rejected` 一概判定。stale layout、
未知 event／button、非法 host transition 或錯誤鍵盤 transport／payload
必須在任何 DOS 動作前被預檢拒絕。host transition、起點或終點面板
開啟時的整批鍵盤隔離沿用上節，不因 Apply／Cancel 收合而改判。

預檢成功後、第一個 DOS 動作前，提交端一次核對 `RouteBase` 仍與
目前 panel、mouse、layout、phase、pending 回合相同；沒有相同狀態
就拒絕且 DOS 零新副作用。提交不得再呼叫可失敗的 hit test、鍵盤
映射、layout 驗證或 `ApplyLayout`。若以現行 `PanelController.Route`
或 `MouseBridge.Handle` 重播 plan，必須證明其每一步在已核對的狀態
下不會出現新的普通拒絕；只比對批次起點而不驗後續狀態轉移不足以
證明這一點。較小的通用 API 方案是由 host 層提供 panel 與 mouse
的純預檢／不可變計畫，並提供在核對來源狀態後**不再做可失敗路由**
的提交操作；session adapter 只負責編排既有 DOS 輸出與鍵盤 transport。
具體候選介面可為單一 `HostRouteOwner.Snapshot() (RouteBase, error)`、
`Prepare(base, []HostRouteCandidate) (HostRoutePlan, error)` 與
`Commit(plan) ([]PreparedDOSAction, error)`；`Commit` 在任何 DOS 輸出前
核對同一版本及完整起點，然後安裝已驗 host 末態並交出定序動作，
不可重播 `Route`／`Handle`／`ApplyLayout`。同 goroutine 內交出動作至
DOS 的區間禁止重入或外部 host mutator；若不能建立此排他性，就須
將動作輸出也收進同一 owner 的提交操作。這是待獨立審查的最小通用
API 形狀，不是已核准的正式實作。
若無法實作此保證，規格仍停在 DRAFT／READY 候選，不以 fake 計數
或一次成功批次宣稱原子拒絕。

提交完成後才將同一批接納為一個 session epoch，記錄 host 終態、
DOS action 數與 pause 決定；拒絕批次不增加 epoch、不送 DOS、不
呼叫 `Advance`，首次可回報錯誤依本規格進 `Failed` 並 Close 一次。
這裡的「零副作用」限 DOS button／座標／mouse callback queue、
BIOS／IRQ queue 與 `Machine.Steps` 的**新增**副作用；既有按住的左鍵
與既有佇列不可被錯誤測試誤判為本批新增。失焦清理若是有效批次，
其 Release 是有意提交，不應歸成拒絕批次的零副作用。此契約不宣稱
記憶體耗盡、程序中止或 Ebitengine 繪圖呼叫可交易式回滾。

READY 前的具體矩陣：

| 起點／批次 | 預期可觀測結果 |
| --- | --- |
| 未按住、canvas Down 後非法 Apply 或 stale Up | 整批拒絕；DOS button／座標／callback／keyboard queue 及 Steps 均無新增；phase Failed、epoch 不增。 |
| 已按住、有效 canvas Up／非 canvas Up／跨 epoch Up | 預檢與提交一致，恰一次 Release；不得留下 pressed 或重複 release。 |
| hostCaptured Down 後 Up；失焦時有／無 DOS pressed | host capture 清理與 DOS Release 分別符合來源狀態；無 pressed 的失焦不能產生多餘 DOS Release。 |
| 同批 Down＋Up；layout／倍率轉移；舊 layout event | 以本批固定順序和各事件正確 layout 計畫；錯誤 epoch 在提交前拒絕，成功時最終 mouse／panel／frontend layout 與 plan 相同。 |
| 起點開啟的 Apply／Cancel＋Enter；起點關閉的 Open＋Enter | 整批 BIOS／IRQ 零交付、零 machine step；下一個關閉回合才可恢復。 |
| 合法 canvas pointer＋多個已映射鍵；末尾未映射或非法 transport | 有效批次依原序交付且計數吻合；未映射處理須符合已審政策，非法 transport 在第一個 DOS 動作前拒絕。 |
| 預檢後狀態／layout token 改變；提交階段可注入錯誤 | 不得部分送入 DOS；若做不到，需縮小或改寫正式提交 API，再審 READY。 |

矩陣須在真實 bridge 與實際 `readFrameInput` adapter、無原版素材的
可重播測試中完成；純資料 fake 只能證明前置邏輯。此子契約的
READY 不等於規格 004 的 cold boot、正常玩家路徑或同狀態完成。

### epoch、預算與停止收據

`Epoch` 是每個**成功接納的 Update 批次**的單調序號，從 1 開始，
同一批的 `InputReceipt`、暫停或執行的 `TickReceipt` 與 snapshot 共用它。
面板零步批次也增加一次；拒絕批次、重試失敗呼叫、單獨 `Draw`／`Close`
都不增加。它不是 `Machine.Steps`、畫面 layout epoch、虛擬時間或
`Advance` 呼叫次數。`Deliver` 恰一次建立本回合 epoch；`Advance`
只能消費該回合一次。未經 `Deliver`、重複 `Advance` 或未完成上回合
便開新回合，均是前端契約錯誤，進入 `Failed`。

暫停回合不呼叫 `Machine.RunUntil`，回傳 `Steps=0`、`PanelPaused`；
它的 budget 不參與判讀。可執行回合必須給正數、有界的
`InstructionBudget`；零預算在呼叫 machine 前拒絕，記為前端契約錯誤，
進入 `Failed`，不能將 `RunUntil(0)` 的原始停止碼解為耗盡預算。
budget 的具體常數由正式 caller 明示並另行驗證，不由本契約猜定。

`Steps` 定義為本回合 `Machine.Steps` 後值減前值，即**Step 嘗試數**；
失敗的嘗試也可能計入，不能稱為成功執行的指令數。前值大於後值、
差分大於 budget 或計數溢位均視為契約故障，停止後續回合。
每次執行前先查 `DOS.Exited`：已退出則不呼叫 `RunUntil`，回傳
`ProgramStopped, Steps=0` 並進入 `Stopped`。執行後依下列優先序
分類，收據同時保留原始 `machine.Stop` 與原始 error 供稽核：

1. 非空 error 優先；觀測者已明示包裝的錯誤為 `ObserverFault`，
   其餘 machine 錯誤為 `OriginalFault`，phase 轉 `Failed`，即使原始
   stop 是 `StopBudget` 或 DOS 同時設為 exited 亦同。
2. 無 error 且 `DOS.Exited` 為 true，`ProgramStopped`，phase 轉 `Stopped`；
   raw `StopBudget` 不能覆蓋這個已觀測的 DOS 狀態。
3. 無 error 且未退出時，`StopPredicate` 與 `StopBreakpoint` 分別回
   `PredicateStopped`、`BreakpointStopped`，不得偽稱程式結束或預算耗盡。
   正式 caller 若未宣告這類停止用途，將其視為 `OriginalFault`。
4. 只有無 error、未退出、raw `StopBudget` 且 `Steps=budget` 才回
   `BudgetExhausted`。其他組合為 `OriginalFault`，不得猜測成功。

`TickReceipt` 即使故障也必須保留已量到的 epoch、budget、前後
`Machine.Steps`、實際 `Steps`、raw stop、error 類別與 phase，
避免把故障前已發生的嘗試寫成零步。`Stopped`／`Failed` 後的
`Advance` 一律零**新**步；`Stopped` 可回相同終止原因，`Failed`
回原始故障，不得重新進入 `Running`。

### `Draw` 故障通知與關閉 owner

Ebitengine 的 `Game.Draw` 無 error 回傳值。正式接線須把可檢查的
`Panel.Snapshot`、session `Snapshot`、`validateSnapshot` 等失敗，
在發現當下以同 goroutine 的 `ReportDrawFault(error)` 同步通知唯一
session owner；`Game` 同時鎖存該 error，下一次 `Update` 先回錯，
不得再交付輸入或推進 DOS。通知至多一次，且不得僅靠下一次
`Update` 才使 session 轉 `Failed`。Ebitengine 繪圖 API 本身未提供
error 回傳；本契約只涵蓋可檢查的錯誤，不虛構 GPU 故障收據。

session owner 收到 `Deliver`、`Advance`、observer／Frame、`Snapshot`
或 `ReportDrawFault` 的首次故障時，立即鎖存根因、轉 `Failed`、
停止後續階段並呼叫一次資源關閉；重複失敗或 `Close` 不重複副作用。
對外明示 `Close` 可重複呼叫，正常視窗結束也由同一 owner 呼叫。
`Closed` 及 `Failed` 均拒絕新輸入與新步進；關閉不抹除先前故障
收據。正式接線必須實測 `Draw` 同步通知、下一次 `Update` 零步、
資源只關一次，以及關閉錯誤的保存；既有 fake 只證明控制流程模型。

## 2026-09-24：DOS 提交目標不一致的正式 bridge 反證

ignored `workplace/dosgolem/frontend/ebiten/route_commit_target_alias_draft_test.go`
（SHA-256 `c73093b27b5d5b362fd7833ed9c674503965bf9c28287519e457ae5a986cd8bc`）
只用合成 machine／DOS，經正式 `Game.New`→`Game.Update` 重現兩例：
一是 `MouseBridge` 接 DOS A、`KeyboardBridge` 接 DOS B，兩個 bridge
各自合法，結果同批 canvas Down＋Enter 把滑鼠寫到 A、鍵盤寫到 B；
二是起點共用 DOS，但在回合 BIOS 前檢後、輸入擷取時改指公開的
`DOS.M`，Down 已改滑鼠位置並按左鍵，後段 `DeliverBIOSKey` 拒絕，
兩台 machine 均未收鍵。兩例 machine steps 均為零。主代理在唯讀、
無網路、有界 Docker／Xvfb 獨立重跑定向兩例及 `go vet` 通過。
此處沒有原版素材，也不證明玩家實際操作會觸發該改指。

這推翻「只核對 panel／mouse／layout 與鍵盤自身 BIOS 目標即可
保證同批 DOS 原子交付」的假設。READY 前，`RouteBase`／來源版本
還須涵蓋滑鼠輸出、鍵盤 transport 所指的**同一 DOS 與同一 machine**，
以及會改變該身分的所有 rebind；唯一提交 owner 必須在整批動作期間
排除 rebind／重入，否則須把完整輸出收進同一個可驗的提交邊界。
僅加一次前檢仍不足以阻止後段普通錯誤。規格仍為限縮 READY 候選；
此為補充的技術阻塞，不改使用者既定的面板／滑鼠操作決定。

## 2026-09-24：共同提交 owner 的可丟棄原型

ignored `workplace/dosgolem/frontend/ebiten/route_commit_owner_draft_test.go`
（SHA-256 `a750e68ea6a299d6ba04f48afd7b025876214df59f4fa6277cba3b3c78c12069`）
用合成 DOS／machine 把既有純路由計畫、共同目標、單調 generation
與一次提交放在同一個測試 owner。後段預檢錯誤、不同 DOS 目標、
改走別台再回到原指標的 ABA、提交前公開 `DOS.M` 改指，皆於首個
DOS 動作前拒絕，epoch／步數不增加；成功批次只交付一次，重入
owner rebind 與舊計畫 replay 被拒。主代理在唯讀 Docker／Xvfb
獨立重跑定向測試與 `go vet` 通過，既有正式 `Game.Update` 分裂目標
反證亦仍通過。

它提供的是**可行性原型**，不是正式 bridge 的證據：測試 owner
直接交付合成 DOS，未取得 `MouseBridge`／`KeyboardBridge` 的共同
目標唯讀身分，也不能阻止其他程式繞過 owner 改公開 `DOS.M`；
`readFrameInput` 的完整提交矩陣及故障 Close 亦未通過。獨立
READY 審查前，不得將此原型搬入 production 或宣稱已修復同批
部分副作用。

## 2026-09-24：提交區間改指反例的訂正

[Issue #18 獨立反例](../re/issue-18-session-turn-ready-candidate-review.md)
證實前節合成 owner 的提交起點指標／generation 核對不足：
其自身 rebind 即使被鎖住，外部仍可在首筆 action 前直接改公開
`DOS.M`，使滑鼠與 BIOS 鍵分送不同 machine，owner 卻增加 epoch。
因此 READY 候選必須把**整個提交區間**的目標獨占、兩座正式橋
實際輸出身分、完整純預檢後不可失敗的已定序動作，以及失敗前
DOS 副作用零新增列為同一契約；不能把一次檢查稱為原子提交。
此為原型反證，非原版玩家路徑收據；本規格維持 DRAFT。

後續[Issue #18 同指標 callback 反例](../re/issue-18-session-turn-ready-candidate-review.md)
把前項阻塞具體化：`DOS.MoveMouse`／`PressMouse` 的 handler callback
會再讀公開 `DOS.M`，因此同一 `*DOS` 指標也能在提交中把 move
callback 留在舊 machine、press callback 與 BIOS key 送進新 machine。
每筆 action 前核對雖能晚拒，拒絕時卻已留下滑鼠／callback 副作用。
READY 候選必須指定可強制的 session 專有 DOS／machine 目標，
消除提交期間外部改指／直接 bridge mutator 的路徑，再做整批
純預檢與不可失敗的提交；不能只以同指標或逐 action 檢查替代。
這仍是可丟棄合成反例，未修改正式前端，規格維持 **DRAFT**。

後續[私有目標 session 原型](../re/issue-18-session-turn-ready-candidate-review.md)
顯示一條較窄的可行路線：新 session 工廠自行建立並私有持有
DOS／machine、panel 與兩橋；公開輸入入口不得接受或洩漏原始
指標、bridge mutator。如此不必為本遊戲全域修改公開的 `DOS.M`，
但既有容許任意兩橋的 `Game.New(Config)` 不能因而宣稱原子性。
原型只驗合成 canvas Down＋Enter，正式入口還需覆蓋完整路由、
純預檢後不會普通拒絕的排他提交、滑鼠狀態版本及故障關閉。
這是 **DRAFT 的限縮 READY 候選**，不是正式 API 授權或驗收。

後續[完整路由與收據複審](../re/issue-18-session-turn-ready-candidate-review.md#完整路由矩陣與推進故障鎖存複審2026-09-24)
補上五類合法輸入批次的反例：純計畫接受，但目前私有 session
原型全部拒絕。推進原型另已修正故障後重試遺失 `OriginalFault`／
原始 error 的缺口，Docker 複審通過；這不會自動封閉正式橋接器的
提交期間排他、完整 `pressedEpoch`、`Draw` 通報與 Close。
因此本規格仍是 DRAFT／限縮 READY 候選，不授權將原型接入 production。

## 2026-09-24 獨立審查定案：封閉 session owner 限縮 READY

本次審查的問題不是「既有 `Game.Update` 是否已原子」，答案仍是否；而是下列
**新建、封閉 owner** 是否已有足夠、無歧義的實作契約。結論是**有**。此前列出的
目標別名、ABA、pressed epoch、同批順序、Draw error 與 Close 問題均已有明確的
失敗即關閉處置，不再是會改變此新 API 語意的未知。尚未把 API 寫進 production
是 implementation gate，不是將規格留在 DRAFT 的理由。

### READY 授權的唯一所有權邊界

production 必須新建一個 session factory／owner；它在同一 goroutine 內自行建立並
私有持有 machine、DOS、panel、mouse bridge、keyboard bridge、layout、route state、
source generation、epoch、phase、第一個 fault 與可關閉資源。它不得接受、回傳或
暴露可改指的 machine／DOS／panel／bridge mutator，也不得把既有 `Game.Config` 的
可注入 bridge 當成此 owner 的內部實作。所有 Input／Advance／observer-frame／
Snapshot／`ReportDrawFault`／Close 必須走這一個 owner。

每一回合依本檔既有 CapturedUpdate → 純 Prepare → 排他 Commit → Advance →
Snapshot 順序處理。Prepare 只能讀完整 `MouseBridge.Snapshot()`、panel、layout、
phase 與 owner generation 的值，並預先確定所有 host 轉移、DOS action、鍵盤
transport、無動作及 pause；不得呼叫會寫 DOS 或 host 的 Route／Handle／ApplyLayout／
DeliverBIOSKey。Commit 在第一筆 DOS action 前核對同一封閉來源 generation 與完整
RouteBase，期間禁止重入與 rebind；它只可執行已預檢且不再有 ordinary route error
的動作。若底層無法提供這個「提交後不再普通失敗」保證，必須在第一個輸出前轉
`Failed`，不得以逐 action 晚拒或回滾幻想替代。

`Epoch`、budget、實際 step 差分、raw stop、錯誤優先序與 Draw/Close 的行為均以
〈epoch、預算與停止收據〉及〈Draw 故障通知與關閉 owner〉為 READY 的一部分。
具體而言，可檢查 Draw fault 必須在同 goroutine 直接呼叫
`ReportDrawFault(error)`；不是等下一個 `Update` 才讓 owner 知道。首次 fault 鎖存
根因、轉 `Failed` 並 Close 一次；後續輸入、Advance、Draw report 或 Close 都不得
復活 session、增加 step 或再關閉資源。

### 獨立證據與失敗矩陣

審查在本機 dosgolem fork `b9082262542fc538f34a7932acd3a2d4b4ce3b6c`、
Go 1.26.7／Ebitengine 2.9.9、有界無網路 Docker／Xvfb 中，以唯讀 fork 重跑：
`TestDraftPrivateBatchAcceptedRouteMatrix`、
`TestDraftPrivateBatchV2SnapshotRejectsPressedEpochDriftBeforeCommit`、
`TestDraftPrivateBatchV2SnapshotEqualsPlanAcrossCrossEpochRelease`、
`TestDraftSealedSessionRouteMatrixCoverageGap`、
`TestDraftSealedSessionRejectsTargetOrLayoutDriftBeforeCommit`、
`TestDraftOwnedCommitDrawSessionBoundary` 及現行無動作矩陣；相關
`-race` 與 `go vet ./frontend/ebiten ./host ./presentation` 均通過。
測試全為 ignored 合成 machine／DOS，未載原版、手冊、字型或存態。

| 失敗／邊界類別 | READY 行為 | 證據 |
| --- | --- | --- |
| 末端非法 host route、stale layout／target、pressed epoch 漂移、舊 plan | 首筆 DOS action 前拒絕；mouse／callback／BIOS／step／epoch 無新增 | `route_private_batch_v2_draft_test.go`、`route_sealed_matrix_gap_draft_test.go` |
| Down＋Up、多鍵、跨 epoch Up、focus loss、host capture、Open／Apply／Cancel＋Enter | 純 plan 與完整 bridge snapshot 一致；保留已定案的 host 消費與非命中無動作政策 | `route_private_batch_v2_draft_test.go`、`route_noop_matrix_draft_test.go` |
| 公開目標改指、bridge target 分裂、提交期重入 | 既有反例證明公開 API 不足；新 owner 必須不外洩目標並排他提交，否則 fail-closed | `route_commit_target_alias_draft_test.go`、`route_commit_owner_draft_test.go` |
| 可檢查 Draw snapshot fault | 同步鎖存、Close 恰一次；後續 submit／Advance 零步且拒絕 | `session_owned_commit_draw_draft_test.go` |

以上不是 production CONFORMED 收據：原型的 Close 計數不等於真實資源關閉，
`Game.Draw` 也尚未呼叫正式 `ReportDrawFault`。production 實作後必須以真實封閉
owner 重跑本矩陣、驗真正 Close error 保存與同 goroutine Draw relay；再另依規格
004 完成 cold boot、正常玩家路徑、存讀檔與原版同狀態，才可主張任何 CONFORMED。
若實作發現現有 bridge 無法封存目標或在 Commit 後仍會回普通錯誤，該發現是新的
規格反例：停止實作、把本限縮契約退回 DRAFT，先補可強制的封閉 primitive；不得
在 production 中猜補。

## 2026-09-24 後續獨立審查：封閉前端的值型 View 限縮 READY

本節**只授權輸入擷取用的值型 View 與來源版本核對**，不授權畫面
`Snapshot(scale)`、原版冷開機或可玩的 Linux 啟動器。審查當時正式
`session.Owner` 只有 `Status`，`CapturedUpdate` 尚無來源版本；現行
`frontend/ebiten.Game.Config` 仍可注入彼此獨立的 panel／bridge／snapshot／
advance，不能冒充封閉前端。本機 dosgolem fork `337ac83` 的 tagged
`session/owner_view_draft_test.go` 用合成 owner 試驗 2×→3×→2×、
Apply／Cancel、初始零 layout、故障單次 Close、版本溢位與不可變欄位。
主代理在 Go 1.26.7／Ebitengine 2.9.9 的無網路 Docker／Xvfb 以唯讀
fork 獨立重跑該 tag 的 `go test ./session`、`go vet ./session` 與
不帶 tag 的正式 `go test ./session` 均通過。收據另涵蓋 Running-only、
非正規 layout、故障後不重讀、Panel／Layout／session Epoch 全同而
來源版本不同的 ABA 舊 token、純 Prepare／owner 失敗收束、
執行中／Stopped 的版本變化，以及測試模型中首筆 DOS 動作前的
版本溢位拒絕。獨立複核在補齊真正同值 ABA 與 owner 編排器負例後，
未再指出會改變此**子契約**的 READY 前缺口。這些仍是**合成證據**；
正式 owner／真實 DOS、原版冷開機、畫面與玩家路徑尚未驗收。

typed API 的必要資訊如下；名稱可依 Go 慣例微調，不得刪去欄位、
放入可變底層目標，或把作用層像素快照混入：

```go
type View struct {
    Phase Phase
    Panel host.PanelState
    Layout host.MouseLayout
    Epoch uint64
    SourceGeneration uint64
}
func (o *Owner) View() (View, error)
// CapturedUpdate 另加 SourceGeneration uint64；StartedPanel 與 Layout
// 必須由同一份 View 擷取，不可各讀一次再拼接。
```

- `View` 只在 `Running` 且私有 layout 已按目前 panel 正規化後交付。
  `Booting`、`Stopped`、`Failed`、`Closed` 回零值 View 與錯誤；終態
  只由既有 `Status` 讀首錯與 Close error，最後畫面的玩家政策留在
  規格 004。`Running` 缺 layout、非正規 layout、`Panel.Snapshot`
  失敗時也回**零值 View 與錯誤**，由 owner 同步鎖存第一個 fault、
  轉 `Failed` 並 Close 一次；不得回傳半份或 stale View，故障後
  再次呼叫 View 不得重讀 panel。
- `SourceGeneration` 是**路由來源版本**，不是畫面影格或手冊作用層
  generation。成功進入 `Running`、接納 `Deliver`、消費暫停或執行中
  `Advance`（包括轉 `Stopped`）時各遞增一次；版本必須覆蓋 panel、
  mouse、layout、phase、pending 的所有成功變更。可能變更 DOS 輸入或
  machine 前先預檢溢位，不得回繞；終態由 phase 使舊 token 失效。
  審查當時正式 owner 只在 `Deliver` 增版本，當時尚未符合本節。
- `CapturedUpdate.SourceGeneration`、`StartedPanel`、`Layout` 均須來自
  同一份 View。Prepare 純讀核對版本與完整值，無副作用；若版本
  過期、同值 ABA 或任一值漂移，封閉 owner 在首筆 DOS action 前
  轉 `Failed`、Close 一次，DOS 動作與 session Epoch 均不增加。

production 驗收須由正式封閉 owner 重跑合法批次跨 Open／Apply／Cancel
的 View↔Prepare 一致性、同值 ABA、面板快照／版面故障、版本溢位、
啟動與各種 `Advance` 的版本遷移，以及失敗後零新步和 Close error
保存。畫面 `Snapshot(scale)` 另需獨立緩衝、frame 身分及多作用層
來源的 READY 證據；不得用本節 View 測試代替。

### 2026-09-24 限縮正式接線紀錄

本機 dosgolem fork `a7cb0eb` 已把本節 `View`、
`CapturedUpdate.SourceGeneration` 與全批次版本／版面核對接進正式
`session.Owner`。正式回歸涵蓋鍵盤、面板與失焦批次的 stale／zero
layout 拒絕、先由真實 View 擷取再經 `Advance` 形成的同值 ABA、
Running 缺版面、面板讀取故障、版本溢位、首錯與單次 Close。
獨立 reviewer 複審未再發現此限縮切片的確定失敗即關閉漏洞；主代理
在無網路 Docker／Xvfb 獨立重跑 `session`、`host`、`frontend/ebiten`
測試、tagged DRAFT 測試、session 競態測試與 vet，均通過。

本段只記**限縮實作已接線**，不把整份規格升為 CONFORMED。畫面
`Snapshot(scale)`、真實原版冷開機、Watcher 等價、封閉玩家視窗與
正常玩家路徑仍各需自己的證據與驗收。

### 2026-09-24 後續 DRAFT 缺口：觀測器與畫面快照

通用 `Machine.RunUntilObserved` 候選接縫只能指出每次嘗試 Step 前的
位置；原版手冊 checkpoint 的 paired-oracle 原型及合成反例已顯示，
Oracle 另有初始條件／中斷點、未遮蔽 A0000 守衛、`OnCall` 動態 hook、
stub 與退出／HALT 次序。現有正式 `Watcher.Install` 僅接受
`*oracle.Oracle`，封閉 `session.Owner` 尚無對應的安全安裝入口。
因此不得把通用接縫或裸 `Machine.RunUntil` 接成正式 Buck Rogers
observer-aware `Advance`，也不得以合成測試替代原版同狀態收據。

畫面 `Snapshot(scale)` 亦保持 DRAFT。雖可重用正式的單幀 indexed
來源、封閉有序作用層及手冊雙層票券元件，`session.Owner` 尚未私有
持有來源 frame 身分、active group 清冊與字型登錄，亦未固定
`Advance → observer／Layer.Frame → 封存 → Snapshot` 的順序。
下一輪最小負例須同時驗證 2×／3× 切換舊票失效、背景→正文缺層／
錯序、Clear／Restore／新 Frame 後失效、同名異字模與缺字、來源
影格錯誤、回傳緩衝區獨立，以及首次錯誤回零值並同步 Failed／
Close 一次；輸入 `SourceGeneration` 不得充當影格身分。

後續本機 fork `670b126` 的 `draft_session_snapshot` 合成測試，
以已提交的 session 與 presentation 元件建立**可丟棄候選模型**。
獨立審查先抓到「Snapshot 時才封 layer／font」及「票券未綁
實際 Owner」兩個假通過；修正後 `prepare` 凍結 indexed／palette、
背景與正文、字型，票券另綁實際 owner、獨立 frameID 與輸入世代。
同票 caller 來源漂移仍投影原封存內容；私有畫格／字型竄改、
另一個同值 owner、2×→3×→2× 舊票、新 Frame、來源與群組故障
均回零快照並使候選 owner Failed／Close 一次。主代理的 Docker
session、競態與 vet，以及 reviewer 的獨立 tagged session 測試通過。
此測試依賴同套件私有欄位與測試 helper，畫布只有合成 2×1；
倍率往返各有新票，不是同一票跨倍率。它**未**觸發正式
`Layer.Frame`、Clear／Restore 或原版觀測器，故僅縮小 DRAFT
契約缺口，不授權正式 `Owner.Snapshot` 或升 READY。

### 2026-09-24 後續 DRAFT：既有 Oracle 回圈與 Owner 的觀測順序

本機 fork 的 tagged `draft_session_oracle_loop` 合成測試以**測試專用**
反射／`unsafe`，讓一個 Oracle 暫時別名同一個 `Owner` 私有的 machine／DOS；
正式 API、`Owner.Advance` 與遊戲檔均未改。獨立審查及 Docker 定向測試確認：
現行 `Oracle.RunUntil` 依序檢查回合條件、DOS exit、HLT、未遮蔽的
`A0000` 禁區，然後執行 `OnCall`、stub 與 `Step`。合成 `RETF 0Ch`
可使正式 `buckrogers.Watcher.Install` 動態註冊 return hook，收到一筆
`post-call`；這只證現有 hook 機制能在同一組私有資源上觸發，不證真實
手冊題目的完整生命週期。

停止值不能直接沿用：`Steps(2)` 配 `Budget(2)` 已走兩步但回
`*oracle.BudgetError`；配 `Budget(3)` 則在下一輪條件檢查回 `nil`、
仍只走兩步。Oracle 零預算回預算錯誤、零步；正式 Owner 的零預算
則是前端錯誤並失敗即關閉。既有 `Owner.Advance` 仍呼叫裸
`machine.RunUntil(nil,budget)`，不觸發 Watcher。合成測試也只量起點
已有 exit／HLT、條件為 false 的情形；中途終止、同時成立的優先序、
具體錯誤類別與 session `TickReceipt` 映射尚未驗。不得把測試中的
`unsafe` 別名搬入正式程式，或據此將 observer-aware Advance 升 READY。

下一個限縮審查須固定：不暴露 machine／DOS 的正式接線方式、
每回合 budget 與 Oracle 停止值／錯誤的 typed 映射、動態 hook 安裝
在第一步前、退出／HLT／守衛與 stub 的負例，以及原版手冊 checkpoint
的同狀態收據；規格確定後才可修改正式 `Advance`。

### 2026-09-24 追加 DRAFT：Oracle 停止收據矩陣與封閉接線候選

本機 fork `b2580a7` 的自包含 tagged 合成測試
`session/owner_oracle_receipt_matrix_draft_test.go`，SHA-256
`cc70d02a86cd39bd0634c2576436590d705c7917c5215031afdc7218df8d9d31`，
由主代理在唯讀、無網路、有界 Docker 獨立重跑測試與 `go vet` 通過。
它只用測試專用反射／`unsafe` 把 Oracle 暫時連到同一組 Owner 私有
machine／DOS；沒有修改正式 `Owner.Advance`，沒有載入原版或字型。
測試裡的合成位址不構成新的原版定位證據。

已證實的現行 Oracle 行為：`Steps(2)` 配 `Budget(2)` 走兩步仍回
`BudgetError`，配 `Budget(3)` 才在下一輪起點回 nil；DOS exit、HLT
及跳入 `A0000` 若恰在最後允許的一步發生，會先呈現預算錯誤，
多一個預算槽才分別呈現終止或守衛錯誤。原始 Step 錯誤仍優先返回；
Oracle 只回 error，沒有 `machine.Stop`，不可據此填造 `TickReceipt.RawStop`。
從 `Machine.Steps=1` 給 `Budget(^uint64(0))` 時，現行 deadline 加法
回繞，零步即回 `BudgetError`；正式封閉 runner 須在提交前拒絕溢位
或訂出可驗證的安全上限。正式 Buck `Watcher` 在合成 `RETF 0Ch`
仍可動態取得 return hook。先前懷疑 stub 跳過 `Step` 可能不計步；
新測試證實 `fireStub` 本身計步，同位址重入三次為三步，故撤回該疑慮。

**2026-09-24 勘誤（限 Oracle 預算加法）**：上一段的 deadline 回繞是
`b2580a7` 當時的真實觀測，保留作成因證據；本機 fork `7444caf` 已在
`Oracle.RunUntil` 執行任何條件／指令前拒絕 `Steps+Budget` 溢位，
回傳明確的非 `BudgetError`，並新增通用單元測試及更新同一 tagged
DRAFT 矩陣。這修正只避免把零步誤報成「預算耗盡」，**不**改
`Steps(n)` 的末步判讀、`Owner.Advance`、typed `TickReceipt` 或
原版觀測器接線；後者仍須獨立 READY 審查。

獨立唯讀 API 審查提出**強推論候選**：通用層提供只讀呼叫視圖
`Regs`／`Caller`／`Arg`／`Byte`／複本 `Bytes`／`Steps`，以及限定作用期
的動態 `OnCall` 註冊；遊戲專屬 watcher 提供位址與 hook 清冊，
session 在第一步前私有安裝，不向 frontend 或回呼外洩
`*Oracle`／`*Machine`／`*DOS`。此候選尚未有完整正式 hook 清冊、
觀測錯誤傳播、frame／A000 pre-write 多路分派、原版冷開機或
`TickReceipt` 映射證據；**仍為 DRAFT，不授權實作**。下一次審查
應先以同一合法原版 checkpoint 比對首個與末個手冊事件、停點與
machine／DOS 狀態，再固定 typed 停止原因及第一步前安裝的負例。

### 2026-09-24 DRAFT：私有 Owner 與獨立原版 checkpoint 的手冊事件配對

本機 fork `2c96d19` 的自包含、單一 build tag 測試
`session/manual_checkpoint_owner_pair_draft_test.go` 從同一合法私有
checkpoint 分別還原 `Owner` 私有 machine／DOS 及另一組 machine／DOS，
在兩邊的第一步前安裝正式手冊 `Watcher`，並以相同步數上限續行。
獨立 Docker 重跑量到 begin／clear／request 各 1 筆，事件摘要、
終點步數、CPU／記憶體／indexed 畫格／palette 摘要與 DOS
`Exited`／`ExitCode` 相同。原版 `GAME.OVR` 與 checkpoint 的固定
SHA-256 都先核對；缺本機輸入時測試跳過，不把私有檔納入版控。

這只證明**此 checkpoint 的有限窗口**可在測試專用 Oracle 別名下
重現相同可見手冊事件；測試沒有經過正式 `Owner.Advance`，也沒
比較完整 DOS 檔案操作／BIOS／IRQ 狀態、冷開機或 Linux 玩家輸入。
先前待補的「合法原版手冊事件局部配對」因此有了 DRAFT 收據，
但 observer-aware runner 的來源封閉、停止收據、完整 hook 清冊與
作用層快照仍未 READY，規格 019 及 Issue #18 不因此完成。

### 2026-09-24 獨立審查追加：observer runner 限縮 READY 候選（仍為 DRAFT）

本節只提出使 `session.Owner.Advance` 能消費既有 Buck Rogers
`Watcher` 的最小候選，不授權實作或把本規格升為 READY。現行
`Owner.Advance` 明確是無 observer 的 `Machine.RunUntil(nil, budget)`
切片；它不會觸發 `oracle.OnCall`。反之，現行 `Oracle.RunUntil` 每次
嘗試 Step 前固定依序判定 condition、DOS exit、HLT、未遮蔽 A0000
守衛、`OnCall` hooks、stub，最後才 Step；手冊 `Watcher.Install` 又會在
dispatcher entry 動態安裝 guarded post-call hook。因此不得以裸
`Machine.RunUntil`、通用「每步 callback」或測試用 Oracle 別名替代該
執行順序。

獨立審查發現兩個不能跳過的介面衝突：現行 `Watcher.Install(*Oracle)`
與 `OnCall(func(*Oracle))` 會把 runner 資源交給 Buck 回呼；現行
`Oracle.RunUntil` 的 `BudgetError` 與 `ExitError` 也可能是正常停止，
不能把所有非 nil error 都歸類為故障。候選正式邊界須由 Owner 私有：
在第一個 instruction 前，以限時、唯讀呼叫視圖和 hook 註冊能力
安裝 Buck watcher；frontend、adapter 與 watcher 回呼均不得持有可重綁
的 `*oracle.Oracle`、`*machine.Machine` 或 `*dos.DOS`。通用逐步核心應
保留 Oracle 已量到的順序，再提供固定預算切片的 typed 停止結果；
正常預算耗盡、DOS 結束和條件達成先與觀測／原版故障分流。各類
`TickReceipt` 映射必須先逐例量測，保存原始停止原因、前後 Steps
與 DOS exit；不能直接套用現有 `RunUntil` 的 error 或裸 Machine stop。

升格限縮 READY 前，審查者必須逐項確認：

1. 不使用 reflection／`unsafe`、公開 resource getter 或 caller 可注入 runner；
   private boot、install、run 與 Close 的所有權鏈可由正式 API 證明。
2. hook 清冊含手冊 dispatcher、clear 與動態 return hook；靜態
   dispatcher／clear 須在本次續行第一步前安裝，動態 return hook
   則在 dispatcher 回呼取得 returnTo 後、對應返回指令前安裝。
   callback 重入、hook／stub／Step 次序及 callback 錯誤都各有負例。
3. 正式 runner 對本切片會用到的 exit、HLT、A0000 guard、hook、Step
   與 budget 邊界以現行 `Oracle.RunUntil` 的已量順序為基準；
   condition／stub 用少量合成反例固定共用核心順序。若最後一步
   造成 DOS exit，Oracle 會先回 `BudgetError`、下一回圈才見
   `ExitError`，現行 Owner 卻在當回合後置檢查回 `ProgramStopped`；
   typed slice 應採哪一種玩家回合收據須明確決定並逐項審核，
   不得用「保留順序」掩蓋差異。正常停止與真正故障均有 typed
   mapping；不得以零值 condition 呼叫舊 API。
4. `2c96d19` 的合法原版 checkpoint paired receipt 改由正式 Owner 路徑重跑：
   同一原版／checkpoint hash、第一步前安裝、相同 budget，且 begin／clear／
   request 順序、終點 steps、CPU／memory／indexed／palette 摘要與 DOS exit
   均與獨立 Oracle continuation 相同。原版缺席時明確 skip。
5. observer callback、hook 安裝或 runner 失敗時，不再 Step、不再送輸入，
   首次故障可稽核且第二次 Advance 為零新增步；Owner 的 Close-once
   依既有生命週期契約驗證。presentation Frame／Snapshot 各守自己的
   DRAFT 閘門，不列為此 runner 切片升格的先決條件。
6. 同一原版 checkpoint 的無 watcher A/B 仍相同；有 watcher 時差異僅為
   核准的值型 observation，不得改變 DOS input、記憶體、返回值或
   已量的 DOS 終點。完整檔案／存檔、畫面 Snapshot／2×／3× 與正常玩家
   路徑另依既有 DRAFT 閘門驗收，不能用此小窗收據取代。

現有 `session/manual_checkpoint_owner_pair_draft_test.go`（commit `2c96d19`）
只完成第 4 項的 DRAFT 對照前半：它以測試專用反射／`unsafe` 建立 Oracle
別名，未經 `Owner.Advance`，亦未驗證上述正式所有權、停止收據與失敗收束。
它可保留為私有原版輸入的回歸探針，不能提升為 production 接線證據。

**2026-09-25 閘門勘誤（獨立審查）**：本節上面的「升格限縮 READY 前」
六項混入了實作後才可能取得的證據，不能照字面要求正式 Owner 先存在才
准許寫正式 Owner。第 1 項的正式 API／私有所有權、第四項的正式 Owner
checkpoint 配對、第五項的 Owner Close-once 與第六項的正式原版 A/B，
均移作下文「實作後才屬 CONFORMED 的驗收」；第 2、3 項只保留其
**行為契約與可丟棄原型證據**作為 READY 前置，正式接線測試同樣留到
CONFORMED。前列六項保留為形成史，不再是現行 READY 清單。

當時的最小缺項，是一份**同時**量到受限 CallView／Registrar、
真實 Buck Watcher 動態 return hook、以及 callback error／panic 當次停止的
tagged 組合收據。下文已補上合法 checkpoint 的 runner＋Watcher 組合對拍；
callback error／panic 則沿用同一 runner 的合成 MZ 負例，並非在該原版
checkpoint 人為觸發。這足以重新審查限縮 READY，**不會自動升格**：
兩個 DRAFT prototype 仍有測試用的外部 `*Oracle` 建構器或不完整生命週期，
不得搬成正式 API；正式 Owner、Close 與完整玩家路徑仍留待實作後驗收。

### 2026-09-24 獨立可審查的 observer runner 最小方案（DRAFT）

本節只定義下一個 `session.Owner.Advance` 切片的**候選設計與審查分界**。
它不是 READY：目前證據足以限制不得使用的捷徑，卻不足以證明新的受限 callback
API 能在真實 Oracle 上同時保留 hook 次序、動態 return hook 與錯誤收束。不得以本節
修改 production。

#### READY 前已知事實、可丟棄證據與最小缺項

| 項目 | 目前分級與可回查證據 | 可作何種結論 |
| --- | --- | --- |
| Oracle 執行次序 | 已證實：`oracle/run.go:RunUntil` 逐次為 predicate → DOS exit → HLT → A0000 guard → `OnCall` → stub → `Machine.Step` | 新 runner 必須逐項保留此順序；不可用裸 `Machine.RunUntil` 或一般每步 callback 代替。 |
| Watcher 的 hook 生命週期 | 已證實：`apps/buckrogers/watcher.go` 的 `Install`／`dispatchEntry`；dispatcher／clear 是靜態 hook，dispatcher 依 caller 動態 `OnCall(returnTo, ...)` | 動態 return hook 是必要能力，且須在 callback 返回後、return instruction 被考慮前生效。 |
| 最後一步的 exit | 已證實：前節 `owner_oracle_receipt_matrix_draft_test.go`；Oracle 預算邊界可先出現，下一輪才會觀察到 exit | session receipt 必須同時保存 loop 邊界與後置 exit，不能由 `BudgetError` 字串猜類別。 |
| 現有 Owner 的終態收束 | 已證實：`session/owner.go:Advance`、`fail`、`Close`；已有限 fake 收據 | 現有 Owner 有 first-fault／Close-once 骨架，但尚未持有 observer runner。 |
| 原版 checkpoint 小窗 | DRAFT：`2c96d19` paired receipt；透過 reflection／`unsafe` 別名同一私有資源 | 可作為原版事件期望值，不能證明正式所有權或正式 `Advance`。 |
| 自包含 map runner 測試 | DRAFT toy model：`session/owner_observer_runner_ready_draft_test.go` | 僅說明擬議欄位可表達 return hook、末步 exit 與 Close-once；**不**證明 Oracle、Watcher 或 Owner 接線，不能作 READY 依據。 |
| 真實 Oracle 合成 MZ facade | DRAFT：`oracle/observer_facade_mz_draft_test.go`；1056 bytes，SHA-256 `bd0f511b26cb63a2de45bd2781d35ddd115ef8696ea31c24e78bd71fc3fa58a6` | 證明公開 `Load`／`OnCall` 可同步安裝下一 instruction 的 hook，也證明現有 callback 包裝若只 recover／鎖存，仍會多執行一個 Step；不能把它稱作既有 fail-closed。 |
| 實際 Watcher 的 checkpoint facade | DRAFT：tagged `oracle/draft_restricted_observer_facade.go` 與 `apps/buckrogers/manual_watcher_facade_oracle_draft_test.go`；透過 `LoadDraftCheckpoint`，checkpoint SHA-256 `8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269` | concrete facade 與其 `*Oracle` 私有於 `oracle` package；Buck 只持有無法命名／型別斷言回 concrete 的 restricted interface。真實 Watcher 的 `ObserveDispatchEntryWithStyle`／`ObserveInstruction` 經值型 CallView／registrar 續行，與 `Watcher.Install(*Oracle)` 同得 9 筆 observation、3 筆 presentation、相同 guarded-return／style 與終態 copied state。缺輸入時 skip。 |

前項關閉了本節原定的最小 DRAFT 缺項：現有 Watcher 已能由受限 facade 以真實 Oracle
hook dispatch 安裝 guarded return hook，且這次 callback 參數沒有洩漏 `*Oracle`。
但 tagged 原型的外層 observer 仍有測試用 `Close`／checkpoint view；Go closure 也可能
捕獲外層資源。這份 paired test **不**證明正式 Owner 的資源封閉，正式 installer 須
限制捕獲範圍並另做黑箱負例。callback error／panic 的同步中止
與末步 exit/budget 仍分別由真實 Oracle 合成 MZ 收據固定；兩組證據必須一起審查，不能
把 checkpoint 成功誤讀成 callback fault 已被現有 `OnCall` 處理。至此本節是
**DRAFT candidate，等待獨立審查**；規格 019 整體仍為 **DRAFT**，尚不授權 production。

hard counterexample 是 READY 契約的一部分：現有 `Oracle.OnCall` callback 簽名為
`func(*Oracle)`，`RunUntil` 在 `fireCallHooksAt` 後無條件走向 stub／Step。故 callback
邊界只做 `recover` 加鎖存，**必然不**能阻止當次 Step。未來 typed runner 必須同步傳遞
fault 並中止 loop；若暫以 unexported sentinel panic unwind 實作，僅 runner 邊界可辨識
並 recover 該 sentinel，其他 panic 一律轉 `ObserverFault`，不得把現有 `OnCall` 包裝
誤稱為已 fail-closed。

同日的 tagged DRAFT `oracle/draft_real_observer_runner.go` 與
`oracle/real_observer_runner_draft_test.go` 以公開 `Load` 載入 1056-byte、
SHA-256 `bd0f511b26cb63a2de45bd2781d35ddd115ef8696ea31c24e78bd71fc3fa58a6`
的合成 MZ，將受限 CallView／registrar hook 包在 Oracle package 私有 concrete runner。
它直接重現 Oracle 的 exit／HLT／A0000／hook／stub／Step 順序，且以私有 sentinel
把 callback error 或 panic 同步帶回 runner loop；測試量到當次零新 Step、後續 Run
同為零步 `ObserverFault`。同一 receipt 另固定：純 budget、末步 DOS exit（raw
`BudgetBoundary` + `AfterLastAttempt` + `ProgramStopped`）、下一 slice 的起點 exit，
以及 dispatcher@0 動態註冊 return@1。這是**真實 Oracle 的可丟棄 prototype**，不是
`Owner.Advance`、正式 Watcher 接線或 CONFORMED 收據；本節和規格 019 仍為 DRAFT。

同日 tagged 組合收據 `TestDraftRealObserverRunnerFacadePairsInstallFromLegalManualCheckpoint`
以合法 checkpoint 的 `LoadDraftRealObserverRunner` 建立上述 runner，Buck 分支只取得
restricted registrar、`Run` 與 copied terminal view，沒有 `*Oracle` 或 `Close`；它以相同
budget 對照另一台 `LoadDraftCheckpoint` + `Watcher.Install(*Oracle)` 基線。兩側均量得
9 筆 observation、3 筆 presentation、相同 begin／clear／request 順序、guard/style、
steps、CPU／memory／indexed／palette 與 DOS exit 摘要。這只證明**此有限 checkpoint**
的組合等價；`NewDraftRealObserverRunner(*Oracle)` 仍是合成 MZ probe 的 DRAFT API，
正式 Owner factory、資源 Close、完整原版路徑與 CONFORMED 驗收均未由此授權。

**2026-09-25 獨立審查：仍為 DRAFT。**上述 9／3 與事件順序是本次執行的
日誌觀測，組合測試目前只斷言兩側相等，未把預期數量與
begin→clear→request 錨點寫成斷言；兩側若同時漏事件也可能通過。
`installDraftWatcherFacade` 另是同套件的平行安裝邏輯，並未讓正式
`Watcher.Install` 經同一受限 registrar 路徑安裝，故尚不能排除日後漂移。
合成 MZ 負例驗證的是 callback error／panic 的零步停止，不是
**installer 本身**的 error／panic、首錯鎖存與零步收束。這三項是
當時限縮 READY 前的具體缺口；補證以前不得依本段修改正式 Owner。

**同日複審後仍為 DRAFT。** tagged 原型已補 9 筆 observation 的完整
kind 順序、3 筆 presentation 的 begin→clear→request、固定事件 key 與
譯文長度關聯；同一個受限 installer 同時接 runner 與 legacy Oracle，
另以 `Watcher.Install` 作獨立基線；合成 MZ 的 installer error／panic
皆回 `ObserverFault` 且零新步。主代理在唯讀掛載原版 checkpoint 的
Docker 重跑上述組合與 oracle 測試及 vet 通過。譯文更新曾使舊的
硬碼字數斷言失效，已改成對照實際 request 的字元數；這是測試
錨點更新，不是原版事件變更。

**2026-09-25 註冊生命週期補證，仍為 DRAFT。** tagged runner 已移除
對外嵌入的 registrar，`Install` 限首次、首次 `Run` 前；installer 與
callback 取得的 scoped registrar 在同步呼叫返回時失效。合成 MZ
負例已拒絕重複／延後安裝、被捕獲的 installer／callback registrar、
callback 內忽略 nil hook 錯誤及 `Run` 重入；首錯優先於後續 panic／
invalid budget，拒絕時零新步且無新增 hook 回呼。當次 callback 的動態
return hook 仍在下一候選 instruction 前生效，合法首題 checkpoint
的 9 筆 observation／3 筆 presentation 對照仍通過。這些只是本機
ignored fork 的 tagged 試驗，非正式 `Owner.Advance`。

獨立複審另指出**尚未封閉的 READY 前缺口**：scoped registrar 只有
`active` 布林，callback 若將它傳給其他 goroutine，該 goroutine 可在
callback 尚未返回時競爭註冊，違反下文「同 goroutine 註冊」契約；
`DraftRestrictedCallView` 亦持有可於 callback 期外查詢的 Oracle 視圖，
尚非真正凍結的值快照。因此上述負例通過仍不得升 READY。下一個
可丟棄候選應讓 callback 只回傳受限的 hook 增量值，由 runner 在
callback 成功返回後、stub／Step 前同步驗證與安裝；靜態 hook 在
首次 Run 前一次性提交，呼叫視圖按次凍結為值。需以跨 goroutine
捕獲、錯誤／panic 丟棄增量、動態 return 可見性及原版 checkpoint
重播再審，不能將現有 scoped registrar 直接搬入 production。

**2026-09-25 Delta 觀測器原型複審，仍為 DRAFT。** 本機 ignored fork 的
`oracle/draft_real_observer_runner.go` 新增第二個、僅 tagged 測試可見的
`DraftDeltaObserverRunner`：首次 `Run` 前一次性提交靜態 hook 清冊，
callback 只取得已凍結的 `CallView` 並回傳至多一筆 `DraftHookDelta`，
不取得 registrar；runner 僅在 callback 成功返回後、stub／Step 前
驗證及同步安裝動態 return hook。凍結視圖複製原版實測所需的傳統
記憶體（`<A0000`）、暫存器、caller 與步數；`Bytes` 再傳回複本，
超出此範圍的讀取轉 `ObserverFault`。caller 從同一份記憶體複本解碼，
不額外觸發 `WatchReadsAt`；此證據只涵蓋 Buck 首題路徑，不等於
通用 Oracle 視圖語意已完成。

可回查的本機測試入口是 `oracle/real_observer_runner_draft_test.go`、
`oracle/draft_delta_internal_test.go` 與
`apps/buckrogers/manual_watcher_facade_oracle_draft_test.go`。合成 MZ
驗證已捕獲視圖仍為舊值、靜態清冊複製、動態 hook 次步可見；callback
error／panic、非法空增量、nil hook、越界讀取均在當次零新步收束，
panic 收據包含 hook 位址與步數。package 內部負例更直接核對：
callback **同時**回傳非空增量與 error 時，動態 hook 清冊未增加、
machine 零步。合法原版首題 checkpoint 與獨立 `Watcher.Install` 基線
仍配對得到 9 筆 observation、3 筆 presentation 及相同有限終態。
定向測試、競態測試與 `go vet` 已在 Docker 通過；競態測試只覆蓋
單 goroutine 正常路徑，**不**證明跨 goroutine 捕獲安全。

獨立複審確認此切片封閉前述「scoped registrar 逸出」與可變視圖問題，
但 hook closure 仍可能捕獲 runner 並由其他 goroutine 呼叫 `Run`／
`Install`；目前 `running`、`fault` 與 machine steps 沒有跨 goroutine
排他保護。正式 Owner 的私有 boot、Close 與 observer-aware `Advance`
也未接線。故不得因 Delta 原型與首題配對通過就把觀測器升 READY，
更不得搬入 production 或宣稱 Linux 可玩版完成。

**2026-09-25 並行逸出重現，仍為 DRAFT。** 被忽略的
`oracle/draft_delta_concurrent_probe_test.go` 以 callback 捕獲 runner、
從另一 goroutine 同時呼叫 `Run`；競態偵測器實際指出
`draft_real_observer_runner.go` 讀取 machine steps 與
`internal/machine/machine.go` 寫入 steps 並行，證實上段風險，
而非僅推測。另有 test-local、非 production 的 atomic CAS gate
`oracle/draft_delta_gate_probe_test.go`，把 `Run`／`Install`／
callback 重入競爭都收束為零新步的鎖存 fault；主代理於 Docker
以 `go test -race -tags 'draft_manual_checkpoint draft_gate_probe' ./oracle -run '^TestDraftGate' -count=1`
重跑通過。這只證明一個受限排他候選可行，不證明正式 Owner、
冷開機、Close 或 Linux 玩家 session 已安全；正式接線前仍須
獨立審查排他範圍及正常原版路徑。

#### 候選 READY 契約（待上述最小缺項關閉後再審查）

正式實作時，Owner 的私有 boot 在第一個 instruction 前建立 runner；Owner 唯一持有
runner、machine、DOS、watcher、hook 清冊與 closer。factory 不接受也不回傳既有的
`*machine.Machine`、`*dos.DOS`、`*oracle.Oracle` 或可注入 `Run` callback。

現行候選改為：Watcher installer 在第一步前一次性提交靜態 hook 清冊，
callback 只取得凍結的值型 `CallView`（regs、caller、arg、byte、複本 bytes、steps）
並回傳受限 hook 增量，不取得 registrar、資源 getter、DOS 寫入、runner 替換或
Close 能力。runner 成功接收增量後、下一候選 instruction 前同步安裝 return hook；
callback error／panic 必須丟棄同次增量並停止當次 Step。Owner／runner 必須封閉
跨 goroutine 逸出與並行呼叫，再能進入 READY 審查。

每次 runner slice 必須回傳值型 receipt：budget、machine 前後 steps、差分、
`LoopStop`、`ExitTiming` 及 cause。正常 exit 不能用 error 表示。優先序固定為：

1. installer／hook fault 優先為 `ObserverFault`；HLT、guard、stub、Step fault 為
   `OriginalFault`；首次 fault 鎖存後不再 Step。
2. 無 cause 的起點 exit 或末步後 exit 都是 `ProgramStopped`；末步 exit 保留
   `LoopStop=BudgetBoundary` 與 `ExitTiming=AfterLastAttempt`。
3. 僅未 exit、無 cause、差分等於 budget 的 budget boundary 是
   `BudgetExhausted`；零 budget、加法 overflow 與未知組合在首步前
   `FrontendFault`。

callback panic 的技術政策在此明定為**失敗即關閉（fail-closed）**：runner 在 installer
與每一個 hook callback 的直接邊界 `recover`，把 panic value 與受限的呼叫位址／steps
包成 `ObserverFault`，鎖存 first fault 並 Close 一次；不得讓 panic 穿出 Ebitengine
goroutine，也不得繼續 Step。`recover` 範圍不得包住 Owner 或 DOS 的其餘程式，以免把
非 observer bug 誤報為 callback fault。此政策仍需由上述真實 Oracle facade 原型驗證。

#### 實作後才屬 CONFORMED 的驗收

以下均是 READY 之後的 implementation／CONFORMED 驗收，**不**是 READY 前置：

1. 正式 runner 以受限 facade 接通 `Watcher.Install`，正式 Owner 私有 boot 安裝它，
   `Owner.Advance` 不再使用裸 `Machine.RunUntil`。
2. 正式黑箱測試證明 frontend／adapter 取不到可變 Oracle／machine／DOS，並重跑真實
   dispatcher→guarded return、nested／guard-drop、callback error 與 panic 收束。
3. 正式 Owner receipt 矩陣覆蓋起點 exit、末步 exit、純 budget、predicate、breakpoint、
   HLT、A0000、Step fault、hook fault、zero／overflow；每一 fault 都驗 Close 一次、
   first fault 和 close error 保存、後續 `Deliver`／`Advance` 零新步。
4. 最後以正式 Owner runner 重跑合法 Buck checkpoint paired oracle：相同 hash、第一步前
   安裝與 budget 下，比對 begin／clear／request 順序、steps、CPU／memory／indexed／palette
   摘要及 DOS exit；無 watcher A/B 不得改 DOS 狀態。原版輸入缺席時必須明確 skip。

任何 production 驗收反例都使該實作回到 DRAFT；不得以 toy model、裸 Oracle、
reflection／`unsafe`、外洩 getter 或 error 字串解析補過。

#### 2026-09-25 Delta gate 首次實作與獨立競態複審（仍 DRAFT）

本機 ignored tagged runner 已把 `Run`／`Install` 的 test-local
原子排他候選搬到 DRAFT runner，主代理再把
`DraftCheckpointView` 納入同一排他。合成 callback 內的跨
goroutine `Run`／`Install`／view 讀取、同 goroutine 重入與
首次 fault 負例，在無網路 Docker 的 `-race`／vet 通過；
合法 Buck 首題 checkpoint 與 `Watcher.Install` 基線仍為
9 筆 observation、3 筆 presentation。這只證特定排程，
不表示 READY。

獨立唯讀複審另指出兩個未封閉 P0：競爭可落在最後一次
fault 檢查與 stub／`Machine.Step` 之間，故仍可能多一步或
在末步回成功收據；inner `real.fault` 與 outer atomic fault
各自鎖存，較晚競爭可能遮蔽較早 callback／installer fault。
另有 P1：view 複製中途的新 fault 仍可能交出非空結果，
並行拒絕收據沒有可信的 StepsBefore／After。正式接線前須
定義並測到 Step／receipt 線性化點及單一首錯順序，補對抗性
交錯負例；callback 內先等待 contender 的舊測試不足。
因此此 tagged Delta runner、規格 019 的觀測器子分支及
Issue #18 均保持未完成，不能進 production Owner。

#### 2026-09-25 Delta gate 對抗性修正複審（仍 DRAFT）

上段 P0／P1 是**首次候選的歷史發現**，不是目前 tagged
草案的未修狀態。被忽略的 dosgolem fork 已將 `fireStub` 與
非 stub 的 `Machine.Step` 納入同一個已授權 attempt；提交前
競爭會使該步零前進，提交後競爭立即鎖存 fault，至多完成
這個已授權 attempt，第二步前停止。同步 stub 回呼重入
`Run`／`Install`／view 不再等候自身返回。view 複製後再次
檢查 fault；並行拒絕收據不假裝知道仍由另一執行緒掌握的
step 數。首錯唯一排序點定為 atomic fault pointer 的 CAS；
gate CAS 只決定步進許可，不決定哪個錯誤先取得 `Cause`。

定向測試固定了提交前／提交後、兩步預算、同步 stub 重入、
callback 與競爭故障雙向排序，以及「gate 已關但競爭者
尚未鎖錯」的交錯；無網路 Docker 的 `-race` 與合法 Buck
首題 checkpoint 的 9 筆 observation／3 筆 presentation
配對均通過，獨立唯讀複審於**此限定範圍**未見新 P0。
這些仍是 build-tag 隔離的 DRAFT 實驗，未含正式 Owner 的
boot／Close／Advance、Linux 冷開機玩家視窗或完整輸入
生命週期，不得升 READY／CONFORMED，也不得關閉 Issue #18。
