# 第一百八十八階段：真正 Exit 提示身分、色彩與失效邊界

日期：2026-09-23  
狀態：**DRAFT 原版證據；不授權 watcher、TSV、覆繪、READY 或 CONFORMED。**

本階段只補足第一百八十三、第一百八十四與第一百八十七階段未能分清的
row 24 提示本體、六格可見選擇尾碼與兩條正常分支的生命週期。它**不**把
row 12 的舊清除重命名為 Exit，也不使用已不可重生的 `125006330`。

## 固定輸入、工具與權利邊界

- 原版 `START.EXE` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；
  `GAME.OVR` SHA-256：
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 合法加入角色起點 `a-joined.state` SHA-256：
  `1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。
- dosgolem 隔離複本固定於 `cb3ca77c66e4909c5f513b807840e885ab5cb4a3`；
  Docker `golang:1.25.0-bookworm`，實際 Go 為 `go1.25.0`。原版與 state
  分別唯讀掛載；容器使用 `--rm --network none --memory 2g --cpus 2`
  `--pids-limit 512` 與目前 UID/GID。
- ignored 探針為
  `workplace/phase188-exit-prompts-draft/dosgolem-cb3ca77/cmd/exit-prompt-identity/main.go`
  （SHA-256 `bc59d13ac98f012e1a5a13561443c05f015bca744781928b1a77894f2c55e388`）。
  它只輸出長度、SHA-256、ABI style、A000 pre-write 與控制轉場；不保存原文、
  glyph byte、答案或畫面。

所有 `37F1:…`、`0763:…` 是 dosgolem 8086 實模式 `segment:offset`；
`A000 linear` 是線性 video 位址。兩者不可混用。

## 雙重正常路徑收據

兩條路徑均從上述 state，以 Right、Enter、七次 Down、Enter 選到真正 row 21；
其後分別送 N，或送 Y 再送 Y。每條各重跑兩次且 JSON 位元組完全一致：

| 分支 | 收據 SHA-256 | 終態 |
| --- | --- | --- |
| N | `9fcb0aa52ab1e195583edc3e7ce37f487e55d618cb1812f031297dbd9439c2ee` | step `125300000`，`Exited=false`，row 21 再選取 active。 |
| Y→Y | `bf93258e0264b2f334ec75b3d7b4127602e0e41d6fffe6d817e9059c83e156ad` | step `125006324`，`Exited=true`，active 強制為空。 |

`125006324` 與第一百八十七階段原文字 runner／最小 A000 控制組相同；本階段沒有把
`125006330` 視為可重生結果。

## 已證實的文字 identity 與選擇尾碼

三個 dispatcher identity 都經 guarded far-return 取得：

| identity | 長度／SHA-256 | entry → return | caller | style（bg/fg,row,col） |
| --- | --- | --- | --- | --- |
| row 21 選取 | 11／`622af18ec40b9e50d8ee66ca0da3e2071c85104b5fe4e3f07ea3b7ff116a7b4e` | `124714336 → 124722949` | `37F1:175D` | `15/0,21,9` |
| 第一確認提示 | 12／`c38a515358859a10e7a2104cab69fe10ee2d492d94024b7d8f17d69b1a409032` | `124811496 → 124820881` | `37F1:101E` | `0/14,24,0` |
| 第二確認提示（僅 Y→Y） | 30／`35023ac3208312fb1c932ec15a737aae88817925d6cabb26d83281bf755bdcb8` | `124906582 → 124929724` | `37F1:101E` | `0/14,24,0` |

因此兩個 row 24 prompt 本體都是黃色（palette index 14），不是先前尚未量到的
猜測。另有**實際可見的六格選擇尾碼**，由 `0763:026B` 直接 glyph path 繪製，
不是 dispatcher 字串的一部分；不能把它簡化成「Y/N 都白色」。初態在第一提示
column 12–17、第二提示 column 30–35，都有三段：1 格 `0/15`、3 格 `0/10`、
2 格 `15/0`。第一個 Y 後與第二個 Y 後還會重畫相同六格，顏色分段改變；例如
第一個 Y 後的第一提示為 3 格 `15/0`、1 格 `0/10`、1 格 `0/15`、1 格 `0/10`。
每段均有 content-free aggregate glyph SHA-256 及 caller／列欄記錄於 ignored
receipt。輸入 N、Y 的 BIOS 消費已由第一百八十三階段證實；本階段不輸出或散布
可還原的尾碼 glyph bytes。

**結論：Y/N 對應的可見選擇提示確實存在，但其原版配色是 stateful 多色／反白，
不能以「保留白色 Y/N」當 READY 事實。** 其中文化時是否保留、重繪或只保護尾碼，
仍是須經 DRAFT 規格與審查的產品／忠實度決策。

## A000 最早相交與分支生命週期

所有 pre-write 都在寫入**前**由 `WatchWrite` 得到，含同值寫入。

| 分支／現有 active layer | 最早相交 pre-write | 作用 |
| --- | --- | --- |
| N、Y→Y 的 row 21 selected | `124800903`，`0763:184D`，A000 `709192`，像素 `(72,168)`，`15→0` | 先移除 selected row21 layer；早於第一 prompt。 |
| Y→Y 的 q1 | `124906844`，`0763:184D`，A000 `716800`，`(0,192)`，同值 `0→0` | 第二 prompt 正在開始輸出時，使第一 prompt layer 失效。 |
| N 的 q1 | `125251139`，`0763:184D`，A000 `716800`，`(0,192)`，同值 `0→0` | N 返回後的 row24 重畫才首次相交；選單 clear `124905849` 不相交 row24。 |
| Y→Y 的 q2 | **未量到** q2 text-safe rectangle 的後續相交 A000 寫入 | `Exited` 於 `125006324` 前終止；不得虛構清除。 |

N 分支的 row21 普通重畫為 `125219476 → 125228089`，再選取為
`125241454 → 125250067`；因此「N 返回選單」已是正常原版重播證據。Y→Y 則在
q2 guarded return 後仍無 q2 相交 pre-write 即結束 DOS。實作層若將 row21、q1、q2
錯當成單一互斥 active token，會在 N 的重選取與 q1 晚到 pre-write 間錯誤清除；
目前只可把這列為 DRAFT lifecycle 風險，不得直接接到正式 watcher。

## 仍缺且禁止升級的事項

1. row24 的正式 text-safe rectangle、中文候選與 2×／3× containment 尚未重新審查。
2. 六格選擇尾碼的保留／覆繪策略涉及玩家可見忠實度，尚未由使用者決定；不得自行選色。
3. q2 無自然 A000 清除，正式 presenter 的 DOS terminal cleanup 與 control／2×／3×
   same-state A/B 都還沒有。
4. 本階段沒有獨立 READY 審查，故不改正式 watcher、TSV、spec 018 狀態或任何
   CONFORMED 聲明。

Docker 任務結束時沒有留下本案容器；所有新 probe／receipt 均在 ignored `workplace/`，
原版資料未入版控。
