# 第六十七階段：角色姓名輸入畫面靜態文字繁中請求

狀態：已完成

## 目標

由修正後的 dosgolem 固定 state，沿正常角色建立路徑接受角色資料頁並進入姓名輸入畫面；
重用第四十四階段已證實的編輯、確認與取消生命週期，從實際文字事件中隔離可翻譯的靜態文字，
建立 UTF-8 TSV exact catalog 與 guarded runtime `DisplayRequest`，同時確保玩家輸入姓名永遠只走
原版動態顯示與語意路徑。

## 範圍

- 以第六十六階段重建的 `fixed-after-bios-space-100m.state` 為起點，重生進入姓名輸入畫面的
  正常 BIOS 按鍵路徑與 content-safe 事件收據。
- 對照第四十四階段 evidence inventory，逐筆分類靜態提示、既有角色資料欄位重畫、玩家姓名
  回顯與清除事件；保留 caller、原文 SHA-256、長度、row／column、顏色與步數。
- 對可翻譯靜態 identity 建立正式 events TSV 與 `zh-TW` catalog；譯文不得參與輸入、比較、
  存檔名稱、角色名稱或任何原版資料結構。
- 在 `apps/buckrogers` 與 `cmd/buckrogers-text-receipt` 接入 exact watcher／catalog，並以正常
  路徑驗證 request 數量、順序、零錯配與動態姓名 catalog miss。
- 只建立顯示請求與資料閘門；本階段不新增 text-safe rectangle 或繪製中文像素。

## 不在本階段

- 不翻譯玩家輸入的角色姓名，不修改原版按鍵、Backspace、Enter、Escape、存檔或欄位長度。
- 不選定 2×／3×，不處理手冊版面，不把動態姓名納入 catalog。
- 不以直接記憶體注入或跳轉取代正常玩家路徑，也不把階段 44 舊收據直接當成修正後 state 的
  新收據。

## 完成條件

1. 修正後 state 的正常玩家路徑與第四十四階段生命週期一致；任何差異均有分類，不默認接受。
2. 每筆正式靜態事件有 exact identity、來源證據與唯一譯文；動態姓名事件有明確排除規則。
3. runtime 收據中靜態事件逐筆產生正確 `DisplayRequest`；玩家姓名回顯、Backspace 清除與輸入
   消費者不受翻譯資料影響。
4. 正反例資料測試、dosgolem 正式測試／vet／相關 race detector 與專案回歸通過。
5. dosgolem 僅提交本機 branch；專案 `main` 推送並更新相關 GitHub Issues。

## 退出條件

- 若姓名畫面仍含未分類的動態欄位，先留下 catalog miss 並回到事件證據，不以畫面文字猜 key。
- 若既有第四十四階段時點因修正後 state 漂移，以事件 identity 與正常輸入對齊，不放寬 exact
  identity，也不改寫原版狀態強迫舊步數成立。
- 若本畫面沒有任何可安全翻譯的靜態文字，保存完整否定證據並轉往下一條玩家可見文字路徑，
  不製造空 catalog 或虛假完成聲明。

## 完成摘要

- 修正後固定 state 的五鍵正常路徑為 183 個事件；姓名提示 exact identity 唯一產生
  `character.name.prompt` 顯示請求，其餘 182 個事件維持 miss。
- 加送 `A` 的路徑為 184 個事件、仍只有同一筆請求與 183 個 miss；玩家姓名回顯未被
  catalog 命中。
- 兩條路徑各重跑一次，JSON 收據與 indexed framebuffer 均逐位元一致。
- dosgolem spec 206 已升為 CONFORMED；本階段沒有建立安全矩形、繪製像素、選定倍率或決定
  手冊版面。
