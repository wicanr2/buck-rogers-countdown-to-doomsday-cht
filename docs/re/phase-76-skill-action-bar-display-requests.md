# 第七十六階段：技能操作列繁中顯示請求

日期：2026-09-21

## 結論

Phase 75 的 `ActionBarEvent` 已接成精確繁中顯示請求。五個文字鍵為「加點、減點、上頁、
下頁、完成」，來源分級是 `runtime-interface`；中文手冊沒有逐字按鈕對照，因此不冒稱手冊譯名。
本階段只建立 request，尚未清除英文或繪製中文。

## 垂直鏈與隔離

`0763:026B` guarded glyph call → `ActionBarEvent` → 16 個 normal／focus exact identities
→ `DisplayRequest` → content-safe JSON metadata。resolver 同時比對 screen、event key、variant、
原文長度與 SHA-256、文字格和像素幾何；譯文不進入 machine、DOS、鍵盤、VRAM 或存檔路徑。

正式事件清冊 SHA-256 為 `99550186d923590e37289955baf8d867c6f02da16f61e05b3f7a7ea2a508f4a0`；
原版 `START.EXE` SHA-256 為 `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`。

## 正常玩家路徑收據

八條路徑的 event／request 數依序為：career base 3、Subtract 6、Done 9；technical base 8、
Subtract 13、Prev 18、Next 23、Done 28。每條 catalog A/B JSON 一致、request 與 event 一對一，
且 0 miss／drop；移除 request metadata 後與純 event control 相同，三組 framebuffer 逐 byte 相同。

本機可重生收據位於被 Git 忽略的 `workplace/phase76/`，驗證器為
`tools/skill_action_bar_request_receipt.py`。專案 144 項 Python 測試、dosgolem 完整
`go test ./...`、`go vet ./...` 與相關 race detector 均通過。spec 214 已 CONFORMED，
但這不代表操作列中文像素已完成。

dosgolem 本機分支提交為 `6d17fd3`，依專案規範未推送其遠端。
