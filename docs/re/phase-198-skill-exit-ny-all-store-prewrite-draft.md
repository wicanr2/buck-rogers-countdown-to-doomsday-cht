# 第一百九十八階段：技能頁離開確認 N／Y all-store pre-write DRAFT

日期：2026-09-24
狀態：**DRAFT 原版證據；不授權正式 watcher、presenter、TSV、覆繪、READY 或 CONFORMED。**

本階段以第一百九十七階段的兩個固定合法 Escape 前 state，各自重播
`Escape→N`、`Escape→Y`。目標僅為量得 row 24 問句本體與六格尾碼「某範圍的
第一筆相交 A000 store」，包含同值 store；它不是完整六格失效、DOS stop、
正式 layer 清除或 runtime 接線的證明。

## 固定輸入、工具及位址空間

- 原版 `START.EXE` SHA-256：`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；
  `GAME.OVR`：`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
  原版只讀掛載為 state 記錄的 `/orig`。
- career state：`skill-exit-pre-esc-102700000.state`，SHA-256
  `fd64f35d19c855eef9f8f6e44357ed2aa295b89ff329bc35ee4ce6fd8eb4fbaa9`；technical
  state：`skill-exit-pre-esc-103600000.state`，SHA-256
  `2302ceede2daff8df0de42ff3cf7fc2e346ac89f64ff2b715b0be281fddb9a8e`。它們是兩個
  不同合法起始 state，不與 phase-52 的 state 混用。
- 固定舊 probe SHA-256：`0bbb7cb1807367556f0fc5a69692a5aa2c05c821ed3170ca9f8c714b65fdd39a`；
  `WatchWrites` 只回報值變更。為診斷建立 ignored、可丟棄的
  `workplace/phase198-skill-exit-confirmation/probe-allstores`，SHA-256
  `9b1e47e6c07d2fa7cfc61eb4dce53e532e1552f46037104ddb2d1f0bd507277d`，Go `1.24.13`，
  `go version -m` 記錄 dosgolem VCS `71f19cb949813c697ea3a7d3cb0a60c35d74bedd+dirty`。
  它以既有 `ObserveVideoWrites` 的
  VGA 寫入前 callback 記同值 store，收據只含 step、位址、CS:IP、write mode；
  診斷 source 已還原，沒有改 production watcher 或 presenter；可重建 source recipe
  位於 ignored `workplace/phase198-skill-exit-confirmation/probe-allstores-rebuild.md`，
  SHA-256 `f8515467af532cc31c60b52d49ff29c4e8407d4c4f4daa40290c1479c58a4570`，其固定 base `observe.go` SHA-256 為
  `661c1b7d8c936176abb55d8f340232fe53bb3453248f49999b95102fa91c5b7e`。
- `A000` 是 Mode 13h 線性 VRAM；`0763:…`、`0CF4:…` 是 dosgolem 8086
  執行期 `segment:offset`。all-store observer 在寫入前報 `0763:184D`，舊變值
  observer 報 `0763:184E`；這是 hook 時機差異，以下僅以 step＋A000 位址對照。

## 可重播控制基準

所有容器使用 `--rm --network none --memory 1g --cpus 1 --pids-limit 128` 與目前
UID/GID。每個 all-store 變體以相同 state、相同 key schedule、相同 stop，另跑一條
舊變值控制組：

```text
probe-allstores -load-state <phase197-state> -root /orig -steps <stop>
  -bios-keys "$(printf '\033N')" -bios-key-from <start> -bios-key-every 200000
  -observe-video-range af000-af140 -observe-video-file <all-store>
```

`Y` 只替換第二鍵。career 使用 start/stop `102700000/103700000`；technical 使用
`103600000/104600000`。控制組改用同一 probe 的
`-watch af000-af13f -watch-file <value-change>`。矩形為 career 本體／尾碼
`[AF000,AF108)`／`[AF108,AF138)`，technical 為
`[AF000,AF110)`／`[AF110,AF140)`。

## 最早相交 A000 store

`same-value` 指 all-store 的 step＋位址不在同一重播的變值控制組；舊 watcher 唯一
省略條件是值未變，故此分類已證實。它不表示後續六格都被完整重畫或清除。

| 頁面／輸入 | 範圍 | all-store 首筆 | 分類 | 變值控制組首筆 |
| --- | --- | --- | --- | --- |
| career N | 本體 | `102907507 AF000 0763:184D` | 值變更 | `102907507 AF000 0763:184E` |
| career N | 尾碼 | `102900580 AF108 0763:184D` | **same-value** | `102921332 AF128 0CF4:1B3C` |
| career Y | 本體 | `103319280 AF000 0763:184D` | 值變更 | `103319280 AF000 0763:184E` |
| career Y | 尾碼 | `102900519 AF108 0763:184D` | 值變更 | `102900519 AF108 0763:184E` |
| technical N | 本體 | `103807523 AF000 0763:184D` | 值變更 | `103807523 AF000 0763:184E` |
| technical N | 尾碼 | `103800494 AF110 0763:184D` | **same-value** | `103829532 AF130 0CF4:1B3C` |
| technical Y | 本體 | `103906680 AF0A8 0CF4:1B3A` | **same-value** | `103906680 AF10A 0CF4:1B3C` |
| technical Y | 尾碼 | `103800433 AF110 0763:184D` | 值變更 | `103800433 AF110 0763:184E` |

因此，只倚賴變值 watcher 會漏掉 career N 尾碼 `AF108`、technical N 尾碼
`AF110`，以及 technical Y 本體 `AF0A8` 的較早 pre-write。這是已證實的 observer
差異；「N/Y 後整個 prompt group 必須失效」仍是強推論，不是 production lifecycle
已驗。

## 私有、content-safe 收據

收據皆在 ignored `workplace/phase198-skill-exit-confirmation/`，未保存原文、glyph 或
framebuffer；all-store 收據不含 pixel byte，僅變值控制組因既有 watcher 格式保留
old/new 色號以判定 `old != new`，不含可還原文字內容：

| 變體 | all-store SHA-256（筆數） | 變值控制組 SHA-256（筆數） |
| --- | --- | --- |
| career N | `6745a784ddf7c71834e5e4ebeb4db3bf8c0da617d63604aa6c192b1002b0db6c`（696） | `4e436679e61780a6718b76b6a0e478849dabed436096ade684d74c4630d2a42d`（86） |
| career Y | `fb8b2670f8bf0c9a9cd459d95180e279b015481382b0b5c8192178d6fd875f19`（696） | `abd0b183433e81e14eccab8262739dd8eedf28831faf7b8f126b4f525a32a9c9`（134） |
| technical N | `6d0ec364a3f02d4d60bb4e241344b654c60aee4a37147aeb637a17f0bb9966d7`（688） | `da64360c99eb8d9b0510b62eff1bd1d94698ca4d965505f48613b21eadf1b55d`（86） |
| technical Y | `9a4f245f7efa58f1a229e650e01acf37a57bd6b2879125214c29223012539ffc`（688） | `514e01bfe74817d250cd2567fa3be3f77a330ed63871df6c181a322082328ac1`（110） |

phase-199 已完成靜態字型 containment；但執行期字型 containment、catalog／typed
lifecycle 審查、runtime A/B、存讀檔、完整正常玩家路徑與完整尾碼失效仍未知；本文件
不得升 READY。
