# 第四十階段：職業選擇繁中執行期顯示請求

狀態：完成

## 目標

將第三十八、三十九階段已證實的職業選擇文字 identity，接入 dosgolem 既有 exact catalog
與 guarded post-call watcher，讓正常三次 Enter、Down／Up 與 Escape 路徑產生可重播的繁中
顯示請求；本階段不載入字型、不繪製像素，也不預先決定 2×／3×。

## 範圍

- 從中文說明書或既有正式專案證據核對職業選擇提示與五個職業譯名；證據不足者不得猜補。
- 建立職業事件 inventory 與 UTF-8 繁中 catalog，涵蓋初始 normal／selected 及已量得的
  Down／Up variant。
- 先建立 dosgolem READY 規格，再擴充共用 catalog loader 與 receipt command；不得另造
  第二套 watcher 或模糊比對。
- 由正常 BIOS 路徑重播 steady、Down→Up 與 Escape，驗證 request 次序、譯文字數、零
  pending／drop，以及只對 exact identity 命中。
- 建立專案 validator、正式收據、正反例測試與研究文件。
- 完成 Docker 測試與衛生檢查後，提交 dosgolem 本機分支、推送專案 `main` 並更新 Issues。

## 不在本階段

- 不載入 GOLEMFNT、不清除英文像素、不繪製繁中 framebuffer。
- 不選定產品倍率，不改寫 2×／3× 待決策狀態。
- 不翻譯尚未量得的其他種族／性別分支或確認職業後畫面。
- 不修改原版 EXE、資料、角色規則、手冊驗證或存檔。

## 成功定義

1. 所有譯詞均有來源類型與可回查證據；無法證實的項目保持失敗即關閉。
2. 正常三 Enter 的 22 個文字事件全部得到 exact 顯示請求；Down→Up 新增四筆 exact 請求。
3. Escape 只對已納入 catalog 的既有事件命中；返回功能選單的不同 identity 必須形成七次
   catalog miss，且不誤沿用職業請求。
4. 三條正式路徑各重播兩次，JSON 逐 byte 相同，request 數、次序、key 與譯文字數固定。
5. dosgolem 規格達 CONFORMED；正式套件測試、`go vet`、相關 race detector 與專案測試通過。
6. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 中文說明書與現有正式證據若不能支持某譯名，該鍵不進 catalog，並在研究文件列為未知。
- 實作若要求改變共用 catalog 格式、玩家可見幾何或倍率預設，停止該分支並先取得使用者決策。
