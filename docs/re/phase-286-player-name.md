# 第二百八十六階段：規格 038 第 1 期實作與同狀態驗收

日期：2026-09-29
狀態：定稿（主代理審閱，2026-09-29）
用途：規格 038（玩家角色名的判定與各畫面顯示）第 1 期的實作紀錄與 §5 驗收收據。
收據、RGBA、PNG、字型與 runner 只在 ignored `workplace/phase286-player-name/`。

## 1. 實作（dosgolem fork `buck-rogers-cht-output-overlay`，commit `dd04345`）

| 檔案 | 內容 |
|---|---|
| `apps/buckrogers/player_name.go`（新） | §3.1 快照 `ReadPartySnapshot`（hook 當下 DS → `DS:4EC5` 鏈、`[DS:3BCC]+0x33E` 隊員數、長度 1–15／0x20–0x7E 防呆、性別 0／1／其他）、`partyTracker`（捨棄時沿用上一份、開機前為空）、`PlayerNames`（036 `english` 位元組相等優先，否則 037 音譯，以名字＋性別快取）、§3.2 ECL 判定 `eclPlayerName`（呼叫端 CodeKey `OVR:00904:0B79`／`0B4A`、型別 `0x81`、白名單 `7C00` 需 `[DS:4EC1]` 在快照內、`7BA4` 取第一筆同名） |
| `apps/buckrogers/ecl_text.go` | `EclTextEntry.Player`；玩家名先於 027 catalog 與 029；「中文(英文)」單元 → 只中文單元 → 既有 passthrough 三段；`EclTextStats` 加 `PlayerNameChineseOnly`、`PlayerNameEnglish`，另加 `PlayerNames`（命中數，診斷用） |
| `apps/buckrogers/engine_dispatch.go` | `ObserveEntryParty`（原 `ObserveEntry` 轉呼叫、快照 nil）；`235A` 指標＝前 N 筆記錄且內容相等 → 欄 23 畫音譯中文（一字一格、≤ 原名格數），欄 1／8／17 不做怪物名查表；其他情形照現行 `monsterSlot` |
| `apps/buckrogers/live_runtime.go` | `056C` 進入（呼叫端為 `0B79`／`0B4A`）與 dispatcher 進入（呼叫端 `235A`）時以 hook 當下 DS 取快照；載入 `text/` 的 037 資料，失敗時玩家名停用並記原因；`DebugSummary` 輸出 `party={taken rejected names=[…]}`；`PartyNames()` |
| `apps/buckrogers/name_glossary.go` | `ChineseFor`（`english` 整串相等） |
| `apps/buckrogers/player_name_test.go`（新） | §5.1 全部合成案例 |

同步到 `workplace/dosgolem-clean`（上列 6 檔逐位元組相同）。通用層（`xlate/` 等）未改。

## 2. 輸入

| 項目 | 值 |
|---|---|
| runner-old（A） | phase285 `runner-new`（規格 036 執行期），SHA-256 `181924ba…4e423a388` |
| runner-new（B） | `dosgolem-clean` 本輪原始碼，golang:1.24-bookworm、`CGO_ENABLED=0`，SHA-256 `f432baa6…6ce6464e` |
| catalog | 主 repo `text/`（HEAD 35dfb93；02b8617 之後 `text/` 無變更），A、B 相同 |
| 字型 | `font/p286-eten-top-pad.golemfnt`，SHA-256 `0462ed06…5afd735b`，2,520 字；以 `tools/eten_font.py build text/*.zh-TW.tsv` 重建（含 `translit-chars.zh-TW.tsv`），A、B 相同。見 §4 第 1 條 |
| 原版 | `workplace/original/BRcdoom`，唯讀 |

每案同一 state、同一按鍵、同一停止點，A、B 各跑 2×、3×；`diff.py` 比對 baseline RGBA、收據
`memory_sha256`／`indexed_sha256`／`palette_sha256`／`stopped_at`，並列出 A、B live 畫面相異的 8×8 格（邏輯座標）。
全部在 Docker（`--rm`、`--network none`、`--cpus` ≤ 4、`--memory`、`--pids-limit`、目前 UID/GID），原版與主 repo 唯讀。

## 3. 結果

| 項目 | 狀態 | 差異位置（8×8 格，邏輯） | 收據檔 | 推論等級 |
|---|---|---|---|---|
| §5.1 單元測試 | 通過 | — | `test-all.txt`（`go test ./...`：29 個套件 ok；`cmd/buckrogers-play`、`frontend/ebiten` 為既有 cgo 標頭 build failed，另以 `GOOS=windows CGO_ENABLED=0` 交叉編譯通過） | 已證實 |
| §5.2 phase254 七條回歸 rerun27 | 通過 | 七份 `rerun27-*.txt` 與 rerun26 逐字相同（全 `same`）；52 份 live RGBA 與 rerun26 逐位元組相同 | `phase254-live-families-parity/rerun27/`、`rerun27-*.txt`；舊 runner 備份 `runner-rerun26` | 已證實 |
| phase-274 `CELESTE ATTACKS.`（`cp/d316` 接 Enter，停 7,036M） | 通過（新基準） | 只有第 17 列第 1–18 欄：「塞萊斯特(CELESTE)發動攻擊。」，舊為「CELESTE發動攻擊。」。原版三雜湊、baseline 相同 | `ab/e274-celeste-*`；`crop-e274-celeste-{old,new}.png` | 已證實 |
| phase-274 通風管（`cp/a2` 接 u，停 26,354M） | 通過（新基準） | 第 17 列第 20–38 欄、第 18 列第 1–9 欄：起點是名字（`. ` 之後），「弗拉維烏斯(FLAVIUS)」加入後同句重排；`BELOW`（`7B90`）與 `. ` 不變 | `ab/e274-airshaft-*`；`crop-e274-airshaft-*` | 已證實 |
| ECL `7C00`（`cp/l7` 接 Enter，停 5,048M，n1） | 通過 | 第 17 列全列、第 18 列第 1–22 欄：頁首名字改「弗拉維烏斯(FLAVIUS)」後整段重排 | `ab/e-n1-7c00-*` | 已證實 |
| ECL `7BA4`＋`7BB8`（d6206） | 通過 | 第 17 列第 21–38 欄、第 18 列第 1–22 欄：起點是名字；`GIRL`（`7BB8`）仍為 catalog「女」 | `ab/e-d6206-*` | 已證實 |
| ECL `7BA4`＋`7BCC`（d6208） | 通過（已知限制） | 只有第 17 列第 1–22 欄（第一個名字）；`7BCC` 印出的第二個 `FLAVIUS` 留英文，同段中英並存（§3.3 已知限制） | `ab/e-d6208-*` | 已證實 |
| ECL `7B90` 門禁句＋`7BA4`（d65） | 通過 | 第 18 列第 18–38 欄、第 19 列第 1–3 欄：`7BA4` 的 `ROARKE` 改「羅克(ROARKE)」；`AUTHORIZED PERSONNELROARKE`（`7B90`）不變（§4 不處理） | `ab/e-d65-*` | 已證實 |
| §5.5 型別抽驗 | 一致 | 上述 6 步在 phase-284 原始紀錄（`runs/*.tsv` 的 `O` 列）中「呼叫端 `0B79`／`0B4A`、`81@7BA4`／`81@7C00`、內容為隊員名」各 1 筆；新 runner 的 `PlayerNames` 計數在 6 步都是 1。`0x80` 字面文字、`7B90`／`7BB8`／`7BCC` 的輸出與舊版相同 | 各案 `-new-2.log` 的 `live:` 行 | 強推論（以計數與畫面對照，未逐筆記錄 runtime 讀到的型別） |
| 戰鬥右欄（`cp/a4`＋a5 按鍵） | 通過 | 停 2,861.5M：只有第 12 列第 23–29 欄（被攻擊者「弗拉維烏斯」）；停 2,869.8M：只有第 1 列第 23–29 欄（行動者「塞萊斯特」）；停 2,909.5M：零差（該格是怪物）。怪物名「特林戰士」不變 | `ab/b-a5-*`；`crop-b-a5-*` | 已證實 |
| 探索隊伍欄（欄 17，a6 按鍵，停 2,930.4M、2,931.5M） | 零差 | none | `ab/x-a6-2930400000-*`、`-2931500000-*` | 已證實 |
| 角色頁（欄 8，停 2,935.6M） | 零差 | none | `ab/x-a6-2935600000-*` | 已證實 |
| 全寬隊伍表（`p281/rm1` 選 REMOVE、Down） | 零差 | none；該案快照取到 1 次 | `ab/h-rm1-down-*`、`h-rm1-enter-*` | 已證實 |
| 創角期 post-class（`probe/after-bios-space-100m`，四個 Enter，停 102M） | 不變 | none；收據 118 筆事件 A、B 相同（只有 `scratch` 路徑欄不同），`text/post-class-events.tsv` 96 筆全在收據中 | `ab/c-post-class-*` | 已證實 |
| 創角期 reroll `N`（同上＋101.4M `n`） | 不變 | none；183 筆事件 A、B 相同，`text/reroll-no-events.tsv` 65 筆全在收據中 | `ab/c-reroll-no-*` | 已證實 |
| §5.3 名單變動 | 通過 | `rm1`：FLAVIUS、PIERRE、NICOLE STEELE、ROARKE、JANELLE；`rm2`：FLAVIUS、PIERRE、ROARKE、JANELLE；`rmf`：CELESTE、PIERRE、NICOLE STEELE、ROARKE、JANELLE；`add1`：六人，CELESTE 在末。與 phase-281 `tally4.txt` 相同；`rejected=0` | `ab/h-{rm1,rm2,rmf,add1}-down-new-2.log` 的 `party=` | 已證實 |
| §5.4 前端端到端（2× live PNG 代替） | 取得 | 敘事：`e2e-narrative-celeste-2x.png`、`e2e-narrative-airshaft-2x.png`；戰鬥：`e2e-battle-celeste-2x.png`、`e2e-battle-target-flavius-2x.png` | 同上收據 | 已證實（LiveRuntime 合成，字型為本輪倚天子集） |

- 本輪樣本的音譯：FLAVIUS→弗拉維烏斯、CELESTE（F）→塞萊斯特、ROARKE→羅克。
- 所有樣本 `PlayerNameChineseOnly`、`PlayerNameEnglish` 皆 0（三段退路的後兩段只有單元測試覆蓋）。

## 4. 限度、未量項與待決

1. **字型**：`workplace/current-font/buckrogers-eten-top-pad.golemfnt`（9/27）不含 037 允許字集。以它跑新 runner 時，
   玩家名頁因缺字被 `syncEclText` 整頁重置（`resets=map[ecl-text:1]`），畫面等於舊版。本輪 A/B 改用重建的子集。
   `current-font` 與發行 Unifont 子集需依正式譯文重建（本輪未改，超出寫入範圍）；phase254 七條回歸用的仍是 `current-font`。
2. **未量到**：移除隊員後進一場戰鬥、確認欄 23 只出現現存隊員（`rm1` 等狀態沒有已知到戰鬥的按鍵路徑）；
   欄 1 的 `235A` 在戰鬥外是否指到記錄（`h-rm1-down` 有 `235A` 進入並取到快照，但未逐筆記錄指標落點）；
   太空戰鬥、交易、訓練畫面的欄 23；所有格 `'S` 後句（本輪樣本未出現）；劇情 NPC 入隊、角色死亡。
3. **實作取捨（請審）**：
   - 快照只在 `056C` 呼叫端為 `0B79`／`0B4A`、dispatcher 呼叫端為 `235A`（在名稱呼叫端清單且不在一般白名單）時取；
     其他 `056C`／dispatcher 進入不讀。
   - 「超出記憶體」以線性位址＋記錄長度 ≤ `0xA0000`（常規記憶體）判斷。
   - 欄位例外只套欄 1／8／17（規格列舉值）；其他欄照現行。
   - 037 資料載入失敗時只停用玩家名顯示；快照與欄 1／8／17 的怪物名查表停用仍生效。
   - 已判定為玩家名但音譯 `ok=false` 時，不再查 catalog，顯示英文；計入 `Misses`，不計入 `PlayerNameEnglish`
     （後者只算排版退到第三段）。
   - `EclTextStats` 多一個 `PlayerNames` 命中計數（規格要求的兩個計數之外），供收據判讀。
4. 通用層未改；`cmd/` 未改。

## 5. 檔案

`ab.sh`、`ab-inner.sh`（A/B）、`p254.sh`（phase254 rerun27）、`go.sh`、`sync.sh`、`diff.py`、`crop.py`、
`ab/`（收據、RGBA、PNG、log）、`crop-*.png`、`full-*.png`、`e2e-*.png`、`font/`、`runner-old`、`runner-new`、`test-all.txt`。
