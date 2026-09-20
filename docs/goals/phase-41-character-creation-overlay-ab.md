# 第四十一階段：性別與職業繁中覆繪倍率 A/B

狀態：完成

## 目標

以 dosgolem 正常玩家路徑產生的性別與職業原版 framebuffer、正式繁中 catalog 與
倍率中立 `xlate` renderer，建立 2×／3× 可丟棄覆繪對照，並證明每筆中文只修改已量得的
文字安全矩形；本階段提供倍率決策證據，不替使用者選定產品倍率。

## 範圍

- 從既有原版文字格座標、完整原文字串寬度與 selection lifecycle 建立性別、職業
  text-safe rectangle 清冊。
- 以正常 BIOS Enter／Down 路徑重生性別 steady／Down 與職業 steady／Down framebuffer。
- 擴充或重用 dosgolem 診斷覆繪工具，使其以同一正式倍率中立核心讀取 menu／gender／class
  inventory、繁中 catalog、安全矩形及 GOLEMFNT。
- 每組 2×／3× 輸出都檢查零缺字、零矩形重疊、安全矩形外零像素差異與 ink containment。
- 每組獨立重生兩次，保存 content-safe 幾何 JSON、PNG 雜湊及人工目視結論。
- 更新研究紀錄與 GitHub Issues；完成測試與衛生檢查後推送專案 `main`。

## 不在本階段

- 不把 2× 或 3× 寫成產品預設。
- 不接入正常玩家路徑的持續 framebuffer renderer。
- 不改變 selected 黑底黑字樣式，不自行美化原版反白。
- 不修改原版 EXE、資料、角色規則、手冊驗證或存檔。

## 成功定義

1. 性別與職業安全矩形都由 exact identity 的 row／column／原文長度導出，並有失敗即關閉驗證。
2. 四個真實原版狀態各有 2×／3× A/B，所有輸出逐檔可重生且安全矩形外零差異。
3. 2× 與 3× 的字格大小、可讀性、留白與最長譯詞容納情形有明確比較，不把偏好寫成事實。
4. dosgolem 診斷規格達 CONFORMED；正式套件測試、`go vet`、相關 race detector 與專案測試通過。
5. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 若任一譯詞在 2× 或 3× 無法留在由證據支持的安全矩形內，該倍率／版面標記為不可行，
  不自動縮字、改譯或擴張矩形。
- 若需要選擇產品倍率、改變 anchor 或美化 selected 樣式，停止該決策分支並交由使用者確認。
