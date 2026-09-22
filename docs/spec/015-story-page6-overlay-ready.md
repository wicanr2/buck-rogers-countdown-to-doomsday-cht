# 015 — 第六頁固定劇情輸出端覆繪

狀態：**READY；僅第六頁六行與已量 page6→page7 Enter 離頁。**
日期：2026-09-23

## 範圍與權利

原版必須先畫英文；繁中僅可在 dosgolem RGBA 輸出層覆繪。不得改寫 EXE／OVR、DOS VRAM、CPU/DOS 記憶體、BIOS 輸入、答案判定、檔案、存檔或任何比較／查找。runtime identity 只用原文 hash 與 event key；譯文不得進語意路徑。

只涵蓋第六頁 rows 17–22 的固定六行與合法第六頁終態的已量 Enter 離頁。右側資訊、row 24、第七頁內容、其他離頁、完整開機與遊戲內存讀檔均排除。原版 state、畫面、倚天字型與衍生字型只留在 ignored `workplace/`，不得散布。

## 原版證據與幾何

原版 `GAME.OVR` SHA-256：`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；位址皆為 dosgolem 實模式 `segment:offset`。依 [phase 149](../re/phase-149-story-page6-ready-prerequisite-diagnostics.md) 與 `text/story-page6-events.tsv`，六行為已證實 identity（rows 17–22、column 1、`0763:04FF`／`0763:026B`、mode/repeat `1/1`、bg/fg `0/10`）。200/200 glyph 已證實 `0763:03D6` opcode `0xCA` 返回 `0763:04FF`、同 SS、相對 `SP+0x12`、七 ABI 高位均為零。

safe rectangle 為 logical `[8,320)×[136,184)`。exit 雙重 receipt 記錄 48 筆相交 fill；最早 pre-execution write 為 step `331026784`、`0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304`。runner `6dcc427…`／SHA `bc9d90…` 對 entry/exit 雙重重生且逐 byte 等於既有 receipt。2×／3×本機字型 containment 分別為 `[16,640)×[272,368)`、`[24,960)×[408,552)`，零缺字。

entry 起始 state SHA-256 為
`dcd08e37d9f394d47b1985b5891f0f3c70ba55d2c345bf9296867657f8ee65f6`；
exit 起始 state SHA-256 為
`d20cbc0bf0b7425ab29b26a59666b91bbd32c1e5776ee9593190b4cd8918fcb5`。
使用 Go 1.26.7、dosgolem 本機 `6dcc42794fc8942451f5e584ba60a7d12b4bd106`
重建的 runner SHA-256
`bc9d90a38fe5ede2dcfe5cd165f1567e81e2ac5430f25ec8e1b8e36c3b2597c7`，
entry／exit 各雙重重播且逐 byte 相等；早期診斷 runner 的精確身分仍未知，
本次重生不倒填舊版本。本機 GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`；
`text/story-page6.zh-TW.tsv` 為編輯性 `runtime-editorial` 譯文，
不能冒稱中文手冊逐字引文。

## READY typed contract 與失敗模式

只在六行依 sequence 1..6 完整 exact-hit length/SHA-256、caller／guard、style、row／column，並驗證真實 return、SS、`SP+0x12`、step 順序與 ABI 高位後，才原子建立 group。partial、duplicate、錯序、hash／style／return／stack／step 漂移、非 READY catalog、缺 key／字型或 execution discontinuity 均失敗即關閉，不得畫局部中文。

僅在執行前 `0CF4:1B3A`、`ES=A000` 的 Mode 13h `DI/CX` half-open span 實際相交 safe rectangle 時清空 active/pending group；未知或不相交 write 無清除權。restore、machine stop 與不連續 handoff 必須清空。

## CONFORMED gate

實作後須由 dosgolem 從同一合法 state、同一 BIOS 排程重生 control、2×、3×：原版 CPU/DOS/BIOS/file ops/writes、indexed framebuffer 與 palette 全等；繁中零缺字，RGBA 僅在安全矩形內有差異。已量 pre-write 必須同 frame 清空，離頁終態 RGBA 與 baseline 逐 byte 相同、無殘字。其他離頁、完整開機與存讀檔仍未驗，不得外推。
