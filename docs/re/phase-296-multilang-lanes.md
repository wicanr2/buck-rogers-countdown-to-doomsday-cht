# 第二百九十六階段：規格 040 第一段（LiveRuntime 多語通道）

日期：2026-09-30
狀態：定稿（主代理審閱，2026-09-30）；實作 dosgolem `d685efd`；phase254 rerun34 與 rerun33 逐位元組相同
規格：`docs/spec/040-multilang-framework-draft.md`（READY，commit 6de8297）§3.1–§3.3、§3.4 中與 LiveRuntime 相關部分、§5.1–§5.5
程式：dosgolem fork `workplace/dosgolem`（分支 buck-rogers-cht-output-overlay，HEAD 9e55973，未提交修改）；同步副本 `workplace/dosgolem-clean`

## 結論

- LiveRuntime 改為「共用觀測＋每語言通道」。只有 zh-TW 與英文時，phase254 七條回歸 rerun34 與 rerun33 **全部檔案逐位元組相同**
  （504 RGBA、236 PNG、52 JSON、52 log、七份文字）。
- 切換正確性四個時點（ECL 敘事窗、水平選單、手札面板開啟、手冊題進行中）× zh-TW／zz／en × 2×、3×：切換後的畫面與
  「一開始就用該語言」逐位元組相同；英文模式等於原版 baseline；所有收據的記憶體、CPU、indexed、palette 雜湊與停止步數相同，
  記憶體雜湊也等於不帶語言旗標的收據（已證實，限這四個時點）。
- 多一條語言通道（zh-TW＋zz）：每格 Frame 成本約 +0.9 ms（每通道），逐步觀測 BeforeStep 在 129M 步增加約 0.7 秒，
  啟動載入由約 0.27 秒增為約 0.42 秒（強推論：只量了一種腳本，重複三次，數值有噪音）。

## 1. 改動檔案

dosgolem（`apps/buckrogers/`、`cmd/buckrogers-text-receipt/`；xlate 通用層未改，清單見 `changed-files.txt`）：

| 檔案 | 內容 |
|---|---|
| `lang.go`（新） | 語言代碼、`LangFile`（`<family>.<lang>.tsv`）、`LangFontPath`（`font/buckrogers-<lang>.golemfnt`）、`LangCycle`、允許空檔的讀取與語言檔讀取 |
| `live_runtime.go`（重寫） | 共用狀態（recorder、加入後選單／動作列／身體圖示／手冊 watcher、隊伍快照、劇情進行中呼叫、ASCII 表、正規化）與通道陣列；`LoadLiveRuntimeOptions`、`Languages`、`Language`、`SetLanguage`、`NextLanguage`、`LaneResets`；英文模式；`LogbookTurn` 依目前語言；DebugSummary 逐語言 |
| `live_lane.go`（新） | `liveLane`：每語言 × 每倍率 presenter、owner（技能離開、加入後提示、劇情第 9 頁）、B 類 watcher、名字資料、字型、計數；載入先建驗證；錯誤只重建本通道；合成時缺字略過該層 |
| `live_menu.go`、`live_menu_load.go`、`live_layer_rects.go` | 選單 presenter 移出 recorder（`newLiveMenuRecorder`）；共用選單載入與每語言譯文、選單逐列先建驗證 |
| `menu.go`、`menu_overlay_runtime.go` | identity-only catalog；presenter 依 TextKey 查本語言譯文，缺譯清自己的矩形 |
| `skill_exit*.go`、`post_join_exit_prompt*.go` | `*Lang` 載入（zh-TW 仍完全吻合）；缺譯清空、保留 watcher、記讓位矩形（第 24 列清除帶／原文格範圍） |
| `post_join_menu.go` | zh-TW 保留常數雜湊釘選；其他語言不釘雜湊、0 或 7 列；缺一項整組不畫、讓位 7 項原文格 |
| `action_bar*.go` | `DeriveActionBarNormalStyle`：恰一個半形 `(X)`、字母同 zh-TW、字母用 `normal_first_fg`；移除長度 5 釘選（改為與推導結果一致）；缺譯清矩形 |
| `body_icon_overlay.go` | `*Lang` 載入；請求為單位缺譯、讓位安全矩形；`validateAll` 先建（含儲存後綴各名字長度） |
| `manual.go`、`watcher.go`、`manual_overlay_runtime.go` | 共用 watcher 只帶鍵；`translation_runes` 由 zh-TW catalog 依鍵補（JSON 不變）；presenter 依鍵查譯文，缺譯接受事件並清空 |
| `live_story.go`、`story_page9_catalog.go` | 劇情頁每語言載入，未完整翻譯的頁整頁略過；第 9 頁雜湊釘選只對 zh-TW |
| `ecl_text.go`、`hmenu.go`、`engine_text.go`、`logbook.go`、`name_glossary.go`、`header_columns.go` | 語言檔名參數化；`NameGlossary` 每語言（zh-TW 用 `name-glossary.tsv`，其他語言 `name-glossary.<lang>.tsv`，缺席即不加註）；欄名列非 zh-TW 語言缺譯或放不下改一般排版 |
| `cmd/buckrogers-text-receipt/main.go`、`lang_flags.go`（新） | `-lang`、`-lang-switch`、`-compose-every-retrace`、`-test-lang-dir`、`-test-lang-font`、`-cpuprofile`；多語旗標時收據加 `cpu_sha256`（與 `session.StateDigest` 同算法）、`live_language`、`live_lang_switches`、`live_frames`、`live_load_ms` |
| 測試 | 新 `live_lang_test.go`（15 項＋載入 benchmark）；`header_columns_test.go`、`logbook_test.go`、`story_font_test.go` 改讀通道欄位 |

主 repo `tools/`：新 `catalog_lang.py`（`catalog_name`、`--lang`）與 `test_catalog_lang.py`；21 支工具接受 `--lang`／`lang=`，預設 zh-TW
（body_icon_catalog、body_icon_text_safe_rects、character_sheet_events、class_events、class_request_receipt、gender_events、
career／technical_skill_screen_catalog、name_prompt_catalog、menu_events、save_roster_join_catalog、save_roster_join_request_receipt、
header_columns、name_glossary、translit、eten_font、ecl／hmenu_translation_merge、logbook_merge、ui／manual_runtime_smoke）。
Big5 檢查只對 zh-TW。`tools/package.sh` 未改（第二段）。

## 2. 測試

| 項目 | 結果 | 檔案 |
|---|---|---|
| `go test ./...`（dosgolem-clean，`BUCKROGERS_ZZ_DIR` 設定） | 29 套件 ok；`cmd/buckrogers-play`、`frontend/ebiten` 為既有 cgo build failed | `test-all.txt` |
| `GOOS=windows CGO_ENABLED=0 go build ./...` | 通過 | `build-windows.txt` |
| Python `unittest discover`（python:3.13-slim） | 297 項 OK（改前 293 項 OK） | `py-base.txt`、`py2.txt` |
| gofmt（本輪改動檔） | 只剩 `live_menu.go` 既有四行未對齊（phase293 待決事項，未代為格式化） | — |

§5.1 單元測試對應：檔名參數化、共用 watcher 只帶鍵與 runes 來源、動作列推導、post_join 釘選／0 或 7 列、四家族缺譯讓位
（技能離開、加入後提示、加入後選單、身體圖示；選單逐列清矩形）、手冊缺譯被消費不重試、英文合成等於原版、`LogbookTurn`
英文回 false 與多語夾住、載入失敗移出（zz 檔壞、缺檔、缺字型）與 zh-TW 失敗為啟動失敗、執行期錯誤只重建本通道、
畫圖缺字略過（選單改原版底圖）、retrace 與合成前都同步所有語言（英文模式也同步）、B 類缺字只影響該語言、
切換後畫面等於一開始即用該語言。`mapKeys`、`lang` 腳本動作、設定檔屬第二段，未做。

## 3. 回歸（phase254 七條）

`runner` 先備份為 `runner-rerun33`（與 `rerun33/runner` 相同，SHA-256 `452ad744…`），換成本輪 `runner-new`（`c9a022c5…`）。
`rerun34/` 腳本由 rerun33 原樣複製。結果：全部 854 個輸出檔、七份 `rerun34-*.txt` 與 rerun33 逐位元組相同。
（實作中途另以 `p254-early/` 跑過一次，同樣全部相同。）

## 4. 切換正確性（§5.3–§5.4）

腳本 `switch/cases.sh`、比對 `switch/compare.py`、結果 `switch/compare.json`。每時點：S-L（一開始用 L）、W-L（三次切換後停在 L）、
M-zz（區間內 11 次循環後停在 zz）、none（無語言旗標）；全程 `-compose-every-retrace`。

| 時點 | state／停止步數（既有腳本） | 2× | 3× |
|---|---|---|---|
| ECL 敘事窗 | `phase104-manual-correct-return/control.state` 409,000,000（phase291 e027-f409 的 15 鍵） | 通過 | 通過 |
| 水平選單 | `phase258-ecl-ab/g2.state` 432,500,000（e028-h432 的 3 鍵） | 通過 | 通過 |
| 手札面板開啟 | `checkpoints/logbook41-pre.state` 5,285,000,000（e030-lb41-open 的 1 鍵） | 通過 | 通過 |
| 手冊題進行中 | `probe/phase12-before-question.state` 266,650,000（phase292 e005-first-b，無按鍵） | 通過 | 通過 |

通過的判準：W／M 等於 S、S-en 等於 baseline、zz 與 zh-TW 畫面不同且 zh-TW 有疊字、記憶體／CPU／indexed／palette／停止步數同。
手冊時點的 RGBA 比對後刪除，只留雜湊；沒有輸出 PNG。

## 5. 效能（§5.5）

固定腳本 e027-f409（129M 步、782 個 retrace），2×，每個 retrace 合成，各三次（`perf/perf.json`、`perf/*.prof`）：

| 組 | CPU 秒（三次） | 平均 |
|---|---|---|
| 無 LiveRuntime | 12.8／10.7／10.0 | 11.2 |
| zh-TW＋英文 | 30.4／24.9／24.0 | 26.4 |
| zh-TW＋zz | 29.9／27.6／26.0 | 27.8 |

profile（第 3 次）：`Frame`（全部通道）0.68 → 1.37 秒，約每通道每格 0.87 ms；B 類 hook 期間（`observeEclText`＋`observeHMenu`）
0.95 → 1.04 秒；`BeforeStep` 累計 4.45 → 5.12 秒；`ComposeWith` 只合成目前語言，2.1 秒不隨通道數變。
啟動（`BenchmarkLiveLoad`，5 次）：zh-TW 0.27 秒、zh-TW＋zz 0.42 秒（收據內 `live_load_ms` 170–360 ms）。
粗估 4 語言：每格 Frame 約 3.5 ms，BeforeStep 在同腳本約多 2 秒，啟動約 0.7 秒（推估，未實測）。

## 6. 交給第二段的 API

- `LoadLiveRuntimeOptions(LiveOptions{TextDir, FontPath, Langs, LangFonts, LangDirs})`；`LoadLiveRuntime(textDir, font)` 等同只載 zh-TW。
  `LangFontPath(root, lang)`；zh-TW 字型由呼叫端決定（倚天優先、`-font` 覆寫照舊）。
- `Languages() []LangStatus{Code, Enabled, Reason}`（F4 循環順序，未載入者 Reason「未載入」，失敗者為原因）、
  `Language()`、`SetLanguage(code)`（未知或未啟用回錯誤）、`NextLanguage()`、`KnownLang(code)`。
- 英文模式：`SetLanguage("en")` 後 `Compose` 等於 `ScaleIndexedRGBA`；`LogbookTurn` 依目前語言面板決定、各通道在自己頁數內夾住。
- 語言停用原因同時印到 stderr（`buckrogers: 語言 X 停用：…`）並出現在 DebugSummary（`語言停用=`）。

## 7. 未量到／偏離

1. 效能是用 receipt 工具量，不是前端 `-frames`／`-clock 50`：前端需 cgo（X11、ALSA），Docker 內無法建置。
2. g2.state 在 430.5M／432.5M 的 ECL 無命中（phase258 `h*.log` Hits:0），ECL 敘事窗改用 e027-f409 的 state；水平選單仍用 g2。
3. zz 劇情第 1–8 頁、B 類家族由 zh-TW 機械刪字產生（`make_zz.py`），手冊為合成填充字；zz 只在 `workplace/phase296-multilang-lanes/zz/`。
4. 未量畫面：商店、戰鬥等其他家族的多語切換沒有收據；只量上表四個時點。

## 8. 待決

1. 劇情第 9 頁的譯文雜湊釘選：規格只寫 post_join 的釘選改制，本輪同樣處理為「只對 zh-TW 釘選」，否則 zz 無法滿足「第 9 頁單列」契約。需確認。
2. `obs.Dropped` 重建依規格不計錯誤，改記在 `rebuilds=`（只在非零時印）；這次回歸路徑上沒有觸發，DebugSummary 未變。
3. 多語旗標才輸出 `cpu_sha256` 等新欄位，以維持既有收據 JSON 逐位元組不變。若要每張收據都帶 CPU 雜湊，基準需更新。
4. 手札鍵盤緩衝狀態目前每通道各一份（由同一事件驅動，狀態相同），不是規格字面上的共用一份。
5. 非 zh-TW 語言的 Python 驗證器仍沿用 zh-TW 的完全吻合檢查（只改檔名）；缺列允許與字集白名單留給 041–045。
6. B 類家族（ECL、水平選單、引擎、手札）的譯文沒有載入時先建（執行期排版），缺字走執行期的單語言 discontinuity。
7. `live_menu.go` 既有 gofmt 未對齊仍未處理。

## 9. 檔案

`go.sh`、`sync.sh`、`changed-files.txt`、`new-files.txt`、`clean-backup/`、`test-all.txt`、`build-windows.txt`、`base-test.txt`、
`py-base.txt`、`py2.txt`、`bench-load.txt`、`make_zz.py`、`zz/`、`p254run.sh`、`p254-early/`、`switch.sh`、`switch/`、`perf.sh`、`perf/`、
`runner-early`、`runner-new`；phase254 目錄新增 `runner-rerun33`、`rerun34/`、`rerun34-*.txt`，`runner` 換為 `runner-new`。
