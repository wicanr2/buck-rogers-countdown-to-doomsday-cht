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

1. Linux Ebitengine 後端的正式事件接線：host chrome hit test、面板鍵盤隔離、Ebitengine key 到
   DOS scan code 的明示映射，以及未命中 pointer 的 mouse forwarding 決定。
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
