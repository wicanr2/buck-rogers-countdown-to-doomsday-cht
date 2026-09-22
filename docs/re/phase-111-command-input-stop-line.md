# 第一百一十一階段：command input 證據停止線

日期：2026-09-22
狀態：**本文件記錄 phase111 當時的停止線；phase112 已由中文手冊補足轉向按鍵證據。**

## 查核結果

本階段查閱既有正常玩家收據、重播腳本與版本控制中的操作證據。當時現有
phase104 成功返回路徑只證實手冊返回後的 Enter 與連續劇情換頁；沒有保存一筆
「進入 command/status 後，某個移動／查詢鍵已被原版正常接受」的合法 input
identity。早期角色建立、技能頁與存檔腳本雖有方向鍵或功能鍵，但它們屬於不同
畫面與不同 state，不能移植成手冊返回後的命令按鍵。

因此 phase111 當時沒有在 dosgolem 送出猜測的 BIOS scan code，也沒有產生新的
command 畫面或翻譯資料。這是內容安全停止，不是 command loop 已完成的結論；
後續手冊原圖證據與可逆轉向重播詳見 phase112。

## 既有可比證據的保留

phase110 的兩份收據仍保留於：

- `workplace/phase110-command-compare/a/receipt.json`
- `workplace/phase110-command-compare/b/receipt.json`

它們分別在 `300000000` 與 `301000000` 排入 Enter，row 24 identity、caller、
幾何、顏色與 indexed framebuffer 均相同。這只能確認目前可重播的穩定
command/status 輸出，不能提供另一個遊戲狀態來分割固定介面詞與動態欄位。

## 下一個解鎖條件

只有取得一筆有來源的正常玩家操作證據（手冊明示按鍵，或既有 dosgolem 正常
路徑收據明示 scan／ASCII、state 與結果）後，才可在同一 state 送入該鍵，對
row 24 與上方區域做 exact diff。若 diff 證實不變固定詞，再建立 DRAFT TSV、
validator 與安全矩形；在此之前所有 command/status 欄位維持原文與 miss。
