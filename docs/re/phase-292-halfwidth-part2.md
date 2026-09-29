# 第二百九十二階段：規格 039 第二段（半形英數字）實作與同狀態驗收

日期：2026-09-29
狀態：定稿（主代理審閱，2026-09-29）；實作 dosgolem `1a51987`（第二段）、`1584b05`（E1）；phase254 新基準 rerun32
範圍：規格 039（READY）第二段：選單類（001／018／020／021）、主選單 3× scoped（004）、手冊 2× 與固定字格 3×（005）、
手冊英文列（034）、手冊 snapshot owner（2×）。
手冊 3× E1（005）：初稿因規格縱向位置矛盾而停（§5）；規格更正為 `sealed.y+0`（主 repo `815499c`）後已實作，見 §9。
本文件不含任何手冊題目、答案或摘錄單字；手冊題畫面只記 RGBA 雜湊與差異格，不輸出圖片。

## 1. 實作

### 1.1 dosgolem（`apps/buckrogers/`；xlate 等通用層未改）

| 檔案 | 內容 |
|---|---|
| `row_group.go`（新） | §3.3 列群組規則：同一原列的各段為一組；觸發 1（段被移除或段數減少）、觸發 2（任一格變 `Transparent`）、觸發 3（本幀新的指紋失效錨定格，且群組以 8×8 格換算的有效錨定格 ≤ 2；錨定格在 Pending→Shown 時依段計算）任一成立，就以整列矩形 `Clear`。Pending→Shown 時同列各段共用整列範圍算出的前景／背景色。Restore 後由 layer 重建群組（錨定格未知，觸發 3 暫停） |
| `menu_overlay.go` | `BuildMenuOverlay` 容量改單位（`2×前綴格＋譯文單位 ≤ 2×格數`）；譯文以 §3.1 補位到整個安全矩形再拆段；缺字預檢略過 U+0020／U+3000；墨跡包含檢查改對整列各段 |
| `menu_overlay_runtime.go` | `Apply` 改為先以安全矩形 `Clear`，再加入各段並登記群組；檢查點：`Frame` 之後、`ClearTextCells`／`clearRect`（`LiveMenuRuntime.ClearRect` 走這裡）之後、`Add` 之後；`ActiveKeys` 回去重後的原列 key |
| `menu_overlay_scoped_3x.go` | 只接受 3×；registry 由兩個字型增為三個（`buckrogers.menu.eten16.v1`、`.eten22.v1`、`buckrogers.menu.eten16.v1.half12x24`），半形字型由已驗 SHA 的底字型以指標衍生，驗寬 12、高 24、名稱、字元集與逐 byte 等於衍生演算法；每次 `Apply`／封存都驗三個指紋；逐段換字型（全形段 22 點、半形段 12×24）；封存驗證以原列 key 比對十鍵白名單，半形段必須是 registry 內的半形字型 |
| `live_layer_rects.go`、`live_menu_load.go`、`live_runtime.go` | `LiveMenuRuntime.ClearRect` 經群組規則；live runtime 只載一次字型，選單家族與其他家族共用同一指標，半形字型因而每 session 只衍生一次；034 字型檢查傳入 2×／3× 半形字型 |
| `post_join_exit_prompt_overlay.go`（021）、`skill_exit_overlay.go`（020） | 容量改單位；補位後拆段；缺字預檢略過空白；墨跡檢查對整列 |
| `manual_overlay_runtime.go` | `manualRows` 改為每列 72 單位、放不下的全形字整字換行、超過 14 列即拒絕（取代 504 字）；每列補位到 72 單位後拆段，空白列為一段 36 個 U+3000；段 key `manual.<gen>.<textKey>.<row>#<n>`；catalog 預檢改列數判準並對半形字查半形字型；無 style 時以列群組規則 `Frame`；E1 路徑不變 |
| `manual_english.go`（034） | 長式／短式以單位計（每列 72 單位）；呈現以段繪製；字型檢查：寬 < 16 的字型視為半形字型，只檢查半形字 |
| `manual_snapshot_owner.go` | 2× owner 持有 `buckrogers.manual.base-16.v1.half8x16` 並記指紋；來源驗證改為「同列 key 各段單位總和 72、`CellW` 為 4 或 8、字型屬 registry」並與決定性重排結果逐欄比對；封存 fonts 加入半形字型並驗指紋 |
| 測試 | 新增 `halfwidth_part2_test.go`；更新 `menu_overlay_test`、`menu_overlay_scoped_3x_test`（合成字型的 ASCII 墨跡移到第 4–11 欄、正式 catalog 測試只跑 3× 並驗 2× 被拒）、`manual_overlay_runtime_test`、`manual_e1_plan_test`（合成 ASCII 墨跡移到第 4 欄）、`manual_english_test`、`manual_snapshot_owner_test`（2× layer Snapshot 黃金雜湊改為新值；RGBA 黃金值不變） |

未改：`manual_e1_plan.go`（E1）、`post_join_menu.go`（018 經 `BuildMenuOverlay` 自動拆段；以 Prewrite 清列，不接群組規則）、cmd/。

### 1.2 主 repo

未改。`tools/*.py` 的行寬 lint 以 rune 計，比單位制嚴格，不會讓現有資料不合格。

## 2. 測試

| 項目 | 狀態 | 收據 | 推論等級 |
|---|---|---|---|
| `go test ./...`（`dosgolem-clean`，`BUCKROGERS_CHT_ROOT` 唯讀掛主 repo text） | 29 套件 ok；`cmd/buckrogers-play`、`frontend/ebiten` 為既有 cgo build failed | `test-all.txt` | 已證實 |
| `GOOS=windows CGO_ENABLED=0 go build ./...` | 通過 | `build-windows.txt` | 已證實 |
| `go vet`（buckrogers、text-receipt；fork 工作樹含未追蹤草稿測試也可編譯） | 無訊息 | — | 已證實 |
| gofmt（只查本段改動檔） | 無差異 | — | 已證實 |
| 私有 39 題 E1 計畫（`TestManualE1PlanAll39PrivateCatalog`，本機 catalog 與字型） | 通過（E1 程式未改，確認新的 catalog 預檢不影響 E1） | `e1-private.txt` | 已證實 |

§5.2 屬本段的單元測試（全部通過）：

| §5.2 項目 | 測試 |
|---|---|
| U+3000／U+0020 通過缺字預檢（選單、020、021、手冊、034）；未使用的缺字不影響，使用到的半形缺字被拒 | `TestHalfPart2BlankNeedsNoGlyph` |
| 容量邊界（選單含前綴、021、020、手冊 72 單位整字換行與 14 列、034 長式） | `TestHalfPart2CapacityUnits` |
| 選單拆段、段 key、半形字型與偏移、2×／3× 半形字模像素 | `TestHalfPart2MenuSegmentsAndGlyphPixels` |
| 選單換字無殘段 | `TestHalfPart2MenuReplaceLeavesNoSegment` |
| Frame 定色同列共用 | `TestHalfPart2MenuFrameColoursShared` |
| 列群組三種觸發：段移除（指紋使半形段整段失效）、`ClearTextCells`、live `clearRect`、後到列覆蓋、`Add` 部分重疊、單格指紋失效、群組錨定格 ≤ 2；對照組不清除 | `TestHalfPart2MenuRowGroupTriggers` |
| 主選單 3× scoped：只接受 3×、registry 三字型、逐段換字型、封存接受半形段、拒絕非 registry 字型（底字型、22 點字型、同名異指標）、registry 同名換指標、半形指紋漂移 | `TestHalfPart2ScopedMenuHalfSegmentsAndSeal` |
| 手冊 2×／3× 固定字格：每列 72 單位、整字換行、空白列 36 個 U+3000、無 style 時單格失效整列清除 | `TestHalfPart2ManualSegmentsAndRowGroups` |
| 手冊 owner 封存接受半形段，拒絕非 registry 字型、單位總和不符、`CellW` 不在 {4, 8}、半形指紋漂移 | `TestHalfPart2ManualOwnerSealAcceptsHalfSegments` |

§5.2 中未做：E1 的 `ValidatePixelGlyphPlan`（見 §5）。

## 3. 靜態回歸（§5.3，只記數量與 key）

探針 `harness/zz_phase292_static_test.go`，輸出 `static.txt`。

- 手冊 39 題：39 題皆通過新的預檢（≤ 14 列）。含英數字 33 題；排版（換列點）改變 31 題；列數減少 15 題、增加 0 題、不變 24 題；全形字整字移到下一列共 31 次。改變的 key 見 `static.txt` 的 `manual-diff` 列。
- 034 英文列：摘錄 35 題，舊（rune 計）與新（單位計）皆可顯示 35 題，皆為長式；形式改變 0 題；排除 0 題。

## 4. 同狀態 A/B（§5.4）

old＝`git archive 6784b4f` 建置（`runner-old`，SHA-256 `12b7269a…`），new＝本輪 `dosgolem-clean`（`runner-new`，SHA-256 `7e92fb5a…`）。
同一份 `/project/text` 與 `workplace/current-font`（倚天），同 state、同按鍵、同停止點，2×、3× 各一次。
腳本：`jobs.sh`、`ab.sh`、`ab-inner.sh`、`run.sh`、`diff.py`（`NOPNG=1` 時不輸出圖片，只記雜湊）；主選單 3× scoped 用 `menu3.sh`＋`harness/zz_phase292_scoped_ab_test.go`（同一檔放進 old／new 兩棵樹跑），差異表 `m3-diff.txt`。
全部 Docker（`--rm`、`--network none`、`--cpus ≤ 4`、`--memory`、`--pids-limit`、目前 UID/GID、log rotation），容器名 `buck-phase292-*`；結束後無殘留容器、無 root 擁有檔。

下表「差異位置」是 old 與 new 畫面相異的 8×8 格（邏輯座標；2× 與 3× 相同）。除註明外，每案原版記憶體、indexed、palette 雜湊、停止點與 baseline old＝new。

| 項目 | 狀態 | 差異位置 | 收據 | 推論等級 |
|---|---|---|---|---|
| 001 主選單整頁重畫（bsave 接 Y、Down） | 新基準 | r16 c12–15（「離開至 DOS」的 `DOS` 半形） | `ab/e001-fm-y*`；`shots/crop-mainmenu-{2,3}x-old-new.png`、`shots/e2e-mainmenu-{2,3}x.png` | live：已證實；記憶體：見 §6 第 1 條 |
| 001 主選單 fm4（再 Down、Enter） | 新基準 | r16 c12–15 | `ab/e001-fm4*` | 同上 |
| 004 主選單 3× scoped（222 checkpoint Down／Up） | 零差 | none；三種模式（一般 2×、一般 3×、scoped 3×）active keys 與原版狀態 old＝new，scoped 封存 old／new 皆 ok | `m3/m222-*`、`m3-diff.txt` | 已證實 |
| 004 主選單 3× scoped（bsave 整頁重畫 fm-y、fm-4） | 新基準 | r16 c12–15；scoped 3× 封存（三字型 registry）通過 | `m3/fm-*`、`shots/crop-mainmenu-scoped3x-old-new.png` | 已證實 |
| 018 加入後選單（row20、row21 游標在「離開至 DOS」） | 零差 | none（第 21 列 `DOS` 在第一段已半形，old＝new） | `ab/e018-pj-row2[01]*` | 已證實 |
| 021 加入後離開提示 q1（「離開至 DOS」） | 新基準 | r24 c3–6 | `ab/e021-q1*`；`shots/crop-exitprompt-{2,3}x-old-new.png` | 已證實 |
| 021 N 返回、q2（無英數字） | 零差 | none | `ab/e021-n*`、`ab/e021-yy*` | 已證實 |
| 選單類：職業／一般技能頁欄名（內容空白改半格） | 新基準 | r4 c23–28（欄名三組間距由 1 格縮為半格，見 §6 第 2 條） | `ab/e001-career-subtract*`、`ab/e001-technical-base*`；`shots/crop-career-columns-2x-old-new.png` | 已證實 |
| 005 手冊首題停止點 266560000（段落尚未出現） | 零差 | none | `ab/e005-first*` | 已證實 |
| 005 手冊首題（段落顯示中） | 新基準 | r9 c8–37、r10 c2–37、r11 c2–28（段落以 72 單位重排）；僅 RGBA 雜湊，無圖片 | `ab/e005-first-b*` | 已證實 |
| 005 錯答後新題（段落無英數字） | 零差 | none | `ab/e005-wrong*` | 已證實 |
| 005 第三題 | 新基準 | r10 c2–37、r11 c2–33（重排）；僅雜湊 | `ab/e005-third*` | 已證實 |
| 034 英文列開啟（gba3 讀檔後問答） | 新基準 | r10–r11（段落重排）、r13 c7–34、r14 c2–12（英文列由兩列變一列，新版只佔 r13）；`英文列=on(35)` 不變；僅雜湊 | `ab/e034-on*` | 已證實 |
| 034 功能關閉（對照） | 新基準 | r10 c2–37、r11 c2–33（只有段落重排） | `ab/e034-off*` | 已證實 |
| 005 手冊 3× E1 | 未量到 | E1 程式未改（§5） | — | — |

### 4.1「離開至 DOS」各路徑歸屬

| 路徑 | 擁有者 | 本段後 `DOS` | 證據 |
|---|---|---|---|
| 功能主選單第 16 列（`function.menu.option.exit_to_dos`） | 選單家族（001；3× 可走 scoped 004） | 半形（本段改） | `e001-fm-y`、`fm-y scoped3` |
| 加入後選單第 21 列 | 第一段家族（dispatcher 或水平選單；加入後選單 catalog 只有第 13–16、18–20 列） | 半形（第一段已改，本段零差） | `e018-pj-row20/21` old＝new；未逐筆追蹤是哪一個家族，強推論 |
| 加入後離開提示第 24 列（021 q1） | 021 家族 | 半形（本段改） | `e021-q1` |

三條路徑在本段後一致為半形。

### 4.2 phase254 七條回歸（rerun31）

- `phase254-live-families-parity/runner` 先備份為 `runner-rerun30`（與原 `runner` 逐位元組相同，SHA-256 `97336565…`），再換成本輪 `runner-new`；新結果在 `rerun31/` 與 `rerun31-*.txt`。差異清單 `p254-diff.txt`（`p254diff.py`）。
- `rerun31/manual.sh` 與 rerun30 的差別：runner 要求輸出手冊 PNG，本輪在每次執行後立即刪除這兩張 PNG（手冊題畫面不保留圖片），RGBA 與文字結果不受影響。
- 七份文字（story、opening、manual、post、skill、action、body）與 rerun30 逐字相同。
- 504 份 RGBA 中 458 份逐位元組相同，46 份不同，全部在本段家族：

| 案例 | 差異位置 | 歸因 |
|---|---|---|
| m266560000（man、expect）、m266650000（live、man、expect），2×／3× | r9 c8–37、r10 c2–37、r11 c2–28 | 手冊段落 72 單位重排 |
| q1（ex、expect、live），2×／3× | r24 c3–6 | 021「離開至 DOS」半形 |
| career-add／down／drawn、tech-down／drawn（menu、expect、live），2×／3× | r4 c23–28 | 技能頁欄名內容空白半格 |

## 5. 規格矛盾：手冊 3× E1（已由主 repo `815499c` 更正，實作見 §9）

規格 039 §3.4 對 E1 寫「所有 U+0021–U+007E 字改用 12×24 半形字型……縱向位置沿用 `sealed.y+4`」。這與既有契約衝突，照條文做不出來：

- E1 每列的 parent stamp 是邏輯 8 像素高，3× 為實體 24 像素 `[sealed.y, sealed.y+24)`。規格 005 要求每個實體 glyph 完全落在 parent 內，`xlate.ValidatePixelGlyphPlan` 也照此拒絕（`g.Y+g.SrcH > py1`）。
- 12×24 字模放在 `sealed.y+4`，底緣是 `sealed.y+28`，一律超出 4 像素，整份 plan 會被拒絕。
- 即使改成只取墨跡範圍（規格沒有這樣寫），量測（Docker 內，本機兩份工作字型，只記數量）：倚天 12×24 半形墨跡在第 3–22 列，放在 +4 時有 9 個字模越界，其中 3 種是手冊 catalog 用到的字元；Unifont 墨跡在第 2–23 列，84 個越界，其中 57 種手冊用到。
- 規格 039 §2 的對齊證據（倚天半形 12×24 墨跡第 3–22 列與中文 22×22＋偏移 1 對齊）與 §3.3「3× 半形段 `GlyphY=0`」都對應 `sealed.y+0`，與 `+4` 互相矛盾。

因此 E1 的字型角色 `ascii-half`、三字型 seal／registry、plan 版本升版、`ValidateTokenPixels` 改半形字型都沒有動；E1 仍是 16×16 字首＋14 像素前進。請規格擁有者決定縱向位置（例如 `sealed.y+0`）後再實作。

## 6. 限度與觀察

1. bsave 重播點（`e001-fm-y`、`e001-fm4`）的原版記憶體雜湊 old≠new，但同一 runner 的 2× 與 3× 兩次也不相同（已用固定暫存層路徑）；indexed、palette、停止點與 baseline 相同。與第一段 `e028-fm4` 的觀察一致，判斷為此重播點本身的記憶體雜湊不可重現，與覆繪無關（強推論；覆繪層不寫模擬記憶體）。
2. 技能頁欄名「點數 加值 總計」的空白是內容空白，依 §3.1 改為半格，欄名間距縮小，欄名與下方數字欄的相對位置改變（見 `shots/crop-career-columns-2x-old-new.png`；舊版本來也沒有對齊數字欄）。這是規格的直接結果，但規格 §3.4 沒有提到這一列，請使用者確認。
3. 主選單 scoped 的正式建構子釘住字型 SHA-256 `150c93af…`，本機現行工作字型是 `0462ed06…`，正式建構子在本機（新舊版皆然）無法建立 scoped runtime；`text-receipt -scoped-menu-3x` 同樣無法執行。本輪 A/B 以套件內部建構子帶入現行字型的 SHA 執行（既有狀況，非本段造成）。
4. phase222 的 `workplace/cold-boot-live-turn-proto/menu3x_production_same_state_test.go` 有 `scoped2` 模式；本段後 scoped 只接受 3×，該測試的 `scoped2` 會失敗（它本來也因上一條的 SHA 不符而無法建立）。依邊界未修改該目錄，改以本目錄的探針重跑。
5. 列群組規則改變了 202 §2.3 的部分覆蓋語意（規格已載明）：選單與無 style 手冊的任一段、任一格失效時整列清除。本輪 A/B 各案 active keys old＝new，未觀察到因此多清的列。
6. 含 `•` 的怪物名遭遇：本機沒有可到達的 state，未量到（與第一段相同）。
7. 本輪 A/B 只用倚天工作字型；Unifont 3× 畫面未實跑。
8. 手冊與 034 的截圖一律不輸出；手冊段落保留英文專名，無法在不讀答案的前提下確認它們不含題目答案，所以只記 RGBA 雜湊與差異格。

## 7. 待決

1. ~~E1 縱向位置~~：已更正為 `sealed.y+0`，見 §9。
2. ~~技能頁欄名內容空白改半格~~：使用者定案接受。
3. phase254：rerun31 之後另有 rerun32（§9.5），請決定基準。
4. scoped 主選單的 SHA 釘選值與現行字型不符（§6 第 3 條），是否更新釘選值或改由 manifest 驗證。
5. 暫存：`dosgolem-clean/workplace/p292-old-src`（約 16M，`runner-old` 的原始碼樹）。請決定是否刪除。

## 8. 檔案

`go.sh`、`go-fork.sh`、`go-old.sh`、`sync.sh`、`changed-files.txt`、`run.sh`、`ab.sh`、`ab-inner.sh`、`jobs.sh`、`diff.py`、`crop.py`、`menu3.sh`、`m3diff.py`、`m3-diff.txt`、`p254.sh`、`p254-manual.sh`、`p254diff.py`、`p254-diff.txt`、`harness/`、`static.txt`、`test-all.txt`、`build-windows.txt`、`e1-private.txt`、`runner-old`、`runner-new`、`ab/`、`m3/`、`shots/`。

## 9. 手冊 3× E1（規格 039 §3.4；基底 dosgolem `1a51987`）

規格更正（主 repo `815499c`）：E1 半形字縱向位置為 `sealed.y+0`。本節在 fork 工作樹實作（未 commit），已同步 `dosgolem-clean`。

### 9.1 實作

| 檔案 | 內容 |
|---|---|
| `manual_e1_plan.go` | U+0021–U+007E（含半形括號與 `./+-%`）改用 12×24 半形字型、角色 `ascii-half`、每字前進 12、字詞寬 12×n、空白 12、`y = sealed.y`、crop 12×24；全形括號（ ）照舊以 22 點字模實際墨跡框前進；`BuildManualE1Plan`／`TextLayer` 多收半形字型並封存其指紋；registry 由兩個字型增為三個（底字型 16×16、22 點、半形 12×24）；hash 網域升為 `buckrogers-manual-e1-layout-v2`、LatinAdvance 欄改 12、雜湊加入半形字型名稱與指紋；`ValidateTokenPixels` 對半形字用半形字型墨跡 |
| `manual_overlay_runtime.go` | E1 呼叫帶入 presenter 的 3× 半形字型（由底字型以指標衍生） |
| `manual_snapshot_owner.go` | 2× 與 3× owner 都持有半形字型並記指紋；E1 驗證 registry 恰三個且指標相符、半形指紋等於 plan 封存值；封存 fonts 一律含半形字型 |
| 測試 | `manual_e1_plan_test.go`、`manual_e1_english_token_test.go`（12 像素前進）、`manual_snapshot_owner_test.go`（ASCII glyph 走半形字型、registry 3）、`halfwidth_part2_test.go` 新增 `TestHalfPart2E1HalfGlyphs`、`TestHalfPart2E1OwnerHalfSeal` |

`manual_snapshot_owner_original_oracle_test.go`（fork 未追蹤草稿）只用 `NewManualSnapshotOwner`，簽章未變，仍可編譯；它比對的 2× 歷史 RGBA 屬既有收據，本輪未執行。

### 9.2 字型檢查（Docker 內，只記數量）

| 字型 | 半形 12×24 字模 | 墨跡列 | 超出 24 像素列 | 39 題 E1 計畫 | `ValidatePixelGlyphPlan(3)` | 行首／行尾 soft separator |
|---|---|---|---|---|---|---|
| 倚天 `current-font` | 96 | 3–22 | 0 | 39／39 | 39／39 | 3／11 |
| Unifont `font-unifont` | 96 | 2–23 | 0 | 39／39 | 39／39 | 3／11 |

收據 `e1-probe.txt`（探針 `harness/zz_phase292_e1_probe_test.go`）。

### 9.3 測試

- `go test ./...`：29 套件 ok；兩個既有 cgo build failed（`test-all-e1.txt`）。
- Windows 交叉編譯通過（`build-windows-e1.txt`）；vet 通過（fork 含未追蹤草稿亦可編譯）；gofmt（本節改動檔）無差異。
- E1 單元測試：半形字位置、前進、字詞寬、空白 12、`y = sealed.y`、全形括號不變、registry 三字型、版本網域 v2、`ValidatePixelGlyphPlan` 通過；缺半形字型、尺寸錯誤、缺半形字模、同名異 bytes 半形字型皆拒絕；owner 三字型封存、半形指紋漂移拒絕、registry 缺半形字型拒絕。私有 39 題計畫與英文 token 測試通過。

### 9.4 E1 同狀態 A/B（3×；另附 2× 固定字格對照）

old＝`git archive 1a51987`，new＝本輪。`e1ab.sh` 以 `phase12-before-question.state`（phase96–104）重播，live runtime 收手冊事件，停止時把全部 presentation 事件交給 `ManualSnapshotOwner`（3× 走 E1）。按鍵只用錯答 `x` 與 Enter。只記 RGBA 雜湊與差異格（`e1-diff.txt`），不輸出圖片。三案原版 indexed、palette、停止點、事件數 old＝new。

| 項目 | 狀態 | 差異位置 | 收據 | 推論等級 |
|---|---|---|---|---|
| E1 首題（266650000） | 新基準 | r9 c8–37、r10 c4–5、r11 c4–14（英數字改 12×24、前進 12） | `e1/e1-first-*` | 已證實 |
| E1 錯答後新題（301240000，段落無英數字） | 零差 | none（registry 2→3，像素相同） | `e1/e1-wrong-*` | 已證實 |
| E1 第三題（304000000） | 新基準 | r10 c2–37、r11 c2–31（重排） | `e1/e1-third-*` | 已證實 |
| 2× 固定字格（三案） | 零差 | none（E1 改動不影響 2×） | 同上 | 已證實 |
| E1 成功返回（phase104 正確作答） | 未量到 | 需要答案輸入，依邊界不重播；只由 phase254 manual（固定字格）覆蓋 | — | — |

差異都在手冊清除矩形 `[7,312)×[72,184)` 內（第 9–22 列）。

### 9.5 phase254 rerun32

- `runner` 先備份為 `runner-rerun31`（與原檔逐位元組相同），換成本輪 `runner-new-e1`（SHA-256 `af7f7986…`）；新結果 `rerun32/`、`rerun32-*.txt`；腳本 `p254-e1.sh`、`p254diff-e1.py`、`p254-diff-e1.txt`。
- 七份文字與 rerun31 逐字相同；504 份 RGBA 全部逐位元組相同（runner 不走 E1）。手冊 PNG 仍於每次執行後立即刪除。

### 9.6 回報事項

- `cold-boot-live-turn-proto/menu3x_production_same_state_test.go` 的 `scoped2` 模式在 scoped 只接受 3× 後會失敗；依指示未修改。
- 暫存：`dosgolem-clean/workplace/p292e1-old-src`（old 原始碼樹）與 `p292-old-src`，請決定是否刪除。
