# 第一百八十四階段：Exit 與確認提示 DRAFT 原型

狀態：**DRAFT；可丟棄 typed 原型，未授權正式覆繪。**  日期：2026-09-23

固定原版輸入沿用第一百八十三階段：`START.EXE` SHA-256
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`、
`GAME.OVR` SHA-256 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，以及
`a-joined.state` SHA-256 `1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。
位址空間維持區分：`37F1:…`、`0763:…` 是 dosgolem 8086 實模式；原字串 offset 是檔案位址。

## 新雙重收據與已證實邊界

以 ignored checkout `f46aa5e915afe178be733f4a731696dbc46f34b4` 的 receipt CLI、Docker
`golang:1.25.0-bookworm`／Go 1.25.0，從合法 state 送 Right、Enter、七次 Down、Enter：

| 分支 | 雙收據 SHA-256 | 已證實結果 |
| --- | --- | --- |
| N | `20d573002fc5f48126189fe33c19c802759b49de2a6ac6b0effc7bebfb089051` | N 於 `124900053` 消費；`124905849` 全選單 clear，row21 在 `125219476` 普通重畫並於 `125241454` 再反白。 |
| Y→Y | `3a98be659947b1f5d055c4e8a56572f4b338e8bd3ddfd1899df71404ef971caa` | 第一個 Y 於 `124900053` 消費，第二提示於 `124906582` 輸出；第二個 Y 於 `125000111` 消費，runner `125006324` 終止。 |

這個 checkout 與第一百八十三階段權威 fork `cb3ca77` 不同，Y→Y stop 比既有收據的
`125006330` 早 6 instructions；因此它只支撐本階段 DRAFT typed 原型的 identity／branch 形狀，
不能取代 `cb3ca77` 的權威收據、更不能拿來升 READY。以下已補權威 fork 原始碼的
同觀測器重跑，但同樣出現六步差異，必須在 READY 前查明；不能因程式碼版本相同便視為
先前 runner 的逐步同一性。

row21 選取 identity 是 11-byte SHA `622af…a7b4e`、`37F1:175D`／`15/0`／row21 col9；Enter 後普通回寫是
`37F1:1856`／`0/10`。其安全矩形是 `[72,160)×[168,176)`，已證實最早相交 A000 pre-write 為
`124800903`、`0763:184D`，故 row21 active 必須先變空。

兩個 row24 identity 皆為 `37F1:101E`／`0/14`／row24 col0，但 length／SHA 不同：第一問 12-byte
`c38a…9032`，矩形 `[0,96)×[192,200)`；第二問 30-byte `3502…dcb8`，矩形
`[0,240)×[192,200)`。它們不可共用 identity 或 generation。

N 前後與 Y→Y 的 row24 trailing-cell clears 不和上述文字安全矩形相交；故本原型只將它們記為
prompt 的輸入／terminal 生命周期證據，**不**冒稱已量到 prompt 的 A000 pre-write。N 的全選單 clear 是 row21
與整個選單的失效邊界；Y→Y 的 runner stop 只強制清空 active，不是假造 clear。

## 權威 fork 原始碼的 A000 候選邊界補測

再用 `cb3ca77c66e4909c5f513b807840e885ab5cb4a3` 的本機唯讀複本及同一合法
`a-joined.state`，在 Docker／Go 1.25.0 執行 ignored、只讀取原版 A000 寫入的
`cmd/exit-prompt-a000/main.go`（SHA-256
`aa9f55669b27a905966f0ef9e6918832864d48d623228e461aad2c94120ce2b6`）。
N 收據 `workplace/phase184-exit-prompt-draft/cb-n.json` SHA-256
`5028c38cbdcb38f63fd66675b15a263a2bb2239afbcb65640c4ac9e7a8ecb46e`；
Y→Y 收據 `cb-yy.json` SHA-256
`990c5a99f141534958ac0f96e4f4fef30215a941914bdcd3ded23ab01810418b`。
以下 CS:IP 都是 dosgolem 的 8086 實模式位址，矩形是候選而非已審核 watcher 契約：

| 分支與區域 | 首筆相交 A000 寫入 | 解讀限制 |
| --- | --- | --- |
| N、Y→Y 的 row21 | step `124800903`、`0763:184D`、`(72,168)`、`15→0` | 與前階段 row21 pre-write 相符。 |
| N、Y→Y 的第一提示尾端 | step `124826001`、`0CF4:1B3A`、`(144,192)`、`15→0` | 位於第一提示候選文字矩形外；不可據此斷言文字已失效。 |
| Y→Y 的第一提示文字區 | step `124906844`、`0763:184D`、`(0,192)`、同值 `0→0` | 第二提示開始輸出時的第一個相交寫入；即使顏色未變仍須考慮失效。 |
| Y→Y 的第二提示尾端 | step `124934844`、`0CF4:1B3A`、`(288,192)`、同值 `0→0` | 位於第二提示候選文字矩形外。 |
| N 的第一提示文字區 | step `125251139`、`0763:184D`、`(0,192)`、同值 `0→0` | N 返回選單後才相交；此 observer 未證實更早的文字區寫入。 |

Y→Y 在 DOS `Exited` 停止前沒有量到第二提示文字矩形的後續相交寫入；N 分支根本
沒有第二提示，收據中其候選矩形的相交值不得解讀為第二提示清除。Y→Y 停止於
`125006324`，仍比第一百八十三階段既有 runner 的 `125006330` 早六步；保持
**DRAFT／未解決**。以上只補足已觀測 A000 候選邊界，不授權正式覆繪或升 READY。

## 可丟棄原型

ignored `workplace/phase184-exit-prompt-draft/verify_exit_prompt_draft.py` 直接固定上述 identity、收據 SHA、
三個半開矩形與候選譯文「離開至 DOS」／「遊戲尚未儲存。仍要離開？」；「離開至 DOS」是第一百八十三階段
已列的 row21 替代 DRAFT 候選，本階段暫供靜態量測，不是正式文案決定。它沒有讀取或建立 TSV。
以現行 local-only 倚天字型 SHA `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`
驗得 2×（16×16 ink）與 3×（22×22 ink、(1,1) pad）皆零缺字、零越界；缺字／零墨跡、未知 identity、未知 decision
與無 active 的 pre-write 一律拒絕。

這是靜態 containment 和 DRAFT 模型，不是 runtime A/B，也不改變原版 Y/N 判定。下一門檻是：
釐清兩種 runner 的六步差異、確認提示矩形與逐幀失效，再獨立審查 typed lifecycle 及候選譯文；
通過 READY 前不得接 watcher。
