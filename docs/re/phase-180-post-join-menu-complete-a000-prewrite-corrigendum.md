# 第一百八十階段：加入角色後功能選單的完整 A000 pre-write 勘誤

狀態：**已證實的原版觀測；維持 DRAFT，不授權 production 或 READY。**  
日期：2026-09-23

## 可重生輸入與收據

- 原版 `GAME.OVR` SHA-256：`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 合法 `a-joined.state` SHA-256：`1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。
- 本案權威 dosgolem fork commit `4589bfe986a7414c418f7ec02d6da0888d7cfd11`、Docker Go
  `go1.26.7`；實模式定位與 linear A000 observer range 不混用。先前誤用的 upstream
  `d9c0c27` 與 fork 的 Machine／VideoWrite／DOS 層存在相關差異，故本節不以其收據外推。
- ignored `workplace/phase180-post-join-menu-a000-observer/` 的一次性 Go probe（SHA-256
  `ca85b78ade1ff26b743dd341eddc7174f7240618f6158b96f26e2ccc2dd6dd1c`）以通用
  `Machine.WatchWrite` 在每 byte 寫入前觀測 `A0000-AFFFF`，**同值也記錄**。它只將
  source 複製至 ignored workspace 以取得 Go `internal/` 可見性，未修改 shared dosgolem。
- phase 161 的 BIOS Right、Enter、九次 Down、Enter 排程從同一 state 重播兩次到
  step `126000000`；兩份私有 observer JSON 逐 byte 相同，皆 SHA-256
  `7421d673aa5455fe243e01b11a2c6f261f0a07767904cbe82e70c274ac4d448c`。

## 21 個 exact variants

版控 [`post-join-menu-variants.tsv`](../../text/post-join-menu-variants.tsv)（SHA-256
`8e81644e94213bd99e9f91c75e21e10e277f498a16257556516302da4e448eb5`）對七個翻譯 row
各列 `initial_normal`（`37F1:15BD`／`0/10`）、`normal_redraw`（`37F1:1856`／`0/10`）
與 `selected`（`37F1:175D`／`15/0`），共 21 筆。每筆保存 length、原文 SHA-256、caller、
色號、row、column 與 phase 161 receipt locator，不保存原文。

第 21 筆是 row 20 在移往 row 21 時的普通回寫；它不把 row 21 selected 納入 catalog。

## 勘誤：active generation 的最早相交 pre-write

phase 161 的 `026F:029C`（step `125119490`）仍是 Enter 後第一筆**全選單 clear**，
但不是 complete cycle 的 active-layer boundary。完整 observer 的各 generation 最早相交
write 都是原版 glyph primitive `0763:184D`：

| generation | previous selected post-call | first pre-write | pixel | old→new |
| ---: | ---: | ---: | --- | --- |
| 1 | 123150388 | 123300757 | `(72,104)` | `15→0` |
| 2 | 123324922 | 123500821 | `(72,112)` | `15→0` |
| 3 | 123521980 | 123700764 | `(72,120)` | `15→0` |
| 4 | 123720420 | 123900750 | `(72,128)` | `15→0` |
| 5 | 124137261 | 124300875 | `(72,144)` | `15→0` |
| 6 | 124334319 | 124500830 | `(72,152)` | `15→0` |
| 7 | 124527433 | 124700875 | `(72,160)` | `15→0` |

整段有 231,936 個 A000 writes、195,105 個同值 writes；七個 safe rectangles 有 44,544
hits、26,380 個同值 hits。因此差分畫面或只攔 `026F:029C` 均不足以失敗即關閉。

每個相交 `normal_redraw` 必須先原子失效 active generation，僅在完整 exact normal／selected
pair 後才可重建。row 20 normal redraw 後的 row 21 selected 未收錄，故 pending 與 active
皆必須 fail-closed，不能讓舊 overlay 存活到 Exit。phase 162 ignored verifier 回讀變體表與
observer，拒絕 partial、duplicate、重排、identity 漂移及此 row 20→row 21 stale-layer case；
它仍不是 production watcher 或 runtime A/B。
