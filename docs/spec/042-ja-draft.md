# 042 — 日文（ja）

狀態：**DRAFT**（2026-09-30）
日期：2026-09-30
Issue：#35
前置：規格 040（多語框架）、039（半形）、036／038（名字）、030（手札）、027–029、005／034（手冊）。
後續：043 韓文、044／045 日韓音譯器（各自另訂）。
證據：[phase-300](../re/phase-300-ja-translation-batches.md)（批次翻譯、檢查、收斂、zh-TW 疑似錯誤）；
Unifont 授權與字形、ECL 禁則的原始調查在 ignored 的 `workplace/ja-l10n/survey.md`。

## 1. 為什麼要做

使用者決定（2026-09-29、09-30）：F4 循環加入日文；以英文原文為源、繁中為語境參考，子代理批次翻譯並統一詞表；
敘事與手札用常體，對白依角色，人名用片假名，NEO、RAM 等組織名留英文；標示為機器輔助譯文、未經母語者校對；
日韓手冊題段落從繁中段落轉譯；缺譯顯示原版英文。日文玩家名用片假名音譯（規格 044）。

本規格定義**日文譯文資料、檢查、排版禁則、字型與驗收**。手冊 39 段與玩家名音譯不在本規格第一期（§4、§6）。

## 2. 證據

- 譯文（已證實，phase-300）：46 批、5,406 個 key、30 個家族檔，逐批與合併後 `check_done.py` 錯誤 0；用字 1,743 個，
  全在允許字集內。
- 字型（已證實，`workplace/ja-l10n/survey.md`）：發行用 `unifont_all-17.0.05.hex.gz` 的 6,356 個 JIS X 0208 漢字與
  `unifont_jp` 逐位元相同（izmg16 排在 wqy 之前）；平假名 86／86、片假名 94／94 皆有 16 寬字模；`…`、`―` 只有 8 寬字模，
  由 `catalog_font.py` 置中轉 16 寬（繁中的「……」已走同一路徑）；`～`（U+FF5E）、`－`（U+FF0D）不在允許字集。
  授權：Unifont 雙授權（OFL-1.1 與 GPL-2.0-or-later 含字型嵌入例外），與現行發行條件相同。
- 排版（已證實，dosgolem `12a684b`）：`ecl_text.go` 的 `layoutEclTextUnits` 只有拉丁連續字不拆、`isEclClosing`
  只含 `，。！？：；、」）…》』,.!?:;)`，沒有行尾禁則；手札 `logbook.go` 逐段呼叫同一函式；引擎片段被自動換行拆兩列時
  （`engine_dispatch.go` `joinWrapped`）沒有任何禁則。
- 語言接口（已證實，dosgolem `12a684b`）：`LangCycle` 已含 `ja`；名字詞表與例外表讀 `name-glossary.<lang>.tsv`、
  `name-glossary-exclude.<lang>.tsv`；`nameTransliterator` 為每語言介面，未提供時玩家名顯示英文（`playersOff`）。

## 3. 契約

### 3.1 檔案

- `text/<family>.ja.tsv`，欄位 `key`、`translation`、`source`（固定值 `ja-machine-assisted`）。範圍：phase-300 的 30 個家族
  （body-icon、career-skill-screen、character-sheet、class、coordinate-line、ecl-text、engine-fragment、engine-template、gender、
  hmenu、item-word、logbook、logbook-panel、menu、monster-name、name-prompt、post-join-exit-prompt、post-join-menu、
  save-roster-join、skill-action-bar、skill-exit-confirmation、story-opening、story-page2–9、technical-skill-screen）。
  key 集合是同家族 zh-TW 檔的子集（規格 040 §3.1），順序與 zh-TW 相同。
- 不產生 ja 檔的家族：`translit-chars`（玩家名音譯字集，規格 044）、`host-ui`（設定面板與說明頁用 zh-TW，規格 040 §3.4）、
  `manual-english-panel`（只在 zh-TW 顯示）、`manual`（§3.9，本期缺譯，手冊題顯示原版英文）。
- 譯文不進入比較、查找、序列化、檔案路徑或存檔（AGENTS.md）；英文原文與批次檔不進 Git。

### 3.2 風格與用語（給人與工具共同遵守）

- 敘事、手札、系統訊息用常體（だ／である）；固定請求句（例：載入中）可用敬體；對白依說話者（軍官簡潔、海盜粗魯、
  學者囉唆、RAM 的人工智慧冷硬、低地人在さ行前加促音「っ」表現口音、太陽王自稱「余」）。
- 稱呼玩家：敘事與手札「君たち」，系統提示（水平選單、DOS 訊息、介面）「あなた」。
- 數字用半形阿拉伯數字；貨幣 CR 譯「クレジット」；標點用全形「」『』、。！？：；，刪節號「……」、破折號「——」；
  原文單引號對白一律改「」；不用半形片假名、全形英數、U+3000、`～`、`－`。
- 拉丁字母：只保留 zh-TW 該列本身保留的詞（NEO、RAM、ECG、DOS、PgDn 等），不得新增英文單字，日文與拉丁字母之間不加空白。
- 玩家冒險日誌（繁中「手札」）稱「日誌」，編號「日誌n番」；裝置紀錄稱「記録」；「手札」在日文指手牌，不用。
- 統一用語與人名以 `workplace/ja-l10n/glossary.ja.tsv` 為準（含英文，不進 Git）；進 Git 的名字資料是 §3.8。
  跨批次已裁決的用語清單見 phase-300 §4。

### 3.3 檢查工具 `tools/ja_check.py`（不含英文，Docker 內執行）

phase-300 的 `check_done.py` 依賴英文與批次檔，不進 Git。進 Git 的檢查改以 zh-TW 與事件檔為基準，逐列驗證：

1. 結構：key 屬同家族 zh-TW；NFC；無 tab、換行、控制字元；非空；無重複 key。
2. 佔位符 `{n}` 的多重集合與 zh-TW 相同；`\n`（兩字元）數量與 zh-TW 相同。
3. 熱鍵：zh-TW 有 `(X)` 的列，日文恰有一個半形 `(X)`，字母相同；水平選單列的大寫 ASCII 與數字集合與 zh-TW 相同。
4. 拉丁字母：日文列的拉丁字母詞集合是 zh-TW 該列的子集；zh-TW 無拉丁字母的列，日文亦不得有（含 `\n` 後接字母的誤判由
   token 化處理：把 `\n` 先移除再取詞）。
5. 寬度（半形 1 單位、其餘 2 單位）：上限依家族由事件檔與安全矩形重算——水平選單 `max(2×original_length, zh-TW 寬)` 且不超過
   `2×(40−起始欄)`；引擎片段、物品詞、怪物名 `2×original_length`；角色頁、選單、動作列等 `capacity_cells×2`；劇情頁每列 78；
   ECL 單頁 456（警告：超過 zh-TW 1.6 倍）；手札每則 3 頁。超過上限為錯誤。
6. 字集：全部字元屬 `font/characters.ja.txt`（§3.7），且不含 §3.2 禁用字元。
7. 引號：每列「開引號數減關引號數」與 zh-TW 相同（跨列引號照 zh-TW 的開關）。
8. 名字：每列出現的名字寫法與 `name-glossary.ja.tsv` 一致（重用 `name_glossary.py --lang ja` lint）。
9. 合成負例測試（必做）：佔位符缺失、熱鍵字母不符或重複、多出拉丁字母詞、超寬、字集外字、引號不平衡、名字寫法不一致、
   key 不在 zh-TW、`\n` 數量不符。

### 3.4 排版禁則（dosgolem）

每語言一份排版設定（layout profile），預設值等於現行行為，zh-TW 與 zh-CN 不變（phase254 逐位元組相同）。日文設定：

| 類別 | 規則 |
|---|---|
| 不放列首 | 小書き假名（ぁぃぅぇぉっゃゅょゎゕゖ ァィゥェォッャュョヮヵヶ）、長音符「ー」、反覆記號（ゝゞヽヾ々〻）、中黑「・」、閉括號補齊（】〕］｝〉〙〗’”）、全形句點「．」，併入現有 `isEclClosing` 集合 |
| 不放列尾 | 開括號（「『（【〔［｛〈《‘“），與下一個 token 黏在一起 |
| 不拆 | 連續的「……」「——」當一個 token，且不放列首 |
| 引擎片段兩列拆分 | `joinWrapped` 的拆點套用同一組列首與列尾禁則 |

拉丁連續字與半形數字維持不拆；名字加註單位（規格 036）維持現行。行尾禁則對 zh-TW 與 zh-CN 不啟用（設定預設關閉）。

### 3.5 載入與錯誤隔離

- 語言碼 `ja`（已在 `LangCycle`）；載入驗證、錯誤隔離、缺譯粒度依規格 040 §3.3；字型檔 `font/buckrogers-ja.golemfnt`。
- 載入驗證逐語言逐倍率建 presenter 內容，暴露真實的容量、缺字與墨跡問題（`check_done.py`／`ja_check.py` 只驗上限公式）。
  驗收要求該驗證對全部 5,406 列零失敗；失敗列退回翻譯者重譯，不以放寬檢查處理。
- 動作列：每則譯文含恰好一個 `(X)`，字母等於 zh-TW（規格 040 §3.1）；加入後選單 7 項為一組，可為 0 或 7 列。

### 3.6 半形與全形

- 規格 039 的半形 ASCII 適用日文；日文間隔號「・」（U+30FB）佔 2 單位，比繁中 `•` 多 1 單位，不做半格處理。
- 名字加註「カタカナ(English)」：括號內英文半形；多段名字（例：「バック・ロジャーズ」）在窄欄只顯示片假名。

### 3.7 字型

- `font/characters.ja.txt` 由正式日文譯文產生（可見 ASCII 加譯文用字，預計約 1,750 字）並進版控；必須是 `charset.ja.txt`
  （JIS X 0208 且 Unifont 日文字形有 16 寬字模）的子集。
- `tools/catalog_font.py --lang ja` 從 `unifont_all-17.0.05.hex.gz` 產生 `font/buckrogers-ja.golemfnt`（JIS 漢字為日文字形，
  與現行來源相同，不另引入 `unifont_jp`）；授權檔隨發行包（`OFL-1.1.txt`、`COPYING`）不變。
- 本機字型放 `workplace/lang-fonts/`（規格 041 §3.7）。倚天字型缺假名與日文漢字，不用於日文。

### 3.8 名字

- `text/name-glossary.ja.tsv`（欄位同 `name-glossary.tsv`，`chinese` 欄改放片假名寫法；`basis` 記 `ja-glossary`）與
  `text/name-glossary-exclude.ja.tsv`。來源為詞表 `name` 段 42 列（人名、店名綽號依詞表），名與姓之間用「・」。
- 檢查：日文譯文中每個名字出現處與名字表一致；片假名寫法唯一；例外片語在每個出現處同樣一致。
- 玩家名：規格 044 之前 ja 的 `PlayerNames` 停用，名字顯示英文（`no-transliterator`），不讓語言失效。

### 3.9 手冊題（本期不做）

- 手冊 39 段（`manual.ja.tsv`）另訂：從繁中段落轉譯，504 格單頁，不得含拉丁字母（防答案外洩），並保存題目證據、繁中段落
  來源與收據（AGENTS.md）。本期 ja 模式手冊題缺譯，顯示原版英文（規格 040 缺譯粒度：手冊以段落為單位）。
- 手冊題提示句（引擎片段中「日誌の第Nページ、見出し…」）已翻譯，語意不含答案。

### 3.10 打包與同步

- `tools/package.sh` 語言清單加 `ja`；前置檢查執行 `tools/ja_check.py`（失敗即中止）；打包內容加 `font/buckrogers-ja.golemfnt`
  與 `text/*.ja.tsv`、名字表；外洩掃描維持（日文譯文不含英文原文）。
- 修改任何 `*.zh-TW.tsv` 而使日文列結構失效（key 消失、佔位符或熱鍵改變）時，`ja_check.py` 失敗，遺漏由打包前置檢查擋下。
  日文內容本身不隨 zh-TW 自動更新。

## 4. 不做什麼

- 韓文（043）、日韓音譯器（044／045）、手冊段落（§3.9）、母語者校對、母語者風格重寫。
- 修正 zh-TW 端的疑似錯誤（phase-300 §5，另案）與 Unifont 對繁中與簡體的日文字形問題（Issue #36）。
- 標點改直排、旁白時態統一、依性別的代名詞處理（日文不分性別，性別片段以中性譯法為準）。

## 5. 驗收

1. `tools/ja_check.py` 對 30 個 ja 檔全綠；合成負例全部失敗（§3.3 第 9 項）。
2. 字型：`font/characters.ja.txt` 為 `charset.ja.txt` 子集；`font/buckrogers-ja.golemfnt` 涵蓋全部日文譯文用字；打包字型雜湊可重建。
3. 載入：前端與收據工具載入後 ja 在 F4 循環內；DebugSummary 無 ja 停用與重建計數；presenter 載入驗證對全部列零失敗。
4. 排版：禁則的單元測試（列首、列尾、成對符號、引擎片段兩列拆分）通過；zh-TW 與 zh-CN 的逐位元組回歸不變。
5. 同狀態收據（2×、3×）：規格 040 §5.3 的四個時點以 `-lang ja` 輸出，記憶體與 CPU 雜湊與 zh-TW 相同；ECL、水平選單、手札、
   劇情頁截圖目視無缺字與溢出。抽測片段串接：至少涵蓋動詞後置片段（含名字夾在片段之間）、引擎片段、名字加註各一條真實遊戲路徑。
6. 回歸：phase254 七條回歸（zh-TW）逐位元組不變。
7. 前端：冷開機切到日文截圖；說明頁「目前語言」列出日文；打包產物含 ja 字型並通過外洩掃描。

## 6. 開放項目與消除條件

| 項目 | 消除條件 |
|---|---|
| 水平選單寬度上限是否可放寬（目前數十處縮寫成非正確譯名，例：主角名、艦名、部分技能名） | 量原版該列在項目右側的空白格；能借用者放寬並重譯，不能者維持 |
| 片段串接品質（動詞後置、名字夾在中間；批次回報標記的數十處） | 驗收第 5 項的真實路徑抽測；發現不通順者退回重譯 |
| 母語者校對 | 有母語者審閱後另訂規格；在此之前 README 與說明頁標示機器輔助譯文 |
| 手冊段落 | §3.9 另訂規格 |
| 玩家名音譯 | 規格 044 |
| zh-TW 疑似錯誤 | phase-300 §5 另案修正並重做該畫面 A/B，日文不受影響 |
