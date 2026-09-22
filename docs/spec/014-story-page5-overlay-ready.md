# 014 — 第五頁固定劇情輸出端覆繪

狀態：**CONFORMED；僅合法第四頁終態進入第五頁五行，及同執行 page5→page6 Enter 離頁。**
日期：2026-09-22

2026-09-23 限縮驗收：正式 runtime control／2×／3×及同執行 active→clear 收據見
[phase 148](../re/phase-148-story-page5-runtime-ab-pending-audit.md)；後續失敗即關閉稽核
見該文件的追加結論。本狀態不包含完整開機、其他離頁或遊戲內存讀檔。

## 範圍、權利與停止線

本規格只授權第四頁合法終態送入既有正常 BIOS Enter 後的第五頁固定五行，及從第五頁
合法終態送入同類 Enter 的已量離頁。原版必須先畫英文；繁中只可在 dosgolem RGBA 輸出層
覆繪。不得改寫 EXE、OVR、DOS VRAM、CPU／DOS 記憶體、BIOS 鍵盤佇列、答案判定、檔案、
存檔或任何原版比較／查找；runtime identity 一律使用原文 hash 與事件 key，譯文不得進入
語意路徑。

右側姓名、row 24、其他離頁、完整開機玩家路徑與遊戲內存讀檔均排除。原版、state、畫面、
倚天來源字型及衍生 `GOLEMFNT` 僅在 ignored `workplace/`；不得入 Git、GitHub 或發行包。
所有位址皆為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址或檔案 offset。原版
`GAME.OVR` SHA-256 為 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。

## 已審查證據

| 項目 | 分級 | 證據 |
| --- | --- | --- |
| 五行身分、順序、樣式與座標 | 已證實 | `text/story-page5-events.tsv`；rows 17–21、column 1、length `34/38/35/36/25`，caller `0763:04FF`、guard `0763:026B`、mode/repeat `1/1`、背景／前景 `0/10`。 |
| 168 glyph 真實 far-return 與 ABI | 已證實 | [phase 145](../re/phase-145-story-page5-ready-evidence-draft.md)：每筆 `0763:03D6` opcode `0xCA` 後回到 `0763:04FF`，entry／return 同 SS、相對 `SP+0x12`、七個 ABI word 高位全 0。 |
| 已量 Enter 離頁的 pre-write | 已證實 | phase 145 雙重 receipt：pre-execution `0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304`，與 `[8,320)×[136,176)` 相交；首個可見差異晚 24 step。 |
| 繁中來源 | 編輯性 DRAFT | `text/story-page5.zh-TW.tsv` 的 `runtime-editorial`；不冒稱中文手冊逐字譯文。 |
| 現行本機字型 | 已證實（本機） | `workplace/phase138-font/eten-subset.golemfont` SHA-256 `b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`；`fontcheck` 對現行 51 個譯文字元回讀零缺字，2×／3× bitmap 墨跡均在安全矩形內。 |
| 其他離頁、完整玩家路徑、存讀檔 | 未知 | 不得由固定 Enter 收據外推。 |

第五頁 entry receipt 由私有第四頁合法終態重播；離頁 receipt 由私有第五頁合法終態重播。
兩組均見 phase 145 所記 SHA-256、dosgolem commit `9a9b769f355942ce9ff4c258f842e1f138938b3e`、
Go 1.26.7／`golang:1.26.7-bookworm`。固定 step、DI 與絕對 SS/SP 都只是收據錨點，
不得成為 runtime identity。

## READY typed contract

watcher 只讀 `GlyphEntry`、`VerifiedFarReturn`、`PreExecutionVideoWrite` 與明示 execution
discontinuity。五行須按 sequence 1..5 完整 exact-hit：原文 length/SHA-256、caller／guard、
mode/repeat、style、row／column，且七個 ABI word 高位必須全為 0；不得先截成 8 位再比對。
每 glyph 還須驗證 `0763:03D6/0xCA → 0763:04FF`、entry/return 同 SS、相對 `SP+0x12` 及
`entry < return < post`，才原子輸出一個 group。原文 bytes 僅可供 hash 並立即丟棄。

TSV 必須恰五個 unique key、UTF-8/NFC、無控制字元、與譯文雙向覆蓋、狀態為 `proven/READY`，
每行不超過 39 個原版 8px cell。partial、duplicate、錯序、identity／style／return／stack／
step 漂移、非 READY catalog、缺 key、缺字或不連續執行均失敗即關閉，絕不畫局部中文。

logical safe rectangle 是 `[8,320)×[136,176)`。2×／3× RGB(A) 墨跡都只准落在其放大後矩形；
原版 320×200 indexed framebuffer 不得改。已量 Enter 離頁只在執行前 `0CF4:1B3A`、`ES=A000`
且實際 `DI/CX` 的 Mode 13h half-open span 相交時清空 active group、pending 與 candidate；
未知 write 無清除權。restore、machine stop 或無法證明連續執行的 handoff 必須清空且不得復活。

## 審查收據與 CONFORMED 閘門

ignored `workplace/page5-ready-atomic-core/` 的可丟棄核心已測五行原子提交、DRAFT 拒絕、
partial／duplicate、identity／ABI／return／stack／step、font miss、unknown／不相交／已量
pre-write 與 discontinuity 負例；它不是 production path。其 `font_containment.py` 直接解碼
現行 GOLEMFNT，記錄 2×／3×零越界 bitmap 墨跡；這是靜態字型收據，不是 runtime A/B。

READY 後才能實作第五頁 adapter。要升 CONFORMED，必須以 dosgolem 從同一合法第四頁／第五頁
state 與既有 BIOS 排程重生 control、2×、3×：原版 CPU／DOS／BIOS／file ops／writes／未實作
服務、indexed framebuffer 與 palette 必須全等；繁中五行零缺字、RGBA 安全矩形外零差異；
page5→page6 的已量 pre-write 必須同 frame 清空且終態與 baseline 逐 byte 相同、無殘字。
正常玩家路徑抽測、其他離頁與遊戲內存讀檔仍須另證，不得因本 READY 外推。
