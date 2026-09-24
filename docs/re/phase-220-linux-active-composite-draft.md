# 第二百二十階段：Linux 前端多作用層單影格合成候選

日期：2026-09-24
狀態：**DRAFT；僅合成、可丟棄原型，不授權 production，不宣稱可玩。**

## 玩家阻塞與固定來源

Issue #16 的正式 Linux 玩家視窗必須在同一原版影格顯示已接通的選單、劇情、
手冊等繁中作用層。現行 fork `cc0b17a` 的
`presentation/layer_snapshot.go` 只接受一個 `*xlate.Layer`；
`apps/buckrogers/manual_overlay_runtime.go` 單是手冊正文就持有背景與文字
兩個 layer，並在自己的 `Draw` 中依序繪製。因此不能把任一單層
`LayerSnapshotProvider` 收據外推成完整玩家前端的多層呈現。

本輪檢查的是 Go API 與無原版素材的合成影格；沒有載入遊戲、手冊、倚天字模、
私有 state 或存檔，沒有原版位址空間。dosgolem fork 本輪未提交的
`presentation/composite_draft_test.go` SHA-256 為
`a6879d6154c700f644463417689eb7b2f7f94096efc9406b452c6690769dfd44`。
它只是一個不會被正式呼叫端 import 的測試用 evaluator。

## 已量候選與推論等級

| 結論 | 等級 | 收據／限制 |
| --- | --- | --- |
| 正式 provider 每次只投影一個 active layer | 已證實 | `NewLayerSnapshotProvider(source, layer, fonts)` 的型別、實作與既有 `layer_snapshot_test.go`；沒有多 layer registry。 |
| 手冊 presenter 需要背景先於正文繪製 | 已證實 | `RuntimeManualOverlay.Draw` 依序呼叫 background、text；其 `Frame`／generation 由該 presenter 自己管理。 |
| 多層 projection 可以只讀一次 indexed／palette，按唯一 z-order 繪在同一 RGBA baseline | 已證實，僅合成原型 | `TestDraftCompositeOneFrameOrderedLayersAndNoMutation`：兩個同點 stamp 依 z-order 產生上層綠色；2×／3× 各只讀一份 frame，兩個原 layer 的 Snapshot bytes 不變。 |
| 缺 slot、重複名稱／z-order、過期 generation 或 nil layer 可在讀 frame 前拒絕 | 已證實，僅合成原型 | `TestDraftCompositeRejectsPartialOrStaleGroupBeforeFrameRead` 的五個負例；固定 manifest 是原型輸入，正式 owner 尚不存在。 |
| 缺字不應交付局部 RGBA | 已證實，僅合成原型 | `TestDraftCompositeMissingGlyphNeverReturnsPartialRGBA`；繪圖前拒絕，錯誤返回沒有可用 RGBA。 |
| 壞字模長度、負座標或超出畫布的 stamp 不應進入 `Draw` | 已證實，僅合成原型 | 獨立審查指出現行 `xlate.Draw` 沒有完整 preflight，隨後加入 `draftValidateStampGeometryAndGlyphs`；`TestDraftCompositeMalformedGlyphOrGeometryNeverDraws` 三例均回錯且不交付 RGBA。正式 `xlate` 與 provider 尚未具備此契約。 |
| 真實各 presenter 可以共用同一 manifest／generation 且不互相殘留 | 未知 | 手冊兩層與其他 watcher 並存、Clear／Restore／discontinuity 的實際順序尚未量；本輪原型沒有這些 owner。 |

## 追加：正式手冊 presenter 雙層的合成入口缺口

同日增加 ignored `apps/buckrogers/manual_composite_draft_test.go`（SHA-256
`287f8d38eeab460eefd8a208548a7b82a06eb3d45d4e613fef2347b7d6521883`）。
它使用現行 `RuntimeManualOverlay` 的正式 begin→request→Frame→Draw
路徑，但 catalog、倚天字模與 320×200 indexed／palette 均為合成資料，
不是原版題目或正常玩家路徑。

- **已證實，限合成正式 presenter：**2× 的原始 16×16 字型若有名稱，
  `LayerSnapshotProvider` 可投影 active text layer；3× 的
  `manualThreeXFont` 目前回傳未命名的 22×22 衍生字型，即使
  `RuntimeManualOverlay.Draw` 正常出圖，單層 provider 仍按既有
  `227-host-active-layer-snapshot-core` 契約拒絕其 text layer。
- **已證實，限測試用變更：**僅在測試中把該衍生字型命名、以同一
  指標登錄，provider 即接受。將同一正式 presenter 的背景與文字
  layer 各自 Snapshot→Restore 成私有 clone，依原順序畫在同一
  合成 baseline；2×、3× 的結果皆與 presenter `Draw` 逐 byte 相同。
  這不代表正式多層 owner 已能存取私有 `background`／`text` 欄位，
  亦不代表真實原版影格上所有文字路徑可以並存。

測試與 `go vet ./apps/buckrogers` 在既有無網路有界 Docker 中通過。
正式接線前，須由遊戲專屬 presenter 明示提供完整背景／文字群組和
衍生字型的穩定名稱／精確 registry，再讓通用合成層讀取；不得在
frontend 以反射、單獨挑 text layer 或用 2× 字型代替 3× 字型。
此為下一個限縮 READY 審查輸入，規格 004 整體仍 DRAFT。

獨立唯讀審查另確認兩項不能由上述合成綠燈外推：`required` manifest
由測試呼叫者自報，尚未綁實際 watcher 註冊表；generation 也沒有連到
正式 session owner 的 Restore／discontinuity。單次讀取只表示 indexed／
palette 同一 baseline，**不**表示 layer 與 machine 的生命週期已同步。
審查也指出測試用 `draftValidateStampGeometryAndGlyphs` 遇到 nil stamp
會在讀取 `stamp.X` 時 panic，且 `GlyphScale` 與索引溢位尚未完整前檢；
因此上表的「不交付局部 RGBA」及幾何負例只涵蓋列出的固定測例，
**不構成一般輸入的失敗即關閉保證**，更不能直接搬入正式合成器。

## 正式 READY 前必須閉合

1. 定義由誰在第一步前註冊全部選定作用層、字型與唯一 z-order；不可讓
   `frontend/ebiten.Game` 按當前畫面自行挑 layer。`manual` 的背景／文字必須
   作為完整群組，缺任一層即失敗即關閉。
2. 定義 group generation 與各 watcher generation 的關係；手冊 begin／clear、
   劇情離頁、還原及執行中斷後，舊 layer 不得被下一個 `Snapshot` 畫出。
3. 所有 active layer 必須在取得一次原版 indexed／palette 後完成唯讀複製、
   幾何與字型預檢，再依固定 z-order 繪製；任一缺字、已存在但長度錯誤的字模、
   未登錄 font、重複順序、尺寸或 stamp 幾何錯誤，不得 panic 或向前端交付
   半張合成畫面。正式 API 尚未提供此 preflight。
4. 用真實手冊／選單／劇情的合法同狀態事件驗證 2×／3×、開關面板後
   raw indexed、palette、machine、BIOS、FileOps 與核准矩形外像素不變；
   再走不靠 checkpoint 的正常玩家路徑及存讀檔。合成綠燈不能替代這些。

`xlate.Layer.Draw` 直接接受 RGBA buffer，本輪測試用 preflight 僅證其
合成輸入的三種壞資料會被拒絕，並非正式 xlate 驗證器；因此目前仍不能把
原型搬進 production。下一個最小切片是用
手冊兩層的**正式** presenter 與另外一個已接通的 active layer，在相同
合法原版影格上驗證 manifest、z-order、generation 與錯誤矩陣，先形成
獨立 READY 審查輸入。

## 可重生檢查與權利邊界

既有 `eob-remake-go:1.26.7-ebiten2.9.9` 映像、`--network none`、
`--read-only`、`--rm`、UID/GID 1000:1000、`--memory 3g --cpus 2
--pids-limit 256`、唯讀 fork 掛載及 `/tmp` 暫存下，執行
`go test -count=1 ./presentation` 與 `go vet ./presentation`，兩者通過。
這些只驗無原版素材的合成與既有 presentation 單元測試。

測試檔在 `.gitignore` 下的 `workplace/dosgolem/`，本文件不含字模、
原版資料、可還原畫面或存態；不授權將其放入公開發行包。
