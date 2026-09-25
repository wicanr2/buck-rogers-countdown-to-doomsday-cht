# 第二百三十七階段：職業技能配置表進入

狀態：**已證實／單次重播（字串表）；catalog 整合另案。**

## 按鍵語意

由 `skill504.state`：Down／Up 各只觸發一次內部單值重畫
（"2"／"8"，`0763:09AF`，選取未動、114 字節底行差異），
**Enter 才是進入配置表的鍵**：44 筆 dispatcher 全表重畫
（ignored `workplace/phase237-skill-alloc/skill-seq.txt`），
終點 VRAM `edfdc9b2…`。

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
- 配方可重生：`skill504.state`＋Down,Up,Enter（1M 間隔），
  中間態未存 checkpoint（按需重跑，秒級）。
