# 052 — 視訊模式設定時覆繪層整層失效

狀態：**READY**（2026-10-02；兩輪獨立審查的必修與建議已併入，審查者認為升 READY 前只需修訂 §5.4 的驗收寫法，已修）。實作與驗收見 docs/re/phase-318（待寫）。
日期：2026-10-02
Issue：#22
前置：規格 026（儲存詢問離頁交接，契約第 5 條提出此缺口）、040（多語通道）、053（手冊 E1 接入玩家路徑，READY）、dosgolem `session` 的 `AudioObserver` 先例。
先後：規格 053 會改 `syncManual`（3× zh-TW `Sync()` 回錯時把 `e1Base` 設 nil 再 `Sync()` 一次）並新增 `liveLane` 欄位。若 053 先實作，§5.4 的 A 是含 053 的父 commit；
本規格 handler 結尾的 `syncManual()` 依 053 的退路處理 E1 失敗；反射測試須涵蓋 053 新增的欄位。
證據：盤點報告（2026-10-02，只讀，dosgolem `e992599`）與獨立審查（`workplace/review052/REVIEW.md`）；行號皆為該 commit。盤點代理無法寫檔，報告正文只在對話中，本規格把後續實作需要的結論全部寫在 §2、§3。

## 1. 為什麼要做

`int 10h AH=00` 經 `internal/dos/bios.go:21` 呼叫 `Machine.SetVideoMode`（`internal/machine/bda.go:68-86`）：寫 BDA、追加 `ModeChange{Mode, Step}`、平面模式（0x0D 至 0x12）呼叫 `VGA.resetMode` 清四個平面（不經 `Write8`），其餘模式只更新時序暫存器。
`machine.ObserveVideoWrites` 的 callback 在 `Write8` 內（`machine.go:660-663`），所以模式設定完全不可見。
依 A000 預寫失效的覆繪家族，以及靠指令鉤或事件鉤的家族，在這個時點都沒有入口得知「顯示已不連續」，可能留下殘字。
Buck 實際路徑只在冷啟動（step 7,520,426）與離開時設模式；目前已驗路徑不觸發，所以列為低優先，但缺口是通用層的。

## 2. 證據（已證實，除非標明）

- `SetVideoMode` 的生產呼叫端只有 `internal/dos/bios.go:21`；`AL` bit 7（不清畫面旗標）被 `& 0x7F` 丟掉（`bios.go:20`，不在本規格範圍）。
- mode 13h 與文字模式 3 不清 `Mem[0xA0000..]`（`bda.go:75-84`）。所以 #22 對 mode 13h 不是「記憶體被清了卻觀察不到」，而是**模式切換是顯示不連續點**，覆繪層沒有入口。覆繪層對任何模式事件都整層失效。
- `state.Load`（`state.go:218`）與 `Snapshot.Restore`（`snapshot.go:183`）直接倒回 VGA 與 `planarOn`，不經 `SetVideoMode`，是同一種洞但不在本規格範圍；`LiveRuntime` 沒有對應 restore 入口。
- `cmd/probe/main.go:1103-1108` 讀 `m.ModeChanges`（只印 `Step`、`Mode`），所以 `ModeChanges` 必須保留追加行為。`ModeChange` 不進 state／snapshot。
- `LiveRuntime` 共 21 個覆繪家族（每條語言 lane、每個倍率各一組 presenter）：9 個訂閱 A000 預寫（`live_runtime.go:850-883`），11 個靠指令鉤或事件鉤、**不**訂閱 A000（story 各頁的 `prewrite()` 全是空函式，`live_story.go:321,383,443,503,565,625,685,745`），1 個衍生面板（本機英文關鍵字列，由手冊 presenter 的 `VisibleRequest()` 驅動）。
- 合成 A000 預寫（設計 B）不可行：post-join、skill exit、exit prompt 對不認識的相交寫入者或超界 `Offset` 一律 fail（post-join 只 fail、計數延到下一次 Entry/Return 的 `resetPostJoin`；skill exit 與 exit prompt 經 `ownersPrewrite` 立即 `recover` 計數，`live_lane.go:500-509`）（`post_join_menu.go:212-227`，相交門檻 `Offset >= 64000`；`skill_exit.go:278-297`，`Offset >= 0x10000` 即 `Fault`；`post_join_exit_prompt.go:228-262`）；
  ECL、hmenu、engine、logbook 對 `Offset >= 64000` 直接忽略（`ecl_text.go:636`、`hmenu.go:304`、`engine_dispatch.go:466`、`logbook.go:328`）；B 家族依寫入者 CS:IP 辨識；body icon 的 `Prewrite` 會追加 `invalidations`（`body_icon_overlay.go:704`）；
  `LiveRuntime.VideoWrite` 每次呼叫都 `storyDirty = true`；且只蓋到 9 個家族。
- 已有的整層失效 API 多數會改變計數或設為 Failed：`SkillExitWatcher.Discontinuity`、`PostJoinExitPromptWatcher.Discontinuity`、`PostJoinMenuWatcher.ObserveDiscontinuity` 都使 watcher `fail`，之後 `resets[...]` 增加（`skill_exit.go:229-236`、`post_join_exit_prompt.go:286`、`post_join_menu.go:238-245`）；它們不可用於模式事件。
- 手冊家族的狀態機：generation 嚴格遞增的檢查在 `RuntimeManualOverlay.Apply` 的 Begin 分支（`manual_overlay_runtime.go:234-236`）；overlay 的 `Clear` 只接受 Pending（no-op）或 Visible（清層，轉 Cleared），其餘狀態回錯（`manual_overlay_runtime.go:242-256`）；
  `ManualPresentationConsumer` 失敗時不推進 cursor，會永久卡住（`manual_presentation_consumer.go:35-40`）。共享 `Watcher` 不可重建，理由有二：(a) 每條 lane、每個倍率的 `ManualPresentationBridge` 持有 `*Watcher` 指標（`manual_presentation_bridge.go:7-10`），重建後 bridge 仍讀舊物件；
  (b) 新 `Collector` 的 generation 從 0 起算，第一個 Begin 的 generation 不大於 presenter 已記錄的值，會被 `Apply` 拒絕，consumer 之後永久卡住。
- 身體圖示的 live 路由要求 `t.Generation > o.generation`（`body_icon_overlay.go:541`），watcher 的 generation 不可歸零。
- story 家族：opening、page2、page3、page5 的 `ObserveExecutionDiscontinuity` 無條件 `drops++`；page4、6、7、8 不計 drops；`Pending()` 只存在於 opening、2、3、5、6、9。`BeforeStep` 只在 `r.storyPending != nil` 時送 `verifiedReturn`，下一次 glyph entry 也只在 `r.storyPending != nil` 時補呼 `discontinuity()`（`live_runtime.go:530-539、676-678`）。
- 冷啟動模式事件（實測）：HEAD `e992599` 的 `cmd/probe` 冷啟動 `START.EXE`，無輸入跑 6,000 萬步，模式事件只有一次：`#7520426→13h`。
- `BeforeStep`、`Frame`、`Compose` 與新 callback 都在同一 goroutine：session 的 callback 在 `RunUntilObserved` 內同步呼叫（`session/observer.go:133-219`）；`buckrogers-play` 在 `Update` 呼 `Advance`、在 `Draw` 呼 `Compose`，Ebitengine 保證 game 函式同一 goroutine。
- 建 `LiveRuntime` 的驅動只有 `buckrogers-play`、`buckrogers-session`（只載 zh-TW）、`buckrogers-text-receipt`。

未知（實作後量測，§5）：有輸入路徑（含離開）的模式事件序列；模式事件落在 glyph、dispatcher 或 ECL 呼叫進行中時的行為（U2）；「冷啟動時所有家族皆空」目前是強推論；`phase-66` 記錄的 100M step raw framebuffer 雜湊在目前 HEAD 是否仍成立。

## 3. 契約

### 3.1 通用層（不放遊戲專屬邏輯）

- `internal/machine`：`Machine` 增 `ObserveModeChanges(fn func(ModeChange))`（nil 關閉）。`SetVideoMode` 在最後（`planarOn` 更新之後）呼叫 callback，**保留** `ModeChanges` 追加。
  `ModeChange` 結構不增欄位（`Mode`、`Step` 已足夠；是否清平面可由 `planarMode(Mode)` 推得，目前沒有消費者需要它）。
  沒掛 observer 時行為與位元組完全不變；callback 不進 `Snapshot` 或 `state`（同 `onVideoWrite`）。
  callback 在 `Step()` 中途被呼叫，不得改變執行狀態、不得 panic；呼叫時機早於 `loadVGA16DAC`，callback 內不讀 `Palette()`。
  不補「mode 13h 實際清畫面」（BIOS 保真度，另案）。
- `session`：仿 `AudioObserver`（`observer.go:24-34`）加可選介面 `ModeObserver { VideoModeChange(machine.ModeChange) }`，不改 `StepObserver`。
  現行 `guard` 宣告在 `AudioObserver` 的 `if` 區塊內（`observer.go:159-173`），改為提到區塊外，`AudioObserver` 與 `ModeObserver` 共用，共用 `videoPanic` latch。
  `runObserved` 在 `SetOnFrame` 之後，若 observer 實作該介面就 `ObserveModeChanges(guarded)`，結束時 `ObserveModeChanges(nil)`。
- 驅動轉發：`cmd/buckrogers-play` 的 `liveObserver`、`cmd/buckrogers-session` 各加 `VideoModeChange` 轉 `LiveRuntime.VideoModeChange`；`cmd/buckrogers-text-receipt` 在 `ObserveVideoWrites` 同處加 `ObserveModeChanges`，**只轉給 `liveAll`**。
  text-receipt 內的 legacy 家族（收據證明線）本輪不接，保持與 live 在沒有模式事件時等價；日後同步時各 owner 已有 `Stop()`／`Restore()`、story 有 `ObserveExecutionDiscontinuity()`＋`Clear()`。

### 3.2 `LiveRuntime.VideoModeChange(machine.ModeChange)`

對每條 lane（含目前不是顯示語言的 lane，與 `r.cur < 0` 的英文情形；規格 040 §3.2：每條 lane 都看每個觀察）、每個倍率的下列家族逐一重置。通則：

- **R1 非 fail**：不用會把 watcher 設成 Failed 的 API。
- **R2 空狀態零副作用**：家族「空」時不得改變任何會進 `DebugSummary` 或收據的值（`resets`、`rebuilds`、`Stats`、`Missing`、`generation`、`drops`、`Actions` 歷史）。
  各家族「空」的定義：ECL `Pages()` 為空；hmenu `Page()==nil`；engine `Lines()` 為空且 `pending==nil`；logbook `open==0`；body icon `len(active)==0`；post-join `stage==0 && !active && pending==nil && !failed`；
  story 見下表；手冊 `collector.active()` 為假；action bar `screen==""` 且無 pending。B 家族非空時 `ObserveDiscontinuity` 會遞增 `Stats.Invalidations`（logbook `Stats.Closes`），那是預期；
  `inCall`、engine `pending`、logbook `tlBy`／`kbArmed` 等非計數欄位不論空不空都會被重置（呼叫框已無法證明），也是預期。
- **R3 結束時的狀態**：handler 結束時 story 的 watcher 不再 active 且 presenter `gen==0`，否則下一步 `applyStories` 會重套。（`needsApply()` 只在 `BeforeStep` 讀取，handler 內部順序不會被觀察到。）
- **R4 不重建持有單調 generation 的共享 watcher**（body icon、manual）。
- **R5 不回傳錯誤**（`live_runtime.go:34-36`：覆繪層出錯不得停止遊戲）；presenter 出錯時計數並 `resetMenuSelf`，同 `menuClear`（`live_lane.go:345-353`）。

| 家族 | 動作 |
|---|---|
| ECL 文字窗、hmenu、引擎 dispatcher、logbook | 各 watcher `ObserveDiscontinuity()`；presenter 由下一次 `Frame`／`ComposeWith` 的 `sync*` 依 `Generation()` 變化清掉 |
| 身體圖示 | 新增 `LiveBodyIconWatcher.Reset()`（清 `state`、`collecting`，**不動 `generation`**）與 `RuntimeBodyIconOverlay.ClearAll()`（清 layer、`active`、`rects`、`missing`，**保留 `generation`、`transition`**）；不借用 `Prewrite(Offset:0x10000)`（會追加 invalidation） |
| 加入後選單 | watcher：`failed` 時**不動**（保留既有的延後計數路徑，真實失敗不被吞掉）；`stage==0 && !active && pending==nil` 時略過；其餘新建 watcher（同 `resetPostJoin` 但不計數、不重建 presenter）。presenter：兩個倍率一律私有 `clear()`（保留 `Missing`） |
| 技能離開確認、加入後提示 | 各 owner 兩個倍率呼叫 `Restore()`（watcher `Restore()`＋presenter `Clear()`，`skill_exit_overlay.go:168`、`post_join_exit_prompt_overlay.go:185`）；exit prompt 的 `Restore()` 本身已重置 `q1Accepted`。不用 `Discontinuity()` |
| 劇情九頁（首屏、第 2 至 9 頁） | `storyFamily` 新增 `modeReset()`，**九個實作都要有**（含 page 9）。動作：先 watcher `discontinuity()`，再 `clear()`（presenter `Clear()`、`gen` 歸零）。略過條件：opening、2、3、5 為 `!Active() && !Pending()`（避免無條件 `drops++`，且不留孤兒 in-flight frame）；page 4、6、7、8 不計 drops，一律執行（page 6 雖有 `Pending()`，一律執行等價且表格較單純）；page 9 一律執行（`StoryPage9Watcher.clear()` 只在有狀態時遞增 generation） |
| 選單 menu | 每條 lane `menuClear([4]uint8{24,39,0,0})`；**共享 recorder 不動** |
| 技能操作列 | 新增 watcher 與 presenter 各一個 `ResetDisplay()`（等價 default 錨點分支：watcher `pending=nil; collector.clear()`，presenter `screen=""; clearAll()`），兩邊同時重置 |
| 手冊題 | 新增 `Watcher.ObserveDisplayReset(step)`：只在 `collector.active()` 時動作；Visible 時私下清 `visible` 並**只**往 `presentation` 追加 `ManualPresentationClear{Generation}`（不追加 `Observation`，不偽造「已證實的清除呼叫」）；Pending 時 `pending.poisoned = true`；handler 結尾立即 `syncManual()`（經規格 053 的退路）。不重建共享 `Watcher`（理由見 §2）；不對 `manPres[i]` 直接 `resetLayers()` |
| 手冊英文列 | 不需動作（手冊 Clear 使 `VisibleRequest()` 為假，下一次 `sync` 丟掉 layer） |
| 共享狀態 | `r.storyPending = nil`、`prevAt`、`prevOp` 歸零，**必須在所有 story 頁 `modeReset()` 之後**；`r.party`、`r.ovl`、`r.norm`、`indexed`、`palette` 不動 |

### 3.3 防回退

- 反射測試列舉 `liveLane` 與 `LiveRuntime` 兩個 struct 的全部欄位（含規格 053 新增者），每欄分類為「重置」（對應 §3.2 的一列）或「明示不動」（附理由，例如 `menu` recorder、`party`、`ovl`、`norm`、`indexed`、`palette`、catalog 與字型、計數 map）。未分類欄位使測試失敗。
- `storyFamily.modeReset()` 讓新增 story 頁面在編譯期被迫實作。
- `LiveRuntime.ActiveFamilies(lang)` 是唯讀方法（只回家族名稱，不改任何狀態），不需在反射測試中分類。

### 3.4 不變量

1. 沒有模式事件時（所有現有 state 起跑的重播），輸出位元組與現行相同。
2. 冷啟動遇到 mode 13h 事件：記憶體、CPU、indexed、palette 雜湊、`Resets()` 與修改前逐字相同；`DebugSummary` 除規格 053 新增的欄位外逐字相同。
3. 有覆繪存在時發模式事件：`ComposeWith` 的結果等於原版放大畫面（`ScaleIndexedRGBA`），無殘字；之後同一家族可以正常再次顯示（單調性不破：body icon、manual、page 9）。
4. 不重複送清除：手冊在模式事件後，真正的 `026F:029C` 清除不會再送一次 Clear，也不使 consumer 報錯。
5. 通用層不含遊戲專屬邏輯。

## 4. 不在範圍

- `state.Load`／`Snapshot.Restore` 的不連續（另案，可重用本規格的重置函式，但不要重用 `ModeChange` 型別）。
- BIOS 保真度（`AL` bit 7、mode 13h 不清 `Mem`）。
- text-receipt 的 legacy 家族。
- 平面模式下覆繪層的 320×200 畫面尺寸假設（Buck 不用平面模式）。

## 5. 驗收

1. 通用層與 session 單元測試：預設 nil；`SetVideoMode(0x13)` 與 `0x12` 都觸發恰好一次；callback 時 `VideoMode()` 已是新模式；`ObserveModeChanges(nil)` 關閉；`len(ModeChanges)` 照常成長；
   `int 10h AH=00`（含 `AX=0093h`，記錄 `& 0x7F`）經 `DOS.int10` 恰好觸發一次；session 合成 COM（`B8 13 00 / CD 10 / EB FE`）事件一次且帶 `Step`、callback panic 停在該步之後、
   沒實作介面的 observer 行為不變、實作介面的 observer 不改 `machineDigest`；`Snapshot`／`state` 位元組不含 callback。
2. 家族負例（全部合成）：每個家族兩個倍率各做 (i) 造出 active、(ii) 發事件、(iii) 斷言 `ActiveKeys()` 為空、`Draw` 等於 `ScaleIndexedRGBA`、(iv) 空狀態下呼叫後 `generation`、`resets`、`rebuilds`、`Stats`、`drops` 都沒變。
   加測：
   - body icon 事件後第二輪 transition 的 `Generation` 仍遞增且不增加 `resets["body-icon"]`。
   - post-join：重置後可重新走完 7 筆 entry 且 `resets["post-join"]` 不變；straddle（entry → 事件 → return）斷言 `resets["post-join"]` 恰 +1 且畫面等於 `ScaleIndexedRGBA`；
     failed → 事件 → 下一個 entry，斷言計數仍 +1（失敗沒被吞掉）。
   - exit prompt：Q1 active → 事件 → Q2 entry，斷言 `resets["exit-prompt"]` 的期望值（`recover` 以 lane 計，每個倍率各 +1）；skill exit 跨事件的 return 因 `Pending()` 為假而被忽略，不計數。
   - manual 三個起始狀態（Visible、Pending、已 Cleared）與「Visible → 模式事件 → 真正的 Clear」不報錯、不重複送 Clear；先前已卡住的 lane 不新增缺陷。
   - action bar 重置後 `screen==""` 且不增加 `resets["action-bar"]`。
   - story 九頁：略過條件各自成立；有 in-flight frame（`Pending()` 為真但 `Active()` 為假）時事件後 watcher 與 presenter 都乾淨；事件後 `storyPending == nil` 且下一個 glyph entry 正常；page 4、7、8 無條件執行。
   - 反射測試（§3.3）。
3. `LiveRuntime` 整合：`VideoModeChange` 後 `ComposeWith` 等於 `ScaleIndexedRGBA`；全新 runtime 呼叫前後 `DebugSummary()` 與 `Resets()` 逐字相同。
4. 重播與冷啟動（A 為實作 commit 的父 commit，B 為實作 commit，各自從乾淨匯出建置；若 053 先實作，A 含 053）：
   - 迴歸：既有 state 起跑的重播（phase316 手冊題時點、phase254 七條）A、B 位元組相同。這些重播不經 `SetVideoMode`，**不證明** mode 13h 路徑，文件須如實寫明。
   - **注入（observer-only，僅供測試）**：text-receipt 增 `-inject-mode-event MODE`（預設關閉）。主迴圈（條件 `for m.Steps < *until && !d.Exited`）正常結束且 `m.Steps == until` 時，在迴圈之後、`live:` DebugSummary 與所有輸出之前，
     呼叫 `liveAll.VideoModeChange(machine.ModeChange{Mode: MODE, Step: until})`；這等於「第 until 步的 `BeforeStep` 之前」，之後不再執行任何指令（不能放在迴圈內：`m.Steps == until` 的 `BeforeStep` 不會發生，放在 until−1 會多跑一道指令而可能使家族重新啟用）。
     迴圈提早結束（`d.Exited` 或 `-stop-after-step`）時拒絕。**不呼叫 `m.SetVideoMode`**（那會改 BDA、CRTC 與 `ModeChanges`，A/B 雜湊不可比）。
     runner 在同一次執行內把三件事寫進 receipt JSON 的新欄位（不改既有欄位）：(a) 注入前 `ComposeWith(m.Indexed(), m.Palette(), live-scale)` 的 SHA-256；(b) `ScaleIndexedRGBA(m.Indexed(), m.Palette(), live-scale)` 的 SHA-256；
     (c) 注入前各家族的 active 清單，由新增的**唯讀、僅供測試與 runner 使用**的方法 `LiveRuntime.ActiveFamilies(lang) []string` 取得（只回家族名稱，不改任何狀態；放在 `apps/buckrogers`）。先合成再注入會使 `syncB` 與 action bar 的 `Draw` 改動 presenter 狀態，
     只影響注入前的那次合成，模式事件本來就會清掉這些狀態，可以接受。斷言：
     (1) 同一 state、同 `-until`、同 `-lang`（必給，否則沒有 `cpu_sha256`），注入與未注入的 `memory_sha256`、`cpu_sha256`、`indexed_sha256`、`palette_sha256` 相同；
     (2) (a) ≠ (b) 且 (c) 非空（非真空）；
     (3) 注入後 `-live-rgba-out` 的 SHA-256 等於 (b)。語言用 zh-TW 與至少一個非參考語言，兩個倍率都跑；不得用 `en`（`r.cur < 0` 時 `ComposeWith` 本來就回原版，真空成立）。
     逐家族至少一個時點依 §7 對照表（含 phase301 的 ecl、hmenu、logbook 與 phase104 的 page 2 至 9）；只有引擎 dispatcher（若 (c) 掃描各時點後仍無）與手冊英文列以 §5.2 合成測試補。
   - phase254 的 live 對 runner 比對本來就有 DIFF（body、opening、post、skill、部分 manual），是 live 含 B 家族與規格 040 差異的既有狀態；本規格的迴歸是 A 對 B，不受影響。
   - 冷啟動：`buckrogers-session`（只載 zh-TW）與 `buckrogers-play`（多 lane，`workplace/phase311/run.sh`，A、B 各建一份並以 `BIN=` 指定；不加 `-manual-english`）。A、B 比對全部 JSON 行與最後的
     `memory_sha256`、`cpu_sha256`、`indexed_sha256`、`palette_sha256`、RGBA、stderr 的 `compose_sha256` 與 `live:` DebugSummary 行。
     另以暫時探針在事件當下記錄每個家族的 `ActiveKeys`／`Pending`（非真空證據，強推論轉已證實）。`buckrogers-session`（預設時脈）斷言序列恰為 `#7520426→13h`；
     `buckrogers-play`（預設 `-clock 50`，步數可能不同）只斷言恰好一次 13h 事件並記錄實際步數，不寫死。有輸入路徑（含離開）的序列另記（回答 U1／U2）。
5. `apps/buckrogers` 套件測試在乾淨匯出（不含未入版控檔）上全過；設 `BUCKROGERS_CHT_ROOT` 與 `BUCK_OWNER_PROJECT` 的閘控測試中，本規格新增者無 `--- SKIP`；`go vet` 通過。
6. 文件：規格 026 契約第 5 條加指向本規格的 pointer；`docs/re/` 加收據；Issue #22 依完成條件逐項回報後關閉。

## 6. 風險

- 手冊與 body icon 的狀態機單調性是最細的部分；錯一步會使 consumer 卡死或 transition 被拒（驗收 2 的加測專門覆蓋）。
- 驗收的真空成立風險：從 state 起跑的重播不發生模式事件，收據相同不代表 mode 13h 路徑正確；所以注入與冷啟動比對是必要項，且注入前要先證明覆繪存在。
- 事件與原版呼叫交錯（U2）時，下列計數是**預期的 fail-closed 結果，不是缺陷**，畫面一律回到原版英文：
  post-join 跨事件的 return 或非 stage 0 的 entry 使 `resets["post-join"]` +1；exit prompt 於 Q1 顯示中發事件，之後的 Q2 entry 使 `resets["exit-prompt"]` +1。
- menu recorder 不動的後果：跨事件的 menu 請求（entry 在事件前、return 在事件後）事件後仍會 `menuApply`，是唯一會在事件後補畫的家族。mode 13h 在 dosgolem 不清 `Mem`，原文仍在畫面上，所以結果正確；平面模式會清平面，這條假設不成立（Buck 不用平面模式）。
- 手冊 Visible 時追加一筆 Clear，所有 lane 都會 `Sync()`；先前已卡住的 lane 會再 `resets["manual"]++`，不是新缺陷。
- 事件到下一次 retrace 之間的 `Compose` 用舊畫面加空覆繪層，即原版英文，是安全方向。
- legacy 家族本輪不接：若日後 legacy runner 與 live 比對在模式事件下分歧，要同步。

## 7. 附錄：家族與可用時點對照（§5.4 注入驗收用）

等級：已證實＝既有收據（rerun42）顯示該家族 active；強推論＝該時點專為該家族取樣，收據沒看逐家族欄位。

| 家族 | 可用時點（state、`-until`、鍵） | 等級 |
|---|---|---|
| 選單 menu | 幾乎每個 phase254 時點（menu 是 compose 的底層） | 強推論 |
| 技能操作列 | `phase254-live-families-parity/action.sh` 五點，例如 `skill504.state` 506,600,000 | 已證實 |
| 身體圖示 | `body.sh` move、refuse、confirm（`bbody.state`） | 已證實 |
| 手冊題 | `manual.sh` m266560000、m266650000（`phase12-before-question.state`） | 已證實 |
| 劇情首屏 | `opening.sh` o280900000（`phase96-first-final/control.state`） | 已證實 |
| 劇情第 2 至 9 頁 | `phase104-manual-correct-return/control.state`，`-until` 依序 290,900,000、300,900,000、310,900,000、320,900,000、330,900,000、340,900,000、350,900,000、352,100,000，鍵用 `story.sh` 的 `KEYS` | 已證實（舊版 runner 的 legacy 家族，2026-09-26 的 `active_keys`）；現行 `story.sh` 只剩三個不 active 的時點，需改回這八點 |
| 加入後選單 | `post.sh` pj-row20（`phase54/a-joined.state` 124,650,000） | 已證實 |
| 加入後提示 | `post.sh` q1、yy | 已證實 |
| 技能離開確認 | `skill.sh` cprompt、tprompt | 已證實 |
| ECL 文字窗 | phase301 `switch/cases.sh` ecl：`phase104…/control.state` 409,000,000，鍵 `F409K` | 強推論 |
| hmenu | phase301 hmenu：`phase258-ecl-ab/g2.state` 432,500,000 | 強推論 |
| logbook | phase301 logbook：`checkpoints/logbook41-pre.state` 5,285,000,000，鍵 5,276,500,000:1c:0d | 強推論 |
| 引擎 dispatcher | 沒找到專門時點：先用 `ActiveFamilies` 在上列各點掃描；都沒有才交給 §5.2 合成測試 | 未知 |
| 手冊英文列 | 需要本機手冊英文摘錄：只用合成測試 | — |
