# 第一百六十一階段：加入角色後功能選單的反白與後續清除

**2026-09-23 語意勘誤：**本階段原始 step、caller、格座標及雙重收據保留；
但當時把 step `125100053` 的 Enter 誤判為 `Exit to DOS`。原版 bytes 與
同份事件順序現已證實 Enter 前選取的是 row 12 `Create New Character`，
row 21 `Exit to DOS` 已回復普通。詳細對照與受影響規格見
[第一百八十三階段](phase-183-post-join-exit-identity-corrigendum.md)。下文舊說僅保存
錯誤形成史，不可作現行 Exit 離頁證據。

## 輸入、工具與權利邊界

- 原版 `GAME.OVR` SHA-256：`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 合法起點 `workplace/phase54/a-joined.state` SHA-256：
  `1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。
- dosgolem 本機分支 commit：`1dafb0a857c42fbda7058157b7615e214a64ec64`；
  Docker 內 Go 1.24.13。本文的位址均為 dosgolem 8086 實模式 `segment:offset`，
  文字列及清除格為原版 8×8 格座標，不與 IDA 線性位址混用。
- 從原版正常 Right→Enter 離開名冊，接著以合法 Down 巡過功能選單；當時意圖抽測
  `Exit to DOS` Enter，實際多按一次 Down 而在 row 12 `Create New Character` 選取時 Enter。
  雙重 content-safe receipt 與 320×200 framebuffer 留在
  被忽略的 `workplace/phase161-post-join-menu-selection/`；原版、存態、字型及圖片不入版控。
  `cycle-exit-a/b.json` 均為 SHA-256
  `5b4c8f66ffd72651344c0dbb45de5946d273276b933dc9d4b902d69297841c36`，
  `cycle-exit-a/b.fb` 均為
  `d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd`。

## 已證實的選取重畫

[`post-join-menu-events.tsv`](../../text/post-join-menu-events.tsv) 的七筆固定文字均於
初次畫面經 `37F1:15BD` 輸出，背景／前景色為 `0/10`。後續逐列選取時，同一
原文長度、SHA-256、row、column 的反白重畫由 `37F1:175D` 輸出，色號 `15/0`；
移往下一列的普通重畫由 `37F1:1856` 輸出，色號 `0/10`。兩份原版 receipt 逐 byte
相同，七列均可由正式 TSV 的雜湊反查，不需把原文全文加入版控。

七項依序位於 row 13、14、15、16、18、19、20，column 9。上方角色姓名／數值、
已收錄的其他選單項與底部 row 24 prompt 不屬這七項譯文。正常 Down 期間看到的
`026F:029C` 清除只涵蓋格 `[25,40)×[24,25)`，即像素
`[200,320)×[192,200)`，與七列文字均不相交；不能因提示列重畫就失效整組譯文。

## 已證實的一條 Enter 後清除與停止線（舊離頁解讀已推翻）

選到原版 row 12 `Create New Character` 後的合法 Enter 在 step `125100053` 由 BIOS
`INT 16h AH=00` 消費。該 Enter 之後第一筆與七列相交的 `026F:029C` 清除 pre-write 在
step `125119490`，格 `[1,39)×[2,23)`，換成像素為 `[8,312)×[16,184)`。
七列原文 glyph 的 y 範圍分別為 `[104,112)`、`[112,120)`、`[120,128)`、
`[128,136)`、`[144,152)`、`[152,160)`、`[160,168)`，均被此清除覆蓋。
此 clear 的原始定位仍已證實；但七列 overlay 更早已因 row 20 普通回寫而失效，
它不能作 active overlay 的首次失效邊界，更不能外推真正 Exit Enter、存讀檔或重入。

上述為「已證實」的輸出事件、座標、配色與有限生命週期；七個選項的實際操作語意
仍為「未知」。譯文 [`post-join-menu.zh-TW.tsv`](../../text/post-join-menu.zh-TW.tsv)
是編輯性 DRAFT，不因本收據自動升 READY 或接入 runtime。READY 前仍需逐項中文文字
安全矩形、錨點及溢位策略、原版印字 guard 的可丟棄 typed request／失敗即關閉模型，
以及上述選取／清除世代的原子失效驗證。正式 watcher／presenter 只能在 READY 後實作；
CONFORMED 另需 2×／3×同狀態 A/B 與適用的正常玩家路徑驗收。

## 2026-09-23 勘誤：完整 A000 observer 的較早邊界

本文件的 `026F:029C` step／矩形與「Enter 後第一筆全選單 clear」結論保留；但它不是
完整 Down→Exit cycle 的 active overlay first intersecting pre-write。後續完整 observer 證實，
每代普通／反白重畫前的 `0763:184D` 已先碰到作用中列；row 20 普通回寫後又進入未收錄
row 21 selected，必須 fail-closed，不能假定 layer 活到 Exit。舊收據與結論保留供回查；
新證據見[第一百八十階段](phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)。
舊清除收據保留；其 `Exit` 語意已由[第一百八十三階段](phase-183-post-join-exit-identity-corrigendum.md)
撤回，不能把錯誤解讀本身當成事實。
