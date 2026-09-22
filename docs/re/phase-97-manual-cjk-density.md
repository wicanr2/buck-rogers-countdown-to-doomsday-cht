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

同一份 760 字模也用在非手冊介面。可重跑的
[`tools/ui_runtime_smoke.py`](../../tools/ui_runtime_smoke.py) 從已驗證的
`fixed-after-bios-space-100m.state` 走角色建立與技能頁，到 `103500000` 指令步。
它同時載入選單、性別、職業、角色資料、姓名提示、職業技能、技術技能七組正式
catalog／安全矩形。2×／3× 終態各有 17 個有效中文覆繪；核准矩形內變更
16,280／34,778 像素，矩形外皆為 0，原版完整機器／DOS 存態、raw indexed
畫面及原版事件與控制組相等。本機收據：`workplace/phase97-ui-all-receipt/`，
其中 `verification.json` 記錄輸入與字型雜湊，兩倍率各有 PNG 與完整存態比較摘要。
這一條只驗證上述七組正常角色建立路徑；底部操作列及其他遊戲畫面另有工作。

## 還原檢查與界線

從首題已顯示後的原版存態重啟命令，在下個已完成的文字呼叫點
`266585072` 停止。2×／3× 都沒有舊中文圖層，RGBA 等於各自 baseline，
完整原版存態等於控制組。收據：`workplace/phase97-restore-stable/`。
舊測試若停在 `266580000`，通用字元 watcher 仍在呼叫中，命令會拒絕收據；
這是中途停止點的測試條件，不是已驗證的玩家返回或存讀檔流程。

目前仍欠真正遊戲內返回、存檔與讀檔路徑；#14 保持開啟。舊 phase12 state 的
palette 15 為黑，使原版周邊部分英文不可見，仍需新鮮正常路徑確認。
手冊掃描、原版、字型產物、圖片與完整存態均留本機 `workplace/`，不加入 Git。

## 後續 catalog 擴充（2026-09-22）

以中文手冊原圖續補 8 題，正式事件／譯文現為 31／39 題。資料及正文
36×14＝504 字容量驗證通過；跨頁、過長或來源未能唯一確認的 8 題保持英文，
不擅自截斷。審核時將流浪漢段落中的「駭入」改回原圖的「通過惱人安全系統」，
水星段落將倚天來源不支援的「裏」校為同義的「裡」。

正式手冊字元清單目前 845 glyph，SHA-256
`e6016c2473c87fcd2504652fabd0b069354b7abbd3c70281b67dfbaec18c7367`；
10 份 catalog 聯集 880 glyph，字庫 SHA-256
`e62a829593257b6eda1b4f88d056dbdf9c9e4ef6fdf88a11e138f84f6d880d32`。
兩者皆為本機未追蹤的倚天產物，詳細來源與檔案雜湊在
`workplace/phase96-font/buckrogers-ui-eten-top-pad.json`。先前 760 glyph 收據
仍為當時 23 題的歷史收據，不代表現行 catalog。新題目前只通過資料／版面
驗證，未逐題取得正常玩家路徑的執行期 A/B 收據。

使用最新 880 字模重跑已證實的手冊第一題：2× 輸出 SHA-256 仍為
`da3007bc54ecd0e52dd6a7f8979619808e54521ca6e176686403374dcafed5fb`，
3× 仍為 `c6e87ba6267ae12f99f7110c02328e0844c32946e7ad8a77cae70a6bb712206e`；
正文外差異均 0，完整原版存態相等。本機收據：`workplace/phase98-manual-31-first-verified/`。
七組角色建立介面亦以最新字庫重跑，2×／3× 各有 17 個有效 key、矩形外差異 0、
完整存態相等；收據：`workplace/phase98-ui-31-receipt/`。這些重跑仍不擴張到
新增手冊題目的玩家路徑。
