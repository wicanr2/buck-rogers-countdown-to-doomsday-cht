# 第一百三十三階段：真實 Ebitengine MouseBridge 有界 Step 收據

狀態：**prototype evidence；MouseBridge 規格 228 維持 DRAFT，不得接 production 或升 READY。**

## 範圍

本階段在 Docker／Xvfb 以真實 X11 `mousedown`／`mouseup` 送入 Ebitengine，並由 ignored
`workplace/phase118-game-ebiten-active-story/` receipt harness 接收。它連結 ignored
`workplace/phase128-mousebridge-prototype/` 的可丟棄 bridge 核心；不是正式 host frontend。

私有輸入為 `phase12-before-question.state`（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）及 `GAME.OVR`
（SHA-256 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`）。工具為
`eob-remake-go:1.26.7-ebiten2.9.9`、Go 1.26.7、Ebitengine 2.9.9、dosgolem
`b4e1fb74b93fddabcde20c7ac07132604de04471`。原版、state、畫面與 JSON 收據均只在 ignored
`workplace/`，不得進 Git 或公開包。

## 2×／3× 真實事件收據

2× 的兩例都是 logical canvas 的 Down `(200,200)`，換算為 DOS `(100,82)`，且都在 Down 後及
Up 後各執行 50,000 Step：

| 實體事件 | private receipt | 已觀測 API 與按鍵狀態 |
| --- | --- | --- |
| canvas Left Down → 同 canvas Left Up | `out/phase130-real-mouse-inside-v4/mouse-receipt.json` | `MoveMouse(100,82)` → `PressMouse(0)` → `ReleaseMouse(0)`；button `0→1→0` |
| canvas Left Down → chrome Left Up | `out/phase130-real-mouse-outside-up-v1/mouse-receipt.json` | 同一 API 序列；Up 不 Move，DOS `(100,82)` 保持不變，button `1→0` |

兩份收據均記錄 mouse position/buttons/press-release counters、BIOS pending、Key IRQ、indexed
framebuffer SHA-256、bounded Step、容器與輸入雜湊。兩例的第二段 Step 終態 indexed hash 均改變；
此處只記錄差異，**未將它歸因於滑鼠，也不聲稱已觀測到玩家可見 mouse 效果。**

3× 以 logical `(300,300)` Down（同樣換算 DOS `(100,82)`）、host chrome 高 `54`，並使用相同
兩段各 50,000 Step 的上限：

| 實體事件 | private receipt | 已觀測 API 與按鍵狀態 |
| --- | --- | --- |
| canvas Left Down → 同 canvas Left Up | `out/phase130-3x-inside-v2/mouse-receipt.json` | `MoveMouse(100,82)` → `PressMouse(0)` → `ReleaseMouse(0)`；button `0→1→0` |
| canvas Left Down → chrome Left Up `(300,15)` | `out/phase130-3x-outside-up-v3/mouse-receipt.json` | Up 只 `ReleaseMouse(0)`；DOS `(100,82)` 保持不變，button `1→0` |

這兩例僅是 3×的同一狹窄收據範圍，不證明完整 3× pointer matrix、玩家可操作性或 frontend readiness。

`cmd/state-compare` 對上述兩例的 private `mouse-before-down.state` 回傳 `equal=true`；其正規化
machine SHA-256 為 `71860cf29796c2017e303a4fda5d06212ab0c5e66c0d6547811521f6049161bd`，DOS SHA-256 為
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。這只證明該 before-down
checkpoint 的完整持久化語意相同，不擴張為所有事件或玩家效果同狀態。

## 存態摘要勘誤與正確比較方式

早期 receipt 的 `machine_and_dos_state_sha256` 是 `SaveStateFile` gzip/gob **檔案位元組** SHA-256。
它會受到 Go map 走訪／gob 輸出順序影響；因此即使同一 private state、同一 Step，inside 與
outside-up 的 before-down 值不同。此欄位只能辨識單一檔案，不是跨 run 的 semantic same-state
證據，後續不得引用它來宣稱兩 run machine 狀態相同。

權威的跨 run 比較入口是 dosgolem 的
`cmd/state-compare`：它解 gzip 兩段 state、解碼 machine/DOS state，排序 map-derived DOS
handles／EMS handles，並以 `machine.StateDigest`／`dos.StateDigest` 產生正規化摘要。要宣稱
same-state，須在每個 receipt phase 保留 private `.state` 並用該工具比較；只比 input state SHA、
Step 或 raw gzip SHA 均不足。新 harness 已改為記錄 `machine_memory_sha256`，並在每個 phase 寫出
private state，以供此正規化比較。

## 2× 已按下後的 panel-open cleanup

`out/phase134-panel-open-up-2x-v2/mouse-receipt.json` 以真實 X11/Ebitengine canvas Down `(200,200)`
建立 DOS `(100,82)` 的 left press；其後 harness 以既有 `PanelController` 開啟面板（此 state transition
不是實體 host click），再以真實 X11/Ebitengine chrome 外 Up 接收為 `(199,9)`。後者是 Xvfb
letterbox 縮放的 ±1 logical-pixel round-off，仍在 chrome 外。API 只有
`MoveMouse(100,82) → PressMouse(0) → ReleaseMouse(0)`；panel-open 後的 Up 不 Move、DOS 座標保持
`(100,82)`、button `1→0`，且 Down／Up 後各有 50,000 Step。終態畫面 hash 改變只作觀測，未歸因。

這是「已 forwarded Down 的 cleanup」狹窄證據；因 panel opening 是 harness precondition，不能宣稱
正式 host hit routing 已驗收。

## 2× panel-open 的新事件隔離

`out/phase134-panel-open-new-2x-v5/mouse-receipt.json` 在 harness precondition 下將 panel 設為 open，
再接收真實 X11/Ebitengine 同點 Down/Up `(199,199)`（原 requested `(200,200)`，Xvfb letterbox
round-off 為 -1）。兩個事件均被 bridge 拒絕為 `panel-open-consumed`／`unmatched-up-rejected`；
`api_calls` 是空集合，DOS mouse `(160,100)`、buttons、press/release counters、BIOS pending、Key IRQ
與 indexed hash 均不變。Up 後再有界 Step 50,000，indexed hash 仍不變，未觀察到玩家可見效果。

此收據只驗證 open precondition 下的新 pointer edge 被隔離；panel 實際開啟 click 的 backend route 及
其他 panel hit/miss 仍未驗。

## 未完成

- 228 的完整 2×／3×邊界矩陣、focus-loss、panel-open 實體開啟 route、重複／orphan Up 事件及 normal player-path
  因果 A/B 均未完成。
- 本階段不改原版 EXE、DOS 規則、正式 host 接線或覆繪生命週期。
