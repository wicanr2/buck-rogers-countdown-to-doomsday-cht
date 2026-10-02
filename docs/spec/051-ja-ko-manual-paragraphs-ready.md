# 051 — 日文與韓文的手冊段落

狀態：**READY**（2026-10-02；實作與驗收見 phase-316；獨立審查的必修項已併入本版）。
驗收範圍：資料層、載入層、手冊題時點離線重播（2×、3×）與一題實機路徑（2×、3×）；其餘手冊題未逐題實機，故維持 READY，不升 CONFORMED。
日期：2026-10-02
Issue：#39
決定：使用者 2026-09-30 定案「日韓手冊題段落從繁中段落轉譯、加拉丁字母白名單防答案外洩、缺譯顯示原版英文」；2026-10-02 同意實作，並確認不縮小字型。
前置：規格 005（手冊 presenter）、034（本機英文關鍵字列，不屬發行包）、040（多語框架）、042、043（日文、韓文）。
與舊規格的關係：本規格取代 042 §3.9、043 §3.9 的「本期不做」與 042 §3.9 的「不得含拉丁字母」（改為白名單，見 §3.3）。

## 1. 為什麼要做

`text/manual.ja.tsv`、`text/manual.ko.tsv` 原本只有標頭（規格 042 §3.9、043）。ja、ko 的手冊查詢題因此顯示原版英文，沒有手冊段落。
簡體（zh-CN）已有 39 段（由繁中轉換）。這一版為 ja、ko 補上 39 段。

## 2. 證據（已證實，除非標明）

- 版面（`text/manual-overlay-layout.tsv`、`manual_overlay_runtime.go` 的 `confirmedManualOverlayLayout`）：36 欄 × 14 列，一列 72 半形單位，
  半形（ASCII、`•`）1 單位、其餘 2 單位；`manualRows` 逐字元換行（放不下的全形字整個移到下一列），超過 14 列即無效。
  **不做詞級換行**：韓文會在單字中間換列（與 zh 相同的逐字元行為）。
- 載入時（`validateManualCatalogFont`）任何一段放不下，`NewRuntimeManualOverlayLang` 回錯。**後果不只是手冊面板失敗**：
  通道建立失敗會把整個語言停用（`r.off[lang]`），該語言的其他家族也回到原版英文。所以放不下的段落不能入版，這是載入層的硬閘門。
- 3× 的語言通道不跑 `BuildManualE1Plan`（`e1Base` 只在測試用的 `NewManualSnapshotOwner` 設定），因此 3× 另需實機驗證（§5.4）。
- 現行 Python 檢查 `tools/manual_catalog.py`、`tools/manual_overlay_layout.py` 原本只比字元數（`len(translation) > 504`），不是半形單位與換列；
  ja、ko 需要與 Go 一致的檢查（`tools/manual_lang.py`，§5.1）。
- 量測（2026-10-02，`text/manual.zh-TW.tsv`）：39 段，`source` 欄全為 `manual-and-runtime`，單位數（半形 1、其餘 2）中位 242、最大 661；容量 1,008（14 × 72，逐字元換行的損耗另計）。
  手札長文的 ko／zh 單位比中位 1.41、ja 1.43；成稿後最長段落 ja 891、ko 886 單位（各一段，逐字元換列後 13 列；其餘不超過 12 列）。
- 執行期查表：手冊面板用 `entry.EventKey` 與 `TextKey` 查本語言 catalog（`translationFor`），譯文為空表示未翻譯、原版英文照顯示；
  `readTSV` 不接受空欄位，所以缺譯的表現是「缺 key」，不是空字串。
- zh-TW 譯文中的拉丁字母詞（NEO、RAM、能力與技能縮寫、`Salvation III`、`Scot.dos`、`Mariposa` 等）是公開發行的內容，白名單以此為界；ja、ko 不會比 zh-TW 多洩漏任何拉丁字母詞。

## 3. 契約

1. `text/manual.ja.tsv`、`text/manual.ko.tsv` 各 39 列，key 集合與順序同 `text/manual.zh-TW.tsv`，`source` 欄與 zh-TW 同列相同。
2. 來源：以 `manual.zh-TW.tsv` 的段落為翻譯來源（原版英文手冊不在翻譯輸入內），術語、專名與詞表（`name-glossary.<lang>.tsv`、`workplace` 的 `glossary.<lang>.tsv`）一致；
   具名人物依 `name_glossary.py lint`（zh-TW 該列有的人物，譯文也要有，例如 `Scot.dos` 在 ja、ko 寫成片假名、諺文）；
   ja 敘述用常體（だ／である），ko 用해라체，與規格 042、043 的風格一致；手冊的規則說明用中性平述。
3. 拉丁字母白名單：譯文中的拉丁字母詞（以字母或數字起頭，由 A–Z、a–z、數字與內部的 `.`、`-`、`'` 構成，至少含一個字母）集合必須是同一列 zh-TW 譯文中拉丁字母詞的子集
   （不得新增英文單字，不得拼出可還原原文的英文詞）；
   數字（含 `%`、小數）的多重集合必須與同一列 zh-TW 完全相同，不增不減不改。
   日文與拉丁字母詞（或數字）之間不加空白；韓文依 043 的띄어쓰기規則。
4. 容量：每段逐字元換列後**至多 13 列**（硬上限 14 列，留 1 列餘量），且總單位數至多 **960**（容量 1,008 的約 95%）。兩者都是政策值，擋在載入層的硬閘門之前。
5. 字集：ja 只用 `font/charset.ja.txt` 內的字，ko 只用 `font/charset.ko.txt` 內的字（ko 字集的全形標點只有「」『』，其餘標點一律用 ASCII）；
   字元清單 `font/characters.<lang>.txt` 仍只由正式譯文重新產生；字型由 `tools/package.sh` 重建。
6. 單一欄位：一段一列、無 tab、無真正的換行；段落內不得有 `\n`（手冊段落是單一段），首尾無空白。
7. 缺譯時的行為不變：缺 key 表示原版英文照顯示；本規格要求 39 段全部有譯文，不留空，也不再允許「只有標頭」。

## 4. 不在範圍

- 縮小字型、詞級換行、多頁手冊（使用者確認不改版面）。
- 日韓版的本機英文關鍵字列（規格 034，只在本機，不屬發行包）。
- 手冊以外的任何家族。
- 母語者校對（發行說明已有「機器輔助譯文」聲明，延伸到手冊段落）。

## 5. 驗收

1. 工具：
   - `tools/manual_lang.py`（新）：與 Go 等價的 `manualRows`、拉丁字母白名單、數字多重集合、字集、13 列／960 單位、tab／換行、ja 空白；`check` 子命令與 `--stats`。
   - `tools/lang_check.py` 的 `manual` 家族改用 `manual_lang.check_catalog`，移除「只准標頭」；`--expect-rows`、`--expect-keys` 期望值由 5,414／5,406 改為 **5,453／5,445**（+39 列、+39 個不同 key）。
   - `tools/manual_catalog.py`、`tools/manual_overlay_layout.py` 改用 `manual_lang.manual_rows`（單位與換列），不再比字元數。
   - `ja_check.sh`、`ko_check.sh` 納入 `manual_catalog.py`、`manual_overlay_layout.py` 與 `manual_lang.py check`；期望值同步改為 5,453／5,445。
   - 單元測試涵蓋每一項的違規例，並與 Go `halfwidth_part2_test` 的換列邊界對照。
2. 資料：39 段 × 2 語言，工具全綠（`ja_check.sh`、`ko_check.sh`、`zh_cn_check.sh`）。
3. 本機洩漏檢查（只在本機、不寫入 Git）：ja、ko 的拉丁字母詞都在同列 zh-TW 的集合內（由工具保證）；另以 ignored 的英文關鍵字摘錄實跑一次，答案詞出現在拉丁字母詞中的列數，ja、ko 須與 zh-TW 相同。不輸出、不記錄任何題目答案、關鍵字或該列數。
4. 載入層：`tools/package.sh linux` 以真實 catalog 與發行字型在 2×、3× 建立 ja、ko 的手冊 presenter，成功；`TestPackagedLanes` 斷言 `len(r.off)==0`（任一語言被停用即失敗）；
   `apps/buckrogers` 套件測試除既有失敗外無新增。
5. 實機層：同一固定腳本（含手冊查詢題）以 zh-TW、ja、ko 各跑一次（2×、3×）：`memory_sha256`、`cpu_sha256` 相同；ja、ko 的手冊頁畫出完整段落、無裁切，離頁（答對返回）無殘字；
   `-lang en` 顯示原版。手冊題畫面不入 Git，也不描述內容。
6. 文件與 pointer：README、`讀我.txt`、發行說明中「手冊題的段落仍顯示原版英文」的敘述改為現況；規格 042 §3.9、043 §3.9 加指向本規格的 pointer；`docs/re/` 加收據文件與索引。

## 6. 風險

- 韓文在單字中間換列，可讀性較差；若不可接受，另開規格處理詞級換行（需要重算容量）。
- 最長的一兩段貼近上限：譯文階段要求精簡，工具擋住超出者；之後改動 zh-TW 段落會連帶影響白名單與數字核對。
- 機器輔助譯文，未經母語者校對。
- 3× 通道與手冊 presenter 的路徑與 2× 不完全相同（§2），不得以 2× 結果推論 3×。
