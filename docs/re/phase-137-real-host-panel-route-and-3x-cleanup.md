# 第一百三十七階段：真實 host panel route 與 3× cleanup

狀態：**prototype evidence；MouseBridge 規格 228 維持 DRAFT，不得接 production 或升 READY。**

## 範圍

本階段延續第一百三十五階段的 ignored
`workplace/phase118-game-ebiten-active-story/` Ebitengine／Xvfb harness。所有原版、state、
畫面與 content-safe JSON 僅在 ignored `workplace/`；Docker 執行皆為 `--rm`、`--network none`、
明確 UID/GID 與有界資源。工具、輸入 state、`GAME.OVR` 雜湊與 dosgolem commit 均由各 receipt
的 metadata 保存。本階段不是正式 frontend，也沒有量到正常玩家路徑。

## 2×／3× 真實 host Open hit 再到 open-panel miss

收據為：

- `out/phase136-panel-host-hit-miss-2x-v1/mouse-receipt.json`
- `out/phase136-panel-host-hit-miss-3x-v2/mouse-receipt.json`

每例先以真實 X11 `mousedown`／`mouseup` click closed-panel 的 host Open button；Ebitengine 接收的
2× logical click 是 `(560,16)`，3× 是 `(840,24)`。`PanelController.Route(Open)` 的 route 都是
`ConsumedByHost=true`、`ForwardToDOS=false`，並開啟 panel；open click 的 release 在 bridge 前被
host 消費，故沒有任何 DOS API。

接著 driver 以第二個真實 X11 click 點選不屬於選擇倍率、套用或取消按鈕的 panel 空白區。Xvfb
letterbox 將它實收為 2× `(259,139)`、3× `(389,208)`；兩例的 `PanelEventPointerMiss` 都保留
既有純核心語意 `ConsumedByHost=false`、`ForwardToDOS=false`（它不是已定案的 hit route）。因 panel
已開，bridge 對 Down 明確回 `panel-open-consumed`，對其 Up 回 `unmatched-up-rejected`；`api_calls`
為空，mouse position `(160,100)`、button、press/release counter、BIOS pending、Key IRQ 與 indexed
framebuffer 在 API checkpoints 全部不變。Up 後的 50,000 Step indexed hash 亦未變，未觀察到玩家
可見效果。

這兩例區分了已證實的 host hit 與刻意未決的 pointer miss：**不得把 miss 的空 route 偽稱為
`PanelController` 已消費**；它在此 private harness 的 open-panel backend bridge 才依使用者已定案的
「open panel 新 pointer 不送 DOS」語意結束為 `panel-open-consumed`。

## 3× accepted Down 後 panel-open cleanup

`out/phase136-panel-open-up-3x-v1/mouse-receipt.json` 以真實 Ebitengine canvas Down `(300,300)`
建立 DOS `(100,82)` 的 left press。harness 隨後以既有 `PanelController` 開啟 panel（這一狀態轉換
不是實體 host hit），並接收真實 chrome Up `(299,14)`。API 僅為
`MoveMouse(100,82)` → `PressMouse(0)` → `ReleaseMouse(0)`；release 沒有 Move，DOS `(100,82)` 保持，
button `1→0`，press/release counter `1/1`，BIOS pending 與 Key IRQ 不變。Down 與 Up 後各有
50,000 Step；終態 indexed hash 改變只作觀測，不歸因給 mouse。

因此本例只補足「3×已轉送 Down 的 panel-open／chrome Up cleanup」；它不證明 panel 是由實體
host hit 在按住 DOS button 時開啟。

## 正規化同狀態與剩餘缺口

以 dosgolem `cmd/state-compare` 比較既有 focus-loss 起點與本階段三例的 `before-down`：

- `out/phase136-panel-host-hit-miss-2x-v1/normalized-before-vs-focus.json`
- `out/phase136-panel-host-hit-miss-3x-v2/normalized-before-vs-focus.json`
- `out/phase136-panel-open-up-3x-v1/normalized-before-vs-focus.json`

三份 JSON 都是 `equal=true`；machine digest
`71860cf29796c2017e303a4fda5d06212ab0c5e66c0d6547811521f6049161bd`、DOS digest
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。這是解碼後、排序 map-derived
state 的正規化比較，非 gzip/gob 檔案 bytes hash。

228 仍缺完整 2×／3×四角與邊界 Down 矩陣、每種 cleanup 的雙倍率實體收據、open-panel miss 的
正式 backend route、以及正常玩家路徑因果 A/B；本階段不改規格狀態。
