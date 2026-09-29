# 第二百九十階段：規格 038 §3.4 第 2 期實作與同狀態驗收

日期：2026-09-29
狀態：定稿（主代理審閱，2026-09-29）；實作 dosgolem `94825fb`；phase254 新基準為 rerun29
用途：規格 038 §3.4（隊伍欄、全寬隊伍表／Pick Character、角色頁標題的玩家名）實作紀錄與驗收收據。
收據、RGBA、PNG 與 runner 只在 ignored `workplace/phase290-party-panel-names/`。未 commit。

## 1. 實作（dosgolem fork `buck-rogers-cht-output-overlay`，工作樹，基底 `2f67d69`）

| 檔案 | 內容 |
|---|---|
| `apps/buckrogers/engine_dispatch.go` | `partySelectedCaller`＝`OVR:2BA60:21DE`、`partyCursorCaller`＝`OVR:27BBE:0388` 以程式常數登記（不進 `text/engine-dispatch-name-callers.tsv`）；`NeedsParty` 涵蓋三呼叫端；`partyName` 改回傳 `partyDecision`：隊員命中後任何欄列都不查怪物名，欄 23 維持第 1 期（只中文、≤ 原名格），§3.4 表內欄列（欄 17 列 4–9：只中文、到欄 33；欄 1 列 4–9：「中文(英文)」→ 只中文 → 英文、到欄 33；欄 8 列 1：同左、到欄 27）；延伸格入口檢查 `extensionClear`（讀 A000，延伸格全部等於該次 `args[2]` 才可延伸；檢查失敗後只接受 ≤ 原名格的候選）；覆繪寬度＝max(顯示字數, 原名長度)，不足以空白格（背景色）補滿；入口讓位範圍改以覆繪寬度計；`21DE`／`0388` 未命中或不在表內時直接返回（不覆繪、不查怪物名、不計數，原版寫入照常使覆繪失效）；新增診斷計數 `PartyStats{Extended, ChineseOnly}` |
| `apps/buckrogers/live_runtime.go` | dispatcher 進入時把 `StepReader` 當 A000 讀取器傳入 `ObserveEntryParty`；`DebugSummary` 在 `PartyStats` 非零時輸出 `party-panel=` |
| `apps/buckrogers/player_name_test.go` | `TestBattleColumnCondition` 依第 2 期更新（表外列才留英文；`21DE` 在欄 23 不畫；`NeedsParty` 三呼叫端） |
| `apps/buckrogers/party_panel_test.go`（新） | §3.4 驗收 1 全部項目（見 §3） |

- 英文部分的字形：沿用 dispatcher presenter；原版字形表取得後 presenter 已由 031 §3.1 重建，不另改程式（截圖可見英文為原版字形）。
- 通用層（`xlate/`、`session/`、`internal/`）與 `cmd/` 未改。`workplace/dosgolem-clean` 已同步上列 4 檔（逐位元組相同）。
- `hmenu_overlay.go`、`player_name.go` 不需改動：合成與 §2.6.1 逐列讓位本來就以 `len(row.Cells)` 計，覆繪寬度變長後自動涵蓋延伸格。

## 2. 輸入

| 項目 | 值 |
|---|---|
| runner-old（A） | `git archive 2f67d69` 重建，golang:1.24-bookworm、`CGO_ENABLED=0`，SHA-256 `00f2c75d…fdca7020` |
| runner-new（B） | `dosgolem-clean` 本輪原始碼，同工具鏈，SHA-256 `2549a8d5…5d836976` |
| text | 主 repo `text/`（HEAD 4eb1cd7），A、B 相同 |
| 字型 | `workplace/current-font/buckrogers-eten-top-pad.golemfnt`（未改），A、B 相同；本輪沒有缺字重置（`resets=map[]`） |
| 原版 | `workplace/original/BRcdoom`，唯讀 |
| 狀態 | phase257 `cp/*.state`、phase281 `states/*.state`、`checkpoints/salvation-station.state`、`probe/after-bios-space-100m.state`，唯讀；各案 `state_start` 與 phase286／289 收據相同 |

A/B：`ab.sh`／`ab-inner.sh`／`jobs.sh`（同 state、同按鍵、同停止點，A、B 各 2×、3×），`diff.py` 比對 baseline、原版三雜湊與 `stopped_at`，列出 live 相異的 8×8 格。
全部在 Docker（`--rm`、`--network none`、`--cpus` ≤ 4、`--memory`、`--pids-limit`、目前 UID/GID、log rotation），容器名 `buck-phase290-*`；結束後無殘留容器、無 root 擁有檔。

## 3. 結果

| 項目 | 狀態 | 差異位置（8×8 格，邏輯；2× 與 3× 相同處只列一次） | 收據 | 推論等級 |
|---|---|---|---|---|
| 驗收 1 單元測試 | 通過 | — | `test-all.txt`（`go test ./...` 29 套件 ok；`cmd/buckrogers-play`、`frontend/ebiten` 為既有 cgo 標頭 build failed；`GOOS=windows CGO_ENABLED=0 go build ./...` 通過） | 已證實 |
| 　三呼叫端表內命中、表外不命中（含欄 1 列 1 物品頁標題、欄 4 訓練頁、欄 8 列 2、列 3／10） | 通過 | — | `TestPartyPanelTable` | 已證實 |
| 　`21DE`／`0388` 非隊員指標、nil 快照：不覆繪、不查怪物名、不計數 | 通過 | — | `TestPartyPanelNonMember` | 已證實 |
| 　`235A` 隊員取名等於怪物名：任何欄列（含欄 4、欄 1 列 1）不畫成怪物；037 缺席時亦然 | 通過 | — | 同上 | 已證實 |
| 　只中文短於原名：原名格以背景色空白格補滿 | 通過 | — | `TestPartyPanelShortPadsOriginalCells` | 已證實 |
| 　格數邊界：隊伍欄 17／18、全寬表 33／34（退只中文）／皆放不下、角色頁 20／21（退只中文）／只中文 20／21 | 通過 | — | `TestPartyPanelBoundaries` | 已證實 |
| 　延伸格入口檢查：延伸格有非底色 → 只中文；只中文也超出原名 → 英文；無 A000 讀取器 → 視同失敗；需要範圍外的非底色不影響 | 通過 | — | `TestPartyPanelExtensionEntryCheck` | 已證實 |
| 　同名在三呼叫端文字相同、前景不同；游標移動換色覆寫 | 通過 | — | `TestPartyPanelSameTextAcrossCallers` | 已證實 |
| 　延伸格被呼叫外寫入 → 移除；新呼叫只重疊延伸格 → 移除 | 通過 | — | `TestPartyPanelExtensionInvalidation` | 已證實 |
| 　指標在快照但內容不等 → 不命中 | 通過 | — | `TestPartyPanelTable`、`TestBattleColumnPlayerNames` | 已證實 |
| `a7`（`d1041`＋`n`，停 26,813M；整欄重畫，列 4 為 `21DE`） | 新基準 | r5 c17–23、r6 c17–22、r7 c17–29、r8 c17–22、r9 c17–23；原版三雜湊、baseline 相同；AC／HP 格（欄 34–38）零差 | `ab/p-a7-*` | 已證實 |
| `a21`（`a20`＋上，停 3,052.5M；游標移動） | 新基準 | r4 c17–23（`235A` 以前景 11 重印舊列）；`0388` 新列（列 9）見 §4 第 1 條 | `ab/p-a21-*`、`dbg/a21.err` | 已證實 |
| `d249`（`d248`＋上，停 6,767.5M；單列重印） | 新基準 | r5 c17–23；名字格顏色 A、B 同為 `ff5555`（該次 `235A` 前景 12） | `ab/p-d249-*`、`fg-check.txt` | 已證實 |
| `ba1`（`bs3`＋下 ×7，停 690.9M；Pick Character 游標移動） | 新基準 | 2×：r4 c1–14、r5 c1–13、r6 c1–11、r7 c1–21、r8 c1–10、r9 c1–12（「中文(英文)」）；列 5 為 `0388` 前景 15 白字 | `ab/p-ba1-*`；`shots/e2e-fullwidth-ba1-2x.png` | 已證實 |
| `ba2`（`bs3`＋`e`，停 674.9M；整表重畫，列 4 為 `21DE`） | 新基準 | 同 `ba1` 的六列範圍 | `ab/p-ba2-*` | 已證實 |
| `v7`（`v6`＋Enter，停 5,499M） | 新基準 | r5–r9 同上範圍；列 4（`21DE`）見 §4 第 1 條 | `ab/p-v7-*` | 已證實 |
| `p281/rm1`（5 人；Enter＋下，停 730M） | 新基準 | r4 c1–14、r5 c1–11；快照五人 A、B 相同 | `ab/p-rm1-down-*` | 已證實 |
| `p281/rm1`（Enter，停 727M） | 零差 | none（該停止點名字格尚未重畫） | `ab/p-rm1-enter-*` | 已證實 |
| 角色頁 `a6`（停 2,935.6M、2,959.5M） | 新基準 | r1 c8–21：「弗拉維烏斯(FLAVIUS)」，欄 28 起的 `hp:`／HP 零差 | `ab/p-a6-2935600000-*`、`-2959500000-*`；`shots/e2e-sheet-a6-2x.png` | 已證實 |
| 角色頁 `e5`（`e4`＋按鍵，停 4,114.5M） | 新基準 | r1 c8–21 | `ab/p-e5-*` | 已證實 |
| 隊伍欄 `a6`（停 2,931.5M） | 新基準 | r5–r9 同 `a7` 範圍 | `ab/p-a6-2931500000-*` | 已證實 |
| 三種重畫文字相同（忽略前景比遮罩） | 相同（可見者） | 全寬表：FLAVIUS 列 4 `235A`（ba1）＝`21DE`（ba2）；CELESTE 列 5 `0388`（ba1）＝`235A`（ba2、v7）；2×、3× 逐點相同。隊伍欄：可見的 `235A` 跨 a7／a21／a6／d249 相同；`21DE`／`0388` 在隊伍欄停止點不可見（§4 第 1 條），改以 runtime 追蹤比對文字：`21DE`（a6）與 `235A`（a21）對 FLAVIUS 產生相同 rune 序列 | `same-text.txt`；`dbg/a6.err`、`dbg/a21.err` | 全寬表已證實；隊伍欄三呼叫端為強推論（像素不可見，以文字追蹤） |
| 物品頁標題（`n5`＋Enter，停 5,193M） | 與第 1 期相同 | none | `ab/q-n6-*` | 已證實 |
| 訓練確認頁欄 4（salvation-station＋phase289 按鍵，停 5,413M） | 與第 1 期相同 | none | `ab/q-train-*` | 已證實 |
| 第 1 期敘事（e274-celeste、e274-airshaft、e-n1-7c00、e-d6206、e-d6208、e-d65） | 不變 | none | `ab/q-e*` | 已證實 |
| 第 1 期戰鬥右欄（b-a5 停 2,861.5M、2,869.8M、2,909.5M） | 不變 | none | `ab/q-b-a5*` | 已證實 |
| 創角期 post-class、reroll `N` | 不變 | none | `ab/q-c-*` | 已證實 |
| 名單快照（rm2、rmf、add1、rm1） | 不變 | 快照名單 A、B 相同（`party=` 名字清單逐字相同；`taken` 多 1 為 `0388`／`21DE` 進入時取快照） | `ab/q-h-*-{old,new}-2.log`、`ab/p-rm1-down-*` | 已證實 |
| 　同上案例的畫面 | 新基準 | 全寬表名字格（rm2：r5 c1–11、r6 c1–10；rmf：r4 c1–13、r5 c1–11；add1：r4–r9） | `ab/q-h-*` | 已證實 |
| phase254 七條回歸 rerun29 | 狀態不變；8 份 live 有預期差異 | 七份 `rerun29-*.txt` 與 rerun28 逐字相同；504 份 RGBA 中 496 份逐位元組相同；`o275000000`、`o280900000`、`o282000000`、`m275000000`（各 2×、3×）的 live 只在 r5 c17–23、r6 c17–22、r7 c17–29、r8 c17–22、r9 c17–23（探索隊伍欄名字格）不同 | `phase254-live-families-parity/rerun29/`、`rerun29-*.txt`；舊 runner 備份 `runner-rerun28` | 已證實；是否算「不變」見 §5 第 1 條 |
| 驗收 3 截圖（2×，text-receipt live） | 取得 | 隊伍欄 `shots/e2e-party-column-a7-2x.png`、全寬表 `shots/e2e-fullwidth-ba1-2x.png`、角色頁 `shots/e2e-sheet-a6-2x.png`；對照舊版 `shots/crop-*-old-2x.png` | 同上 | 已證實 |

本輪樣本的顯示：FLAVIUS→弗拉維烏斯、CELESTE（F）→塞萊斯特、PIERRE→皮埃爾、NICOLE STEELE（F）→妮可•斯蒂爾、ROARKE→羅克、JANELLE→賈內爾。
全部表內樣本都採第一段（隊伍欄只中文、全寬表與角色頁完整），沒有實跑樣本降段（`party-panel=` 只出現 `Extended`）。

## 4. 限度與觀察

1. **前景 15 在探索畫面的停止點不可見**：`a7`、`a21`、`a6` 2,931.5M、`v7` 的停止點上，原版畫面（baseline）的 `Name` 表頭、AC 值與 `21DE`／`0388` 列名字也都看不到，
   即當下 DAC 色盤第 15 色等於底色；`a7` 在 26,805.5M、26,807M、26,809M、26,811M 另取四個停止點結果相同。runtime 追蹤（`dbg/*.err`）確認 `21DE`／`0388` 的覆繪列已建立且合成時保留，
   只是跟著原版色盤不可見；`ba1`、`ba2` 的前景 15 可見且已顯示中文。色盤第 15 色何時、為何變暗未追（假說：選取列閃爍）。
2. 隊伍欄三呼叫端「像素層級」的相同只在全寬表量到；隊伍欄以文字追蹤代替（強推論）。
3. `a21` 從 `a20` 狀態起跑，停止點前沒有重畫的列（5–8）沒有覆繪，差異只在本步重印的列；屬重播起點限制，不是遺漏。
4. 延伸格入口檢查失敗、只中文、退回英文三種降段只有單元測試（本輪實跑樣本名字都放得下）。
5. 規格 §3.4 已知未量項（角色死亡、劇情 NPC 入隊、其他 Pick Character 路徑、10 步單列重印的用途）本輪未新增證據。
6. 除錯 runner（`runner-dbg`，在 engine_dispatch 加 stderr 追蹤的暫時版本）只用於 §4 第 1 條的判讀，不是交付物。

## 5. 待決

1. phase254：規格 §3.4 驗收 2 寫「phase254 七條回歸…不變」。七份狀態文字逐字相同，但 control.state 起跑的 4 個停止點畫面上有探索隊伍欄，名字格依本期改為中文（8 份 live RGBA 不同，差異只在名字格）。
   依本期目的屬預期差異，請主代理決定是否以 rerun29 為新基準（沿例 phase287 對 opening 280.9M 的處理）。
2. `workplace/dosgolem-clean/workplace/p290-old-src`、`p290-dbg-src`（各約 16M，runner-old／runner-dbg 的原始碼樹）與 `runner-p290-dbg` 為暫存；本輪清理被安全檢查擋下，未刪除，請使用者決定。

## 6. 檔案

`go.sh`、`sync.sh`、`run.sh`、`ab.sh`、`ab-inner.sh`、`jobs.sh`、`jobs.log`、`diff.py`、`crop.py`、`same_text.py`、`same-text.txt`、`fg-check.txt`、`dbg.sh`、`dbg/`、
`p254.sh`、`p254.log`、`runner-old`、`runner-new`、`runner-dbg`、`test-all.txt`、`ab/`、`shots/`。
