# 第二百二十二階段：原版主選單 3× 實體切換與中文字距 DRAFT

狀態：**DRAFT 原型證據**；不授權修改正式 dosgolem 字模繪製路徑。
範圍只限原版冷開機後功能主選單的六筆現有繁中覆繪，以及 Linux
Ebitengine 設定面板的 2×→3× 實體 Apply。這不是完整玩家入口、
手冊、存讀檔或所有文字路徑的驗收。

## 輸入與方法

- 原版 `START.EXE` SHA-256
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`，
  僅以 `/orig` 唯讀掛載；其他原版資料及已購字型留本機 ignored `workplace/`。
- `text/menu.zh-TW.tsv` SHA-256
  `16db36301675ef3c528ce6b37525463ab9e222305356fca9404d8242b91fa366`；
  `text/menu-text-safe-rects.tsv` SHA-256
  `a6cc54e8583fc288924edfc4f8923328ffe2b0d62441ff8b7a13c68c2777ff99`；
  本機倚天 `GOLEMFNT` SHA-256
  `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
- 工具：dosgolem fork `cbd5683`、Go 1.26.7、Ebitengine 2.9.9、
  容器內 Xvfb／xdotool／ImageMagick `import`；Docker 使用 `--rm`、
  無網路、原版與整體專案唯讀，僅 ignored 擷取目錄可寫。
- 可丟棄原型為 `workplace/cold-boot-live-turn-proto/scale3_original_physical_draft_test.go`
  （SHA-256 `7b9f794a7c1d073e5031fdbf7955acacea6429ee5529d6991461e6f69f4d7e39`）
  與 `menu3x_typography_draft_test.go`（SHA-256
  `1bcb5ab5b31f3460d54e49e92e67f8373a99a06eac77cc813e4ff348c82c6ba1`）。
  後者只在測試記憶體建立 22×22 字模，不修改正式程式或產物。

## 已證實的實體切換

從原版 EXE 冷開機到 `Machine.Steps=100000000` 的功能選單，正式
`frontend/ebiten.Game` 在真正 X11 視窗接受設定→暫選 3×→Apply。
Apply 當刻為 step `100000464`，面板開啟、暫選與收合的 Update
均為零 DOS 步；收合後繼續前進至 `100001216`，沒有重啟機器。
3× snapshot 成功 41 次，六筆功能選單繁中保持可見且零缺字；
設定面板使用已選 A 的倚天原生 24 點畫筆。兩張實體視窗圖留在
ignored `workplace/cold-boot-live-turn-proto/out/`：
`3x-original-menu-closed.png` SHA-256
`27b5927c29b136e4824e293d99b2007442ddf68f45eb0ed6fe8f8cd8df232a1b`，
`3x-original-menu-panel.png` SHA-256
`b309343a70818a4e7a3af7f58db3f513c023cba8a7826a81f9eb2ef020ed2b32`。
ImageMagick 的 X11 window 擷取為 920×654／920×679，與 960×600
的純 DOS 畫布 RGBA 不同；不能拿窗口圖尺寸冒充邏輯畫布幾何。
此原型沒有驗完整 memory／DOS state A/B，也沒有正式 session owner。

## 字距根因與可丟棄 A/B

正式 `BuildMenuOverlay` 在 3× 的每個 8×8 logical cell（輸出 24×24）
仍用 16×16 倚天字模、`GlyphX=GlyphY=4`；因此相鄰中文字的字模
外框間隔為 8 像素。這是程式碼與實際圖共同支持的**已證實**結論，
不是譯文插入空格：正式 TSV 的「將角色加入隊伍」等譯文沒有字間空白。

測試用 B 候選將同一 16×16 本機倚天字模以固定最近鄰規則衍生為
22×22，放在同一 24×24 cell 的 `GlyphX=GlyphY=1`；CJK 字模
外框間隔降為 2 像素，文字容量、draw anchor、原版色號及清除矩形
均不變。ASCII 保留原生 16 點字模並置中衍生畫布，避免把 `DOS`
或快捷字母擴成 CJK 寬墨。這只是**設計原型**，並非已核准的正式字型策略。

以同一原版 1 億步 indexed／palette、六筆 active exact 身分與正式 TSV
做 A（現行 16 點）／B（衍生 22 點）：兩版 RGBA 有 4,477 個不同
像素；B 對原始基底的差異在六個核准文字矩形外為 **0**，零缺字。
A／B RGBA SHA-256 分別為
`d2f6a13aae1ba412ba042b5be161a199f5ab80eb524f7ae733c313ca349797b8`／
`27b9c9b4eeb4d11b41c3e4672373933e89a7720306488d117085e7152f325e21`。
兩張 960×600 原生比例 PNG 僅留在 ignored `workplace/cold-boot-live-turn-proto/out/`：
`3x-menu-A-current16.png`、`3x-menu-B-derived22.png`。主代理目視確認
B 中文較大、字間更緊，仍須由獨立審查檢查所有正式 menu 變體的
容量、色彩、失效、2× 不變與原版同狀態，才可升限縮 READY。

獨立審查另以可丟棄的
`workplace/cold-boot-live-turn-proto/menu3x_typography_catalog_review_test.go`
（SHA-256 `02504327425d13c35ab975f5da2ad9089becb53f057dbf0fb11b54c131621655`）
覆蓋正式 `function.menu.*` 的九個變體，其中兩個為 selected；
主代理於 Go 1.26.7／Ebitengine 2.9.9 的唯讀 Docker／Xvfb 獨立重跑通過。
九筆均未超出安全矩形、未缺字，僅出現原版背景／前景色；四個
ASCII 字元格的像素與現行 16 點字模相同。這是合成幾何及色盤檢查，
**不是**九筆各自的原版同狀態收據，也未覆蓋其他選單路徑。正式
READY 尚需固定衍生字型契約，並驗 2× 不變及原版正常／selected
重繪、清除與返回。

PC-98／黃金盒的繁中版面研究只提供「字模尺寸、advance、行高分開量」
的方法；本案仍保留《拯救地球》DOS 的 320×200 邏輯畫布、原版
色彩角色與文字區，不複製其他遊戲畫面或把 PC-98 當行為 oracle。

## 原版 Down→Up normal／selected 補證（2026-09-24）

獨立子代理新增 ignored
`workplace/cold-boot-live-turn-proto/menu3x_lifecycle_original_draft_test.go`
（SHA-256 `742cfff3f4578358e7cc6d7af609c347cead5a15aaa31bf78b14d65d112d928a`）。
原版 checkpoint `after-bios-space-100m.state` SHA-256
`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`，
`START.EXE` 雜湊沿用上節；來源唯讀。於 step 100010000 送 BIOS Down，
停在 100060000；再送 BIOS Up，停在 100120000。正式 watcher 的
`transition.old.create`、`selected.add`、`normal.add`、`selected.create`
依序在 100025959、100042542、100080268、100096042 完成 guarded
post-call，顏色各為原版 0／10、15／0、0／10、15／0。兩個停點的
active keys 均與預期 normal／selected 轉移相符，無上一個選項的
舊 stamp。

主代理用同一 Go 1.26.7／Ebitengine 2.9.9 唯讀 Docker／Xvfb
獨立重播通過。兩個停點的 2× 候選與正式 16 點 RGBA 逐 byte 相同；
3× 現行 16 點與可丟棄 22 點候選分別改動 1,259／1,488 個像素，
核准作用中選單矩形外均為零。投影前後原版 step、indexed 與 palette
未變。這補上原版 normal／selected 的短路徑證據，**未**建立正式
長存 22 點 layer，也未驗它在真正視窗內反覆切換／存讀檔。

目前可送限縮 READY 審查的候選僅是功能主選單官方事件集；
`RuntimeMenuOverlay` 同時服務 race 等其他文字路徑，不能因這批
收據就把共用 constructor 的所有 3× 字型無條件換成 22 點。
若正式接線須改共用 builder，必須以精確 event／catalog 範圍隔離，
並保留其他路徑現行畫面，才不會將主選單證據外推。

## 限縮 READY 審查結論（2026-09-24）

獨立審查確認原版 Down→Up 已覆蓋 transition 的正常重繪；接下來
不需再延長這條原版逆向。正式事件全集是 21 個 identity：1 個
`menu.transition.*`、9 個 `function.menu.*`、11 個 `race.*`；先前
「13 筆」指譯文筆數，不能拿來當事件白名單。規格仍是 **DRAFT**，
最短 READY 補證如下：

1. 用完整鍵值的十鍵白名單限制主選單 3× 分支，對合成
   `menu.transition` 驗幾何及 2× 不變；對 `race.*`、post-join
   與偽前綴鍵做不變反例。不可用字串前綴擴大範圍。
2. 衍生 22 點字型須有穩定 `Name`、精確指標 registry、可核對的
   fingerprint，並通過快照／還原測試。現有原型的空 `Name` 不能
   直接進正式層。
3. 共用 builder 應保留原 16×16 基礎分支；22 點分支須在來源、
   輸出、樣式、倍率、文字安全矩形及混合批次方面完成失敗即關閉
   的預檢測試。

以上是規格與合成測試的缺口，不是再去猜原版行為；正式長存 layer、
同狀態及視窗反覆切換則屬 READY 後的 CONFORMED 驗收。

## 十鍵範圍與字型身分合成補證（2026-09-24）

子代理新增 ignored
`workplace/cold-boot-live-turn-proto/menu3x_scoped_routing_draft_test.go`
（SHA-256 `a3f44a444309994d0d09dd970b102bdf2eadf3007e91843f4b3ddee9a66a27e5`）。
測試讀取正式 `menu-events.tsv`（SHA-256
`fddbd09ae363e986a2879013e384cdfef717f46fa47786bbad0cb96ae67bfcfc`）、
`menu.zh-TW.tsv`（`16db36301675ef3c528ce6b37525463ab9e222305356fca9404d8242b91fa366`）
及 `menu-text-safe-rects.tsv`（`a6cc54e8583fc288924edfc4f8923328ffe2b0d62441ff8b7a13c68c2777ff99`）。
主代理逐行檢視後，以 Go 1.26.7／Ebitengine 2.9.9 的唯讀、無網路
Docker／Xvfb 獨立重跑兩項定向測試通過。

原型只對十個**完整相等**鍵把 3× 的正式 16 點 stamp 換成測試用
22 點字型；正式 21 個事件的 2× 畫面逐 byte 相同、11 個 race
事件的 3× 亦相同。合成 `menu.transition` 的 3× 差異限安全矩形；
`post_join.menu.synthetic` 與兩個偽前綴鍵維持原畫面。這證明白名單
候選可限縮，**沒有**讓 production `RuntimeMenuOverlay.Apply` 實際
採用該分流。

第二項測試為測試用字型賦予 `draft.menu.derived-22` 名稱，得到
`FontFingerprint=b2413c6f69eec76e5206729445e2d485dbe2b67424b6c1aef63a2050cc7b18d5`；
同名同指標 registry 的封存與 snapshot／restore RGBA 同值，而空名、
缺 registry、key/name 不符及同名不同指標在相應測試路徑被拒絕；
其中**同名不同指標只由 `WithSealedOrderedLayers` 封存閘門拒絕**，
普通 `xlate.Layer.Restore` 僅按 `Font.Name` 查 registry，不驗指標
或 fingerprint。此名稱與字模
**只是原型身分**，正式 `manualThreeXFont` 仍可能產出空名；
`BuildMenuOverlay` 仍只接受 16×16，故共用 builder、正式字型身分與
接線尚待 READY 審查。不得把本合成 PASS 稱為正式 3× 字距已修復。

## 共用 builder 的失敗矩陣與新發現（2026-09-24）

子代理另以 ignored
`workplace/cold-boot-live-turn-proto/menu3x_builder_failure_matrix_draft_test.go`
（SHA-256 `5cdf949c1d9233f8f8591bbf638589ca7f7c678a30fec7a8190e22b6bef1db4d`）
建立測試用 22 點 builder。主代理逐行審閱，並在同版唯讀 Docker／Xvfb
把本檔三測試與上一節兩測試獨立重跑，全部通過。現有正式 16 點
builder 的 2×／3× 配色、偏移及混合 race 批次不變；nil、零倍率、
22 點直接輸入、後筆樣式／容量／幾何／缺字／重疊均整批回 nil 與錯誤。
測試用 22 點分支的兩種選取／指示列在 3× 均留在核准矩形，保留
原 BG／FG；來源、輸出、倍率、樣式、矩形與混合 race／post-join
共 19 種壞案均拒絕。

新發現的真實程式邊界是：現有 `BuildMenuOverlay` 只驗本次譯文
引用的字模，也接受一般正整數的 4×；但整套 16→22 字型衍生器
會讀**所有**來源字模。以一個未引用、長度不符的字模餵入時，
正式 16 點 builder 可成功，未預檢衍生器卻會 panic。此反例要求
22 點分支在衍生之前先核對來源全部字模，並明定只允許 3×、
精確十鍵、完整批次原子拒絕；不能為了新字距全域放寬共用 builder。
目前所有 22 點 builder 與字型名稱仍只在 ignored 測試，正式規格
保持 DRAFT，尚未取得 production 接線授權。

## 限縮 READY 正式接線與原版同狀態收據（2026-09-24）

本機 ignored dosgolem 分支 `buck-rogers-cht-output-overlay` 的
`3b02f88` 已新增明示的十鍵 `BuildScopedThreeXMenuOverlay`、
`NewScopedMenuRuntimeOverlay` 及預設關閉的文字收據 CLI 旗標；
既有 16 點 API 不變。正式來源 `GOLEMFNT` SHA-256
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`，
衍生 22 點 `FontFingerprint`
`757d5128ca2b86419e6d69b149b259f9c17b1caccc01fdefa8a7ca414f8fba20`。
主代理逐行審閱四個正式檔，於唯讀、無網路 Docker 重跑
`apps/buckrogers` 與文字收據 CLI 套件的完整測試及 `go vet` 通過。
正式 21 個事件的 2×／3× 分流、十鍵白名單、11 個 race 不變、
偽造 request、壞字模、錯倍率、混合批次及同 session 封存還原均有
定向測試；這些是程式契約，非原版同狀態的替代品。

ignored 驗收測試
`workplace/cold-boot-live-turn-proto/menu3x_production_same_state_test.go`
SHA-256 `eabaab5367bfbd30c182c957e609d5c1e2aeb3f4372bbadf3194219e5e5e1790`，
直接使用正式舊／新 runtime，從同一原版 checkpoint
`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`
重播 Down→Up。原版 `START.EXE` SHA-256
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`。
主代理在 Go 1.26.7／Ebitengine 2.9.9 的唯讀 Docker／Xvfb 獨立重跑
`TestProductionMenuThreeXOriginalSameState` 通過：四模式 old2／scoped2／
old3／scoped3 在 Down step `100060000`、Up step `100120000` 的原版
step、frame、indexed、palette 一致；scoped2 與 old2 RGBA 逐 byte
相同。old3→scoped3 的差異分別為 1,259／1,488 像素，作用中
核准安全矩形外為零；scoped3 相對原版 raw control，矩形外亦為零。
停點前正式作用層仍為 pending，測試先斷言 `Draw` 不交付，再以
正式 `RuntimeMenuOverlay.Frame` 錨定後確認 `Draw` 成功；原版
machine 狀態未被該投影改動。

文字收據 CLI 的 control JSON 另存 ignored `out/menu3x-down-control.json`
（SHA-256 `cac87a5f71db29ac63258e8a7734e5a89f95edebdfbfd3250d0b2e14d275f530`）
及 `out/menu3x-up-control.json`
（`46ac2ad99c1f5932bef9633dbf73810b2debfab214b41a2a0fc80c86c339cebb`），
其 indexed／palette hash 與測試相同。但舊 3× 與新
`-scoped-menu-3x` CLI 在 Down 停點都因終態未錨定影格而回
`drew=false active=3`，**沒有成功的 CLI 覆繪 JSON／RGBA 收據**。
這是共用 CLI 終態投影缺口，不可寫成新字型同狀態已由 CLI 驗收。
真正 Ebitengine 視窗 2×→3×→2×、正常玩家入口、整體 session
原子輸入及存讀檔仍未驗；十鍵子契約維持 READY，不升 CONFORMED。

## CLI 終態錨定與部分檔案反例（2026-09-24）

ignored 原型
`workplace/cold-boot-live-turn-proto/menu3x_terminal_anchor_draft_test.go`
SHA-256 `b95271c0c903a19fa2b8374e169a11059ec51f3ebfb4b5ea4a8245d7564d3cab`。
主代理逐行審閱，於同一原版 EXE／checkpoint、唯讀 Docker／Xvfb
獨立重跑 `TestDraftMenuThreeXTerminalAnchorOriginal` 的舊／新 3×
兩組通過。Down 停點 step `100060000` 只有一個原版 frame；兩組
active 皆為三筆 `Pending`，所以現行 CLI 不先呼叫 `Frame` 就
`Draw`，兩組同樣 `drew=false active=3`。原型在 stop 當刻使用同一
indexed／palette，至多補一次正式 runtime `Frame` 後繪製；
重複取樣不再錨定、清層無 active 只回 raw control、正常 frame
已處理者不再補錨、偽造 request 失敗後不交付。前後原版 step、
frame、記憶體、indexed 與 palette 均相同。這是**可丟棄的終態
呈現投影**，不是新增的原版畫格或正式 CLI 已通過。

另核對正式 CLI `cmd/buckrogers-text-receipt/main.go`：目前先寫
`baseline-rgba-out`，其後才 `Draw` 並執行
`validateOverlayDraw`。前述失敗實際留下部分 RGBA 檔，已對精確
確認的測試輸出個別清除；未觸碰原版或其他收據。正式修正至少須
先在記憶體完成錨定、繪製與驗證，再提交輸出，並處理後續 I/O
失敗避免留下看似完整的單邊收據。

收據語意仍待選：在指定停止步數明示標註「同狀態呈現投影」；或
只接受下一個真正 `OnFrame`，但此時原版狀態及停止步數已改；
亦可暫維持 CLI 在 `Pending` 停點失敗。上述三者不得混稱同一種
原版收據。此處只記錄證據與候選，未改正式 CLI 或規格狀態。

## 正式 scoped runtime 的實體視窗回切（2026-09-24）

ignored 測試
`workplace/cold-boot-live-turn-proto/menu3x_scoped_physical_acceptance_test.go`
SHA-256 `2edac5caadb4e7388cd3cb790b0d74e22a8bbc0168e717002dd04d4b681813af`。
它從同一原版 checkpoint 經 Down→Up 到 step `100120000`，
直接建立正式 `NewScopedMenuRuntimeOverlay` 的 2×／3× 作用層，
把兩者的正式 `Draw` 接到 `frontend/ebiten.Game.Config.Snapshot`；
使用真正 Xvfb／xdotool 視窗點開設定、Apply 3×、再 Apply 2×。
這是**既定原版選單狀態的限縮視窗驗收**：測試預先將已觀測的
三個 exact 事件送入 3× 作用層，並非 #18 的完整直播 session。

子代理初跑與主代理在唯讀、無網路、有界 Docker／Xvfb 獨立重跑
均通過。主代理收據：首次／第二次 Apply 於 step `100120400`／
`100120688`；面板開啟或收合的 85 個回合均零 DOS 步，閉合的
62 回合各推進固定 16 步。2×／3× snapshot 分別 69／23 張，
零缺字；前後原版 indexed／palette 不變，回到 2× 的 RGBA
逐 byte 等於切換前，SHA-256
`cd73ad5ee152765893dcd952d4c4b879841004f10392f64d3b9e17649d1f2436`。
3× 相對同狀態 raw control 改動 4,980 像素，作用中核准文字
安全矩形外為零。子代理另留兩張實體視窗 PNG 於 ignored `out/`，
不入 Git。不同重播的停留回合與 Apply 步數會隨實際點擊時序變動；
固定驗收是面板回合零步、兩次 Apply 生效、前後畫面約束，而非
這組偶然的步數常數。

此收據補齊十鍵主選單字距的限縮實體回切，但 CLI 正式收據仍
無終態錨定、#18 正式輸入原子性、正常玩家入口與存讀檔仍未知；
規格 004 十鍵子契約維持 READY，不升整體 CONFORMED。

## 2026-09-24 CLI 驗證失敗半份收據的限縮修正

本機 ignored dosgolem 分支 `18575d2` 將選單、加入角色選單、技能離頁
及 Exit 問句四條 CLI 覆繪路徑的基準 RGBA 寫入移到 `Draw` 與
`validateOverlayDraw` 成功之後；這是收據工具的輸出順序修正，
**不**改終態 `Pending`／`OnFrame` 語意或原版執行。

主代理於 Go 1.26.7 的唯讀、無網路、有界 Docker 執行
`go test -count=1 ./cmd/buckrogers-text-receipt` 與同套件 `go vet`，
均通過。再由已驗 `after-bios-space-100m.state` 從相同步數排入 Down，
於 `100060000` 跑正式 scoped 3× CLI：仍按既有契約以
`drew=false active=3` 失敗，但容器暫存區的 baseline 與 overlay
兩檔均不存在；原版輸入唯讀。用同一 state 於 `100000000` 跑
2× 有效停點，CLI 成功且兩檔與 JSON 均非空。

這只證明繪製／驗證錯誤不再先留下 baseline；若第一個輸出檔已寫入、
第二個輸出檔的 I/O 才失敗，仍可能有單邊檔。完整多檔提交策略及
終態 A／B／C 收據語意尚未決定，不能宣稱 CLI 已取得 3× 覆繪收據。

## 2026-09-24 多檔收據的程序內回復與原版重跑

上述 `18575d2` 只修「繪製驗證前先寫 baseline」；後續本機
dosgolem fork `a18e86a`、`c08263b` 把 CLI 各輸出先驗證並暫存，
以同目錄 rename 發布。若後續檔案發布或 stdout 寫入於程序內
回錯，回復既有目標 bytes 並撤銷新增檔；重複實體目標路徑
（包含父目錄 symlink 別名）、目標 symlink 與目錄混型均拒絕。
主代理在 `eob-remake-go:1.26.7-ebiten2.9.9`、無網路、唯讀 fork
的有界 Docker 獨立重跑 CLI package 單元、競態測試及 `go vet`
通過；失敗注入涵蓋第二／第三檔 rename、跨輸出目錄及 stdout。

再以既有 ignored `workplace/command_status_roster_ab_probe.sh`，
唯讀掛載原版與字型，重跑合法 `roster.loading` 入頁
`308000000`／自然清層 `309000000` 的 control／2×／3×。
兩倍率四組原版事件、BIOS 鍵、memory／indexed／palette 與
machine／DOS digest 同於 control；安全矩形外差異皆零，
入頁內 2×／3× 分別 1,272／2,669 像素，清層後皆零。
四份 JSON 收據 SHA-256 依序仍為
`8f23387a9788aa9eef824888ca94b6db56ea865ce155b696af568e46d731efcb`、
`7d4f55c4b8379961c9fb2e958111e94c22005a8e82bff07e57333f9662753eb8`、
`1945d41e5f0d905009683fc01674cf739191b92bcc07e54d2dc0819d95b6e357`、
`f9e860381675ad09773015fb73bcddb103b6494b0822e890132ff252f2bd7ba3`。
Go 在唯讀模組快取嘗試寫 stat cache 曾發出非致命警告；全部
比較通過，非產品失敗。

這是**程序內錯誤回復**，非跨檔案系統交易；程序被殺或斷電
仍可能留下部分新檔，rollback 自身遇 I/O 錯誤時會回報並保留
可復原備份。停止格尚未經原版 `OnFrame` 的 `Pending` 仍依舊
失敗；是否允許明示的同狀態投影，仍待使用者決定。
