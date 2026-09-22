# 第一百三十八階段：第三頁合法離頁的最早故事區 pre-write

日期：2026-09-22
狀態：**已證實原版輸出寫入邊界；第三頁 catalog／覆繪規格仍為 DRAFT，未接 runtime。**

## 可重播輸入與工具

從第三頁合法終態 `workplace/phase104-post-return-enter-3/control.state` 開始；該私有 state 的
SHA-256 為 `49d4bb0681269fca1954f3e02cb2cffe93bac48086d607dcfa5d975174750cc0`。
原版 `GAME.OVR` 只讀掛載，SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
在 step `301000000` 排入一筆正常 BIOS Enter（scan `0x1c`、ASCII `0x0d`），執行至
`310000000`。這與[第四頁低階收據](phase-124-story-page4-first-glyph-trace.md)是同一合法轉場。

工具為本機 dosgolem branch `buck-rogers-cht-output-overlay` commit `f6579d9`，Go
`1.26.7`、Docker image `golang:1.26.7-bookworm`；用
`cmd/buckrogers-text-receipt` 的 `-story-fill-trace -story-pixel-trace
-glyph-return-edge-trace`。`story_fill_writes` 只記錄實模式 `CS:IP`、`ES:DI`、`CX`
與 step；不含原版字串、VRAM bytes、答案或畫面。輸入與私有收據均留在 ignored
`workplace/page3-prewrite-probe/`。兩次相同重播的 JSON 逐 byte 相同，SHA-256 均為
`b707af7a80fb2322769edb7fdd7aca41afcaa05000afa5173db54ff9ac84df6c`；終態記憶體、
indexed framebuffer、palette 的 SHA-256 分別為
`76f7360c4d973a357c872d9e8531473e3a51ecfac593a9e3c24722920ec40b48`、
`4f9d1bb280724737ca72599c3e7d387c23c076f7e0a8637d8d3ebc9164514bf2`、
`726d468223f5e24b68dae2a5c853f9280a9be3c40990b6e3102ac11968aaba08`。

## 已證實的離頁邊界

全部位址均為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址。監測的文字安全矩形是
logical `[8,320)×[136,176)`（第三頁 rows 17–21）。原版在 step `301108549` 的
`0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304` 首次將既有 fill span 寫入此矩形；
它在第四頁第一個固定故事 glyph entry step `301110011` **之前**。

第一次可見的 indexed pixel 差異較晚，於 step `301108573` 的同一原版指令、
`A000:AB48`、`CX=304`，矩形 `x=9..270,y=137`。兩者相差 24 step，不能把
「首個可見像素差異」錯稱為「最早原版寫入」。收據共記錄 40 筆與五行安全矩形相交的
pre-write；`story_fill_writes` 的 64 筆上限未觸及。

這只授權後續 DRAFT→READY 審查使用「原版 pre-execution 視訊寫入與安全矩形相交」作為
第三頁 active group 的候選清除時機。step、DI、CX 是這次收據錨點，不可寫成 runtime
固定值；也不能從這一條 Enter 路徑推論其他離頁方式、存讀檔或第三頁已中文化。
下一閘門仍須審查五行 exact identity、far-return 相對 guard、譯文版面與字型、失敗即關閉
負例，再升 READY 才能實作覆繪；最後另做 2×／3×同狀態 A/B 和清除同幀驗證。
