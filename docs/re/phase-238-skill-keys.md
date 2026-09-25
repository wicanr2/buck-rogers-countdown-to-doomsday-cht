# 第二百三十八階段：命名提示的按鍵語意

狀態：**已證實／單次重播各一。**

## 觀測（皆由 `skill504.state` 展開，BDA 定時鍵）

`skill504.state` 停在 `Character name: ` 命名提示，名字為空。

- Escape（504.1M）：被取走（int16-AH00），只重新準備一次
  "Character name: " 字串，VRAM 零差異至 510M。
- Enter×2＋Escape（504／506／508M）：三鍵皆取走，畫面凍結
  （`c58d13c2…` 不變）。空名字無法確認。
- Down,Up,Enter：Down／Up 以數字鍵盤 `2`／`8` 寫入名字，Enter
  確認名字 `28` 後進入職業技能配置表（`edfdc9b2…`，
  `alloc508.state`）。
- `BUCK`＋Enter：確認名字後進入同一配置表（第二百四十三階段）。

## 結論

命名提示只接受非空名字；方向鍵在此屏不是游標鍵，而是被當成數字
字元輸入。`alloc508.state`、`point1.state`、`tech511.state`、
`tpoint1.state` 都承接名字 `28`；以正常名字重建的鏈見第二百四十三階段。

勘誤紀錄：WORKLOG 2026-09-25「直播鏈命名提示勘誤」。
