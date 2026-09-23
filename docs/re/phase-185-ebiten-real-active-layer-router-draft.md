# 第一百八十五階段：真實繁中作用層接入 Ebitengine 輸入路由原型

日期：2026-09-23
狀態：**DRAFT 原型；不是 Linux 可玩版或正式前端驗收。**

## 本次接通的垂直切片

從第一百二十階段已使用的本機合法手冊後 checkpoint
`workplace/probe/phase12-before-question.state`，同一 dosgolem watcher 在視窗開啟前
以原本的百萬步邊界前進，實際產生首屏故事五個作用中繁中 key。其後由
`frontend/ebiten.Game` 的正式通用輸入路由接管畫格：每次 `Update` 有界推進原版
16 instructions，`Draw` 從同一 watcher／`LayerSnapshotProvider` 取圖；使用實體 X11
滑鼠打開設定、選 3×、按 Apply，面板自動收合，倍率只改輸出投影。這不是合成
layer，也沒有改原版 EXE、判定、記憶體或字型來源。

可丟棄 caller 位於 ignored
`workplace/phase118-game-ebiten-active-story/main.go`（SHA-256
`8cad223b9d9110fa4b3b2a775e4aed4917611d1fb46d1f53be5e8c463906a4b2`）與
`router_draft.go`（SHA-256
`fe56da83f2237a74d45c632e8d6e57c9cabc349cdde496f729693bbbffdda589`）。
dosgolem 本機 fork 是 `3092dade3aa5deaf86395864a6c539f4088bdf23`；原版輸入、
有界 BIOS 排程、字型和完整畫面收據都留在 `workplace/`，不加入 Git。

## 實際驗證與限制

以既有 `eob-remake-go:1.26.7-ebiten2.9.9` 在無網路、有資源上限的
Docker／Xvfb 執行；`go test ./...` 通過。`router-receipt.json` SHA-256
`520462b1a5a7ca405bf574544321cca6f6a23273b4fe0939e84db5a760b6e8b8`。
原型在程式內直接讀取第一百十五階段 CLI 私有 RGBA 收據，做**逐位元組相等**
斷言；兩倍率不是只比較 PNG 外觀：

| 驗證點 | 結果 |
| --- | --- |
| 視窗前／後的首屏繁中 key | 5／5，無缺字 |
| 起始 2× RGBA 對既有 CLI | 完全相等，SHA-256 `35fcdbb0eb45cde3ec67db839ff165fc48cfdcfff2998e22104ec1f940666e91` |
| Apply 後 3× RGBA 對既有 CLI | 完全相等，SHA-256 `bebcfb0e7508280966915deec66d8a58c1cd6332f764638d6afe399f64689960` |
| 實際 `Draw`／`Advance`／原版步數 | 101／244／`276399999→276403903` |
| 最終 host 面板／倍率 | 收合／3× |
| 操作前後 indexed 畫面 SHA-256 | 皆為 `964943c39af4fe3a69655d3e39b47f2774ff6fdea684995a2ce08bd26ddd1bba` |

實體視窗擷取留於 ignored `workplace/phase231-router-active-draft/`：2× PNG SHA-256
`49e94cf8c1b3cea05126042c98feee89f594f066f773e189d58ba9b4dc51621b`；3× PNG
`cf4b14f3d7e87092abdb144f398c791b377bdc195f4169905788243af5efb452`。
人工檢視可見原版人物畫面、首屏五行繁中及 3×較大的緊密中文字；兩張圖均不是
人工繪製假畫布。

這只從合法私有 checkpoint 啟動，**不是冷開機到遊玩的完整鏈**；host 操作期間
原版仍有推進，雖然前後 indexed 雜湊相同，不能將它冒稱「相同 step 的 DOS 狀態
A/B」。這次也沒有驗收 save/load、完整 watcher 轉場、面板鍵盤隔離或 DOS 滑鼠
轉送；後兩項已有其他限縮原型收據，但不能直接替本次路徑補證。通用
`frontend/ebiten.Game` 已被真實繁中作用層的 caller 使用，然而 caller 仍 ignored，
[規格 004](../spec/004-dosgolem-host-frontend-draft.md) 仍 DRAFT。下一步需先審查
完整前端生命週期為 READY，才可把這個 caller 收進正式玩家程式並做正常路徑驗收。
