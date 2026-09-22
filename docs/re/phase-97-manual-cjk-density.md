# 第九十七階段：手冊 3× 中文密度與第二題

日期：2026-09-22。此階段沿用已確認的 16×16 倚天 top-pad 來源與手冊顯示事件。
使用者檢視實際畫面後確認 2× 可維持，3× 的中文字應放大並縮小字間空隙。
dosgolem 本機提交為 `4b58dc7`，留在 `buck-rogers-cht-output-overlay` 分支，未推上游。

## 3× 版面

原本 3× 輸出字格為 24×24 像素，16×16 中文墨跡留約 8 像素水平空隙。
現在手冊 presenter 在記憶體將中文字模最近鄰取樣為 22×22，置中留約 2 像素；
ASCII 墨跡維持 16×16。2× 完全沿用原 16×16，首題 RGBA SHA-256 保持
`da3007bc54ecd0e52dd6a7f8979619808e54521ca6e176686403374dcafed5fb`。
3× 新首題 RGBA SHA-256 為
`c6e87ba6267ae12f99f7110c02328e0844c32946e7ad8a77cae70a6bb712206e`；
正文內 6591 像素不同，正文外 0。原版完整存態與無覆繪控制組相等。
本機預覽：`workplace/phase97-first-verified/3x.png`。

## 第二題與翻譯審核

低階模型補入原版 page 41、`Technical Skills`、word 2 的事件，對應
`manual.page41.technical_skills.word2` → `manual.rules.technical_skills`。
主代理以中文手冊 `SCAN0352_046.jpg` 原圖（印刷第 87 頁）校正分類；原圖 SHA-256
`cb945ff43ab9d72b407fa87c5e20109cbd4fa4218a01109d402e35c3d81c4367`。
原草稿把智力技能中的仿聲、導航、行星學、程式設計列入技術技能，已刪除，
並按原圖保留 13 項技術技能及其冒險／戰鬥用途。這是譯文訂正，不改遊戲規則。
原版 `START.EXE` SHA-256
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`。

由 `phase12-before-question.state` 排入錯答 `300100000:2d:78`、Enter
`301100000:1c:0d`，至 `301240000` 時第二代 request 確實命中新段落。
2×／3× 正文外差異均為 0，完整機器與 DOS 存態等於控制組；終態只保留第二代
`manual.rules.technical_skills` stamps。收據於本機 `workplace/phase97-next-verified/`；
3× PNG 為 `3x.png`。這證實錯答後換題與舊段落失效，不宣稱 39 題全部翻譯完成。

正式 10 份 catalog 合併的本機倚天字庫由 `tools/eten_font.py` 重建，含 760 glyph，
SHA-256 `6fb92d1bcde389ee02c2953cf175838f21be5dd8782f87aaad40c0837cb29624`；
翻譯、source 與字模的完整 manifest 僅在 `workplace/phase96-font/`。
手冊 catalog 現為 23 段，來源之外不憑 OCR 猜缺頁內容。

## 還原檢查與界線

從首題已顯示後的原版存態重啟命令，在下個已完成的文字呼叫點
`266585072` 停止。2×／3× 都沒有舊中文圖層，RGBA 等於各自 baseline，
完整原版存態等於控制組。收據：`workplace/phase97-restore-stable/`。
舊測試若停在 `266580000`，通用字元 watcher 仍在呼叫中，命令會拒絕收據；
這是中途停止點的測試條件，不是已驗證的玩家返回或存讀檔流程。

目前仍欠真正遊戲內返回、存檔與讀檔路徑；#14 保持開啟。舊 phase12 state 的
palette 15 為黑，使原版周邊部分英文不可見，仍需新鮮正常路徑確認。
手冊掃描、原版、字型產物、圖片與完整存態均留本機 `workplace/`，不加入 Git。
