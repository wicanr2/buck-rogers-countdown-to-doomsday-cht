# 第四十二階段：確認職業後的下一畫面文字路徑清冊

狀態：已完成

## 目標

從既有固定 state 依序送出四次正常 BIOS Enter，接受預設種族、性別與職業，量測下一個
玩家可見畫面的文字事件與 framebuffer，建立 content-safe、可重播且失敗即關閉的正式收據。

## 範圍

- 先以可丟棄 probe 確認第四次 Enter 的安全時間、轉場完成邊界與新畫面事件數。
- 只為辨識事件語意而以原版 bytes／雜湊作一次性核對；正式檔案不得保存英文全文。
- 保存每筆新增事件的完整 length、SHA-256、runtime caller、色號、row／column、語意角色與
  推論等級。
- 以 dosgolem 正常 BIOS 輸入獨立重跑兩次，固定 JSON 與 64,000-byte indexed framebuffer。
- 建立正式 inventory、嚴格 verifier、正反例測試、dosgolem 診斷規格及研究文件。
- 完成測試與衛生檢查後，提交 dosgolem 本機分支、推送專案 `main` 並更新 Issues。

## 不在本階段

- 不翻譯新畫面、不建立繁中 catalog 或 renderer。
- 不送方向鍵、Escape 或第五次 Enter，不外推尚未走過的角色建立分支。
- 不選定 2×／3×，不修改原版角色屬性、亂數、規則或存檔。

## 成功定義

1. 第四次 Enter 由正常 BIOS 輸入送出，沒有 direct-entry、狀態注入或測試專用跳關。
2. 新增事件均由 guarded post-call 完成，具有 exact identity 與可回查的語意證據。
3. 兩次正式收據與 framebuffer 各自逐 byte 相同，並固定 state、原版與 command 雜湊。
4. verifier 對 schema、排程、事件數、次序、step、identity、輸入或畫面漂移失敗即關閉。
5. dosgolem 規格達 CONFORMED；正式套件測試、`go vet`、相關 race detector 與專案測試通過。
6. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 若畫面需要亂數且目前無法固定，依 RND() 鐵則先建立受控 seed 證據，不挑選碰巧結果。
- 若第四次 Enter 觸發會改變正式角色規則、資料格式或玩家體驗的新分支，只保存原版觀測，
  不實作推測行為。
