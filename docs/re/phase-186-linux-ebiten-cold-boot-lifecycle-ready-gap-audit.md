# 第一百八十六階段：Linux Ebitengine 冷開機玩家前端 READY 缺口稽核

日期：2026-09-23
狀態：**DRAFT 稽核；不授權 production 前端，也不變更規格 004 的狀態。**

## 問題與限定結論

第一百八十五階段已從私有 checkpoint 以真實作用中首屏故事 layer 開出 Ebitengine 實體視窗，並以實際 X11 設定操作驗得 2×→3× output projection。它不是 cold boot：caller 位於被忽略的 `workplace/`，起點跳過原版開機、初始輸入、watcher 安裝順序、存檔根目錄與正常玩家到達該 state 的過程。

最短可驗證缺口不是另一張 checkpoint 截圖，而是一個可失敗即關閉的 **session composition root**：從本機原版唯讀輸入建機、在第一個 instruction 前安裝所有已選 lifecycle observer、在同一 goroutine 有界 Step／更新 overlay／讀取畫面，再將已分類的 host 與 DOS 輸入送入該回合。現有 `frontend/ebiten.Game` 是可重用視窗 loop 元件，並不是 composition root。

本文件只稽核前端 READY 前的 typed lifecycle 與失敗界線；不重跑原版、不記錄原文、答案、字型 bytes、state、PNG 或其他私有輸出。

## 程式與既有證據

稽核時 `workplace/dosgolem` commit 為 `3092dade3aa5deaf86395864a6c539f4088bdf23`（2026-09-23）。

| 已有項目 | 分級 | 可回查證據 | 不足以證明的事 |
| --- | --- | --- | --- |
| `host.PanelController`、`ScaleController` | 已證實／純核心已符合 | `host/panel.go`、`host/scale.go` 與測試 | 沒有開機、視窗、DOS 或存檔生命週期。 |
| `MachineFrameSource`→`LayerSnapshotProvider` | 已證實／純投影 | `presentation/machine.go`、`layer_snapshot.go` | 只投影一個已存在的 `xlate.Layer`；不安裝 watcher、不呼叫 `Layer.Frame`、不管理多個 overlay。 |
| `frontend/ebiten.Game` | 已證實為 backend 元件 | `frontend/ebiten/game.go` | 沒有 `main`／公開 command；沒有載入原版、DOS 安裝、cold boot、catalog/font 載入、observer hub、save root 或 teardown。 |
| 作用中繁中實體視窗 | 已證實但只限原型 | [第一百八十五階段](phase-185-ebiten-real-active-layer-router-draft.md) | 從私有 checkpoint 起；host 互動期間仍 `Advance`，非同 DOS step A/B；未驗冷開機、存讀檔或所有 layer。 |
| 滑鼠左鍵橋接 | 限縮 CONFORMED | [第一百七十九階段](phase-179-formal-mousebridge-conformance.md) | 只限明載的 320×200 收據；不是完整視窗或全部玩家輸入。 |

`Game.Update` 的實際順序是：讀 pointer／focus／key → 呼叫可選 `Advance`；`Draw` 才呼叫 `Snapshot`。所以每個 host 操作後仍可能在同一次 Update 執行 caller 提供的 Step。這與「Apply 本身不可送鍵或直接改 VRAM」不衝突，但表示「host 操作不 Step」只能描述 bridge 呼叫，**不能**描述完整 UI 回合的 DOS 狀態。

## 最短的 typed session 契約（DRAFT）

下列是建議的最小 production 輸入，不是本輪實作授權。所有型別以值或窄介面傳遞；`frontend/ebiten` 不可直接取得原版路徑、存態檔、watcher 私有指標或 `Machine`。

```go
type ColdBootConfig struct {
    OriginalRoot ReadOnlyGameRoot // 僅本機；preflight 驗版本／雜湊，不寫入
    SaveRoot     WritableSaveRoot // 與 OriginalRoot 必須不同；沒有即失敗
    Catalogs     CatalogSet        // UTF-8 TSV 與唯一 key／glyph preflight 結果
    Fonts        LocalFontSet      // 僅本機載入；2×／3× 各自驗證
    StartScale   host.OutputScale  // 固定為 2；不得載入持久化偏好
}

type Session interface {
    Advance(budget InstructionBudget) (TickReceipt, error)
    Deliver(InputBatch) (InputReceipt, error)
    Snapshot(scale host.OutputScale) (presentation.LayerPresentationSnapshot, error)
    Close() error
}

type TickReceipt struct {
    Epoch uint64
    Steps uint64
    Phase SessionPhase // Booting, Running, Stopped, Failed
}
```

建議單 goroutine 回合：

```text
preflight → machine/DOS 建立 → install all selected observers → cold boot
→ classify one host input batch → Deliver（host 先消費；僅許可者進 DOS）
→ Advance(明示、有上限的 instruction budget)
→ observer/lifecycle owner Frame/失效 → Snapshot(active composite, scale) → Draw
```

`Snapshot` 不可推進 machine、消費 watcher event、改 stamp 或補作 lifecycle。`Advance` 的 receiver 才可持有 machine；其回傳必須記錄 epoch、實際步數及停止原因，避免目前裸 `func() error` 無法分辨「自然停機、預算耗盡、原版 fault、前端錯誤」。scale Apply 只重建 output projection／layout；不能重建 session、重裝 observer、重新讀盤或清掉 active layer。

### 作用層聚合缺口

現有 `LayerSnapshotProvider` 的單 layer 介面足以重現 phase185 的首屏，但 cold boot 至少要容納 menu、角色建立、manual、story、action bar 等相異 lifecycle owner。READY 前必須定義 `ActivePresentation` 的唯一 owner：它以已驗證的 z-order、font registry 與 generation 將多個 active layer 組成一個唯讀 snapshot；不得讓 frontend 自行挑某個 `PresentationLayer()`，也不得讓兩個 overlay 直接互改 `xlate.Layer`。未登錄字型、重複 z-order、跨 generation、未知／partial group 都須失敗即關閉並保留 DOS 原圖，不畫猜測譯文。

## 必須先釘住的失敗邊界

1. **原始輸入與存檔：** 原版 root 缺失、版本／雜湊不符、DOS install 或 cold boot 失敗時不開窗；save root 缺失、等同原版 root、不可寫或 path escape 時不啟動。正式 session 不得把存檔寫回原始唯讀輸入，也不得以 checkpoint 取代 cold boot。
2. **observer 安裝時序：** 所有本次宣稱可中文化的 watcher 必須在第一個原版 instruction 前完成安裝；任一 catalog、font、identity 或 hook preflight 失敗，對應 layer 不得啟用。restore、未觀測 handoff、hook fault 與 generation mismatch 必須呼叫 execution discontinuity，再清除衍生 layer；不得保留舊 stamp。
3. **回合所有權：** `Deliver`、`Advance`、lifecycle owner、`Snapshot` 必須同 goroutine。`Snapshot` 或 Draw 失敗後 session 轉 `Failed`，後續 Update 不可再 Advance；目前 `Game.Draw` 僅將錯誤暫存到下一次 Update，READY 實作需修正或用外層 gate 保證 fail-stop。
4. **host 面板與時間（已確認決策）：** 使用者已確認面板開啟期間暫停 DOS CPU；Cancel／Close 或 Apply 自動收合後才恢復，排除持續 Step 的方案。正式 session 必須在 host route 後、呼叫 `Advance` 前讀取 panel state；`Open` 或仍為 open 的 `SelectScale` 回合回傳 `Steps=0` 的 pause receipt。Apply／Cancel 在該輸入回合只更新 host state、layout 與 output projection，**不得**偷渡一個恢復後的 DOS Step；下一個 closed-panel 回合才可依明示 budget 恢復。這是玩家時間與輸入語意，需以真實 Ebitengine callback 驗證；現有 `Game.Update` 無條件呼叫 `Advance`，不符合此已確認契約，但本 DRAFT 不授權直接修改它。
5. **輸入映射：** `mapKey` 現只涵蓋 Enter、Escape、Backspace、Tab、Space、方向鍵、A–Z、0–9；F keys、標點、修飾鍵、鍵盤重複、右鍵／中鍵與 window-close 尚未定義。未知鍵一律拒絕，不得猜 mapping。
6. **視窗座標：** hit test 假設 320×200 Ebitengine logical coordinate；尚未驗使用者 resize、DPI／scale factor、window close、3× cleanup 與 right/bottom 實體邊界。READY 須選定禁用 resize，或定義 device→logical 轉換並於兩倍率實測。

## READY 前測試矩陣

| 類別 | 最小案例 | 必測證據／不變量 |
| --- | --- | --- |
| cold boot | 正常本機原版、缺原版、雜湊不符、DOS install 失敗 | 前三失敗不開窗且零原版／save 寫入；正常者先安裝 observer 後才 Step。 |
| storage | 乾淨 writable save root、唯讀／同一路徑／escape | 正常保存只寫 save root；其餘失敗即關閉，原版 tree digest 不變。 |
| lifecycle | boot→首個已量 overlay→正常輸入離開→下一畫面；restore／discontinuity | generation 單調；離頁前最早失效點清 layer；無舊 stamp、無 partial group。 |
| host route | closed/open × 2×/3× × keyboard、host hit、canvas left down/up、outside/panel/focus-loss cleanup | host 事件零 BIOS/IRQ/VRAM/save 副作用；既有限縮 MouseBridge 收據仍通過。 |
| timing | Open、SelectScale、Cancel、Apply、closed DOS key、snapshot/Draw fault；每案於 2×／3×實體 X11 重跑 | Open／Select 時 `Steps=0`，DOS PC／VRAM／BIOS queue／IRQ／save digest 不變；Cancel／Apply 收合的**同一回合**仍 `Steps=0`，下一 closed 回合才可依 budget 推進；任何 frontend error 後步數不再增加。 |
| projection | 每個 active composite 的 2×→3×→2× | 同 raw indexed/palette/active generation 的 RGBA 可重生；差異只限核准 output/chrome pixels；無 16×16 稀疏放大。 |
| normal player | 不用 checkpoint、teleport 或 direct watcher call，從 cold boot 走一條可到達的已量文字路徑；host 操作後繼續；save/load | fixed seed（若該段用 RNG）、輸入、step receipts、machine/DOS/save digest、active keys；原文／繁中差異只限核准覆繪與 chrome。 |
| window | X11 實體 2×/3×、focus loss、close、resize/DPI 所選政策 | 不留按鍵、無背景 goroutine/容器；坐標與 cleanup 行為符合選定政策。 |

## 本輪收據與限制

在 `eob-remake-go:1.26.7-ebiten2.9.9`、`--network none`、唯讀掛載下重跑：

- `go test ./host ./presentation ./apps/buckrogers` 通過。
- `go test ./frontend/ebiten` 未能執行：目前 worktree 沒有 Ebitengine module cache，無網路容器依規範拒絕下載 `github.com/hajimehoshi/ebiten/v2@v2.9.9`。這是驗證環境缺口，**不是** frontend 通過收據或產品缺陷結論。

所有容器均使用 `--rm`、目前 UID/GID、資源上限與無網路；本輪沒有產生或輸出原版、字型、state、PNG 或其他私有資料。規格 004 保持 **DRAFT**。

### 同日驗證環境訂正

主代理改用已含 Ebitengine 2.9.9 的同名專用 image，在無網路容器中可離線
解析 frontend module；第一次仍因未設定 `DISPLAY` 而使 GLFW 初始化失敗。
於相同 image 加上有界 Xvfb、明示 `DISPLAY=:99` 後，
`go test ./frontend/ebiten ./host ./presentation ./apps/buckrogers` **全部通過**。
故上面的「未能執行」只描述代理當時的容器條件，不是本案當前測試結論。
這些仍是元件測試，不含 cold boot、面板暫停／恢復或正常玩家路徑；規格
004 仍 DRAFT。
