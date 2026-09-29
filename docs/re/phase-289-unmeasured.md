# 第二百八十九階段：規格 036／038 未量項補量

日期：2026-09-29
狀態：定稿（主代理審閱，2026-09-29）
用途：規格 036 §3.5、038 §3.6 列為「未量到」的項目逐一補量或記錄到不了的原因。
全部產物只在 ignored `workplace/phase289-unmeasured/`；另新增探針測試檔
`workplace/dosgolem-clean/apps/buckrogers/zz_phase289_tier_scan_probe_test.go`（SHA-256 前綴 `3487a64495a3c732`）。

## 1. 輸入

| 項目 | 舊（A） | 新（B） |
|---|---|---|
| runner | `runner-old`＝phase283 `runner-rerun25`，SHA-256 `dd449b29…42e03436` | `runner-new`＝`dosgolem-clean` 現行原始碼（apps/cmd/xlate 與 dosgolem 分支 HEAD `2f67d69` 逐檔相同），golang:1.24-bookworm、`CGO_ENABLED=0`，SHA-256 `1500287a…a1ca41` |
| text | `text-old/`＝phase285 的 `git archive 6b35726^ text` | 主 repo `text/`（HEAD 6520a41；執行期間 HEAD 前進到 056c382，`text/` 無變更） |
| 字型 | `workplace/current-font/buckrogers-eten-top-pad.golemfnt`，SHA-256 `0462ed06…5afd735b`（與 phase286 重建子集相同） | 同左 |
| 原版 | `workplace/original/BRcdoom`，唯讀掛載於 `/orig` | 同左 |

- A/B：`ab.sh`／`ab-inner.sh`（沿用 phase286 方法），同 state、同按鍵、同停止點，A、B 各跑 2×、3×；`diff.py` 比對 baseline、
  原版三雜湊與 `stopped_at`，列出 live 相異的 8×8 格。harness 先重跑 phase286 `b-a5` 2,861.5M，得到相同結果（只有第 12 列第 23–29 欄），確認可沿用。
- 原版事件：`np`（phase284 探針原樣複製重建）記 `0424`／`056C` 進入時的指標落點、nameIdx、隊員數 N 與鏈；
  `walk.py` 以 phase257 的 `gt`（原版、無覆繪）逐段推進。以 `analysis/cmpw.py` 核對重播與 phase257 原紀錄的 W／D 事件步數逐列相同。
- 全部在 Docker（`--rm`、`--network none`、`--cpus` ≤ 3、`--memory`、`--pids-limit 256`、目前 UID/GID、log rotation），容器名 `buck-phase289-*`；
  結束後無殘留容器、無 root 擁有檔。

## 2. 結果

| # | 項目 | 狀態 | 路徑 | 舊新差異（8×8 格，邏輯） | 收據 | 推論等級 |
|---|---|---|---|---|---|---|
| 1 | 036：Zane 的水平選單（`hmenu.a4da3f4fffd1`）與怪物名遭遇 | 到不了 | 見 §3.1 | — | `inventory-states.tsv` | 已證實（無 ECL3–6 存態）；可行性評估為強推論 |
| 2 | 038：移除隊員後進戰鬥 | 已量到 | `checkpoints/salvation-station`（5,377M）→ HQ → 隊伍選單移除 CELESTE → Begin Adventuring（未出手冊問答）→ Port → 發射 → 廢棄飛船 → phase257 d1 探索按鍵（平移 +42.5M）＋固定巡迴移動 → 5,933M 遭遇 `SM. E.C. GENNIE` | 5,934M：第 1、10 列第 23–29 欄（FLAVIUS）；5,935.5M：第 1、10 列第 23–28 欄（ROARKE）；5,987M：第 1、10 列第 23–28 欄、第 12 列第 23–29 欄（ROARKE、JANELLE）。原版三雜湊與 baseline 相同 | `ab/p2-rm1b-*`；`runs/rm/r6.tsv`；`walk/r1–r6.*` | 已證實 |
| 2a | 同上：快照與指標 | 已量到 | 同上 | 新 runner `party=` 為 FLAVIUS、PIERRE、NICOLE STEELE、ROARKE、JANELLE（`rejected=0`）。原版欄 23 事件 11 筆：隊員 9 筆指 REC[0]／[3]／[4]（nameIdx < N=5），怪物 2 筆 REC[8]（nameIdx=5）；CELESTE 的舊記錄 `5762:000F` 已不在鏈上，欄 23 無 CELESTE | `analysis/dsum.py runs/rm/r6.tsv` | 已證實 |
| 3 | 038：欄 23 在太空戰鬥、交易、訓練 | 部分量到 | 交易：depot Buy／Sell（`walk/t1–t4`）；訓練：HQ → Train Character（`walk/t5–t9`）；太空戰鬥：到不了 | 交易與訓練舊新零差（`p3-sell-5405000000`、`p3-train-5413000000`） | `runs/trade/{sell,train}.tsv`；`ab/p3-*` | 已證實（交易、訓練）；太空戰鬥未知 |
| 3a | 同上：`235A` 的欄位用法 | 記錄 | 同上 | 交易：購買訊息走 `0A58` 第 24 列，不經 `235A`；Sell 物品頁標題 `235A` 欄 1（REC[0]），隊伍欄 17。訓練：全寬隊伍表欄 1（REC[1]–[5]），**「FLAVIUS will become:」的名字走 `235A` 欄 4 第 4 列（REC[0]）**。兩處都沒有欄 23 | 同上 | 已證實 |
| 3b | phase257 全紀錄的欄 23 | 記錄 | 4,252 段原版紀錄 | `235A` 欄 23 共 1,905 筆，每一筆距最近的戰鬥右窗（`L23`）印字 ≤ 12,301 步；無一筆在戰鬥外 | `analysis/col23-context.txt`、`d235a-columns.txt` | 已證實（限紀錄涵蓋範圍） |
| 4 | 038：名字命中後旗標 0 的所有格後句 | 已量到 | phase257 `d28`（CELESTE）、`d328`（PIERRE）、`d375`（NICOLE STEELE）、`d447`（ROARKE）、`d499`（JANELLE）：`0B79` 旗標 1 印名字（`81@7BA4`），`0B4A` 旗標 0 接 `'S LEG ITCHES FOR A MOMENT.`（`80` 字面，catalog `ecl.2.32.01850` 命中） | 只有第 17 列，從第 1 欄（名字起點）到句尾：d28 c1–22、d328 c1–20、d375 c1–30、d447 c1–19、d499 c1–21。畫面「塞萊斯特(CELESTE)的腿突然一陣發癢。」，舊為「CELESTE的腿…」。原版三雜湊、baseline 相同 | `ab/p4-*`；`shots/crop-p4-*` | 已證實 |
| 4a | 所有格後句未命中（規格已知限制） | 未見 | 紀錄中唯一另一例 `d6208` 的 `'S HEARTBEAT.` 前面是 `7BCC` 名字（非白名單，名字本身留英文），不是「命中後接未命中」 | — | `analysis/player-w-events.tsv` | 已證實（樣本內無此組合） |
| 5a | 038：角色瀕死後的戰鬥右欄 | 已量到 | `cp/a4`＋a5 按鍵，停 2,884.5M：JANELLE 於 2,835M `goes down / and is Dying`，之後以 `is bandaged` 出現在第 10 列 | 第 1 列第 23–35 欄（NICOLE STEELE）、第 10 列第 23–29 欄（JANELLE）。快照六人 | `ab/p5-a5-2884500000-*` | 已證實 |
| 5b | 038：隊友倒下（HP 0）後的戰鬥右欄 | 已量到 | `cp/d17171`＋d17172 按鍵：探索隊伍欄在 26,306M 已顯示除 FLAVIUS 外五人 HP 0；最後一戰只出現 FLAVIUS 與 `RAM H.D. ROBOT` | 33,977.5M：第 1、10 列第 23–29 欄；33,987M：第 12、16 列第 23–29 欄（FLAVIUS 被擊倒）。怪物名不變 | `ab/p5-d17172-*`；`runs/death/*.tsv` | 已證實；「HP 0 是死亡或昏迷」未解（記錄的狀態欄位未知） |
| 5c | 同上：快照 | 記錄 | 同上 | 瀕死、HP 0 的隊員仍在鏈上，N 仍為 6（`np`：N=6、鏈 12 筆）；新 runner 快照六人 | 同上 | 已證實 |
| 5d | 038：劇情 NPC 入隊 | 到不了 | — | — | — | 見 §3.2 |
| 6 | 036／038 退路第 2、3 段的實跑樣本 | 到不了 | 見 §3.3 | — | `analysis/npc-w-events.tsv`、`player-w-events.tsv`、`tier-scan.tsv` | 已證實（樣本不存在）；靜態掃描為強推論 |

截圖（2×）：`shots/crop-p2-rm1b-{5934000000,5987000000}-{old,new}-2x.png`（右欄）、`shots/full-p2-*`、
`shots/crop-p4-*-{old,new}-2x.png`（敘事窗第 16–19 列）、`shots/crop-p5-*-{old,new}-2x.png`、`shots/full-p3-{train,sell}-*`。

附帶量到（038 §3.6「欄 1 指標落點逐筆紀錄」）：訓練路徑全寬隊伍表欄 1 五筆、Sell 物品頁標題欄 1 一筆，指標全部是
REC[i]+00 且 i < N（已證實，6 筆）。

## 3. 到不了的項目

### 3.1 Zane（ECL5）

- 盤點：以 `tools/scan`（`LoadStateFile` 後掃記憶體中的 `ECL?.DAX`、`GEO?`、`WALLDEF?`、`BACK?`、`CPIC?`、`BIGPIC?` 檔名字樣，並讀隊伍鏈）
  掃遍 `workplace/` 5,222 個 `.state`（不含 phase288／289）：模組字樣只有 1、2，沒有 3–6。N 分布 0（182）、1（13）、4（1）、5（2）、6（5,024）。
- 存檔：`SAVGAM*` 共 140 份，只有兩種內容（SHA-256 `4d8424e8…`、`e5c176bb…`），來源都是 phase244–270 的創角／存讀檔流程。
- phase257 最後一段（`d17172`，33,990M）是隊伍全滅，之後回到創角；探索器在廢棄飛船第 8 層失敗（phase-272）。
- ECL5 的地名字樣以 VENUS 為主；前往條件至少要完成廢棄飛船（phase257 探索紀錄：登船後外艙門脫落、「YOUR SHIP IS NOWHERE TO BE SEEN」）。
- 可行性：以 phase-272 的探索器推進需要：戰鬥策略（現行只按 `q` 快速戰鬥，第 3 層起隊員陸續倒下）、休息治療、跨模組的劇情與航行流程；
  成本估計為數十個 phase257 規模的自動化段落，且結果不保證。本輪不做。
- 需要什麼才到得了：(a) 使用者以前端正常遊玩並在 ECL5（金星）提供 checkpoint；或 (b) 具戰鬥與休息邏輯的自動遊玩器。
  不得改存檔或記憶體跳關（本輪未做）。

### 3.2 劇情 NPC 入隊

- phase257 紀錄與 5,222 個狀態中 N 從未大於 6、鏈長變動只來自隊伍選單。ECL 原文中「JOIN(S) YOUR PARTY／ACCOMPANY」類字樣只出現在 ECL5（2）與 ECL6（1）。
  限度：只以字串搜尋，其他寫法未查（強推論）。條件同 §3.1。

### 3.3 退路第 2、3 段

- phase257 全紀錄中含 036 譯名的 ECL 印字只有 3 筆（`ld1`、`s2`、`d260`），都是敘事窗 L1 T17 R38 B22 從頭印；隊員名 36 筆也都在同一寬窗。
- 靜態掃描（新增探針測試，只記 key 與段別）：174 條含譯名的 ECL 譯文，以敘事窗與戰鬥窗 `L23 T2/T11 R38 B21` 從頭排版全部採第 1 段；
  只有假設的 `L23 T13 R38 B16`（`05A4` 用的 4 列窗）會出現第 2 段 21 條、第 3 段 1 條、整窗溢出 12 條。ECL 敘事在紀錄中沒有進過這個窗。
- 結論：第 2、3 段只可能在「接續印字且游標已接近窗底」時觸發；現有紀錄沒有這種樣本。需要：一段在窗底附近接續印出含人名（或隊員名）句子的原版路徑。
  不以合成輸入或改記憶體造狀態。

## 4. 限度與觀察

1. 項目 2 的路徑是本輪以正常玩家輸入新走的（`walk/r1–r5` 的按鍵紀錄在各 `.tsv` 的 `K` 列）；探索段沿用 phase257 d1 的前 20 步按鍵平移，
   之後是固定巡迴移動。遭遇是否為隨機遭遇未查；A/B 兩邊從同一個 `walk/r5.state` 出發，原版三雜湊相同。
2. HQ 的隊伍選單（「Training facilities」）可移除隊員，Begin Adventuring 直接回站內，沒有出手冊問答（本輪該步未截圖）。phase-270 的問答只見於讀檔後。
3. **欄 4（訓練畫面）**：同一 CodeKey `OVR:2BA60:235A` 在訓練確認頁以起始欄 4 印玩家名，指標直指隊員記錄。規格 038 §3.3 列舉的欄位是
   1／8／17／23，欄 4 不在其中。現行照「其他欄照現行」處理（怪物名查表，玩家名不是怪物名時留英文），舊新零差；若玩家取名等於怪物名，
   欄 4 會被畫成怪物中文（與 §3.3 描述的欄 1／8／17 既有問題同類）。不影響欄 23 判定。
4. 戰鬥訊息嵌名句（`FLAVIUS makes his tactics roll.` 等）仍為英文名＋中文句，屬規格 038 §4 第 3 期範圍，本輪不列為差異。
5. 項目 5b 的「死亡」：只證實 HP 0 且原版不再把他們畫進戰鬥右欄；記錄內的死亡／昏迷狀態欄位未解。

## 5. 檔案

`run.sh`（Docker 包裝）、`ab.sh`／`ab-inner.sh`、`diff.py`、`crop.py`、`png.py`、`walk.py`、`np-batch.sh`、`np`、`runner-{old,new}`、`text-old/`、
`tools/scan`、`tools/np`、`inventory-states.tsv`、`states-all.txt`、`analysis/`（`trace_scan.py`、`plan.py`、`chain.py`、`cmpw.py`、`dsum.py`、
`col23_ctx.py`、各 TSV／TXT、`keys-*.txt`、`plan-*.txt`）、`runs/`、`walk/`、`ab/`、`shots/`。
