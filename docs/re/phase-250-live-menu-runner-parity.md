# 第二百五十階段：選單家族即時元件與 runner 逐位元對照

日期：2026-09-26  
狀態：**已證實／單次重播。**

## 做法

dosgolem fork `42656e7` 的 `LiveMenuRuntime` 只透過唯讀 `StepReader`（CS:IP、SS:SP、
無副作用讀取、palette）重現 receipt runner 的選單家族逐步邏輯：`026F:029C` 清除、
`0763:0424` dispatcher 進入、其餘指令做 guarded return 與 request 套用，並同時維護
2×／3× presenter。runner 新增 `-live-menu-rgba-out`，在同一次執行中並行驅動它，
最後把兩者的 RGBA 逐位元比較。

## 結果

| 路徑 | 起點 | 時間點 | 請求數 | 2× | 3× |
|---|---|---|---:|---|---|
| 存檔→主選單→加入隊伍 | `menu511.state` | 512.6M | 7 | 相同 | 相同 |
| 職業屏→角色頁→命名→職業技能表 | `class500.state` | 501.5M | 44 | 相同 | 相同 |
| 同上 | 同上 | 502.9M | 79 | 相同 | 相同 |
| 同上 | 同上 | 504.7M | 79 | 相同 | 相同 |
| 同上 | 同上 | 506.0M | 92 | 相同 | 相同 |

名冊路徑的 runner 輸出也與第二百四十九階段逐位元相同。

私有收據留在 ignored `workplace/phase250-live-menu-parity/`。
