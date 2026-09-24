# 024 — 手冊背景／正文作用層群組與字型身分

狀態：**DRAFT；待獨立複審。不得授權 production。**

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
