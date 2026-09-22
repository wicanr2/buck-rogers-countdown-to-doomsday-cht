# 017 — 第八頁固定劇情輸出端覆繪

狀態：**CONFORMED；僅第八頁固定四行與已量合法 Enter 進出。**
日期：2026-09-23

## 範圍與權利

原版英文先由 DOS 正常繪製；繁中只能在 dosgolem RGBA 輸出端清除
核准矩形後覆繪。不得修改 `GAME.OVR`、原版記憶體、indexed framebuffer、
BIOS 輸入、檔案、存檔、規則或比較／查找。只涵蓋 row 17–20、
column 1 的固定四行。右側動態資訊、row 24、第九頁、其他入口／出口、
完整開機及存讀檔均排除。原版、state、完整事件、畫面與倚天字型只留
ignored `workplace/`，不得加入 Git、GitHub 或公開包。

## 原版證據

原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
位址均為 dosgolem 實模式 `segment:offset`。依
[第一百三十一階段](../re/phase-131-story-page8-enter-trace.md)與
[第一百五十五階段](../re/phase-155-story-page8-ready-prerequisite-evidence.md)，
四行長度 `38/37/33/22`、共 130 glyph，exact identity 存於
`text/story-page8-events.tsv`。entry A/B 逐 byte 相同，130/130 return
edge 均由 `0763:03D6` opcode `0xCA` 返回 caller `0763:04FF`，同 SS、
相對 `SP+0x12`、ABI 高位零；明文低位的 mode/repeat `1/1`、背景／前景
`0/10`、row／column 連續。glyph low byte 由同一 replay 的四行 glyph-run
length／SHA／首尾 step 與 130 edge 序列交叉承諾。

entry 起始 state SHA-256
`e869b67264539aff95ca5929a9858c74475feea47e0c7b3a505ea9cd0aa9a460`；
exit 起始 state SHA-256
`327dc1cb8baf4bee71cdcd0173538af123c47266c8bbf556b28f38d89355b0a9`。
工具為 dosgolem `d42567de27da30b003584a777c63a5f91e8e39d6`、
Go 1.26.7，診斷 runner SHA-256
`8d2b62cebaa38857b0a263c65103467746f853a268ca651febfeccf7af86fa7e`。

## 幾何與失效

完整英文清除／覆繪安全矩形為半開
**`[8,312)×[136,168)`**。最長原文 38 glyph×8 pixels，自 x=8
延伸至 x=311；exit A/B 在 32/32 scanline 均量到 x=8、`CX=304`
的原版 fill。先前只包中文的 `[8,96)` 已勘誤，禁止用作清除範圍。

2×矩形為 `[16,624)×[272,336)`，字模 16×16；3×為
`[24,936)×[408,504)`，24×24 cell、22×22 ink、offset 1。
現行 GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`；
四行譯文零缺字、墨跡零越界。字型勘誤收據 SHA-256
`03b13f401ef7f8be989108f778abcf1e2a9a78dd38427cc7ab79512b7ba21cc8`。

合法 page8→page9 Enter 最早相交 pre-execution write 是 step
`351154334`、`0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304`。
只有該 fill instruction、A000 segment 且逐列半開 span 實際相交安全
矩形時才清 active／pending group；x=7 不交、x=8／311 交、x=312
不交。restore、machine stop 與 execution discontinuity 清空 group。

## READY typed contract 與失敗模式

只有四行依 sequence 1..4 完整命中 length／SHA、caller／guard、style、
row／column、130 return edges、SS／SP、每筆 entry<return 及跨行順序、
ABI 與字型後，才能原子提交。partial／mixed／duplicate、identity／hash／
ABI／RETF／stack 漂移、非 READY catalog、缺 key／譯文／字型、未知回呼
及 discontinuity 均失敗即關閉。不得泛稱 verifier 已證同一行每對相鄰
edge 的全面時間單調；正式實作至少須維持 entry<return 與事件不倒退。

端到端 typed-core 勘誤收據 SHA-256
`dc5b46e364f955910cac31f3f55c6b727cd43dd7a437e89560a24021264924c3`，
直接解析雙重 entry／exit 與同 replay glyph-run JSON；正式 DRAFT catalog
被拒，只用暫存 READY fixture 驗核心。`text/story-page8.zh-TW.tsv` 的
`runtime-editorial` 譯文已逐行校對，但不是手冊逐字引文。

## CONFORMED 收據

本機 dosgolem `c0f6d76b0eb60caa72e74a619c1b981c91b340a5` 已接通正式
watcher／strict loader／presenter／CLI。從同一合法 state 重生的 control、2×、3×
均為四 key、零缺字，RGBA 差異只在安全矩形，正規化 machine／DOS 狀態相等。
同程序合法 Enter 離頁在 step `351154334` 記錄 active 4→0，終態
RGBA==baseline 且無殘字。獨立審查確認正式 2×／3×失敗即關閉矩陣，Docker
定向 test／vet／race 通過。完整收據與證據限制見
[第一百五十七階段](../re/phase-157-story-page8-runtime-conformance.md)。

本結論不涵蓋完整開機、其他入口／出口、右側動態資訊、存讀檔、第九頁或其餘
遊戲文字；這些不得由本頁收據外推。
