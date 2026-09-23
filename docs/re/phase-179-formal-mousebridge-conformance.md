# 第一百七十九階段：正式 MouseBridge 限縮符合性

## 可重播基準與權利邊界

本機 dosgolem 專用分支 `buck-rogers-cht-output-overlay` 的正式 `host.MouseBridge`
程式及收據基準 commit 為 `1dafb0a857c42fbda7058157b7615e214a64ec64`；規格
`docs/spec/228-host-mouse-bridge-ready-candidate.md` 之後在本機 commit `4589bfe`
標記限縮 CONFORMED，未推送上游。原版 `GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，
合法 `phase12-before-question.state` SHA-256 為
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`。
所有滑鼠座標是 host 輸出邏輯像素或 DOS 虛擬滑鼠座標，不是 IDA 位址；
本節沒有推論原版 EXE callsite。

真實 Ebitengine 2.9.9／Go 1.26.7／Xvfb 收據由 Docker
`eob-remake-go:1.26.7-ebiten2.9.9`、`--network none`、目前使用者 UID/GID 產生；
ignored harness `workplace/phase118-game-ebiten-active-story/mouse_receipt.go` 直接建立
`host.NewMouseBridge` 並傳入不可變的 320×200 `host.MouseLayout`，沒有再使用 phase128
可丟棄 bridge。harness source SHA-256 為
`203d8ff92c8e6234fd433d87d3ff44e1ee6e086ea0eefdd1e18ef664401b086d`，
`go.mod` 為 `5ad1de815348c0407571ff586f7b1fa0d91b5bf1b23ac07116112eb38c2ade50`，
driver 為 `fbd3ab0fa6d8931e276291e1a425b7ae70b205e5fe10a4c9bb27cbd0e9c5545d`。
原版資料、字型、存態、完整收據與 PNG 均只在被忽略的 `workplace/`。

## 限縮同狀態 A/B

以下 SHA-256 都指向 `workplace/phase179-formal-mousebridge/<case>/mouse-receipt.json`：

| 倍率／事件 | case | SHA-256 |
| --- | --- | --- |
| 2×無滑鼠 | `control-2x` | `1989d93c7212e794acca40544408cf5239907d9b97a9691a87cbe43fd0722732` |
| 2×畫布內點擊 | `inside-2x` | `e6c59a2bcf47f5872e7560579719cbbcd4782e25a2777a2a715bb5ca24bdcde5` |
| 3×無滑鼠 | `control-3x` | `9b87dacd9bc8e8b539ac5fa917a7494f43434c714f85ec4adf268ab205a6dfe8` |
| 3×畫布內點擊 | `inside-3x` | `d0e7c2179b1c92ed8f390f44816eedbe492d2ba8b56ad840c3c98dc9ee3a3556` |
| 2×畫布外放開 | `outside-up-2x` | `dbe5694360b304761508bf6cb5a21d0785e13ad0db18cae89bcd334143925d93` |
| 2×面板開啟後放開 | `panel-open-up-2x` | `1a42d7c0112cadb21ddd830ee137fc63b9426d973b7cf7a746e7268508acfb07` |
| 2×視窗失焦放開 | `focus-loss-2x` | `109afffeb17866b554d65f09ba81737ba8324d61dc0cdec400bf3766559c3c9b` |

兩倍率控制組與點擊組都從同一 state 各 Step 兩段 50,000 指令。控制組原版
indexed SHA-256 始終是 `964943c39af4fe3a69655d3e39b47f2774ff6fdea684995a2ce08bd26ddd1bba`；
點擊組在 Up 後變為
`13fcacde4c0b693f1478a290910d87571e86d153ab0b291da2e4546487bda7f8`，
API 順序為 `Move→Press→Move→Release`，DOS 座標為 `(100,82)`、按鍵終態 0。
兩個控制組零 DOS API，因此這個固定檢查點的 indexed 差異可歸因該次點擊，
不能外推整款遊戲可由滑鼠操作。

畫布外／面板／失焦三組都是 `Move→Press→Release`，只清已接受的按下，
不移動最後 DOS 座標，終態按鍵為 0。面板案例在 harness 切換 epoch 後走
`epoch-changed-release`；失焦案例確實觀察到 `ebiten.IsFocused()` 真轉假。
主代理以唯讀 Docker 將七份正式收據與 phase170／172／165 原型對應組逐欄比較：
`api_calls`、所有 `phases`（含 step、indexed、memory、mouse）、原版 state 與
`GAME.OVR` 雜湊全等。正式 `host` 的 `go vet`、單元及 race 測試也由主代理重跑通過。

## 結論與未驗範圍

正式 `host.MouseBridge` 僅在上述 **320×200、2×／3×同狀態畫布點擊及 2×三種
cleanup** 範圍限縮 CONFORMED。本專案的[前端規格 004](../spec/004-dosgolem-host-frontend-draft.md)
仍是 DRAFT；正式 Ebitengine 玩家視窗尚未接線。3× cleanup、其他遊戲滑鼠路徑、
完整開機／存讀檔亦未由本節驗收。實體視窗的 right／bottom exclusive 邊界在無 guard
條件下仍無 Ebitengine public event，沿用 phase158 停止線；純核心對邊界座標拒絕，
不能冒充實體邊界已量。
