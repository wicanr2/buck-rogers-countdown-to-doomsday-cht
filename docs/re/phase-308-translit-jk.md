# 第三百零八階段：日文與韓文玩家名音譯（規格 044、045）

日期：2026-10-01
狀態：規格 044、045 的實作與第一版證據。dosgolem `2d00b50`（匯出共用前端）、`02857eb`（`xlate/translitjk`）、`1b8b303`（接線與韓文續接空白）、`8f9b403`（發行包冒煙）、`8923d67`（載入成本紀錄）、`65333e2`（審查後的兩處規則修正）；單元測試、全字典不變式、兩位獨立審查、離線重播、前後對照 104 個時點、phase254 七條回歸、`package.sh linux` 完成。
推論等級：**已證實**＝重跑測試或腳本並比對輸出；**強推論**＝由程式或截圖推得、未實跑；**未知**＝未量。
原版遊戲與英文原文只在 ignored 的 `workplace/`，本文只記數字、key 與判定。

## 1. 實作內容（已證實）

| 項目 | 內容 | 位置 |
|---|---|---|
| 共用前端匯出 | `Phone`、`ParsePron`、`SpellingPhones`、`AlignVowels`、`SharedCMU`（互斥鎖加每條目 `sync.Once`，四個語言通道同一進程只解析一次詞典）；zh 的輸出不變 | dosgolem `xlate/translit/export.go` |
| 音節化 | F1 至 F8：`ER` 後接元音補 `R`、元音與字母對齊、單一聲母、`C+Y+V`、元音後 `R` 併入、詞尾 `TS`／`DZ`、無元音字 `ok=false` | `xlate/translitjk/front.go` |
| 日文後端 | J1 至 J9；`jaClean`（J8）是安全網，全字典 117,493 詞改動 0 詞 | `ja.go` |
| 韓文後端 | K1 至 K10，音節以 Unicode 算式合成；允許字集 2,128 個預組音節 | `ko.go` |
| 載入與查找 | `Load(textDir, lang)`、`Transliterate`、`TransliterateTrace`（規則編號）、`Rules()`、`Allowed()`、`WithRuleOnly()`、`FromPhones()`；查找順序 dict、cmudict、spelling | `translitjk.go` |
| 接線 | `live_lane.go` 的 `case LangJa, LangKo`：`translitjk.Load` 成功後做載入期字型檢查（缺字：`translit-font: 缺 U+XXXX 等 N 字`），失敗只關玩家名（`translit-<lang>: <錯誤>`），語言通道與其他語言不受影響 | `apps/buckrogers/live_lane.go` |
| 韓文續接空白 | 玩家名版面選擇抽成 `layoutPlayerName`；欠空白時依規格 045 §3.4 的次序先試含空白，`SpaceDropped` 照舊計 | `ecl_text.go` |
| 資料 | `text/translit-ja-names.tsv`、`translit-ko-names.tsv`（各 86 列，`basis` 為 `machine-reviewed`）、`text/translit-chars.ja.tsv`（88 字）、`translit-chars.ko.tsv`（2,128 字） | Buck repo `text/` |
| 字型 | `font/characters.ja.txt` 1,770→1,780 字（多 `ゾ ヂ ヅ ヌ ヮ ヰ ヱ ヲ ヵ ヶ`）、`characters.ko.txt` 1,159→2,523 字（多 1,364 個音節）；本機字型 ja 65,469→65,839 位元組、ko 42,862→93,330 位元組 | `font/`、`workplace/lang-fonts/` |
| 工具 | `tools/translit_jk.py`（`chars`、`lint`、`verify-fixed`、`examples --check`）、`lang_check.py` 的 `NON_CATALOG_PREFIX` 加 `translit-chars`、`translit.py --lang` 限 zh-TW、`ja_check.sh`／`ko_check.sh` 加四步與 `test_translit_jk.py` | `tools/` |
| 打包 | `package.sh` 複製 `text/cmudict/` 與 `LICENSE-translit-table.md`、前置檢查、字型迴圈後的 `TestPackagedLanes` 冒煙；`THIRD-PARTY.md` 加 CMU 發音詞典與英語人名譯音表；`讀我.txt`、`README.md`、`font/README.md` 同步 | `tools/package.sh`、`tools/release/third_party.py` |

## 2. 單元測試與不變式（已證實）

| 測試 | 保證 |
|---|---|
| `TestFullDictionaryInvariants`（`BUCKROGERS_CHT_ROOT` 閘控） | 全部 117,493 個純字母詞（第一個讀音、規則模式）：`ok=false` 恰為 26 個單字母詞加 `FS HM HMM HMMM MM SH SHH THS`，其餘全部成功；輸出每字在允許字集內、ja 詞首無 `ッ ー ン` 且無 `ーー ンー ーッ`、ko 無單獨 Jamo；`TransliterateTrace` 與 `Transliterate` 逐詞相同、性別不影響；違反 0 |
| `TestFixedNames`、`TestFixedNamesAgainstBuck` | 固定名單 ja 60 列、ko 57 列（dict 8、cmudict 33／30、spelling 12、none 7）逐列比對輸出、tier、規則編號；testdata 的 text 副本、三種表與 CMUdict 子集（206 行，全是完整詞典的原樣行）與 Buck repo 逐位元相同，並由目前的資料重算候選名單；缺 `BUCKROGERS_CHT_ROOT` 時 skip 並印原因 |
| `TestRuleCoverage` | 固定名單、規則回歸表、`FromPhones` 音素表三者命中編號的聯集等於 `Rules()`（ja 90 條、ko 58 條）；池內（名字表單字）沒有的 ja 28 條、ko 12 條由 28 列音素表涵蓋；全字典沒有命中零的編號 |
| `TestSpecExamples` | 例子表 ja 49 列、ko 51 列在規則模式逐列比對；`!` 規則不得命中；idiom 列（ja 4、ko 5）斷言規則輸出與慣用寫法不同 |
| `TestFromPhones`、`TestDictionaryNames`、`TestLoadErrors`、`TestAllowedSet`、`TestBoundaryNames`、`TestOutputOutsideAllowedSet`、`TestRuleOnlyIsolation`、`TestConcurrentLoad` | 音素表、詞典名在兩種模式的輸出、`Load` 的九種負例與空白規則、`Allowed()` 升冪、邊界輸入、允許字集外的輸出整名 `ok=false`、規則模式不改原物件、兩個 goroutine 同時 `Load` 得同一份對照表（`-race`） |
| `TestJkPlayerNamesOnFormalText`、`TestJkMissingFileDisablesOnlyPlayerNames`、`TestJkFontMissingGlyphDisablesPlayerNames` | 正式資料的 ja、ko 通道玩家名啟用；缺詞典只關該語言的玩家名；缺一個只有音譯會用到的字模時玩家名停用並回報 `translit-font` |
| `TestPackagedLanes` | 以發行包形式的 `text/` 與 `font/` 載入四個通道，玩家名全啟用、每個通道對 `NICOLE STEELE` 有結果；負對照（移除 `text/cmudict/`）四個通道都回報玩家名停用，證實規格 044 §3.7 推論的發行包缺口 |
| `TestEclPlayerNameSpace*`、`TestLayoutPlayerNameOrder` | 韓文欠空白時六個嘗試次序與 `SpaceDropped`、`DOE` 型只譯名恰為助詞字串仍補空白、左欄換列與新頁不補、zh-TW、ja、`layoutKoChars` 不補 |
| `TestLayoutPlayerNameMatchesPre045WithoutSpace` | 規格 045 之前的玩家名版面選擇區塊（逐字複製的凍結副本）與新函式在無欠空白時，對四種 profile、八個名字、五個視窗、全部游標位置共 18,528 組輸入逐位相同 |
| `test_translit_jk.py`（19）、`test_lang_check.py`（22，新增「音譯檔不是家族」）、`test_translit.py`（12，新增 `--lang` 限制） | 工具的真實資料護欄與合成負例（允許字集外的字、重複 `english`、`basis` 白名單、`english` 集合、ja 空白、ko 首尾與連續空白、pending 與審查格式、副本雜湊、例子表欄位）；負對照：把 `NON_CATALOG_PREFIX` 改回舊值，`test_lang_check.py` 失敗 |

dosgolem `apps/buckrogers` 與 `xlate/...` 全套在 Docker 內以完整環境執行：全過，排除既有的兩個字型雜湊失效測試（`TestScopedMenuRuntime*`，phase-305 §8）與未追蹤的 `TestCommandStatus*` 探針檔。

## 3. 兩位獨立審查與規則修正（已證實）

審查者 A（規則符合性）以規格逐字手推 cmudict 層的全部列，審查者 B（語音合理性）看輸出是否讀得回原名；兩人互相看不到對方報告，報告在 ignored 的 `workplace/phase308-review/{A,B}.md`。

| 結果 | ja | ko |
|---|---|---|
| A：手推與名單一致 | 59／60，1 列有疑慮（`PHILLIPS`，J6(b) 兩種讀法） | 57／57 |
| B：錯 | 0 | 2（`MARIE` 得 머리，同 `Murray` 的慣用譯名；`ANNE MARIE SMITH` 同一缺陷） |
| B：可議 | 5（`PHILLIPS`、`BEOWULF`、`CARLOS`、`DEERING`、`WILHELMINA-ROSE`） | 7（`O'BRIEN`、`POWELL`、`BEOWULF`、`EXIT`、`CARLOS`、`JANELLE`、`DEERING`） |
| A 指出的規格含糊處 | 5 項：J6(b) 範圍、F2 拆組細節、K2「詞尾」、K5 的「前一音節」、J3 的「字母」；固定名單內沒有任何列因此得到不同結果 |  |

修了兩處規則（兩處都有 A 與 B 的共同依據；規格 044 §3.4 J6(b)、規格 045 §3.2 K2 加修訂註）：

- ja J6(b)：改為詞尾輔音串的第一個輔音為 `K P T D`，或詞尾 `TS`、`DZ`（比照 (a)）。`Phillips` フィリプス 變 フィリップス；全字典 J6(b) 命中 6,132 詞，其中 562 詞是舊讀法不會命中的。
- ko K2：F1 由 `ER0` 改成的 `AH0`、其後元音有重音、字母為 a 時取ㅏ，`Marie` 마리、`Maria` 마리아。第一版曾不加「其後元音有重音」，結果 `Margaret` 變 마가릿、`Barbara` 變 바바라（規則回歸表的比對抓到），所以加上這個條件；全字典 481 詞受影響。

其餘 B 的意見（雙元音拆音節後接無重音元音、無重音 `IH` 恆為ㅣ、含 `x` 取第一讀音、西葡語系的 `AA R` 加輔音、`Deering` 缺 /ɪə/ 後半、詞典 `JANELLE` 저넬 的首音節）不改規則，記入規格 044、045 §6，並以 idiom 例子列（規則輸出與慣用寫法不同）釘住。`review` 欄 `ok:agentA,agentB` 表示兩位審查者都看過該列，B 判可議的列不擋入庫；`PHILLIPS` 與 `MARIE` 兩列審查後才改，新值就是 B 建議的寫法。

審查前自己寫音素表時，對照規格 J3（字母為 u 的無重音 `AH` 加小字 `ュ`）發現 `jaPal` 的該分支漏掉小字（`Regular` 規格要求 レギュラー，程式會得 レギラー），當場修好；這是實作缺陷，不是規格修訂。

## 4. 前後對照收據（已證實）

舊：dosgolem `43a1e27`（規格 047）的 runner、現行 `text/`、規格 047 時的 ja、ko 字型；新：現行 runner（`65333e2`）、現行 `text/`、重建後的字型；`noplayer`：現行 runner，`text/` 缺 `translit-ja-names.tsv` 與 `translit-ko-names.tsv`（玩家名停用的測試開關）。同一狀態、同一組按鍵，104 個時點：五個時點（ecl、hmenu、logbook、manual、join）× {zh-TW、zh-CN、ja、ko} × 2×、3× 共 40，加 16 個家族時點 × 四個語言（2×）共 64。`ab-compare.py`：

| 結果 | 數字 |
|---|---|
| 機器狀態（記憶體、CPU、indexed、palette、停止步數）三版相同 | 104／104 |
| menu 畫面三版相同 | 104／104 |
| `noplayer` 與舊版 live 畫面逐位元相同 | 104／104（證明改動沒有波及名字以外的格） |
| 新舊 live 畫面相同 | 94；zh-TW、zh-CN 全部相同 |
| 新舊畫面不同 | 10：ja 5、ko 5（ecl 時點 2×、3× 各一，opening-275、-2809、-282 三個家族時點） |
| 失敗 | 0 |

十個不同的時點相異像素全落在欄 17 至 29、列 5 至 9（探索隊伍欄，ja 39 格、ko 38 格）。隊伍欄只顯示譯名（規格 038 §3.4）：ja 為 セレスト、ピエール、ニコール・スティール、ローク、ジャネル，ko 為 설레스트、피에르、니콜 스틸、로크、저넬（目視 ignored 的 `workplace/phase308/png/crop-{ja,ko}.png`）。現有狀態的玩家名只有這六個；固定名單的其餘名字只由單元測試驗收。en 沒有覆繪，不在收據內。第一輪（runner `8f9b403`，規則修正前）與第二輪（`65333e2`）結果相同，因為這六個名字的輸出沒有受兩處修正影響。

## 5. 離線重播與 phase254 回歸（已證實）

- phase257 trace 重播（W 3,886、H 361、D 12,975）：五份輸出（畫面層、引擎呼叫、`ecl` 紀錄、引擎翻譯、報告）與規格 047 的基準 `post047-1` 逐位元組相同；四個語言的 `ecl` 列 `dPlayer` 合計 0、`dSpaceDropped` 合計 0（重播紀錄沒有隊伍快照，玩家名路徑不可達，所以降段分布無可列）。ECL 溢出 0、缺字 0。
- phase254 七條回歸（`rerun41`，新 runner `65333e2`、現行 `text/`、腳本取自 `rerun40` 目錄）：七份文字輸出（action、body、manual、opening、post、skill、story，行數 10、6、8、6、8、8、6）與 `rerun40` 逐位元組相同，live 與 runner 組合畫面皆為 `same`。
- 載入成本（只記錄，不設門檻；機器負載平均約 15 至 22，數字偏高且有雜訊）：zh-TW 單語 `LoadLiveRuntimeOptions` 1.26 秒、HeapAlloc 增加 39.6 MB（含 CMU 詞典解析）；四語 1.76 秒、增加 30.1 MB（詞典已由 `SharedCMU` 快取，不重解析）；載入後 HeapAlloc 62.0 MB。

## 6. 資料、工具與打包檢查（已證實）

| 項目 | 結果 |
|---|---|
| `ja_check.sh`、`ko_check.sh`、`zh_cn_check.sh` | 全部通過（含 `translit_jk.py` 的 `lint`、`chars --check`、`examples --check`、`verify-fixed`，`font/characters.<lang>.txt` 重生比對，`charset.<lang>.txt` 與 Unifont 比對） |
| `translit_jk.py chars --check` | ja 88 字、ko 2,128 字與版控檔逐位元組相同 |
| `package.sh linux` | rc=0（前置檢查、`ja_check.sh`、`ko_check.sh`、`zh_cn_check.sh`、複製 `text/cmudict/` 與 `LICENSE-translit-table.md`、各語言字型、字型迴圈後的 `TestPackagedLanes`、Linux AppImage、外洩掃描 254 個檔案、237 個雜湊、268 個檔名無命中）；發行包暫存目錄的 `common/` 含 `text/cmudict/{cmudict.dict,LICENSE,README}`、`LICENSE-translit-table.md`、四個 `translit-*` 檔與四個語言字型，`THIRD-PARTY.md` 末段列 CMU 發音詞典與英語人名譯音表；以該暫存目錄另跑 `TestPackagedLanes`：PASS，四個通道的 `NICOLE STEELE` 為 妮可•斯蒂爾、妮可•斯蒂尔、ニコール・スティール、니콜 스틸。Windows、macOS 包未重打 |

## 7. 未做與後續

1. 母語者校對固定名單與詞典；規格 044、045 §6 的開放項目（含 B 的語音意見）仍開。
2. 規格 044 §3.8：引擎片段中嵌入的玩家名（`FLAVIUS は`、`FLAVIUS 은(는)`）仍是英文，屬規格 038 §4 的另案。
3. zh-TW、zh-CN 是否為 `甲板5。` 補呼叫起點空白（規格 047 §5），待使用者決定。
4. 規格 044、045 仍為 READY：§5 的整體項目（雙語抽審、Windows、macOS 打包模擬）未做，不升 CONFORMED。
