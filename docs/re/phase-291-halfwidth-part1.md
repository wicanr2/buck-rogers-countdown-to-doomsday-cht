# 第二百九十一階段：規格 039 第一段（半形英數字）實作與同狀態驗收

日期：2026-09-29
狀態：定稿（主代理審閱，2026-09-29）；實作 dosgolem `6784b4f`；phase254 新基準 rerun30
範圍：規格 039（READY，2d68806）第一段：字型工具、dosgolem 半形衍生與版面模型、ECL（027）、水平選單（028）、引擎 dispatcher（029／036／038）、手札（030）、劇情逐頁（010–017、022）、動作列（215）、身體圖示與劇情第 9 頁容量。
第二段（選單類 001／018／020／021、主選單 3× scoped、手冊 2×／E1、034 英文列、手冊 owner）未動程式。
收據、RGBA、PNG、runner 只在 ignored 的 `workplace/phase291-halfwidth/`。

## 1. 實作

### 1.1 dosgolem（fork `buck-rogers-cht-output-overlay`，工作樹，基底 94825fb；已同步 `dosgolem-clean`，apps／cmd／xlate 逐檔相同）

| 檔案 | 內容 |
|---|---|
| `apps/buckrogers/halfwidth.go`（新） | 半形單位（U+0020–U+007E、U+2022＝1，其餘 2）；§3.1 補位（先 U+0020 到偶數、U+3000 補格、奇數終點尾補 U+0020）；拆段 `splitSegments`（寬度類別或前景色改變）；段 key `<列 key>#<段序>` 與去重 `dedupRowKeys`；`DeriveHalfFonts`（第 4–11 欄 → 8×16，最近鄰 1.5 倍 → 12×24，墨跡越界即失敗，名稱 `.half8x16`／`.half12x24`，空名用 `buckrogers.`）；`halfFontsOf` 以底字型指標快取，同 session 共用同一指標與名稱 |
| `ecl_text.go`、`ecl_text_overlay.go` | 排版以單位計（`Left`／`Right`／`CursorCol` 換算、`EclTextLine.Col` 與 `endCol` 為單位）；presenter 每列組合後補位再拆段；起始列 X 仍為 `TopCol×8` |
| `hmenu.go`、`hmenu_overlay.go` | 總寬 `2×(40−起始欄)` 單位、分隔 1 單位；`HMenuRow.Pos`／`UnitPos`／`Units`／`WidthCells`；每 rune 一筆 stamp、key 不變，X＝起始格＋單位位置×4 |
| `engine_dispatch.go` | 一般路徑「單位 ≤ 原文長度×2」、`Text` 補位到 `2×Width`；§2.9 以單位判斷；§2.10 前段放到 `2×len(S1)`、全形字整字移到後段；038 候選「≤ 可用格×2 單位」，延伸格終點 `col+⌈單位/2⌉`；`Page()` 帶單位位置 |
| `engine_text.go` | §2.6 表格列：總單位＝原文長度×2，最後一欄靠右錨定原文右緣，前段與最後一欄間 §3.1 補位且至少 1 單位，放不下退回英文 |
| `logbook.go` | 本文 72 單位／列、19 列；標題 76 單位（036 選段同步）；面板以段繪製 |
| `live_runtime.go` | dispatcher 逐列讓位與 `untouchedRows` 改用 `WidthCells()`；031 字形表搜尋與計數保留作診斷，取得後不再重建通用 presenter、不再換劇情字型；半形衍生失敗時 `DebugSummary` 記 `half-font-error=` |
| `story_*_overlay.go`、`story_page4.go`、`story_font.go` | 九頁劇情每列補位到 `2×格數` 單位後拆段；容量 78 單位（第 8 頁 76、第 9 頁 40）；`ActiveKeys` 回去重後的列 key；`SetFont` 只換全形段字型（API 相容，已無呼叫者） |
| `action_bar_overlay.go` | 半形字改用半形字型、`GlyphX/Y=0`、`GlyphScale=1`；前進與 key（`<event>#<rune>`）不變；全形字 2×、3× 不變 |
| `body_icon_overlay.go` | 容量以單位計，以段繪製（目前譯文無半形字） |
| `name_scan.go`、`cmd/buckrogers-name-scan` | 靜態掃描介面沿用格座標、內部換算單位；手札標題寬度欄改為單位 |
| `cmd/buckrogers-text-receipt`（`main.go`、`story_ascii.go`） | 劇情字形表搜尋保留、不再 `SetFont`；`presenters`／`set_font_errors` 恆為 0 |
| 測試 | 新增 `halfwidth_test.go`；依單位語意更新 `ecl_text_test`、`engine_text_test`、`hmenu_test`、`name_glossary_test`、`party_panel_test`、`player_name_test`、`story_font_test`（031 換字型測試改為 039 行為）、`action_bar_overlay_test`、`action_bar_overlay_runtime_test` |

xlate 等通用層未改。第二段家族（`menu_overlay*`、`post_join_*`、`skill_exit_*`、`manual_*`、`help.go`）未改。

### 1.2 主 repo（工作樹）

| 檔案 | 內容 |
|---|---|
| `tools/halfwidth.py`（新） | 半形單位與 16×16 字模第 4–11 欄墨跡規則 |
| `tools/catalog_font.py` | `build` 前檢查半形墨跡，越界即失敗 |
| `tools/eten_font.py` | `encode_golemfnt` 與 `decode_golemfnt` 都檢查半形墨跡 |
| `tools/story_*_catalog.py`（9 個） | 以準確單位計；上限 78（第 8 頁 76、第 9 頁 40） |
| `tools/logbook_merge.py` | 72 單位／列，與 Go 排版一致 |
| 測試 | `test_catalog_font.py`、`test_eten_font.py`（合成負例）、`test_story_*_catalog.py`（邊界改單位）、新增 `test_logbook_merge.py` |

## 2. 測試

| 項目 | 狀態 | 收據 | 推論等級 |
|---|---|---|---|
| `go test ./...`（`BUCKROGERS_CHT_ROOT` 掛主 repo text，唯讀） | 29 套件 ok；`cmd/buckrogers-play`、`frontend/ebiten` 為既有 cgo 標頭 build failed | `test-all.txt` | 已證實 |
| `GOOS=windows CGO_ENABLED=0 go build ./...` | 通過 | `build-windows.txt` | 已證實 |
| `go vet`（buckrogers、text-receipt、name-scan） | 無訊息 | — | 已證實 |
| Python `unittest discover`（tools/） | 282 項通過 | `py-test-all.txt` | 已證實 |
| 兩份工作字型半形墨跡（含 `•`） | 倚天 x[4,11] y[2,14]、Unifont x[5,11] y[1,15]；各 96 個半形字、錯誤 0 | `font-ink-check.txt`、`font_ink_check.py` | 已證實 |

§5.2 對應的單元測試（全部通過）：

| §5.2 項目 | 測試 |
|---|---|
| 單位與拆段：純英文、純中文、混排、奇數長、內容空白、`•`、前景色切段 | `TestHalfUnitsAndSegments` |
| 補位順序（先 U+0020 再 U+3000、奇數終點尾補） | `TestHalfPaddingOrder` |
| U+3000／U+0020 通過缺字預檢（ECL、水平選單／dispatcher、手札、劇情） | `TestHalfBlankNeedsNoGlyph` |
| 2×、3× 半形字模像素（含 1.5 倍取樣對照）、執行期墨跡檢查與負例、同 session 共用 | `TestHalfFontDerivation`、`TestHalfGlyphPixelsThroughPresenter` |
| 容量邊界：ECL、水平選單、手札（本文／標題）、劇情 78／76／40、身體圖示 | `TestHalfCapacityBoundaries`、`TestHalfBodyIconCapacityUnits` |
| dispatcher 一般路徑、表格最後一欄右緣與退回英文、讓位範圍 | `TestHalfDispatcherGeneralCapacity`、`TestHalfTableLastColumnRightEdge`、`TestHalfDispatcherYieldRange` |
| 熱鍵色逐 rune 不變、每 rune 一筆 stamp 與 key | `TestHalfHMenuStampsPerRune` |
| 列群組三種觸發（動作列：段移除、部分 Clear 造成透明、錨定格指紋改寫）與對照 | `TestHalfActionBarRowGroupClears` |
| 動作列 key 不變、助記字母完整 | `TestActionBarOverlayMnemonicWholeAndKeysKept` |
| 038 邊界（單位） | `TestPartyPanelBoundaries` 等（已改單位） |

§5.2 中屬第二段的項目（Frame 定色同列共用、選單換字無殘段、主選單 3× scoped 與手冊 owner 封存驗證、E1）本段未做。

## 3. 靜態回歸（§5.3）

詳見 `static-diff.md`。摘要：

- ECL 標準窗：2,542 key 溢出 0→0、036 段別全為「全部加註」不變；27 個 key 少 1 列。
- 引擎片段 1,497、怪物名 49：單獨畫出時放得下的條數不變（1,491／49）。
- 水平選單：993／1,699 個項目變窄，合計少 1,141 格；最寬 36→25 格。
- 手札：71 則皆 1 頁、段別不變；22 則本文少 1–3 列，另 19 則首列換行點改變。
- 038：7 個樣本中 NICOLE STEELE 的角色頁標題由只中文升為完整加註；其餘只是覆繪變窄。

## 4. 同狀態 A/B（§5.4）

old＝`git archive 94825fb` 建置（`runner-old`，SHA-256 `501f4fdc…dbf3e84`），new＝`dosgolem-clean` 本輪（`runner-new`，SHA-256 `97336565…d8702a`，重建逐位元組相同）。
同一份 `/project/text` 與 `workplace/current-font`（倚天），同 state、同按鍵、同停止點，2×、3× 各一次。
腳本：`ab.sh`／`ab-inner.sh`／`run.sh`／`jobs.sh`／`jobs-038.sh`／`diff.py`／`abtable.py`；全表 `ab-table.txt`。
全部 Docker（`--rm`、`--network none`、`--cpus 2`、`--memory`、`--pids-limit`、目前 UID/GID、log rotation），容器名 `buck-phase291-*`，結束後無殘留容器、無 root 擁有檔。

下表「差異位置」是 old 與 new live 相異的 8×8 格（邏輯座標；2× 與 3× 全部相同）。除 `e028-fm4` 外，每案 baseline（原版畫面）old＝new，原版記憶體、indexed、palette 雜湊與停止點 old＝new。

| 項目 | 狀態 | 差異位置 | 收據 | 推論等級 |
|---|---|---|---|---|
| 027 f409（phase104 control，接續句） | 新基準 | r7 c19–22（隊伍欄 `•`）、r15 c17–27（座標列） | `ab/e027-f409-*` | 已證實 |
| 027 shaft（通風管，「弗拉維烏斯(FLAVIUS)」） | 新基準 | r15 c17–29、r17 c18–38、r18 c1–9（重排；第 18 列後段不再需要） | `ab/e027-shaft-*`；`shots/e2e-ecl-shaft-2x.png` | 已證實 |
| 027 atk2（CELESTE 發動攻擊） | 新基準 | r17 c5–18 | `ab/e027-atk2-*` | 已證實 |
| 036 lb41-ecl2（「卡頓•特必安(CARLTON TURABIAN)」） | 新基準 | r17 c6–38 | `ab/e036-lb41-ecl2-*` | 已證實 |
| 036 lb60-panel（手札 60 人名加註） | 新基準 | r2–r20（面板本文重排） | `ab/e036-lb60-panel-*` | 已證實 |
| 028 h431、h432（主指令列） | 新基準 | r24 c4–34、c2–34 | `ab/e028-h43[12]-*` | 已證實 |
| 028 h430（負控制，原版 `Exit`） | 零差 | none | `ab/e028-h430-neg-*` | 已證實 |
| 028 m5330（交誼廳選單） | 新基準 | r24 c6–30 | `ab/e028-m5330-*` | 已證實 |
| 028 fm4（功能選單，bsave 接 Y） | live 零差；原版記憶體雜湊不可比 | none；見 §5 第 1 條 | `ab/e028-fm4*` | live：已證實；記憶體：強推論 |
| 029 gbuy（商店表格，最後一欄數字） | 新基準 | r2–r16 名稱欄與數字欄、r24 c11–17；數字右緣落在原文右緣（欄 38 右緣） | `ab/e029-gbuy-*`；`shots/crop-table-gbuy-2x-base-old-new.png` | 已證實 |
| 029 gder（座標列「24,20 西 01:02」） | 新基準 | r7 c19–22、r15 c17–29 | `ab/e029-gder-coord-*`；`shots/e2e-coord-gder-2x.png`、`crop-coord-gder-3x-*` | 已證實 |
| 029 ggren（§2.9「誰要撲向手榴彈？」） | 新基準 | r7 c19–22、r24 c26–32（同列水平選單以單位重排） | `ab/e029-ggren-2.9-*` | 已證實 |
| 029 c870（戰鬥：NEO 戰士、爆能槍 (250)、兩列選單） | 新基準 | r1 c23–28、r7 c26–31、r23 c4–22、r24 c2–28 | `ab/e029-c870-*` | 已證實 |
| 029 gear（FLAVIUS 的裝備） | 新基準 | r6 c7–11、r24 c4–34 | `ab/e029-gear-*` | 已證實 |
| 029 ginj（治療句，無英數） | 零差 | none | `ab/e029-ginj-*` | 已證實 |
| 030 lb41 開啟 | 新基準 | r2–r12（面板重排；混合大小寫人名改以覆繪字型小寫顯示，見 §5 第 3 條） | `ab/e030-lb41-open-*`；`shots/e2e-logbook-lb41-2x.png`、`crop-logbook-lb41-2x-old-new.png` | 已證實 |
| 030 lb41 關閉 | 零差 | none | `ab/e030-lb41-close-*` | 已證實 |
| 030 lb38 開啟 | 新基準 | r2–r17（面板重排） | `ab/e030-lb38-open-*` | 已證實 |
| 030 lb38 關閉（座標列「23,22 南 01:29」） | 新基準 | r15 c17–29 | `ab/e030-lb38-close-coord-*` | 已證實 |
| 劇情第 1 頁 p1（(BUCK ROGERS)、(RAM)） | 新基準 | r17 c8–21、r21 c8–14；另 r7 c19–22、r15 c17–28（背景探索畫面） | `ab/e287-p1-*`；`shots/e2e-story-p1-2x.png` | 已證實 |
| 劇情第 2 頁 p2（NEO） | 新基準 | r17 c8–17 | `ab/e287-p2-*` | 已證實 |
| 劇情第 6 頁 p6、p6alt（036 加註「(CARLTON TURABIAN)」、NEO） | 新基準 | r19 c3–25、r21 c8–15 | `ab/e287-p6*-*` | 已證實 |
| 038 ba1、ba2（全寬表／Pick Character） | 新基準 | r4–r9 名字欄；ba1 另 r24 c17–25、ba2 另 r22 c12–15、r24 c20–22 | `ab/e038-ba[12]-*`；`shots/e2e-fullwidth-ba1-2x.png`、`-3x.png` | 已證實 |
| 038 a6 角色頁標題 | 新基準 | r1 c13–21、r11 c11–15、r24 c4–30 | `ab/e038-a6-sheet-*` | 已證實 |
| 038 a7 隊伍欄 | 新基準 | r7 c19–22（「妮可•斯蒂爾」的 `•` 半形） | `ab/e038-a7-column-*` | 已證實 |
| 038 rm1（5 人，Enter＋下） | 新基準 | r4 c6–14、r5 c4–11、r24 c17–25 | `ab/e038-rm1-down-*` | 已證實 |
| 動作列 career-subtract | 新基準 | r24 c2–16：舊版助記字母只剩左半（裁切），新版 `(A)(S)(D)` 完整 | `ab/e215-career-subtract-*`；`shots/crop-actionbar-{2,3}x-old-new.png` | 已證實（修正 215 既有裁切） |
| 動作列 technical-base | 新基準 | r24 c2–26 | `ab/e215-technical-base-*` | 已證實 |
| 動作列 career-base（停止點為名字提示列，動作列未出現） | 零差 | none | `ab/e215-career-base-*` | 已證實 |
| 動作列 technical-exit（負控制） | 零差 | none | `ab/e215-technical-exit-neg-*` | 已證實 |

### 4.1 phase254 七條回歸（rerun30）

- `runner` 先備份為 `runner-rerun29`（SHA-256 `2549a8d5…5d836976`，與原 `runner` 逐位元組相同），再換成本輪 `runner-new`；新結果在 `phase254-live-families-parity/rerun30/` 與 `../rerun30-*.txt`。腳本 `p254.sh`，差異清單 `p254-diff.txt`（`p254diff.py`）。
- 七份文字：story、opening、manual、post、action、body 與 rerun29 逐字相同；skill 由「cprompt、tprompt same」變為 DIFF（見下）。
- 504 份 RGBA 中 444 份逐位元組相同，60 份不同，全部位於本段家族的英數字或重排處：

| 案例 | 差異位置 | 歸因 |
|---|---|---|
| career-add／down／drawn、tech-down／drawn（ab、expect、live） | r24 c2–16／c2–26 | 動作列半形助記字母 |
| cprompt、tprompt（live） | r24 c33–38／c34–39 | 水平選單「是(Y) 否(N)」：舊版 11 格超出起始欄 33 後的 7 格（`Overflows:1`），新版 11 單位放得下（`Hits:1`）而顯示中文 |
| cn（live） | r24 c2–16 | 同一列水平選單改為單位（舊版已是 DIFF） |
| confirm（live） | r24 c12–19 | 「是(Y) 否(N)」半形（水平選單或 dispatcher 繪製；本段家族，強推論） |
| move、refuse（live） | r24 c22–24 | 「完成(D)」的 `(D)` 半形（同上，強推論） |
| o275000000、o282000000、m275000000（live） | r7 c19–22、r15 c17–28 | 隊伍欄 `•`、座標列 |
| o280900000（opening、expect、live） | r17 c8–21、r21 c8–14（live 另有 r7、r15） | 劇情第 1 頁 (BUCK ROGERS)、(RAM) |
| pj-row20、q1、yy（live） | r21 c12–15；q1 另 r24 c13–15、yy 另 r24 c31–33 | 加入後選單「離開至 DOS」的 `DOS` 與第 24 列選單英數字（本段家族覆繪，強推論） |

skill 的 cprompt／tprompt 文字變為 DIFF，是因為比對基準（menu＋skill 家族輸出合成）不含水平選單，而水平選單這次首次在該列顯示；列內其他格與 rerun29 相同。

## 5. 限度與觀察

1. `e028-fm4`：old 與 new 的原版記憶體雜湊不同，但同一 runner 的 2× 與 3× 兩次也不同（固定暫存層路徑重跑 `e028-fm4-fixed` 亦然），indexed、palette、停止點與 live 畫面相同。判斷為此重播點（帶暫存層）本身的記憶體雜湊不可重現，與覆繪無關（強推論；覆繪層不寫模擬記憶體）。原因未追。
2. 3× 半形字高：倚天 12×24 墨跡在格內第 3–22 列，與中文對齊；Unifont 版差 1 像素（規格 §2 已記）。本輪 A/B 只用倚天工作字型，Unifont 的 3× 畫面未實跑。
3. 手札、劇情第 6 頁等以混合大小寫加註的英文（036 `NameCaseMixed`），舊版經 031 原版字形表只有大寫字形而顯示成大寫；新版用覆繪字型的半形字，顯示為原本的大小寫（如 `Carlton Turabian`、`Bank of Luna`）。屬換字形的直接結果，請使用者確認是否接受。
4. 加入後選單的「離開至 DOS」列，`DOS` 在本段已變半形。021 家族程式未改，該列由本段家族（029 共用呼叫端 dispatcher 或 028）覆繪（強推論：該幀 dispatcher 與水平選單皆有命中，未逐筆追蹤）。第二段處理 021 時請一併確認這一列的擁有者。
5. 含 `•` 的怪物名遭遇：本機沒有可到達的 state，只有單元測試（`•` 以半形計）。未量到。
6. 列群組三種觸發只在動作列實作與驗證（動作列本來就是每 rune 一筆 stamp，`reconcileGroups` 已涵蓋）；選單類與無 style 手冊屬第二段。
7. 靜態回歸的 ECL 只量標準窗；手札換行點只比對首列雜湊。

## 6. 待決

1. phase254：是否以 rerun30 為新基準（skill 的 cprompt／tprompt 文字結果由 same 變 DIFF，原因見 §4.1）。
2. §5 第 3 條大小寫顯示是否接受。
3. 本輪執行 `gofmt -w apps/buckrogers` 時誤改了非本段檔案的空白格式：3 個已追蹤檔（`live_menu.go`、`ecl_text_test.go`、`party_panel_test.go`）已以 `git checkout` 還原；2 個未追蹤檔（`story_page9_candidate_geometry_test.go`、`story_page9_candidate_prewrite_test.go`）已用 `dosgolem-clean` 內的原檔還原（原檔經 gofmt 後與誤改結果逐位元組相同）；另 4 個未追蹤檔（`command_status_columns_probe_test.go`、`command_status_cross_state_probe_test.go`、`command_status_literal_probe_test.go`、`command_status_roster_identity_negative_test.go`）沒有原檔副本，只被 gofmt 改了空白排版，內容語意未變，無法還原成原排版。請使用者決定是否需要處理。
4. 修正了兩個原本在設定 `BUCKROGERS_CHT_ROOT` 時就失敗的既有測試（`TestRuntimeActionBarOverlayFrameDrawReappliesInjectedColors`、`TestActionBarOverlayUses22PixelCJKOnlyAtThreeTimes`，以 94825fb 原始碼重跑確認為既有失敗；兩者把 layer 順序當 rune 序號，與正式譯文「加點(A)」不符）。
5. 暫存：`dosgolem-clean/workplace/p291-old-src`（約 16M，runner-old 的原始碼樹，內含靜態探針）。請使用者決定是否刪除。
6. dosgolem fork 歷史作者含 `codex@openai.com`（既有，非本輪產生）。

## 7. 檔案

`go.sh`、`go-old.sh`、`sync.sh`、`new-files.txt`、`run.sh`、`ab.sh`、`ab-inner.sh`、`jobs.sh`、`jobs-038.sh`、`diff.py`、`abtable.py`、`ab-table.txt`、`crop.py`、`p254.sh`、`p254diff.py`、`p254-diff.txt`、
`zz_phase291_static_test.go`、`static/`、`static-diff.md`、`font_ink_check.py`、`font-ink-check.txt`、`test-all.txt`、`build-windows.txt`、`py-test-all.txt`、`runner-old`、`runner-new`、`ab/`、`shots/`。
