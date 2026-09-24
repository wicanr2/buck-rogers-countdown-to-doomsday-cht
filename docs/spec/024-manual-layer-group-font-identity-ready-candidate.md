# 024 — 手冊背景／正文作用層群組與字型身分

狀態：**READY（限手冊背景／正文封存投影與字型身分）**。只授權下文的
無別名、同 goroutine 正式元件實作；正式 Linux session 接線、原版同狀態
與玩家路徑仍未 CONFORMED。下方較早的 DRAFT 審查節保留為歷史證據；
以末節「限縮 READY 定案」為目前契約，不把舊缺口誤認為仍未處理。

## 範圍與已證實事實

本文件只追蹤 Linux presentation 如何讀取既有手冊覆繪；不改題目、catalog、watcher、
原版輸入、DOS 狀態、倍率 UI、session/source-token 或 row 15／row 24。

固定程式身分是本機 dosgolem fork `buck-rogers-cht-output-overlay`
`cc0b17ac92b1e3aea8ff676936684ddcf8064594`。

| 結論 | 等級 | 可回查證據 |
| --- | --- | --- |
| `RuntimeManualOverlay` 有 320×200 的 `background` 與 `text`，`Draw` 固定 background→text | 已證實 | `apps/buckrogers/manual_overlay_runtime.go` 的 `resetLayers`、`build`、`Draw` |
| `Clear` 會重設兩 layer，但不遞增或歸零 `generation` | 已證實 | 同檔 `Apply`、本文件 ignored 反證測試 |
| `manualThreeXFont` 產生 22×22 衍生字型且 `Name==""` | 已證實 | 同檔 `manualThreeXFont` |
| `LayerSnapshotProvider` 只收一個 layer，且在讀取 frame **後**才驗 layer；具 font 的 stamp 要求命名及 exact-pointer registry | 已證實 | `presentation/layer_snapshot.go` |
| 單獨 text 投影不等於 presenter；背景／正文私有 clone 依序畫才逐 byte 相同 | 已證實，限無原版合成 | ignored `manual_composite_draft_test.go` |

原版、手冊掃描、倚天字型、state 與畫面均非本 DRAFT 的輸入，且未寫入版控。

## 已推翻的早期候選

先前版本錯把 `[]ManualPresentationLayer` 中公開的 `*xlate.Layer` 稱為 immutable；它們是可變
別名，呼叫端可在 snapshot 前改 stamp。更嚴重的是，舊 group 在 `Clear` 前取得後仍保存舊 layer
指標，而 `ActiveGeneration()` 在 Clear 後仍回舊值。因此只比較 generation、並由呼叫者手動提供
`visible`，會接受 stale group。這不是可安全升 READY 的 API。

同樣地，既有單層 provider 會先 `ReadPresentationFrame`，才檢查 layer；nil stamp 被視為略過，
並未證實群組的 nil stamp、幾何、字模長度、缺 glyph、錯層或錯 registry 可在讀 frame 前拒絕且
零 RGBA。先前對「preflight-before-frame／read-once／零部分 RGBA」的敘述只是目標，不能當成
已驗證能力。

## 待實作的無別名 typed 契約

下一輪若要重提 READY，應採**同 goroutine、立即消費、不可逃逸**的 owner callback；不得回傳
`*xlate.Layer`、`map[string]*xlate.Font` 或可由 frontend 留存的 group。名稱可調整，等價語意如下：

```go
// 只能由擁有 RuntimeManualOverlay 生命週期的 goroutine 呼叫。
// sealed 僅在 callback 動態範圍有效，callback 返回後不可再使用。
type ManualPresentationOwner interface {
    WithSealedManualGroup(func(presentation.SealedLayerGroup) error) error
}

// 欄位不匯出；它只保存兩 layer 的 Snapshot bytes、深複製且不可變的
// font registry、固定 key/generation/z-order，沒有 *xlate.Layer 或 *xlate.Font 別名。
type SealedLayerGroup struct { /* presentation package private fields */ }
```

交易必須在 owner 的同一 goroutine 內完成：owner 先確認 `manualOverlayVisible`、非零 generation、
確切兩 slot（`background=0`、`text=1`），再序列化兩 layer，深複製字型資料與 registry，並在
callback 返回前由通用 projector 做完整 preflight。只有 preflight 成功才呼叫 `ReadPresentationFrame`
一次，接著以 sealed bytes restore 私有 clone，畫 background→text，交付唯一完整 RGBA。Clear、
Begin、Restore 或 discontinuity 不得在這筆交易中插入；它們結束後也沒有可逃逸舊 group 可重畫。

3×字型仍需有版本化身分，但目前只是擬議值：2× `buckrogers.manual.base-16.v1`，3×
`buckrogers.manual.derived-22.v1`。衍生字型不得修改 base；同一 sealed group 的每個 text stamp
必須以 name 找到內容完全相同的私有 registry 項。名稱相同但內容不同、空名稱、2× font 冒充
3×、frontend 依尺寸重造字型都必須拒絕。這項命名尚未由正式 loader 或 provider 採用。

完整 preflight 至少涵蓋 group key／generation／slot 數及順序、canvas 尺寸、nil stamp、font 名稱／
registry／glyph 存在與精確列長、stamp 的 Cells／CellW／CellH／座標及整數溢位。任一失敗須在
frame read 前回錯，沒有 RGBA、沒有部分 layer、沒有 panic。

## 現有無原版反證與缺口

ignored `apps/buckrogers/manual_group_ready_candidate_test.go` 只使用合成 catalog、16×16 glyph 與
320×200 indexed/palette：

| 案例 | 結果與等級 |
| --- | --- |
| 完整 2×／3× clone 的 background→text | 與正式 `Draw` 逐 byte 相同；已證實合成繪製順序，不證明 API 安全。 |
| 3× 未命名字型 | 現行單層 provider 拒絕；已證實。 |
| Clear 後保存舊 group | `ActiveGeneration` 仍相同，舊指標仍可重畫，舊模型會接受；已證實反證。 |
| nil stamp／缺 slot／反序／錯 registry | 僅 test-only DRAFT model 在 source read 前拒絕，計數為零；不代表正式 provider。 |

因此尚未證實：正式 sealed owner、深複製字型、所有 preflight 項目、正式 read-once、真實 watcher
註冊表、手冊與選單／劇情並存、Restore/discontinuity generation owner，以及真實原版 2×／3×
同狀態、冷開機與存讀檔。這些仍由 phase-220、規格 004、Issue #14／#16 追蹤。

下一次 READY 審查前，須先用可丟棄原型與反例把無別名交易、完整前檢、
Clear／Restore 後失效及零部分 RGBA 的契約證據補齊；獨立審查核准
READY **之後**才能修改正式程式。正式元件測試、原版同狀態及玩家路徑
收據屬實作後的 CONFORMED 閘門，不倒置 READY→實作的順序。

## 2026-09-24：封存群組原型補證，仍為 DRAFT

本機 ignored dosgolem fork 中、僅測試用的
`workplace/dosgolem/apps/buckrogers/manual_sealed_owner_projection_draft_test.go`
（SHA-256 `1dbbd0d4d41ee80f22d7bb5de9714b20153020c5901dd445c1a93e4bf75ec4ba`）
以 callback 作用域與退出時撤銷的 lease 限制群組生命週期，封存兩個 layer 的
Snapshot bytes 與深複製字型，並對 slot、字型 registry 及逐字模計算 SHA-256。
同一 owner 的合成 2×／3× 測試證實：背景→正文結果與現有 presenter 逐 byte
一致且只讀一筆影格；nil slot、反序、錯字型、尺寸仍合法的字模竄改、
Clear、模擬 Restore discontinuity 和逸出 callback 的舊群組，都在讀影格前
拒絕，無部分 RGBA。主代理在既有 Go 1.26.7 映像，以唯讀 fork 掛載、
無網路 Docker 重跑 `go test -count=1 -run '^TestDraftSealedManual' -v
./apps/buckrogers` 與 `go vet ./apps/buckrogers`，均通過。

這只證明一種可行的**原型契約**。目前正式 `RuntimeManualOverlay` 沒有
callback-scoped owner 或 Restore/discontinuity 來源；3× 正式字型載入器與
跨 watcher 的群組登錄也不存在。原型內的 3× 命名和 Restore token 是
測試模型，不是已實作功能；還須獨立審查其 race／重入與正式 API 邊界。
所以本規格保持 DRAFT，不准據此接 production 或聲稱手冊已完整中文化。

## 2026-09-24：獨立 READY 審查（限雙層投影／字型身分）

判定：**仍為 DRAFT**。本節只審 `background→text` 的封存投影與 2×／3× 字型身分；
不審原版題目選擇、39 題玩家路徑或手冊存讀檔。依審查時本機 fork
`e05bfd304436001c04cee50b41ea289ac27f22bb` 的正式
`manual_overlay_runtime.go`、`presentation/layer_snapshot.go`、`xlate/layer.go` 與上列
SHA-256 固定的 ignored 原型，獨立在 Go 1.26.7、無網路、唯讀掛載的 Docker 重跑
`go test -race -count=1 -run '^TestDraftSealedManual' -v ./apps/buckrogers` 及
`go vet ./apps/buckrogers`，均通過。`-race` 只涵蓋測試實際建立的 goroutine；
目前兩個案例都沒有併發寫入，不可把綠燈解讀成 owner 可跨 goroutine 使用。

已證實的正例僅是：在目前合成手冊資料、有效 stamp 與字型下，封存後來源字模變動
不改投影，2×／3× 的兩層順序與正式 presenter 逐 byte 相同，且成功時讀一筆影格。
這足以支持收斂 API 形狀，尚不足以授權正式實作。最小阻塞與補證如下：

1. **封存前的失敗即關閉尚未成立。** 原型 `WithGroup` 對來源 layer 直接呼叫
   `Snapshot()`；正式 `xlate.Layer.Snapshot` 會對每個 `Stamps` 元素解參照，
   未先拒絕 `nil`。因此來源含空 stamp 時存在先 panic、後 preflight 的路徑。
   這是原始碼可直接證實的缺口，不是現有「修改已封存群組的 nil slot」負例所涵蓋。
   補證須從 owner **封存前**注入來源 `nil` stamp、非法畫布與失效字型，要求
   不 panic、零影格讀取、零 RGBA；成功路徑仍只讀一筆影格。
2. **名稱尚非可信的字型身分。** 目前原型的 SHA-256 只證明群組在建立 digest
   **之後**沒有被改；它沒有將 `buckrogers.manual.base-16.v1` 與
   `buckrogers.manual.derived-22.v1` 綁到同一份已驗證 base 字型及固定衍生演算法。
   兩份在封存前就不同、但同名且尺寸合法的字模，仍可各自產生自洽 digest。
   READY 前須明定每次 session 唯一的不可變 base 字型登錄、base 內容指紋、
   3× 衍生演算法版本與由該 base 算出的內容指紋；owner 只接受與該登錄**逐 byte**
   相同的字型，不能由 frontend 重建或以名稱／尺寸猜測。負例要以「同名、同尺寸、
   有效列長，但一個 glyph 位元不同」在**封存前**拒絕，並保持零影格讀取與零 RGBA。
3. **交易隔離的具體失敗點尚未補測。** 規格要求同 goroutine 且 Clear／Begin／Restore
   不得插入，但原型只在投影開始前檢查 lease、epoch 與 visible；
   `ReadPresentationFrame` 返回後未再核對 owner token。READY 契約須明定該 frame source
   不得重入 owner；若要容許重入，則讀取返回後、繪製前再核對同一 token，失效即
   回錯且不交付 RGBA。用可使 owner 失效的 frame-source 負例驗證最終失敗點。

前三項只要求可丟棄模型與規格證據；它們不要求先完成正式 Linux 視窗、真實 watcher
或 39 題原版驗收。獨立複審確認後，最多可把「封存兩層、固定字型身分、單次影格投影」
升為限縮 READY，再由正式 owner／projector 實作與同狀態測試進入 CONFORMED；
不得把限縮 READY 外推為手冊玩家路徑或全遊戲中文化完成。

## 2026-09-24：第二次獨立複審與限縮 READY 定案

### 判定、證據與不涵蓋範圍

**READY 僅限可重用的兩層封存投影、手冊 owner 邊界及 session 內字型身分。**
它不是現成的 production API，更不是手冊或遊戲的 CONFORMED 宣稱。此元件的
玩家可見效果限於既有手冊 presenter 已確認的 `[7,312)×[72,184)` 邏輯像素
正文清除區：同一張 320×200 indexed／palette 影格先畫 `background`，再畫 `text`，
倍率只准 2×或3×。原版題目、答案、catalog 查找、文字內容、watcher 判定、
DOS 輸入／狀態／存檔均不得經此元件變更。手冊提示的原版定位與同狀態證據
仍以[規格 005](005-manual-runtime-presenter-draft.md)及其引用收據為準；
本投影元件不解讀原版位址或手冊素材。

獨立審查的本機 fork tracked 程式為
`e05bfd304436001c04cee50b41ea289ac27f22bb`；可丟棄原型
`workplace/dosgolem/apps/buckrogers/manual_sealed_owner_projection_draft_test.go`
SHA-256 為 `eccd78e52eda69460940b21de415114ebfc3a3ff30a68c008882a663ee46962b`。
在 `eob-remake-go:1.26.7-ebiten2.9.9`、無網路、唯讀 fork 的 Docker 中獨立重跑
`go test -race -count=1 -run '^TestDraftSealedManual' -v ./apps/buckrogers`
及 `go vet ./apps/buckrogers`，均通過。這些是**已證實的合成元件證據**：
2×／3× 有效群組與正式 presenter 逐 byte 相同、成功時恰讀一張影格；
原始 nil stamp、封存前同名異字模、封存後篡改、錯 slot、Clear、模擬
Restore、callback 逸出及影格讀取期間失效，都依各案例回錯且不交付部分 RGBA。
`-race` 沒有建立跨 goroutine 的安全保證。可信本機字型**來源**不是這些測試所證實，
而是以下 caller 前置契約；不能把原型自己計出的指紋當成來源真實性證明。

### READY 實作契約

1. **字型輸入與身分。** caller 先以[規格 008](008-eten-top-pad-local-font-builder-draft.md)
   的固定來源 SHA-256、正式 catalog 集合及本機 manifest 驗證 `GOLEMFNT` 的
   SHA-256、16×16 格式、字模數及完整譯文字元覆蓋；缺 manifest、雜湊／catalog
   不合或來源不明時不得建立 owner。它只接受使用者本機合法來源，不把來源、
   manifest 或字模加入公開封包。以下是此前 22 份 catalog 的**歷史**驗證樣本，
   目前 `text/` 已有 24 份繁中 TSV；即使字元聯集未變，也須在正式接線前按
   當次選定的 catalog 重建或重新核對 manifest，不能直接以舊 sidecar 過關：
   `workplace/current-font/buckrogers-eten-top-pad.golemfnt` SHA-256
   `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`，
   sidecar SHA-256 `d9b299b8b63cdd4972061489b89fef7831a1f8bb9ff8db8efdda57cda7a8f76a`；
   後續 catalog 改動須重建並重驗，不得把此樣本雜湊當永久常數。
2. **每次 session 的 canonical 登錄。** 已驗證的 16×16 base 深複製後只登錄一次，
   名稱固定 `buckrogers.manual.base-16.v1`，以排序碼點、尺寸及逐字模 bytes
   產生內容指紋；3× 只能以現行 `manualThreeXFont` 的 v1 演算法從這份 base
   **一次衍生** 22×22 字型，固定名稱
   `buckrogers.manual.derived-22.v1` 並另算內容指紋。此名稱與指紋的組合
   是該 session 的身分；同名不同內容、錯倍率或 frontend 自行重造字型都拒絕。
   現行 `manualThreeXFont` 回傳 `Name==""`，所以正式 3× constructor／loader
   **必須在 `RuntimeManualOverlay.build` 建立 text stamp 之前**完成命名與
   canonical 登錄，不能等 `Snapshot` 後才替 clone 命名：原 layer 的快照
   只記 `Font.Name`，空名稱會遺失字型參照。2× base 也須在建立 stamp 前命名。
3. **owner 的 typed input 與生命週期。** 只有擁有 `RuntimeManualOverlay`
   `Apply`／`Frame` 與 session discontinuity 的同一 goroutine 可呼叫
   `WithSealedManualGroup(callback)`。owner 內部維持非零 generation 及每次
   Begin／Clear／Restore／stop 都會失效的 epoch／source token；只有
   `manualOverlayVisible` 且兩層已對同一 indexed／palette 執行 `Frame` 後可封存。
   先檢查來源 layer 非 nil、320×200、每個原始 stamp 非 nil，以及兩層各
   14 筆符合既有 layout 的 stamp，**再**呼叫 `xlate.Layer.Snapshot()`；
   任何來源不合法不得 panic、讀影格或呼叫 callback。封存值含固定 group key、
   generation、epoch、`background` z=0 與 `text` z=1 的私有 snapshot bytes、
   深複製不可變字型 registry 與完整內容指紋；不得向 frontend 暴露原始
   `*xlate.Layer`、`*xlate.Font` 或可變 map／slice 別名。callback 結束立即撤銷
   lease；即使呼叫者保存了封存值，也不得再投影。跨 goroutine 呼叫或同時
   Step／Apply／Restore 不在此契約內，正式 session 必須序列化這些操作。
4. **投影、失敗與輸出。** projector 在讀 frame **之前**驗 group key、generation、
   lease／epoch、完整兩 slot 順序、canvas、stamp 狀態與安全幾何、字型名稱／
   canonical 內容指紋、glyph 覆蓋及精確列長；不接受 nil、空名、錯 registry、
   錯倍率、溢位、缺字或缺層。然後從 `host.FrameSource` 讀**恰一張** 320×200
   indexed／palette，讀取返回後、畫 RGBA 前重新驗 owner token 與封存完整性；
   即使來源在讀取期間重入並使 owner 失效，也不得交付舊群組。最後以私有 clone
   畫 background→text，回傳唯一完整、全不透明的 640×400 或 960×600 RGBA。
   影格或 preflight 失敗時回錯且 RGBA 為空；preflight 失敗讀影格次數為零，
   讀取期間失效可已讀一次但不得交付部分 RGBA。不得寫入 DOS 機器、答案、
   存檔或原始 framebuffer。

可直接落程式的最小所有權形狀如下；名稱可異，但責任不得拆散：

```go
// apps/buckrogers：唯一持有可變 RuntimeManualOverlay 與其 consumer 的 owner。
// 不回傳 overlay、layer、Font 或封存群組給 frontend。
type ManualSnapshotOwner interface {
    Consume([]ManualPresentationEvent) (int, error) // 包住唯一 consumer／Apply
    PrepareFrame(host.IndexedFrame) (ManualFrameTicket, error) // 同 goroutine 呼叫 overlay.Frame，保存同影格的私有複本
    Snapshot(ManualFrameTicket, int) (presentation.LayerPresentationSnapshot, error)
    Invalidate() // Restore、stop、source discontinuity；撤銷全部舊 ticket／lease
}

// ticket 欄位不匯出，綁 owner、generation、epoch、320×200 indexed 複本與 palette 值。
type ManualFrameTicket struct { /* private fields */ }
```

session 在同一個 Update 迴圈只讀一次 DOS indexed／palette，交給 `PrepareFrame`；
`PrepareFrame` 先對該影格呼叫現有 `RuntimeManualOverlay.Frame`，再交 ticket。
`Snapshot` 先由 owner 檢查來源 stamp，呼叫 `xlate.Layer.Snapshot` 封存兩層及
canonical 字型私有複本，令 `presentation` projector 做**投影前檢**；
上文 `WithSealedManualGroup` 是 owner 內部短生命週期方法，不是 frontend
可持有的公開介面；對 frontend 只暴露此處的 `Snapshot` 結果。
前檢成功才從 ticket 所持的 frozen frame source 取一次**同一份影格**，讀後再驗
owner token／digest，最後畫 RGBA。如此「前檢前零次 frame read」指的是投影用
`ReadPresentationFrame`，不是遊戲迴圈取得 `PrepareFrame` 輸入的原始讀取；
兩者不可混計。若實作沿用現有 `host.FrameSource` 而非 ticket，則須用等價方式
釘住與 `Frame` 相同的 indexed／palette，且不容許在其間 Step machine。
`presentation` 不呼叫 `RuntimeManualOverlay.Frame`、`Apply` 或 DOS machine；
`apps/buckrogers` 不自行放大／畫圖。倍率切換時撤銷舊 ticket，重建相應
2×／3× presenter 與 owner，不得在已建立 stamp 上臨時替換 font 名稱。

正式實作可選等價的型別與封裝，但不可放寬上述失敗語意。`presentation`
通用層只負責封存、驗證、單次取幀及依 z-order 合成；`apps/buckrogers`
owner 提供手冊 key／兩層順序／layout／字型與生命週期，frontend 不得
重新拼湊手冊專屬 layer 或猜 font。由於目前正式單層
`LayerSnapshotProvider` 是先讀 frame 後驗 layer，它不得直接充當此雙層 API。

### 實作後的 CONFORMED 閘門

正式元件測試須重跑合成正例及上述各負例，另覆蓋缺少任一 14 行 stamp、
錯行序／安全矩形、非法 font 名稱或指紋、字模列長、來源影格錯誤、
Clear／Begin／Restore 後舊 group 與 `FrameSource` 讀中失效；確認零 panic、
零部分 RGBA、必要時讀零或一張 frame，且原 layer／font／DOS state 均未變。
2×／3× 正式 projector 的 RGBA 須與同一份 presenter 輸出逐 byte 比對。
正式 Linux session、watcher 與其他選單／劇情 overlay 的共存，及手冊首題／
答錯換題／返回／存讀檔的原版同狀態與正常玩家路徑，需另有 dosgolem 收據
才可擴張 CONFORMED。其餘 38 題不能以此元件測試推定已驗收；所有原版與
倚天輸入及其衍生字模仍只留本機，不得上傳 GitHub 或公開發行。
