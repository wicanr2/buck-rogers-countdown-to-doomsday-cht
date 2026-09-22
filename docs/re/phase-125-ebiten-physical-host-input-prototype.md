# 第一百二十五階段：Ebitengine 實體 host 輸入 prototype

狀態：prototype evidence；不升 READY，不是可玩版。

以私有合法原版 state、真實 Buck Rogers machine、作用中的第一頁故事 layer，在 Docker
Linux／Xvfb 中開啟 Ebitengine 2.9.9 視窗。`xdotool` 只對 X11 視窗送出 pointer／Enter；程式
僅從 `CursorPosition`、`IsMouseButtonJustPressed` 與 just-pressed keyboard API 接收，沒有直接
呼叫 `PanelController` 冒充玩家事件。

私有 receipt：`workplace/phase118-game-ebiten-active-story/out/phase125-final-receipt-v2/receipt.json`。
它不含原版文字、答案、字型 bytes 或截圖。收據確認順序：開啟設定、開啟面板時 Enter、暫選
3×、Cancel、重開面板、再次暫選 3×、Apply、關閉面板時 Enter。

- Cancel 後 active／selected 都是 2×；重開面板仍為 2×，符合「關閉即取消暫選」。
- Apply 後 active／selected 都是 3×且面板收合；3× host RGBA 逐像素等於 phase115 CLI 收據。
- 開啟面板的 Enter 被 host 消費；BIOS pending、KeyIRQs、indexed VRAM hash 與 DOS mouse state/polls
  均不變。關閉面板的 Enter 才依已證實 BIOS 契約排入一鍵，仍未 Step machine。
- 每個 host hit 的前後 raw indexed hash 均為
  `964943c39af4fe3a69655d3e39b47f2774ff6fdea684995a2ce08bd26ddd1bba`。

Xvfb 沒有 window manager，視窗維持 640×436，而展開面板的 logical layout 為 640×584；Ebitengine
以 letterbox 顯示。runner 因此每次 click 重取 X11 geometry，並以 `min(window/logical)` 與置中 offset
換算座標；這是可重播的環境修正，不是產品 hit-test 規格。

未命中 pointer 在此 prototype 明確不轉送 DOS mouse，僅為安全 fallback；DOS mouse forwarding 的
玩家 UX 尚待使用者決定。完整啟動、其他鍵映射、pointer miss 決策、存讀檔與完整遊戲路徑皆未完成。
