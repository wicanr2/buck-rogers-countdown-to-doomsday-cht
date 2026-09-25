# 第二百三十七階段：職業技能配置表進入

狀態：**已證實／單次重播（字串表）；catalog 整合另案。**

## 按鍵語意

`skill504.state` 停在命名提示。輸入的字元由 `0763:09AF` 逐字回顯；
非空名字按 Enter 確認後，進入職業技能配置表，44 筆 dispatcher
全表重畫。

- 正常名字：`BUCK`＋Enter（`workplace/phase243-live-chain-audit/name.txt`）。
- Down／Up 被遊戲讀成數字鍵盤 `2`／`8` 寫進名字；Down,Up,Enter
  會建立名為 `28` 的角色（`skill-seq.txt`、`due.txt`），終點 VRAM
  `edfdc9b2…`。這不是正常玩家命名路徑。

## 字串表（`2684` 系呼叫者）

"Career skill points:" "80 " ／ "Maximum per skill:" "30" ／
"Career Skills" ／ "Points Bonus Total" ／八技能
（Notice、Maneuver in 0G、Use Jetpack、Pilot Rocket、
Pilot Fixed Wing、Drive Ground Car、Pilot Rotor Wing、Drive Jetcar）
各配 Points／Bonus／Total 三值（如 10／14／24），末段重複一輪。
80 點總額、單項 30 上限與第 51 階段實測配置規則一致。

## 邊界

- 本表只有呼叫者＋字串，無前景／背景／列欄；`career-skill-screen`
  家族的逐筆對帳（Issue #71 系）另案。
- 正常命名的配置表 checkpoint 見第二百四十三階段。

勘誤紀錄：WORKLOG 2026-09-25「直播鏈命名提示勘誤」。
