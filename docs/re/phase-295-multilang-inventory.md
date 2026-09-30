# 第二百九十五階段：多語框架盤點

日期：2026-09-30
狀態：定稿（主代理審閱）；程式行號以 dosgolem `94825fb` 為準，後續 commit 可能位移，以函式名為準。
用途：規格 040 的原版與程式證據。只讀調查；未讀手冊題庫、答案解碼工具或手冊內文。

## 0. 結論

1. **切換語言不需要動原版。** LiveRuntime 是純觀察者：`StepReader` 只有讀取方法
   （`apps/buckrogers/live_menu.go:14-27`），覆繪只在 `ComposeWith` 疊到輸出 RGBA
   （`apps/buckrogers/live_runtime.go:1104-1248`）。「英文」模式等於前端改畫
   `ScaleIndexedRGBA(indexed, palette, scale)`（`apps/buckrogers/menu_overlay_runtime.go:215`），
   原版畫面必然完整露出。可用 `owner.Digest()` 做「按 F4 與不按 F4 同腳本機器狀態相同」的收據。
2. **建議架構：單一觀測分派，多條語言通道（lane）。** 現有程式已是「一個 watcher、每倍率一個
   presenter」（`[2]` 陣列）。延伸成 `[語言][倍率]`；對版面依語言而變的四個家族（ECL 敘事窗、
   水平選單、引擎訊息分派、手札）每語言各一個 watcher，但由同一個 `BeforeStep` 餵事件。
   不建議「每語言一個完整 LiveRuntime 並行」：phase-253 量到觀測器已佔 250M 步中的
   約 5–12 秒（33 秒對無觀測 21–28 秒），四條並行約增加一倍 CPU，前端 `-clock 50` 的餘裕不夠（需實測）。
   也不建議「切換時重建 runtime」：會遺失手冊題進行中狀態、隊伍快照（規格 038 只在兩個姓名 hook 取快照）、
   劇情頁進度與原版 ASCII 字形表。
3. **所有語言在啟動時載入並驗證**（現行各家族在載入時就做版面驗證，失敗即中止啟動）。
   新語言的驗證失敗應讓該語言從 F4 循環中停用並記錄原因，不應讓遊戲無法啟動（需使用者確認）。
4. **字型必須每語言一份，不能合併成單一字型。** 同一碼位在中文與日文字形不同：Unifont 主字型的
   漢字取自文泉驛，Unifont tarball 另附 `unifont_jp-17.0.05.hex`（JIS X 0213 字形）。
   現行 `LiveRuntime` 只持有一個 `*xlate.Font`（`live_runtime.go:120,139`），需改為每 lane 一份。
5. **英文原文不進 Git 的邊界可以守住。** Catalog 只存 key、原文長度與 SHA-256（例如
   `text/ecl-text-events.tsv`、`text/hmenu-item-events.tsv`），英文原文只在 ignored 的
   `workplace/*-l10n/source.tsv`。日韓批次翻譯照 zh-TW 的既有流程在 workplace 內進行，
   只把 `key + translation` 合併進 `text/*.ja.tsv`、`text/*.ko.tsv`。
6. **`original_length` 是語言無關的格數預算。** events 檔已帶英文長度，可在 Git 內對每個語言
   lint「譯文格數 ≤ 英文長度」，不需要英文原文。

## 1. Catalog 載入與執行期切換

### 1.1 現況

- `.zh-TW.tsv` 檔名在 Go 端全部寫死，沒有語言參數：
  - `live_runtime.go:124-131`（skill-exit、exit-prompt、post-join、action-bar、manual、body-icon 的必要檔清單）
  - `live_runtime.go:228`（ecl-text）、`:283`（hmenu）、`:376-384`（engine fragment／item／phrase／template／monster）、
    `:394`（coordinate-line）、`:458`、`:468`（logbook、logbook-panel）、`:1311`（manual-english-panel）
  - `live_menu_load.go:18-25`（8 個選單家族）、`live_story.go:51`（`prefix+".zh-TW.tsv"`）
  - `help.go:27`、`menu.go:32-74`、`skill_exit.go:50`、`action_bar.go:56`、`hmenu.go:49`、`ecl_text.go:61`、
    `engine_text.go:113-158,457`、`logbook.go:48,150`、`manual.go:230`、`manual_english.go:34`（錯誤訊息與 readTSV 名稱）
- 啟動入口 `LoadLiveRuntime(textDir, fontPath)`（`live_runtime.go:115`），前端在
  `cmd/buckrogers-play/main.go:409` 呼叫一次。
- **寫死翻譯雜湊**：`post_join_menu.go:18,52` 把 `post-join-menu.zh-TW.tsv` 的 SHA-256 釘成常數。多語時必須改成
  每語言各自登記或移除此釘選。
- Key 格式：語意 key（`menu.create_new_character`）、原文雜湊前綴（`hmenu.0021d5fe20a0`、`frag.xxxx`、
  `item.xxxx`）、ECL 位置（`ecl.1.16.00278`）、手札編號（`logbook.1`、`logbook.1.title`）。
  全部與語言無關，可直接沿用於各語言檔。
- 可選檔行為不一致：ecl／hmenu／engine／logbook 翻譯檔缺席時該家族照樣載入（全英文），
  選單、劇情頁、手冊、body-icon 等缺檔則啟動失敗。

### 1.2 家族狀態分類（決定切換怎麼做）

| 類別 | 家族 | watcher 狀態是否依語言 | 切換做法 |
|---|---|---|---|
| A. 事件辨識與語言無關，presenter 帶譯文 | 選單 8 家族、skill-exit、exit-prompt、post-join、action-bar、body-icon、手冊、劇情頁 1–9 | 否（watcher 以英文雜湊與 callsite 辨識） | presenter 由 `[2]` 擴為 `[L][2]`，每次 `Apply` 對所有 lane 套用；切換只換 compose 用的索引 |
| B. watcher 產出已排版頁面 | ECL 敘事窗（`EclTextPage.Lines`、`endRow/endCol` 中文游標接續，`ecl_text.go:110-127`）、hmenu、engine dispatch、logbook | 是（版面與游標接續隨譯文長度變） | 每 lane 一個 watcher，由同一個 `BeforeStep` 的 `observeEclText`／`observeHMenu`／dispatch entry 餵入；這些只在 hook 命中時工作，成本隨 lane 數線性但不在每步路徑 |

- 同一 lane 在非作用期間照常更新，但 `sync*`（`live_runtime.go:329,488,504,563`）只在 `ComposeWith` 呼叫；
  切換時對新 lane 先跑一次 sync 追上 generation 即可，不需清空重畫。
- 家族出錯的 `recover` 與 `resets` 計數（`live_runtime.go:634`）改為每 lane 各自計。
- 原版 ASCII 字形表（規格 031，`findOriginalASCII`，`live_runtime.go:682`）、legacy normaliser、
  隊伍快照、劇情 pending 與 `storyPending` 屬共用觀測狀態，放在分派層，不分 lane。

### 1.3 英文模式

- 前端：`composed()`（`cmd/buckrogers-play/main.go:285-293`）與截圖 `screenshot()`（`:226`）在英文模式改用
  `ScaleIndexedRGBA`。說明頁照疊（說明頁是前端 UI，不是原版畫面；英文模式的說明頁語言需決定）。
- **手札面板會吃 PgUp／PgDn**：`mapKeys` 呼叫 `g.live.LogbookTurn`（`main.go:151`、`input.go:112`），
  面板開啟時按鍵不送原版。英文模式面板不顯示，`LogbookTurn` 必須回 false，否則玩家按鍵被看不見的面板吞掉。
- 規格 034 英文摘錄面板屬手冊家族，英文模式一併不畫。
- 收據：英文模式 `Compose` 輸出須逐位元組等於 `ScaleIndexedRGBA`；同腳本插入多次 F4 後 `owner.Digest()`
  須與不按相同（同時證明 F4 沒送進 BIOS）。

## 2. 版面限制與預先驗證

| 家族 | 限制 | 驗證時機與位置 | 多語需要 |
|---|---|---|---|
| 說明頁 | 每行 ≤ 38 格、1–15 行、字型須有字模 | 載入時，`help.go:17-55` | 每語言一份 `host-ui.<lang>.tsv` |
| 手札 | 每行 36 格、每頁 19 行、**最多 3 頁**、標題 38 格；姓名加註三段退讓 | 載入時全部預排，`logbook.go:17-36,120-140,146-190` | 每語言跑一次；zh-TW 最長一則 458 字、容量約 1,995 格，日韓可容納 |
| 手冊段落 | 36 欄 × 14 列 = 504 格，`single-page-reject` | `text/manual-overlay-layout.tsv`、`tools/manual_overlay_layout.py` | **zh-TW 最長 363 字，日文約 1.3–1.5 倍、韓文含空白更長，可能超過 504**；需逐列量 |
| ECL 敘事窗 | 執行期排版，放不下整窗退回英文（`ecl_text.go:476-555`） | 執行期；溢位計數 `Stats.Overflows` | 斷行規則需擴充（見下） |
| 水平選單 | 每列 `40 - startCol` 格，溢位整列退回英文；ASCII 大寫字母與數字以熱鍵色畫（`hmenu.go:200-226`） | 執行期 | 各語言譯文須保留熱鍵字母，例 `(E)` |
| 選單家族 | `*-text-safe-rects.tsv` 的 `capacity_cells`、`line_count`、`overflow_policy` | 載入時（`menu_overlay_runtime.go:12-17`）與 `tools/*_text_safe_rects.py` | 每語言跑一次 |
| 劇情頁 1–9 | 每行一個 key，逐行預先斷行，對應原版一行的列欄；第 9 頁有安全矩形檢查（`story_page9_overlay.go:26`） | 載入時 | 日韓譯者須拿到每行格數預算；意思不可跨行搬移 |
| 引擎模板 | `{0}`／`{1}` 佔位（`text/engine-template.zh-TW.tsv`） | 載入時 | 韓文助詞依前字有無收尾子音變化（을／를、이／가），需「을(를)」式中性寫法或助詞選擇機制 |

Python 端寫死 `zh-TW` 的工具（需加語言參數或迴圈）：`catalog_font.py`、`eten_font.py`、`ecl_translation_merge.py`、
`hmenu_translation_merge.py`、`logbook_merge.py`、`name_glossary.py`、`translit.py`、`menu_events.py`、
`gender_events.py`、`class_events.py`、`character_sheet_events.py`、`body_icon_catalog.py`、
`body_icon_text_safe_rects.py`、`career_skill_screen_catalog.py`、`technical_skill_screen_catalog.py`、
`save_roster_join_catalog.py`、`save_roster_join_request_receipt.py`、`class_request_receipt.py`、
`name_prompt_catalog.py`、`manual_runtime_smoke.py`、`ui_runtime_smoke.py`；打包 `tools/package.sh:83,89`
以 `text/*.zh-TW.tsv` 建字型。

Big5 檢查寫死在合併工具：`ecl_translation_merge.py:5,37`、`logbook_merge.py:78`。多語時改為
「該語言字型來源有字模＋字集白名單」檢查。

### 2.1 斷行規則

`layoutEclTextUnits`（`ecl_text.go:476-555`）一字一格，只把連續 ASCII 字母數字視為不可拆的詞
（`isEclLatin`，`:557`），行首禁則只有 `isEclClosing` 的標點（`:561-563`）。

- 日文：需補行首禁則（`ー`、`っ`、`ゃゅょ`、`ぁぃぅぇぉ` 與片假名小字、`・`、`゛゜`），否則會出現行首長音符。
- 韓文：韓文以空白分詞，現規則會在音節中間斷行；需把連續諺文音節視為一詞（類似 `isEclLatin`）。
  空白佔一整格（16 像素字模的一格），韓文字距會很鬆；這與規格 039 的半形機制相關，需一起設計。

## 3. 字型

### 3.1 現況

- 字型子集只由正式譯文產生：`tools/catalog_font.py` 讀所有 catalog 的 `translation` 欄，固定併入
  0x21–0x7E（`catalog_font.py:158-168`），從 Unifont hex 取 8×16 或 16×16 字模轉 16×16 GOLEMFNT（`:176-225`）。
  `font/characters.txt` 目前 2,520 行。
- GOLEMFNT 以 rune 為鍵（`xlate/font.go:22-27`），一字一格（`xlate/layout.go:10`）。
- 倚天：`tools/eten_font.py` 以 Big5 編碼取字（`:69-108`），**無法編碼即失敗，沒有後備字型**；只供本機完整版。
  前端找到倚天字型就優先用（`cmd/buckrogers-play/main.go:391-398`）。

### 3.2 Unifont 17.0.05 覆蓋（本機實測）

來源：`workplace/unifont-src/unifont_all-17.0.05.hex.gz`（另有 `unifont-17.0.05.tar.gz`，內含
`font/precompiled/unifont_jp-17.0.05.hex`）。

| 區塊 | 覆蓋 | 字寬 |
|---|---|---|
| 平假名 U+3040–309F | 96／96 | 全 16 |
| 片假名 U+30A0–30FF、擴充 U+31F0–31FF | 96／96、16／16 | 全 16 |
| 諺文音節 U+AC00–D7A3 | 11,172／11,172 | 全 16 |
| 諺文字母 U+1100–11FF、相容字母 U+3130–318F | 全 | 全 16 |
| CJK 基本區 U+4E00–9FFF、擴充 A | 全 | 全 16 |
| GB2312 6,763 漢字 | 缺 0 | |
| JIS X 0208 6,355 漢字 | 缺 0 | |

Big5 不含的 GB2312 漢字 2,380 個、JIS X 0208 漢字 1,039 個，所以簡體與日文不能用倚天。

### 3.3 策略選項

| 選項 | 內容 | 評估 |
|---|---|---|
| F1（建議） | 每語言一份 GOLEMFNT：zh-TW＝倚天（本機）或 Unifont；zh-CN、ko＝Unifont；ja＝`unifont_jp` | 字形正確；每份約 2,000–4,000 字、每字 37 bytes，總量數百 KB。需改 LiveRuntime 每 lane 一份字型、劇情頁 `setFont` 衍生每 lane 各做 |
| F2 | 所有語言合併一份 Unifont 子集 | 程式改動最小，但日文漢字用中文字形（例如「直」「骨」一類），日文玩家會看出不對 |
| F3 | zh-TW 以外全用倚天 | 不可行（Big5 無諺文、缺上千簡體與日文漢字） |

`unifont_jp` 的授權與字形來源（README 稱映射自 JIS X 0213）需另讀 tarball 內說明確認後才可放進發行包。

## 4. 前端

- 保留鍵表：`cmd/buckrogers-play/input.go:35-37`（F1 說明、F2 倍率、F3 靜音、F11 全螢幕、F12 截圖）。
  F4 目前不在表內，經 `dos.KeyNamed`（`internal/dos/scancode.go:63`，F4＝掃描碼 3Eh）送進原版。
- 改為前端保留：`hostKeysReserved` 加 `"F4": actLang`，`apply()`（`main.go:201-224`）處理循環；
  自動模式腳本 `parseScript`（`input.go:162` 起）加 `lang` 動作。WORKLOG 規則（`WORKLOG.md:3594`）：
  前端功能鍵須在自動模式實際觸發過一次才算驗收。
- 語言狀態：目前沒有任何設定檔。`userDataDir()`（`launcher.go:47`）已有使用者資料目錄，可放
  `settings.json`（只存語言），加 `-lang` 旗標覆寫；寫檔失敗不致命。視窗標題 `windowTitle`
  （`main.go:249`）與 `-text-dir` 旗標說明「繁中 catalog 目錄」（`main.go:344`）需一併改。
- 發行說明 `docs/release/讀我.txt:25-32` 寫明「F4 到 F10 照原版送進遊戲」，需改寫。
- **原版是否用 F4：未知，需量測。**
  - docs/re、WORKLOG 無 F4 或掃描碼 3Eh 的讀鍵紀錄（`docs/re/phase-238-skill-keys.md` 只測 Esc／Enter／方向鍵）。
  - 靜態掃描（主機只讀）：`START.EXE`、`GAME.OVR` 都沒有 `cmp ah,3Eh`（`80 FC 3E`）、`cmp ax,3E00h`。
    `GAME.OVR` 0x3918–0x39BB 的 `cmp al,3Bh…4Bh` 是連續 0x32–0x4B 的分派鏈，形狀像 ECL 指令分派而非讀鍵（強推論）。
    `START.EXE` 0xBF78 的 `3B 3C 3D 3E` 是 Turbo Pascal 執行期錯誤訊息旁的字元表；0xFD30 的
    `4F 50 51 4B 20 4D 47 48 49` 是數字鍵盤方向表。沒有找到功能鍵表。
  - 靜態沒找到不等於不用（可能以算術或表格間接比較）。需在 dosgolem 對 int 16h 回傳 AX=3E00h
    的後續分支做動態量測（主選單、探索、戰鬥、角色頁各一）。

## 5. 特殊家族在各語言的處理

| 家族 | zh-CN | ja | ko | 限制 |
|---|---|---|---|---|
| 手冊查詢題段落（005／034，中文來自中文印刷手冊） | OpenCC 轉 zh-TW 段落 | 需重譯；建議以 zh-TW 段落為主、本機英文手冊為對照 | 同 ja | 504 格單頁上限；**譯文不得保留英文單字**（避免把可能是題目答案的字帶進 Git），需加「拉丁字母白名單」lint；規格 034 英文摘錄面板照舊只在本機 |
| NPC 譯名（036） | OpenCC 轉 `chinese` 欄 | 需片假名欄 | 需諺文欄 | `NameGlossary` 在譯文中找 `chinese` 字串加註（`name_glossary.go:14-30`），所以每語言都要該語言的名字形式。OpenCC 詞組轉換可能改動名字用字，需 lint「轉換後名字出現次數不變」 |
| 玩家名音譯（037／038） | zh-TW 音譯結果做字級繁轉簡；允許字集另建 | 新音譯表 ARPAbet→片假名 | 新音譯表 ARPAbet→諺文 | `PlayerNames` 透過介面呼叫 `Transliterate`（`player_name.go:172,199-211`），可掛不同語言實作；CMUdict 共用；分隔符 zh-TW `•`，ja 慣用 `・`，ko 慣用空白 |
| 劇情頁 1–9 | OpenCC | 逐行重譯，給每行格數 | 同 ja | 行數、每行格數固定 |
| host UI（`text/host-ui.zh-TW.tsv`，18 列） | OpenCC | 人工翻譯 | 人工翻譯 | 說明頁 38 格 × 15 行；3× host 面板用倚天 24 點（`font/README.md`），其他語言需另定 |
| 手札（030） | OpenCC | 從英文重譯 | 同 ja | 3 頁上限、姓名三段退讓 |
| 水平選單 | OpenCC | 重譯並保留熱鍵字母 | 同 ja | 熱鍵字母可用 zh-TW 列交叉檢查（同一 key 的大寫 ASCII 集合須相同） |

音譯表來源：日本「外来語の表記」（內閣告示）與韓國「외래어 표기법」（文化體育觀光部告示）是官方規範，
但沒有現成的 ARPAbet 對照，需專案自建；兩者在各自著作權法下的地位未查證，只能當規則參考，比照 037 的做法另建表。

## 6. 規模與英文原文位置

### 6.1 zh-TW catalog（`text/*.zh-TW.tsv`，35 檔）

| 檔案 | 列數 | 譯文字數 |
|---|---:|---:|
| ecl-text | 2,542 | 43,781 |
| logbook | 142 | 13,248 |
| hmenu | 1,699 | 8,937 |
| manual | 39 | 5,446 |
| engine-fragment | 765 | 3,574 |
| translit-chars | 329 | 329 |
| monster-name | 49 | 296 |
| host-ui | 18 | 230 |
| 其餘 27 檔（選單、劇情頁、UI） | 178 | 約 1,191 |
| **合計** | **5,802** | **77,032** |

### 6.2 英文原文（只在 ignored `workplace/`）

| 檔案 | 列數 | 英文單字 | 英文字元 |
|---|---:|---:|---:|
| `workplace/ecl-l10n/source.tsv` | 2,548 | 22,198 | 124,485 |
| `workplace/logbook-l10n/source.tsv` | 64 | 7,710 | 44,702 |
| `workplace/engine-l10n/fragments.tsv` | 1,237 | 3,781 | 24,024 |
| `workplace/hmenu-l10n/source.tsv` | 1,953 | 3,276 | 18,231 |
| `workplace/item-l10n/source.tsv`、`monster-source.tsv` | 103 | 167 | 965 |

- 合計約 21 萬英文字元、3.7 萬字／語言；手冊段落與選單、劇情頁的英文不在上表（手冊英文在
  `workplace/buckrogers-original-manual-english.html`，本次未讀）。
- hmenu、fragments 的原文列數多於 zh-TW 譯文列（雜訊列未翻）。日韓應以 zh-TW 已有的 key 集合為翻譯範圍。
- ECL 有重疊切片（同一段英文被切成數列），日韓也要逐片翻、接起來通順，沿用 `workplace/ecl-l10n/INSTRUCTIONS.md` 的片段規則。
- 估計日韓各約 45 批（每批 130 列）：ECL 約 20、hmenu 約 13、fragments 約 6、手札 3、其他 3。
- 譯文進 Git：與 zh-TW 相同狀態（已是既有先例）。英文原文只在 workplace，批次輸入輸出檔也在 workplace。

## 7. kb `batch-subagent-localization.md` 與本案相關的做法

- 切批約 130 則，prep 腳本過濾不可動的列（控制碼、佔位符、雜訊）。本案另要過濾手冊題相關內容。
- **先試作一批給使用者看**，風格與尺度定案後再全面 fan-out。日文與韓文各做一次試作。
- 共用 `INSTRUCTIONS.md` 與統一詞表是降漂移的主要手段。本案現成的 `workplace/ecl-l10n/INSTRUCTIONS.md`
  寫死「只能用 Big5」「台灣繁體」，要分出 ja、ko 版本；詞表需補片假名與諺文欄。
- 用中階模型（sonnet），不用最便宜的。
- 合併時逐列核對 key 與控制碼數量，這是最後防線；再做全域一致性掃描收斂專名。
- 編碼檢查從 Big5 改成「該語言字型有字模＋字集白名單」。
- 重建後要端到端實跑，不能只看 lint。
- 平行子代理避免同名中間檔，輸出檔名帶批次號與語言。

## 8. 建議分期

| 期 | 範圍 | 退出條件 |
|---|---|---|
| 040-1 框架 | 檔名參數化（`<family>.<lang>.tsv`）、lane 結構、每 lane 字型、post-join 雜湊釘選改制、F4 前端保留與設定檔、英文模式、`LogbookTurn` 英文模式回 false、Python 工具語言參數 | 只有 zh-TW＋英文兩個選項時，現有全部收據不變；英文模式逐位元組等於原版；F4 前後 `Digest` 相同；原版 F4 用途量測完成 |
| 040-2 簡體 | OpenCC（Docker、鎖版）產生 `*.zh-CN.tsv` 並進 Git，另設人工覆寫表；名字 lint；字型子集 | 各家族載入驗證通過；抽樣 A/B |
| 040-3 日文 | 斷行禁則、`unifont_jp` 授權確認、片假名音譯器、NPC 片假名欄、批次翻譯（試作後 fan-out） | 手冊段落 504 格逐列通過；溢位計數在正常路徑為 0 |
| 040-4 韓文 | 諺文分詞斷行、空白寬度（接 039）、助詞處理、諺文音譯器、批次翻譯 | 同上 |

## 9. 風險

1. **效能**：若選「多個 LiveRuntime 並行」，CPU 約增一倍（依 phase-253 推估）。lane 設計把成本限制在 hook 命中時，但 B 類家族仍每 lane 各跑一次。
2. **重構面大**：`live_runtime.go` 1,374 行，presenter 由 `[2]` 改 `[L][2]` 會碰到所有 reset／recover 路徑，現有收據是主要防線。
3. **手冊段落溢位**：日韓可能超過 504 格單頁上限；超過就退回英文或需另定分頁規格。
4. **手冊答案外洩**：日韓手冊段落若從英文翻而保留英文單字，可能把答案字帶進 Git（Git 歷史清不掉）。
5. **韓文助詞與引擎模板**：玩家名、物品名插入模板後助詞不一致。
6. **OpenCC 詞組轉換改動專名或術語**：需覆寫表與名字 lint。
7. **字形正確性**：F2 合併字型會讓日文漢字顯示中文字形。
8. **載入失敗策略**：現行「任一 catalog 驗證失敗就中止啟動」若直接套到新語言，任何一個語言出錯都會讓整個遊戲無法啟動。

## 10. 需要使用者決定

1. 日韓模式的 NPC 與玩家名是否保留「(英文)」加註，還是只顯示片假名／諺文。
2. 某語言某列缺譯時：顯示英文（fail-open，與現行一致），還是退回繁中。
3. 某語言載入驗證失敗時：從 F4 循環移除並提示，還是中止啟動。
4. 簡體標點：保留「」或改為“”；音譯分隔符 `•` 改 `·`。
5. 說明頁與視窗標題在英文模式用哪種語言（原版無前端 UI）。
6. 語言設定是否持久化到使用者資料目錄；首次啟動預設語言（依系統語系或固定繁中）。
7. 日韓手冊段落的翻譯來源：以中文印刷手冊段落為主或以本機英文手冊為主。
8. 本機完整版的 zh-TW 是否仍用倚天（其他語言只能用 Unifont，風格會不一致）。
9. 發行包是否帶全部語言，或依語言分包（字型與 catalog 總量不大，建議全帶）。

## 11. 需要實測的證據

1. 原版對 F4（int 16h 回 AX=3E00h）的反應：主選單、探索、戰鬥、角色頁各量一次，確認 F4 可由前端保留。
2. CPU 成本：以 `-cpuprofile` 比較 1 lane 與 4 lane（或 4 個並行 runtime）在固定腳本、`-clock 50` 下的每格 CPU。
3. 啟動時間：載入並驗證 4 語言全部 catalog（手札三段退讓預排最重）。
4. 切換正確性：固定腳本在 ECL 敘事窗、水平選單、手札面板開啟、手冊題進行中四個時點各按 F4 循環一輪，
   比對每個 lane 畫面與「一開始就用該語言」的同格畫面逐位元組相同。
5. 英文模式與原版 `ScaleIndexedRGBA` 逐位元組相同；F4 前後 `owner.Digest()` 相同。
6. `unifont_jp` 授權文字與字形來源。
7. OpenCC 轉換結果的名字與術語差異清單（量出需要覆寫的列數）。
