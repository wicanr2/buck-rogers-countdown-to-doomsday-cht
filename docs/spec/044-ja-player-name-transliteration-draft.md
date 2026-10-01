# 044 — 日文玩家名音譯（片假名）與日韓共同前端

狀態：**DRAFT**（2026-10-01；兩輪獨立審查已併入第三版）
日期：2026-10-01
Issue：#35
前置：規格 037（中文音譯器，同型做法）、038（玩家名判定與顯示）、040（多語框架）、042（日文）、036（譯名表）、039（半形單位）、046（串接）。
後續：045 韓文玩家名音譯（共用本規格 §3.1 至 §3.3、§3.5 至 §3.8、§5 的做法）。

## 1. 為什麼要做

使用者決定（2026-09-29）：日文模式的玩家名用片假名音譯，格式同中文「譯名(英文)」，窄欄只顯示譯名。規格 042 §3.8、043 §3.8 讓 `PlayerNames` 在 ja、ko 停用（`playersOff=no-transliterator`），玩家名維持英文，語言本身不失效。
本規格補上日文音譯器與接線，並把日文、韓文共用的「英文名到音節」前端定義一次。

## 2. 證據（已證實，除非標明）

- 接線點很小：`nameTransliterator` 介面只要 `Transliterate(name string, gender translit.Gender) (string, translit.Tier, bool)`（`apps/buckrogers/player_name.go`），`NewPlayerNames(tr, names)` 先查該語言的名字表（`ChineseFor`，ja、ko 各自載入 `name-glossary.<lang>.tsv`），查不到才呼叫音譯器。
  ECL 路徑把結果組成 `譯名(英文)`，放不下時降段（只譯名、再退回英文），不管語言。目前只有 zh-TW、zh-CN 在 `live_lane.go` 的 `switch l.lang` 設定音譯器，其餘走 `default` 設 `playersOff=no-transliterator`。
- 專案音譯詞典（`text/translit-names.tsv`）的 85 個英文名全在 CMU 發音詞典（`text/cmudict/cmudict.dict`，135,166 行、126,052 個詞條、39 個音素）內；名字表（`name-glossary.tsv`）的單字中有 12 個不在 CMUdict（`TURABIAN`、`HOLZERHEIN`、三個 `.DOS` 鍵等），由名字表本身處理，不經音譯器。
- 日文字型字集（`font/charset.ja.txt`，6,686 字）含片假名 U+30A1 至 U+30F6 全部 86 個、`ー`（U+30FC）、`・`（U+30FB）；`ヷ ヸ ヹ ヺ`（U+30F7 至 U+30FA）不含。現行字型子集（`font/characters.ja.txt`）含 76 個片假名字母加 `ー`、`・`；
  字型子集由 catalog 產生，音譯輸出要保證渲染，必須先把允許字集做成 catalog（做法同規格 037 §3.4 的 `translit-chars`）；本機 Unifont 對這 88 個字都有 16 寬字模（已實測）。
- 日文名字表（`text/name-glossary.ja.tsv`）寫多字名用 `・`，例 `アレクサンダー・ウィリアムズ`；韓文用空白（規格 045）。
- 原版角色名可含數字、空白、`.`、`?`，也可只有一個字元（規格 037 §2，phase-244）；名字最長 15 字元（規格 038 §3.1）。
- 日文片假名沒有單一官方的英語轉寫標準；本規格的規則是專案自訂（依內閣告示《外来語の表記》的音韻對應與常見人名慣例整理），由專案詞典與固定名單校準，**母語者未校對**（§6）。
- 兩輪審查對 117,493 個純字母 CMUdict 詞（第一讀音）的統計：12,609 個（10.7%）含相鄰元音，其中 3,858 個是 `ER` 後接元音；2,889 個含「輔音＋`Y`＋元音」；詞尾相鄰 `T S`、`D Z` 共 3,735 個；元音後 `R` 被吸收的有 10,429 個；26 個是單字母詞；8 個沒有元音。這些情形是 §3.3、§3.4 必須有明確規則的理由。

## 3. 契約

### 3.1 介面與載入（日韓共用，Go，通用層 `xlate/translitjk`）

- `Load(textDir, lang string) (*Transliterator, error)`：`lang` 只接受 `ja`、`ko`，其他值回錯誤。讀 `textDir` 下的 `translit-<lang>-names.tsv`、`translit-chars.<lang>.tsv` 與 `cmudict/cmudict.dict`，不讀語言目錄（與 `translit-zh-CN-map.tsv` 同）。
  任一檔缺漏、標頭不符、`english` 重複、`translation` 為空或含允許字集外的字，回傳錯誤；`Load` 不寫檔。
- `Transliterate(name string, g translit.Gender) (out string, tier translit.Tier, ok bool)`，`g` 不使用。`Tier` 沿用 `translit.Tier`（`dict` ＞ `cmudict` ＞ `spelling`）。純函式、決定性、可多 goroutine 並行使用；不寫檔、不進存檔。
  `*Transliterator` 必須滿足 `apps/buckrogers` 的 `nameTransliterator`，以 `var _ nameTransliterator = (*translitjk.Transliterator)(nil)` 在 `player_name_test.go` 於編譯期鎖定。另匯出：
  `Allowed() []rune`（允許字集，升冪，不含 U+0020 與 `-`）；`TransliterateTrace(name, g) (out, tier, ok, rules []string)`（`out`、`tier`、`ok` 與 `Transliterate` 逐位相同，`rules` 是命中的規則編號，依命中次序、可重複；不進介面）；`Rules() []string`（全部規則編號，格式 `J<n>.<列>`、`K<n>.<列>`）；
  測試用選項 `RuleOnly`（關閉 `dict` 層，不進發行路徑；規則追蹤只在規則模式回傳）與 `FromPhones(phones []translit.Phone, letters string)`（直接餵 ARPAbet 音素串與拼寫）。
- 名字先轉大寫、以空白切成字；**任一字含 A–Z、`'`、`-` 以外的字元時整名 `ok=false`**；單一字母的字整名 `ok=false`；連續空白視為一個；整名沒有任何字時 `ok=false`（同規格 037 §3.1）。
- 含 `-` 的字：先以整個字（含 `-`）查詞典與 CMUdict，查不到再分段，各段分別走完整查找，結果依原位置以各語言的連字號連接；任一段為空或只有一個字母，整名 `ok=false`（與 zh 的略過空段不同，三個語言各自照自己的規則；`MARY-` 在 zh 得結果、在 ja、ko 回英文）。含 `'` 的字：查詞典與 CMUdict 時保留原拼寫，拼寫後備時先去掉。
- 輸出每個字元都必須在該語言的允許字集內，**U+0020 與 `-` 除外**（同 `translit` 對連字號的豁免；ja 的輸出不含這兩者，ko 的輸出以它們連接多字與連字號段）；否則整名 `ok=false`。`Load` 檢查詞典 `translation` 時同樣豁免 U+0020 與 `-`：ja 的 `translation` 不得含它們，ko 的 `translation` 可含單一內部空白，首尾不得有空白、不得連續空白、不得含 `-`。
- **共用前端放在 `xlate/translit`（zh 與 ja、ko 同一份程式）**，以包裝方式匯出，既有程式與測試一字不動：新檔 `export.go` 匯出 `Phone`（音素、重音、是否元音，複製自內部 `ph`）、`ParsePron`、`SpellingPhones`（輸入須為小寫、無撇號、無連字號，函式內部正規化）、`AlignVowels(letters string, phones []Phone) []string`（nil 表失敗）與 `SharedCMU(path string) (map[string][]string, error)`。
  `SharedCMU` 以一個互斥鎖保護 `map[string]*entry`，`entry` 帶自己的 `sync.Once`、對照表與錯誤；以 `filepath.Abs` 後的路徑為鍵；解析失敗時從 map 移除該 `entry`，下一次呼叫重新解析；成功值載入後唯讀，任何呼叫端不得寫入。`translit.Load`（zh-TW、zh-CN）與 `translitjk.Load` 都經由它取得詞典，四個語言通道在同一進程只解析一次。
  F1、F6 在 `translitjk` 內自寫（約 16 行），不改 zh 的 `normalize`（zh 專屬的步驟與它交織）。
- **zh 不變的護欄**：在動 `translit` 之前，先在基準 commit 對 `text/cmudict/cmudict.dict` 全部純字母詞（117,493 個）與 `Male`、`Female`、`GenderUnknown` 各執行一次 `Transliterate`，輸出每列 `word\tgender\tzh\ttier\tok` 的 SHA-256 記入 phase 文件；改動後同法重算必須相同。測試以 `BUCKROGERS_CHT_ROOT` 閘控，缺少時 skip 並印原因，有執行時印出涵蓋的詞數；另以 `translit_test.go` 與 phase254 七條回歸為護欄。
- 載入期字型檢查只在 `live_lane.go` 的 `case LangJa, LangKo` 內、`translitjk.Load` 成功之後執行：`Allowed()` 的每個字元都必須在 `l.font.Glyphs` 內；缺任一字，玩家名停用，`playersOff` 為 `translit-font: 缺 U+XXXX 等 N 字`（`U+XXXX` 取最小碼位）；載入失敗為 `translit-<lang>: <錯誤>`。語言通道與其他語言不受影響；zh-TW、zh-CN 不加此檢查。

### 3.2 每個字的查找順序（日韓共用）

1. 專案詞典 `text/translit-<lang>-names.tsv`：欄位 `english`、`translation`、`basis`；`english` 全大寫、不含空白；人工審定或機器草擬後審定，可放慣用譯名。命中即為 `dict`。
2. CMU 發音詞典：取該字**第一個**讀音（ARPAbet，帶重音數字），走 §3.3 前端與各語言後端。命中為 `cmudict`。
3. 拼寫後備：直接使用 `translit.SpellingPhones`（同規格 037 §3.2 第 3 點），再走同一個前端與後端。標 `spelling`，品質最差，供診斷區分，仍照常顯示。後備產出為空（例如只含 `h`）整名 `ok=false`。

`tier` 取各字中最低的來源等級。含 `x` 的詞第一讀音常是 `G Z`（`exit`、`alexander`），不加規則，交詞典。

### 3.3 共用前端：音素到音節（日韓共用）

輸入：一個字的音素串（ARPAbet，元音帶重音數字 0、1、2）與去掉撇號與連字號的小寫拼寫。輸出：音節串，每個音節 `Syl` 含：

| 欄位 | 內容 |
|---|---|
| `Pre` | 獨立輔音串（不與元音合成的輔音），每個帶位置標記 `Initial`（詞首串）、`Medial`（兩個元音之間的串） |
| `Onset` | 緊鄰元音之前的單一輔音（`Pal` 時為 `Y` 之前的輔音），或空；`NG` 不當 `Onset` |
| `Pal` | `Onset` 之後緊接 `Y` 再接元音（輔音＋`Y`＋元音）時為真，`Y` 併入該音節 |
| `Nuc` | 元音音素、重音、對應的字母（見 F2，可為空） |
| `R` | 元音後的 `R`（接輔音或詞尾）被吸收，記在元音上 |
| `Post` | 只有最後一個音節有：詞尾輔音串（位置 `Final`） |

後端判斷「X 後接輔音 Y」時，Y 取同一音節 `Pre` 的下一個元素，沒有則取 `Onset`（`Pal` 時為其輔音）；詞尾串內取 `Post` 的下一個元素；查找不跨過元音。以上結構是契約的語意，實作可改為扁平序列。

- **F1 ER 後接元音**：`ER` 後直接接元音時，無重音 `ER0` 改為 `AH0`，有重音 `ER` 保留，並補一個 `R` 作為下一音節的頭輔音（`Maria`、`Everett`）。同規格 037 `normalize` 的第一步。
- **F2 元音與拼寫對齊**：元音字母組是連續的 `a e i o u`，加上不在 `a e i o u` 之前的 `y`；`w` 屬前一個 `a e o` 組（`aw ew ow`），條件是 `w` 之後不是元音字母；`qu` 的 `u` 不算；詞尾單獨的 `e`、`-es`、`-ed` 的 `e` 不發音，**只在字母組多於元音音素時扣掉**。
  字母組少於元音音素時，把 `i y e u o a` 起頭且長度至少 2 的組拆成兩組，直到相等；拆完仍不等，整字不給字母。對齊成功時每個元音音素得到一個字母組；後端的判讀：`AA` 看字母組是否以 `o` 起首；無重音 `AH`、`IH`，以及 `EH`，取字母組的**末位字母**（`michael` 的 `ae` 取 `e`），末位為 `w` 時取其前一個字母（`aw` 取 `a`）。
  實作即規格 037 的 `alignVowels`，匯出為 `AlignVowels`，不另寫；本條是摘要，兩者不一致時以程式為準並回頭修本條。
- **F3 單一聲母音節化**：每個元音為一個音節核；緊鄰其前的單一輔音為 `Onset`（`Y` 前面有輔音時見 F4）；其餘輔音為獨立輔音（詞首串的非末位、元音之間輔音串的非末位、詞尾串），帶位置標記。`NG` 不當 `Onset`。同規格 037 `syllabify`。
- **F4 輔音＋`Y`＋元音**：`Y` 之前緊接一個輔音（不是 `NG`、`Y`）且之後是元音時，該輔音為 `Onset`，`Y` 併入該音節、`Pal` 為真（`HH Y UW` 的 `Hugh`、`M AE TH Y UW` 的 `Matthew`、`W IH L Y AH M` 的 `William`）。`Y` 前沒有輔音（詞首或接在元音後）時，`Y` 是 `Onset`、`Pal` 為假（`Yuri`）；`Y` 前是 `NG` 時，`NG` 為獨立輔音、`Y` 是 `Onset`（`Pyongyang`）。
- **F5 元音後的 `R`**：`R` 在元音後、接輔音或詞尾時，併入該元音（`R=true`）、不再是獨立輔音；`R` 在元音前是頭輔音；`ER` 本身已含 r。
- **F6 詞尾 `T S`、`D Z`**：詞尾相鄰的 `T`、`S` 合為 `TS`，`D`、`Z` 合為 `DZ`（`Roberts`、`Edwards`、`Watts`、`Woods`）。CMUdict 沒有這兩個音素，由前端合成。
- **F7 其他**：`K W`、`G W`、`HH W` 不合併（`Quinn`、`Quentin` 交詞典）；`TH`、`DH`、`ZH` 保留各自的音素，由後端決定。
- **F8 沒有元音音素的字**（`HM`、`SH`、`FS`）整名 `ok=false`（輸出為空即不顯示，名字維持英文）。

### 3.4 日文：音節到片假名

規則編號 `J1` 至 `J9`；每條至少一個固定測試名（§5 第 1 點的規則追蹤）。括號內的例子是意圖；它們全部抽成 `docs/re/phase-NNN-spec-examples.ja.tsv`（欄位 `name`、`expected`、`rule`、`kind`），以規則模式逐列比對（§5 第 1 點），與規則不符的例子視為規格缺陷；慣用寫法與交詞典的例子標 `kind=idiom`，只列出差異。

**J1 元音（「X 列」指與頭輔音合成的拍，例如 `T`＋`IY` 為 `ティ`）。**

| 音素 | 片假名 | 備註 |
|---|---|---|
| `IY` | イ列＋`ー` | 長音條件見 J7；`T`、`D` 之後的詞尾無重音 `IY` 為 `ティ`、`ディ`，不加 `ー`（`Betty` ベティ、`Eddie` エディ；`Billy` ビリー） |
| `IH` | イ列 | 無重音且字母為 e、a、o、u 時按 `AH` 無重音的字母表（`Elaine` エレイン）；字母為 i、y 或無字母時為イ列 |
| `EY` | エ列＋`イ` | `Kate` ケイト |
| `EH` | エ列 | 字母（末位）為 a 且其後為 `R`＋元音（`Harry`、`Larry`、`Sarah`、`Karen`）時按 `AE` |
| `AE` | ア列；`K`、`G` 之後為 `キャ`、`ギャ` | `Kathy` キャシー |
| `AA` | ア列；字母組以 o 起首時為オ列 | `Scott` スコット |
| `AH` | 有重音：ア列；無重音：按字母 `a`→ア、`e`→エ、`i`→イ、`o`→オ、`u`→ア、`y`→イ，無字母→ア | `Celeste` セレスト |
| `AO` | オ列＋`ー` | `Paul` ポール |
| `OW` | 有重音：オ列＋`ー`；無重音：オ列 | `Joe` ジョー、`Milo` マイロ |
| `UW` | ウ列＋`ー` | `Lou` ルー |
| `UH` | ウ列 | |
| `AW`、`AY`、`OY` | ア列＋`ウ`、ア列＋`イ`、オ列＋`イ` | |
| `ER` | ア列＋`ー`（r 併入） | `Peter` ピーター |

**J2 頭輔音（接元音時）。** 順序為 ア イ ウ エ オ：`K` カ キ ク ケ コ；`G` ガ ギ グ ゲ ゴ；`S` サ シ ス セ ソ；`Z` ザ ジ ズ ゼ ゾ；`T` タ ティ トゥ テ ト；`D` ダ ディ ドゥ デ ド；`N` ナ ニ ヌ ネ ノ；`HH` ハ ヒ フ ヘ ホ；`B` バ ビ ブ ベ ボ；`P` パ ピ プ ペ ポ；`M` マ ミ ム メ モ；`R`、`L` ラ リ ル レ ロ；
`F` ファ フィ フ フェ フォ；`V` バ ビ ブ ベ ボ（不使用 `ヴ`，見 §6）；`W` ワ ウィ ウ ウェ ウォ；`Y` ヤ イ ユ イェ ヨ；`SH` シャ シ シュ シェ ショ；`CH` チャ チ チュ チェ チョ；`JH`、`ZH` ジャ ジ ジュ ジェ ジョ；`TH` サ シ ス セ ソ；`DH` ザ ジ ズ ゼ ゾ。
`Y`＋`IY` 為 `イー`，`Y`＋`UW` 為 `ユー`，`W`＋`UW` 為 `ウー`；其中的 `ー` 是 J1 的 `ー`，受 J7 的條件限制（其後直接接元音時不加，`Euan` ユアン）。

**J3 輔音＋`Y`＋元音（`Pal`）。** 輔音取イ列字（`K` キ、`G` ギ、`HH` ヒ、`B` ビ、`P` ピ、`M` ミ、`N` ニ、`L`／`R` リ、`V` ビ、`F` フ、`T` テ、`D` デ、`S` シ、`Z` ジ、`TH` シ、`SH` シ、`CH` チ、`JH`／`ZH`／`DH` ジ），其後依後接元音：
`UW`、`UH`（或字母為 u 的無重音 `AH`）加小字 `ュ`，`UW` 的 `ー` 依 J1、J7（`Hugh` ヒュー、`Cuba` キューバ、`Annual` アニュアル）；`AA`、`AE`、有重音 `AH`、`ER`、`AY`、`AW` 加 `ャ`；`EH`、`EY` 加 `ェ`；`AO`、`OW`、`OY` 加 `ョ`；`IY`、`IH` 不加小字；後綴（`ER` 的 `ー`、`AY`、`EY` 的 `イ`、有重音 `OW` 的 `ー`）依 J1。
後接無重音 `AH` 時按 J1 的字母取ア、エ、オ，不加小字（`William` ウィリアム、`Daniel` ダニエル、`Julia` 的 `リア`）；字母為 i、y 時不另加元音。`Pal` 不得產生 `ン` 開頭。例：`Kyoto` キョート、`Billiard` ビリャード。

**J4 獨立輔音（不接元音）。** `T`、`D`→`ト`、`ド`；`CH`、`JH`、`ZH`→`チ`、`ジ`、`ジ`；`SH`→`シュ`；`F`、`HH`→`フ`；`V`→`ブ`；`TH`→`ス`；`DH`→`ズ`；`R`、`L`→`ル`；`W`→`ウ`；`Y`→`イ`；`TS`→`ツ`；`DZ`→`ズ`；其餘為ウ列（`K ク`、`G グ`、`S ス`、`Z ズ`、`B ブ`、`P プ`）。
鼻音：`N` 在元音後或輔音後（不在詞首）為 `ン`（`Kiln` キルン），詞首且接輔音時為 `ヌ`；`M` 在 `B`、`P`、`F` 前（詞首除外）為 `ン`，其餘輔音前與詞尾及詞首為 `ム`；`NG` 在 `K`、`G`、`T` 前為 `ン`，`NG` 後直接接元音時為 `ン` 加該元音音節的ガ行（`Singer` シンガー），其餘為 `ング`。

**J5 元音後的 r（`R=true`）。** `AA R`、`AO R`、`OW R`、`AE R`、`AH R`：元音列＋`ー`；`EH R`：エ列＋`ア`；`IH R`、`IY R`：イ列＋`ア`；`UH R`、`UW R`：ウ列＋`ア`（`Sure` シュア、`Poor` プア，`Moore` ムーア 一類慣用交詞典）；`AY R`、`AW R`、`EY R`、`OY R`：該雙元音＋`ア`。`ER` 見 J1。
J5 的 `ア` 優先於 J1、J7 的 `ー`。

**J6 促音 `ッ`。** 加在輔音拍之前，條件是下列之一（元音須 `R=false`）：
(a) 有重音（重音 1 或 2）的短元音（`AE EH IH AH AA UH`）緊接詞尾輔音串的第一個輔音，且該輔音為 `K P T CH JH D`，或詞尾的 `TS`、`DZ`（`Jack` ジャック、`Ted` テッド、`Watts` ワッツ、`Woods` ウッズ）；
(b) 無重音 `AH`、`IH` 之後的詞尾 `K P T D`，或詞尾 `K S`（`Eric` エリック、`Janet` ジャネット、`Alex` アレックス）。
有 `R=true` 的元音不加 `ッ`（`Park` パーク、`Clark` クラーク、`Bart` バート）。詞中的輔音串與兩個元音之間的輔音不加（`Jackson` ジャクソン、`Hudson` ハドソン、`Patrick` パトリック、`Betty` ベティ）。

**J7 長音 `ー`。** `IY`、`UW`、`AO`、`OW` 的 `ー` 只在其後緊接輔音或詞尾時加；其後直接接元音時不加（`Leo` リオ、`Cynthia` シンシア、`Joel` ジョエル）；`IY` 前面沒有輔音（接在另一個元音之後）時也不加；詞首的 `IY` 加 `ー`（`Eve` イーブ）。`Leo` 的慣用 レオ 交詞典。

**J8 不得出現的形式。** 詞首不出現 `ッ`、`ー`、`ン`；`ー` 不連續、不接在 `ン`、`ッ` 之後；`ン` 之後不接 `ー`；`ッ` 不接在 `ー` 之後（無 `ーッ`）。詞首的 `M`、`N` 接輔音時依 J4 取 `ム`、`ヌ`。

**J9 組成。** 多字名以 `・`（U+30FB）連接；連字號的各段同樣以 `・` 連接。

### 3.5 允許字集、檔案與工具

- 專案詞典 `text/translit-ja-names.tsv`（韓文 `text/translit-ko-names.tsv`），欄位 `english`、`translation`、`basis`。檔名刻意不用 `translit-names.<lang>.tsv`：`catalog_font.py`、`lang_check.py`、`name_glossary.py` 都以 `*.<lang>.tsv` 取得語言 catalog，且標頭必須是 `key/translation/source`。
  詞典的 `english` 集合為 `translit-names.tsv` 的 85 個名字加規格列名的補充名（`PIERRE`，規則得 ピエア，慣用 ピエール、피에르）；`translit-names.tsv` 之後新增名字時，ja、ko 詞典同步補上審定譯名（lint 以此為準，刻意的同步政策）。
- 允許字集檔 `text/translit-chars.ja.tsv`：`key/translation/source` 三欄，`source` 為 `translit-table`，一列一字，不含 U+0020 與 `-`。日文的集合為 U+30A1 至 U+30F6 全部片假名 ∪ {`ー`、`・`} ∪ 專案詞典全部用字（皆在 `charset.ja.txt`）。它屬 `*.<lang>.tsv`，`catalog_font.py chars/build --lang ja` 自動併入字型字元清單（重建後 `characters.ja.txt` 多 10 字：`ゾ ヂ ヅ ヌ ヮ ヰ ヱ ヲ ヵ ヶ`）。
- 工具修改（已在複本實測）：
  - `tools/lang_check.py` 的 `NON_CATALOG_PREFIX` 改為 `("name-glossary", "translit-chars")`：`families()` 對任何語言都不回傳 `translit-chars`，`check()` 與 `test_ja_check.py`、`test_lang_check.py` 的真實資料覆蓋測試共用同一份家族清單（不在 `check()` 內另濾，否則 ko 的 2,128 列使 `test_caps_cover_most_rows` 失敗）；`LangConfig.no_files` 內的 `translit-chars` 保留；`test_lang_check.py` 新增一例：合成 text 目錄放入 `translit-chars.<lang>.tsv` 與 `translit-<lang>-names.tsv` 時，`families()` 不含 `translit-chars`，`check()` 的列數、key 數、錯誤數與不放時相同。
  - 新增 `tools/translit_jk.py`：`chars --lang <ja|ko> [--check]`、`lint --lang`、`verify-fixed`、`examples --check`；`tools/test_translit_jk.py`（含 `lint` 的合成負例：允許字集外的字、重複 `english`、`basis` 不在白名單、`english` 集合不符、ja 詞典含空白、ko 詞典首尾或連續空白）。
  - `ja_check.sh`、`ko_check.sh` 第 1 步的 unittest 行加入 `test_translit_jk.py`，並加 `translit_jk.py lint`、`chars --check`、`examples --check` 三步。
  - `tools/translit.py` 的 `--lang` 限制為 zh-TW（`translit.py --lang ja|ko|zh-CN` 會用 zh 譯音表寫出內容錯誤的字集檔）；`font/README.md` 補述。
- 專案詞典 lint：`english` 集合同上、無重複、NFC、`translation` 非空且每字在允許字集內（U+0020 與 `-` 豁免，見 §3.1）、`basis` 屬於 {`machine-reviewed`、`reviewed`}。
- 規格 042 §3.1 的「不產生檔案的家族」清單中 `translit-chars` 改註為「音譯允許字集，不是翻譯家族；ja、ko 的 `translit-chars.<lang>.tsv` 由規格 044、045 定義」（043 §3.1 以 042 §3.1 為準）。
- 字型子集因此多出的字在同一個 commit 重生 `font/characters.ja.txt`；`ja_check.sh` 第 4 步 `cmp` 通過。字型 manifest 只綁 `*.zh-TW.tsv`，不受影響。

### 3.6 接線與顯示

- `live_lane.go` 的 `switch l.lang` 加 `case LangJa, LangKo`：`translitjk.Load(l.textDir, l.lang)` 成功才做載入期字型檢查（§3.1）、`NewPlayerNames(tr, names)` 並 `SetPlayerNames`，失敗只設 `playersOff`；`default` 保留給測試語言 zz。`ja_test.go`、`ko_test.go` 對 `playersOff` 的既有斷言同步修改（檔案齊全且字型已以新允許字集重建時 `players != nil` 且 `playersOff == ""`；字型尚未重建時失敗原因會是 `translit-font`，實作次序先重建字型），並加負例（缺檔、缺一個字的合成字型：`players == nil`、`playersOff` 以 `translit-<lang>:` 或 `translit-font:` 起頭、語言通道仍啟用、其他語言不受影響）。
- 顯示格式、降段、窄欄只譯名、名字註記階層：沿用規格 038 與 036，不改。ECL 的 `譯名(英文)` 以半形 `(` `)` 組成，名字註記單位涵蓋整個 `譯名(英文)`（單位內的空白個數不影響 `eclWordTokens`：整個單位是一個 token，單位加黏著字寬於視窗時才在單位內每個空白前切開）。
- 寬度一律以半形單位計（規格 039）：片假名、`ー`、`・`、諺文音節為 2 單位，ASCII 空白、`-`、括號與英文為 1 單位；上限比較沿用現行程式（`stringUnits(zh) <= 2*n`、`textUnits(c) > 2*avail`），規格 038 §3.3、§3.4 的「字數」一律讀作單位（`・` 在 ja 是 2 單位，`•` 在 zh 是 1 單位）。
  日文名字比中文長（85 個詞典名平均 ja 約 4.2 字、zh 約 2.6 字；原型粗估只有極少數超出戰鬥欄），寬度不夠時依既有降段落到只譯名，再落到英文。
- 名字表命中優先於音譯（`ChineseFor`，區分大小寫的精確比對），玩家取名與名字表人物同名時顯示名字表譯名（規格 038 §3.2）。`PlayerNames` 的快取鍵含性別，ja、ko 同名不同性別會有兩筆相同結果，無害。

### 3.7 打包與授權

- `tools/package.sh` 在 `text/*.tsv` 迴圈之後，另複製 `text/cmudict/cmudict.dict`、`text/cmudict/LICENSE`、`text/cmudict/README` 到發行包的 `text/cmudict/`，複製 `text/LICENSE-translit-table.md`；新的四個 `.tsv`（兩個詞典、兩個字集）由迴圈自動帶入，`TEXT_EXCLUDE` 不需增列。
  `THIRD-PARTY.md` 由 `tools/release/third_party.py` 整檔重寫，CMU 發音詞典（BSD 式授權，全文隨包）與音譯表（CC BY-SA 4.0，自中文維基轉錄）的聲明加在該腳本；`docs/release/讀我.txt` 同步。
  目前發行包只複製 `.tsv`，沒有 `text/cmudict/`，既有 zh-TW、zh-CN 的玩家名音譯在發行包內載入失敗（推論，未實跑發行包）；本條一併補上。發行包原始增量約 3.6 MB（壓縮後較小）。
- 前置檢查（複製之後、各語言字型建置之前）：對暫存的 `text/` 逐項 `test -f`：`cmudict/cmudict.dict`、`cmudict/LICENSE`、`LICENSE-translit-table.md`、`translit-table.tsv`、`translit-arpabet.tsv`、`translit-names.tsv`、`translit-chars.zh-TW.tsv`、`translit-ja-names.tsv`、`translit-chars.ja.tsv`、`translit-ko-names.tsv`、`translit-chars.ko.tsv`；缺任一項打包失敗。
- 打包後冒煙：`apps/buckrogers` 新增 `TestPackagedLanes`，以環境變數 `BUCKROGERS_PKG_ROOT`（指向發行包的 `common/`，含 `text/` 與 `font/`）閘控；載入 `LoadLiveRuntimeOptions`（zh-TW 用 `font/buckrogers-unifont.golemfnt`，其餘用 `font/buckrogers-<lang>.golemfnt`），斷言四個通道全部啟用、`DebugSummary` 不含 `語言停用` 與 `玩家名=off`，且每個通道對 `NICOLE STEELE`（女）的 `Chinese` 有結果。
  `package.sh` 在字型迴圈之後以 `GO_IMAGE`、`$STAGE/common` 唯讀掛載執行 `go test ./apps/buckrogers -run TestPackagedLanes -count=1 -v`，輸出必須含 `--- PASS`、不得含 `--- SKIP`，否則打包失敗；`package.sh` 以 `git archive` 取已推送分支 HEAD 的 dosgolem，測試先進該 commit。
- `docs/release/讀我.txt`、`README.md` 的「玩家名暫時顯示英文（音譯尚未提供）」隨實作改寫（規格 042 §3.10、043 §3.10 已有同類條款）。外洩掃描只比對檔案雜湊與基本檔名，已查四個禁止來源沒有同名衝突。

### 3.8 範圍邊界

- 本規格只處理「整個字串就是玩家名」的路徑（規格 038 §3.2：ECL 玩家名單元、戰鬥右欄、隊伍欄、角色頁）。引擎片段中嵌入的玩家名（`FLAVIUS は`、`FLAVIUS 은(는)` 型，規格 046）仍是英文，不在本規格；那一類屬規格 038 §4 的另案。
- ko 的 ECL 玩家名續接呼叫起點空白見規格 045 §3.4。

### 3.9 實作時要加的修訂註

規格 042 §3.1（`translit-chars` 清單）、042 §3.8 與 043 §3.8（玩家名：`PlayerNames` 啟用，`no-transliterator` 只留給測試語言 zz）、042 與 043 §3.10（打包）、038 §3.3、§3.4（「字數」讀作半形單位）、046 §3.4 與 §3.6（玩家名分支見規格 045 §3.4）、037 §3.1、§3.3、§5（`translit` 匯出符號，行為不變；「CMUdict 授權全文隨發行包」由 §3.7 達成）、035 §3.5（第三方與打包內容）、`docs/re/README.md`（phase 文件與兩份固定名單、兩份例子表的索引）、`README.md`、`docs/release/讀我.txt`、`font/README.md`。

## 4. 不做什麼

- 判斷字串是不是玩家名、各畫面怎麼顯示（規格 038）。
- 非英語名字的專門規則（照英語處理）、日文名字的漢字寫法、長音與促音的多種慣用寫法並存（只出一種，其餘交詞典）。
- 手冊段落、母語者校對（§6）、`ヴ` 行。

## 5. 驗收

1. 單元測試：J1 至 J7 每個規則編號與表格列至少一個樣本；J8 由輸出不變式涵蓋；J9 由 §5 第 2 點 (4) 的 `NICOLE STEELE`、`MARY-JANE` 涵蓋。三層查找各有命中樣本；含數字或標點的名字（`A 1.?`、`R2D2`）、單一字母名（`Z`）、含單字母段的連字號名（`MARY-J`）、無元音的字（`HM`）回 `ok=false`；含撇號或連字號的名字（`O'BRIEN`、`MARY-JANE`）正常；允許字集外的輸出回 `ok=false`；決定性；`Gender` 不影響輸出。
   - 規則追蹤：`TransliterateTrace` 與 `Transliterate` 逐位相同（全字典）；覆蓋測試斷言固定名單命中的編號集合等於 `Rules()` 去掉「不可達」編號；全字典（含拼寫後備輸出）命中數仍為零的編號，在固定名單檔以 `unreachable:<編號>:<原因>` 列出。
   - 輸出不變式（需完整 `text/cmudict/cmudict.dict`，以 `BUCKROGERS_CHT_ROOT` 閘控，缺少時 skip 並印原因，有執行時印出「檢查 N 詞、`ok=false` M 詞」）：對 117,493 個純字母詞，`ok=false` 的集合必須恰等於預期集合（26 個單字母詞加 8 個無元音詞），其餘詞一律 `ok=true`；輸出詞首無 `ッ ー ン`、無 `ーー`、無 `ンー`、無 `ーッ`、每個字元在允許字集內；兩次執行輸出相同。
   - 例子表：規格括號內的「名字＋寫法」抽成 `docs/re/phase-NNN-spec-examples.<lang>.tsv`，`translit_jk.py examples --check` 以規則模式逐列比對。
   - `-race` 下兩個 goroutine 同時 `Load` 同一路徑；「只解析一次」以兩次 `Load` 回傳的對照表指標相同斷言。
2. 固定測試名單與期望輸出：候選由 dosgolem `xlate/translitjk` 的 `go test -run TestFixedNames -update-fixed` 產生，存為 `docs/re/phase-NNN-translit-fixed-names.<lang>.tsv`（欄位 `name`、`expected`、`tier`、`rules`、`review`；`review` 為 `pending` 或 `ok:<審查者1>,<審查者2>`），dosgolem `xlate/translitjk/testdata/` 放逐字副本與 CMUdict 子集（含 `LICENSE`，由同一測試從完整詞典擷取固定名單所需的詞條與其連字號段），以雜湊與 Buck repo 的檔互鎖；
   `BUCKROGERS_CHT_ROOT` 存在時比對兩份相同，缺少時 skip 並印原因，不得靜默通過。`tools/translit_jk.py verify-fixed` 檢查欄位、`review` 欄與副本雜湊，含 `pending` 的列使它失敗。
   選名原則：(1) 規格列名的名字：`ROARKE`、`CELESTE`、`FLAVIUS`、`JANELLE`、`PIERRE`、`NICOLE STEELE`、`ALEXANDER`、`JENNIFER`、`MICHAEL`、`WILLIAM`、`BUCK`、`WILMA`、`PORT`、`EXIT`；
   (2) 規則覆蓋：對 J1 至 J7 的每個規則編號與表格列，從名字表單字（不含專案詞典的名字、不含 `spelling` 層名字）依字母序取第一個在**規則模式**（`RuleOnly`，關閉 `dict` 層）下觸發該列的名字；池內沒有時，不取 CMUdict 詞，改用單元測試以 `FromPhones` 直接餵 ARPAbet 音素串（避免選出審查者無法判斷慣用寫法的罕見詞）；沒有任何輸入能觸發的分支刪除條文或以音素串測試標「無單字輸入」；
   (3) 三層各至少 5 個：`dict`、`cmudict`、`spelling`（`spelling` 取 CMUdict 查無的名字表字與 3 個合成拼寫）；專案詞典的 85 個名字另列為 `dict` 層樣本，只驗 tier 與「輸出等於詞典該列」，同時在規則模式下也跑一遍，期望值記入規則回歸表，防止規則缺口被詞典蓋住；
   (4) 邊界：`Z`、`A 1.?`、`R2D2`、`O'BRIEN`、`MARY-JANE`、`NICOLE STEELE`、15 字元最長名、連續空白、只含 `h` 的字。期望值入庫前由兩位獨立審查者確認（避免以規則輸出回填的循環驗證）。
3. 專案詞典 `text/translit-ja-names.tsv`：§3.5 的 `english` 集合，草擬後逐列審定，`basis` 記 `machine-reviewed`；`translit_jk.py lint` 通過。
4. 字型：`translit-chars.ja.tsv` 與 `characters.ja.txt` 重建零缺字（先於 `ja_test.go` 斷言）；載入期字型檢查與合成字型負例；`ja_check.sh`、`lang_check.py`、`name_glossary.py lint`、`catalog_font.py lint` 通過；`tools/package.sh` 的前置檢查與冒煙（§3.7）通過。
5. 離線與同狀態：日文通道的玩家名在隊伍欄、戰鬥欄、ECL 敘事、角色頁顯示 `カタカナ(ENGLISH)` 或降段結果。以前後對照收據（舊 runner 加舊資料對新 runner 加新資料，做法同 phase-306 §4）：zh-TW、zh-CN、en、ko 的時點畫面與機器狀態逐位元相同；ja 的機器狀態相同，`skips=0`，畫面差異只在玩家名相關格：以新 runner 的測試開關關閉玩家名時，與舊 runner 逐位元相同（證明改動沒有波及名字以外的格），再以 ECL 追蹤與覆繪矩形斷言相異格集合是名字格集合的子集。
   現有狀態含的玩家名只有六個（`FLAVIUS`、`CELESTE`、`PIERRE`、`NICOLE STEELE`、`ROARKE`、`JANELLE`），固定名單的其餘名字只由單元測試驗收；收據前先重建含新允許字集的 `workplace/lang-fonts/buckrogers-ja.golemfnt`。
6. 離線重播（phase257 trace）：ja 通道 `ecl` 紀錄的 `dPlayer` 計數與降段分布列出（目前恆為 0）；其他語言逐列相同。`LoadLiveRuntimeOptions` 前後的 `runtime.MemStats.HeapAlloc` 與耗時（zh-TW 單語、四語各一次）只記錄，不設門檻。

## 6. 開放項目

| 項目 | 消除條件 |
|---|---|
| 音素到片假名規則是專案自訂，慣用寫法有多種（`ー`、`ティ` 與 `チ`、`ッ`、`Y` 行大小字：`ビリャード` 與 `ビリヤード`），母語者未校對 | 母語者校對固定名單與詞典；規則逐條調整並回寫 §3.4 |
| `V` 取バ行（`ビクター`）而名字表有 `ヴィルニコフ`、`セヴァーン`（用 `ヴ`）：同一畫面可能並存兩種寫法 | 使用者或母語者決定規則改用 `ヴ` 行，或名字表那幾條標為例外 |
| 次重音（重音 2）是否算 J6 的「有重音」（暫算：`Acrobat` アクロバット） | 母語者校對 |
| 拼寫後備品質差，原版名字多為英文常見名或幻想名 | 專案詞典逐步覆蓋；`spelling` 等級的名字在診斷計數 |
| 慣用長短不一的名字（`Walter` ウォルター、`Greg` グレッグ、`Duke` デューク、`Tony` トニー、`Stuart` スチュアート、`Steven`／`Stephen` スティーブン、`Leo` レオ） | 進專案詞典 |
| 名字比中文長，窄欄與表格退回英文的比例 | 驗收第 5 點的收據量測各畫面實際降段情形；必要時另訂縮短規則 |
