# 041 — 簡體中文（zh-CN）

狀態：**READY**（2026-09-30，兩輪獨立審查；第二輪應改已併入）
日期：2026-09-30
Issue：#35
前置：規格 040（多語框架）、039（半形）、036／037／038（名字）、005／034（手冊）。
證據：[phase-298](../re/phase-298-zh-cn-probe.md)（OpenCC 盤點與原型）。

## 1. 為什麼要做

使用者決定（2026-09-29、09-30）：F4 循環加入簡體；由正式繁中譯文以 OpenCC 詞彙級轉換產生並進版控；
做法為 `tw2sp`＋專案詞表（防止資訊科技用語誤套到敘事）＋少量逐列覆寫；標點維持「」『』與 `•`；用語採大陸慣用
（文档、图像、数据、读取、信息、英尺）；簡體模式的玩家名＝繁中音譯後逐字轉簡。

## 2. 證據

- phase-298：OpenCC（PyPI `OpenCC` 1.4.2，Apache-2.0，wheel SHA-256 `25c34e75…3f63`，只有 x86_64）；原樣 `tw2sp` 錯譯
  （「核心區→内核区」35 處、「呼叫(H)→调用(H)」、「自毀程序→自毁进程」）與前綴匹配錯誤（「許多工程→许多任务程」）；
  版面、字型、名字一致性、執行期載入的量測結果見該文件。
- 第一輪審查實測（`buck-phase298-opencc:1.4.2`，已證實）：
  - 專案詞表插在第一段用語群組最前面時，同一起點上專案詞條優先於官方較長詞（例：加 `資料→数据` 後「資料夾」變「数据夹」，
    原樣為「文件夹」；「執行檔」相關片語同理）。
  - text 字典的 `cn` 含空白時被當成多個候選、只取第一個且不報錯；重複 key 由 OpenCC 報錯。
  - 斷詞（mmseg）只用官方 `TSPhrases`，專案詞表不參與斷詞。
  - 「去掉漢字後的字元序列完全相同」的不變量下，U+3000 與「、，。！？：；（）～…—」等全形標點 OpenCC 都不改。
- 第二輪審查實測（已證實）：OpenCC Python API 只有 `convert()`，不暴露匹配位置；以「標記字典追蹤」可取得逐處匹配——把匯出的
  官方 text 字典與專案詞表每個詞條的值換成唯一私用區字元，只保留正規化、斷詞與第一段群組；官方 ocd2 換成匯出 text 字典後
  5,812 列輸出與原樣 `tw2sp` 相差 0 列，逐列位置累加斷言全數成立。官方 `TWPhrasesRev` 本身已含「資料→數據、文件→文檔、
  影像→圖像」，並會改變字數（記憶體→内存、使用者→用户、檔名→文件名等）。

## 3. 契約

### 3.1 產生器

- `tools/zh_cn_convert.py`（主 repo），在固定版本 Docker image 內執行；Dockerfile 與 wheel 雜湊鎖定檔在
  `tools/docker/opencc/`；只有下載 wheel 的建置步驟開網路（wheel 快取放 `workplace/`），轉換一律 `--network none`。
  `tools/package.sh` 打包 `text/` 時排除詞表、覆寫表與帳本。
- OpenCC 設定在容器內由官方 `tw2sp.json` 產生（`include_tofu_risk_dictionaries=True`），把專案詞表插在第一段用語群組最前面，
  群組 `match_policy` 維持 `short_circuit`；版控只放詞表 TSV 與官方字典的 SHA-256 清單（以檔名記，不含容器絕對路徑）。
- **匹配追蹤**：產生器以「標記字典追蹤」取得原樣 `tw2sp` 與專案設定兩種設定下的逐處匹配（位置、長度、詞條、來源字典），
  並先驗證追蹤設定的轉換輸出與正式設定逐列相同。§3.2 自檢、遮蔽偵測、§3.4 字數核算、§3.5 帳本都以追蹤結果為準。
- 輸入：全部 `text/*.zh-TW.tsv` 的 translation 欄，**排除** `translit-chars`、`host-ui`、`manual-english-panel`（zh-CN 模式的
  說明頁照規格 040 用 zh-TW；英文摘錄面板只在 zh-TW）。輸出 `text/*.zh-CN.tsv`，key 集合與 zh-TW 相同，其他欄不動。
- 手工不得直接編輯產生檔；修正只經詞表或覆寫表。
- 決定性：同一輸入、image、詞表、覆寫表與帳本，輸出位元組相同。`--check` 重新產生並比對全部產生檔、驗證詞表與覆寫表與帳本，
  任何差異或檢查失敗即非零結束。

### 3.2 專案詞表 `text/zh-CN-phrases.tsv`

- 欄位：`tw`、`cn`、`kind`、`reason`。`kind`：`keep`（保留原詞）、`map`（指定對應）、`guard`（為避免遮蔽官方較長詞或修正
  前綴匹配錯誤而加的較長詞條）。用語偏好中「文档、图像、数据」由官方 `TWPhrasesRev` 產生，不設 `map`（避免遮蔽「資料夾、
  資料庫」）；`map` 只用於官方沒有的偏好：載入→读取、訊息→信息、呎→英尺。
- 自檢（任一失敗即產生失敗）：
  1. `tw`、`cn` 不含空白或 tab；不得有重複 `tw`。
  2. 每條單獨轉換的結果等於 `cn`（第二段繁→簡對 `cn` 恆等）。
  3. 每條至少在正式譯文**實際匹配**一次（依追蹤結果，不以字面出現計）。
  4. 每條在 zh-TW 的每個出現位置，依追蹤結果必須是「該詞條在此處實際匹配」或「被較長的 `guard`／`map` 詞條覆蓋」；兩者皆非
     即失敗。
- **遮蔽偵測**（依追蹤結果）：下列三類位置必須由 `guard` 詞條或覆寫表處理，未處理即失敗：
  1. 同一起點上專案詞條使官方較長詞失效（例：「執行<執行檔」）。
  2. 官方匹配的起點落在專案詞條內部（例：「許多|多工」）。
  3. 官方匹配覆蓋專案詞條的起點。
  例外：該處的最終輸出與「不套用該專案詞條」時相同（例：`keep` 詞被官方變體詞吃掉但輸出仍含原詞），免加 `guard`。

### 3.3 覆寫表 `text/zh-CN-overrides.tsv`

- 欄位：`family`、`key`、`zh_tw_sha256`（該列 zh-TW translation 欄 UTF-8 位元組的 SHA-256）、`translation`、`reason`。
- 雜湊不符、key 不存在（孤兒）、覆寫結果違反 §3.4 不變量，都讓產生失敗。

### 3.4 不變量（產生結果與覆寫都適用）

- NFC 正規化；無控制字元；每列去掉漢字（CJK 統一表意文字）後的字元序列與 zh-TW 完全相同（涵蓋 ASCII、佔位符 `{n}`、`\n`、
  `(X)`、全形標點、U+3000、`•`）；括號數相同。
- 每列漢字數的改變量，必須等於該列依追蹤結果套用的官方用語詞條（`TWPhrasesRev`）與專案 `map`／`guard` 詞條的長度差總和；
  不符即失敗。

### 3.5 審閱帳本 `text/zh-CN-term-review.tsv`

- 範圍：依追蹤結果，官方 `TWPhrasesRev` 與專案 `map`／`guard` 的每個套用位置（不含 `keep` 與異體字典 `TWVariantsRev*`）；
  以現行譯文估約 500–550 處，逐一審閱，不抽樣。
- 審閱清單：產生器把全部套用處連同 zh-TW 前後文與 zh-CN 結果輸出到 `workplace/zh-cn-review/`（gitignore，手冊家族也列，
  供審閱者判斷），不寫進 `text/`。
- 帳本 `text/zh-CN-term-review.tsv` 欄位：`family`、`key`、`zh_tw_sha256`、`occurrence`（該列內的出現序號）、`term_id`
  （詞條識別：官方詞條為字典名與詞條序號，專案詞條為詞表列號；不含詞彙本身）、`verdict`（`ok`／`override`）、`note`
  （手冊家族留空）。
- 帳本須涵蓋全部套用處；缺項、雜湊不符或出現新套用處時 `--check` 失敗。

### 3.6 名字

- 036：產生器輸出 `text/name-glossary.zh-CN.tsv`（`chinese` 欄以同一流程轉換；`english`、`english_mixed` 等與語言無關的欄不動；
  `note` 的 `old=` 對 zh-CN 無作用）與 `text/name-glossary-exclude.zh-CN.tsv`（片語轉換）。檢查：譯文中每個出現位置轉換後與
  名字表 zh-CN 寫法一致；轉換後 `chinese` 唯一；例外表的片語在譯文中的每個出現位置同樣轉換一致。Go 端 NameGlossary 與例外表每語言讀取各自檔案（zh-TW 維持現行檔名）。
- 037：產生器輸出唯一的音譯對照 `text/translit-zh-CN-map.tsv`（欄位 `tw`、`cn`；允許字集 329 字；值為單一字元；一對一，碰撞
  即失敗）；不產生 `translit-chars.zh-CN.tsv`，`tools/translit.py chars --check` 只用於 zh-TW。
- Go 端：zh-CN 的 PlayerNames 包一層字級對照（`nameTransliterator` 介面）：先以 zh-TW 音譯器產生，再逐字轉換；`-` 與 `•` 直接
  通過；表外字元出現時該名字顯示英文（與音譯失敗同）。對照檔從共用 text 目錄讀取，載入失敗時 zh-CN 的 PlayerNames 停用、
  名字顯示英文，不讓語言失效。

### 3.7 驗證與字型

- 驗證命令以 `tools/zh_cn_check.sh`（Docker 內）統一執行，逐支明列呼叫形式：
  - OpenCC image：`zh_cn_convert.py --check`。
  - 以 `--lang zh-CN` 呼叫：menu_events、gender_events、class_events、character_sheet_events、name_prompt_catalog、body_icon_catalog、
    career_skill_screen_catalog、save_roster_join_catalog、technical_skill_screen_catalog、header_columns、name_glossary（lint）、
    catalog_font（lint）、skill_action_bar_catalog（本規格新增 `--lang`）。
  - 以 `*.zh-CN.tsv` 路徑呼叫：story_opening_catalog、story_page2–9_catalog、manual_catalog、manual_overlay_layout。
- 跨家族一致性（`--check`）：同一 zh-TW 詞在不同家族（例：技能名在技能頁與手冊）轉換後必須相同，不同即失敗或需覆寫。
- 需改的工具：`name_glossary.py`（`--lang` 讀 `name-glossary.<lang>.tsv` 與 `font/characters.<lang>.txt`，catalog glob 排除
  名字表檔，`apply` 不對產生檔執行）；`catalog_font.py` 新增 `--lang`（輸入排除名字表檔、併入音譯對照的簡體字）；
  `technical_skill_screen_catalog.py` 與 `skill_action_bar_catalog.py`：zh-TW 照舊比對字面，zh-CN 改為只查結構與 `(X)` 字母
  （字面由產生器 `--check` 保證），`skill_action_bar_catalog.py` 新增 `--lang`；ja、ko 由後續規格定義。
- 字元清單 `font/characters.zh-CN.txt` 由正式 zh-CN 譯文（含音譯對照簡體字）產生並進版控。
- 打包：`tools/package.sh` 的語言清單明列 `zh-TW zh-CN`；前置檢查執行 `zh_cn_check.sh`，失敗即中止；對清單內每個語言建
  `font/buckrogers-<lang>.golemfnt`（zh-TW 維持現行產物名 `buckrogers-unifont.golemfnt`）。發行包約增加 3–4%。
- 本機：`workplace/current-font` 旁另建 `buckrogers-zh-CN.golemfnt` 的命令寫進 `font/README.md`。

### 3.8 同步關卡

- 修改任何 `*.zh-TW.tsv` 或名字表的 commit，必須同時提交重新產生的 zh-CN 檔與更新的帳本；打包前置檢查擋下遺漏。

### 3.9 收據工具

- `cmd/buckrogers-text-receipt` 通用化：`-lang-dir <lang>=<dir>`、`-lang-font <lang>=<path>`（取代只收 zz 的測試旗標，zz 仍可用），
  未指定時 `-lang-dir` 預設為 `-live-text-dir`，並自動載入 `<repo 根>/font/buckrogers-<lang>.golemfnt`（存在時；根目錄由
  `-font-root` 指定，預設為 `-live-text-dir` 的上一層）。

## 4. 不做什麼

- 標點改大陸慣用（“”、·）；簡體專屬的譯文重寫；日文、韓文（042–045）。

## 5. 驗收

1. 產生器：追蹤設定輸出與正式設定逐列相同；兩次產生位元組相同；`--check` 通過；合成負例失敗——不變量違反、字數核算不符、
   覆寫雜湊不符、孤兒覆寫、詞表含空白、詞條未實際匹配、詞條出現處未匹配也未被覆蓋、三類遮蔽未處理、帳本缺項或新套用處、
   名字寫法不一致、`chinese` 重複、例外片語不一致、跨家族不一致、音譯對照碰撞。
2. `zh_cn_check.sh` 全部通過；兩支字面驗證器的 zh-TW 行為不變。
3. 執行期：前端與收據工具載入後 zh-CN 在 F4 循環內；DebugSummary 無 zh-CN 停用與重建計數。
4. 同狀態收據（2×、3×）：規格 040 §5.3 的四個時點以 `-lang zh-CN` 輸出，記憶體與 CPU 雜湊與 zh-TW 相同；ECL、水平選單、手札
   截圖目視無缺字與溢出（手冊題時點只記雜湊）。三列變寬（呎→英尺兩列、`frag.5250b5de07b3`）以單元先建或針對性收據驗證整列寬度。
   玩家名：phase-286 的 `cp/a4`＋a5 按鍵停 2,861.5M，戰鬥右欄預期「弗拉维乌斯」。
5. 回歸：phase254 七條回歸（zh-TW）逐位元組不變。
6. 前端：冷開機切到簡體截圖；說明頁「目前語言」為簡體中文；打包產物含 zh-CN 字型並通過外洩掃描。
