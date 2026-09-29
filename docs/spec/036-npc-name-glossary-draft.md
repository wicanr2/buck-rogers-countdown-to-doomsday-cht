# 036 — 具名人物譯名表與「中文(英文)」顯示

狀態：**DRAFT**（2026-09-29）
日期：2026-09-29
Issue：#33
前置：規格 027（ECL 敘事窗）、028（水平選單）、029（引擎訊息與怪物名）、030（手札面板）、
010／015（固定劇情逐頁）、024（字型身分）。玩家角色名另見規格 037。

## 1. 為什麼要做

使用者決定（2026-09-29）：具名人物在寬的文字區顯示「中文(英文)」，窄欄只顯示中文。現行譯文有 8 組
人名不一致，也有錯譯（開場第 6 頁把原文 `CARLTON TURABIAN` 寫成錯拼的英文；手札第 48 則把普通名詞
*the orphan* 譯成人名）。

## 2. 證據（本機盤點，報告不入庫）

- 具名人物約 30 位（Buck Rogers、Wilma Deering、Carlton Turabian、Holzerhein／.dos、Talon、Gilbert、
  Milo Phillips、Jim、Tuskon、Atha、Leander、Landon、Zane、Justin Robeno、Jason Dupare、Gavilan、
  Scot.dos、Huer.dos、Dr. Williams、Dr. Conchitez、Garrity、Bobby、Kilroy.dos、Barney、Max Wyman、
  Vilnikov、Powell、Severn，以及只出現在怪物記錄的 Beowulf Sand、Carlos Rioja、Jason Braga）。
  原文出處是 ignored `workplace/` 的 ECL、手札、選單、怪物名來源檔（已證實，雜湊比對）。
- 版面（已證實，規格條文）：怪物名與引擎訊息只能畫在原文格內（029）；水平選單總寬受限且 ASCII 大寫會被
  畫成熱鍵色（028）；ECL 敘事窗的視窗大小是執行期參數，超出可用列數整窗退回英文（027 §3.4）；
  手札每則最多 3 頁、每頁 684 格（030）；固定劇情逐頁每行有上限（010／015）。

## 3. 契約

### 3.1 譯名表 `text/name-glossary.tsv`

- 欄位：`english`（原版大小寫，ECL 為全大寫）、`english_mixed`（手札等混合大小寫來源的寫法，可空）、
  `chinese`（正式中文名）、`kind`（full／short，全名或單稱）、`person`（同一人物的識別碼）、
  `basis`（`printed:<頁或位置>` 中文印刷手冊、`xinhua` 新華社式音譯、`nickname` 意譯綽號）、`note`。
- 譯名基準（使用者定案）：中文印刷手冊有的沿用；沒有的用新華社式音譯。印刷手冊的依據要在本機以
  手冊 OCR／crosswalk 核對並記在 `basis`，核不到的一律不得標 `printed`。
- 間隔號統一為 `•`（U+2022）。
- 例外清單 `text/name-glossary-exclude.tsv`：含人名字樣但不是人名的中文片語（店名等），比對時整段跳過。
- lint（`tools/name_glossary.py lint`）：同一 `person` 的 `chinese` 在所有 `text/*.zh-TW.tsv` 只准出現表中的
  寫法；舊寫法（例如同一人的第二種譯法）一律報錯；新增字要在字型子集。

### 3.2 譯文收斂（一次性資料修改）

- 以譯名表把所有 catalog 的人名收斂成正式中文（例：Zane、Dr. Williams、Dr. Conchitez、Max Wyman、
  Holzerhein 各種寫法）。
- 移除譯文裡既有的「（English）」人名註記（手札、手冊），改由 §3.3 在執行期統一加註；
  手冊段落（`manual.zh-TW.tsv`）只做中文收斂，不加註（版面固定且涉及查詢題）。
- 手札第 48 則「歐凡」改回「孤兒」（含標題）。
- 開場第 6 頁 `story.page6.line.003`：改成正式中文名並重新斷行；本頁與 `story.opening.line.001` 依 §3.3 規則處理
  加註，重做規格 015／010 的同狀態 A/B。
- 修改前後的 catalog 由 `tools/name_glossary.py apply --dry-run` 列出每筆替換（key、舊、新），人工抽審後才寫回。

### 3.3 執行期加註（顯示層）

- 加註規則：在「寬家族」的譯文中，找到譯名表的 `chinese`（最長優先、跳過例外片語、已緊接 `(` 的不重複加），
  在其後插入 `(` + 英文 + `)`，英文用該家族的原版大小寫（ECL 用 `english`，手札用 `english_mixed`，空則用
  `english`）。每次出現都加。
- 寬家族與退路：
  - ECL 敘事窗（027）：先以加註後文字排版；超出可用列數時改用未加註的原文字排版；仍超出才照 027 的
    overflow 退回英文。overflow 計數分開記「加註退回」與「整窗退回」。
  - 手札面板（030）：加註後超過 3 頁時改用未加註文字。
  - 固定劇情逐頁（010／015）：頁內換行是預先斷好的，不在執行期加註；§3.2 直接把加註寫進該兩行的譯文並
    重新斷行，通過該頁行寬驗證才生效。
- 窄家族不加註：怪物名、引擎訊息與片段（029）、水平選單（028）、手冊段落、各 UI 畫面。
- 加註只影響顯示，不進任何比對、雜湊、存檔或原版語意路徑。

### 3.4 字型

- 新譯名用字（新華社式音譯新增的字）經正式 catalog 進字型子集；加註的英文走原版 ASCII 字模（規格 031）。

## 4. 不做什麼

- 玩家角色名（規格 037）。
- 手冊段落加註、怪物名與選單加註。
- 無名敵人種類。

## 5. 驗收

1. `tools/name_glossary.py lint` 對全部 catalog 通過；`apply --dry-run` 清單經人工抽審，無誤替換（特別是店名與
   含人名字樣的片語）。
2. 單元測試：加註的最長優先、例外跳過、已有括號不重複、大小寫依家族、ECL 退路三段、手札 3 頁退路。
3. 同狀態 A/B：phase254 七條回歸與既有 ECL、手札 A/B 重跑；差異只能出現在人名處（加註或收斂後的中文），
   逐一核對；開場第 6 頁與第 1 頁重做 A/B。
4. 前端端到端：到含 Buck Rogers／Turabian 的敘事、手札至少各一則，截圖確認加註；戰鬥或選單中同名人物只顯示中文。
5. 字型重建後零缺字；一般版外洩掃描照常通過。
