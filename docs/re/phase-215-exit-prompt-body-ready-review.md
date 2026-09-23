# 第二百一十五階段：真正 Exit 問句本體限縮 READY 審查

日期：2026-09-24
狀態：**限縮 READY 審查通過；正式 TSV、watcher、presenter 與原版 A/B 尚未實作。**

## 審查輸入與決議

獨立審查逐項核對[規格 021](../spec/021-post-join-exit-prompt-body-only-draft.md)、
[第一百八十三階段](phase-183-post-join-exit-identity-corrigendum.md)的真正 Exit
與舊 row 12 勘誤、[第一百八十七階段](phase-187-exit-stop-six-step-corrigendum.md)
的可重生 DOS 退出點、[第一百八十八階段](phase-188-exit-prompts-draft-evidence.md)
的 N／Y→Y 各雙重原版收據、[第二百一十三階段](phase-213-exit-prompt-font-draft.md)
的倚天雙倍率靜態檢查，以及[第二百一十四階段](phase-214-exit-prompt-body-lifecycle-fake-draft.md)
訂正後的型別化生命週期負例。原版 `START.EXE` SHA-256 為
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；
`GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
原版、存態、字型與完整收據只留 ignored `workplace/`。

READY 只授權兩筆 row 24 exact 問句的**本體**：q1
`[0,96)×[192,200)`，q2 `[0,240)×[192,200)`，均為 320×200 logical
半開矩形。核准的顯示譯文分別為「離開至 DOS」、「遊戲尚未儲存。仍要離開？」；
它們是顯示資料，不進原版語意。q1／q2 後接的六格原版多色尾碼
`[96,144)`／`[240,288)`（同列 y=`[192,200)`）完全不清、不譯、不重畫；
每次正式 Draw 均須驗其 RGBA 零差。這項停止線不宣稱尾碼逐格語意已解。

## 原版事實與候選契約

- **已證實**：兩筆原文長度與 SHA-256、`37F1:101E`、row 24 column 0、
  `bg/fg=0/14`、guarded Entry→Return、上述本體／尾碼邊界；兩條正常分支
  的雙重收據各自逐位元組相同。`37F1:…` 是 dosgolem 8086 實模式位址，
  `GAME.OVR` offset 是檔案位址，A000 寫入是線性視訊位址。
- **已證實**：Y→Y 的 q2 Entry `124906582` 早於 q1 的同值 A000
  pre-write `124906844`，而 q2 guarded Return 是 `124929724`。
  N 返回時 row 21 重新反白早於 q1 本體首筆同值寫入 `125251139`。
  q2 無自然本體 clear，DOS `Exited=true` 的可重生點為 `125006324`。
- **限縮 READY 契約**：q1、q2 逐欄 exact identity 加同世代 guarded
  Return 才建立本體層；q2 只由同 owner 已接受的 q1 exact 事件授權。
  q2 pending 可與 q1 active 共存；已量 q1 pre-write 僅清 q1，不清 q2
  pending；未清 q1 前 q2 Return 必須拒絕。本體任何相交 A000 pre-write
  包括同值寫入都要先清對應層。Stop 為 terminal Closed，Restore
  清層但可由更大 generation 重建；Discontinuity／Fault、錯序／未知
  identity／未知 writer／越界為 terminal Failed，均依規格 021 處理。
- **強推論而非已證實**：已量路徑及 `GAME.OVR` 定長掃描未見 q1
  exact 身分在異境重用；不能保證所有未量玩家路徑都唯一。row 21 Enter
  是原版證據來源，不是正式 watcher 的額外啟用 guard。專案既定的原文、
  callsite、座標加長度／SHA／style 已足以限縮辨識顯示；若另一合法路徑
  重用完全相同的顯示事件，本體譯文仍不改尾碼、輸入或判定。

修正版 ignored `fake_test.go` SHA-256
`50ccb08e7b189a282a12142e90ad85c0b08041b68f019367804274e3fa7ed773`；
主代理以唯讀掛載、無網路 `golang:1.25.0-bookworm`／Go 1.25.0、
`--rm --memory 1g --cpus 2 --pids-limit 128` 與目前 UID/GID 獨立重跑
`go test fake_test.go -count=1 -v`，七組頂層測試及其負例通過。
主代理另在既有 `nectaris-font-subset:20260821` 中獨立重跑
phase 213 字型驗證；兩句 2×／3× 均零缺字、零本體越界、尾碼靜態遮罩
零相交。fake 與靜態遮罩不載入原版 runtime，不能當 CONFORMED 收據。

## READY 後工作與停止線

dosgolem 現有 dispatcher Entry、guarded Return 與寫入前 A000 observer
具備觀測此時序的底層能力；把它們接到正式 Exit owner、建正式 TSV／
watcher／presenter 是**READY 後實作**，不是本審查已完成項目。正式
Restore／Stop 事件來源、其他正常 writer、異境抽樣與 Linux 視窗亦待驗。
實作後須從同一合法原版初態重生 control／2×／3× 的 q1 active、
N 返回、q2 active 與 DOS 退出，核對 machine／DOS、BIOS／FileOps、
indexed／palette 同狀態、僅問句本體有核准 RGBA 差異、尾碼零差與終態
零殘字。未得這些收據前，只能稱限縮 READY，不能稱已中文化或可玩。
工作追蹤在 [Issue #19](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/19)。
