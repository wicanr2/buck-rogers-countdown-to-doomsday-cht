# 第二百九十三階段：規格 039 §3.4 欄名列實作與同狀態驗收

日期：2026-09-30
狀態：定稿（主代理審閱，2026-09-30）；實作 dosgolem `9e55973`；phase254 新基準 rerun33
範圍：規格 039 §3.4「欄名列」（READY，主 repo `0f8a271`）。基底 dosgolem fork 分支 `buck-rogers-cht-output-overlay`
HEAD `1584b05`（未 commit，工作樹改動）；已同步 `dosgolem-clean`。
本文件不含英文原文、手冊題目或答案。

## 1. 實作

### 1.1 主 repo（未 commit）

| 檔案 | 內容 |
|---|---|
| `text/header-columns.tsv`（新） | `family`、`key`、`cols`、`evidence` 四欄三列：`menu` `career.screen.columns.heading` 2,8,14；`dispatcher` `frag.442e07fe93c9` 0,17,32；`dispatcher` `frag.0ddcc5022a9c` 0,17,32。evidence 只存 workplace 相對路徑、步數與代號 |
| `tools/header_columns.py`（新） | 載入檢查（標頭、family、`.uc` 鍵、重複、cols 非負嚴格遞增、token 切分與空白規則、欄寬、末欄 ≤ 原文長度×2、key 同在 events 與 catalog；選單類 events→譯文對照與 `live_menu_load.go` 相同）；原版核對：dispatcher 從 `workplace/engine-l10n/fragments.tsv` 取原文、驗長度與 SHA-256 等於 events、以空白切分重算欄名起點比對 cols，evidence 的 trace 另驗該步字串雜湊；選單類以 evidence 指定的原版 baseline RGBA 重算資料欄起點比對 cols。原文或證據缺席時印「跳過原版驗證」。輸出不含英文 |
| `tools/test_header_columns.py`（新） | 11 項：正式名單、單位計算、遞增、欄寬、末欄、token 數、三種空白、未知鍵（選單、片段、`.uc`）、缺譯文、`token_starts`、原文缺席跳過 |

### 1.2 dosgolem（`apps/buckrogers/`、`cmd/buckrogers-text-receipt/`；xlate 未改）

| 檔案 | 內容 |
|---|---|
| `header_columns.go`（新） | `LoadHeaderColumns`（檔案本身的結構檢查）；`anchorColumns`（§3.4 第 1–3 條：U+0020 切 token、各欄自 `2·cols[i]` 單位起、欄前以 §3.1 補位、欄寬／末欄檢查、補到總寬）；`tokenStarts`（原文欄名起點）；`ValidateMenu`（對合併後選單 catalog，逐 identity 以原文長度檢查）；`ValidateDispatcher`（片段鍵與 `.uc` 變體都驗，譯文必須存在）；`dispatcherColumns`（原文整串為名單片段時回傳 cols，`.uc` 去尾） |
| `menu_overlay.go` | `MenuOverlayEntry` 加 `Columns`；`BuildMenuOverlay` 有 Columns 時以 `anchorColumns(譯文, cols, 2×(格數−前綴))` 取代 `padUnits`，失敗即回錯誤 |
| `menu_overlay_runtime.go` | `RuntimeMenuOverlay.SetHeaderColumns`；`Apply` 依 `request.EventKey` 填 Columns |
| `live_menu.go`、`live_menu_load.go` | `LiveMenuRuntime.SetHeaderColumns`（先 `ValidateMenu`，再裝到 2×／3× presenter）；live 從 text 目錄讀 `header-columns.tsv`：檔案不存在＝不錨定（比照 ECL／引擎 catalog 的選用檔），存在但載入檢查失敗＝`LoadLiveRuntime` 回錯誤 |
| `engine_dispatch.go` | 一般路徑命中後呼叫 `headerText`：原文整串是名單片段、`tokenStarts(原文)` 等於 cols 才錨定；不符（或錨定失敗）照一般路徑並計 `HeaderStats.Mismatches`；成功計 `HeaderStats.Anchored`。`SetHeaderColumns` 先 `ValidateDispatcher` |
| `live_runtime.go` | 引擎 dispatcher 載入時裝名單（檢查失敗回錯誤）；名單有 dispatcher 列但 dispatcher 未載入時回錯誤；`DebugSummary` 有計數時輸出 `header-columns={Anchored Mismatches}` |
| `post_join_menu.go` | 唯一一處位置式 `MenuOverlayEntry{…}` 字面值補 `nil`（新增欄位的編譯需要，行為不變） |
| `cmd/buckrogers-text-receipt/main.go` | 新旗標 `-header-columns`：runner 自己的一般選單 presenter 與 `-live-menu-rgba-out` 的 live menu 套用同一份名單（先對 runner 的合併選單 catalog 做 `ValidateMenu`）；與 `-scoped-menu-3x` 併用即失敗。`-live-text-dir` 的 LiveRuntime 一律從 text 目錄自行載入 |
| `header_columns_test.go`（新） | 見 §2 |

同步清單 `changed-files.txt`、`sync.sh`；Docker 包裝 `go.sh`（容器名 `buck-phase293-*`）。

## 2. 測試

| 項目 | 結果 | 收據 |
|---|---|---|
| `go test ./...`（`dosgolem-clean`，唯讀掛主 repo text 與 current-font，`BUCKROGERS_CHT_ROOT` 設定） | 29 套件 ok；`cmd/buckrogers-play`、`frontend/ebiten` 為既有 cgo build failed | `test-all.txt` |
| `GOOS=windows CGO_ENABLED=0 go build ./...` | 通過（無輸出） | `build-windows.txt` |
| `go vet ./apps/buckrogers/ ./cmd/buckrogers-text-receipt/` | 無訊息 | — |
| gofmt（本輪改動檔） | 只有 `live_menu.go` 被列出，原因是 `LiveMenuRuntime` 結構既有四行未對齊（fork HEAD 版本同樣被 gofmt 列出）；本輪新增欄位另起一段，未重排既有行 | — |
| Python 工具與測試（`python:3.13-slim`，主 repo 唯讀） | 11 項通過；正式名單載入檢查 3 列通過；原版核對全部相符（見下） | `python-tool.txt` |

§5.2 欄名列單元測試（全部通過）：

| 項目 | 測試 |
|---|---|
| H1 2×、3×：段數 1、段 key `#0`、總寬 36 單位；點／加／總的邏輯 X 為欄 23、29、35；像素墨跡自該欄起、前一格與欄間無墨跡；無名單時仍為一般排版（5 段） | `TestHeaderColumnsMenuAnchor` |
| 載入檢查失敗：檔案層（family、`.uc`、重複、遞增、非數字、負數、空欄）；選單（token 數、欄寬、末欄、連續／前導／結尾空白、未知鍵）；邊界值本身通過（欄間恰 1 單位、末欄恰到 2×長度）；dispatcher（未知鍵、欄寬、末欄、無譯文、無引擎 catalog） | `TestHeaderColumnsLoadCheckFailures` |
| dispatcher：名單片段與 `.uc` 變體錨定到 0、17、32 格；原文欄名起點不符（0,16,32）時照一般路徑並計 Mismatches；無名單時一般排版；Hits 不變 | `TestHeaderColumnsDispatcher` |
| live：正式 text 目錄載入後名單裝到選單與 dispatcher；三種壞名單（選單欄寬、dispatcher 末欄、未知鍵）使 `LoadLiveRuntime` 失敗且錯誤訊息指出 `header-columns.tsv` | `TestHeaderColumnsLiveLoad` |

原版核對（`tools/header_columns.py`，Docker 內唯讀）：

| key | 結果 | 推論等級 |
|---|---|---|
| `career.screen.columns.heading` | phase292 `e001-career-subtract` 原版 baseline 列 6–13、`e001-technical-base` 列 6–7、9–18 的資料欄起點都是欄 23、29、35（相對 2、8、14）＝cols。技術技能頁第 8 列的技能名延伸到欄 21，所以該列不列入 | 已證實 |
| `frag.442e07fe93c9` | 原文長度與 SHA 等於 events；原文欄名起點 0、17、32＝cols；phase257 `cp/a6.tsv` 步 2924335190 的字串雜湊相符（列 4、欄 1） | 已證實 |
| `frag.0ddcc5022a9c` | 原文欄名起點 0、17、32＝cols；沒有 trace 樣本 | 欄起點已證實；畫面位置強推論 |

## 3. 同狀態 A/B

old＝`phase292-halfwidth/runner-new-e1`（本輪改動前的 `dosgolem-clean`，SHA-256 `af7f7986…`，即 phase254 rerun32 所用），
new＝本輪 `dosgolem-clean`（`runner-new`，SHA-256 `452ad744…`）。同一份 `/project/text`（含新名單；old 不認得此檔）與
`workplace/current-font`（倚天），同 state、同按鍵、同停止點，2×、3× 各一次。new 另帶 `-header-columns`。
腳本 `jobs.sh`、`ab.sh`、`ab-inner.sh`、`run.sh`、`diff.py`（另比 runner 選單 presenter 的 old／new）；墨跡欄段 `cols.py`、`cols.txt`；裁切 `shots.sh`、`crop.py`。
全部 Docker（`--rm`、`--network none`、`--cpus ≤ 4`、`--memory`、`--pids-limit`、目前 UID/GID、log rotation）。

| 項目 | 狀態 | 差異位置（8×8 邏輯格） | 收據 | 推論等級 |
|---|---|---|---|---|
| H1 職業技能頁（`e001-career-subtract`） | 新基準 | live 與 runner 選單 presenter 都只在 r4 c21–36；原版記憶體、indexed、palette、停止點 old＝new | `ab/e001-career-subtract*`；`shots/crop-e001-career-subtract-{2,3}x-old-new.png` | 已證實 |
| H1 一般技能頁（`e001-technical-base`） | 新基準 | 同上 r4 c21–36 | `ab/e001-technical-base*`；`shots/crop-e001-technical-base-{2,3}x-old-new.png` | 已證實 |
| H2 治療結果表頭（phase257 `cp/a5.state` 接 `cp/a6` 同一組五個按鍵，停在表頭印完 2924364920、結果列印完 2924900000） | 已錨定、畫面零差 | none；new 的 live 計數 `header-columns={Anchored:1}`（2×、3× 各一次） | `ab/e029-medic-hdr*`、`ab/e029-medic*` | 錨定：已證實；零差原因見下 |
| H3 修理結果表頭 | 未量到 | 沒有可到達的 state | — | — |

H1 墨跡欄段（`cols.txt`，2×、3× 相同）：

| 畫面 | r4 欄名墨跡 | 下方資料列 r6、r7 |
|---|---|---|
| old | 21–27（三個欄名擠在一起） | — |
| new | 23–24、29–30、35–36 | 23、29–30、35 |

欄名分別起於欄 23、29、35，與下方數字同欄。old／new 裁切見 `shots/`（上 old、下 new；不輸出原版英文畫面）。

H2 零差的原因：停在表頭剛印完（2924364920）時，原版 baseline 第 4 列本身就沒有可見墨跡；原版以前景色 15 印表頭（trace 與
本輪 dispatcher 觀察一致），覆繪沿用同一前景色，所以錨定後的中文與 old 的一般排版在畫面上都看不到。判斷為色 15 在此畫面
與背景同色（強推論；未直接讀 palette 值）。欄位錨定本身由計數與單元測試證實。

## 4. phase254 七條回歸（rerun33）

- `phase254-live-families-parity/runner` 先備份為 `runner-rerun32`（與原檔逐位元組相同，SHA-256 `af7f7986…`），再換成本輪
  `runner-new`（`452ad744…`）。新結果 `rerun33/` 與 `rerun33-*.txt`；腳本由 rerun32 複製，唯一改動是 `rerun33/common.sh` 的
  `MENU` 前加 `-header-columns $T/header-columns.tsv`，讓 runner 自己的選單 presenter 與 live 用同一份名單（否則 live-vs-runner
  會在技能頁欄名列出現預期外的 DIFF）。手冊 PNG 照 rerun32 於每次執行後刪除（本輪 0 張殘留）。
- 驅動 `p254.sh`，差異 `p254diff.py` → `p254-diff.txt`。
- 七份文字（story、opening、manual、post、skill、action、body）與 rerun32 逐字相同（含既有的 live-vs-runner 行）。
- 504 份 RGBA 中 474 份逐位元組相同，30 份不同，全部是技能頁欄名列：

| 案例 | 檔案 | 差異位置 |
|---|---|---|
| career-add／down／drawn、tech-down／drawn，2×／3× | menu、live、expect | r4 c21–36 |

其他家族（劇情、手冊、加入後選單與提示、操作列、身體圖示）零差。

## 5. 未量到

1. H3 修理結果表頭：phase257 各 trace 沒有樣本，沒有可到達的 state。
2. H2 的可見像素：原版表頭在此畫面不可見，只能證實錨定發生，無法以畫面比對欄位。
3. Unifont 3× 實跑（沿用 phase292 的限度，本輪只用倚天工作字型）。

## 6. 待決

1. H2 表頭在原版畫面不可見（色 15）。是否仍保留在名單中（目前保留；錨定不改變可見畫面）。
2. `live_menu.go` 的既有 gofmt 未對齊（四行），是否另開一筆只做格式化的變更。
3. `header-columns.tsv` 缺席時 live 不錨定、不報錯（比照 ECL／引擎的選用檔）。若要改為必備檔，需同步改 `LoadLiveRuntime`。
4. 規格 §3.4 欄名列第 5 條的選單類核對，本輪以「evidence 指定的原版 baseline RGBA」實作；證據畫面在 `workplace/phase292-halfwidth/ab/`，
   若日後清理該目錄，選單類核對會輸出「跳過原版驗證」。
5. phase254 基準：rerun33 是否取代 rerun32。

## 7. 檔案

`changed-files.txt`、`sync.sh`、`go.sh`、`test-all.txt`、`build-windows.txt`、`python-tool.txt`、`runner-old`、`runner-new`、`run.sh`、`ab.sh`、
`ab-inner.sh`、`jobs.sh`、`jobs.log`、`diff.py`、`cols.py`、`cols.txt`、`crop.py`、`shots.sh`、`shots/`、`ab/`、`p254.sh`、`p254.log`、`p254diff.py`、`p254-diff.txt`。
