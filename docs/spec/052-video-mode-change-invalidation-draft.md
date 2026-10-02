# 052 — 視訊模式設定時覆繪層整層失效

狀態：**DRAFT**（2026-10-02，待獨立審查）。
日期：2026-10-02
Issue：#22
前置：規格 026（儲存詢問離頁交接，契約第 5 條提出此缺口）、040（多語通道）、dosgolem `session` 的 `AudioObserver` 先例。
證據：盤點報告（2026-10-02，只讀，dosgolem `e992599`；行號皆為該 commit）。盤點代理無法寫檔，報告正文只在對話中，本規格把後續實作需要的結論全部寫在 §2、§3。

## 1. 為什麼要做

`int 10h AH=00` 經 `internal/dos/bios.go:21` 呼叫 `Machine.SetVideoMode`（`internal/machine/bda.go:68-86`）：寫 BDA、追加 `ModeChange{Mode, Step}`、平面模式（0x0D 至 0x12）呼叫 `VGA.resetMode` 清四個平面（不經 `Write8`），其餘模式只更新時序暫存器。
`machine.ObserveVideoWrites` 的 callback 在 `Write8` 內（`machine.go:660-663`），所以模式設定完全不可見。
依 A000 預寫失效的覆繪家族，以及靠指令鉤或事件鉤的家族，在這個時點都沒有入口得知「顯示已不連續」，可能留下殘字。
Buck 實際路徑只在冷啟動（step 7,520,426）與離開時設模式；目前已驗路徑不觸發，所以列為低優先，但缺口是通用層的。

## 2. 證據（已證實，除非標明）

- `SetVideoMode` 的生產呼叫端只有 `internal/dos/bios.go:21`；`AL` bit 7（不清畫面旗標）被 `& 0x7F` 丟掉（`bios.go:20`，不在本規格範圍）。
- mode 13h 與文字模式 3 不清 `Mem[0xA0000..]`（`bda.go:75-84`）。所以 #22 對 mode 13h 不是「記憶體被清了卻觀察不到」，而是**模式切換是顯示不連續點**，覆繪層沒有入口。覆繪層對任何模式事件都整層失效，與是否清了平面無關。
- `state.Load`（`state.go:218`）與 `Snapshot.Restore`（`snapshot.go:183`）直接倒回 VGA 與 `planarOn`，不經 `SetVideoMode`，是同一種洞但不在本規格範圍；`LiveRuntime` 沒有對應 restore 入口。
- `cmd/probe/main.go:1103-1108` 讀 `m.ModeChanges`（只印 `Step`、`Mode`），所以 `ModeChanges` 必須保留追加行為，`ModeChange` 增欄位不改其輸出。
- `LiveRuntime` 共 21 個覆繪家族（每條語言 lane、每個倍率各一組 presenter）：9 個訂閱 A000 預寫（`live_runtime.go:850-883`），11 個靠指令鉤或事件鉤、**不**訂閱 A000（story 各頁的 `prewrite()` 全是空函式，`live_story.go:321,383,443,503,565,625,685,745`），1 個衍生面板（本機英文關鍵字列，由手冊 presenter 的 `VisibleRequest()` 驅動）。
- 合成 A000 預寫（設計 B）不可行：post-join、skill exit、exit prompt 對不認識的相交寫入者或 `Offset >= 0x10000` 一律 fail 並增加 `resets[...]` 計數（`post_join_menu.go:212-224`、`skill_exit.go:266-285`、`post_join_exit_prompt.go:228-262`）；
  B 家族依寫入者 CS:IP 辨識；body icon 的 `Prewrite` 會追加 `invalidations`（`body_icon_overlay.go:704`）；`LiveRuntime.VideoWrite` 每次呼叫都 `storyDirty = true`；且只蓋到 9 個家族。
- 已有的整層失效 API 多數會改變計數或設為 Failed：`SkillExitWatcher.Discontinuity`、`PostJoinExitPromptWatcher.Discontinuity`、`PostJoinMenuWatcher.ObserveDiscontinuity` 都使 watcher `fail`，之後 `resets[...]` 增加；它們不可用於模式事件。
- 手冊家族的狀態機：overlay 的 `Clear` 只接受 Pending（no-op）或 Visible（清層，轉 Cleared），其餘狀態回錯（`manual_overlay_runtime.go:242-254`）；`ManualPresentationConsumer` 失敗時不推進 cursor，會永久卡住。`Watcher.Begin` 要求 generation 嚴格遞增（`watcher.go`），共享 watcher 不可重建。
- 身體圖示的 live 路由要求 `t.Generation > o.generation`（`body_icon_overlay.go:533-540`），watcher 的 generation 不可歸零。

未知（實作後量測，§5）：Buck 是否只在啟動與離開設模式（一手證據只有 `docs/re/phase-66-vga-palette-state-parity.md:16` 的啟動 `#7,520,426`）；
模式事件落在 glyph、dispatcher 或 ECL 呼叫進行中時的行為（U2）；`phase-66` 記錄的 100M step raw framebuffer 雜湊在目前 HEAD 是否仍成立。

## 3. 契約

### 3.1 通用層（不放遊戲專屬邏輯）

- `internal/machine`：`ModeChange` 增 `Cleared bool`（本次是否由 `resetMode` 清了四個平面，即 `planarMode(Mode)`）；`Machine` 增
  `ObserveModeChanges(fn func(ModeChange))`（nil 關閉）。`SetVideoMode` 在最後（`planarOn` 更新之後）呼叫 callback，**保留** `ModeChanges` 追加。
  沒掛 observer 時行為與位元組完全不變。callback 在 `Step()` 中途被呼叫，不得改變執行狀態、不得 panic；呼叫時機早於 `loadVGA16DAC`，callback 內不讀 `Palette()`。
  不補「mode 13h 實際清畫面」（BIOS 保真度，另案）。
- `session`：仿 `AudioObserver`（`observer.go:24-34`）加可選介面 `ModeObserver { VideoModeChange(machine.ModeChange) }`，不改 `StepObserver`；
  `runObserved` 在 `SetOnFrame` 之後，若 observer 實作該介面就 `ObserveModeChanges(guarded)`（guard 同 AudioObserver 區塊，共用 `videoPanic` latch），結束時 `ObserveModeChanges(nil)`。
- 驅動轉發：`cmd/buckrogers-play` 的 `liveObserver`、`cmd/buckrogers-session` 各加 `VideoModeChange` 轉 `LiveRuntime.VideoModeChange`；`cmd/buckrogers-text-receipt` 在 `ObserveVideoWrites` 同處加 `ObserveModeChanges`，**只轉給 `liveAll`**。
  text-receipt 內的 legacy 家族（收據證明線）本輪不接，保持與 live 在沒有模式事件時等價；日後同步時各 owner 已有 `Stop()`／`Restore()`、story 有 `ObserveExecutionDiscontinuity()`＋`Clear()`。

### 3.2 `LiveRuntime.VideoModeChange(machine.ModeChange)`

對每條 lane、每個倍率的下列家族逐一重置。通則：

- **R1 非 fail**：不用會把 watcher 設成 Failed 的 API。
- **R2 空狀態零副作用**：家族空閒時不得改變任何會進 `DebugSummary` 或收據的值（`resets`、`rebuilds`、`Stats`、`Missing`、`generation`、`drops`、`Actions` 歷史）。空閒判定用家族自己的 `Active()`、`Pending()`、`ActiveKeys()`。冷啟動 step 7,520,426 設 mode 13h 時所有家族都是空的。
- **R3 順序**：先 watcher 後 presenter（與 `clearWrite` 相同，`live_story.go:314-320`）；反過來會讓 `needsApply()` 看到 watcher 仍 active 而把 presenter 重畫。
- **R4 不重建持有單調 generation 的共享 watcher**（body icon、manual）。
- **R5 不回傳錯誤**（`live_runtime.go:34-36`：覆繪層出錯不得停止遊戲）；presenter 出錯時計數並 `resetMenuSelf`，同 `menuClear`（`live_lane.go:345-353`）。

| 家族 | 動作 |
|---|---|
| ECL 文字窗、hmenu、引擎 dispatcher、logbook | 各 watcher `ObserveDiscontinuity()`；presenter 由下一次 `Frame`／`ComposeWith` 的 `sync*` 依 `Generation()` 變化清掉（空時 `gen`、`Stats` 不動） |
| 身體圖示 | 新增 `LiveBodyIconWatcher.Reset()`（清 `state`、`collecting`，**不動 `generation`**）與 `RuntimeBodyIconOverlay.ClearAll()`（清 layer、`active`、`rects`、`missing`，**保留 `generation`、`transition`**）；不借用 `Prewrite(Offset:0x10000)`（會追加 invalidation） |
| 加入後選單 | 空閒（`stage==0 && !active && pending==nil && !failed`）略過；否則新建 watcher（同 `resetPostJoin` 但**不計數**），presenter 用既有私有 `clear()`（保留 `Missing`） |
| 技能離開確認、加入後提示 | `Restore()`（不是 `Discontinuity()`），兩個倍率；`q1Accepted` 重置（進行中的兩題流程須重來） |
| 劇情第 9 頁 | `StoryPage9Owner.ObserveExecutionDiscontinuity()` 後呼叫 `clear()` 使 `gen[i]` 歸零 |
| 選單 menu | 每條 lane `menuClear([4]uint8{24,39,0,0})`；**共享 recorder 不動** |
| 技能操作列 | 新增 watcher 與 presenter 各一個 `ResetDisplay()`（等價 default 錨點分支：watcher `pending=nil; collector.clear()`，presenter `screen=""; clearAll()`），兩邊同時重置 |
| 手冊題 | 新增 `Watcher.ObserveDisplayReset(step)`：只在 `collector.active()` 時動作；Visible 時私下清 `visible` 並**只**往 `presentation` 追加 `ManualPresentationClear{Generation}`（不追加 `Observation`，不偽造「已證實的清除呼叫」）；Pending 時 `pending.poisoned = true`；handler 結尾立即 `syncManual()`。不重建共享 `Watcher`；不對 `manPres[i]` 直接 `resetLayers()` |
| 手冊英文列 | 不需動作（手冊 Clear 使 `VisibleRequest()` 為假，下一次 `sync` 丟掉 layer） |
| 劇情首屏與第 2 至 8 頁 | `storyFamily` 介面新增 `modeReset()`（編譯期強制新頁面實作）：先 `discontinuity()` 再 `clear()`（歸零 `gen`）；以 `Active()` 等為條件略過空狀態（避免 `drops++`） |
| 共享狀態 | `storyPending = nil`、`prevAt`、`prevOp` 歸零；`r.party`、`r.ovl`、`r.norm`、`indexed`、`palette` 不動 |

所有 lane 都要重置（規格 040 §3.2：每條 lane 都看每個觀察），包含目前不是合成語言的 lane 與 `r.cur < 0`（英文）時。

### 3.3 防回退

- 一個列舉 `liveLane` 欄位的反射測試：每個覆繪相關欄位對應一個重置動作，新增欄位沒有分類就失敗。
- `storyFamily.modeReset()` 讓新增 story 頁面在編譯期被迫實作。

### 3.4 不變量

1. 沒有模式事件時（所有現有 state 起跑的重播），輸出位元組與現行相同。
2. 冷啟動遇到 mode 13h 事件（所有家族皆空）：記憶體、CPU、indexed、palette 雜湊、`DebugSummary`、`Resets()` 與修改前逐字相同。
3. 有覆繪存在時發模式事件：`ComposeWith` 的結果等於原版放大畫面（`ScaleIndexedRGBA`），無殘字；之後同一家族可以正常再次顯示（單調性不破：body icon、manual、page 9）。
4. 不重複送清除：手冊在模式事件後，真正的 `026F:029C` 清除不會再送一次 Clear，也不使 consumer 報錯。
5. 通用層不含遊戲專屬邏輯。

## 4. 不在範圍

- `state.Load`／`Snapshot.Restore` 的不連續（另案，可重用本規格的重置函式，但不要重用 `ModeChange` 型別）。
- BIOS 保真度（`AL` bit 7、mode 13h 不清 `Mem`）。
- text-receipt 的 legacy 家族。
- 平面模式下覆繪層的 320×200 畫面尺寸假設（Buck 不用平面模式）。

## 5. 驗收

1. 通用層與 session 單元測試：預設 nil；`SetVideoMode(0x13)` 得 `Cleared=false`、`0x12` 得 `Cleared=true` 且平面為零；callback 時 `VideoMode()` 已是新模式；`ObserveModeChanges(nil)` 關閉；`len(ModeChanges)` 照常成長；
   `int 10h AH=00`（含 `AX=0093h`）經 `DOS.int10` 恰好觸發一次；session 合成 COM（`B8 13 00 / CD 10 / EB FE`）事件一次且帶 `Step`、callback panic 停在該步之後、沒實作介面的 observer 行為不變、實作介面的 observer 不改 `machineDigest`。
2. 家族負例（全部合成）：每個家族兩個倍率各做 (i) 造出 active、(ii) 發事件、(iii) 斷言 `ActiveKeys()` 為空、`Draw` 等於 `ScaleIndexedRGBA`、(iv) 空狀態下呼叫後 `generation`、`resets`、`rebuilds`、`Stats`、`drops` 都沒變。
   加測：body icon 事件後第二輪 transition 的 `Generation` 仍遞增且不增加 `resets["body-icon"]`；post-join 重置後可重新走完 7 筆 entry 且 `resets["post-join"]` 不變；exit prompt 的 `q1Accepted` 被重置；
   manual 三個起始狀態（Visible、Pending、已 Cleared）與「Visible → 模式事件 → 真正的 Clear」不報錯、不重複送 Clear；action bar 重置後 `screen==""` 且不增加 `resets["action-bar"]`；story 各頁「只重置 watcher、presenter 不動時 `needsApply()` 為假」；反射測試。
3. `LiveRuntime` 整合：`VideoModeChange` 後 `ComposeWith` 等於 `ScaleIndexedRGBA`；全新 runtime 呼叫前後 `DebugSummary()` 與 `Resets()` 逐字相同。
4. 重播與冷啟動（同一 dosgolem 工作樹 A/B：實作 commit 的父 commit 為 A，實作 commit 為 B）：
   - 迴歸：既有 state 起跑的重播（phase316 手冊題時點、phase254 七條）A、B 位元組相同。這些重播不經 `SetVideoMode`，**不證明** mode 13h 路徑，文件須如實寫明。
   - 注入：在 text-receipt 加**僅供測試**的 `-set-video-mode-at STEP:MODE`（預設關閉，不進生產），用 phase254 的 state 讓某家族 active 後注入，斷言 `-live-rgba-out` 等於不含覆繪的放大畫面。
   - 冷啟動（唯一會發生啟動期模式事件的路徑）：`cmd/buckrogers-session`，步數超過 7,520,426，A、B 比對全部 JSON 行與最後的 `memory_sha256`、`cpu_sha256`、`indexed_sha256`、`palette_sha256` 與 RGBA；`buckrogers-play`（`workplace/phase311/run.sh`）比對 stderr 的 `compose_sha256` 與 `live:` DebugSummary 行。
     另記錄整個腳本期間實際收到的模式事件序列（暫時計數，只記 Mode 與 Step），回答 U1／U2。
5. `apps/buckrogers` 套件測試在乾淨匯出（不含未入版控檔）上全過；設 `BUCKROGERS_CHT_ROOT` 的閘控測試無 `--- SKIP`；`go vet` 通過。
6. 文件：規格 026 契約第 5 條加指向本規格的 pointer；`docs/re/` 加收據；Issue #22 依完成條件逐項回報後關閉。

## 6. 風險

- 手冊與 body icon 的狀態機單調性是最細的部分；錯一步會使 consumer 卡死或 transition 被拒（驗收 2 的加測專門覆蓋）。
- 驗收的真空成立風險：從 state 起跑的重播不發生模式事件，收據相同不代表 mode 13h 路徑正確；所以冷啟動比對與注入測試是必要項。
- 事件在 glyph、dispatcher、ECL 呼叫進行中發生時（U2）：本規格清 `storyPending`、不動 menu recorder（其 pending frame 由自己的返回護欄收斂），強推論；以冷啟動期間的事件序列與合成測試驗證。
- 事件到下一次 retrace 之間的 `Compose` 用舊畫面加空覆繪層，即原版英文，是安全方向。
- legacy 家族本輪不接：若日後 legacy runner 與 live 比對在模式事件下分歧，要同步。
