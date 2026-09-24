# 013 — 第四頁固定劇情輸出端覆繪

狀態：**CONFORMED；僅合法第三頁終態進入第四頁六行，及同執行 page4→page5 Enter 離頁。**
日期：2026-09-22

2026-09-23 限縮驗收：正式 runtime control／2×／3×及同執行 active→clear 收據見
[phase 147](../re/phase-147-story-page4-runtime-ab-pending-audit.md)；後續失敗即關閉稽核
見該文件的追加結論。本狀態不包含完整開機、其他離頁或遊戲內存讀檔。
2026-09-24 跨頁引號標點勘誤後，以新 TSV 與目前本機字型重跑同範圍
control／2×／3×及 active→clear，結果仍通過；新雜湊與像素數見
[phase 147 的追加收據](../re/phase-147-story-page4-runtime-ab-pending-audit.md#2026-09-24跨頁引號標點勘誤後重驗)。

## 範圍、停止線與權利

本規格只授權合法第三頁終態送入既有正常 BIOS Enter 後的第四頁固定六行劇情，及從合法第四頁終態送入同類 Enter 的已量離頁。原版必須先畫英文；繁中只可在 dosgolem RGBA 輸出層覆繪。不得改寫 EXE、OVR、DOS VRAM、CPU／DOS 記憶體、BIOS 鍵盤佇列、答案判定、檔案、存檔或任何原版比較／查找；所有 runtime identity 一律使用原文 hash 與事件 key，譯文不得進語意路徑。

右側姓名與數值、row 24、第五頁內容、其他離頁方式、完整開機玩家路徑與遊戲內存讀檔均排除。原版、state、畫面、倚天來源字型及衍生 `GOLEMFNT` 僅在 ignored `workplace/`；不得入 Git、GitHub 或發行包。

所有位址皆為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址或檔案 offset。原版 `GAME.OVR` SHA-256 為 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。

## 已審查原版證據

| 項目 | 分級 | 證據 |
| --- | --- | --- |
| 六行 identity、順序、row、length、SHA-256、style、entry/post step | 已證實 | [phase 124](../re/phase-124-story-page4-first-glyph-trace.md)、`text/story-page4-events.tsv`；rows 17–22，column 1，length `34/37/33/31/33/24`。 |
| 192 個 glyph 的真實 return 與 ABI | 已證實 | [phase 143](../re/phase-143-story-page4-ready-evidence-draft.md)：每筆 `0763:03D6` opcode `0xCA` 後到 `0763:04FF`，同 SS、相對 `SP+0x12`、ABI 高位遮罩 0。 |
| 六行 safe rectangle 與已量 Enter pre-write | 已證實 | phase 143 的 rows=6 雙重收據：`[8,320)×[136,184)`、`0CF4:1B3A` pre-execution `ES:DI=A000:AA08`、`CX=304`、step `310023777`；48 個 bounded span 全相交，row 22-only 命中、row 23-only 排除。 |
| 繁中來源 | 編輯性 DRAFT | `text/story-page4.zh-TW.tsv`，`runtime-editorial`；不冒稱手冊逐字譯文。 |
| 字型涵蓋 | 已證實（當時本機字型） | [phase 118](../re/phase-118-story-draft-font-rebuild.md) 的正式 loader 對當時 page4 譯文報告缺字 0；當時 TSV 為 57 個文字字元、53 個唯一 Unicode code point。2026-09-24 譯文與字型重驗見 phase 147 追加收據。 |
| 未量離頁／完整玩家路徑／存讀檔 | 未知 | 不得從這一條固定 Enter 收據外推。 |

phase 143 的 rows=6 receipt 為 `workplace/page4-ready-evidence/page4-six-row-ac1f7fb-{a,b}.json`，逐 byte 相同 SHA-256 `4f1bd9940877601138f77e16dfa290d1243566506670db52344f707a94f20f3d`。所用 dosgolem commit 為 `ac1f7fb4f52680f3a96c42c475667ec7a9dd6b2d`；Go `1.26.7`／`golang:1.26.7-bookworm`。絕對 step、SS／SP 只屬收據錨點，不是 runtime identity。

## READY typed contract

adapter 只讀 `GlyphEntry`、`VerifiedFarReturn`、`PreExecutionVideoWrite` 與 execution discontinuity。六行必須按 sequence 1..6 完整 exact-hit：原文 length/SHA-256、caller `0763:04FF`、guard `0763:026B`、mode/repeat `1/1`、背景／前景 `0/10`、row 17..22、column 1；七個 ABI word 高位必須全為 0。每 glyph 還必須驗證 `0763:03D6/0xCA → 0763:04FF`、entry/return 同 SS、`SP+0x12` 與 `entry < return < post`。暫存原文 bytes 僅供 hash，完成後立即丟棄。

只在六行完整且順序正確時原子提交一個 group；partial、duplicate、錯序、identity／style／return／stack／step 漂移、非 READY catalog、缺 key、缺字或不連續執行均失敗即關閉，絕不畫局部中文。TSV 必須恰六筆、key 唯一且與譯文雙向覆蓋、UTF-8/NFC、無控制字元；每行不超過 39 個原版 8px cell。

safe rectangle 固定為 logical `[8,320)×[136,184)`；每列 39×8 logical pixels。2× 使用 16×16 top-pad 字模；3× 中文墨跡 22×22、置於 24×24 output cell。原版 indexed framebuffer 不得修改，RGBA 差異僅可出現在放大後的 safe rectangle。

已量 Enter 離頁只在執行前的 `0CF4:1B3A` 且 `ES=A000` 時，按 `DI/CX` 的 Mode 13h half-open span 與 safe rectangle 做 row-aware intersection。命中即清空 active group、pending 與 candidate，使同 frame RGBA 回到 baseline；未知 write 無清除權。restore、machine stop 或無法證明連續執行的 handoff 必須清空，不得復活舊 group。這只處理已量 Enter，不宣稱解決其他離頁。

## 實作前與 CONFORMED 驗收

可先以 ignored `workplace/page4-ready-atomic-core/` 的可丟棄 typed-core 驗證六行原子提交、DRAFT 拒絕、partial／duplicate、identity／style／return／stack／step、未知／相交寫入、字型缺字與 discontinuity 負例；它不是 production path。

實作後必須由 dosgolem 從同一合法第三頁／第四頁 state 與既有 BIOS 排程重生 control、2×、3× receipt：原版 CPU／DOS／BIOS／file ops／writes／未實作服務、indexed framebuffer 與 palette 必須全等；繁中六行可讀且缺字 0，RGBA safe rectangle 外零差異。page4→page5 的已量 pre-write 必須同 frame 清空，終態 RGBA 與 baseline 逐 byte 相同且無殘字。上述與固定合法正常路徑抽測皆通過後，才可將本規格限縮升為 CONFORMED；其他離頁、完整開機與存讀檔仍須保持未知。
