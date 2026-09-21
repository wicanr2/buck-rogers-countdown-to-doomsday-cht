# 第八十四階段：dosgolem host 前端能力盤點

日期：2026-09-21
狀態：完成（DRAFT 證據；未實作 host 前端）

## 固定輸入與方法

- dosgolem 本機工作副本：`workplace/dosgolem/`。
- Git branch／revision：`buck-rogers-cht-output-overlay`／
  `8bfd5b4e5802f65d428d3fb439196b3c571c002b`；工作樹乾淨，未推送。
- 在 Docker 的 Go 1.24.13 執行 `go test ./xlate ./apps/buckrogers`，兩套件均通過。
- 檢閱 README、CLAUDE、`docs/spec/000-index.md`、`docs/spec/001-scope-and-mvp.md`、
  `cmd/run/main.go`、`cmd/probe/main.go`、`xlate/`、`apps/buckrogers/*overlay*`；並對所有受版控
  Go source 和 `go.mod` 搜尋 window／frontend／SDL／Ebiten／GLFW／event-loop token。

## 證據表

| 結論 | 分級 | 可回查證據 |
| --- | --- | --- |
| dosgolem 是無頭、決定性的程式化觀測器，而非現成玩家視窗 | 已證實 | `workplace/dosgolem/README.md` 開頭與 `CLAUDE.md` 定位；`cmd/run/main.go` 只以 flags 載入、執行與 stdout report。 |
| 可重用的是 output compositing，不是視窗 | 已證實 | `xlate/layer.go` 的 `Frame`／`Draw` 讀來源並繪入新 RGBA；`apps/buckrogers/menu_overlay_runtime.go` 的 `Draw` 用 `ScaleIndexedRGBA` 建立 presentation baseline，不回寫 indexed framebuffer。 |
| 既有 runtime object 不支援原地換倍率 | 已證實 | `RuntimeMenuOverlay` 與 `RuntimeActionBarOverlay` 將 `scale` 設為私有欄位，constructor 僅接受 2 或3，沒有 setter。 |
| 目前滑鼠是模擬 DOS 輸入，不是 host pointer input | 已證實 | `cmd/probe/main.go` 的 `-mouse-*`／`-click-*` 依 absolute instruction step 排程並呼叫 DOS mouse 路徑。 |
| 沒有可直接重用的 host window frontend | 強推論 | `go.mod` 沒有外部前端依賴，完整 Go source token 搜尋沒有 window／frontend／SDL／Ebiten／GLFW／event-loop 命中，與無頭 README 相符；但新 backend 選擇尚未發生。 |

## 結論

Phase 82 的控制列與面板幾何仍成立，但它是畫面／hit-test contract，不是已存在的執行期 UI。
可以延用 `xlate` 的 output-only 疊層及當前 raw frame/palette；必須新增的是通用 host presenter、
host pointer router、chrome layout 與 output re-render。Buck Rogers adapter 不得知道視窗或按鈕。

本階段沒有修改 dosgolem，沒有把 DOS 滑鼠診斷能力誤接為 host UI，也沒有代替使用者決定
option click 的套用語意。對應 DRAFT 規格為
[`004-dosgolem-host-frontend-draft.md`](../spec/004-dosgolem-host-frontend-draft.md)。
