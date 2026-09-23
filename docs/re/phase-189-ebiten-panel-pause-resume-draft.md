# 第一百八十九階段：真實繁中視窗的面板暫停／恢復 DRAFT 原型

日期：2026-09-23  
狀態：**DRAFT 原型；不是正式 Linux 玩家前端或同狀態完整驗收。**

## 已確認的決策與原型邊界

使用者已選定設定面板展開時暫停 DOS CPU，關閉面板後恢復。這次僅在
ignored `workplace/phase118-game-ebiten-active-story/` 的 caller 層加入可丟棄
`-router-pause-draft` 路徑；正式 `frontend/ebiten.Game`、原版 EXE、遊戲規則、
譯文 catalog 與 dosgolem watcher 均未修改。原型每個 `Update` 先處理真實
Ebitengine/X11 輸入，再依面板狀態決定是否呼叫有界 `Advance(16)`：

- 面板開啟的每一回合均不推進原版。
- Cancel 或 Apply 使面板收合的**同一回合**仍不推進；下一個關閉回合才恢復。
- 2× 暫選 3×後 Cancel 仍為 2×，再次開啟選 3×並 Apply 後為 3×。

本次從本機合法手冊後私有 checkpoint 起跑，真實首屏五行繁中 watcher 已作用；
不從冷開機進入，亦不代表完整玩家路徑。原版檔案、私有 state、字型與截圖只在
`workplace/`，不加入 Git。dosgolem 本機 fork 為
`3092dade3aa5deaf86395864a6c539f4088bdf23`；原型來源
`main.go` SHA-256
`dd541798725609f977d3e64d9c708e92b0a125d9f91603a07e92dbcd00dc4316`，
`router_draft.go` SHA-256
`fd4d6605896f32f430eab371a00612894f40d9b4cfb071af78e2a344105d531b`。
這些雜湊只定位本次 ignored 原型版本，不取代第一百八十五階段當時的來源。

## 實體收據

沿用 `eob-remake-go:1.26.7-ebiten2.9.9`，在無網路、資源受限的
Docker／Xvfb 中以實體 X11 點擊跑完整個 Cancel→重新開啟→Apply 序列；
原型 `go test ./...` 通過。私有 JSON
`workplace/phase189-router-pause-draft/router-receipt.json` SHA-256 為
`1281f37cd5925de30520b4ee0f9a72cdb2cb19494358c2b0db8fe6787d1b8eb0`。

| 觀測點 | 實際結果 |
| --- | --- |
| 首次開面板錨點／下次關閉回合 | `276400351`／`276400367`，差 16 步 |
| 第二次開面板錨點／下次關閉回合 | `276401231`／`276401247`，差 16 步 |
| 開面板未推進回合／收合同回合略過 | 89／2；後者分別是 Cancel 與 Apply |
| 前後原版 indexed 畫面 SHA-256 | 均為 `964943c39af4fe3a69655d3e39b47f2774ff6fdea684995a2ce08bd26ddd1bba` |
| 2×／3× 繁中 RGBA 對既有 CLI 私有收據 | 兩者皆逐位元組相等 |
| 最終倍率／面板 | 3×／收合 |

每次開面板記錄的 machine step 及 raw indexed SHA 在展開與收合同回合保持
不變；第一個恢復回合才各前進 16 步。2× RGBA SHA-256 為
`35fcdbb0eb45cde3ec67db839ff165fc48cfdcfff2998e22104ec1f940666e91`，
3× 為
`bebcfb0e7508280966915deec66d8a58c1cd6332f764638d6afe399f64689960`；
兩張實體視窗 PNG 雜湊分別為
`49e94cf8c1b3cea05126042c98feee89f594f066f773e189d58ba9b4dc51621b` 與
`cf4b14f3d7e87092abdb144f398c791b377bdc195f4169905788243af5efb452`。

這些收據僅釘住 ignored caller 的 CPU Step 排程、原版 indexed 畫面與
已接首屏繁中投影；尚未逐欄驗證 DOS memory、IRQ、BIOS queue、虛擬時間、
檔案副作用或控制／中文兩側同一步 A/B，也未驗冷開機、手冊路徑、存讀檔
與其他 watcher。不能將「面板中 step 不變」外推為完整 DOS 狀態不變。
正式前端應先完成[規格 004](../spec/004-dosgolem-host-frontend-draft.md)的
READY 審查，再將此排程語意接進 production path 並補上述同狀態收據。
