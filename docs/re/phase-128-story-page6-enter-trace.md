# 第一百二十八階段：第五頁後合法 Enter 的第六頁 trace

狀態：**六行低階 identity 與 page5 失效前緣已確認；已有繁中 DRAFT 譯文，未接 runtime、未升 READY。**

dosgolem source commit `9f6cac6c425a759024d7656dcf2a485049042465` 的 `buckrogers-text-receipt` 在 Docker 暫存重建。前置 state 位於 ignored `workplace/phase123-story-page6-enter/page5.state`（SHA-256 `dcd08e37d9f394d47b1985b5891f0f3c70ba55d2c345bf9296867657f8ee65f6`）；在 step `321000000` 送既有 BIOS Enter（`1c/0d`）至 `330000000`。兩次 receipt 位於 ignored `workplace/page6-next-trace/next*.json`、逐 byte 相同，SHA-256 `1421740fbf5e7d2e6285a24a0d1b85c8070764b11dff8ce87943c6c13531a633`；原版 OVR SHA-256 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。

六筆 row 17–22 均為 `0763:04FF → 0763:026B`、mode/repeat `1/1`、背景/前景 `0/10`、column `1` 的 guarded contiguous run。完整 length/hash/entry/post 已鎖在 `text/story-page6-events.tsv`；右側角色名與 row 24 command/status 均排除。

所有控制流位址均為 dosgolem 實模式 `segment:offset`；`A000:AB48` 是實模式視訊記憶體位址。第一個第六頁 glyph 前，step `321118406` 的 `0CF4:1B3A` 對該位置以 `CX=304` 寫入，第一筆可見 story-region 差異在 x=`11..269`、row `137`。這是 page5 原版失效前緣證據，不授權 runtime invalidation。

低階翻譯代理只依 private 故事框裁切的 row 17–22 建立 `text/story-page6.zh-TW.tsv` 六行
`runtime-editorial` 繁中 DRAFT，並以 `tools/story_page6_catalog.py` 驗證 exact key、NFC、控制字元、
來源與保守 39 格寬度。專名 `CARLETON JURADIAN` 暫保留原文，因尚無可靠固定繁中譯名；
不能把未核實音譯當成手冊術語。譯文不是原版 identity，也不是 runtime 已中文化證據。

全部 17 份正式與 DRAFT 繁中 TSV 的本機倚天 `top-pad` 字型已在無網路 Docker 重建；
manifest 記錄 1014 glyph、字元清單 SHA-256
`91ed941652102ce935a0ff9afd1dd1b85da5964d0f8d53d8a3334a87e4f6d24c` 與 GOLEMFNT
SHA-256 `16e0e8cd687bbcd0f12b8330a47a7eed9519dd861063c41c01388f9ffc41d024`。
dosgolem `cmd/fontcheck` 正式 loader 對全部譯文字元回讀為 `glyphs=1014 coverage=6084`、
缺字零。第三方字型來源與輸出只在 ignored `workplace/phase128-font/`，不入 Git 或公開包。

終態 state／indexed framebuffer 在 ignored `workplace/phase123-story-page6-enter/`；receipt、重生 PNG
與故事框裁切在 ignored `workplace/page6-next-trace/`。本階段不建立正式幾何、watcher、renderer
或 A/B；`confirmed` identity 不等於 READY。
