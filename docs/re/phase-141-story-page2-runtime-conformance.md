# 第一百四十一階段：第二頁四行覆繪的雙倍率同狀態驗收

日期：2026-09-22
狀態：**CONFORMED 僅限第二頁四行與已量到的 page2→page3 Enter 離頁；不是全遊戲中文化或完整開機路徑驗收。**

## 輸入與權利

從私有 `workplace/probe/phase12-before-question.state`（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）
開始，原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`
只讀掛載。control、2×、3×使用同一份私有合法 BIOS 排程、同一停止點
`288000000`；離頁三組另在 `291000000` 排入同一筆正常 Enter，停止於
`298000000`。排程明細只在 ignored 收據，不公開手冊答案或原版 bytes。

工具是本機 dosgolem branch `buck-rogers-cht-output-overlay` commit `2f8c807`、
Go 1.26.7／`golang:1.26.7-bookworm` Docker，`cmd/buckrogers-text-receipt` 與
`cmd/state-compare`。原版位址皆為 dosgolem 實模式 `segment:offset`。20 份
現行繁中 TSV 重建的本機倚天 top-pad GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`，
1024 字模，正式 loader 對 6179 個譯文字元零缺字；來源、字模與 PNG 均留在
ignored `workplace/`。所有正式四筆 event／譯文仍只由版控 TSV 載入。

## 穩定第二頁 A/B

私有 `workplace/phase141-page2-final/{control,2x,3x}/receipt.json` 的 SHA-256
依序為 `273025bc7568fcf1123ff440944bc8628026ddc40e288c7302ae45640ab41536`、
`618d7965d48eb5e145a1395aadf1c30db0d73855258ff6c9f7aa55280e580fb9`、
`99ec6cc1319d1113c791327e40a9feb356c92fda23febf73ed864e05e9a8242c`。
兩倍率皆完整啟用 `.001`–`.004` 四個 key、`drew=true`、缺字 0；2×／3×
安全矩形外像素差均為 0，矩形內分別為 9194／20104，沒有右側或 row 24 差異。
真實 PNG 四行繁中可讀（仍是指定 state 的畫面，不外推完整遊戲）。

移除唯一 output-only `story_page2_overlay` 物件後，control／2×／3× JSON
逐欄相同，包含 BIOS keys／reads、file ops／writes、未實作服務與原版
memory／indexed framebuffer／palette。三組 memory SHA-256 均為
`941fc5bd027a99e0206ca63b17c97caa4e4fc4b53225baaead39ee4808c49497`，
indexed SHA-256 均為
`5521a2f5433fd39f58f502f2d5795655822eb14618ec8ccc5792afc1442daf5e`。
`cmd/state-compare` 對 control→2×、control→3×均 `equal=true`；machine digest
`a8f796824726698bf889810be659cebaa4b91bb86eea70aaa9074cc45bf4fe6c`、
DOS digest `8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`
在雙側相同。

## 已量 Enter 離頁與失敗即關閉

私有 `workplace/phase141-page2-final/{exitcontrol,exit2x,exit3x}/receipt.json`
SHA-256 依序為
`0a2c9465f7bc7e7c3c07c7d464e9e777e99a4e65c068cfe1e86668c795b8a11b`、
`4fd4737220276a4da6225368f2c5d377c7e474f9101e379370e8ce33d42b69d7`、
`543cbe1ca3da337ff30d982b761fe99d06303b2009c6d3e57358b34618e4ac37`。
2×、3×都在 step `291020464`、原版 `0CF4:1B3A`、`ES:DI=A000:AA08`、
`CX=304` 的 **pre-execution** 交集處記錄 `active_keys_before=4`，立即清除
watcher／presenter；終態 active 空、`drew=false`、RGBA 與 baseline 逐 byte
相同、內外像素差皆 0。移除 output-only overlay／invalidation metadata 後，
兩倍率原版 receipt 與 control 逐欄相同；完整 machine／DOS 正規化 state
也分別 `equal=true`，離頁 machine digest
`28f78edbd408e735344604ff8679f4c026f286baac14815e17ef8245df77f7d2`，
DOS digest 同上。

正式 loader 現只接受四個已審核的 READY key／sequence／length／SHA-256／caller／guard
與樣式；雙倍率測試將完整一行改末字後確實觸發 SHA mismatch，而非以單個未完成
glyph 假裝 hash 負例。`TestStoryPage2FailureMatrixNeverDraws` 在 2×／3×各驗
caller／guard／mode／repeat／style／order、hash、partial、restore、return caller／
SS／SP 失敗皆零 event、零 active、`Draw=false`、RGBA 等於 baseline。
`TestStoryPage2UnknownWriteHasNoLifecycleAuthorityAtBothScales` 驗未知 instruction／
非 A000 write 不會清除既有 group、已量交集 write 則清除且不殘留；另外有雙倍率
font miss、non-READY TSV、mixed／duplicate generation，以及 CLI 對 RETF
predecessor／opcode／caller／SS／SP 的失敗即關閉測試。Docker 中相關 package 的
`go vet` 與 `go test -race -count=1` 通過。

本結論只覆蓋上述合法 state、第二頁四行、雙倍率、已量 Enter 離頁和指定負例；
未知離頁方式、完整開機玩家路徑、遊戲內存讀檔與其他故事頁仍未驗，不能據此宣稱
整款遊戲完成繁中化。
