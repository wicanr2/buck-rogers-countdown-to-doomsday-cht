# 第一百三十五階段：真實 Ebitengine 焦點遺失與放開邊緣

狀態：**prototype evidence；MouseBridge 規格 228 維持 DRAFT，不得接 production 或升 READY。**

## 範圍與重跑環境

本階段沿用第一百三十三階段的 ignored
`workplace/phase118-game-ebiten-active-story/` harness。真實輸入由 Docker／Xvfb
中的 `xdotool` 送入 Ebitengine；原版、state、畫面、GOLEMFNT 及所有 JSON／state
收據均留在 ignored `workplace/`。這不是正式 host frontend，也不是正常玩家路徑。

輸入為私有 `phase12-before-question.state`
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`、`GAME.OVR`
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；工具為
`eob-remake-go:1.26.7-ebiten2.9.9`、Go 1.26.7、Ebitengine 2.9.9、dosgolem
`b4e1fb74b93fddabcde20c7ac07132604de04471`。每次執行皆為 `docker run --rm`、
`--network none`、明確 UID/GID 與資源上限；容器收尾時已無此 image 的執行中或停止容器。

## 2× accepted Down 後的真實 X11 focus-loss

私有收據 `out/phase135-focus-loss-2x-v2/mouse-receipt.json` 先接收 Ebitengine 真實
canvas Left Down logical `(200,200)`，轉為 DOS `(100,82)`，並有 50,000 Step 的有界
觀測。driver 接著啟動另一個真正的 Ebitengine X11 視窗並以 `xdotool windowfocus`
將焦點移走；harness 只在 `ebiten.IsFocused()` 自真轉假後才送出 bridge 的
`FocusLost`，不是以計時器或合成 Pointer 代替焦點事件。

API 序列為 `MoveMouse(100,82)` → `PressMouse(0)` → `ReleaseMouse(0)`。focus-loss
cleanup 沒有 `MoveMouse`：DOS mouse 維持 `(100,82)`，left button `1→0`，press/release
counter 為 `1/1`，BIOS pending 與 Key IRQ 均不變；其後再有界 Step 50,000。終態
indexed framebuffer hash 改變只記錄為觀測，**不歸因為滑鼠且不宣稱玩家可操作**。

## 2× orphan／repeated X11 `mouseup`

`out/phase135-orphan-up-2x-v2/mouse-receipt.json` 的 driver 已確認送出一個沒有先前
X11 Down 的實體 `mouseup`。Ebitengine 的 public input API 沒有產生 `JustReleased`
edge，因此 bridge 沒有接到 callback，`api_calls` 為空，DOS mouse、button、counter、BIOS、IRQ、
indexed framebuffer 與 machine memory 均不變。這證實此 backend input surface 下 orphan
release 不會觸及 DOS；它不是「bridge 已收到 orphan Up」的宣稱。

`out/phase135-repeated-up-2x-v2/mouse-receipt.json` 先完成一個真實 Down→Up，得到唯一
一次 `ReleaseMouse(0)`；driver 再確認送出第二個實體 `mouseup`。Ebitengine 只暴露第一個
release edge（`ebiten_release_edges=1`），第二個沒有形成新 edge，故沒有第二次 bridge
callback 或額外 DOS API。兩個 API checkpoint 之間的 mouse／button／press-release counter、
BIOS、IRQ 與 indexed framebuffer 一致。這是 Ebitengine state-edge 的明確停止線；bridge
對「已收到的重複 Up」的 fail-closed 單元測試仍是另一層純核心證據，不能把本收據擴張為
raw X11 message callback API。

## 3× panel-open 的新事件隔離

`out/phase135-panel-open-new-3x-v3/mouse-receipt.json` 在 harness panel-open precondition
下接收真實 X11/Ebitengine Down／Up `(299,299)`（Xvfb letterbox 的 -1 logical-pixel
round-off；請求點為 `(300,300)`）。兩事件均沒有 DOS API；DOS mouse `(160,100)`、button、
press/release counter、BIOS pending、Key IRQ 與 indexed framebuffer 在 API checkpoints
完全不變。Up 後另 Step 50,000，indexed hash 仍不變，未觀察到玩家可見效果。

此例只驗證 open precondition 下的新 pointer 邊緣隔離；panel 實際由 host hit 開啟的 route
尚未量到，不能宣稱正式面板 click 已驗收。

## 同狀態比較與限制

不得以 gzip/gob `.state` 檔案位元組雜湊宣稱跨 run 同狀態。用 dosgolem
`cmd/state-compare` 對 focus-loss 起點與 orphan、repeated、3× panel-open 起點比較，私有
JSON 分別為：

- `out/phase135-focus-loss-2x-v2/normalized-before-vs-orphan.json`
- `out/phase135-focus-loss-2x-v2/normalized-before-vs-repeated.json`
- `out/phase135-focus-loss-2x-v2/normalized-before-vs-panel-3x.json`

三者均回傳 `equal=true`，machine digest 為
`71860cf29796c2017e303a4fda5d06212ab0c5e66c0d6547811521f6049161bd`，DOS digest 為
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。

本階段只補足 2× accepted Down→真實 focus-loss cleanup、實際 X11 orphan／repeated
release 的 backend edge 邊界，以及 3× panel-open 新事件隔離。228 仍缺 2×／3×完整四角與
邊界矩陣、兩倍率的全部 cleanup 分支、panel 實體 host hit/miss route，以及正常玩家路徑
因果 A/B；因此維持 DRAFT。
