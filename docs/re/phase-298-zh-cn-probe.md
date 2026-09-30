# 第二百九十八階段：簡體（zh-CN）OpenCC 轉換盤點與原型（規格 041 前置）

狀態：定稿（主代理審閱，2026-09-30）。使用者已定案 §12 各點：tw2sp＋專案詞表、標點維持、用語採大陸慣用、玩家名繁中音譯後逐字轉簡。

日期：2026-09-30
狀態：調查與原型（本文件已由主代理定稿）（未進主 repo；只寫 `workplace/phase298-zh-cn/`）
依據：規格 040（READY）§3.1–§3.4、phase-296、phase-297；dosgolem 分支 `buck-rogers-cht-output-overlay` HEAD `9c6abb1`（同步副本 `workplace/dosgolem-clean`）

## 結論

1. **OpenCC 官方 `tw2sp` 原樣不能直接用。** 它的台灣→大陸用語表（`TWPhrasesRev`）是資訊科技詞彙，套在本作敘事上會產生錯譯：
   「核心區」→「内核区」（35 處）、「自毀程序」→「自毁进程」、「擴音器」→「免提器」、「簡報」→「演示文稿」、
   屬性「智慧」→「智能」、「呼叫(H)」→「调用(H)」、「超控序列」→「超控串行」，還有兩類機械錯誤：
   「許多工程」斷成「多工」→「许多任务程」、「防寫保護」→「写保护保护」。原樣轉換與建議做法相比，有 **275 列**不同。
2. **建議流程：OpenCC `tw2sp` ＋ 專案詞表。** 用 OpenCC 自訂設定，在 `tw2sp` 第一段（用語）群組最前面插入一份專案詞表
   （本原型 31 條：21 條保留原詞、3 條待決保留、6 條字級、1 條修重複）。詞表是全域規則，列級覆寫只留給少數例外。
   原型輸出 `text/*.zh-CN.tsv` 以這個設定產生。
3. **版面幾乎不受影響。** 5,812 列中，寬度（規格 039 單位）改變的只有 23 列，全在 ECL、引擎片段、水平選單三個 B 類家族；
   變寬的只有 3 列（+2 單位，「呎→英尺」兩列、「檔名→文件名」一列），其餘 20 列變窄。A 類家族（選單、劇情頁、手冊、手札、
   技能、身體圖示、加入後選單與提示、動作列）與手札**逐列寬度不變**，字數也不變，所以斷行與 zh-TW 相同。
4. **執行期可以載入。** dosgolem 以 `LoadLiveRuntimeOptions` 載入 zh-CN：通過規格 040 §3.3 全部載入驗證、進入 F4 循環；
   Unifont 17.0.05 涵蓋全部 2,461 字（缺字 0）；手札 71 則頁數、名字加註層級與 zh-TW 全同。兩個既有 state 的 2× 畫面正常顯示簡體，
   記憶體與 CPU 雜湊三語言（zh-CN／zh-TW／en）相同。
5. **標點建議不轉。** OpenCC 不改「」『』•—…。改成“”‘’與「·」在 Unifont 下是半形窄字模置中於全形格，畫面上引號兩側留空、
   間隔號變寬（見 `shots/logbook-zz-variant-b.png`）。建議維持「」『』與「•」，此點需使用者決定。
6. **需要調整的 Python 驗證器有兩支。** `technical_skill_screen_catalog.py`（技能名對照中文手冊的字面釘選）與
   `skill_action_bar_catalog.py`（五則譯文的字面釘選）對 zh-CN 失敗，原因是釘的是 zh-TW 字面；其餘 19 支與 zh-TW 結果相同。

## 1. OpenCC 環境

| 項目 | 值 |
|---|---|
| 套件 | PyPI `OpenCC` 1.4.2（官方 Python 綁定，`opencc.__version__` = 1.4.2） |
| wheel | `opencc-1.4.2-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl`，SHA-256 `25c34e75fe2ab2bf5b43d89e2cf9413fbfd693c9e4851c9b7b641d50e9793f63` |
| 授權 | Apache License 2.0（wheel 內 `METADATA`：`License: Apache License 2.0`；`licenses/LICENSE` 為 Apache 2.0 全文） |
| image | `buck-phase298-opencc:1.4.2`，Id `sha256:4779be11972987cd2684fab2d5ae217b8fba6a5e2e64789188603e9185028c46`；基底 `python:3.13-slim@sha256:6771159cd4fa5d9bba1258caf0b82e6b73458c694d178ad97c5e925c2d0e1a91` |
| 建置 | wheel 只在下載步驟開網路取得；`docker build --network none`，`pip --no-index --require-hashes` |
| 設定檔 | 官方 `tw2sp.json`（SHA-256 `f8cf900c…c167d5`）；專案設定 `opencc/buckrogers-tw2sp.json`（`9a4daf13…d591c3`） |
| API | `opencc.OpenCC(config, include_tofu_risk_dictionaries=True)`、`.convert(str)`（讀 wheel 內 `opencc/__init__.py` 確認）；config 可給內建名稱或 json 絕對路徑 |

`tw2sp` 結構（讀 wheel 內 json）：正規化 `CJK_Compatibility_Ideographs` → mmseg 斷詞（`TSPhrases`）→
第一段群組 `TWPhrasesRev`／`TWVariantsRevPhrases`／`TWVariantsRev`（short_circuit）→ 第二段群組 `TSPhrases`／`TSCharactersExt`／`TSCharacters`。
各字典 SHA-256 見 `dict/sha256.txt`，文字版在 `dict/*.txt`（`opencc_dict -f ocd2 -t text` 匯出）。
`include_tofu_risk_dictionaries=False` 與預設結果逐列相同（0 列不同）。

專案設定的做法：官方 json 原樣，只在第一段群組最前面插入 `{"type": "text", "file": "…/buckrogers-phrases.txt"}`，
其內容由 `project-phrases.tsv` 產生（`make_config.py`）。專案詞條的目標值寫最終簡體，第二段對它是恆等（`make_config.py` 逐條核對，0 條不符）。

## 2. 轉換與不變量

- 35 個 `text/*.zh-TW.tsv`、5,812 列；只轉 translation 欄，key、source 原樣；另轉 `name-glossary.tsv` 的 chinese 欄為 `name-glossary.zh-CN.tsv`。
- 不變量（`convert_zh_cn.py`）：去掉漢字後的字元序列轉換前後完全相同（涵蓋 ASCII、`{0}`、`\n`、`(X)`、全形標點、•），NFC、無控制字元、
  括號數相同。原樣與專案設定兩種輸出都是 **0 違反**。`tools/catalog_font.py lint` 35 檔全數通過。
- 兩次完整重跑（`pipeline.sh`）輸出檔 SHA-256 相同。

| 指標 | 原樣 `tw2sp` | 專案設定 |
|---|---|---|
| 有變化的列 | 4,695 | 4,686 |
| 含詞組級改寫的列（逐字轉換 ≠ 整句轉換） | 540 | 369 |
| 寬度改變的列 | 25 | 23 |
| 輸出不同字數 | 2,449 | 2,444 |
| 非 GB2312 殘留字 | —、•、吋、呎、暱、牠、瞇、瞭、砲 | —、•、瞭（「瞭望」，大陸同用） |

逐家族（專案設定；詞組列一欄並列原樣數字）：

| 家族 | 列 | 有變化 | 詞組列（原樣） | 詞組列（專案） | 變寬／變窄 | 寬度差 |
|---|---|---|---|---|---|---|
| ecl-text | 2542 | 2465 | 258 | 139 | 0／1 | -4～0 |
| engine-fragment | 765 | 578 | 82 | 72 | 2／10 | -4～+2 |
| hmenu | 1699 | 1147 | 124 | 101 | 1／9 | -4～+2 |
| logbook | 142 | 135 | 40 | 27 | 0／0 | 0 |
| manual（只記數字） | 39 | 39 | 13 | 12 | 0／0 | 0 |
| translit-chars | 329 | 92 | 0 | 0 | 0／0 | 0 |
| 其餘 29 家族 | 296 | 230 | 23 | 18 | 0／0 | 0 |

完整逐列統計：`out/rows.tsv`（不含譯文）；逐家族：`out/summary.json`。原樣版本在 `out-raw/`、`text-raw/`。

## 3. 寬度與容量

- 會改寬度的只有字數改變的列；字數改變的列只有 23 列（ecl 1、engine-fragment 12、hmenu 10）。其餘 5,789 列逐字寬度序列與 zh-TW 相同
  （漢字對漢字、非漢字序列相同），ECL／手札的斷行規則只看寬度與字元類別，因此排版結果與 zh-TW 相同。
- 變寬 3 列：`frag.2260006382e7`、`hmenu.a5add1365529`（呎→英尺，2→4 單位，原文 5／4 字元）、`frag.5250b5de07b3`（8→10 單位，原文 15 字元）。
  三列仍在原文寬度內，但引擎片段與水平選單是執行期組字，是否影響整列總寬未實跑。
- 手札：Python `logbook_merge.pages` 與 Go `LoadLogbookCatalogLang` 兩邊都算，71 則全部 1 頁、最多 16 列，zh-TW 與 zh-CN 相同；
  標題最寬 17 單位（上限 76）。
- 手冊（14 列、504 格）、劇情頁（78／76 單位）、選單、欄名列：寬度不變；Go 載入先建驗證全部通過；`header_columns.py --lang zh-CN`
  3 列通過且沒有退回一般排版的列。
- 水平選單總寬、ECL 視窗容量：B 類家族不在載入時先建（phase-296 待決 6），本輪只證明逐列寬度不增（除上面 3 列），未逐視窗實跑。

## 4. 用語改寫

原樣 `tw2sp` 在非手冊家族套用了 77 個 `TWPhrasesRev` 詞條、618 處（`out-raw/terms.tsv`，前後文 `out-raw/term_contexts.tsv`）。
依前後文判斷，下列會造成錯譯或不自然，已放進 `project-phrases.tsv`：

| 繁中 | OpenCC 給 | 處數 | 問題 | 專案詞表 |
|---|---|---|---|---|
| 核心 | 内核 | 35 | 「核心區」是太空站區域 | 保留「核心」 |
| 程序 | 进程 | 9 | 自毀程序、授權程序 | 保留 |
| 擴音器／擴音 | 免提器 | 7 | 牆上廣播喇叭 | 保留 |
| 許多工程 | 许多任务程 | 2 | 斷詞錯誤（切出「多工」） | 加「許多」 |
| 簡報 | 演示文稿 | 1 | 任務簡報 | 保留 |
| 序列 | 串行 | 1 | 超控序列 | 保留 |
| 複製 | 拷贝 | 2 | 複製畫、複製本 | 保留 |
| 呼叫 | 调用 | 2 | 呼叫巡洋艦、選單「呼叫(H)」 | 保留 |
| 智慧 | 智能 | 7 | 角色屬性（Wisdom）、「智慧技能」 | 保留 |
| 執行 | 运行 | 11 | 執行任務、無法執行 | 保留 |
| 支援 | 支持 | 8 | 部隊支援、選單「支援(S)」 | 保留 |
| 整合／宣告／停用／遮蔽／連結／批次／物件 | 集成／声明／禁用／屏蔽／链接／批量／对象 | 1–5 | 敘事語意不同 | 保留 |
| 裝置 | 设备 | 62 | 爆破裝置、控制裝置大陸也用「装置」 | 保留 |
| 存檔 | 存盘 | 12 | 大陸遊戲慣用「存档」 | 「存档」 |
| 防寫保護 | 写保护保护 | 1 | 詞條與後字重疊造成重複 | 「写保护」 |
| 文件／影像／資料 | 文档／图像／数据 | 3／21／27 | 紙本文件、全息影像、資料 | **暫定保留，待使用者決定** |

字級補充（大陸規範字）：牠→它、暱→昵、瞇→眯、砲→炮、吋→寸、呎→英尺。

專案設定後仍套用的 51 個詞條（`out/terms.tsv`、前後文 `out/term_contexts.tsv` 381 處）多為合理的大陸用語：
雷射→激光、磁碟→磁盘、螢幕→屏幕、訊息→消息、通訊→通信、滑鼠→鼠标、記憶體→内存、載入→加载、儲存→保存、程式→程序、
檢視→查看、開啟→打开、感測器→传感器、掃描器→扫描仪、建立新角色→创建新角色、數位人格→数字人格 等。未逐處人工審完。

`TSPhrases` 的一對多字形判斷（計畫→计划、項鍊→项链、彷彿→仿佛、反覆→反复、甦醒→苏醒；抽查 乾隆／皇后／著名／瞭望／于先生 等不誤轉）
另列於 `out/unexplained.tsv`，都是正確轉換。

NEO、RAM 本身是半形 ASCII，不變；「新地球組織（NEO）」→「新地球组织（NEO）」、「美蘇貿易聯邦（RAM）」→「美苏贸易联邦（RAM）」。
周邊被改寫的只有「聯絡→联系」「通訊→通信」「訊息→消息」「高階→高级」。

## 5. 專名

- `name-glossary.tsv` 42 列：27 列字形改變、15 列不變（`out/names.tsv`）。整句轉換與逐字轉換結果 42 列全同，
  名錄譯名在譯文中出現的每一處轉換後都仍是同一寫法（**不一致 0 列**）。例：巴克羅吉斯→巴克罗吉斯、威瑪•狄琳→威玛•狄琳、
  何茲漢→何兹汉、傑森•杜帕→杰森•杜帕。
- 專案詞表不影響名錄（原樣與專案設定的名錄轉換結果相同）。
- 名字加註：zh-CN 通道讀 `name-glossary.zh-CN.tsv`（規格 040 §3.1 路徑），Go 載入通過；手札 71 則的本文、標題加註層級與 zh-TW 相同。

## 6. 標點

- OpenCC `tw2sp` 不改「」『』•—…（實測）。非手冊家族次數：「536、」519、…252、—87、•26、『16、』16；手冊家族另有「」各 18、…10、—4。
- 改成大陸慣例的影響（變體 B：•→·、「」→“”、『』→‘’；`text-variant-b/`）：
  - 寬度：「」→“”不變（皆 2 單位）；•→·每處 +1 單位（· 不在規格 039 半形集合），26 列變寬（ecl 14、logbook 8、monster-name 3、story-page6 1），最多 +1。
    Go 載入仍全數通過。
  - 外觀：Unifont 的 “ ” ‘ ’ · 都是 8 像素寬字模，建置時置中放進 16 像素格。畫面上引號兩側各空半格、間隔號前後留空
    （`shots/logbook-zz-variant-b.png` 對照 `shots/logbook-zz.png`）。要做成大陸排版的外觀需另建全形引號字模，屬字型工作。
- 建議：維持「」『』與「•」。

## 7. 字型

- `tools/catalog_font.py build`（全部 zh-CN 檔，含固定 ASCII）→ `font/buckrogers-zh-CN.golemfnt`，2,461 字模，
  SHA-256 `38f2be9fc13f1bd64cd55e2659d2b1611dc748b79510531164bc15d280e080a3`；字元清單 `font/characters.zh-CN.txt`
  （`56debae9…901cf1dc0`）。來源 `workplace/unifont-src/unifont_all-17.0.05.hex.gz`（`7b182454…0b5e574`）。**缺字 0**，半形墨跡檢查通過。
- 與 zh-TW 字集相比：zh-CN 有 834 字不在 zh-TW 字集，zh-TW 有 894 字不在 zh-CN 字集。
- Go 端以 `xlate.LoadFont` 逐字核對 5,812 列譯文，缺字 0。
- `host-ui`、`manual-english-panel`：規格 040 說明頁用 zh-TW 字型與文字、英文摘錄面板只在 zh-TW，這兩檔的 zh-CN 版不會被讀；原型仍產生以便比對，
  正式流程建議不產生。

## 8. 音譯（規格 037）

- `translit-chars.zh-TW.tsv` 329 字 → zh-CN 329 字，92 字改變，**無碰撞**（一對一）；逐字轉換與 `t2s` 相同。
  譯音表（290 字）與譯名表（116 字）用字都在允許字集內；zh-CN 字全在 Unifont。
- 注意：原型檔的 key 仍是 zh-TW 字的碼位（`translit.char.U+XXXX`），92 列與譯文碼位不符。
- 玩家名建議：zh-CN 仍用 zh-TW 音譯器產生繁中名，再做**字級**對映（不用詞組級）。實例：譯名表的「傑佛瑞」整句 `tw2sp` 會被改成「杰福雷」，
  逐字才是「杰佛瑞」。對映表可直接用這份 329 列檔（key＝繁中字碼位、translation＝簡體字），即 `translit-chars.zh-CN.tsv` 的語意定為
  「zh-TW 允許字 → zh-CN 字」，由正式檔機械產生、檢查一對一。
- 目前 dosgolem 非 zh-TW 通道一律 `玩家名=off(no-transliterator)`（`live_lane.go`），玩家名在 zh-CN 顯示英文；要接上需要規格 041 定義並改 Go。

## 9. Python 驗證器

以函式呼叫、與 `tools/test_*.py` 同一組共用輸入，zh-TW 用正式檔、zh-CN 用原型檔（`validators.py`，結果 `out/validators.tsv`）：

| 驗證器 | zh-TW | zh-CN |
|---|---|---|
| menu_events、gender_events、class_events、character_sheet_events、name_prompt_catalog、body_icon_catalog、career_skill_screen_catalog、save_roster_join_catalog、manual_overlay_layout、manual_catalog、story_opening_catalog、story_page2–9_catalog | 通過 | 通過 |
| technical_skill_screen_catalog | 通過 | **失敗**：`technical.screen.skills: 譯名不符中文手冊`（`MANUAL_TERMS` 字面釘選 zh-TW） |
| skill_action_bar_catalog | 通過 | **失敗**：`action.add: 譯文或 NFC 漂移`（`TEXTS` 字面釘選 zh-TW 五則） |

另：`header_columns.py --lang zh-CN --lang-dir` 通過；`catalog_font.py lint` 35 檔通過。
這兩支失敗是驗證器把 zh-TW 字面當規則，不是 zh-CN 內容錯；規格 041 要定義非 zh-TW 的對應檢查（例如「等於 zh-TW 字面經同一轉換的結果」或改驗規格 040 的動作列推導規則）。

## 10. 執行期載入與截圖

- Go 測試 `workplace/dosgolem-clean/apps/buckrogers/zh_cn_phase298_probe_test.go`（新檔，缺環境變數即 skip）：
  `LoadLiveRuntimeOptions{Langs: [zh-CN], LangDirs, LangFonts}` → `Languages()`：zh-TW、zh-CN、en 啟用，ja、ko 未載入；
  `SetLanguage("zh-CN")` 成功；DebugSummary 無停用、無 resets。變體 B 同樣通過。`gofmt -l`、`go vet ./apps/buckrogers` 無輸出。
- 收據工具只接受測試語言 zz（`-test-lang-dir`），所以把 zh-CN 檔改名 `.zz.tsv` 載入（`shots/zzcn/`），`-test-lang-font` 給 zh-CN 字型，zh-TW 用 Unifont 子集。
  runner 由 dosgolem-clean 重建（`runner`，SHA-256 `b6a624f3…0b53cd1`）。停止步數與按鍵沿用 phase-296 `switch/cases.sh`：

| 時點 | state／停止步數 | zh-CN 畫面 | 記憶體／CPU 雜湊 | en＝原版 |
|---|---|---|---|---|
| 水平選單 | `phase258-ecl-ab/g2.state`，432,500,000（e028-h432 三鍵） | `shots/hmenu-zz.png` | 三語言相同（`7290b7b3…`／`995a44ac…`） | 是 |
| 手札面板開啟 | `checkpoints/logbook41-pre.state`，5,285,000,000（e030-lb41-open 一鍵） | `shots/logbook-zz.png` | 三語言相同（`ceb6b6fc…`／`29f8055d…`） | 是 |

  兩張 zh-CN 畫面沒有缺字、斷行與 zh-TW 相同（手札第 41 則，字形與標點正常，名字加註「卡顿•特必安(Carlton Turabian)」）。
  水平選單底列「移动 查看 观察 变更 存档」；熱鍵括號內字母在這一格 zh-TW 畫面同樣是空的，屬既有狀態，本輪未查。未截手冊題畫面。

## 11. 覆寫需求與格式建議

- 原樣 `tw2sp` 需要約 275 列逐列覆寫（ecl 177、hmenu 31、logbook 31、engine-fragment 28、其他 8），而且譯文日後改動會讓覆寫失效，不建議。
- 專案詞表方式：全域規則 31 條處理掉已知問題。仍需人工審的範圍：
  - 381 處已套用的大陸用語前後文（`out/term_contexts.tsv`），預估多數合理；
  - 手冊家族 12 列含詞組級改寫（只列 key：`manual.lore.2456_now`、`manual.rules.more_on_abilities`、`manual.rules.careers`、
    `manual.world.rocketships`、`manual.world.mercury`、`manual.rules.ranged_weapons`、`manual.log.11.the_elevator`、
    `manual.log.27.bucks_speech`、`manual.log.57.acidic_victory`、`manual.log.63.alert_screen`、`manual.rules.technical_skills`、`manual.lore.2456`）；
  - 待決三詞（文件、影像、資料）。
  估計列級覆寫在 0–20 列之間（推估，未逐處審）。
- 建議檔案（進版控）：
  - `text/zh-CN-phrases.tsv`：`tw`、`cn`、`kind`（keep／phrase／char）、`reason`。產生 OpenCC 自訂設定；每條須在正式譯文中至少命中一次（避免死詞條）。
  - `text/zh-CN-overrides.tsv`：`family`、`key`、`zh_tw_sha256`（覆寫時 zh-TW 譯文的 SHA-256）、`translation`、`reason`。
    產生器在 zh-TW 譯文雜湊不符時失敗，強迫重審；覆寫後的譯文同樣要過非漢字序列不變、`(X)` 字母相同、NFC 檢查。
  - 產生器：`tools/zh_cn_convert.py`（本目錄 `convert_zh_cn.py`＋`make_config.py` 合併），固定 OpenCC 版本與字典雜湊；輸出 `text/<family>.zh-CN.tsv`
    與 `text/name-glossary.zh-CN.tsv`，重跑逐位元組相同。

## 12. 需要使用者決定

1. 用「`tw2sp`＋專案詞表」取代「`tw2sp` 原樣＋逐列覆寫」。
2. 引號：維持「」『』，或改“”‘’（需另做全形引號字模）。
3. 間隔號：維持「•」（1 單位），或改「·」（每處 +1 單位、Unifont 下兩側留空）。
4. 待決三詞：文件（→文档？）、影像（→图像？）、資料（→数据？）。
5. 其他用語偏好：存檔→存档（本原型）、載入→加载（OpenCC；大陸遊戲也常用「读取」）、儲存→保存、訊息→消息（或「信息」）。
6. 「呎→英尺」使兩列 +2 單位；可改保留「呎」。
7. 玩家名音譯是否在 zh-CN 用「zh-TW 音譯＋字級對映」（需 Go 改動與規格 041 定義）；未接上前玩家名顯示英文。
8. 手冊段落 12 列的詞組改寫由誰審（本報告不列內容）。

## 13. 未量到與風險

- 381 處用語前後文未逐一人工審；只審了會錯譯的類型。
- 水平選單整列總寬、ECL 各視窗容量未逐視窗實跑（B 類不先建）；變寬只有 3 列，風險低。
- 截圖只有兩個時點；商店、戰鬥、角色頁、劇情頁、手冊題的 zh-CN 畫面未實跑（手冊題依規定不截）。
- 前端 `buckrogers-play` 未實跑 zh-CN（需要把 zh-CN 檔與字型放進 `text/`、`font/`，本輪不得寫主 repo）。
- OpenCC 詞典改版會改變輸出：正式流程要鎖版本與字典雜湊（本目錄 `dict/sha256.txt`）。

## 14. 檔案（`workplace/phase298-zh-cn/`）

| 路徑 | 內容 |
|---|---|
| `docker/`、`build.sh`、`dl/` | Dockerfile、requirements（雜湊）、wheel |
| `run.sh`、`go.sh`、`pipeline.sh`、`pipeline.log` | Docker 包裝與完整重跑流程 |
| `project-phrases.tsv`、`make_config.py`、`opencc/` | 專案詞表與產生的 OpenCC 設定 |
| `convert_zh_cn.py` | 轉換、不變量、統計 |
| `term_audit.py`、`term_contexts.py` | 詞條歸因與前後文 |
| `validators.py` | Python 驗證器 zh-TW／zh-CN 對照 |
| `text/`（專案設定）、`text-raw/`（原樣）、`text-variant-b/`（標點變體） | zh-CN 原型譯文 |
| `out/`、`out-raw/` | `rows.tsv`、`summary.json`、`terms.tsv`、`term_rows.tsv`、`term_contexts.tsv`、`unexplained.tsv`、`names.tsv`、`validators.tsv` |
| `dict/` | OpenCC 字典文字匯出與 SHA-256 |
| `font/` | zh-CN 字型子集、字元清單、變體 B 字型 |
| `runner`、`shots/` | 收據工具與截圖（`hmenu-*.png`、`logbook-*.png`、`logbook-zz-variant-b.png`） |

dosgolem-clean 新增：`apps/buckrogers/zh_cn_phase298_probe_test.go`（未改既有檔）。自建 image：`buck-phase298-opencc:1.4.2`（保留）。
