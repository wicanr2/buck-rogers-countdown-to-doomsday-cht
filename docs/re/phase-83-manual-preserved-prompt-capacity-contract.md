# 第八十三階段：手冊保留原題的 504 字容量契約

日期：2026-09-21
狀態：完成（資料與 DRAFT 規格收斂；尚非 presenter 同狀態收據）

## 證據與結論

使用者已採用保留原版頁碼、英文標題與序數的版面。Phase 62 的真實 framebuffer 幾何指定
繁中只可在下方 `[7,312)×[72,184)` 顯示，且不能重新使用 Phase 17 整框 prototype 的
`[7,312)×[7,184)`／36×17／612 字前提。

正式 `text/manual-overlay-layout.tsv` 固定一筆 `manual.paragraph.body`：清除與文字安全矩形同為
`[7,312)×[72,184)`；文字 anchor `(16,72)`，每格 8×8 logical pixels，36 欄×14 行，故唯一
導出單頁容量為 504 字。overflow policy 是 `single-page-reject`，不截斷、不換頁、不送入 DOS
輸入，也不變更原版答案判定。

`tools/manual_overlay_layout.py` 驗證固定 schema、幾何、格線 containment、容量導出與所有正式
catalog 條目；`tools/manual_catalog.py` 以相同 36×14 公式驗證事件映射。兩個測試組皆證實
504 字接受、505 字拒絕。現有 22 筆已逐字校訂段落最長 236 字，均在上限內。

## 範圍邊界

- 已證實：資料與 DRAFT 規格的 production 容量是 504 字。
- 已取代但保留可追溯性：Phase 17／61 的 612 字內容是整框 prototype 與其當時收據，不能作為
  現行實作依據。
- 未知／未完成：dosgolem presenter、原版 `word?` 時機的同狀態覆繪、連續幀失效與 A/B 像素收據。
  本階段沒有修改這些路徑。
