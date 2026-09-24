# 004 — dosgolem host 前端與執行期倍率

狀態：DRAFT（正式面板暫停 `Advance` 呼叫排程另有局部 CONFORMED）

2026-09-24 多作用層前置：[第二百二十階段](../re/phase-220-linux-active-composite-draft.md)
用不載原版的可丟棄 evaluator 驗得「一次 indexed／palette 讀取、固定
z-order、完整群組、同 generation、缺字不交付局部 RGBA」的最小候選。
正式 `LayerSnapshotProvider` 仍只接受單一 layer；手冊正文實際已有背景與
文字雙層。真實 presenter 並存、失效／還原與玩家路徑未驗，故本規格仍
DRAFT，不授權把該 evaluator 接入正式前端。

2026-09-24 3× host 字型前置：[第二百一十二階段](../re/phase-212-host-only-3x-eten-font-ab-draft.md)
已用不載原版的並列原型核對原生倚天 24 點與既有原型 22 點，
均不缺字且在 host 控制項矩形內；24→22 直接裁切會損筆畫。
使用者現已選擇 A：3× 設定面板使用倚天原生 24 點，排除 22 點衍生原型。
後續本機 dosgolem fork `cc0b17a` 已將正式 `Game.New`／`Draw` 改接
24×24 Wide＋16×24 ASCII；[第二百一十二階段後續收據](../re/phase-212-host-only-3x-eten-font-ab-draft.md#2026-09-24-a-原生字型正式畫筆的本機限縮收據)
在合成畫布的真實 Ebitengine 畫格驗 3× Apply、五標籤像素與
2× 往返。原版 DOS／存檔同狀態與正常玩家入口仍未驗，
字型子契約保持限縮 READY，本規格整體維持 DRAFT。

後續本機 dosgolem fork `f51c455` 增加 `LoadHostFont3`：由外部明示
兩份本機子集路徑與 SHA-256，對同一次讀入的 bytes 驗雜湊並解析，
再檢查 24×24 Wide、16×24 ASCII、必需字模與安全矩形；舊 22 點、
缺字、替換檔及畸形檔皆失敗即關閉。合成負例與本機倚天子集測試
通過；**正式 Linux 啟動器尚未提供這兩份來源並接入 Game.New**，
因此這是已完成的載入元件，不是可玩前端的來源前檢驗收。
本機 fork `e471bcb` 另使 `Game.New` 在驗證後深複製 2×／3×
字模；呼叫者後續修改來源 map／字模 bytes 不再改變正在顯示的
host 標籤。定向測試、前端／橋接／呈現套件測試與競態測試已通過；
此為已驗字型來源身分的元件保護，不能代替正式啟動器的來源核驗。
同一 fork `b908226` 後續新增 `LoadHostFont2`：要求呼叫者提供本機 16×16
子集路徑與預期 SHA-256，對同一份已雜湊 bytes 解析，再驗證五個
host 標籤的字模與安全矩形。合成負例及現有本機 2× 子集測試通過；
它不改 2× 字距、字形或畫筆。兩種字型各有可版控的本機
重建工具與來源雜湊收據；**正式啟動器**尚未讀取經審的 manifest
並接入 2×／3× 雙載入器，不能以元件測試宣稱
冷開機可玩或原版同狀態。
後續[第二百二十二階段新增收據](../re/phase-222-original-menu-3x-typography-draft.md#2026-09-24-倚天-host-字型先驗後冷開機重跑)
只在 ignored 原版實體視窗原型中，先以兩個正式 loader 驗本機
2×／3× 字型，才從第零步建立 DOS machine；2×→3× Apply 後
仍在同一 machine 繼續前進。此為正式啟動器來源前檢的可行性
證據，**不是**規格 004／019 已 READY 或可玩版已交付。

## 3× host 字型限縮 READY：倚天原生 24 點

狀態：**限縮 READY；僅授權本節的 3× host 字型接線，004 整體仍 DRAFT。**
[獨立證據審查](../re/phase-212-host-only-3x-eten-font-ab-draft.md#2026-09-24-獨立-ready-審查)
已核對 A 版原型收據雜湊、正式 `Game.New`／`drawText` 與 `xlate.LoadFont`
的現行能力；審查當時尚未取得正式 3× Apply 或完整玩家路徑收據。
使用者在 phase212 A/B 並列原型後選擇 A：3× 設定面板中文字與全形
符號使用倚天原生 24×24、ASCII 數字使用原生 16×24；B 的 16→22
衍生字型及把 24×24 裁成 22×22 均排除。此決定只及於 host 控制列
與設定面板，不改遊戲畫布、繁中覆繪字型、輸入、規則或存檔。

證據等級與輸入：phase212 的 ignored host-only 收據記錄九個相異
標籤字元均有墨跡，A 五項文字的 advance 與實際墨跡均位於既有
控制項安全矩形；直接裁切 24→22 的九種整數偏移都損筆畫，最好
偏移仍合計少 57 點。這是**已證實的本機字型／幾何原型**，不是
正式 `Game.New`、3× Apply、真實視窗或原版畫面收據。來源是使用者
本機 `ET353S/FILES/STD.24M`（SHA-256
`347ae2655807fc250a18673e6634a363dfba7feee6c3355b886a0810d2d9c030`）、
`SPCFONT.24`（`da7574d2eee10b9d3b2a2d90bbc39e2ba482b9b2b73a9803f1e4dbefdd91a92a`）
與 `ASCFONT.24`（`7e69f74bfedf57579fad41a1bc2f0c3a6da873cba1734fd30a1c4afc64893ada`）；
解壓器與產物雜湊見[phase212 審查紀錄](../re/phase-212-host-only-3x-eten-font-ab-draft.md)。
這些檔及抽字所得點陣均只可作本機唯讀輸入／ignored 產物，不能加入
Git、GitHub、公開包或可散布測試語料。

正式 3× host 輸入需能表達兩種**各自有固定字模尺寸**的本機來源，
例如下列 typed view；名稱可調，但不能把混合字寬塞回單一等寬
`xlate.Font{W:22,H:22}`：

```go
type HostFont3 struct {
    Wide  *xlate.Font // 倚天 24×24：標籤中的漢字與「×」
    ASCII *xlate.Font // 倚天 16×24：標籤中的「2」「3」
}
```

兩份本機子集可分別經既有 `xlate.LoadFont` 讀入，但建立者須記錄上列
來源 SHA-256、ETUNPACK 解壓器版本／雜湊、抽字清單及輸出雜湊；
漢字／符號按標籤 Unicode rune → Big5 區段索引抽取，ASCII 按原生
字元索引抽取，不得把自訂碼位直接當 Big5 索引；
`xlate.Font` 的 GOLEMFNT 檔頭只載單一 W／H，來源位元組本身不可
由型別或檔名推定。`Game.New` 在任何 Draw 前失敗即關閉地驗證：
Wide 為 24×24、ASCII 為 16×24；每個標籤 rune 僅按既定分類取
指定來源，存在、列長為 72／48 bytes、至少有一個墨點；不得
缺字 fallback、縮放、裁切或把衍生 22 點冒稱原生。來源身分另以
本機輸入雜湊與可重建流程核對；單看 `W`／`H` 不能驗證字形出處。
字距（advance）與繪製共用同一個逐字量測器：漢字／「×」每字 24px，
ASCII 數字每字 16px，字模高度一律 24px；`2×`／`3×` 各 40px，
「設定／套用／取消」各 48px。任何後續新增 host 標籤也必須先
驗 coverage、advance、實際墨跡及安全矩形，不能只改文案後讓畫筆裁切。

3× 文字仍以目前 `drawChrome` 的起點與控制項／hit rectangle 作
定位，不移動遊戲畫布：設定 `(744,8)`、`2×` `(36,114)`、`3×`
`(216,114)`、套用 `(450,198)`、取消 `(675,198)`，單位為 3×
output 像素。對應安全矩形依序為 `[732,6,948,45)`、
`[24,105,186,174)`、`[204,105,366,174)`、`[435,189,639,261)`、
`[660,189,864,261)`；量測 advance box 與逐像素 ink box 均須
完整落入各自矩形，左右與上下都檢查。phase212 A 的右邊界分別
為 792、76、256、498、723，均小於安全矩形右界；這只是
host-only 原型收據，正式畫筆要重測相同幾何。

2× `HostFont2` 繼續使用現有 16×16 等寬 `xlate.Font`、每字
advance 16 與既有驗證／畫筆；切到 3× 再返回 2×，2× 標籤與
控制項像素、hit rectangle、畫布 origin 應與切換前一致。不得
為了共用 3× 混合字寬而改動 2× 的字距或字型來源。

接線前的 `frontend/ebiten/game.go` 使用單一 `*xlate.Font` 作為
`Config.HostFont3`，3× 驗證固定 22×22、`drawText` 每字增加
`font.W`；此為當時的差距，不是現況。上文所記本機 fork
`cc0b17a` 已新增 3× 專用 typed view 與逐字驗證／量測／繪製選字；
`HostFont2` 及 2× 分支維持原契約。
本機載入端須以三份原生來源建立兩份僅含 host 標籤的子集，
將 Wide／ASCII 注入 `Config`；不在正式程式內硬編私有字型路徑、
攜帶字模或把字型嵌進二進位。3× 啟用前若任一來源缺席、雜湊不符、
解壓／抽字失敗、尺寸／列長錯誤、缺字或超出安全矩形，應回明確
錯誤且不得以 22 點原型或 2× 拉伸字型靜默代替。

Docker 驗收矩陣（限縮實作後逐項驗證）：

| 條件 | 必要結果 |
| --- | --- |
| 無私有來源的合成 24／16 點 glyph | 3× validator、逐字 advance 與安全矩形正例；尺寸 22、錯列長、空白或漏一字均在 `Game.New` 前拒絕，不需原版素材。 |
| 已鎖雜湊的本機三份倚天來源 | 在有界、無網路 Docker 內唯讀掛載並重建兩份 ignored 子集；量到九字 coverage、24／16×24 來源、40／48px advance、逐像素 ink containment，輸出可重播雜湊。 |
| 正式 3× `Game.New`、Open／Select／Apply／Cancel | 本機 Docker／Xvfb 以正式 adapter 跑實際 3× Apply 與返回 2×，檢查文字未裁切、控制項點擊／焦點、面板回合零 `Advance`，並保存有界畫面與步數收據。 |
| 同一初始狀態的 2× 基線及 2×→3×→2× | 2× 標籤／控制項與畫布像素不變，DOS raw indexed、BIOS／IRQ／mouse、存檔不因純倍率切換而改；未完成正常玩家路徑不得聲稱整體前端符合。 |
| 缺少本機字型或公開工作樹檢查 | 正式啟動明確拒絕 3× 必需字型、無 22 點 fallback；Git／封包不含原生字型、GOLEMFNT 子集、字形圖或可還原素材。 |

所有原型、截圖與本機子集留在 ignored `workplace/`。這份限縮
字型契約不解決規格 004 的 cold boot、session、原版同狀態或
完整玩家路徑；只有上列限縮範圍升 READY，未通過其正式驗收前不得稱 CONFORMED。

2026-09-24 實體 live-turn 原型：[第二百零九階段](../re/phase-209-cold-boot-live-ebiten-panel-pause-draft.md)
從第零步到選單後，正式 `frontend/ebiten.Game.Update` 已在 2× X11 視窗
繼續推進同一部 DOS machine；Open／展開／Cancel 收合當回合零步，下一
關閉回合恢復。這補的是單次原型步數收據，**不**涵蓋 3×、完整狀態
A/B、其他作用層、存讀檔或正式 typed session，本規格仍 DRAFT。

2026-09-24 冷開機原型：[第二百零八階段](../re/phase-208-cold-boot-menu-ebiten-prototype-draft.md)
已從原版 `START.EXE` 第零步跑到首個已量選單，並以 Ebitengine 顯示
繁中終態；然而 DOS 在開窗前已推進完畢，視窗只重畫靜態影格，沒有 live
玩家輸入、host 面板或正式 session。故此原型補上冷開機可達性證據，
不使本規格 READY，也不取代以下完整前端驗收。

2026-09-24 Issue #18 進度：[第二百零三階段](../re/phase-203-linux-session-mixed-batch-fake-review.md)
補齊可丟棄 session fake 的 Open／Apply／Cancel＋Enter 混合批次隔離；
這只涉及 host 回合候選鍵，不涵蓋 cold-boot preflight、observer 安裝、
多作用層、實際 DOS 指令收據或正常玩家路徑，本規格整體仍 DRAFT。

2026-09-24 補充：[第一百九十六階段](../re/phase-196-ebiten-panel-batch-keyboard-gate.md)
另將正式 `Game.Update` 的 Apply／Cancel 同批鍵盤隔離限縮驗收；
面板起點開啟時，即使同批收合，也不把該批鍵盤送入 DOS。
這仍不是 typed session、實體 X11 同批事件或可玩前端驗收。

2026-09-24 現況勘誤：[第一百九十四階段](../re/phase-194-formal-ebiten-panel-pause-conformance.md)
已以本機 dosgolem `docs/spec/231-linux-ebiten-panel-pause-gate.md` 的 READY→實作→
驗收流程，證實正式 `Game.Update` 在面板展開、Open／Select／Cancel／Apply
及收合同回合均不呼叫注入的 `Advance`，下一個關閉回合恢復。這**只**是 callback
排程，不是原版 DOS 指令或完整 machine／DOS 同狀態收據；冷開機 session、
多作用層、存讀檔與可玩玩家入口仍保持 DRAFT。後文較早的「正式 `Game.Update`
仍無條件呼叫 `Advance`」描述是修正前的歷史觀測，不再代表目前程式。

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
- 3× 面板的中文字型已選 A：倚天原生 24 點；不得以裁切 24→22 或既有
  16→22 衍生原型冒充正式字型。2× 已確認的字距與外觀不隨此決定更動。
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

## 2026-09-24：session-turn 限縮 READY 候選交接

[規格 019](019-linux-frontend-session-turn-boundary-draft.md)現將同批事件的
固定處理順序、接納批次 epoch、正預算／實際 machine step 嘗試差分、
DOS 退出與 raw stop／error 優先序，以及 `Draw` 同步故障通知唯一
session owner 的責任寫成**待獨立審查的限縮 READY 候選**。
[Issue #18 審查紀錄](../re/issue-18-session-turn-ready-candidate-review.md)
列出目前正式 API、可丟棄 fake 及合成 COM 的證據界線。
規格 019 尚未獲獨立 READY 審查；本規格 004 的原版根／存檔根
preflight、observer 安裝、多作用層、正常玩家路徑與存讀檔仍待補，
故本規格整體維持 **DRAFT**，現有 `Game` 亦非正式 cold-boot session。

## 2026-09-24：3× 遊戲畫布字距訂正候選（DRAFT）

使用者先前已確認 2× 繁中字距合適，3× 中文需要更大、更緊密；
3× host 面板另已選定倚天原生 24 點 A 版。兩者是不同字型路徑，
不可因 host 面板完成而宣稱遊戲畫布的 3× 字距也已修好。

[第二百二十二階段](../re/phase-222-original-menu-3x-typography-draft.md)
從原版冷開機功能選單取得實體 2×→3× Apply 與純畫布 A/B：
正式 menu 覆繪目前在 24×24 輸出 cell 中置中 16×16 字模，
外框相鄰間隔 8 像素，與 3× 中文較鬆的目視結果一致。可丟棄
22×22 最近鄰衍生字模置中後，間隔降為 2 像素，兩版在同一
indexed／palette 下只有核准選單文字矩形內不同；它並未修改
正式程式。2× 應保持現行 16×16 與既有收據逐 byte 相同。

**本節僅為 DRAFT 候選**：若獨立審查採用 3× 22 點，須先把
倚天來源、衍生演算法版本、字元覆蓋、24×24 cell 幾何、所有正式
選單變體的行寬／清除／顏色、快捷取字母白色及原版語意不變寫成
限縮 READY；之後才可修改 `apps/buckrogers` 正式字型接線，並以
原版 control／2×／3× 同狀態和真實視窗回切驗收。單一主選單截圖
不能取代全遊戲其他文字路徑或 Linux session 原子輸入的驗收。

後續[第二百二十二階段原版 Down→Up 收據](../re/phase-222-original-menu-3x-typography-draft.md)
補上 normal／selected 轉場：兩停點的 2× 候選與正式畫面逐 byte
相同，3× 可丟棄 22 點與現行 16 點的差異只在核准 active 選單
矩形。這足以提出**限功能主選單**的 3× 字型 READY 審查，尚未
定稿正式 font identity、共用 `RuntimeMenuOverlay` 的事件分流或
長存層驗收，故本節仍 DRAFT。`RuntimeMenuOverlay` 也供 race 等
介面使用；不得把主選單結果無條件套到所有呼叫者。

獨立 READY 審查後仍維持 **DRAFT**。主選單僅允許 1 個
`menu.transition.*` 加 9 個 `function.menu.*` 的精確完整鍵值；
`race.*` 等另 11 個 identity、post-join 與偽前綴鍵不得落入
22 點分支。進正式程式前須固定衍生字型 `Name`／registry／
fingerprint／快照還原契約，並在共用 builder 測 16 點原分支及
22 點分支的來源、樣式、倍率、矩形與混合批次失敗即關閉。
原版 Down→Up 不需重複逆向；上述合成規格通過後再安排接線與
同狀態驗收，不把「13 筆譯文」錯算為 13 個事件。

候選十鍵須逐字匹配下列 `text/menu-events.tsv` identity：

```text
menu.transition.old.create_new_character
function.menu.option.create_new_character
function.menu.option.add_character_to_team
function.menu.option.load_saved_game
function.menu.option.joystick_mouse_initialize
function.menu.option.exit_to_dos
function.menu.selected.create_new_character
function.menu.instruction.choose_function
function.menu.selected.add_character_to_team
function.menu.normal.add_character_to_team
```

### 功能主選單 3× 字型限縮契約（限縮 READY）

此契約只處理上述十鍵的**畫布顯示像素**，不動原版 indexed／palette、
輸入、選取狀態、清除事件或字串 identity。原版證據是第二百二十二階段
的冷開機選單及 Down→Up guarded post-call；來源是本機倚天子集
`GOLEMFNT` SHA-256
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`，
由全部正式 TSV 和三個固定倚天檔重建，僅留 ignored `workplace/`。
輸出演算法版本暫定 `buckrogers.menu.eten22.v1`：每個漢字／非 ASCII
字模由 16×16 以整數最近鄰取樣為 22×22；U+0000–U+00FF 字模
保持 16×16，置中於 22×22 的 (3,3)。3× 的 24×24 cell 內
使用 (1,1) 墨跡偏移、`GlyphScale=1`，不改 8×8 邏輯格與文字
安全矩形。2× 完全沿用現行 16×16 產物。

正式實作須保留現有 `BuildMenuOverlay` 的 16 點 API 與既有 caller：
另設明示啟用的 3× 主選單 builder，**對傳入該 builder 的一整批**
必須全部是上列完整鍵值；混入 `race.*`、post-join 或偽前綴時
整批拒絕。新增的 scoped runtime 入口須持有由固定
`menu-events.tsv` 與 `menu.zh-TW.tsv` 載入的 canonical
`MenuCatalog`、原 16 點字型與一次衍生的 22 點字型。
`RuntimeMenuOverlay.Apply` 是逐**單事件**呼叫：先對原
`TextEvent` 重做 `MenuCatalog.Resolve`，要求所得 `EventKey`／
`TextKey`／`Translation` 與傳入 `DisplayRequest` 完全相同；
未經 canonical Resolve 的任意 request 不得藉偽造十鍵取得
22 點。`scale=3` 且精確命中十鍵才選新 builder；已知的 11 個
`race.*` 在同一 runtime 前後出現時仍走舊 16 點 builder，
不可因先前主選單事件而拒絕整段 runtime。post-join 使用自己的
presenter；不在本分支的事件若缺正式 catalog／矩形，仍依原失敗
規則拒絕，不得由模糊前綴路由。
建立衍生字型前，先對來源**全部** glyph 驗 `16×16` 與 32 bytes，
不可只驗本次譯文引用者；衍生後全表驗 `22×22` 與 66 bytes、
完全同一 rune 集及版本化演算法逐 byte 相等。新分支只接受
`scale=3`，來源或輸出不符、缺字、樣式／容量／幾何錯誤、重疊或
任一筆墨跡越界，一律回 `nil,error`，不得留下半批作用層。
現有 16 點 builder 接受未引用壞字模與 4× 是已觀測 API 邊界，
不能把它們誤當新分支的核准值，也不在本項順手改舊 caller。
builder 的整批拒絕只約束**單次 builder 呼叫**；逐次 `Apply`
各自原子。後筆錯誤不回滾已成功前筆，但不可交付「看似成功」
的半更新影格：錯誤須傳回上層 session owner，由它停止新影格
交付並使該回合失效。若日後提供多事件合併更新，須先全批
stage／驗證才發布，不能沿用單筆原子性作跨筆保證。

衍生字型的正式 `Name` 固定為上述演算法版本字串；同一
`RuntimeMenuOverlay` 生命週期只建立一次字型物件，將其完整 bytes
計算 `FontFingerprint`，以該**相同指標**註冊至封存 registry。
`WithSealedOrderedLayers` 在封存時驗精確指標、名稱與 fingerprint；
但原始 `xlate.Layer.Snapshot` 只記 `Font.Name`，普通 `Restore`
只按名稱查 registry，**不會**驗指標或 fingerprint。正式還原
不能單靠 `Restore` 的成功值：同一 session 的 owner 必須先核對
來源 GOLEMFNT 固定 SHA-256、已複製並固定的來源物件、來源及
衍生 `FontFingerprint` 與同一 registry，然後才還原及封存供畫面
讀取。空名、同名不同指標、鍵名不一致、缺 registry 或指紋漂移
在**封存 owner 流程**均須失敗即關閉；snapshot／restore 後 stamp
身分與 RGBA 須逐 byte 同值。跨 session 持久化還原不在本子契約；
若將來支援，須把指紋寫入 snapshot metadata 並獨立驗收。
實際 fingerprint 值隨正式 catalog 字元聯集記入同次收據；不能
拿本次 test-only `draft.menu.derived-22` 指紋當永久正式值。

READY 後的實作驗收：正式 runtime 十鍵、11 個 race 鍵及至少一個
post-join／偽前綴負例；2× 全 RGBA 與舊版逐 byte 同值，3× 只十鍵
在各自核准文字矩形內有差，選取／指示列 BG／FG 和原版文字生命週期
不變。再以相同原版 state、同輸入的 control／2×／3× 重播與真正
Ebitengine 視窗反覆 2×→3×→2× 驗收；正常玩家入口、存讀檔與
整體 Linux session 的 #18 原子輸入另行驗收，不因本子契約過關
而宣稱完整前端可玩。

獨立審查已核對原版正常／反白 Down→Up、十鍵 exact 合成範圍、
19 種失敗矩陣與正式 `RuntimeMenuOverlay`／`xlate` API，並在補明
canonical Resolve、逐事件／批次分界及同 session 字型 owner 後，
將**本子契約限縮升為 READY**。它授權依上述條款修改正式
`apps/buckrogers` 3× 主選單字型路徑；正式分支、`Name`、registry、
同狀態與真正視窗驗收尚未完成，所以不是 CONFORMED。規格 004
其他 Linux 前端／session 範圍仍為 DRAFT，不能外推。

實作進度（2026-09-24）：本機 dosgolem 分支 `3b02f88` 已接上述
十鍵限縮 runtime，正式套件測試與同原版 checkpoint 的 Down→Up
四模式收據見[第二百二十二階段](../re/phase-222-original-menu-3x-typography-draft.md)。
2× 與舊版逐 byte 相同，3× 差異限核准矩形；但 CLI 終態錨定影格
及實體 Ebitengine 2×→3×→2× 回切未過驗收。因此本子契約仍是
**READY，非 CONFORMED**，其餘規格仍 DRAFT。

限縮實體視窗補驗（2026-09-24）：上述正式 scoped runtime 已在
原版 checkpoint 選單狀態經真正 Ebitengine 視窗完成 2×→3×→2×；
面板回合零 DOS 步、2× 往返 RGBA 同值、3× 差異限核准矩形，
見[第二百二十二階段](../re/phase-222-original-menu-3x-typography-draft.md)。
測試以既有原版事件預先建置 3× 作用層，再由視窗切換 snapshot，
不是完整 #18 session；CLI 終態覆繪收據仍失敗。因此此子契約
依舊 **READY，非 CONFORMED**。
