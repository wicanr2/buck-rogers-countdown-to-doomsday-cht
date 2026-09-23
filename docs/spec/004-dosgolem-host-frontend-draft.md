# 004 — dosgolem host 前端與執行期倍率

狀態：DRAFT

前置：[第八十二階段 host 面板 prototype](../re/phase-82-host-settings-panel-visual-prototype.md)、
[第八十四階段能力盤點](../re/phase-84-dosgolem-host-frontend-capability-audit.md)

## 目的與邊界

本規格只界定一個通用、玩家可操作的 dosgolem host 前端應承接什麼資料與輸入邊界，讓
2×／3× 倍率能在執行期改變而不影響 DOS。它不是 Buck Rogers adapter、不是原版輸入模擬器，
也不授權實作任何視窗後端或設定面板。

Buck Rogers 的 host 控制列與面板必須將完整 320×200 畫布下推；既有幾何位於第八十二階段
證據。本規格不重複該遊戲的 rectangle，亦不把它放進 `apps/buckrogers/`。

## 已證實能力與缺口

| 項目 | 分級 | 證據與結論 |
| --- | --- | --- |
| dosgolem 現況 | 已證實 | 本機 `buck-rogers-cht-output-overlay` 的 `9240c3b19ad5eaba7a44a2b9b4f4420fe1653a0a`；README 明定它是無頭、決定性、供程式化觀測的執行器。 |
| 既有輸出疊層 | 已證實 | `xlate.Layer` 只讀 indexed framebuffer 與 palette，畫入新的 RGBA；`apps/buckrogers.RuntimeMenuOverlay.Draw` 同樣先重建 RGBA，沒有寫回 machine VRAM。 |
| 2×／3× 輸出 | 已證實 | Buck Rogers runtime overlay constructor 明示只接受 2 或 3；其 `scale` 為私有欄位，沒有執行期 setter。既有 instance 不能自行改倍率。 |
| C 的倍率 state core | 已證實／CONFORMED（純核心） | dosgolem spec 219 與第 89 階段：generic `host.ScaleController` 將 selected 與 active 分離，只有 Apply 提交；唯一直接 import 是 `fmt`，沒有 backend／DOS／遊戲依賴。 |
| host 面板事件核心 | 已證實（純核心；非玩家前端） | 本機 dosgolem 分支 `ecac793` 的 `host.PanelController` 只處理已分類的 host 事件：面板開啟時鍵盤及 host hit 不轉送，Apply 提交後自動收合；未命中 pointer 保持未決。Docker race／vet 已通過，未接 Ebitengine、machine 或持久化。 |
| DOS 滑鼠能力 | 已證實 | `cmd/probe` 的 `-mouse-*`／`-click-*` 是以固定 instruction step 呼叫模擬 DOS 滑鼠；它是原版輸入／對拍能力，不是 host 視窗事件。 |
| 可重用 host 視窗與事件迴圈 | 強推論：不存在 | `go.mod` 沒有前端依賴；所有 Go source 的 window／frontend／SDL／Ebiten／GLFW／event-loop token 搜尋為零；命令均為無頭診斷或收據工具。結論與 README 的定位一致，但實際選用哪個新 backend 仍未知。 |

`xlate.Layer`、原始 indexed framebuffer、palette 與 active overlay stamps 是可重用的資料層；
原生視窗、host pointer events、控制列繪製、hit test、面板焦點與 output-present loop 都需要
新增通用能力。不得把後者誤放入 `apps/buckrogers/`。

## 擬定通用契約

1. host presenter 的每一幀只讀取目前的 indexed framebuffer、palette 與 active presentation
   layer，建立 output RGBA；不改 VRAM、DOS 記憶體、檔案、存檔、BIOS queue 或 IRQ。
2. host layout 以目前 output scale 與 host chrome state 導出遊戲 canvas 的 output origin；遊戲
   canvas 必須完整保留，不能被 host control 覆蓋、裁切或以不同倍率重採樣。
3. 滑鼠移動、按下、放開先以 output-space hit rectangle 判斷。命中 host rectangle 的事件必須在
   任何 DOS 座標轉換、DOS mouse API、BIOS 或 IRQ 前被消費；未命中的未來 forwarding 另由
   backend 明示，不可借用 `cmd/probe` 的診斷注入。
4. 倍率改變時以同一份目前 raw indexed framebuffer、palette 與 active overlay state 重繪，
   不重啟 DOS、不送鍵、不清除 VRAM，也不遺失已顯示的繁中 stamp。
5. API 與 state 只可表達通用的 output scale、canvas、host chrome、host hit event 與重繪；
   Buck Rogers 的題目、翻譯鍵、矩形、手冊答案與遊戲座標不可出現在通用層。

## DRAFT：唯讀畫面快照邊界

為免 Ebitengine renderer 直接持有 machine 或誤把畫面讀取與輸入轉送混在一起，通用層
已建立最小的 `host` 純資料契約：

```go
type FrameSource interface {
    ReadPresentationFrame() (IndexedFrame, error)
}

type IndexedFrame struct {
    Canvas  Canvas
    Indexed []uint8
    Palette [256][3]uint8
}
```

`host.PresentationSnapshotProvider.Snapshot` 必須剛好讀取一份 `IndexedFrame`、檢查
`len(Indexed) == Canvas.Width * Canvas.Height`，並複製 indexed bytes 後才交給 renderer。
Palette 為值型別。故 presenter 即使修改它拿到的 slice，也沒有回寫 VRAM、DAC、DOS memory、
BIOS queue、IRQ、檔案或存檔的能力。這只是一條讀取邊界；它不處理 input、overlay Draw、
host chrome 或 backend event loop。

本機 dosgolem 分支已另有純 `host.PanelController`：它不持有 DOS machine，不自行送鍵，
只回傳 `ConsumedByHost`／`ForwardToDOS` 許可。它已實作「未按 Apply 即關閉面板」等於 Cancel：
selected 重設為 active 後收合；也不保存倍率至磁碟。因此不能把單元測試視為實際
BIOS／IRQ 零副作用收據。

具體 frontend adapter 必須在同一個 machine-stepping thread 取得此 frame，不能在 machine
並行 Step 時呼叫 source。這是避免取得跨幀 indexed／palette 配對的執行緒契約，而不是
允許 presenter 控制 machine。現階段尚未把 `Machine` 直接放進 `host` package，以維持 host
沒有 machine reference 的既有層次；Linux Ebitengine frontend 將以一個只實作
`FrameSource` 的邊界 adapter 接上。

## 已確認操作語意與未決前沿

使用者已選擇 option 點擊後「先選取、再按 Apply」（C），排除兩種立即套用。DRAFT host state
至少區分 `activeScale` 與暫存 `selectedScale`：點選 option 只能改後者；只有 Apply 可將它提交為
新的 output scale。第八十九階段已將這個 value-only transition 實作並 CONFORM；實際以同一 raw
input、palette 與 active layer 重繪仍屬未接線 frontend 責任；不推定跨重啟持久化。

- host 面板玩家可見文案使用繁體中文，按鈕至少以「設定／套用／取消」清楚表達；
  2×／3× 倍率記號保留。中文採使用者指定的本機倚天字型來源，不把字型 bytes 或衍生
  GOLEMFNT 放進 Git／公開包。具體字級、對齊與版面仍須實際截圖核對，不能由
  headless CLI 或 DOS mouse injection 推定。
- 使用者於 2026-09-22 確認第一個可玩版本先支援 Linux，架構保留日後擴充
  Windows／macOS 的能力；第一版三平台同步打包與驗收已排除。這只定平台優先序，
  不替持久化定案。
- 使用者其後確認設定面板開啟時，鍵盤只由 host 面板處理，不向 DOS 轉送；
  面板關閉後才恢復遊戲鍵盤。面板開啟仍能以鍵盤操作遊戲的分支已排除。
  host 面板命中的滑鼠與鍵盤事件均須對 DOS BIOS queue／IRQ 零副作用。
- 使用者看過 A／B 可丟棄原型後，確認按 Apply 提交倍率時自動收合面板，
  立即恢復遊戲鍵盤；保持展開以便連續調整的分支已排除。Apply 不得額外送鍵進 DOS。
- 使用者確認第一個 Linux 可玩版的 2×／3× 倍率只在本次遊戲期間保留；
  不寫跨重啟設定檔；每次啟動預設 2×，玩家可於本次遊戲中切到 3×。
  預設 3× 與跨重啟記住上次倍率的分支已排除。
- 使用者看過純 host 狀態 A／B 原型後，確認未按 Apply 即關閉面板等於取消暫選；
  再開時 `selectedScale` 回到目前 `activeScale`。保留隱藏待套用選取的分支已排除；
  Close／Cancel 仍只由 host 消費，不向 DOS 送鍵或滑鼠事件。
- 不改原版 EXE、DOS 輸入、原版手冊驗證、存檔結構、遊戲規則或 adapter 的 exact output identity。

### Linux Ebitengine 後端的可丟棄驗證

2026-09-22 在既有 `eob-remake-go:1.26.7-ebiten2.9.9` Docker image、`--network none`
與 Xvfb 中，可丟棄 Ebitengine 2.9.9 原型已將 320×200 logical 畫布開成 960×600
的 3× 視窗，三次更新後正常結束；暫存原型已清理。這只證明 Linux 視窗後端
可啟動，沒有連接 dosgolem、輸入分流、繁中覆繪或設定面板。Ebitengine 的
[官方功能矩陣](https://ebitengine.org/en/documents/features.html)列出 Linux、
Windows 與 macOS 的視窗／鍵盤／滑鼠能力；[安裝說明](https://ebitengine.org/en/documents/install.html)
指出目前桌面標準後端仍需 X11／XWayland 與圖形驅動。SDL3 可作替代，
但[官方建置文件](https://wiki.libsdl.org/SDL3/README-cmake)顯示須另處理 CMake／
平台工具鏈；本專案目前沒有已驗證的 SDL3 Go 綁定或專用 image。Ebitengine
較快接通原是工程建議；使用者其後明確選定 Go／Ebitengine 作為 dosgolem
畫面前端，SDL3 分支已排除。原型仍不足以把本規格升為 READY。

## 2026-09-22 有界 READY 審查

本次將可由通用 API 獨立證實的兩個小邊界收斂為本機 dosgolem 分支的
`docs/spec/226-host-machine-presentation-bridge.md`：

1. `MachineFrameSource` 在與 `Machine.Step` 相同 goroutine 中，從 `VideoSize`、`Indexed` 與
   `Palette` 建立 `host.FrameSource`；indexed 是 machine 回傳複本、palette 是值，之後仍由
   `PresentationSnapshotProvider` 複製。這不跨執行緒，也不含 active xlate layer。
2. `KeyboardBridge` 只接收已由未來視窗後端映射的 DOS scan code；它先以
   `PanelController` 決定是否可送，面板開啟時不改 machine keyboard queue，關閉時才明示呼叫
   `QueueKey`。它不處理 pointer、mouse 或 Ebitengine 的 key mapping。

第一百一十六階段已以私有原版 state 在 Docker／Xvfb 驗證真實 Machine step→snapshot→Draw、
2×／Cancel／Apply 與 BIOS key forwarding；完整 receipt 見 `docs/re/phase-116-game-loaded-ebiten-prototype.md`。
該原型的 `active_layer_connected=false`，故不能單獨當成繁中 active layer 或完整可玩版。

其後本機 dosgolem `docs/spec/227-host-active-layer-snapshot-core.md` 已 CONFORM 純 projection：
它將已由 lifecycle owner 定色的 active stamps clone 後繪製，保證 presenter 不改原 layer。
第一百二十階段進一步在同一 machine-stepping Ebitengine thread，將真實首屏 story watcher 的
private active layer 接入這個 projection。指定 private state 中，host 的 2×、暫選 3×後 Cancel
回到 2×，以及 Apply 3×後，RGBA 都逐像素等於第一百一十五階段 CLI 收據；host 操作前後 raw
indexed SHA-256 相同。3×會重建**僅 output-side**的 22×22 story presenter 與其 font registry，
不會把 2× 16×16 font 稀疏放大，也不會 Step／寫入 DOS。完整限定證據見
`docs/re/phase-120-game-active-story-layer-prototype.md`。

上述是 ignored prototype 的窄範圍證據，並沒有把本規格升為 READY。正式前端仍有下列最小缺口：

第一百二十五階段的 Docker/Xvfb prototype 已由真實 Ebitengine pointer／Enter 事件驗證：暫選 3×後
Cancel 會回到 2×且重開仍顯示 2×；再次選 3×後 Apply 收合並切至 3×。host hit 與面板開啟時鍵盤均不改
BIOS queue、IRQ、raw indexed VRAM 或 DOS mouse，關閉後 Enter 才排入已證實 BIOS key。這仍是 ignored
prototype evidence；未命中 pointer 不轉 DOS mouse 只是安全 fallback，並非正式 UX 決定。

使用者現已定案 pointer route：面板**關閉**時，host chrome 外、canvas 內的 pointer click 必須轉送
原版 DOS mouse；面板**開啟**時所有 pointer（含 panel 外 miss）均由 host 消費。排除「關閉時永不
轉送」方案。此決定只固定 route，尚未證實任一遊戲狀態的可見遊戲效果。

MouseBridge 的 READY 候選邊界為：source 是 Ebitengine logical canvas 的 pointer down／up，destination
是既有 DOS `MoveMouse`／`PressMouse`／`ReleaseMouse`；bridge 只在 closed panel、canvas rect 內工作，
不得把 host chrome／panel 座標交給 DOS，不 Step machine、不製造 keyboard IRQ。2×／3×的座標換算、
canvas 邊界、left button down/up 順序與拒絕無效按鍵須由純核心測試釘住。phase127 只證實 state mutation，
尚未 Step，不能當玩家可見效果收據。使用者其後也決定：只有關面板且畫布內的 Left Down
能建立新的 DOS 按鍵狀態；已轉送 Down 的 Up 若在畫布外、控制列、開啟面板或視窗失焦，
仍須只呼叫一次 `ReleaseMouse(0)`，不移動最後有效 DOS 座標；無配對或重複 Up 不送 DOS。
本地 dosgolem 分支的 `docs/spec/228-host-mouse-bridge-ready-candidate.md` 當時保存 DRAFT 契約與
純 fake prototype 驗證；後續限縮符合性結果見本規格最末的現況勘誤。
ignored `workplace/phase128-mousebridge-prototype/bridge.go` 曾對畫布內配對 Up
也只 Release、不 Move；已在可丟棄純核心修正為 closed-canvas 內
`Move→Release`、外部／panel／失焦只 Release，雙倍率四角與邊界 fake 測試通過。
這在當時不等於真實 Ebitengine／dosgolem 事件矩陣已通過；後續已補實體
畫布內 Up 的座標、呼叫順序與固定 checkpoint 因果收據，見本規格最末現況勘誤。

[第一百五十四階段](../re/phase-154-ebiten-panel-pointer-miss-prototype.md)再以真實
Ebitengine 2×／3×驗得閉面板畫布轉送及面板開啟時三種 pointer hit／miss
對 DOS 零呼叫；雙倍率畫布外、控制列、面板、失焦的已接受 Down 清理也
均只 Release、不 Move。這仍是 ignored 原型。正式 `PanelController` 在
開面板空白 miss 目前回 `{consumed:false,forward:false}`，僅原型局部政策
補成消費；正式接線前須令整體 host route 在面板開啟時直接保證
`{consumed:true,forward:false}`，並以測試固定。面板展開造成的座標
重映射不得將已按下的 host target 的 Up 轉送 DOS。這些是已定決策的
實作契約，不是新增的遊戲輸入行為。

[第一百四十六階段](../re/phase-146-real-ebiten-inside-up-corrected.md)已以修正後原型
重跑真實 Ebitengine 2×／3×畫布內 Down→Up；兩倍率均觀測到
`Move→Press→Move→Release`，DOS button 清除，輸入 API 邊界的 BIOS／IRQ／indexed
與 memory 不變。這在當時只補上述畫布內 Up 呼叫順序；後續 spec228 的限縮結果
另見下節，**本規格 004** 仍維持 DRAFT。

1. Linux Ebitengine 後端的正式事件接線：將 prototype host chrome hit test、面板鍵盤隔離、Ebitengine key 到
   DOS scan code 的明示映射，以及已定案的畫布 pointer forwarding 接到正式玩家視窗。
2. 從遊戲開機到故事 state 的完整正常玩家路徑，以及 host 操作後繼續遊玩、存檔／讀檔的同狀態
   收據；第一百二十階段的受控 direct host events 不可替代它。
3. 同一套 active-layer scale-switch lifecycle 對其他已接／未接 Buck Rogers overlay 的資料治理與
   正常玩家路徑驗收；不得以首屏五行的成功外推全部繁中路徑。

第 226 號規格僅為純核心 CONFORMED；它沒有把本規格升為 READY，也不構成可玩的 frontend。

## READY 前置與未來驗收

進入實作前，必須依已選定的 Linux／Ebitengine、C 語意、面板焦點隔離及 session-only
倍率、2× 啟動預設及未 Apply 的取消語意，補齊 host 文案／字型的實際視覺驗證與事件接線。
READY 後至少驗證：

1. 2×與3×的 host canvas 與控制列幾何；畫布內容逐 byte 等於同一 raw input 的輸出投影。
2. 每個 host hit event 對 DOS mouse state、BIOS key queue、IRQ、raw framebuffer、DOS memory
   與存檔均為零副作用。
3. 切換前後以相同 raw input、palette 與 active layer 重繪；繁中 stamps 不遺失，且不新增
   原版輸入或重啟。
4. 以至少一條正常玩家路徑做原文／繁中、2×／3×與切換前後的同狀態收據；差異只在核准的
   presentation pixels 與 host chrome 範圍。

在上述項目完成前，本規格維持 DRAFT，不能作為 production 視窗前端或手冊 presenter 的許可。

## 2026-09-23：MouseBridge 限縮符合性現況勘誤

本機 dosgolem `host.MouseBridge` 已依獨立審查的 spec228 限縮 READY 實作，並以
正式程式連接 ignored Ebitengine/Xvfb harness，完成 320×200 的 2×／3×同 state
無滑鼠控制組與畫布點擊 A/B，以及 2×畫布外、面板、失焦的 release-only 清理。
七份正式收據在 DOS API 與完整 phase 欄位逐項等於舊原型，來源雜湊與未驗停止線見
[第一百七十九階段](../re/phase-179-formal-mousebridge-conformance.md)。
因此 spec228 **僅此範圍限縮 CONFORMED**；前文關於 spec228「仍 DRAFT」的段落是
早期證據狀態，不再代表此元件現況。

這沒有接通正式 Linux 玩家視窗，也沒有關閉本規格的 Ebitengine hit-test、
鍵盤映射、active-layer 全路徑、完整開機或存讀檔驗收。3× cleanup 與實體
right／bottom exclusive 邊界亦未由這批正式收據驗證。**spec004 整體仍 DRAFT。**

## 2026-09-23：真實繁中層與通用 Game 的 DRAFT 接線現況

[第一百八十五階段](../re/phase-185-ebiten-real-active-layer-router-draft.md)已在
ignored caller 從合法私有 checkpoint 取得首屏五行真實繁中作用層，再接入
本機 fork 的 `frontend/ebiten.Game`。實體 X11 滑鼠完成 2×→3× Apply，
畫格期間原版持續 Step；兩倍率畫布 RGBA 與既有 CLI 收據逐位元組相同。
這訂正本規格早期「所有實體視窗原型都是空 active layer」的現況，
但不使 caller 成為正式玩家程式。完整冷開機、手冊、存讀檔、其他覆繪生命週期
及相同 step 的 DOS A/B 仍未驗；本規格保持 **DRAFT**。

### 已確認：設定面板展開時暫停 DOS CPU

使用者於 2026-09-23 確認：正式 Linux 可玩版的設定面板開啟期間，
不只攔截送往原版的鍵盤與滑鼠，也**暫停 DOS CPU Step**；面板關閉
或按 Apply 自動收合後才恢復。排除 ignored 原型目前「面板開著仍呼叫
`Advance`」的行為。這只控制 host 的 instruction 排程，不改原版 EXE、
虛擬時間或遊戲規則；暫停期間可重畫既有 snapshot 與 host 面板，
但不可消費原版輸入、推進 watcher 或改 DOS 狀態。故 READY 驗收需含：
面板開啟前後的 step／DOS state 錨點、選項暫選與 Cancel、Apply 收合，
以及恢復後第一個有界回合；任一面板展開回合均不得 Step。
這是使用者決策，不表示上述生命週期已正式實作或驗收；規格仍 DRAFT。

### 暫停／恢復的實體 DRAFT 收據

[第一百八十九階段](../re/phase-189-ebiten-panel-pause-resume-draft.md)已在 ignored
caller 以真實 Ebitengine/X11 點擊驗證 Cancel 與 Apply：面板展開 89 個更新回合
沒有 DOS Step，收合同回合也略過，下一個關閉回合各恢復 16 步；首屏五行
繁中在 2×／3× 仍與既有 CLI 私有 RGBA 收據逐位元組相等。這只是
`-router-pause-draft` 的排程原型；正式 `frontend/ebiten.Game` 未改，
冷開機、完整 DOS 狀態 A/B、存讀檔和其他輸出路徑仍待 READY 後實作與驗證。

### 正式 session 的 API 缺口

[第一百九十階段](../re/phase-190-linux-frontend-session-ready-prerequisites.md)
對目前 fork API 的唯讀稽核確認：`Game.Advance func() error` 沒有 instruction
budget、step receipt 或 session phase；`Update` 也不保證面板 Open／Select／
Cancel／Apply 回合零 Step。正式 cold-boot preflight、多繁中作用層聚合、
錯誤 teardown 與 `Close` 責任仍未成為 typed contract。此結論只描述
固定 commit 的前端 API，沒有否定既有可丟棄真實視窗收據；本規格仍 DRAFT。
