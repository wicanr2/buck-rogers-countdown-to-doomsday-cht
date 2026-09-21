# 第七十七階段：技能操作列覆繪幾何與配色前沿

日期：2026-09-21

## 已證實幾何

Phase 76 真實 career／technical framebuffer 是 320×200 indexed 畫面。底部操作列事件矩形皆為
`y=192..200`；五個正式譯文都是兩字。既有 dosgolem renderer 將 16×16 GOLEMFNT 以 glyph
scale 1 畫在倍率後輸出：2× 安全矩形高 16 output pixels，3× 高 24 output pixels並上下各留
4 pixels。兩倍率都能完整容納字模，不需要擴張 logical 高度。

比較的第二版面是向上擴張到 `y=184..200` 的 16 logical-pixel command band；真實畫面顯示這會
清除原版金色底框，因此已由畫面證據排除。正式候選只保留原事件 exact 矩形：career 三個、
technical 五個，互不重疊，也不侵入技能列或動態數值。

PC-98 Golden Box 參考只支持「CJK 點陣字採整數倍率、命令與內容分區、原生解析度驗收」；
本案沒有採用其 640×400 畫布、裝飾、配色、文案或素材。實際幾何仍由 Buck Rogers DOS
framebuffer 與 Phase 74–76 events 決定。

## 配色事實與待決策

原版 normal 標籤為黑底，第一個英文字元使用 palette 15（白），其餘使用 palette 10（亮綠）；
focus 為 palette 15 白底、palette 0 黑字。繁中不存在自然對應的「英文首字母」；正式譯文也沒有
內嵌快捷鍵字元。

本機 `workplace/phase77/` 已用 Phase 71／73 真實 RGBA、正式兩字譯文與新字型子集建立 2×／3×
可丟棄 prototype：

- `technical-first-white-2x.png`：延續首字白、次字綠；
- `technical-all-green-2x.png`：normal 兩字全綠；
- career 與 3× 有同樣兩組對照。

逐像素檢查證實兩張 technical 2× 圖在 `y<192` 的全部 output pixels 都與 Phase 73 基底相同。
prototype 不納入 Git，也不構成 production 決策。dosgolem spec 215 維持 DRAFT，等待使用者選擇
normal 配色後才能完成證據審查。

dosgolem DRAFT 規格提交為本機分支 `952c596`，依專案規範未推送遠端。
