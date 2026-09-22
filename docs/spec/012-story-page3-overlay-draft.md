# 012 — 第三頁固定劇情輸出端覆繪

狀態：**READY；僅五行 typed adapter 契約可接 production，尚非 CONFORMED。**
日期：2026-09-22

## 範圍與權利邊界

只處理第二頁正常 Enter 後、第三頁 bottom story area 的五行固定敘事。原版先畫英文，
dosgolem 只在 RGBA output layer 覆繪繁中；不可修改 EXE、DOS VRAM、原版記憶體、
BIOS 輸入、檔案與存檔、答案判定或譯文的語意用途。right-side 人名／數值、row 24
狀態列、第四頁與其後內容都不屬本規格。原版 state／手冊／畫面、本機倚天字型與
衍生 GOLEMFNT 只准留在 ignored `workplace/`，不得入 Git／GitHub／發行包。

## 原版證據與分級

位址均為 dosgolem 實模式 `segment:offset`。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。

| 項目 | 分級 | 證據 |
| --- | --- | --- |
| 五行 exact identity、順序、長度、SHA-256、樣式與座標 | 已證實 | [第 108 階段](../re/phase-108-story-page3-draft.md)、`text/story-page3-events.tsv`；caller `0763:04FF`、guarded primitive `0763:026B`、rows 17–21、column 1、mode/repeat `1/1`、背景／前景 `0/10`，長度 `34/37/31/37/5`。 |
| 每個 glyph 的真實完成控制流 | 已證實 | [第 139 階段](../re/phase-139-story-page3-return-edge.md)：144 筆皆是緊前 `0763:03D6` opcode `0xCA` 的 RETF 後到 caller；補充的雙重收據逐筆證實相同 SS、`SP+0x12`。 |
| page3→page4 已量 Enter 的最早視訊寫入 | 已證實 | [第 138 階段](../re/phase-138-story-page3-exit-prewrite.md)：`0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304`，step `301108549`；比首個可見差異早 24 step，且早於第四頁 glyph。 |
| 五行繁中候選 | 編輯性 DRAFT | `text/story-page3.zh-TW.tsv`；來源為私有原版畫面語意校對，不是中文手冊逐字譯名。 |
| 其他離頁方式、完整開機玩家路徑與遊戲內存讀檔 | 未知 | 不以這條 Enter 收據外推。 |

第二頁合法終態 state `workplace/phase104-post-return-enter-2/control.state` SHA-256
`b15abdf487f59d982657d1d097c0b38fe3668ca3fd6d15e49c310a5486e238e2`；
第三頁合法終態 `workplace/phase104-post-return-enter-3/control.state` SHA-256
`49d4bb0681269fca1954f3e02cb2cffe93bac48086d607dcfa5d975174750cc0`。
收據由本機 dosgolem branch `buck-rogers-cht-output-overlay` commit `f6579d9`、
Go 1.26.7／`golang:1.26.7-bookworm` Docker 重生。固定 receipt step 與當次絕對 SS/SP
都只是證據錨點，不是 runtime identity。

## READY typed contract

可沿用已 READY 的[第二頁 typed adapter](011-story-page2-overlay-draft.md)之狹窄模式，
但不得直接把第二頁四行 constants 當第三頁資料。第三頁 watcher 只讀
`GlyphEntry{guard,caller,ss,sp,abiWords[7],entryStep}`、
`VerifiedFarReturn{previousAddress,previousOpcode,at,ss,sp,postStep}`、
`PreExecutionVideoWrite{at,es,di,cx,step}` 與明示 execution discontinuity。

五行只在各自完整、按 sequence 1..5 exact-hit original length／SHA-256、caller／guard、
mode／repeat、style、row／column，並驗證每 glyph 真實 far-return、同 SS、相對
`SP+0x12` 及 `entry < post < next entry` 後，才原子輸出一個 group。暫存的原文 bytes
在雜湊後丟棄；export event、presenter、JSON 不得保留原文、答案、ABI 高位或 machine pointer。
TSV 必須精確五個 key、唯一、雙向 coverage、UTF-8/NFC、無控制字元、每行不超過
39 個原版 8px cell，並確認本機 16×16 top-pad 字型涵蓋。缺 key／字模、非 READY
data status、partial、duplicate、順序、caller、style、hash 或 return 漂移都失敗即關閉，
不得畫部分行。

logical text-safe rectangle 為 `[8,320)×[136,176)`，五行各佔 39×8 logical pixels。
2×使用現有 16×16 top-pad 字模；3×中文字墨跡為 22×22、置於 24×24 output cell，
ASCII 仍依既有樣式。原版 320×200 indexed framebuffer 不得改，RGBA 差異只准落在
相應放大後的安全矩形；right-side 動態欄與 row 24 不得覆繪。

已量到的 Enter 離頁候選 gate 是執行 **前** 的 `0CF4:1B3A`、`ES=A000`，並以實際
`DI/CX` 的 Mode 13h row-aware half-open span 是否與 `[8,320)×[136,176)` 相交判定；
命中時應先清空整個 active group 與 pending/candidate，使同 frame RGBA 回到 baseline。
未知 write 不具清除權；restore、machine stop 與無法證明連續執行的 handoff 應清空
衍生層，不能復活舊 group。這只描述已量 Enter 路徑及保守失敗邊界，不聲稱其他
離頁方式已解。

## READY 審查與 CONFORMED 閘門

[第一百四十二階段獨立審查](../re/phase-142-story-page3-ready-review.md)已重算五個 TSV
identity、144 個逐筆 return edge、行界與 39-cell 上限，驗證現行 20 份 catalog
的本機倚天字型覆蓋，並以可丟棄核心測試上述 typed input、原子提交、清除交集與
失敗即關閉負例。這只使五行 adapter 契約升 READY，不是 runtime 驗收。

READY 後可實作第三頁 adapter；再由同一合法原版 state、同一 BIOS 排程的 control、
2×、3×做 A/B：原版 CPU／DOS／BIOS／file ops／writes／未實作服務與 indexed framebuffer／
palette 全等；第三頁五行繁中可讀、零缺字、RGBA 安全矩形外零差異。page3→page4 的
已量 Enter 要同一 pre-write frame 清空，後續與 baseline 逐 byte 相同、無第三頁殘字；
2×／3×各驗 identity、return、partial、duplicate、non-READY TSV、font miss、unknown
write、restore／discontinuity 負例皆零繪製且不改原版狀態。這些由 dosgolem 重生且
正常玩家路徑抽測通過後，才可限縮標為 CONFORMED。
