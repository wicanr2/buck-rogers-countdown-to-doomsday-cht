# 第四十四階段：角色姓名輸入的編輯、確認與取消生命週期

狀態：已完成

## 目標

從第四十三階段相同固定 state，沿四次 Enter 與 `N` 接受能力值的正常 BIOS 路徑到達姓名
提示，量測可見字元輸入、退格、Enter 確認與 Escape 取消的實際行為，建立 content-safe、
可重播且失敗即關閉的姓名輸入生命週期收據。

## 範圍

- 先以獨立 probe 分支測試 ASCII 字元、Backspace、Enter 與 Escape，不修改原版記憶體。
- 以事件、indexed framebuffer 與後續畫面辨識輸入語意，不以其他 Gold Box 遊戲經驗猜測。
- 正式驗證至少涵蓋一條「輸入→退格」編輯路徑及一條非空姓名 Enter 確認路徑；若 Escape
  有可見作用，再納入取消分支。
- 固定 state、七鍵以上的 BIOS 排程、輸入文字、事件 identity、終點 framebuffer 與原版／
  命令雜湊；正式事件只保存必要的短測試輸入或雜湊，不保存原版英文全文。
- 建立嚴格 verifier、正反例測試、dosgolem 診斷規格與研究文件。
- 完成測試與衛生檢查後，提交 dosgolem 本機分支、推送專案 `main` 並更新 Issues。

## 不在本階段

- 不把玩家姓名翻譯或改寫，不改姓名長度、允許字元、角色資料或存檔格式。
- 不追入確認姓名後的完整下一子系統；只量到第一個穩定玩家可見邊界。
- 不建立角色資料頁繁中 catalog 或 renderer，不選定 2×／3×。

## 成功定義

1. 正常 BIOS 輸入證實字元追加、Backspace、Enter 與可判定的 Escape 行為。
2. 正式分支各從相同 state 獨立重播兩次，JSON 與 64,000-byte framebuffer 逐 byte 相同。
3. 清冊區分原版提示、玩家輸入回顯、轉場重畫及下一畫面事件，並保留 exact identity／step。
4. verifier 對輸入排程、事件數、次序、step、identity、輸入、畫面及輸入雜湊漂移失敗即關閉。
5. dosgolem 規格達 CONFORMED；正式套件測試、`go vet`、相關 race detector 與專案測試通過。
6. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 若 BIOS 鍵未到達遊戲 consumer，先量鍵盤緩衝區與等待邊界，不以記憶體注入繞過。
- 若 Enter 確認直接觸發大型新子系統，只保存第一個穩定轉場邊界並另開後續切片。
- 若 Escape 行為沒有可見差異，只保存負面證據，不宣稱它具有取消語意。
