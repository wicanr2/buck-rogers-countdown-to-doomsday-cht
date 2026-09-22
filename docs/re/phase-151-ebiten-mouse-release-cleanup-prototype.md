# 第一百五十一階段：真實 Ebitengine 畫布外放開與失焦清理

日期：2026-09-23
狀態：**可丟棄原型證據；MouseBridge／Linux 前端仍為 DRAFT。**

## 固定輸入與觀測邊界

沿用 ignored `workplace/phase118-game-ebiten-active-story/` 的真實
Xvfb／X11／Ebitengine 2.9.9 harness，以 Go 1.26.7、
`eob-remake-go:1.26.7-ebiten2.9.9` 在有界、無網路、一次性 Docker
執行；`go test -race -count=1 ./...` 通過。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，
私有初始 state SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`。
原版、字型、完整收據與畫面只在 ignored `workplace/`，不入 Git／GitHub。
舊 harness 的 `dosgolem_commit` 寫死欄位不可當本次 source 身分。

每筆收據均為
`workplace/phase118-game-ebiten-active-story/out/phase150-cleanup-<倍率>-<情境>/mouse-receipt.json`；
以下 SHA-256 已回讀：

| 情境 | 2× | 3× |
| --- | --- | --- |
| 控制列 `chrome` | `f04c02991f818889d4bdf85c72fade3bbbc616eb4a53aa768420bc3244c23f90` | `0fa07ea16aee7acdbe13268b2eaa7d97b114b687a8eed43a7f247303ae60cadd` |
| 失焦 `focus` | `804c0ecd920c7bdc7f992bc5d531ba40c37966e3fa74860cd2aa9503d9fd7001` | `4fd6bb515cd0def8d445a41e25e647eb6868a4bf961f08edf0757d92d765f3e5` |
| 畫布外右側 `outside-right` | `98bdbdf0ba8a2d5945a62e063e8ca7d521a75e80584134e2a7a5a2dbd23be1ab` | `f8c03ffeea6aec1c3add824b0c4bfbc6f12beae39f88c08529d9ecfa24090158` |
| 面板已開 `panel-open` | `3a8583b8db71e316c7fbfecdb6a935fa95d29bf56faca02113c990f298125af9` | `bb409148c754d6ad9811ccd6bf13a3579aa4f8cd7da676cb787a9b8d56f682d7` |
| 孤兒 Up `orphan` | 未重跑 | `f47d784306d096cc05892fff2bf603f18f85ee0b38d4f2d375a8653aef61de0f` |
| 重複 Up `repeated` | 未重跑 | `116a6c2df1e4f987745d7d11f1d5a3e265e4f1c576bc12d99d1d34ef81d7e091` |

## 已觀測結果

雙倍率的控制列、畫布外右側、預先開啟面板及失焦四種情境，都先於
畫布內接受 Down，DOS `MoveMouse(100,82)→PressMouse(0)`；隨後只呼叫
一次 `ReleaseMouse(0)`，**不再 Move**。終態 DOS 座標保持 `(100,82)`、
button 1→0，press／release count 各 1。失焦案例由真實焦點切換觸發，
Ebitengine release edge 為 0；清理來自焦點處理，不偽稱收到 Up。
面板開啟案例由 harness 設定面板狀態作前提，**沒有**量到玩家實際點
host 按鈕打開面板的完整路由。

各輸入 API 邊界 BIOS pending 與 Key IRQ 均為零；release API 前後
indexed framebuffer 與 machine memory 未被橋接改寫。後續每段有界
50,000 machine steps 的 hash 可改變，不能歸因於滑鼠本身。3×孤兒
實體 X11 mouseup 沒有 Ebitengine release edge，故零 DOS API、
座標仍 `(160,100)`；3×重複 Up 的第二個實體 X11 mouseup 也沒有
第二個 edge，只有第一次正常畫布內 Up 的 `Move→Release`，
第二次零額外 DOS API。這是目前 public API 的觀測停止線，
不是已收到重複事件後再拒絕的證據。

畫布外右側 exclusive 邊界仍沿用 ignored prototype 的 1 logical-pixel
觀測 guard；它不是正式 DOS 畫布或產品版面。畫布下方 cleanup、
2×孤兒／重複 Up、正式面板空白 miss 消費契約、原版玩家可見滑鼠因果、
完整開機與存讀檔仍未驗。本規格不授權正式前端接線或升 READY。
