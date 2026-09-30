# 040 — 多語框架與 F4 語言切換

狀態：**READY**（2026-09-30，三輪獨立審查；第三輪應改已併入）
日期：2026-09-30
Issue：#35
前置：規格 039（半形英數字）、036／037／038（名字）、005／034（手冊）、030（手札）、027–029、010–017、022、
dosgolem 241（前端輸入）。後續：041 簡體、042 日文、043 韓文、044／045 日韓音譯器（各自另訂）。
證據：[phase-295](../re/phase-295-multilang-inventory.md)（多語盤點，行號以 dosgolem `94825fb` 為準）；
原版 F4 用途量測 [phase-294](../re/phase-294-f4-usage.md)（已完成）。

## 1. 為什麼要做

使用者決定（2026-09-29、09-30）：
- 前端 F4 循環切換 繁體 → 簡體 → 英文 → 日文 → 韓文 → 繁體；英文＝關閉覆繪、顯示原版。
- 簡體用 OpenCC 詞彙級轉換；日韓以英文原文為源、繁中為語境參考批次翻譯；日韓手冊題段落從繁中段落轉譯。
- 缺譯顯示原版英文；語言記住上次選擇、首次為繁體、`-lang` 參數可覆寫；一個發行包帶全部語言。
- 日韓模式的名字格式同中文「譯名(英文)」。

本規格只定義框架（第一期）。本期可用語言只有 `zh-TW` 與 `en`；另以一個**測試專用假語言**驗證多語結構（§5）。

## 2. 證據

- 覆繪是純觀察（已證實，phase-295 §0）：LiveRuntime 只讀原版記憶體，覆繪在輸出合成時疊加。
- Catalog 檔名在 Go 與 Python 端寫死 `.zh-TW.tsv`；`post_join_menu` 把譯文 SHA-256 釘成常數（已證實）。
以下三條為兩輪審查讀程式核對（已證實，dosgolem `9e55973`），phase-295 中與之衝突的段落已由本規格取代：
- A 類家族的 catalog 在載入時要求 key 完全吻合（`menu.go:129-139`、`manual.go:296-306`、`skill_exit.go:59-70`、
  `action_bar.go:89`、`post_join_menu.go:94`）；watcher 的判斷本身不依賴譯文，依賴譯文的只有讓位矩形、presenter
  失敗連帶 watcher 故障、手冊收據的 `translation_runes`、手札面板開啟判斷。B 類查無譯文時照原版。
- 疊字狀態：Pending 要經一次 `Frame` 才顯示，Shown 要連續指紋不符才失效，列群組在 `Frame` 內（`xlate/layer.go:409-432`、
  `menu_overlay_runtime.go:195-197`）；合成前的 `sync*` 失敗會改變 watcher 狀態（`live_runtime.go:1086-1089`）。
- 執行期錯誤：選單 Apply 失敗使共用 recorder 故障（`live_menu.go:204-212`）；部分家族出錯時同時重建共用 watcher 並
  提早 return（`live_runtime.go:909-916, 969-971`）；合成時任一層缺字即整格回錯（`live_runtime.go:1100-1107`）。
- 字型（已證實，phase-295 §3）：Unifont 17.0.05 完整涵蓋平假名、片假名、諺文、GB2312、JIS X 0208；日文字形在
  `unifont_jp`；倚天缺諺文與上千簡體、日文漢字。
- 原版是否使用 F4（phase-294）：主選單、讀檔後與 Hq 隊伍選單、站內選單、3D 探索、廢棄飛船敘事與提示、Yes／No 提示、
  戰鬥行動選單與移動模式、角色頁、命名輸入共 14 個畫面，沒有任何指令以 3Eh 比較；F4 與 F5 結果逐位元組相同（只差堆疊內
  原始鍵值），角色頁的底列重建與站內的時序差屬「不認得的延伸鍵」共用分支（已證實，限量到的路徑）。正對照：F10 在戰鬥
  移動模式有專屬分支，方法看得出單鍵反應。未量：商店、酒吧、診所、港口、訓練、太空航行與戰鬥、探索子選單、存讀檔選單、
  標題與結束畫面、手冊題（強推論相同，依共用讀鍵層）。

## 3. 契約

### 3.1 語言代碼與檔案

- 語言代碼：`zh-TW`、`zh-CN`、`en`、`ja`、`ko`；測試另用 `zz`（只存在測試資料，不出現在發行包與 F4 循環）。
- 共用檔（與語言無關）：events、安全矩形、layout、callers、`header-columns.tsv` 結構、名字與音譯的原文側資料。
  共用檔出錯維持啟動失敗。
- 語言檔：`text/<family>.<lang>.tsv`，key 集合是共用 events 的子集（可缺列）。
- 所有寫死 `.zh-TW.tsv` 的 Go 與 Python 載入、驗證、合併、字型工具改為接受語言參數；預設 `zh-TW`，行為與收據不變。
- A 類家族拆成「共用身分」與「每語言譯文」：watcher 只輸出 TextKey（與原文身分），由各語言的 presenter 查該語言
  譯文。zh-TW 載入時仍要求 key 完全吻合（維持現行）；其他語言允許缺列。
- 劇情第 9 頁的譯文雜湊釘選同樣只對 zh-TW（實作回寫，2026-09-30）。
- `post_join_menu`：zh-TW 保留現行常數雜湊釘選；其他語言不釘雜湊，允許 0 列或恰好 7 列（逐列先建驗證），
  0 列時整組顯示原版英文，不讓語言失效。
- 動作列：每語言的 normal 配色由譯文推導——每則譯文須含恰好一個半形括號熱鍵 `(X)`，且字母等於 zh-TW 同 key 譯文的字母；
  熱鍵字母用 events 的首色（`normal_first_fg`），其餘用 `normal_rest_fg`；不符者該語言該則缺譯。focus 配色維持單色。
  zh-TW 推導結果須與現行固定配色逐字相同（已核對 5 則皆為 {10,10,10,15,10}）；實作移除「長度 5」的釘選。
- 手冊收據的 `translation_runes` 改由 zh-TW catalog 依 TextKey 補上，收據 JSON 不變；手冊 presenter 以 TextKey 查譯文，
  不再比對請求所帶譯文。
- 每語言專用的名字資料（036 譯名、037 允許字集等）由後續語言規格定義；本期保證載入介面接受語言參數，
  `NameGlossary` 與 `PlayerNames` 為每語言一份。

### 3.2 語言通道（lane）

- 一個觀測分派服務所有已啟用語言。共用、不分語言的狀態：overlay 正規化（OverlayUnits）、原版字形表搜尋、
  隊伍快照、劇情進行中的呼叫與前一指令、手冊題進行中狀態、選單共用 recorder、動作列與身體圖示的 watcher、
  手札鍵盤緩衝狀態、`header-columns` 名單資料（逐語言驗證）。
- 每語言一份：presenter（每語言 × 每倍率）、B 類 watcher、NameGlossary、PlayerNames、字型與其半形衍生字型、
  reset 與統計計數。每倍率一個 owner 且內含 watcher 的家族（技能離開、加入後提示、劇情第 9 頁），可改為每語言
  一組 owner。
- **每格同步**（單一規則）：LiveRuntime 現在對「每倍率 presenter／owner」做的每一個呼叫，都改為對每個已啟用語言
  各做一次；包括 Apply、Frame、Prewrite、ClearTextCells、ClearRect／Clear、ObserveAnchorEvent、SetStyle、手冊 bridge
  Sync、owner 的 ObserveEntry／ObserveReturn、`obs.Dropped` 觸發的 owner 重建、劇情協定（glyphEntry、verifiedReturn、
  discontinuity、clearWrite、待套用 apply 與 clear）、B 類 watcher 的 hook 事件與 presenter Sync。
- B 類 sync（`syncEclText`、`syncHMenu`、`syncEngineDispatch`、`syncLogbook`）維持現行兩個時點：每個 retrace，以及
  `ComposeWith` 之前（收據工具在任意步數輸出需要它，phase-259）。兩個時點都對**所有**已啟用語言一起執行；合成只讀
  當前語言。所有語言在相同時點同步，因此切換只改合成時使用的語言索引，不重建、不清空、不追趕，zh-TW 收據不變。
- B 類 sync 遇缺字：只對該語言自己的 watcher 呼叫 `ObserveDiscontinuity` 並清該語言的 presenter（兩個時點同一路徑）。
- 畫圖階段某層缺字：略過該層並計數，不回錯、不改任何語言的狀態；選單家族是底圖，缺字時改用 `ScaleIndexedRGBA`
  當底圖。
- 讓位（`yieldMenu` 等）逐語言計算：每個語言用自己 presenter 的矩形清自己的層；該語言缺譯而沒有疊字時，改用該事件
  的原文格範圍讓位：body-icon 用 `body-icon-text-safe-rects.tsv`；加入後提示與加入後選單由 TextEvent 的 `Row`、`Column`、
  `OriginalLength` 推出原文格範圍；技能離開用第 24 列的清除帶。
- 缺譯粒度（該語言該筆顯示原版英文）：選單類逐列；加入後選單 7 項為一組（缺任一項整組不畫）；劇情頁以頁為單位
  （缺任一行整頁不畫）；手冊以段落為單位；身體圖示、技能離開、動作列以各自的請求為單位。缺譯時該語言的 presenter
  仍要清掉自己原本的矩形，不留前一筆的疊字。
- 不在本期 lane 範圍：主選單 3× scoped 路徑（只在收據工具使用，綁倚天字型雜湊，屬 zh-TW 收據）、手冊 E1
  snapshot owner（未接進 LiveRuntime）、規格 034 英文摘錄面板（只在 zh-TW 顯示）。

### 3.3 錯誤隔離

- 載入驗證（每語言 × 每倍率）：把該語言每一列譯文先建一次 presenter 內容，檢查容量、缺字、墨跡、半形字型衍生
  （`halfFontsOf(font).Err`）與欄名列錨定。欄名列在某語言缺譯或放不下時，該語言該列退回一般排版，不讓語言失效。
- 某語言的語言檔驗證失敗：該語言從 F4 循環移除；zh-TW 失敗維持啟動失敗。
- 執行期某語言某家族出錯：沿用現行「清空並重建該語言該家族的 presenter／owner，並計數」，不碰共用 watcher 與 recorder，
  不提早 return，其他家族與其他語言照常；`obs.Dropped` 的重建屬正常生命週期，不計錯誤。共用 recorder 本身的錯誤維持致命。
  實作需把選單 presenter 移出 `LiveMenuRuntime`（其失敗不再觸發共用 recorder 故障），並拆分「重建共用 watcher」與
  「重建單一語言」；`syncManual` 逐語言處理，一個語言失敗不跳過其他語言。
- 缺譯走「清空且不回錯」的路徑（手冊 consumer 不因缺譯卡住重試）。非作用中的語言出錯不影響作用中語言的合成。
- 錯誤紀錄寫到 stderr 與 DebugSummary（逐語言、逐家族計數）。

### 3.4 F4、英文模式與設定

- F4 加入前端保留鍵（規格 241 §3.3 同步修改），每按一次切到下一個已啟用語言；互動模式按 F4 只產生前端動作、
  不送 BIOS 鍵。自動模式腳本新增 `lang` 動作（腳本內的鍵名 `F4` 仍直接送 BIOS，驗收用 `lang`）。
- 已啟用語言：`en` 恆啟用；其他語言在其全部 A 類語言檔存在並通過 §3.3 載入驗證、且字型存在時啟用。
- F4 改前端保留的前提（phase-294 判定條件）：量主選單、Hq 隊伍選單、探索、文字窗、水平選單提示、戰鬥、角色頁、
  命名輸入；判準為 int 16h 回傳 3E00h 後原版是否進入比對分支或狀態改變；F4–F10 同輪量；沒量到的畫面標未知。
  列出的畫面全部量到且都不使用 F4 才採用；任一畫面用到或標為未知，本節改選他鍵或補量後回到審查。
  phase-294 已量完列出的畫面且都不使用 F4：採用 F4。未列出的畫面若日後量到 F4 專屬行為，回到本節。
- 英文模式：合成與截圖輸出逐位元組等於原版 `ScaleIndexedRGBA`（說明頁開啟時不在比對範圍）；手札面板不顯示。
- 手札翻頁：PgUp／PgDn 是否由前端吃掉，由**目前語言**的手札面板是否開啟決定；`Turn` 對所有語言各自在其頁數內夾住後
  翻頁；目前語言沒吃掉 PgUp／PgDn 時，任何語言的 `Turn` 都不執行。因此語言影響原版輸入的例外是：目前語言的手札面板未開啟時（英文模式，或該語言缺該則手札、面板缺字關閉），
  PgUp／PgDn 送進原版。驗收腳本避開這兩鍵，翻頁只以單元測試驗證。
- 設定檔：使用者資料目錄下 `settings.json`，只存 `{"lang": "<代碼>"}`；讀寫失敗不致命。優先序：`-lang` ＞ 設定檔 ＞
  `zh-TW`。`-lang` 給不認得的代碼視為用法錯誤、結束；`-lang` 或設定檔給出已知但未啟用的代碼時退為 `zh-TW` 並記錯誤。
  說明頁列出未啟用的語言與原因摘要（互動模式下 stderr 使用者看不到）。
  自動模式（`-frames>0`）與開發模式（`-save`）不讀也不寫設定檔。
- 字型檔名：`font/buckrogers-<lang>.golemfnt`；本機完整版的 zh-TW 另可用 `font/buckrogers-eten-top-pad.golemfnt`
  （存在時優先，維持現行）。`-font` 只覆寫 zh-TW。
- 說明頁與視窗標題用 zh-TW 字型與文字；說明頁新增顯示目前語言的樣板列；視窗標題改為不標語言的「拯救地球」，
  目前語言顯示在說明頁。`docs/release/讀我.txt` 同步。

## 3.5 實作狀態（2026-09-30）

- 第一段（LiveRuntime 通道）：dosgolem `d685efd`，收據 phase-296。phase254 rerun34 與 rerun33 逐位元組相同；四時點切換正確；
  每多一條語言通道每格約多 0.87 ms（收據工具量測，前端未量）。第二段（前端 F4、設定檔、英文模式 UI、說明頁）待做。
- 非 zh-TW 的 Python 驗證器仍沿用完全吻合檢查（只改檔名），允許缺列與字集白名單留給 041–045。

## 4. 不做什麼

- 簡體、日文、韓文的譯文、斷行規則、名字與音譯（041–045）。
- 語言除 §3.4 手札翻頁例外外，不影響遊戲狀態或存檔。

## 5. 驗收

1. 單元測試：
   - 檔名參數化（zh-TW 預設不變）；A 類 watcher 只輸出 TextKey、presenter 依語言查譯文；缺譯粒度與清矩形。
   - 每格同步：非作用中語言收到全部事件；切換後第一格畫面等於「一開始就用該語言」。
   - 錯誤隔離：某語言載入失敗移出循環；執行期某語言某家族出錯只停用自己；非作用中語言出錯不影響合成。
   - `mapKeys`：互動按 F4 只產生語言動作、不產生 BIOS 鍵；`lang` 腳本動作。
   - 英文模式合成等於原版；`LogbookTurn` 英文模式回 false；`Turn` 多語夾住。
   - 設定檔優先序、未知 `-lang` 為用法錯誤、自動與開發模式不讀寫設定檔。
   - post_join：zh-TW 雜湊釘選不變；其他語言 0 或 7 列。動作列配色推導（zh-TW 與現行逐字相同）。
   - 畫圖缺字只略過該層（選單改用原版底圖）；缺譯的讓位矩形（四家族）；retrace 與合成前 sync 都對所有語言執行，
     各語言狀態不因合成時點而分岔；B 類 sync 缺字只影響該語言。
2. 回歸：只有 `zh-TW` 與 `en` 時，phase254 七條回歸（基準 rerun33）與既有各家族收據逐位元組不變。
3. 切換正確性：`buckrogers-text-receipt` 新增 `-lang`、`-lang-switch <步數>:<代碼>[,…]`、`-compose-every-retrace`
   （每個 retrace 都對目前語言合成，貼近前端）與測試專用的 `-test-lang-dir`／`-test-lang-font`（載入 zz；前端不提供）。
   zz 滿足所有 A 類載入契約（技能離開兩列非空、加入後選單 7 列、動作列每則一個 `(X)`、劇情第 9 頁單列、手冊 504 格
   與 14 列；手冊段落用合成填充字，不由 zh-TW 手冊段落改寫），譯文長度與 zh-TW 不同，字模都在 zh-TW 字型內，只存在測試資料。以 zz、zh-TW、en 在四個時點切換：
   ECL 敘事窗與水平選單（`workplace/phase258-ecl-ab/g2.state` 與其腳本按鍵）、手札面板開啟
   （`workplace/checkpoints/logbook41-pre.state`）、手冊題進行中（`workplace/probe/phase12-before-question.state`）；
   停止步數沿用各 state 既有腳本並記入收據。每個時點的畫面與「一開始就用該語言」的同格畫面逐位元組相同。
4. 原版不受影響：前端與收據工具輸出 `StateDigest` 的記憶體與 CPU 雜湊（收據新增 CPU 雜湊欄）；同腳本插入多次 `lang` 與不插入，雜湊相同
   （英文模式手札翻頁例外不在腳本中出現）。
5. 效能：`-cpuprofile` 加 `-frames N`，固定腳本、`-clock 50`，量 1 語言與 2 語言（zh-TW＋zz）每格 CPU 與啟動時間，
   分開記每語言每格 Frame 成本與 B 類呼叫期間成本，估 4 語言。
6. 前端：自動模式觸發一次 `lang` 並截圖確認切換、英文模式與說明頁目前語言。
