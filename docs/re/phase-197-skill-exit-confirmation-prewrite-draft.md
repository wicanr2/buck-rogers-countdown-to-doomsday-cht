# 第一百九十七階段：技能頁離開確認提示的 pre-write、尾碼與矩形 DRAFT

日期：2026-09-24
狀態：**DRAFT 原版證據；不授權正式 watcher、TSV 改動、覆繪、READY 或 CONFORMED。**

本階段只補第一百九十一階段明列的三項缺口：兩頁提示文字區的實際 A000
最早相交 pre-write、原文 dispatcher 外的可見選擇尾碼，以及可供後續版面審查的
logical text-safe rectangle。它不改變 `text/skill-exit-confirmation.zh-TW.tsv`，亦不把
中文寫進原版的輸入、比較、存檔或判定路徑。

## 固定輸入、工具與位址空間

- 原版 `START.EXE` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；
  `GAME.OVR` SHA-256：
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 本階段唯一的直接 prompt／glyph／A000 證據起點是
  `workplace/phase66/fixed-after-bios-space-100m.state`，SHA-256
  `209a78934d9936fd9b6a9e28cd5e51da294dd459b4ce6abab47a36a284aa2cc5`；原版目錄以
  唯讀方式掛載至 `/orig`。所有重播在 Docker `alpine:3.20`、`--network none`、
  `--memory 1g`、`--cpus 1`、`--pids-limit 128`、目前 UID/GID 下執行。
- 收據 runner：`workplace/phase52/skill-exit-receipt-20260924`，SHA-256
  `9413e4713019d0445feedb55929c7f3ed1b35f2a6d454777b09184118b5832df`；其輸出與
  `dosgolem/probe` 的 `WatchWrites` 只留在 ignored `workplace/`／暫存研究區。
  前者 `go version -m` 為 Go 1.26.7、dosgolem 基底 `540a5228e539`；
  實際 probe 是 ignored `workplace/dosgolem/probe`，SHA-256
  `0bbb7cb1807367556f0fc5a69692a5aa2c05c821ed3170ca9f8c714b65fdd39a`，
  `go version -m` 為 Go 1.24.13、模組基底 `e6212fc85a9e+dirty`。
  這兩個是不同版本的診斷執行檔；不能把其中一個的位址或收據冒稱由另一個產生。
- `37F1:…`、`0763:…` 均為 dosgolem 8086 實模式 `segment:offset`；`A000` 為線性
  Mode 13h video 位址。watch 輸出中的 `0763:1855` 是觀測器回報的 IP；依第七十四
  階段既有 renderer 定位，它緊鄰背景／前景 glyph 寫入 primitive，不能與檔案 offset
  混用。

## 私有收據與可重播命令

下列皆為本機私有、未版控的 `workplace/phase197-skill-exit-confirmation/` 收據，
並非可散布素材：

| 收據 | 路徑 | SHA-256 |
| --- | --- | --- |
| career instruction trace | `skill-exit-career-instruction-trace-20260924.json` | `47d42ac5865be21822dda9a86a98d83220f67601370e7c79b0b5a3acd2d7d528` |
| career glyph trace | `skill-exit-career-glyph-trace-20260924.json` | `732fc2f0444ff7c52969860e8a0cd01172b4ffc283fae7785a8384b4afa58de5` |
| career A000 watch | `skill-exit-career-prompt-a000-20260924.txt` | `1ad9d30c43856bea0666103c80c6d6049e432311ba2f5598bc60f51767109fe6` |
| career Escape 前 state | `skill-exit-pre-esc-102700000.state` | `fd64f35d19c855eef9f8f6e44357ed2aa295b89ff329bc35ee4cefd8eb4fbaa9` |
| technical glyph trace | `skill-exit-technical-glyph-trace-20260924.json` | `c90b1c37be485dd7c5e0be8bb78e31c2c44464c82025921067f2245812654022` |
| technical A000 watch | `skill-exit-technical-prompt-a000-20260924.txt` | `c89027874468701fe1817039733484452dc439694951393a3cf798a4d27abf9a` |
| technical Escape 前 state | `skill-exit-pre-esc-103600000.state` | `2302ceede2daff8df0de42ff3cf7fc2e346ac89f64ff2b715b0be281fddb9a8e` |

以 runner 從 phase66 state 建立 career Escape 前 state 的精確鍵排程為：

```text
skill-exit-receipt-20260924 -state fixed-after-bios-space-100m.state -until 102700000
  -bios-key-at 100010000:1c:0d -bios-key-at 100240000:1c:0d
  -bios-key-at 100400000:1c:0d -bios-key-at 100650000:1c:0d
  -bios-key-at 101400000:31:6e -bios-key-at 102050000:1e:61
  -bios-key-at 102150000:1c:0d -state-out skill-exit-pre-esc-102700000.state
```

再將同一原版唯讀掛到 `/orig`，用 `dosgolem/probe`：

```text
probe -load-state skill-exit-pre-esc-102700000.state -steps 102730000
  -bios-keys "$(printf '\033')" -bios-key-from 102700000 -bios-key-every 1000000
  -watch a0000-affff -watch-file skill-exit-career-prompt-a000-20260924.txt
```

technical 版本多加 `102900000:15:79`、建立 step 改為 `103600000`；probe 的 state、
起始／終止 step 改為 `skill-exit-pre-esc-103600000.state`、`103600000`／`103640000`。
上述 `printf` 必須在 Docker 容器內執行；此舊 probe 只有 `-bios-keys`，
沒有較新原始碼的 `-bios-key-names`。主代理以同一唯讀原版與上述兩個
pre-ESC state 分別重跑，career／technical `-watch-file` 的 SHA-256 均與表中相符。
glyph 收據則加 `-glyph-trace -glyph-return-edge-trace`：career 為
`-glyph-trace-from 102700000 -until 102800000`，technical 為
`-glyph-trace-from 103600000 -until 103700000`，並沿用各自完整 BIOS 排程。

## 已證實 prompt 與尾碼形狀

兩個 dispatcher prompt 仍維持第一百九十一階段的已證實 identity：caller
`37F1:101E`、`bg/fg=0/13`、row 24、column 0。職業頁 entry→return 為
`102701085→102726497`，長 33、SHA-256
`65108526a62ebc58d90c1406cce2b83133f5a8fa5221f87e6f62f40589bc07a9`；技術頁為
`103601017→103627195`，長 34、SHA-256
`5592b4048986b175d187438df9b7ecd154cdedc775a9ff290231d5e3863a9a9b`。

本階段的 guarded glyph trace 顯示 prompt dispatcher return 後仍有六個可見 glyph
cell；它們不是上述 dispatcher string 的一部分，故不得合併為 TSV identity：

| 頁面 | prompt cell | 尾碼 cell | 初態樣式（依序） | 證據等級 |
| --- | --- | --- | --- | --- |
| career | 0–32 | 33–38 | `0/15`、`0/10`×3、`15/0`×2 | 已證實 |
| technical | 0–33 | 34–39 | `0/15`、`0/10`×3、`15/0`×2 | 已證實 |

職業 glyph 收據 SHA-256 為
`732fc2f0444ff7c52969860e8a0cd01172b4ffc283fae7785a8384b4afa58de5`；技術 glyph
收據 SHA-256 為
`c90b1c37be485dd7c5e0be8bb78e31c2c44464c82025921067f2245812654022`。二者只保存
style、row、column、caller 與時序，未保存 glyph bytes 或原文。

## 最早相交 A000 pre-write 與候選矩形

row 24 的 cell 高度是 8 logical pixels，故文字本體的候選安全矩形（半開）為：

| 頁面 | 文字本體矩形 | 尾碼保護矩形 | 本體首個實際相交 A000 write | 證據等級 |
| --- | --- | --- | --- | --- |
| career | `[0,264)×[192,200)` | `[264,312)×[192,200)` | step `102716699`，A000 `AF1E1`，`00→0D`，觀測 IP `0763:1855` | 已證實 |
| technical | `[0,272)×[192,200)` | `[272,320)×[192,200)` | step `103623531`，A000 `AF22B`，`00→0D`，觀測 IP `0763:1855` | 已證實 |

上述是各文字本體在 Escape 後首次**實際變值**且相交的 `WatchWrites` 記錄；不是
dispatcher entry、也不是猜測性的固定 step。職業 A000 觀測收據 SHA-256 為
`1ad9d30c43856bea0666103c80c6d6049e432311ba2f5598bc60f51767109fe6`；技術為
`c89027874468701fe1817039733484452dc439694951393a3cf798a4d27abf9a`。由於空白 glyph
與同值寫入可能早於第一個變值，這兩個 step **不是**「第一個 renderer invocation」或
「第一個可能同值 A000 store」的證明；後續 lifecycle watcher 不得把它們偷換成更強的
pre-write 契約。

矩形只隔離可翻譯本體；六 cell 尾碼必須保留為獨立、原版管理的保護區，不能被中文
本體 clear rectangle 覆蓋。實際使用中文前仍需以正式字型量測 TSV 兩筆字串，在兩種
支援倍率下驗證 ink containment；目前矩形不是覆繪授權。

## N／Y 轉場與 DRAFT lifecycle

phase52 的 N／Y JSON 使用不同的合法 state
`workplace/probe/after-bios-space-100m.state`（SHA-256
`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`）。因此它們在
本文件只能作為控制流的**交叉參照**，不是與 phase66 prompt／glyph／A000 收據同一
初始 state 的同狀態證明。該組既有 phase52 排程為：career Escape 於 `102700000`，`N` 於
`102900000`；technical Escape 於 `103600000`，`N` 於 `103800000`，或 `Y` 於
`103800000`。控制收據的最終 framebuffer／memory identity 分別記於
`skill-exit-career-refuse-20260924.json`、`skill-exit-technical-refuse-20260924.json`、
`skill-exit-technical-confirm-20260924.json`；其 JSON SHA-256 依序為
`bc271b18ee64e5bc907621ebc5f856ee53e80b549ef87b79660d723c31cc5572`、
`011011a18808fd0a2385030eaaeae7785bd588a51a5f7ff07923415202225c63`、
`3d8d70c7705bb5ecab49ef0e4ecfb0cd85c2517c39719b487fc17738964402de`。

第 45–47 階段已證實 N 回到相同技能頁、career Y 轉到 technical、technical Y 轉入
身體圖示頁。因此後續 typed model 至少必須把「prompt 本體＋六 cell 尾碼」視為同一個
prompt group：N 與 Y 任一輸入消費後都不能讓舊中文 layer 留在 row 24。這是由正常路徑
與初態尾碼共同支撐的**強推論**，不是已實作 watcher。

## 未解決項目與 READY 禁止條件

1. 尚未量到 N／Y 消費後、兩個矩形各自的**最早含同值寫入** A000 pre-write；本階段只量到
   prompt 顯示時的首個變值相交。不得以 terminal framebuffer 或群組推論偽稱已量到 clear。
2. 尚未取得 N／Y 後六 cell 尾碼每一格的完整重畫／清除 trace；不得預設其配色永遠不變，
   也不得把尾碼翻成中文或寫入 TSV。
3. 尚未審查 catalog 兩筆譯文的 2×／3×字型、ink containment、正式 lifecycle 規格、
   watcher，及原文／繁中同狀態 A/B。

因此本階段只能讓後續審查從可追溯的 DRAFT 邊界開始，絕不構成 READY。
