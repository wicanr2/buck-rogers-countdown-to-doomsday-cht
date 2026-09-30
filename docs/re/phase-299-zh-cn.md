# 第二百九十九階段：規格 041 簡體中文（zh-CN）實作與驗收

日期：2026-09-30
狀態：定稿（主代理審閱，2026-09-30）；實作 dosgolem `a665258`、第 12 節 char 對應與字型位置另見本段；phase254 rerun36 與 rerun35 逐位元組相同
規格：`docs/spec/041-zh-cn-draft.md`（READY，commit 0657bde）
程式：主 repo 工作樹（未 commit）；dosgolem fork `workplace/dosgolem`（分支 buck-rogers-cht-output-overlay，HEAD 9c6abb1，未提交修改），
同步副本 `workplace/dosgolem-clean`（`sync.sh`，原檔備份在 `clean-backup/`）。

## 結論

- 產生器 `tools/zh_cn_convert.py` 以標記字典追蹤取得原樣 `tw2sp` 與專案設定的逐處匹配。5,453 列追蹤輸出與正式設定逐列相同，匯出 text 字典設定與官方 ocd2 也逐列相同。
  兩次產生位元組相同，`--check` 通過，§5.1 合成負例 20 項全數如預期失敗或通過。
- 專案詞表 33 條（keep 21、map 3、guard 9），覆寫表 0 列（不需要，未建檔）。帳本 488 處逐一審閱，全部 `ok`。
- `tools/zh_cn_check.sh` 全部通過。兩支字面驗證器在 zh-TW 下行為不變，Python 測試 324 項 OK。
- 執行期：zh-CN 在 F4 循環內（zh-TW → zh-CN → en），DebugSummary 沒有 zh-CN 停用、重建或略過。
- 同狀態收據：四個時點在 2× 與 3× 下，zh-CN 的記憶體、CPU、indexed、palette 雜湊與停止步數都與 zh-TW、en、無語言旗標相同；
  切換後停在 zh-CN 的畫面，與一開始就用 zh-CN 的畫面逐位元組相同。玩家名收據中戰鬥右欄顯示「弗拉维乌斯」。
- phase254 七條回歸：rerun35 與 rerun34 的 853 個輸出檔（不含 runner）和 7 份文字結果全部逐位元組相同。
- 前端冷開機切到簡體，說明頁顯示「目前語言：簡體中文」。模擬打包：`common/` 含 `buckrogers-zh-CN.golemfnt`，外洩掃描通過。

## 1. 改動

主 repo：

| 檔案 | 內容 |
|---|---|
| `tools/docker/opencc/Dockerfile`、`requirements.txt`、`build.sh` | `buck-zhcn-opencc:1.4.2`。基底以 digest 鎖定，wheel 以 SHA-256 鎖定。wheel 快取在 `workplace/opencc-wheels/`，只有下載步驟開網路（本輪沿用 phase298 已下載的 wheel，未開網路）。image Id `sha256:fdc38613…15ea92` |
| `tools/docker/opencc/opencc-dicts.sha256` | tw2sp.json 與 7 份官方字典的 SHA-256，以檔名記錄，產生器啟動時逐檔核對 |
| `tools/zh_cn_convert.py`（新） | 產生、追蹤、自檢、遮蔽偵測、不變量、字數核算、覆寫、帳本、名字與例外表、音譯對照、跨家族一致性、`--check`、`--review-dir`、`--stats-out` |
| `tools/zh_cn_check.sh`（新） | 依 §3.7 逐支呼叫，另比對 `font/characters.zh-CN.txt` 是否與重生結果相同 |
| `tools/test_zh_cn_convert.py`、`tools/test_zh_cn_tools.py`（新） | §5.1 負例與工具 `--lang` 測試；沒有 OpenCC 的 image 會自動略過 |
| `tools/name_glossary.py` | `--lang` 讀取 `name-glossary.<lang>.tsv`、`name-glossary-exclude.<lang>.tsv`、`font/characters.<lang>.txt`；非 zh-TW 時 `old=` 不生效；glob 排除名字表；`apply`、`strip-logbook-notes` 只對 zh-TW |
| `tools/catalog_font.py` | `lint／chars／build --lang`：glob `text/*.<lang>.tsv`，排除名字表；非 zh-TW 併入 `translit-<lang>-map.tsv` 的目標字；明列路徑的行為不變 |
| `tools/technical_skill_screen_catalog.py`、`tools/skill_action_bar_catalog.py` | zh-TW 照舊比對字面；非 zh-TW 只查結構與 `(X)` 字母。`skill_action_bar_catalog.py` 新增 `--lang` |
| `tools/package.sh` | `LANGS=(zh-TW zh-CN)`；前置檢查執行 `zh_cn_check.sh`；非 zh-TW 語言各建 `font/buckrogers-<lang>.golemfnt`；打包時排除詞表、覆寫表與帳本 |
| `font/README.md` | 新增「簡體（zh-CN）字型」一節（字元清單與本機建置命令） |
| `text/zh-CN-phrases.tsv`、`text/zh-CN-term-review.tsv`（新） | 詞表、帳本 |
| 產生檔（留在工作樹） | 32 份 `text/*.zh-CN.tsv`、`name-glossary.zh-CN.tsv`、`name-glossary-exclude.zh-CN.tsv`、`translit-zh-CN-map.tsv`、`font/characters.zh-CN.txt`（2,460 字，SHA-256 `86adb3c9…be679`） |

沒有修改任何 `*.zh-TW.tsv`、zh-TW 名字表或 `docs/`。

dosgolem（`changed-files.txt`；xlate 未改）：

| 檔案 | 內容 |
|---|---|
| `apps/buckrogers/lang.go` | `LangZhCN` |
| `apps/buckrogers/name_glossary.go` | 非 zh-TW 語言從語言目錄讀取 `name-glossary-exclude.<lang>.tsv`，缺檔時不排除 |
| `apps/buckrogers/player_name.go` | `charMapTransliterator`：先以 zh-TW 音譯器產生，再逐字對照；`-`、`•` 直接通過，遇到表外字元就回英文。另有 `LoadTranslitCharMap`（單字、一對一）與 `TranslitMapFile` |
| `apps/buckrogers/live_lane.go` | zh-CN 的 PlayerNames 由 `translit.Load(textDir)` 包上 `text/translit-zh-CN-map.tsv`。對照檔載入失敗時只記 `玩家名=off(translit-map: …)`，語言本身仍啟用 |
| `cmd/buckrogers-text-receipt/main.go`、`lang_flags.go` | `-lang-dir <lang>=<dir>`、`-lang-font <lang>=<path>`（可重複）、`-font-root`。只載入 `-lang`、`-lang-switch`、`-lang-dir`、`-lang-font` 提到的語言；`-test-lang-*` 保留為 zz 別名。不帶語言旗標時不多載任何通道 |
| `apps/buckrogers/zh_cn_test.go`、`cmd/buckrogers-text-receipt/lang_dirs_test.go`（新） | 見 §3 |

## 2. 詞表與帳本

詞表 `text/zh-CN-phrases.tsv`：

- keep 21 條。沿用 phase298 的 19 條，其中「擴音器」改由「擴音」涵蓋。本輪依審閱新增 2 條：
  - `檢視`：水平選單同一列有「檢視(V)」與「查看(L)」，官方轉換會讓兩項同名。
  - `開啟`：開關選項在官方轉換後寫成「摇杆打开」，不自然。
- map 3 條，只有規格指定的 載入→读取、訊息→信息、呎→英尺。文件、影像、資料三詞沒有設 map，由官方 `TWPhrasesRev` 產生文档、图像、数据；「資料夾→文件夹」「資料庫→数据库」照官方轉換，沒有被遮蔽。
- guard 9 條：
  - 防寫保護（避免「写保护保护」）、許多工程（避免「许多任务程」）。
  - 的核心、之核心：官方異體詞「的核」「之核」會蓋住「核心」的起點。輸出不變，加 guard 是為了讓 keep 規則在每個出現處都能驗證。
  - 執行檔→可执行文件：「執行」的 keep 會遮蔽官方較長的「執行檔」（遮蔽類 1）。
  - 儲存槽、儲存區：這兩處指容器與存放區，不是存檔的「保存」。
  - 取樣本：「鑽取樣本」原本會被斷成「钻采样本」。
  - 貼上牆：「把耳朵貼上牆壁」原本會被轉成「粘贴墙壁」。

帳本 488 處（`TWPhrasesRev` 435、專案 map／guard 53；手冊家族 21、其他 467）。依 `workplace/zh-cn-review/review.tsv` 的 zh-TW 與 zh-CN 前後文逐處看過，全部判為 `ok`，override 為 0。
審閱中發現的 6 類問題（「查看」撞名、開關語境的「打开」、儲存槽、儲存區、取樣本、貼上牆）都以詞表修正後重新產生，再逐處複核。
note 的寫法分三類：使用者定案用語（文档、图像、数据、读取、信息、英尺）、大陸慣用語、專案 guard。手冊家族的 note 一律留空。

原樣 `tw2sp` 與正式輸出不同的列有 235 列，寬度改變的列有 24 列。變寬的有 4 列：`frag.2260006382e7`、`hmenu.a5add1365529`（呎→英尺）、`frag.5250b5de07b3`（新文件名），以及本輪因 guard 選用「可执行文件」而新增的 `frag.4844cec572c9`（14→18 單位）。

## 3. 測試

| 項目 | 結果 | 檔案 |
|---|---|---|
| `zh_cn_convert.py` 產生兩次，產生檔與詞表、帳本的雜湊彙總相同；`--check` | 通過（5,453 列、35 檔、帳本 488 處） | — |
| `test_zh_cn_convert.py` 20 項 | OK。涵蓋：不變量違反、字數核算不符、覆寫雜湊不符、孤兒覆寫、覆寫違反不變量、詞表含空白、詞條未實際匹配、出現處未匹配也未被覆蓋、遮蔽類 1／2／3、guard 修正類 1、帳本缺項或新套用處、帳本雜湊不符或多出、手冊 note、名字不一致、`chinese` 重複、例外片語不一致、跨家族不一致、音譯碰撞、手改產生檔後 `--check` 失敗 | `py-all.txt` |
| `test_zh_cn_tools.py` 7 項 | OK。兩支字面驗證器在 zh-TW 下行為不變、非 zh-TW 查熱鍵；`name_glossary`／`catalog_font` 的 `--lang`；zh-TW 明列路徑的 `chars` 仍等於 `font/characters.txt` | `py-all.txt` |
| tools 全部 Python 測試（buck-zhcn-opencc，repo 唯讀） | 324 項 OK（python:3.13-slim：OK，略過 20 項） | `py-all.txt`、`py-slim.txt` |
| `tools/zh_cn_check.sh` | 全部通過 | — |
| `go test ./...`（dosgolem-clean，ebiten image） | 31 套件 ok、0 FAIL | `test-all.txt` |
| `go vet`（apps/buckrogers、cmd/buckrogers-text-receipt）、`gofmt -l`、`GOOS=windows CGO_ENABLED=0 go build ./...` | 無輸出／通過 | `vet.txt`、`build-windows.txt` |

新增的 Go 測試：

- `TestCharMapTransliterator`、`TestLoadTranslitCharMap`：字級對照、`-` 與 `•` 通過、表外字元回英文、碰撞與重複等錯誤。
- `TestNameGlossaryLangFiles`：例外表每個語言讀自己的檔。
- `TestZhCNLaneOnFormalText`：F4 循環為 zh-TW,zh-CN,en；DebugSummary 沒有停用、重建或略過；FLAVIUS→弗拉维乌斯，BUCK→巴克（名字表優先）；zh-TW 仍是弗拉維烏斯。
- `TestZhCNMapMissingOnlyDisablesPlayerNames`：對照檔缺席時只停用 zh-CN 的玩家名，語言照常啟用。
- `TestZhCNWidenedRowsFitEnglishCells`：見 §5。
- `TestReceiptLangs`：收據工具新旗標。

## 4. 同狀態收據（§5.4）

腳本 `switch.sh`、`switch/cases.sh`，比對 `switch/compare.py`，結果 `switch/compare.json`。
停止步數與按鍵沿用 phase296。每個時點跑五組：S-zh-TW、S-zh-CN、S-en、W-zh-CN（zh-TW→en→zh-TW→zh-CN 切換後停在 zh-CN）、none（無語言旗標），全程 `-compose-every-retrace`。
zh-CN 使用正式 `text/`，字型以 `-lang-font` 指定本輪建置的 `font/buckrogers-zh-CN.golemfnt`（SHA-256 `34eedaf2…b0a50`）。

| 時點 | 停止步數 | memory／cpu（2×、3× 相同，各語言相同） | 結果 |
|---|---|---|---|
| ECL 敘事窗 | 409,000,000 | `877f715f…`／`91835ee6…` | 通過 |
| 水平選單 | 432,500,000 | `7290b7b3…`／`995a44ac…` | 通過 |
| 手札面板開啟 | 5,285,000,000 | `ceb6b6fc…`／`29f8055d…` | 通過 |
| 手冊題進行中 | 266,650,000 | `7900785e…`／`425cf745…`（只記雜湊，RGBA 已刪除，未截圖） | 通過 |

通過的判準：
- W-zh-CN＝S-zh-CN、S-en＝原版 baseline。
- 記憶體、indexed、palette、停止步數在各組與 none 之間相同，CPU 雜湊在各組之間相同。
- 停止時的語言正確。
- 各時點的 zh-CN 畫面都與 zh-TW 不同，也與原版不同（有疊字）。

截圖目視：`ecl-zh-CN-2x/3x.png`、`hmenu-zh-CN-2x/3x.png`、`logbook-zh-CN-2x/3x.png`，另附 zh-TW 對照 `*-zh-TW-2x.png`。沒有缺字，也沒有溢出。
- ECL 畫面右欄的隊員名也以簡體音譯顯示（塞莱斯特、妮可•斯蒂尔 等）。
- 水平選單括號內的熱鍵字母是空的，zh-TW 也一樣（phase298 已記錄的既有狀態）。

玩家名：`phase257-text-window-trace/cp/a4.state`，Esc 按鍵在 2,861,000,000，停在 2,861,500,000（`pn/inner.sh`）。
zh-TW 與 zh-CN 在 2×、3× 的記憶體（`2a30e3d9…`）與 CPU（`15626952…`）雜湊相同。
zh-CN 戰鬥右欄顯示「特林战士 攻击 弗拉维乌斯 ，但没有命中。」（`player-name-zh-CN-2x.png`、`-3x.png`）。

## 5. 變寬列（§5.4）

- `width-bound.json`：四個變寬項的 zh-CN 單位數（4、18、10、4）都不超過它取代的英文格數（每個原文字 2 單位：10、46、30、8）。
  hmenu 與 engine-fragment 中超出英文格數的項目，zh-TW 與 zh-CN 都是 54 項與 5 項，沒有任何一項只在 zh-CN 超出。
- Go 單元先建 `TestZhCNWidenedRowsFitEnglishCells`：以 zh-CN catalog 把 hmenu 的「feet」放在英文剛好放得下的第 36 欄，可以排版，而且補滿 8 單位。
- 限制：這證明逐項不超過英文，也證明該項在英文的最右位置放得下。它沒有量過實際畫面中與其他 zh-TW 已超長項目同列時的整列總寬。
  這種情況下 watcher 的 overflow 會讓整列改回原版英文，不會溢出。來源顯示這 4 項分別是啟動錯誤訊息（START.EXE「unable to load com file」）、存檔改名提示與距離單位，本輪沒有找到能到達這些畫面的 state。

## 6. 回歸（phase254 七條）

`phase254-live-families-parity/runner` 先備份為 `runner-rerun34`（SHA-256 `c9a022c5…`，與 `rerun34/runner` 相同），再換成本輪 `runner`（`899c7b75…`）。
`rerun35/` 的腳本由 rerun34 原樣複製（`p254run.sh`）。結果：854 個檔案中，除 runner 以外的 853 個輸出檔與 `rerun35-*.txt` 七份，都與 rerun34 逐位元組相同。

## 7. 前端（buckrogers-play，Xvfb，自動模式，冷開機 1500 畫格，zh-TW 用 Unifont 子集 `font-uni/`）

| 執行 | 腳本 | 結束語言 | memory／cpu | 合成 |
|---|---|---|---|---|
| a0 | 無 | zh-TW | `13fb0226…`／`c4d05f4a…`（與 phase297 相同） | `7125ce2e…` |
| c1 | `1300:lang` | zh-CN | 相同 | `342ac18d…`（標題列「播放(P) 示范(D)」，`c1.png`） |
| b2 | `1300:lang,1400:lang` | en | 相同 | 等於原版 `0dc3ec5d…` |
| h1 | `1300:lang,1450:help` | zh-CN | `319c73aa…`／`8d0a5394…`（與 phase297 h2 相同） | 說明頁「目前語言：簡體中文」「未啟用：日文、韓文（缺語言檔）」（`h1.png`） |

stderr 只有 ja、ko 的停用訊息。zh-CN 字型依 `font/buckrogers-zh-CN.golemfnt` 相對執行檔的路徑找到。

## 8. 打包（模擬，未跑完整 package.sh）

完整 `package.sh` 會 git archive 已推送的 dosgolem HEAD（不含本輪改動），而且會清掉 `dist-all/` 的同變體舊產物，所以本輪沒有執行。
改在 `pkg-stage/` 依同一套邏輯複製 `text/`（排除 3 檔）並建兩份字型，再以 `tools/release/leak_scan.py` 掃描四個禁止來源：
- 掃描 154 個檔案，0 命中。
- `buckrogers-zh-CN.golemfnt` 為 `34eedaf2…`，與本機建置相同，屬決定性輸出。
- zh-CN 新增內容（譯文與對照檔加字型）未壓縮約 523 KB；壓縮後的增量未量。

## 9. 未量到

1. 變寬 4 列的整列實跑（§5）。
2. 商店、戰鬥選單、角色頁、劇情頁等其他家族的 zh-CN 畫面：只量了四個時點與玩家名，手冊題依規定只記雜湊。
3. 完整 `tools/package.sh`（三平台產物與壓縮後增量）；互動模式按 F4 的實機操作。
4. `buck-zhcn-opencc` 的 wheel 下載分支（快取已存在，本輪未走網路路徑）。

## 10. 待決

1. **非 GB2312 殘留字**：規格 §3.2 規定 map 只有 3 條，所以 phase298 原型中的字級項（牠→它、暱→昵、瞇→眯、砲→炮、吋→寸）本輪沒有放入。
   zh-CN 譯文中仍有「牠」45 列、「砲」21 列、「暱」「瞇」「吋」各 1 列。列數太多，不適合逐列覆寫。建議修訂規格，允許這類字級 map。
2. **本機字型位置與外洩掃描衝突**：規格 §3.7 要把本機 `buckrogers-zh-CN.golemfnt` 建在 `workplace/current-font`，但該目錄是 `package.sh` 外洩掃描的禁止來源；
   放入後，發行包的同名同內容字型會被擋下。`font/README.md` 已註明「打包前需先移出」，是否改用其他位置待定。
3. guard「執行檔→可执行文件」使 `frag.4844cec572c9` 變寬 4 單位，是規格列出的 3 列以外新增的一列。它仍在英文格數內。
4. 跨家族一致性的「詞」本輪定義為：整列只含漢字（可含 •）、長 2–12 字的列。它在其他家族出現時，只比對邊界與匹配對齊的位置；邊界落在某個官方詞內時，視為不是同一個詞而略過。遮蔽偵測的豁免條件以「整列輸出與拿掉該詞條時相同」判定。這兩處是規格用語的實作解讀。
5. `docs/release/讀我.txt` 沒有提到簡體（本任務不得改 docs/）。
6. 收據工具保留 `-test-lang-dir`／`-test-lang-font` 作為 zz 的別名。

## 11. 檔案

- 腳本：`run.sh`、`run-play.sh`、`go.sh`、`sync.sh`、`switch.sh`、`switch/`、`pn/`、`p254run.sh`、`width_bound.py`、`width-bound.json`、`make_ledger.py`、`dbg.py`。
- 統計與測試輸出：`stats.json`、`py-all.txt`、`py-slim.txt`、`test-all.txt`、`vet.txt`、`build-windows.txt`。
- 程式與字型：`runner`、`buckrogers-play`、`font/`、`font-uni/`、`pkg-stage/`、`zz/`（phase296 的 zz 測試資料複本）、`clean-backup/`、`changed-files.txt`、`new-files.txt`、`*.png`。
- 審閱清單：`workplace/zh-cn-review/review.tsv`（含手冊前後文，不進版控）。
- phase254：新增 `runner-rerun34`、`rerun35/`、`rerun35-*.txt`；`runner` 已換成本輪版本。

## 12. 第二輪：規格 041 修訂（commit 4afaa7e）

基底：主 repo dd5b256＋4afaa7e、dosgolem a665258。本輪改動沒有 commit。

### 12.1 結論

- 新增 `char` 字級對應，在 OpenCC 轉換之後逐字套用。詞表中 char 4 條：牠→它、砲→炮、暱→昵、瞇→眯；新增 map 3 條：吋→英寸、紀錄→记录、掃瞄→扫描。
- 重新產生後帳本共 595 處（官方用語詞條 435、專案 160）。新增 107 處逐一審閱，全部 `ok`，覆寫表仍為 0 列。
- `--check` 與 `zh_cn_check.sh` 全部通過，Python 測試 329 項 OK（新增 char 測試 5 項）。
- 本機非 zh-TW 字型改放 `workplace/lang-fonts/`。前端新增 `-lang-fonts <目錄>` 旗標，`play.sh` 可選擇把該目錄掛進去。
- 四時點收據、phase254 rerun36（與 rerun35 逐位元組相同）、打包外洩掃描都已重跑並通過。

### 12.2 盤點與決定

zh-CN 輸出（譯文欄與名字表 `chinese` 欄）中的非 GB2312 字與台灣慣用寫法：

| 字／詞 | 處數 | 決定 | 理由 |
|---|---|---|---|
| 牠 | 67（含手冊） | char →它 | 逐處看過：都是動物、ECG、斯科特（電腦人格）、蛙王、低地人幼體、鸚鵡、雕像的代詞。名字表、例外表、怪物名、物品名都沒有「牠」 |
| 砲 | 21 | char →炮 | 舰炮、激光炮、加速炮、回旋炮、店名「枪炮反斗行」，都是一般字，不是專名用字 |
| 暱、瞇 | 各 1 | char →昵、眯 | 大陸規範字 |
| 吋 | 1 | map →英寸 | 改變字數，依規格用 map（「每一吋」→「每一英寸」） |
| 紀錄 | 9 | map →记录 | 文件記載義；「纪录」在大陸偏指成績紀錄 |
| 掃瞄 | 7 | map →扫描 | 台灣異體寫法；「瞄」單字另有「瞄准」等用法，不能用 char |
| 瞭 | 1 | 保留 | 「瞭望」在《通用規範漢字表》保留「瞭」 |
| —、• | 91、37 | 保留 | 標點，規格 §4 不改 |
| 帮浦、杂讯 | 4、1 | 未處理 | 屬於詞彙改譯（泵、噪声），超出規格 §4 的「簡體專屬譯文重寫」範圍 |

名字表 `chinese`、例外表與音譯對照都經過同一條「OpenCC＋char」流程。這三個檔在本輪逐位元組未變，所以玩家名收據不受影響。

### 12.3 產生器改動（`tools/zh_cn_convert.py`）

- `kind=char`：`tw` 與 `cn` 必須各是單一且不同的漢字。char 不送進 OpenCC 設定，改在 OpenCC 輸出上逐字套用。
- char 的自檢：
  - 單獨轉換（OpenCC＋逐字）的結果要等於 `cn`。
  - 在 OpenCC 輸出上至少命中一次。
  - `cn` 必須在 `font/characters.zh-CN.txt` 內。產生模式下這項只列為帳本警告，`--check` 時才算錯誤，因為字元清單是由產生結果重生的。
- 字數核算把 char 視為長度差 0。char 不參加遮蔽偵測與「出現處」檢查，因為它是 OpenCC 之後的後處理，不會和 OpenCC 的詞條互相遮蔽。
- 帳本：每列的 char 套用處接在該列的 OpenCC 套用處之後編號，位置用最終輸出座標，`term_id` 為 `zh-CN-phrases:<列號>`。
- 名字表、例外表、音譯對照也套用 char。
- 新增負例與正例測試（`test_zh_cn_convert.py`）：
  - char 多字元會失敗。
  - char 從不命中會失敗（例：「們」在 OpenCC 輸出已經是「们」）。
  - char 的 `cn` 不在字元清單會失敗。
  - char 的正例與帳本編號。
  - 名字表跟著 char 轉換。

### 12.4 本機字型位置

- `workplace/lang-fonts/buckrogers-zh-CN.golemfnt`（SHA-256 `70db5f48…faed3`）。
  `workplace/current-font` 原本就沒有 zh-CN 字型，沒有檔案需要搬移，目錄仍只有倚天 zh-TW。
- dosgolem `cmd/buckrogers-play`：
  - 新增 `-lang-fonts <目錄>`：有給就只在該目錄找 `buckrogers-<lang>.golemfnt`，沒給則照舊在發行包的 `font/` 找。
  - 新測試 `lang_fonts_test.go`。
- `workplace/play.sh`（備份在 `play.sh.bak-phase299`）：
  - 新增 `PLAY_BIN_DIR`：有設時掛入 `workplace/lang-fonts` 並傳 `-lang-fonts`。
  - 預設仍用 phase252 的前端；那一版不支援多語，所以預設不傳這個旗標。
- `font/README.md` 已改寫本機命令與說明。
- 實跑（`lf-c1`、`lf-h1`）：工作目錄設在 `/tmp`，執行檔旁邊沒有 `font/`，只給 `-lang-fonts /lf`。
  結果 zh-CN 啟用、切換成功，合成雜湊與第一輪 c1 相同（`342ac18d…`），說明頁仍顯示「目前語言：簡體中文」；記憶體與 CPU 雜湊與第一輪相同。

### 12.5 驗收重跑

- 四時點收據（`switch.sh`）：2×、3× 全部通過，記憶體、CPU 雜湊與 zh-TW 相同，也與第一輪相同。截圖已更新（`ecl-`、`hmenu-`、`logbook-zh-CN-2x/3x.png`；第一輪的收在 `r1/`）。
  這四個時點的畫面不含本輪改動的字，所以 zh-CN 畫面雜湊與第一輪相同。char 與新 map 的實際效果以產生檔、帳本與單元測試驗證，沒有另做畫面收據。
- 變寬列：新增 `ecl.6.97.04086`（吋→英寸，+2 單位，34 單位，英文 51 字＝102 單位），已加入 `TestZhCNWidenedRowsFitEnglishCells`，通過。
- phase254：`runner` 備份為 `runner-rerun35`（與 `rerun35/runner` 相同）。receipt 程式本輪未改，重建出的 runner 與前一版同雜湊（`899c7b75…`）。
  `rerun36/` 的 853 個輸出檔與 7 份文字結果，都與 rerun35 逐位元組相同。
- 打包模擬：`pkg-stage/common/font/buckrogers-zh-CN.golemfnt` 為 `70db5f48…`，詞表、覆寫表、帳本已排除（0 檔），外洩掃描 154 檔、0 命中。
- Go 測試：`./apps/buckrogers`（zh-CN 相關）與 `./cmd/buckrogers-play` 通過，`go vet ./cmd/buckrogers-play` 通過，Windows build 通過。本輪沒有重跑整個 `go test ./...`。

### 12.6 待決

1. `play.sh` 的預設前端仍是 phase252（沒有多語），要不要改用新版前端待定。
2. 「帮浦」「杂讯」這類詞彙差異要不要處理：規格 §4 不做簡體專屬的譯文重寫，本輪沒有動。
3. 新增的 map「紀錄→记录」「掃瞄→扫描」不在規格原列的 map 範例內，是依「盤點決定」加入的，請確認。
