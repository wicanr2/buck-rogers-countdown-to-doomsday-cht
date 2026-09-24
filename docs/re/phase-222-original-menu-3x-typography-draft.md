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
