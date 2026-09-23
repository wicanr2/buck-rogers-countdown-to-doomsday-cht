# 第二百一十七階段：真正 Exit 問句八列初畫寫入審查

日期：2026-09-24
狀態：**限縮 READY 證據審查；只核准固定合法 Y→Y 路徑的 q1／q2 pending 初畫 writer，不是正式覆繪 A/B。**

## 來源與可重生條件

獨立審查以[規格 021](../spec/021-post-join-exit-prompt-body-only-draft.md)、
[第一百八十八階段](phase-188-exit-prompts-draft-evidence.md)及
[第二百一十六階段](phase-216-exit-q2-glyph-writer-draft-corrigendum.md)為起點。
`START.EXE` SHA-256 為
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`，
`GAME.OVR` 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
合法 `a-joined.state` 為
`1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。
dosgolem 隔離複本 HEAD 為 `cb3ca77c66e4909c5f513b807840e885ab5cb4a3`，
Docker image `golang:1.25.0-bookworm`，Go `go1.25.0`。
原版及存態唯讀掛載；探針與完整收據只在 ignored `workplace/`。

可重生探針位於
`workplace/phase188-exit-prompts-draft/dosgolem-cb3ca77/cmd/exit-prompt-body-writers/main.go`，
SHA-256 `849fce7d59bf9572572c2ae5435edcb32a6915573e6f4fabe4d2ab562a84fc2a`。
兩次固定 Y→Y 重播收據 `q1q2-full-writers-a.json`／`-b.json` 同目錄、
位元組一致，SHA-256 均為
`504da2a889af5ab257b82ac67c80f81e2eb1b9050c9cfc83263d4968f50c1bd0`。
收據逐筆保留 step、A000 段內 offset、像素座標、舊值、新值與同值註記；
沒有原文、字模或答案。原 phase188 探針暫改後已還原，SHA-256
`bc59d13ac98f012e1a5a13561443c05f015bca744781928b1a77894f2c55e388`。

`0763:…` 是 dosgolem 8086 實模式 `CS:IP`；A000 offset 以 320 像素行寬
換算 x/y，與 EXE／OVR 檔案 offset 不同。以下時間窗為 Entry 含起點、
guarded Return 不含終點，只收本體八列的 pre-write（包含同值）：

| 問句 | pending 時窗（step） | 本體矩形（320×200 logical） | `0763:184D` | `0763:1854` | 不重複像素 |
| --- | --- | --- | ---: | ---: | ---: |
| q1 | `[124811496,124820881)` | `[0,96)×[192,200)` | 636 筆，step `124811758–124820771` | 132 筆，step `124811855–124819901` | 768／768 |
| q2 | `[124906582,124929724)` | `[0,240)×[192,200)` | 1,577 筆，step `124906844–124929614` | 343 筆，step `124906941–124928726` | 1,920／1,920 |

主代理在唯讀 Docker 中獨立驗算兩收據雜湊與逐位元組相等；兩組 writer
均只有上述兩個 `CS:IP`，每筆 offset 均符合 `y×320+x` 及對應本體矩形，
不重複像素數恰等於本體面積。`184D` 的同值寫入 q1 為 540 筆、q2 為
1,378 筆；`1854` 的同值寫入 q1 為零、q2 為 81 筆。同值寫入也須觸發
既有 active 層失效判斷，不能僅按像素是否改變決定。

## 獨立審查結論與停止線

**已證實**：在這條固定合法 Y→Y 路徑、兩筆 exact 問句各自的 pending
Entry→Return、各自完整本體八列，`0763:184D` 與 `0763:1854` 都是原版
正常初畫寫入者。這訂正了第一百八十八階段僅記錄「最早相交寫入」容易被
誤讀為唯一 writer 的問題，也證實先前首列型判定
不足以覆蓋下七列。

可對規格 021 作**限縮 READY 修訂**：已辨識 q1／q2 exact Entry 所建立的
pending，只在其同世代 guarded Return 前、對應本體像素相交時，接受這兩個
已量 writer；不對尾碼、其他 row 24 事件、active 後未知 writer、其他位址
或未量路徑作通用白名單。實作仍要把 active 本體任何相交 pre-write
（包括同值）先清層，並以未知 writer、錯序、越界失敗即關閉。

本收據只走 Y→Y，沒有量其他初始狀態、Restore 後重入或 Linux 實體玩家路徑；
也沒有執行正式 watcher＋presenter 的 control／2×／3× A/B。此前首列型程式
得出的 q1／N 暫時綠燈因漏掉下七列 `1854`，已撤回，不得列為 CONFORMED。
正式實作須重跑完整矩形、雙倍率與 N／Y→Y 兩支，確認尾碼／矩形外零差、
原版 machine／DOS／indexed／palette 同狀態及 Stop 無殘字。
