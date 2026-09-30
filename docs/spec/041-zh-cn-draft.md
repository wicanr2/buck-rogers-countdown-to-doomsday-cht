# 041 — 簡體中文（zh-CN）

狀態：**DRAFT**（2026-09-30，第一輪審查後修訂）
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

## 3. 契約

### 3.1 產生器

- `tools/zh_cn_convert.py`（主 repo），在固定版本 Docker image 內執行；Dockerfile 與 wheel 雜湊鎖定檔在
  `tools/docker/opencc/`；只有下載 wheel 的建置步驟開網路（wheel 快取放 `workplace/`），轉換一律 `--network none`。
- OpenCC 設定在容器內由官方 `tw2sp.json` 產生（`include_tofu_risk_dictionaries=True`），把專案詞表插在第一段用語群組最前面；
  版控只放詞表 TSV 與官方字典的 SHA-256 清單，不放含容器絕對路徑的設定檔。
- 輸入：全部 `text/*.zh-TW.tsv` 的 translation 欄，**排除** `translit-chars`、`host-ui`、`manual-english-panel`（zh-CN 模式的
  說明頁照規格 040 用 zh-TW；英文摘錄面板只在 zh-TW）。輸出 `text/*.zh-CN.tsv`，key 集合與 zh-TW 相同，其他欄不動。
- 手工不得直接編輯產生檔；修正只經詞表或覆寫表。
- 決定性：同一輸入、image、詞表、覆寫表與帳本，輸出位元組相同。`--check` 重新產生並比對全部產生檔、驗證詞表與覆寫表與帳本，
  任何差異或檢查失敗即非零結束。

### 3.2 專案詞表 `text/zh-CN-phrases.tsv`

- 欄位：`tw`、`cn`、`kind`、`reason`。`kind`：`keep`（保留原詞）、`map`（指定對應，含用語偏好文档、图像、数据、读取、信息、
  英尺）、`guard`（為避免遮蔽官方較長詞或修正前綴匹配錯誤而加的較長詞條）。
- 自檢（任一失敗即產生失敗）：
  1. `tw`、`cn` 不含空白或 tab；不得有重複 `tw`。
  2. 每條單獨轉換的結果等於 `cn`（第二段繁→簡對 `cn` 恆等）。
  3. 每條至少在正式譯文命中一次。
  4. 每條在 zh-TW 的每個出現位置，專案設定的輸出都含該 `cn`。
- **遮蔽偵測**：逐處比對「專案設定」與「原樣 tw2sp」在同一位置的最長匹配；專案詞條使官方較長詞失效、或官方詞吃掉專案詞的位置，
  必須由 `guard` 詞條處理（例：`資料夾→文件夹`、執行檔相關片語給對應 `guard`），或在覆寫表明確處理；未處理即失敗。

### 3.3 覆寫表 `text/zh-CN-overrides.tsv`

- 欄位：`family`、`key`、`zh_tw_sha256`（該列 zh-TW translation 欄 UTF-8 位元組的 SHA-256）、`translation`、`reason`。
- 雜湊不符、key 不存在（孤兒）、覆寫結果違反 §3.4 不變量，都讓產生失敗。

### 3.4 不變量（產生結果與覆寫都適用）

- NFC 正規化；無控制字元；每列去掉漢字（CJK 統一表意文字）後的字元序列與 zh-TW 完全相同（涵蓋 ASCII、佔位符 `{n}`、`\n`、
  `(X)`、全形標點、U+3000、`•`）；括號數相同。
- 漢字數只能因 `map` 或 `guard` 詞條改變（例：呎→英尺）；其他情形漢字數必須相同。

### 3.5 審閱帳本 `text/zh-CN-term-review.tsv`

- 產生器列出全部「用語套用處」（官方用語詞條與專案 `map`／`guard` 的每個套用位置）。帳本欄位：`family`、`key`、`zh_tw_sha256`、
  `term`、`verdict`（`ok`／`override`）、`note`。手冊家族只記 key、雜湊與結論，不記內容。
- 帳本須涵蓋產生器列出的全部套用處（逐一審閱，不抽樣）；缺項、雜湊不符或出現新套用處時 `--check` 失敗。

### 3.6 名字

- 036：產生器輸出 `text/name-glossary.zh-CN.tsv`（`chinese` 欄以同一流程轉換；`english`、`english_mixed` 等與語言無關的欄不動；
  `note` 的 `old=` 對 zh-CN 無作用）與 `text/name-glossary-exclude.zh-CN.tsv`（片語轉換）。檢查：譯文中每個出現位置轉換後與
  名字表 zh-CN 寫法一致；轉換後 `chinese` 唯一。Go 端 NameGlossary 與例外表每語言讀取各自檔案（zh-TW 維持現行檔名）。
- 037：產生器輸出唯一的音譯對照 `text/translit-zh-CN-map.tsv`（欄位 `tw`、`cn`；允許字集 329 字；值為單一字元；一對一，碰撞
  即失敗）；不產生 `translit-chars.zh-CN.tsv`，`tools/translit.py chars --check` 只用於 zh-TW。
- Go 端：zh-CN 的 PlayerNames 包一層字級對照（`nameTransliterator` 介面）：先以 zh-TW 音譯器產生，再逐字轉換；`-` 與 `•` 直接
  通過；表外字元出現時該名字顯示英文（與音譯失敗同）。對照檔從共用 text 目錄讀取，載入失敗時 zh-CN 的 PlayerNames 停用、
  名字顯示英文，不讓語言失效。

### 3.7 驗證與字型

- 驗證命令以 `tools/zh_cn_check.sh`（Docker 內）統一執行，明列：`zh_cn_convert.py --check`（OpenCC image）、各家族驗證器
  `--lang zh-CN`、`name_glossary.py --lang zh-CN lint`、`catalog_font.py --lang zh-CN lint`、`header_columns.py --lang zh-CN`。
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
  未指定時自動載入 `font/buckrogers-<lang>.golemfnt`（存在時）。

## 4. 不做什麼

- 標點改大陸慣用（“”、·）；簡體專屬的譯文重寫；日文、韓文（042–045）。

## 5. 驗收

1. 產生器：兩次產生位元組相同；`--check` 通過；合成負例失敗——不變量違反、覆寫雜湊不符、孤兒覆寫、詞表含空白、詞條未命中、
   詞條在某處未產生 `cn`、遮蔽未處理、帳本缺項、名字寫法不一致、`chinese` 重複、音譯對照碰撞。
2. `zh_cn_check.sh` 全部通過；兩支字面驗證器的 zh-TW 行為不變。
3. 執行期：前端與收據工具載入後 zh-CN 在 F4 循環內；DebugSummary 無 zh-CN 停用與重建計數。
4. 同狀態收據（2×、3×）：規格 040 §5.3 的四個時點以 `-lang zh-CN` 輸出，記憶體與 CPU 雜湊與 zh-TW 相同；ECL、水平選單、手札
   截圖目視無缺字與溢出（手冊題時點只記雜湊）。三列變寬（呎→英尺兩列、`frag.5250b5de07b3`）以單元先建或針對性收據驗證整列寬度。
   玩家名：phase-286 的 `cp/a4`＋a5 按鍵停 2,861.5M，戰鬥右欄預期「弗拉维乌斯」。
5. 回歸：phase254 七條回歸（zh-TW）逐位元組不變。
6. 前端：冷開機切到簡體截圖；說明頁「目前語言」為簡體中文；打包產物含 zh-CN 字型並通過外洩掃描。
