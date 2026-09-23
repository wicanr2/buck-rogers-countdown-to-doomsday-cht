# 規格索引

只有標為 READY 的規格可以授權正式程式路徑。本目錄包含尚待原版／玩家路徑證據的 DRAFT，以及
不改玩家行為的候選審查工具收據；兩者都不能單獨宣稱覆繪已完成。

| 規格 | 狀態 | 範圍 |
| --- | --- | --- |
| [選單文字輸出端覆繪](001-menu-text-output-overdraw-draft.md) | DRAFT | 第一個功能選單的字串分派事件與未解生命週期。 |
| [手冊查詢繁中段落覆繪](002-manual-paragraph-overlay-draft.md) | DRAFT | 依原版題目 metadata 顯示對應中文段落，保留原版答案判定。 |
| [手冊事件 adapter 整合邊界](003-manual-event-adapter.md) | DRAFT | 指向 dosgolem READY 純核心，並隔離尚未獲准的 hook／renderer 整合。 |
| [dosgolem host 前端與執行期倍率](004-dosgolem-host-frontend-draft.md) | DRAFT | 將 host canvas、輸入隔離、重繪與未決倍率操作語意分開。 |
| [手冊繁中輸出端 presenter 整合](005-manual-runtime-presenter-draft.md) | DRAFT | 將 typed 手冊 request 接到 14 行 RGBA 段落，並明列 lifecycle 與字型 READY 缺口。 |
| [手冊正式字型候選 manifest 驗證器](006-formal-font-candidate-manifest-validator.md) | CONFORMED（候選審查工具） | 審查本機候選的來源、授權 metadata 與 coverage；不採用、建置或散布字型。 |
| [倚天 15 點字型候選輸入契約](007-eten-15-font-candidate-intake-draft.md) | DRAFT | 本機倚天來源、691 glyph coverage、兩個 16×15 對齊 preview 與待決的 production／公開界線。 |
| [倚天 top-pad 本機字型建置器](008-eten-top-pad-local-font-builder-draft.md) | CONFORMED（本機建置器） | 三來源固定身份、691 字模、top-pad、雙檔失敗回復與 dosgolem 回讀已驗證。 |
| [身體圖示畫面文字輸出端覆繪](009-body-icon-overlay-draft.md) | READY（限縮） | 七筆固定文字；只授權已驗 move／refuse／confirm 群組、generation 與 first-write 原子失效契約。 |
| [首屏劇情文字輸出端覆繪](010-story-opening-overlay-draft.md) | READY（僅首屏五行） | 手冊成功返回後五行固定敘事的 guarded glyph identity、文字安全矩形與 row-aware story-region 寫入失效契約。 |
| [第二頁劇情文字輸出端覆繪](011-story-page2-overlay-draft.md) | CONFORMED（僅四行與已量 Enter 離頁） | 雙倍率 runtime、exact identity、真實 far-return／相對 stack、同狀態 A/B、安全矩形與 pre-write 清除已驗；其他離頁、完整開機與存讀檔未驗。 |
| [第三頁劇情文字輸出端覆繪](012-story-page3-overlay-draft.md) | CONFORMED（僅五行與已量 Enter 離頁） | 雙倍率正式 runtime、五行 exact identity、逐筆 far-return、同狀態 A/B 與 pre-write 清除已驗；其他離頁、完整開機與存讀檔未驗。 |
| [第四頁劇情文字輸出端覆繪](013-story-page4-overlay-draft.md) | CONFORMED（僅六行與已量 Enter 離頁） | 六行正式 runtime、雙倍率同狀態 A/B、失敗即關閉矩陣與 page4→page5 pre-write 清除已驗；完整開機及存讀檔未驗。 |
| [第五頁劇情文字輸出端覆繪](014-story-page5-overlay-ready.md) | CONFORMED（僅五行與已量 Enter 離頁） | 五行正式 runtime、雙倍率同狀態 A/B、失敗即關閉矩陣與 page5→page6 pre-write 清除已驗；完整開機及存讀檔未驗。 |
| [第六頁劇情文字輸出端覆繪](015-story-page6-overlay-ready.md) | CONFORMED（僅六行與已量 Enter 離頁） | 六行正式 runtime、雙倍率同狀態 A/B、失敗即關閉矩陣與 page6→page7 pre-write 清除已驗；完整開機及存讀檔未驗。 |
| [第七頁劇情文字輸出端覆繪](016-story-page7-overlay-ready.md) | CONFORMED（僅六行與已量 Enter 進出） | 六行正式 runtime、雙倍率同狀態 A/B、同程序 active 6→0 及完整失敗即關閉矩陣已驗；完整開機及存讀檔未驗。 |
| [第八頁劇情文字輸出端覆繪](017-story-page8-overlay-ready.md) | READY（僅四行與已量 Enter 進出） | 130 return edge、完整英文清除矩形、雙倍率字型幾何與 page8→9 pre-write 已審；正式 runtime／A/B 未完成。 |
