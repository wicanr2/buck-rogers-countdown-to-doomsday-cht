# 第二百二十五階段：sealed 路徑真機按鍵消耗首證

狀態：**已證實／僅下述無頭 launcher 序列。** 不含畫面比對、選單語意、
Linux 視窗或存讀檔。

## 實驗

本機 fork `cmd/buckrogers-session` 新增 `-keys`（單字元→BIOS 鍵，
每回合經 `Deliver` 投遞）與 receipt 的 `keys_pending_before／after`
（`session.TickReceipt` 新欄）。無網路 Docker，唯讀原版
（`START.EXE` SHA-256 `58a34a38…466226cf1`），save 為暫存複製：

- 3 回合 × 1M 步、每回合一空白鍵：`dos_calls_committed=1`，
  pending 1→1、2→2、3→3。**開機前 3M 步遊戲不輪詢鍵盤**，
  鍵在佇列累積；投遞本身經 sealed 路徑成功。
- 10 回合 × 10M 步、每回合一空白鍵：每回合 pending 皆 1→0。
  **3M–10M 步之間遊戲開始消耗按鍵**，每回合所投即被取走；
  `Steps==budget`、`BudgetExhausted`、Running、無 fault。

這是第一個真機 sealed 輸入消耗證據：排入（Deliver receipt）與取走
（TickReceipt 前後深度）皆由正式收據表達，無需第二次機器讀取。
按鍵造成什麼遊戲語意變化（選單推進？）須待畫面比對，不在本階段推論。

## 限制

- 所投均為空白鍵；其他鍵、懸置鍵、組合鍵未測。
- 消耗不等於語意：只證佇列深度變化，未證遊戲狀態機轉換。
- 收據與暫存 save 均為本機驗證副產，不入 Git；原版只讀。
