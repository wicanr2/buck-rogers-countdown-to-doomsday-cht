# 第五十四階段：已保存角色的名冊與加入隊伍路徑

狀態：已完成

## 目標

沿用第五十三階段已證實會建立 `A.who`／`A.stf` 的預設 Enter 保存分支，接續正常功能選單
的 Add 操作，驗證原版是否顯示已保存角色、如何選取並加入隊伍，以及此流程實際讀取哪些
保存檔；訂正第五十至五十二階段由不保存分支產生的空名冊結論。

## 範圍

- 從相同 `save-before.state`、pristine `CHARS.DAX` 與空白可寫 scratch 開始，先執行預設
  Enter 保存，再以正常方向鍵與 Enter 進入 Add。
- 在保存完成、Add 名冊、角色選取與加入後第一個穩定畫面各取得可重播 checkpoint；記錄
  dispatcher identity、framebuffer、FileOps、scratch manifest 與檔案 SHA-256。
- 確認 Add 對 `A.who`／`A.stf` 的實際 open／read 行為，並將玩家可見角色列與檔案 consumer
  連成一條證據鏈；沒有讀取證據的欄位不得命名。
- 相同輸入由空白 scratch 獨立重播兩次，區分可決定的事件／畫面／檔案內容與受 DOS 時鐘
  影響的狀態，不用不穩定 memory byte 冒充失敗。
- 原版素材與生成存檔只留在被 Git 忽略的 `workplace/`；不解析或散布可還原的角色內容。
- 完成後推送專案 `main` 並更新 GitHub Issues；若未發現 dosgolem 行為缺口，不修改其正式
  程式碼，也不新增無必要規格。

## 不在本階段

- 不使用 direct-entry、記憶體注入、預製存檔或手動搬運另一輪角色檔取代正常流程。
- 不翻譯名冊／加入後畫面、不接中文 renderer，也不選定 2×／3×。
- 不研究加入隊伍後的完整遊戲玩法；只追到第一個穩定、可辨識的玩家可見邊界。

## 成功定義

1. 真正保存後的 Add 路徑可由同一 state 與空白 scratch 完整重播，且保存檔建立與後續讀取
   都有 content-safe FileOps 收據。
2. 名冊是否顯示角色、選取後如何轉場及第一個加入後畫面均以 framebuffer 與文字事件證實。
3. 兩次獨立重播的事件、framebuffer、scratch manifest 與 `A.who`／`A.stf` 雜湊一致；若
   有明示的時鐘差異，個別列出且不誤稱產品不決定性。
4. 第五十至五十三階段文件中的空名冊／保存結論已按新證據追加勘誤或關閉未知項。
5. 研究文件、CONTEXT、WORKLOG 與 Issues 已更新，專案 `main` 已推送，Docker 與兩個工作樹
   乾淨。

## 退出條件

- 若保存檔已存在但 Add 仍不列出角色，先以 FileOps 與畫面證據區分檔名／目錄、讀檔失敗、
  原版資格判定或 dosgolem 缺口；不得偽造名冊。
- 若加入後立即進入大型新互動畫面，保存第一個穩定邊界後另立窄階段，不在本輪擴張玩法。
- 若出現未實作服務或錯誤平台語意，回到 RE → DRAFT → READY，不由 probe 特例進 production。

## 2026-09-21 完成收據

- 真正保存後，Add 先讀 `A.WHO` 的名冊必要區段並列出角色 `A`；選取後顯示載入提示，完整
  讀取 `A.WHO`／`A.stf`，最後從可加入名冊移除角色。
- 兩次完整重播在正規化 scratch 路徑後的 18-event／2,611-FileOps JSON、framebuffer 與兩個
  保存檔逐 byte 相同；未實作服務為空，沒有修改 dosgolem production code。
