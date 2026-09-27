# 第二百七十二階段：手札第 38 則（廢棄飛船）

日期：2026-09-27

## 1. 原版觸發（已證實）

- 路徑：Salvation III → Port → 發射 → 太空中發現廢棄飛船 → 登船（ECL2 區塊 32）。
  以自動探索器（`workplace/phase257-text-window-trace/explore.py`，以遊戲回報的座標探路、
  遇提示與戰鬥自動處理）走到船長日誌的房間。
- 聽完日誌後 `YOU TAKE THE LOG`（`228D:0B79`，旗標 1），接著 `0763:056C` 進入
  `228D:2547`：` and you record IT as logbook entry 38.`，游標 (17,17)——接在同一列後面，
  不像第 41 則另起一列。數字前沒有補白。
- checkpoint：`workplace/checkpoints/logbook38-pre.state`（只存本機）。

## 2. 面板 A/B

| 量測點 | 結果 |
|---|---|
| 6,889M | 面板開啟：「手札第 38 則：威廉博士的錄音」，一頁正文；2×／3× 記憶體雜湊相同 |
| 6,910M（再按一次 Enter） | 回到探索畫面，面板已關閉，無殘留；座標列顯示「23,22 南 01:29」 |

## 3. 小結

手札已在兩個不同模組（ECL1 區塊 17、ECL2 區塊 32）、兩種版面（另起一列、接在同列後面）
驗證開啟與關閉。

## 4. 手札第 50 則（同一艘船，第 3 層）

- 探索器依畫面「ON DECK n」換層：第 2 層（入口）、第 1 層（輪機）探索完後上到第 3 層，
  被寄生植物纏住、奮力掙脫並打倒後 `YOU TAKE IT`（`2516:0B79`），接著
  ` and you record THE PAPER as logbook entry 50.`，游標 (34,19)：從第 34 欄接續，
  整串跨到下一列。checkpoint：`workplace/checkpoints/logbook50-pre.state`。
- 面板 A/B：「手札第 50 則：維生系統紙條」一頁；2×／3× 記憶體雜湊相同。
- 至此三種版面都已驗證：另起一列（41）、同列接續（38）、行中接續並跨列（50）。

## 5. 手札第 21 則（同一艘船，第 4 層）

- 探索器探完第 1–3 層後上到第 4 層，進入貨箱搭成的隱蔽居住區（ECL2 區塊 32），
  `YOU TAKE THEM`（`3332:0B79`，旗標 1），接著 ` and you record THEM as logbook entry 21.`
  （`3332:2547`），游標 (10,20)。checkpoint：`workplace/checkpoints/logbook21-pre.state`。
- 面板 A/B：「手札第 21 則：康琪博士的日記」一頁（三天日記）；2×／3× 記憶體雜湊相同。
- 再按 Enter：回到探索畫面，面板關閉，無殘字；座標列「42,43 北 05:57」由 engine-dispatch
  覆繪（舊家族同一串記為 catalog miss，屬預期分工）。
- 廢棄飛船上的三則手札（21、38、50）都已驗證。

## 6. 手札第 17 則（ECL2 區塊 33，第 7 層）

- 第 5 層起走通風管（`YOU COULD JUST FIT INTO THE AIRSHAFT. DO YOU ENTER?`，Yes／No 選單，
  Yes 為預設）上到第 7 層；探索器在該提示選 No 留在本層。在凌亂的艙房
  `YOU FIND A DIARY`（`1D28:0B79`），接著 ` and you record IT as logbook entry 17.`
  （`1D28:2547`）。checkpoint：`workplace/checkpoints/logbook17-pre.state`。
- 面板 A/B：「手札第 17 則：枕下發現的書」一頁；2×／3× 記憶體雜湊相同。兩筆 catalog miss
  都是座標列（第 15 列、13 字），由 engine-dispatch 覆繪。
- **關閉：未通過（已證實）。** 原版印完訊息後回到冒險選單，敘事窗文字留著；之後按 Enter、
  向左轉，3D 視窗與座標列都更新，但不再進 `056C`，也沒有整窗清除，面板一直蓋著畫面。
- 讀鍵量測（`gt -int-log`，同狀態）：`056C` 返回後只有 `0C10:0303` 的 `int 16h` AH=01 查鍵；
  Enter 送出後才取鍵。修正提案見規格 030 §3.3 關閉條件 4（DRAFT）。
