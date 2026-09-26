# 第二百六十九階段：ECL 挑人提問經 dispatcher 印出

日期：2026-09-26

- 太空港控制室手榴彈場景（`workplace/phase257-text-window-trace/cp/l6`）：
  `D 216E:101E` 印出 `WHO FALLS ON GRENADE? `（22 位元組，含一個尾隨空白）於第 24 列
  （已證實，追蹤紀錄）。216E 當時屬 unit `2BA60`，偏移 101E 即共用呼叫端 `OVR:2BA60:101E`。
- ECL catalog 有 `ecl.1.16.05798`（`WHO FALLS ON GRENADE?`，無尾隨空白）與譯文；
  同區塊另有 `ecl.1.16.04909`（`WHO SHOOTS?`）。含空白的整串雜湊不在任何 catalog（已核對）。
- 推論（強推論）：ECL 挑人指令把運算元字串加一個空白後交給 dispatcher 當提示。

## 驗收（規格 029 §2.9）

- 單元測試：無 ECL catalog 時略過；尾隨空白命中並補回；無尾隨空白、開頭空白、大小寫不同、
  譯文過長都不命中；經 dispatcher watcher 畫在第 24 列。
- 手榴彈場景（`l5` 接續、按 G）：第 24 列顯示「誰要撲向手榴彈？」，2×／3×。
  該次收據有 `skill-exit` 家族兩次重設：101E 正規化後被技能離開家族觀察到、事件不符而
  自行重建，屬既有的失敗保護，畫面無影響。
- 七條回歸與上一輪相同。
