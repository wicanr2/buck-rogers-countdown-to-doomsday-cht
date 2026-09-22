# 第一百四十六階段：修正後的畫布內滑鼠放開實體收據

日期：2026-09-22
狀態：**可丟棄原型證據；MouseBridge 與 Linux 前端仍為 DRAFT。**

## 範圍與來源

本階段只重驗使用者已確認的畫布內 Left Down→Up：Down 必須
`MoveMouse→PressMouse(0)`，Up 仍在關閉面板的畫布內時必須
`MoveMouse→ReleaseMouse(0)`。畫布外、面板及失焦仍以最後有效 DOS 座標
只放開一次；本次沒有重跑那些格。修正後的可丟棄橋接碼位於 ignored
`workplace/phase128-mousebridge-prototype/bridge.go`，SHA-256
`b984f77aec9edd2c774c8507a58662bdf3a054825ccca946a3852ae570d11977`。
其實體事件 harness 位於 ignored `workplace/phase118-game-ebiten-active-story/`。

以 `eob-remake-go:1.26.7-ebiten2.9.9`、Go 1.26.7、Ebitengine 2.9.9、
Xvfb 與真實 X11 `xdotool` press/release，在 `--rm --network none` 且有界資源的
Docker 中執行；原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，
私有起始 state `phase12-before-question.state` SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`。
位址／座標是 Ebitengine logical pixels 與 DOS mouse virtual coordinates，非
IDA 線性位址。dosgolem 本機 source HEAD 為 `8da5a0d`；harness JSON 的
`dosgolem_commit` 欄為早期寫死的 `b4e1fb7`，**不能**當作本次 source 版本證明。

第一次 2× 執行因錯誤覆蓋 image 的 `GOPATH`，離線 Go 試圖下載依賴；已中止，
未產生有效滑鼠收據。重跑沿用 image 原有 `/go` 模組快取後成功。

## 已觀測結果

| 倍率 | 私有收據與 SHA-256 | 真實 logical Down／Up | DOS 呼叫順序 |
| --- | --- | --- | --- |
| 2× | `out/phase146-inside-up-2x-rerun/mouse-receipt.json`；`06205fcb73cc98db60e2151de0b7c5a9db883e28b76d23779aa3053b5ad3388e` | `(200,200)`／`(200,200)` | `Move(100,82)→Press(0)→Move(100,82)→Release(0)` |
| 3× | `out/phase146-inside-up-3x/mouse-receipt.json`；`4e42a2ce6a91cff1f11aa2d1cd3bca84c9fd64f0e6e9ed9cbcc5625cb4d51fde` | `(300,300)`／`(300,300)` | `Move(100,82)→Press(0)→Move(100,82)→Release(0)` |

兩例各接收一個 Ebitengine release edge。DOS mouse 都從 `(160,100)`、button 0
變為 `(100,82)`、button 1，再於 Up 後變為 button 0；press/release count
均為 1／1。Down、Up 兩段各執行 50,000 machine steps。在每個輸入 API 邊界，
BIOS pending 與 Key IRQ 均為零，indexed framebuffer 與 machine memory SHA-256
在該 API 呼叫前後不變。Up 後有界 Step 的 indexed hash 改變，僅記為觀測，
不得歸因為滑鼠造成的玩家可見效果。

這只補「畫布內 Up 在修正後確實 Move→Release」一格；不是四角／邊界、
open-panel hit/miss、畫布外與失焦雙倍率矩陣，也不是正式後端或正常玩家
滑鼠因果 A/B。spec 228 與專案 spec 004 均維持 DRAFT。
