# 第一百二十七階段：pointer miss A/B prototype

狀態：可丟棄 UX 證據；非 READY、非正式 MouseBridge。

輸入為私有 `workplace/probe/phase12-before-question.state`（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）與唯讀原版
`GAME.OVR`（SHA-256 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`）。
工具為本機 dosgolem 分支 `d495e93` 加 ignored `workplace/phase118-game-ebiten-active-story/`
實驗原型、Ebitengine 2.9.9 與 Xvfb；此處座標為 host logical pixel 及 DOS mouse 座標，
不是反組譯的線性位址。

同一私有原版 state 與同一 Ebitengine/Xvfb 實體 click（closed panel、logical 200,200）分別跑
`no-forward` 與 `dos-mouse`。唯一應解讀的私有最小收據是
`workplace/phase118-game-ebiten-active-story/out/phase127-clean-*/pointer-ab-receipt.json`；它不沿用
phase125 的倍率／鍵盤欄位，未執行的行為不以 `false` 表示。

兩組 indexed 畫面 hash 均為 `964943c39af4fe3a69655d3e39b47f2774ff6fdea684995a2ce08bd26ddd1bba`；BIOS pending、
KeyIRQs、mouse buttons、events 與 polls 不變。no-forward 的 mouse 座標保持 (160,100)；實驗性
`DOS.MoveMouse/PressMouse/ReleaseMouse` 轉送後為 (100,82)。此 state 未 Step machine，沒有玩家可見畫面
差異；不能推論遊戲實際滑鼠操作效果。

實驗 mapping 為 `(logical x/scale, (y-chrome)/scale)`，不是產品座標契約。panel 開啟時 pointer miss 維持
隔離。正式 host mouse bridge、DOS forwarding UX 與 normal-path visible reaction 仍待使用者決定與證據。
