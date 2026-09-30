# 042 — 日文（ja）

狀態：**DRAFT**（2026-09-30，第一輪兩份獨立審查的應改已併入，待第二輪）
日期：2026-09-30
Issue：#35
前置：規格 040（多語框架）、041（簡體，做法對齊）、039（半形）、036／038（名字）、030（手札）、027–029、005／034（手冊）。
後續：043 韓文、044／045 日韓音譯器（各自另訂）。
證據：[phase-300](../re/phase-300-ja-translation-batches.md)（批次翻譯、檢查、收斂、zh-TW 疑似錯誤）；
Unifont 授權與字形、ECL 禁則的原始調查在 ignored 的 `workplace/ja-l10n/survey.md`。

## 1. 為什麼要做

使用者決定（2026-09-29、09-30）：F4 循環加入日文；以英文原文為源、繁中為語境參考，子代理批次翻譯並統一詞表；
敘事與手札用常體，對白依角色，人名用片假名，NEO、RAM 等組織名留英文；標示為機器輔助譯文、未經母語者校對；
日韓手冊題段落從繁中段落轉譯；缺譯顯示原版英文。日文玩家名用片假名音譯（規格 044）。

本規格定義**日文譯文資料、檢查、排版禁則、字型、名字與驗收**。手冊 39 段與玩家名音譯不在本規格第一期（§3.9、§4）。

## 2. 證據

- 譯文（已證實，phase-300）：46 批、5,414 列、5,406 個不同 key、31 個家族檔，逐批與合併後 `check_done.py` 錯誤 0；
  用字 1,743 個，全在允許字集內。第一輪審查以獨立腳本重算：31 檔對 zh-TW 逐列比對，佔位符、`\n` 數、熱鍵序列、
  拉丁詞子集、引號差、禁用字元全部 0 不符；0 列超過逐項寬度上限。
- 字型（已證實，`workplace/ja-l10n/survey.md` 與審查重算）：發行用 `unifont_all-17.0.05.hex.gz` 的 6,356 個 JIS X 0208
  漢字與 `unifont_jp` 逐位元相同（izmg16 排在 wqy 之前）；平假名 86／86、片假名 90（含「・ー ヽヾ」共 94）皆有 16 寬字模；
  `…`（U+2026）、`—`（U+2014）、`←→` 只有 8 寬字模，由 `catalog_font.py` 置中轉 16 寬（zh-TW 已用 U+2014 共 91 處、
  `……`），兩個破折號各佔格中央 8 像素、中間有空隙；譯文實際用 U+2014，不是 U+2015。`～`（U+FF5E）、`－`（U+FF0D）不在
  允許字集。`charset.ja.txt` 含 230 個非 16 寬碼位。授權：Unifont 雙授權（OFL-1.1 與 GPL-2.0-or-later 含字型嵌入例外），
  與現行發行條件相同。
- 載入器（已證實，dosgolem `12a684b`）：A 類家族的 Go 載入器硬比對 zh-TW 的 `source` 欄值
  （`action_bar.go:77`、`skill_exit.go:71`、`post_join_exit_prompt.go:54`、`story_page7/8/9_catalog.go`）；
  `live_runtime.go:129-132` 的 `laneFamilies` 含 `manual`，`missingLaneFiles` 只 `os.Stat`，缺檔即以「缺語言檔」停用整個
  語言；只有標頭的檔可過（`lang.go` `readTSVAllowEmpty`、`manual_overlay_runtime.go` allowMissing）。
- 排版（已證實）：`ecl_text.go` 的 `layoutEclTextUnits`（:485）只有拉丁連續字不拆，`isEclClosing`（:575）只含
  `，。！？：；、」）…》』,.!?:;)`，沒有行尾禁則；手札 `logbook.go` 的 `layoutLogbookUnits`（:110，:134）逐段呼叫同一函式；
  引擎片段被自動換行拆兩列時（`engine_dispatch.go` `joinWrapped`，:406）沒有禁則。zh-TW 譯文有開括號 654 處
  （「554、（81、『16、《1）；新增的列首禁則字元在 zh-TW 與 zh-CN 譯文為 0 處。
- 語言接口（已證實）：`LangCycle` 與 `KnownLang` 已含 `ja`；收據工具 `-lang`、`-lang-dir`、`-lang-font` 通用；名字詞表與
  例外表每語言讀 `name-glossary.<lang>.tsv`、`name-glossary-exclude.<lang>.tsv`；無音譯器時 ja 走 default 分支
  （`live_lane.go:699`），`PlayerNames` 對 nil 安全；`host-ui.zh-TW.tsv` 已有 `lang.ja`。Python 工具 `catalog_lang.py` 的
  `KNOWN_LANGS` 含 ja，多數 `--lang` 工具可跑 ja；`story_*_catalog.py`、`manual_*` 只吃路徑。
- 名字（已證實，審查重算）：42 個名字在 zh-TW 有 284 個出現處，其中 278 處日文寫法一致；6 處不一致（因寬度上限縮寫
  3、SCOT.DOS 名字在前片段 1、名字只在手札標題 1、店名 1），無同人兩種拼法、無殘留漢字、無字內誤配。

## 3. 契約

### 3.1 檔案

- `text/<family>.ja.tsv`，欄位 `key`、`translation`、`source`。**`source` 逐列沿用 zh-TW 同 key 的值**（載入器與現有驗證器
  比對該值；`ja_check.py` 驗證相等）。「機器輔助」標示不放在 `source`，見 §3.11。
- 範圍：phase-300 的 31 個家族（body-icon、career-skill-screen、character-sheet、class、coordinate-line、ecl-text、
  engine-fragment、engine-template、gender、hmenu、item-word、logbook、logbook-panel、menu、monster-name、name-prompt、
  post-join-exit-prompt、post-join-menu、save-roster-join、skill-action-bar、skill-exit-confirmation、story-opening、
  story-page2–9、technical-skill-screen）加 `manual.ja.tsv`（**只有標頭、0 列**，見 §3.9）、`name-glossary.ja.tsv`、
  `name-glossary-exclude.ja.tsv`，合計 34 檔，與 zh-CN 相同。
- key 集合**等於**同家族 zh-TW 檔的 key 集合（`manual` 除外）：`ja_check.py` 對缺列與多列都失敗，例外走
  `text/ja-coverage-exemptions.tsv`（key、原因；預設空）。覆蓋斷言釘定：31 個家族檔共 5,414 列、5,406 個不同 key
  （`character.skill.*` 共 8 個 key 同屬 career-skill-screen 與 character-sheet，兩檔譯文必須相同）。
- 不產生 ja 檔的家族：`translit-chars`（規格 044）、`host-ui`（設定面板與說明頁用 zh-TW，規格 040 §3.4）、
  `manual-english-panel`（只在 zh-TW 顯示）。
- 譯文不進入比較、查找、序列化、檔案路徑或存檔（AGENTS.md）；英文原文與批次檔不進 Git。

### 3.2 風格與用語

- 敘事、手札、系統訊息用常體（だ／である）；固定請求句可用敬體；對白依說話者（軍官簡潔、海盜粗魯、學者囉唆、RAM 的
  人工智慧冷硬、低地人在さ行前加促音「っ」表現口音、太陽王自稱「余」）。SCOT.DOS 與全息影像在部分列用敬體（共 14 列），
  不強改。
- 稱呼玩家：敘事與手札「君たち」，系統提示（水平選單、DOS 訊息、介面）「あなた」。
- 數字用半形阿拉伯數字；貨幣 CR 譯「クレジット」；標點用全形「」『』、。！？：；，刪節號「……」、破折號「——」（U+2014 兩個）；
  原文單引號對白一律改「」；不用半形片假名、全形英數（U+FF10–FF19、U+FF21–FF3A、U+FF41–FF5A）、U+3000、`～`、`－`。
- 拉丁字母：只保留 zh-TW 該列本身保留的詞（NEO、RAM、ECG、DOS、PgDn 等），不得新增英文單字；拉丁字母前後的空白位置
  與 zh-TW 該列相同（例：版本字串），不另加或刪。
- 玩家冒險日誌（繁中「手札」）稱「日誌」，編號「日誌n番」；裝置紀錄稱「記録」；「手札」在日文指手牌，不用。
- 統一用語以 `workplace/ja-l10n/glossary.ja.tsv` 為準（含英文，不進 Git）；跨批次已裁決的用語見 phase-300 §4。

### 3.3 檢查工具 `tools/ja_check.py` 與 `tools/ja_check.sh`

phase-300 的 `check_done.py` 依賴英文與批次檔，不進 Git。進 Git 的檢查改以 zh-TW 與事件檔為基準，逐列驗證：

1. 結構：key 屬同家族 zh-TW 且集合相等（§3.1）；`source` 等於 zh-TW 同 key；NFC；無 tab、換行、控制字元、BOM、CRLF；
   非空；無重複 key；順序同 zh-TW。跨檔共用 key 譯文一致。
2. 佔位符 `{n}` 的多重集合與 zh-TW 相同；`\n`（兩字元）數量與 zh-TW 相同。
3. 熱鍵：`(X)` 的**個數與字母序列**與 zh-TW 相同（水平選單有 20 列 zh-TW 本身含 2 至 6 個 `(X)`）；水平選單列的大寫 ASCII
   與數字集合與 zh-TW 相同。
4. 拉丁字母：先移除 `\n` 再取詞，日文列的拉丁詞集合是 zh-TW 該列的子集；zh-TW 無拉丁字母的列，日文亦無。（此項同時是
   「日文不含英文原文」的保證，外洩掃描 `leak_scan.py` 只比對檔案雜湊與檔名，不看文字內容。）
5. 寬度（半形 1 單位、其餘 2 單位）：以 Go 的實際檢查為準，Python 與 Go 的常數以單元測試互鎖。依家族：

   | 家族 | 上限與來源 |
   |---|---|
   | hmenu | 逐項 `max(2×original_length, zh-TW 寬)`（`hmenu-item-events.tsv`，經驗上限：日文有 47 列大於 2n、皆不超過 zh-TW）；硬限制是整列總和 ≤ `2×(40−起始欄)`（`hmenu.go`，起始欄為執行期值），由 §5.4 的重播判定 |
   | engine-fragment、item-word、monster-name | `2×original_length`；引擎片段實際檢查整個 dispatch 字串 2n（`engine_dispatch.go:390`），換行拆兩列時為 2×n1、2×n2（:421-424，n1、n2 不在 events），由 §3.5 的 harness 判定 |
   | character-sheet、menu、skill-action-bar 等 | 安全矩形 `capacity_cells×2` |
   | 劇情開場與 2 至 7 頁 | 每列 78；第 8 頁 76（`story_page8_overlay.go:39`）；第 9 頁 40（`story_page9_overlay.go:33`） |
   | skill-exit-confirmation | 264／272 像素（`skill_exit_overlay.go:33-37` 常數） |
   | post-join-exit-prompt | 12／30 格；post-join-menu 用 events `original_length`（`post_join_menu.go:340`） |
   | logbook | 每則排版 ≤ 3 頁（Go `LoadLogbookCatalogLang` 為準，含名字單位與禁則）、標題 ≤ 76 單位；`logbook-panel` 標題 76 |
   | coordinate-line | 恰一字 |
   | ecl-text | 視窗寬為執行期值（`ecl_text.go:376`）；靜態上界 456，警告：超過 zh-TW 1.6 倍 |
   | engine-template | 執行期組合，靜態只驗佔位符 |

   超過上限為錯誤（ECL 的 1.6 倍為警告）。
6. 字集：全部字元屬 `font/characters.ja.txt`，且不含 §3.2 的禁用字元。
7. 引號：每列「開引號數減關引號數」與 zh-TW 相同。
8. 名字：每列出現的名字寫法與 `name-glossary.ja.tsv` 一致，**錯誤**（不是警告）；行級豁免走 `name-glossary-exclude.ja.tsv`（§3.8）。
9. 定行家族（水平選單不換行、劇情頁每 key 一列）的首尾字元：不得以 §3.4 的列首禁則字元開頭、以開括號結尾（禁則只在單一
   呼叫內生效；引擎片段有 15 列、ECL 有 4 列以「、。：？……」開頭屬跨呼叫接續，不在此限）。
10. 欄名列：`header-columns.tsv` 列出的欄名列，日文為單空白分隔、token 數等於 `cols`（連續空白會使 `anchorColumns` 失敗並退回一般排版）；
    `header_columns.py --lang ja` 不得印退回說明。
11. 合成負例測試（必做）：source 不符、佔位符缺失、熱鍵字母或個數不符、多出拉丁字母詞、超寬、字集外字、引號不平衡、
    名字寫法不一致、key 不在 zh-TW 或缺列、`\n` 數量不符、跨檔共用 key 不一致、欄名列連續空白、定行家族首尾字元違規。

`tools/ja_check.sh`（Docker 內，比照 `zh_cn_check.sh`）逐支明列現有 `--lang ja` 驗證器：menu_events、gender_events、
class_events、character_sheet_events、name_prompt_catalog、body_icon_catalog、career_skill_screen_catalog、
save_roster_join_catalog、technical_skill_screen_catalog、skill_action_bar_catalog、header_columns、name_glossary（lint）、
catalog_font（lint）；以路徑呼叫 story_opening_catalog、story_page2–9_catalog、manual_catalog、manual_overlay_layout。
`technical_skill_screen_catalog.py` 與 `skill_action_bar_catalog.py`：ja 只查結構與 `(X)` 字母（規格 041 §3.7 交給本規格）。
`tools/package.sh` 的語言清單與前置檢查改為依 `LANGS` 迴圈（現行硬綁 zh-CN）。

### 3.4 排版禁則（dosgolem）

每語言一份排版設定（layout profile），注入點在載入語言時（`live_lane.go` 設定名字處旁）；預設值等於現行行為，
zh-TW 與 zh-CN 不變（phase254 逐位元組相同）。**行尾禁則對 zh-TW 與 zh-CN 預設關閉**（zh-TW 有 654 處開括號）。日文設定：

| 類別 | 規則 |
|---|---|
| 不放列首 | 小書き假名（ぁぃぅぇぉっゃゅょゎゕゖ ァィゥェォッャュョヮヵヶ）、長音符「ー」、反覆記號（ゝゞヽヾ々〻）、中黑「・」、閉括號補齊（】〕］｝〉〙〗’”）、全形句點「．」，併入 `isEclClosing` 的語言集合 |
| 不放列尾 | 開括號（「『（【〔［｛〈《‘“）與其後的 token 合為一個 token |
| 不拆 | 連續的「……」「——」當一個 token，且不放列首 |
| 引擎片段兩列拆分 | `joinWrapped` 的拆點套用同一組列首與列尾禁則；拆點後第二列超過 2×n2 即整段回英文，成功率須量（§5.4） |

tokenization：開括號、其後的拉丁連續字或名字單位、尾隨閉括號合為一個 token；token 超過一列寬時仍只在名字加註的英文空白拆，
開括號跟著第一段（現有 `layoutEclTextUnits` 的 `units[u].Start==i` 與「Never run into the next unit」假設 token 不跨進名字單位，
需改寫）。拉丁連續字與半形數字維持不拆；名字加註單位（規格 036）維持現行。

需改的程式：`isEclClosing`、`layoutEclTextUnits`、`layoutEclText` 與其呼叫點（`ecl_text.go:376`、:394、:405）、`EclTextWatcher`
加 profile 欄位、`layoutLogbookUnits`（`logbook.go:110`、:134）、`joinWrapped` 與 `EngineDispatchWatcher` 欄位
（`live_lane.go:829`）、`name_scan.go` 與 `cmd/buckrogers-name-scan`（加 `-lang`，現只讀 zh-TW 名字表）、直呼上述函式的 8 處測試。
手冊逐字貪婪填列（`manualRows`）與水平選單、劇情頁不換行，禁則不適用；手冊日文於 §3.9 另訂。

### 3.5 載入與錯誤隔離

- 語言碼 `ja`；載入驗證、錯誤隔離、缺譯粒度依規格 040 §3.3；字型檔 `font/buckrogers-ja.golemfnt`。
- **A 類**（選單、劇情頁、動作列、技能離開、加入後提示與選單、身體圖示等）：`loadLane` 逐語言逐倍率建 presenter 內容，
  驗收要求零失敗。
- **B 類**（ECL、水平選單、引擎片段，共 5,117 列）：載入只做結構檢查，缺字與溢出到執行期 sync 才丟頁。因此驗收另設
  「Go 靜態 harness」：對全部 B 類列以 ja 字型與 §3.4 的 layout profile 跑版面，`Overflows=0`、缺字 0；失敗列退回翻譯者重譯，
  不以放寬檢查處理。
- 手札：`LoadLogbookCatalogLang` 任一則排不進 3 頁或標題超寬，整個 ja 失效，故手札頁數與標題寬度以 Go 為準。
- 動作列：每則譯文含恰好一個 `(X)`，字母等於 zh-TW（規格 040 §3.1）；加入後選單 7 項為一組，可為 0 或 7 列。

### 3.6 半形與全形

- 規格 039 的半形 ASCII 適用日文；日文間隔號「・」（U+30FB）佔 2 單位，比繁中 `•` 多 1 單位，不做半格處理。
- 名字加註「カタカナ(English)」：括號內英文半形；多段名字（例：「バック・ロジャーズ」）在窄欄只顯示片假名。

### 3.7 字型

- `tools/ja_charset.py` 從 `unifont_all-17.0.05.hex.gz` 產生允許字集 `font/charset.ja.txt`（可見 ASCII、JIS X 0208 中 Unifont
  有 16 寬字模者、U+2014 與 U+2026 等已知 8 寬置中字元；不含全形英數與 U+3000）並進版控；`--check` 重生後 `cmp`。
- `font/characters.ja.txt` 由正式日文譯文產生並進版控（可見 ASCII 加譯文用字，預計約 1,750 字），必須是
  `charset.ja.txt` 的子集；`tools/catalog_font.py --lang ja` 對不在字集的字失敗（不靜默置中轉寬）。
- `tools/catalog_font.py --lang ja` 從 `unifont_all-17.0.05.hex.gz` 產生 `font/buckrogers-ja.golemfnt`（JIS 漢字為日文字形，
  與現行來源相同，不另引入 `unifont_jp`）；連建兩次 SHA-256 相同；授權檔隨發行包（`OFL-1.1.txt`、`COPYING`）不變。
- 本機字型放 `workplace/lang-fonts/`（規格 041 §3.7）。倚天字型缺假名與日文漢字，不用於日文。

### 3.8 名字

- `text/name-glossary.ja.tsv`（欄位同 `name-glossary.tsv`，`chinese` 欄改放片假名寫法；`basis` 記 `ja-glossary`；`note` 補
  `old=`）與 `text/name-glossary-exclude.ja.tsv`。來源為詞表 `name` 段 42 列，名與姓之間用「・」（U+30FB）。
- `tools/name_glossary.py` 需改：分隔號與 `basis` 允許值改為每語言設定（現行寫死 U+2022 與 `printed:`／`xinhua`／`nickname`）；
  lint 新增「寫法一致」為錯誤；例外表 `scope` 欄支援精確 key。
- 行級豁免（`name-glossary-exclude.ja.tsv`，附原因）至少含：店名（ジンボのロケット・バー、スコッツ・シーフード、スコッツ）；
  水平選單因寬度上限縮寫的名字（`hmenu.1d54d5514269`、`hmenu.34efb50db494`、`hmenu.a4da3f4fffd1`）；名字只在標題或在前一片段的
  列（`logbook.21`、`ecl.5.83.00246`）。§6 第 1 項若放寬 cap，縮寫改回正式寫法後移除對應豁免。
- 玩家名：規格 044 之前 ja 的 `PlayerNames` 停用，名字顯示英文（`no-transliterator`），不讓語言失效。

### 3.9 手冊題（本期不做）

- 手冊 39 段（`manual.ja.tsv`）另訂：從繁中段落轉譯，504 格單頁，不得含拉丁字母（防答案外洩），並保存題目證據、繁中段落
  來源與收據（AGENTS.md）。本期 `manual.ja.tsv` 只有標頭，ja 模式手冊題缺譯，顯示原版英文（規格 040 缺譯粒度：手冊以段落為單位）。
- 手冊題提示句（引擎片段中「日誌の第Nページ、見出し…」）已翻譯，語意不含答案。

### 3.10 打包與同步

- `tools/package.sh` 語言清單加 `ja` 並依 `LANGS` 迴圈；前置檢查執行 `tools/ja_check.sh`（失敗即中止）；打包內容加
  `font/buckrogers-ja.golemfnt` 與 34 個 ja 檔；發行包約增加 3 至 4%。
- 修改任何 `*.zh-TW.tsv` 使 ja 的 key 集合、佔位符或熱鍵失效時，`ja_check.py` 失敗（key 集合相等，§3.1），遺漏由打包前置檢查擋下。
  日文內容本身不隨 zh-TW 自動更新。

### 3.11 機器輔助標示

- `host-ui.zh-TW.tsv` 的 `lang.ja` 改為「日文（機器輔助）」（8 字，用字均在現行 `font/characters.txt` 內；說明頁每行上限 38）；
  README 與 `docs/release/讀我.txt` 說明日文為機器輔助譯文、未經母語者校對。驗收 §5.7 檢查。

## 4. 不做什麼

- 韓文（043）、日韓音譯器（044／045）、手冊段落（§3.9）、母語者校對、母語者風格重寫。
- 修正 zh-TW 端的疑似錯誤（phase-300 §5，另案）與 Unifont 對繁中與簡體的日文字形問題（Issue #36）。
- 標點改直排、旁白時態統一、依性別的代名詞處理（日文不分性別，性別片段以中性譯法為準）。

## 5. 驗收

1. `tools/ja_check.sh` 全綠（§3.3 的 ja_check.py 與逐支驗證器）；合成負例全部失敗；`ja_charset.py --check`、`catalog_font.py` lint 通過。
2. 覆蓋斷言：31 個家族檔 5,414 列、5,406 個不同 key，key 集合等於 zh-TW；`manual.ja.tsv` 0 列；`source` 逐列等於 zh-TW。
3. 載入：前端與收據工具載入後 ja 在 F4 循環內；DebugSummary 有 `lane[ja]`、無「語言停用=」與 `rebuilds=`，A 類載入零失敗，
   四時點 `skips=0`；`header_columns.py --lang ja` 無退回說明。
4. 版面：§3.4 禁則的單元測試（列首、列尾、成對符號、名字單位、引擎片段兩列拆分）通過；Go 靜態 harness 對 B 類全部列
   `Overflows=0`、缺字 0（報告加禁則前後的溢出頁數變化，並量 `joinWrapped` 成功率）；重播已捕捉的水平選單呼叫，整列 `Overflows=0`。
   zh-TW 與 zh-CN 的 phase254 七條回歸與 phase-299 收據逐位元組不變。
5. 串接：依既有 trace 批量產生實際串接後的字串（ECL、引擎片段、水平選單），機器驗證首尾字元與 `Misses=0`；抽審至少 100 條並記錄
   通順率（ja 以助詞、逗號或冒號收尾的 ECL 列有 344／2,542，zh-TW 約 6.5%）。抽審含動詞後置片段與名字夾在片段之間。
6. 同狀態收據（2×、3×）：規格 040 §5.3 的四個時點以 `-lang ja` 輸出，記憶體與 CPU 雜湊與 zh-TW 相同；ECL、水平選單、手札、
   劇情頁截圖無缺字與溢出，截圖列出檢視清單（家族、key、結果）。真實路徑各一條並寫明 state 檔與腳本：動詞後置片段、引擎片段、
   名字加註、手札。
7. 語義分歧對照：phase-300 §5 的「與 zh-TW 分歧清單」（手札約 30 則、三個已證實的 zh-TW 錯誤列）作為 A/B 對照；加雙語審查抽樣，
   記錄語意忠實錯誤率；錯誤率門檻由抽樣結果與使用者定案。
8. 前端與打包：冷開機切到日文截圖；說明頁「目前語言」為「日文（機器輔助）」；打包產物含 ja 字型並通過外洩掃描；README 與讀我.txt 含機器輔助說明。

## 6. 開放項目與消除條件

| 項目 | 消除條件 |
|---|---|
| 水平選單寬度上限（226 列 ≥ 90%、120 列 > 95%；數十處縮寫成非正確譯名，例：主角名、艦名、部分技能名） | 用既有執行期 trace 取整列文字，量每項右側可借用的空白；能借用者放寬並重譯、移除名字豁免，不能者維持 |
| 片段串接品質（review-notes 涉及約 175 個完整 key 加 107 個短位移） | §5.5 批量串接與抽審；發現不通順者退回重譯 |
| 母語者校對 | 有母語者審閱後另訂規格；在此之前維持機器輔助標示 |
| 手冊段落 | §3.9 另訂規格 |
| 玩家名音譯 | 規格 044 |
| zh-TW 疑似錯誤 | phase-300 §5 另案修正並重做該畫面 A/B，日文不受影響 |
| 破折號觀感（U+2014 兩個各佔格中央，中間有空隙） | §5.6 截圖檢查；不理想時另訂替代字元 |
