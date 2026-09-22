# 第一百二十二階段：第四頁後合法 Enter 的下一頁 trace

日期：2026-09-22
狀態：**已確認下一個固定劇情頁的五行低階 glyph identity；繁中資料仍為 DRAFT，未接 runtime。**

## 證據範圍

本輪從被忽略的 `workplace/phase104-post-return-enter-4/control.state` 開始，輸入
state SHA-256 為
`48885cadf2bc51d6c44c09e2f220a3bb80bb23487506c0494eecd977613bf07a`，在
`310000000` 送入一筆合法 BIOS Enter（scan `0x1c`、ASCII `0x0d`），執行至
`320000000`。原版 `GAME.OVR` 只讀掛載，SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。

使用 dosgolem `buckrogers-text-receipt`，工作樹 commit
`9f6cac6c425a759024d7656dcf2a485049042465`，開啟 `-glyph-trace`、
`-glyph-return-edge-trace`、`-story-pixel-trace` 與 `-clear-trace`。兩次相同重播
receipt SHA-256 都是
`434b53fa1e0b3d97ef63d31992b493cc0cffc949e9f62e1fecf3618b4ee1902d`，收據在
`workplace/phase120-next-enter/next.json` 與 `next-b.json`。原始 state、原版檔案、
indexed framebuffer 與私有畫面均不進版控。

## 已證實 identity

下方敘事框五行均由 `0763:04FF` 呼叫 `0763:026B`，`mode=1`、`repeat=1`、背景色 `0`、
前景色 `10`，欄位從 `1` 開始，分別位於 row 17–21。五筆 length／SHA-256、entry／
post-call step 由 `text/story-page5-events.tsv` 保存；該檔只保存 content-safe metadata，
不保存原文 glyph bytes。

私有 indexed 畫面複核後，row 17–21 的五筆 identity 對應的是畫面下方五行固定敘事，
不是右側角色名列。右側角色名位於其他 row，未納入本 catalog，也沒有因本輪收據而
宣稱其為固定或可翻譯文字。底部敘事的五筆 length／SHA-256 與畫面行序一致；本階段
分類為「下一個固定劇情頁（page5）」的五行已量測，不是 command loop 完成證據。

## 勘誤

初版草稿曾把 row 17–21 誤讀成右側角色名，並把底部敘事標為未捕獲；這是畫面座標
辨識錯誤，已以私有 `workplace/phase120-next-enter/next.png` 的 row 對照更正。原始
receipt、indexed framebuffer 與畫面不改寫；五筆 metadata hash、caller、guard、步數
保持不變。底部其餘未由本輪 `0763:026B` trace 覆蓋的文字／畫面元素仍不加入 catalog。

## DRAFT 資料與限制

`text/story-page5-events.tsv` 與 `text/story-page5.zh-TW.tsv` 是五行的 DRAFT catalog；
繁中候選只作視覺辨識後的編輯草稿，不能授權 production overlay。驗證器
`tools/story_page5_catalog.py` 會嚴格檢查五筆 identity、caller、guard、色號、row、
步數、DRAFT 狀態、翻譯覆蓋與字寬；`tools/test_story_page5_catalog.py` 覆蓋 hash drift、
非 DRAFT 狀態及 key drift 的失敗案例。

本階段沒有修改原版 EXE、dosgolem production hook、既有 page catalog 或 READY spec。
五行敘事的 caller／guard／length／hash 已有本階段的可重播證據；要升 READY 前，仍需
審查逐字譯文與文字安全矩形，追出下一個轉場的清除／失效邊界，並訂定同狀態及正常玩家
路徑收據。右側人物姓名屬另一輸出區域，不得混入本段固定敘事 catalog。

## 倚天字型涵蓋補驗

第五頁草稿加入後，全部正式與 DRAFT `text/*.zh-TW.tsv` 合併需求增加至 1006 字模。
舊的 997-glyph 本機字型被 dosgolem `fontcheck` 正確拒絕，缺少九個新字；沒有為遷就
缺字而改譯。主代理再以使用者指定的本機倚天三檔唯讀掛載，在 Docker 內重建
16×16 top-pad `GOLEMFNT`，並以正式 loader 對字元清單第二欄回讀：
`GOLEMFNT 16x16 glyphs=1006 coverage=1006`，缺字為零。

字元清單 SHA-256 為 `2a5ea8cf88ea2f55734712b9fbdf90d4a8a11296139b00dff8a274e796dc0d5f`；
本機字型 SHA-256 為 `3530e8e81a5d934a2ddb4bbf9648d9ead6407fa9e357b30e60ddbcc00b53ed2d`；
建置 manifest SHA-256 為 `7610ffaeb2232c5e85f6c57669bbc1ad6737a7cb657b3efabe20412d45cdc955`。
字型、來源與 manifest 只保留在被忽略的 `workplace/phase122-font/`，不可散布。
這只證明草稿字模涵蓋，不是第五頁 runtime 覆繪或版面 A/B 驗收。
