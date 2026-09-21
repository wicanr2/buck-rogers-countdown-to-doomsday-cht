# 第八十八階段：手冊正式 GOLEMFNT 子集的來源與可重生性

狀態：完成（DRAFT 稽核；正式候選缺席）

## 目標

在不散布第三方字型、原版遊戲或手冊素材的前提下，將手冊 22 筆正式繁中段落所需的
691 個碼點，從已存在的本機字型候選建立可稽核的輸入清冊、授權告知與可重生 GOLEMFNT
子集收據。這是規格 005 的字型 READY 前置，不把字型或 presenter 接入正常遊戲 runtime。

## 已確認前提

- `text/manual.zh-TW.tsv` 與 `manual-overlay-layout.tsv` 已由正式 verifier 固定為 22 筆、最大
  236 rune、36×14／504 字容量；其字元需求清單為 691 個 Unicode 碼點。
- 第八十七階段的 `RuntimeManualOverlay` 在 constructor 前要求全部 rune 都有 16×16、32-byte
  glyph；缺字時必須拒絕整個 presenter，不能局部顯示。
- `font/README.md` 僅允許版控字元需求與可重生流程；第三方字型與生成 GOLEMFNT 必須留在
  `workplace/`，且採用前須從實際版本回讀完整授權文字與必要告知。

## 範圍

- 在 Docker 中盤點現有本機字型候選、版本／檔名、SHA-256、授權檔與實際格式；輸入一律只讀，
  metadata、字元清單、建置暫存與收據只寫入被忽略的 `workplace/`。
- 從正式手冊 TSV 決定性重生字元清單，對候選實作完整 691 glyph coverage 與 16×16／32-byte
  回讀；若資料、版本、授權文字或任何 glyph 不完整，失敗即關閉並保留缺口 metadata。
- 先建立 dosgolem DRAFT→READY 規格，清楚區分「候選輸入已盤點」「可重生本機子集」與
  「可散布正式字型」，不得把前兩者誤稱已取得散布授權。
- 以不含原作或第三方字型本體的 verifier／測試，驗證缺檔、缺 glyph、錯誤 header、非 16×16
  字模與雜湊／授權告知漂移均拒絕。

## 不在本階段

- 不下載新字型、不新增或散布第三方字型／GOLEMFNT、也不作法律意見或宣稱發行授權已核准。
- 不接 `RuntimeManualOverlay` 到 command、正常玩家路徑、host Apply、DOS VRAM、BIOS／DOS
  輸入、答案比較、檔案或存檔。
- 不將原版英文、中文手冊掃描、答案或可還原文字寫入 Git、Issue 或公開收據。

## 完成條件

1. dosgolem 字型規格經證據審查後明定候選輸入、雜湊、授權告知、typed manifest、coverage、
   失敗模式與可散布停止線；只有實作與本機回讀符合時才可標為 CONFORMED（本機子集）。
2. 691 glyph 的實際可重生子集可在 Docker 中建置並回讀，或以可追溯的缺口收據失敗即關閉；
   兩者都不得留下 root-owned 檔案或未追蹤字型本體。
3. 專案資料驗證、dosgolem 相關測試、文件、main 推送與相關 GitHub Issue 回寫完成；規格 005
   只在字型前置實際完成時勾選，不因 synthetic fixture 而提前升級。

## 退出條件

- 若本機沒有完整可核對的候選、授權告知或字模 coverage，維持 DRAFT 並在 Issue 記錄精確缺口；
  不下載替代字型或自行假設授權。
- 若正式字型的採用或公開散布條款出現多個合理選項，先依共同決策規則提出單一決策問題；
  未得到使用者選擇前不把候選寫成產品預設或發行包內容。
