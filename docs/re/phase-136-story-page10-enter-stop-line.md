# 第一百三十六階段：第九頁後合法 Enter 的第十頁停止線

日期：2026-09-22
狀態：**未發現新的固定故事行；只確認 command/status 區重畫，未建立第十頁翻譯 catalog。**

## 重播與輸入

本輪從第九頁合法終態 `workplace/page9-next-trace/page9-a.state` 開始，輸入 state
SHA-256 為 `563ed40ba276c6857c57b05344949dec5891e4596ad783a9fc89b805eae8c2a4`。
在 `361000000` 排入一筆正常 BIOS Enter（scan `0x1c`、ASCII `0x0d`），執行至
`370000000`。原版 `GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，只讀掛載。

使用 dosgolem `buckrogers-text-receipt`（工作樹 commit
`b4e1fb74b93fddabcde20c7ac07132604de04471`），在 Docker image
`golang:1.26.7-bookworm` 以 `/usr/local/go/bin/go run ./cmd/buckrogers-text-receipt`
重播；開啟 `-glyph-trace`、`-glyph-return-edge-trace`、`-clear-trace` 與
`-story-pixel-trace`。兩次收據逐 byte 相同：

- receipts：`workplace/page10-next-trace/page10-a.json`、`page10-b.json`
- receipt SHA-256：`a4be4b7ff5db76ab80fa6c1904961a54e20bb8669fc2e6fcaa871f281df427a9`
- indexed framebuffer SHA-256：`0aba8869b347eb07683bf3a74825ccfc36eecbf8feaf96b20cd2ac50c1745df0`
- palette SHA-256：`6ff2334f924ec0eeb8d96fdddd074ba4a74ed43aab6036c32e48805870f3633d`
- `receipt_cmp=0`、`indexed_cmp=0`

兩份終態 savestate 的 raw hash 不同（分別為
`9643b91720a70c06495c4217c0cbc63b180d3d7035e4609412aa9fefc0c6afea` 與
`2b2c5fe91ea4bb70d4f5a1b4fe3fdb07a7835ed4264958a95290f37dc54929b1`）；原始序列化
bytes 不適合作跨次同狀態判準，差異原因本輪未解碼定位。本輪只以逐 byte 相同的 receipt、
indexed framebuffer 與 content-safe metadata 證明所列觀測一致，不宣稱完整持久化 state 相等。

## 精確停止線

兩次收據各有 6 個相同形狀的 dispatcher／glyph run：

- caller `1FEB:2AF5` 的 dispatcher event，`original_length=12`，row 15、column 17、
  background／foreground `0/10`
- 低階 glyph caller `0763:049B`，同一 row／column，每次連續 12 字元
- 每次先由 `026F:029C` 清除 `bottom=15,right=38,top=15,left=17`，再重畫同一區域
- 六次 entry 分別為 `361111677`、`362779419`、`364324276`、`365998070`、
  `367490310`、`368993709`
- 六筆 content-safe original hash 依序為：
  `f79a55d262f6fad8b1c452dff14538a7c9d1d7fe80710a7c32a65d20d2f3e990`、
  `71acf265857c8c3ed8215a92d449ed2d2f189014aef16dd9ec83d7a93f50303c`、
  `fc399efbe66ecb225bed82f042f457e26c87c2f1c550c097f883e016dcd3ae0d`、
  `07bafe8e810d56fb813fe77dea795c8d512ae46230bc917c57c3becbb468eecf`、
  `514f6f6c20881d279579b7896f1cb3b5a74ad4396a14f2d695c49a2637310b84`、
  `a833fa64677710d2b8e776137220154e2fe51ffa965ffadc361c63be3770f66c`

receipt 的 `story_pixel_write` 為 `null`，`glyph_return_edges` 為 0；因此沒有新的
story-region 低階固定敘事 glyph identity。私有檢視圖顯示畫面仍保留第九頁 row 17
固定故事行，新增內容只位於上方 command/status 區。該區為動態／重畫輸出，不能猜譯或
升格成第十頁固定故事。

## 結論與邊界

本輪不建立 `text/story-page10-events.tsv`、`text/story-page10.zh-TW.tsv` 或 validator，
因沒有符合「新固定故事行」條件的事件。第十頁目前的可證實停止線是：一次合法 BIOS Enter
至 `370000000` 只得到 row 15 command/status 重畫，沒有新的固定故事輸出；若要繼續，需
先取得另一個合法玩家狀態／輸入分支，不可把此重畫誤當成翻頁劇情。

原版 state、receipt、indexed framebuffer 與私有 PNG 均留在被 Git 忽略的
`workplace/page10-next-trace/`，未寫入版本控制；本輪未修改第 2 頁、滑鼠資料或原版素材。
