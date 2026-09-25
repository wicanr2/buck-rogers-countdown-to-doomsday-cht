# 規格索引

規格必須先達 READY 才能授權正式程式路徑；CONFORMED 表示已在明示範圍通過實作驗收。
本目錄也包含尚待原版／玩家路徑證據的 DRAFT，以及不改玩家行為的候選審查工具收據；
兩者都不能單獨宣稱覆繪已完成。

| 規格 | 狀態 | 範圍 |
| --- | --- | --- |
| [選單文字輸出端覆繪](001-menu-text-output-overdraw-draft.md) | DRAFT | 第一個功能選單的字串分派事件與未解生命週期。 |
| [手冊查詢繁中段落覆繪](002-manual-paragraph-overlay-draft.md) | DRAFT | 依原版題目 metadata 顯示對應中文段落，保留原版答案判定。 |
| [手冊事件 adapter 整合邊界](003-manual-event-adapter.md) | DRAFT | 指向 dosgolem READY 純核心，並隔離尚未獲准的 hook／renderer 整合。 |
| [dosgolem host 前端與執行期倍率](004-dosgolem-host-frontend-draft.md) | DRAFT；3× 原生倚天字型子契約限縮 READY | A 原生 24 點已接正式畫筆並通過 host-only 像素／2× 往返；原版 DOS／存檔同狀態與可玩入口未驗，不升整體 CONFORMED。 |
| [手冊繁中輸出端 presenter 整合](005-manual-runtime-presenter-draft.md) | CONFORMED（明確 presenter 範圍） | 39 題 catalog／版面／字型預檢與已量題目抽樣、返回清除；其餘逐題執行期、存讀檔及視窗仍待驗。 |
| [手冊正式字型候選 manifest 驗證器](006-formal-font-candidate-manifest-validator.md) | CONFORMED（候選審查工具） | 審查本機候選的來源、授權 metadata 與 coverage；不採用、建置或散布字型。 |
| [倚天 15 點字型候選輸入契約](007-eten-15-font-candidate-intake-draft.md) | DRAFT | 本機倚天來源、691 glyph coverage、兩個 16×15 對齊 preview 與待決的 production／公開界線。 |
| [倚天 top-pad 本機字型建置器](008-eten-top-pad-local-font-builder-draft.md) | CONFORMED（本機建置器） | 三來源固定身份、691 字模、top-pad、雙檔失敗回復與 dosgolem 回讀已驗證。 |
| [身體圖示畫面文字輸出端覆繪](009-body-icon-overlay-draft.md) | CONFORMED（限縮） | 七筆固定文字；move／refuse／confirm 的 control／2×／3× 同狀態、first-write 清除與零污染收據通過。 |
| [首屏劇情文字輸出端覆繪](010-story-opening-overlay-draft.md) | CONFORMED（僅首屏五行與已量 Enter 離頁） | 雙倍率同狀態、零缺字、矩形外零差及同程序 active 5→0 已驗；其他出口與存讀檔未驗。 |
| [第二頁劇情文字輸出端覆繪](011-story-page2-overlay-draft.md) | CONFORMED（僅四行與已量 Enter 離頁） | 雙倍率 runtime、exact identity、真實 far-return／相對 stack、同狀態 A/B、安全矩形與 pre-write 清除已驗；其他離頁、完整開機與存讀檔未驗。 |
| [第三頁劇情文字輸出端覆繪](012-story-page3-overlay-draft.md) | CONFORMED（僅五行與已量 Enter 離頁） | 雙倍率正式 runtime、五行 exact identity、逐筆 far-return、同狀態 A/B 與 pre-write 清除已驗；其他離頁、完整開機與存讀檔未驗。 |
| [第四頁劇情文字輸出端覆繪](013-story-page4-overlay-draft.md) | CONFORMED（僅六行與已量 Enter 離頁） | 六行正式 runtime、雙倍率同狀態 A/B、失敗即關閉矩陣與 page4→page5 pre-write 清除已驗；完整開機及存讀檔未驗。 |
| [第五頁劇情文字輸出端覆繪](014-story-page5-overlay-ready.md) | CONFORMED（僅五行與已量 Enter 離頁） | 五行正式 runtime、雙倍率同狀態 A/B、失敗即關閉矩陣與 page5→page6 pre-write 清除已驗；完整開機及存讀檔未驗。 |
| [第六頁劇情文字輸出端覆繪](015-story-page6-overlay-ready.md) | CONFORMED（僅六行與已量 Enter 離頁） | 六行正式 runtime、雙倍率同狀態 A/B、失敗即關閉矩陣與 page6→page7 pre-write 清除已驗；完整開機及存讀檔未驗。 |
| [第七頁劇情文字輸出端覆繪](016-story-page7-overlay-ready.md) | CONFORMED（僅六行與已量 Enter 進出） | 六行正式 runtime、雙倍率同狀態 A/B、同程序 active 6→0 及完整失敗即關閉矩陣已驗；完整開機及存讀檔未驗。 |
| [第八頁劇情文字輸出端覆繪](017-story-page8-overlay-ready.md) | CONFORMED（僅四行與已量 Enter 進出） | 130 return edge、正式雙倍率 runtime／A/B、完整英文清除矩形及 page8→9 失效已驗；其他路徑未驗。 |
| [加入角色後功能選單輸出端覆繪](018-post-join-menu-overlay-draft.md) | 固定七列路徑限縮 CONFORMED；其餘 DRAFT | 合法加入角色存態的七列重畫與 row20 普通回寫前清層已有正式逐寫入收據、雙倍率同狀態 A/B；真正 Exit、提示、重入與存讀檔仍未驗。 |
| [Linux 前端失敗即關閉 session 回合邊界](019-linux-frontend-session-turn-boundary-draft.md) | 限縮 READY 候選待獨立審查 | 最小 typed session 回合、整批面板鍵盤隔離、零步暫停、step receipt 與失敗後 Close；不含 cold boot、多作用層、存讀檔或可玩前端。 |
| [儲存詢問的名字前後綴覆繪](025-save-prompt-name-affix-overlay-draft.md) | READY | 取代 009 的 save_prompt 固定身分；前後綴比對、名字格保留原版墨跡。 |
| [技能頁離開確認提示繁中覆繪](020-skill-exit-confirmation-overlay-draft.md) | 限縮 CONFORMED（僅兩句本體與固定無頭路徑） | 兩個合法 state 的 Escape→N／Y、2×／3× 正式 A/B 已驗；尾碼零覆繪且終態無殘層。存讀檔、Restore bridge、Linux 視窗與冷開機未驗。 |
| [加入角色後真正 Exit 問句本體覆繪](021-post-join-exit-prompt-body-only-draft.md) | 限縮 CONFORMED（固定 N／Y→Y 路徑、兩句本體） | 正式 watcher／presenter 已完成 2×／3× 同狀態 A/B 與已量生命週期驗收；原版多色六格尾碼保留，其他路徑與 Linux 玩家視窗未驗。 |
| [第九頁固定單行劇情輸出端覆繪](022-story-page9-overlay-draft.md) | 限縮 CONFORMED（固定入頁＋Ctrl+C 退出 DOS 的 Stop 清層） | 正式雙倍率入頁 A/B、同次 active 1→0 與終態零殘層已驗；遊戲內自然離頁與其他出口未知。 |
| [row 15／row 24 命令狀態列輸出端](023-command-status-overlay-draft.md) | 既有 `roster.loading` 第三頁轉場限縮 CONFORMED；其餘 DRAFT | 21-byte 既有 exact key 的 2×／3× 同狀態入頁、自然清層與負例已驗；row 15、33 格直接 glyph 和其他動態身分未核准新譯文或正式接線。 |
| [手冊背景／正文作用層群組與字型身分](024-manual-layer-group-font-identity-ready-candidate.md) | 限縮 READY；正式元件已接線，未達 CONFORMED | 雙層封存投影與 session 字型身分已在本機 fork 實作並通過合成雙倍率負例及首題原版事件投影；caller 來源核驗尚未接入正式 Linux session，正常玩家／存讀檔與多層並存未驗。 |
