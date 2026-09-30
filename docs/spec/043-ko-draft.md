# 043 — 韓文（ko）

狀態：**DRAFT**（2026-10-01，第一輪審查意見已併入，待第二輪）
日期：2026-10-01
Issue：#35
前置：規格 040（多語框架）、041（簡體）、042（日文，做法對齊；本規格只寫與 042 不同之處）、039（半形）、036／038（名字）、030（手札）、027–029、005／034（手冊）。
後續：044／045 日韓音譯器（各自另訂）。
證據：[phase-302](../re/phase-302-ko-translation-batches.md)（批次翻譯、檢查、收斂、稽核）；Unifont 韓文字形與排版的原始調查在 ignored 的 `workplace/ko-l10n/`。

## 1. 為什麼要做

使用者決定（2026-09-29、09-30、10-01）：F4 循環加入韓文；以英文原文為源、繁中為語境參考，子代理批次翻譯並統一詞表；敘事與手札用해라체、
直接對玩家的請求與提問用합쇼체、對白依角色；人名用韓文音譯，NEO、RAM 等組織名留英文；標示為機器輔助譯文、未經母語者校對；日韓手冊題段落從繁中段落轉譯；
缺譯顯示原版英文。2026-10-01 另定：Yes／No 用「예(Y)／노(N)」、GENNIE 用「개조인」、引號用「」『』。

本規格定義**韓文譯文資料、檢查、排版（以詞為單位換行）、字型、名字與驗收**。手冊 39 段與玩家名音譯不在本規格第一期（§3.9、§4）。

## 2. 證據

- 譯文（已證實，phase-302）：46 批、5,414 列、5,406 個不同 key、31 個家族檔，逐批 `check_done.py` 錯誤 0；合併後以 `ja_check.py` 邏輯預檢（覆蓋斷言 5,414／5,406、
  `source`、佔位符、`\n`、熱鍵、水平選單大寫與數字、拉丁字母子集、引號差、逐項寬度上限）錯誤 0，警告 142（ECL 寬度超過 zh-TW 1.6 倍）。
  用字（譯文欄加名字表韓文欄）1,130 個：韓文音節 1,057、可見 ASCII 67、「」『』`→``←` 6。ECL 寬度與繁中的比平均 1.29、第 99 百分位 1.88、最大 2.36，遠低於單頁上限 456。
  語意稽核約 3,300 列中旗標 59、採納 52 條修正；獨立審查（規格 043 第一輪）另抽 60 列對英文與繁中，語意錯誤 0。
- 字型（已證實）：發行用 `unifont_all-17.0.05.hex.gz` 有現代韓文音節 U+AC00–D7A3 共 11,172 個，**全部**是 16 寬（16x16）字模，KS X 1001 的 2,350 個常用音節包含在內；
  「」『』（U+300C–300F）16 寬；`←`（U+2190）、`→`（U+2192）只有 8 寬，由 `catalog_font.py` 置中轉 16 寬（與日文相同，zh-TW 已用）；
  `…`（U+2026）、`—`（U+2014）、`“ ”`（U+201C、U+201D）、`·`（U+00B7）同為 8 寬，程式以非 ASCII 記為 2 單位，畫面會有空隙，故譯文不用。
  `catalog_font.py build --lang ko` 連建兩次雜湊相同（審查實測 42,862 位元組）。韓文用字不含漢字，不受 Issue #36 影響。授權同 042。
- 載入器（已證實，與 042 §2 相同）：A 類家族硬比對 zh-TW 的 `source` 欄；缺家族檔即停用整個語言；只有標頭的檔可過。DebugSummary 目前對韓文印
  `語言停用=ko(缺語言檔 skill-exit-confirmation.ko.tsv)`，補齊檔案後消失。以合併檔模擬 `text/`，13 支 `--lang ko` 驗證器、story 2–9、`manual_overlay_layout.py`
  全部通過（rc=0），只有 `name_glossary.py lint` 因姓名含空白失敗（見名字一項）；`manual_catalog.py` 依規格排除。
- 排版（已證實）：`ecl_text.go` `layoutEclTextP` 的 token 規則是：名字單位（NameUnit，規格 036）是一個 token（:506–528）；連續的拉丁字母、數字與 `.` `'` `-`（`isEclLatin`，:586–588）為一個 token；
  收尾標點（`isEclClosing`）黏在前一個 token（:535–538）；其餘每個字元各為一個 token，空白也是獨立 token。因此韓文音節在詞中斷行。
  手札 `logbook.go`（:140、:199）與 `live_lane.go`（:674、:831）已把 profile 傳入同一函式。引擎片段被自動換行拆成兩列時（`engine_dispatch.go` `joinWrapped`，:429–430）：
  `layout.adjustBreak(r, k)` 只回傳新拆點，第二列是否放得下由 :430 的 `textUnits(r[k:]) > 2*n2` 判定，放不下整段回英文（:393–401）。
  以 Python 移植 `layoutEclTextP` 對合併後 ECL 2,542 列與手札 71 則實測：標準窗 76／56／40／30 單位，字級詞中斷 227／472／951／1,515 處，詞級降為 3／3／11／17 處，
  行數多 3／11／41／119 行（約 0.1% 至 2.3%）；最長詞 27 單位；手札最長 24 行，上限 57，0／71 超頁。
  `"..."` 在 ko ECL 有 72 列，其中 4 列以 `...` 開頭；`.` 同時屬於 `isEclLatin` 與 `isEclClosing`。
- 名字（已證實）：`name_glossary.py` `read_glossary`（:186）與 Go `LoadNameGlossary`（`name_glossary.go`:113）都拒絕含空白的 `chinese` 欄；`person_errors`（:569）與列級豁免檔
  `ja-name-exemptions.tsv`（:452、:571）只對 `lang == "ja"` 生效，ko 目前會靜默不跑雙向比對。韓文外國人名依外來語標記法以空白分隔名與姓（42 列中 13 個名字含空白）。
  以 zh-TW 與韓文各自的名字表雙向比對，不加例外時 5,414 列有 25 列不一致：zh-TW 有而韓文缺 2 列（`donna-conchitez`，名字只在標題）；韓文多出 23 列：`짐` 17 列
  （太陽王自稱「朕」11 列、`짐작` 2、`쓰러짐` 2、`짐보` 店名 2）、`스콧` 5 列（店名 SCOTT'S）、`아사` 1 列。執行期誤標只有 Go 讀得到的 `name-glossary-exclude.ko.tsv` 能擋。
  `nameGlossary` 的 `Matches`（Go）與 Python 掃描的語意不同（Go 有內部規則，:238–248）。
- 語言接口：`LangCycle` 與 `KnownLang` 已含 `ko`（`lang.go`:38–52），但沒有 `LangKo` 常數；`LayoutFor`（`layout_profile.go`:36–41）只認 ja；`catalog_lang.py` 的 `KNOWN_LANGS` 含 ko；
  收據工具 `-lang`、`-lang-dir`、`-lang-font` 通用。`host-ui.zh-TW.tsv` 第 26 列已有 `lang.ko`（現值「韓文」）。042 規劃的 `cmd/buckrogers-name-scan -lang` 尚未實作
  （`cmd/buckrogers-name-scan/main.go`:19–21、`name_scan.go`:34 仍是 zh-TW 與 nil profile）。

## 3. 契約

### 3.1 檔案

與規格 042 §3.1 相同，語言碼 `ko`：31 個家族檔、`manual.ko.tsv`（只有標頭）、`name-glossary.ko.tsv`、`name-glossary-exclude.ko.tsv`，合計 34 檔；
key 集合等於 zh-TW；`source` 逐列沿用 zh-TW 同 key；覆蓋斷言釘定 5,414 列、5,406 個不同 key（`character.skill.*` 8 個 key 兩檔相同）。
審閱用的 `ko-coverage-exemptions.tsv`、`ko-name-exemptions.tsv` 不進發行包。

### 3.2 風格與用語

- **語體**：敘事、手札與狀態陳述（`경험치를 얻는다.`、`센서 파괴됨`）用해라체；系統直接對玩家的請求、提問與問候（載入提示、`어떻게 하겠습니까?`、`축하합니다.`）用합쇼체；
  「」內與 NPC 的話依說話者：廣播與正式演說합쇼체；軍官簡潔命令；海盜與粗人半語；商人、酒保、店員、孩子用해요체；SCOT.DOS 與 RAM 的 AI 冷硬해라체；
  太陽王自稱「짐」、稱對方「그대들」並用하라체；沙漠跑者首領與長者用하오체；低地人的口音每則只用一兩處重複音（ㅅ→ㅆ）。
  NPC 口吻與系統提示不混：同一商人整段維持一種語體。
- **稱呼玩家隊伍**：敘事與手札能省略主語就省略；必須明示時用「당신들」（單一隊員「당신」）；NPC 客氣對白用「여러분」；軍人稱上級「지휘관님」；敵對或冷硬者「너희」；
  水平選單與 DOS 訊息不用代名詞。
- 띄어쓰기依標準正字法；助詞與詞尾黏在前詞，數字與量詞黏寫；拉丁字母詞後接名詞加一個半形空白（`NEO 요원`），後接助詞或詞尾不加（`NEO는`、`K형`）；
  助詞依拉丁字母詞的讀音尾音選（NEO→네오，RAM→램，DOS→도스）。
- 執行期插入的名字或數字之後的片段不能依尾音選助詞：用不隨尾音變化的助詞（`의`、`에게`、`에서`、`도`、`만`）或括號並列形（`은(는)`、`이(가)`、`을(를)`、`와(과)`）；
  ECL 靜態句中的名字依實際尾音選助詞。目前資料中括號並列形開頭的列約 220（`은(는)` 202、`이(가)` 9、`을(를)` 8、`와(과)` 1）。
- 標點用半形 ASCII（`. , ! ? : ; ( )`），引號用「」『』，刪節號用 `...`，不用破折號、ASCII 雙引號 `"`、`~`、`·`、全形標點與全形英數；貨幣 CR 譯「크레딧」；
  數字用半形；`Yes`／`No` 用「예(Y)」「노(N)」；GENNIE 一律「개조인」（犬類合成詞「개조견」2 列為例外）；玩家冒險日誌一律「일지」；方位 북、동、남、서。
  英文短訊息沒有句號時韓文盡量也不加，屬風格建議，不設檢查。
- 執行期在片段後接數字的標示（LAB、DECK、LEVEL、FLOOR、POD）以名詞收尾、數字放後面；靜態 ECL 句內含數字者照韓文語序。
- 引擎片段若是空白分隔項目的選單字串（例：儲存、取消、變更名字），每個項目必須是不含空白的單一詞，項目數與英文相同。
- 拉丁字母：只保留 zh-TW 該列本身保留的詞，不得新增英文單字。
- 統一用語以 `workplace/ko-l10n/glossary.ko.tsv` 為準（含英文，不進 Git）；跨批次裁決見 phase-302。

### 3.3 檢查工具

- 新增 `tools/lang_check.py`：把 `ja_check.py` 的共用邏輯抽成依語言設定的模組（設定含：語言碼、字集檔、禁用字元、列首與列尾禁則集合、不產生檔案的家族、
  列級豁免檔名、覆蓋斷言數字）；`ja_check.py` 改為薄包裝，**原名轉出** `check`、`Report`、`ROOT`、`families`、`read_catalog_raw`、`cap_for`、`load_cap_sources`
  （`test_ja_check.py` 直接使用這些名稱），命令列與測試不變。ja 硬編處（`ja_check.py` :23、:28、:40–43、:179–188、:241、:262）全部改成設定取值。
  韓文設定：`charset.ko.txt`、禁用 §3.2 所列字元、**無**列首禁則集合（標點為 ASCII，已屬 `isEclClosing`）、定行家族首尾字元只檢「不得以半形空白開頭或結尾」。
  `catalog_font.py` 本身不做字集檢查，「不在字集就失敗」由 `lang_check.py` 負責。
- 逐列檢查項目同 042 §3.3 第 1 至 11 項（寬度、名字雙向比對、合成負例全部適用）；差異與新增：
  12. **連續空白**：連續兩個以上半形空白的數量不得多於 zh-TW 同 key；zh-TW 本身有者（欄名列與手札等）依此自然通過，不另開豁免；
  13. **拉丁字母詞相鄰**：zh-TW 保留的拉丁字母詞後接韓文時，接的若不是下列助詞或詞尾開頭，必須有一個半形空白：`의 이 가 은 는 을 를 과 와 로 으로 에 에서 에게 까지 에는 에게는 에서의 들 들이 들은 들을 들에게 입니다 이며 이다 이라면 형`
     （清單放在 `lang_check.py`，測試覆蓋；實測資料中拉丁字母黏韓文 202 處、24 種前綴，助詞與讀音尾音 0 錯）；
  14. 韓文特有：不得含相容字母（U+3130–318F）、Hanja（U+4E00–9FFF）、`~`、`·`；
  15. **名字邊界審計**：名字表中的韓文名在譯文出現時，其後若緊接非助詞清單的韓文音節（例：`짐작`、`짐보`）即為錯誤，除非該處在 exclude 表；
      名字前緊接韓文音節的情形同樣報告。此項補足集合層級比對「同列已有真人又混入同形詞」的缺口（審查實測 5 列同一人物次數 ko 多於 zh-TW）。
- `tools/ko_check.sh`（Docker 內）：比照 `ja_check.sh` 逐支列出 `--lang ko` 驗證器與 story 路徑呼叫，加 `ko_charset.py --check`；不含 `manual_catalog.py`。
  `name_glossary.py lint` 需在 §3.8 修好後才納入。

### 3.4 排版（dosgolem）

韓文 layout profile 加詞級換行；預設 profile（zh-TW、zh-CN）與日文 profile 的行為逐位元組不變。

| 類別 | 規則 |
|---|---|
| 詞 token | 在 `layoutEclTextP` 內，profile 的 `word` 為真時：連續的非空白、非名字單位字元（韓文音節、拉丁字母、數字、收尾標點）合為一個 token；名字單位加其後黏著的非空白連續字（助詞）合為一個 token，放得下一列才併；`「`、`『` 設為 `noLineEnd`，沿用 `joinOpening` 與下一 token 併合 |
| 退回 | (i) 詞（或名字單位加黏著字）寬於一列時，該詞退回現行 tokenization（逐字，收尾標點仍黏前字）；(ii) 詞級排版因 `row > bottom` 失敗時，該次呼叫整體退回字級後再判定，避免原本放得下的視窗變回英文，也避免手札超過 3 頁使整個 ko 停用 |
| 引擎片段兩列拆分 | 不改 `adjustBreak(r, k)` 簽名（`layout_profile_test.go` 直接呼叫）；profile 新增 `splitRows(r, n1, n2)`：拆點落於詞中時，在第一列容量內往前找最近的空白，只在第二列仍放得下（`textUnits ≤ 2*n2`）時採用，該空白不顯示；否則維持原拆點。`joinWrapped` 呼叫它 |
| 禁則 | 不另設；`isEclClosing` 已涵蓋韓文譯文用到的 `. , ! ? : ) 」 』`；`...` 由 `.` 的雙重身分正確處理，列首的 `...` 不被拆開 |

實作位置：`layout_profile.go`（新增 ko profile、`word` 欄位、`splitRows`）、`layoutEclTextP` token 迴圈、`engine_dispatch.go` `joinWrapped`；`LayoutFor` 認 `ko`；`lang.go` 補 `LangKo`。
手札與 `EclTextWatcher` 已由 042 接 profile，不需再改。手冊逐字貪婪填列、水平選單、劇情頁不換行，詞級不適用。

三語位元組不變由機制保證：詞級分支只在 `prof != nil && prof.word` 進入，其餘路徑零改動（nil 接收者方法 `layout_profile.go`:44–51）；
另加**差分測試**：保留舊版函式副本，對全部 zh-TW、zh-CN、ja 的 ECL 與手札逐行比對新舊輸出相同。

### 3.5 載入與錯誤隔離

同 042 §3.5：A 類零失敗；B 類做 Go 靜態預檢（測試）：標準窗 76／56／40／30 單位，ECL 溢出 0、手札 ≤ 3 頁、字級對詞級的行數差與 fallback 次數報告入收據；手札頁數與標題寬度以 Go 為準。

### 3.6 半形與全形

同 042 §3.6。韓文音節 2 單位；ASCII 標點與空白 1 單位；名字加註「한글(English)」，括號內英文半形；多段名字（`벅 로저스`）在窄欄只顯示韓文。

### 3.7 字型

- 新增 `tools/ko_charset.py`（不沿用 JIS 專用的 `ja_charset.py`）產生 `font/charset.ko.txt`：可見 ASCII（U+0020–007E）∪ 現代韓文音節（U+AC00–D7A3，11,172 字，需 16 寬字模）∪ 「」『』（U+300C–300F）
  ∪ 8 寬置中箭頭 {U+2190、U+2192}；共 11,273 字。`--check` 重生後與檔案逐位元組比對。
- `font/characters.ko.txt` 由正式韓文譯文產生並進版控，必須是字集的子集；`tools/catalog_font.py --lang ko` 產生 `font/buckrogers-ko.golemfnt`，連建兩次 SHA-256 相同。
- 本機字型放 `workplace/lang-fonts/`。`font/README.md` 補 ko 段。

### 3.8 名字

- `text/name-glossary.ko.tsv`（`chinese` 欄放韓文寫法；`basis` 為 `ko-glossary`）與 `name-glossary-exclude.ko.tsv`；來源為詞表 `name` 段 42 列，名與姓以**一個半形空白**分隔。
- **Python**：`lang_name_rules("ko")` 分隔符為空白；`read_glossary` 對 ko 允許 `chinese` 內單一內部空白（拒絕首尾空白與連續空白）；`basis` 允許 `ko-glossary`；
  `person_errors` 的呼叫（:569）改為 ja 與 ko 共用，列級豁免檔名改 `f"{lang}-name-exemptions.tsv"`（:452、:571）；合成負例補 ko 版。
- **Go**：`LoadNameGlossary` 加內部 `allowSpace` 版（以語言決定），ko 允許內部單一空白，並**補拒**首尾與連續空白（現只有 Python 端檢查）；`loadNameGlossaryLang` 對 ko 傳入。
- **例外分工**：`name-glossary-exclude.ko.tsv` 是**唯一對執行期有效**的（Go 讀取），用來擋同形普通詞與稱號：`짐`（太陽王自稱，scope 用 key 樣式如 `ecl.6.97.*`、`logbook.42`、`logbook.47`）、
  `짐작`、`쓰러짐`、`짐보`、`스콧의 시푸드`；`ko-name-exemptions.tsv` 只給 Python 雙向比對用（缺名字的列與真人名的列級豁免，例：`logbook.21`、`logbook.28`、`ecl.4.64.04301`、`ecl.2.32.07797`）。
  兩表的初始清單**由 `lang_check.py` 的雙向比對與邊界審計產生**，不手寫。
- **一致性測試**：Go 的 `Matches` 與 Python 掃描對全部 ko 譯文逐列比對，差異只許來自已登記的語意分歧（Go 內部規則）。
- `cmd/buckrogers-name-scan` 與 `name_scan.go` 補 `-lang`（042 遺留）。
- 玩家名：規格 045 之前 ko 的 `PlayerNames` 停用，名字顯示英文。

### 3.9 手冊題（本期不做）

同 042 §3.9：`manual.ko.tsv` 只有標頭；手冊題提示句為韓文，段落顯示原版英文；韓文段落從繁中段落轉譯並另訂規格。

### 3.10 打包與同步

- `tools/package.sh`：`LANGS` 加 `ko`；前置檢查在現有逐語言 `if` 之後加第三個 `if`，傳同樣的 `UNIFONT_DIR`；`TEXT_EXCLUDE` 加 `ko-coverage-exemptions.tsv`、`ko-name-exemptions.tsv`。
- **`host-ui.zh-TW.tsv` 的 `lang.ko` 改為「韓文（機器輔助）」**（現有列，不是新增，新增會被 `catalog_font.py` 拒絕重複 key）：8 字均在現行 `font/characters.txt` 內，字元清單與字型不變，
  但該檔整檔 SHA-256 會變，`eten_font.py` manifest 與 `frontend/ebiten/host_font_manifest.go` 的 `verifyCurrentCatalogs` 必須重建，見 042 §3.11。
- README、`docs/release/讀我.txt`（:28、:38–42）與 `font/README.md` 更新語言章節與機器輔助說明。
- 新增 `ko_test.go`（仿 `ja_test.go`）：ko 通道載入、靜態預檢、差分測試。

### 3.11 機器輔助標示

同 042 §3.11；manifest 重建後 zh-TW 收據逐位元組不變列入驗收（§5.9）。

## 4. 不做什麼

- 韓文玩家名音譯（規格 045）、手冊段落（§3.9）、母語者校對。
- 修正 zh-TW 端的疑似錯誤（Issue #37）。
- 韓文直排或 Hanja 併記。
- 統一詞表內部的所有歧義（§6 列為開放項目）。
- 跨呼叫黏接的重新排版（見 §6）。

## 5. 驗收

1. `tools/ko_check.sh` 與 `tools/ja_check.sh`、`test_ja_check.py` 全綠（`ja_check.py` 薄包裝後原行為不變）；合成負例（含 ko 專屬的連續空白、拉丁字母相鄰、名字邊界、名字表空白規則）
   全部失敗；`ko_charset.py --check`、`catalog_font.py --lang ko` 通過。
2. 覆蓋斷言：31 個家族檔 5,414 列、5,406 個不同 key；`manual.ko.tsv` 0 列；`source` 逐列等於 zh-TW。
3. 載入：前端與收據工具載入後 ko 在 F4 循環內；DebugSummary 有 `lane[ko]`、無「語言停用=」與 `rebuilds=`，A 類載入零失敗，四時點 `skips=0`；`header_columns.py --lang ko` 無退回說明。
4. 版面：§3.4 的單元測試（詞 token、名字單位加助詞、`「` 不落行尾、長詞與溢出退回、拆點找空白、`...` 開頭）與差分測試通過；zh-TW、zh-CN、ja 的 phase254 七條回歸與既有收據逐位元組不變；
   Go 靜態預檢（§3.5）入收據。trace 重播閘門沿用 042 §5.4 的工具與通過條件；該工具完成前，043 的重播項以「報告」處理，宣稱範圍限於 §5.6 的收據。
5. 串接：依既有 trace 批量產生串接後字串，機器驗證首尾字元；抽審至少 100 條並記錄通順率。判定式：ECL 列不以終止標點（`. ! ? 」 』`）收尾的比例（現況 ko 25.4%、zh-TW 26.8%）只記錄不設門檻；
   不通順的列退回重譯。
6. 同狀態收據（2×、3×）：規格 040 §5.3 的四個時點以 `-lang ko` 輸出，記憶體與 CPU 雜湊與 zh-TW 相同；另 16 個家族時點（phase-301 的清單）機器狀態相同；截圖無缺字與溢出，列出檢視清單。
7. 語義對照：以 Issue #37 的 key 清單為分歧對照；雙語審查（獨立的非母語者模型審查者）分層抽樣至少 100 列，記錄語意忠實錯誤率與語體問題率，不設數字閘門，抽樣發現的錯誤全部修正。
8. 覆蓋表：每個家族列出證據等級（同狀態收據覆蓋、trace 重播覆蓋、只有載入與靜態驗證）；README 與讀我.txt 只對前兩級宣稱「已韓文化」。
9. 前端與打包：冷開機切到韓文截圖；說明頁「目前語言」為「韓文（機器輔助）」；打包產物含 ko 字型並通過外洩掃描；**host-ui 改動後 manifest 重建，zh-TW 收據不變**；README 與讀我.txt 含機器輔助說明。

## 6. 開放項目與消除條件

| 項目 | 消除條件 |
|---|---|
| 水平選單寬度上限（多處縮寫：`포드`、`잠금`、`관문` 等，110 列 ≥ 90% cap、32 列恰等於 cap） | 與 042 §6 第 1 項共用的 trace 量測；能借用空白者放寬並重譯 |
| 片段串接品質（動詞後置、`은(는)` 接名字） | §5.5 批量串接與抽審 |
| 跨呼叫黏接：續接呼叫的首詞（如 `은(는)`）放不下時換行，與前一呼叫末尾的名字分家；逐呼叫排版無法回頭 | 詞級不改善也不惡化；以 §5.5 抽審記錄發生率，嚴重者另訂規格 |
| 母語者校對 | 有母語者審閱後另訂規格 |
| 手冊段落、玩家名音譯 | 規格 045 與手冊另訂 |
| 詞表內部不一致（LEVEL 레벨／층、SECURITY 보안／경비、Order、Engn 기관／엔진等，phase-302 §6） | 實機串接抽審時一併看；需統一者逐項建 Issue 並重做該畫面 A/B |
| hmenu 欄名列（ko 用 9 至 11 個空白對齊英文欄，zh-TW 為 4 個） | 實機截圖確認；必要時登記 `header-columns.tsv` |
| Yes／No 「노」為外來語，非標準否定詞 | 母語者校對；寬度上限放寬後可改「아니(N)」 |
