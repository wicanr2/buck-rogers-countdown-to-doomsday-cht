# 第一百二十三階段：手冊成功返回分支的保存／讀檔入口邊界

日期：2026-09-22
狀態：**已確認保存／讀檔只屬主選單或隊員管理選單；成功返回分支尚未到達該選單，遊戲內保存／讀檔 A/B 未開始。**

## 手冊證據與範圍

本階段只使用被忽略的本機英文手冊快照與中文 Data Card 原圖。英文快照 SHA-256 為
`e8528a31b66d76e7162abe358bff1f27d7d5a5d4070914beee470867e59e728a`；中文原圖
`2F3_SCAN1240_006.jpg`、`009.jpg`、`010.jpg`、`012.jpg` 的 SHA-256 依序為
`9d64f284dda1801d84c6858c037f999e6c57d61e3ef16b12ebfe669e8b3ffd33`、
`e0a52cfa66f9d3ed4e4d0161667e1e0e750457f38199d597f36eecd9cb476240`、
`e99203adacad7b5a8a55598342d4df8c76c9429d2b837d46493dcfe55fd2e8e7`、
`76ef44b47a8cc07eee35642ff66397511e5931d5fd5603a6e93b115c57446900`。原文、OCR 與
掃描影像均只留在 `workplace/`，本文件不收錄可還原的手冊內容。

手冊已證實下列玩家介面契約：

- `LOAD SAVED GAME` 可在主選單或隊員管理選單使用。
- `SAVE CURRENT GAME` 是隊員管理選單的功能，並要求在 A–J 十個槽位選擇一個儲存。
- 主選單的安裝／載入媒體步驟不是遊戲內 save/load，不能混用。
- Data Card 要求數字鍵盤方向操作時 Num Lock 開啟；數字鍵盤 8 為前進。Esc 只取消尚未完成的
  移動，Ctrl+C 是回 DOS，兩者都不是已證實的隊員管理選單返回或保存入口。

因此，先前角色建立分支的保存、名冊與讀取證據（第五十二至五十四階段）雖然證實原版
檔案讀寫，卻不是本手冊成功返回分支的可銜接 checkpoint，不能拼接為本階段驗收。

## 成功返回後的最早可重播狀態

以第一百二十二階段已確認的正常 Enter，從
`phase104-post-return-enter-4/control.state`（310M）重建 page5；輸出 state SHA-256 為
`dcd08e37d9f394d47b1985b5891f0f3c70ba55d2c345bf9296867657f8ee65f6`。在 page5 的穩定狀態
（320M）再送同一條連續劇情 Enter，至 330M 得到 state SHA-256
`d20cbc0bf0b7425ab29b26a59666b91bbd32c1e5776ee9593190b4cd8918fcb5`。

330M 終態只有既有 row 24 command/status identity：原文長度 21、SHA-256
`e920b38b45dd6a828b466a06f4c4c4f63645f1c6a82e488599dc3da46b5280f2`、dosgolem 實模式
caller `0763:1307`、row 24／column 0。這不是主選單或隊員管理選單 identity；沒有觀測到
保存槽、讀檔槽、保存檔寫入或載入 consumer。

## 合法輸入探針與停止線

為排除先前 `ASCII=00` 導航碼未符合 Num Lock 條件，本階段從同一 330M state 明示送入
Data Card 支持的數字鍵盤前進：step `331000000`、scan `48h`、ASCII `38h`。這不是猜測的
按鍵；收據 `forward-numlock.json` SHA-256 為
`abc078693728d5ee7c59c036b7019e6e9a34410099ca3edc891a3ce501b78142`。

至 340M，原始 indexed framebuffer 與 palette 都等於 330M，沒有新的 dispatcher event、
沒有 FileOps、也沒有未實作 DOS／BIOS 服務。另由同一 330M state 無鍵延長至 400M，畫面、
palette、事件與 FileOps 亦不變。這僅證實此 state 尚未接受／呈現該已知前進動作；不能把
row 24、無變化或時間推進推定為可操作冒險狀態，更不能推定有保存入口。

本階段未送 Ctrl+C、Esc、未記載功能鍵或任意選單字母；未改寫原版 state、未建立假存檔，
也沒有使用建角保存分支。因而目前沒有足夠證據執行遊戲內保存／讀檔同狀態 A/B。

## 下一個窄切片

下一步只應在此 330M state 追蹤已排入 BIOS 鍵的原版 keyboard consumer、其條件分支與
後續等待／轉場邊，判斷為何 Data Card 的 Num Lock 前進輸入沒有玩家可見效果。只有先量到
一條通往主選單或隊員管理選單的正常玩家狀態轉移，才可依手冊的 A–J 槽位規則驗證
`SAVE CURRENT GAME`，再從同一玩家路徑驗證 `LOAD SAVED GAME`。在那以前，此分支停止。

## 環境與權利

所有重播在一次性、無網路 Docker 容器內完成，原版只讀掛載至 `/orig`，所有 state、收據和
畫面只寫入被 Git 忽略的 `workplace/phase123-story-page6-enter/`。本階段未修改 dosgolem
production code、原版資料、翻譯 catalog 或正式規格。
