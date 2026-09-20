# 第五十六階段：保存、名冊與加入隊伍執行期繁中顯示請求

狀態：已完成

## 目標

將第五十五階段已證實的保存→功能選單→名冊→加入隊伍 exact identity 與 UTF-8 繁中
catalog，接入 dosgolem 既有 `apps/buckrogers` guarded post-call watcher，使正常玩家路徑只對
靜態介面文字產生 typed 繁中顯示請求，並以正式雙重重播證實動態角色名維持原始 bytes。

## 範圍

- 先把第五十五階段證據整理成 dosgolem DRAFT spec，逐項審查後才升 READY 並實作。
- 沿用既有 `MenuCatalog`／`MenuRequestWatcher` exact identity 管線，不建立第二套 watcher。
- 擴充收據命令明示載入保存／名冊 catalog；顯示請求只含穩定 event key、text key 與譯文
  rune 數，不輸出或改寫保存內容。
- 由第五十四階段相同真正保存正常路徑完整重播兩次；驗證事件、請求、FileOps、寫入長度、
  終態 framebuffer 與保存檔雜湊決定性一致。
- 對四筆動態姓名事件要求 catalog miss，不得因 miss 放寬 exact identity，也不得翻譯 `A`、
  固定欄寬姓名或 `* A`。
- 完成後更新專案研究、CONTEXT、WORKLOG、dosgolem spec，提交 dosgolem 本機分支與專案
  `main`；只推送專案 `main`，並回寫 GitHub Issues。

## 不在本階段

- 不載入字型、不清除英文像素、不呼叫 renderer，也不選定 2×／3×。
- 不修改原版 EXE、角色檔、存檔／加入控制流或玩家輸入排程。
- 不把動態姓名加入 catalog，不擴張到加入隊伍後的新畫面。

## 成功定義

1. dosgolem 規格依 `RE → DRAFT → READY → implementation → verification → CONFORMED` 完成。
2. 18 筆事件全部完成 guarded post-call；14 筆靜態事件產生對應繁中請求，四筆動態姓名保持
   miss，且零 pending／drop／非預期 miss。
3. 正式雙重重播的正規化收據、framebuffer、FileOps／writes 與保存檔雜湊一致；譯文不影響
   原始語意或檔案行為。
4. catalog malformed、identity 漂移、動態姓名誤納、請求數錯誤及未載 catalog 均有正反例
   測試，所有 dosgolem 正式 packages test／vet／race 與專案測試通過。
5. 文件、Issues 與兩個 Git 工作樹完成稽核；專案 `main` 已推送，dosgolem commit 只留本機。

## 退出條件

- 若既有 watcher 無法區分靜態與動態事件，回到 spec 修正 typed catalog 契約，不以 caller
  特例或姓名內容判斷硬補。
- 若翻譯請求改變 FileOps、保存檔或 framebuffer，視為語意污染並停止升 CONFORMED。
- 若重播發現第五十四階段 identity 漂移，先回到 RE 解釋差異，不更新 fixture 讓測試通過。
