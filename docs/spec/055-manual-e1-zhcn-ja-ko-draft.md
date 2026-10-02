# 055 — 手冊 E1 擴及 zh-CN、ja、ko（3×）

狀態：**DRAFT**（2026-10-02，第二版；第一輪獨立審查的必修 3 項與建議 10 項已併入，待複審）。
日期：2026-10-02
Issue：#40
決定：使用者 2026-10-02 選定規格 053 這一輪只接 zh-TW，zh-CN、ja、ko 另開 Issue（#40）。本規格沿用 053 的啟用、預檢、退路與不變量，只寫三種語言與 zh-TW 不同之處。
前置：規格 053（E1 接線，限縮 CONFORMED）、005（手冊 presenter）、051（ja、ko 手冊段落）、039（半形）、040（多語通道）、dosgolem 規格 234（共用繪字層）。

**取代規格 053 的條文**（實作時在 053 對應處標註「2026-10-02 起見規格 055」）：§3.1 首段「zh-CN、ja、ko 的 `e1Base` 必為 nil」、§3.3 第 1 點「3× 的 zh-CN、ja、ko 與實作前逐位元組相同」、§5.1 的啟用矩陣與「五種語言 `Compose(3)` 位元組不變」、§5.5 只斷言 zh-TW 的 `manual-e1=on`、§4 第一項。其餘條文（預檢順序、退路、並存、zh-TW 的輸出）不變。

## 1. 為什麼要做

規格 053 讓 zh-TW 的 3× 手冊用 E1：段落中保留的拉丁字母詞與括號專名整詞換行，不在列尾被拆開；E1 另外把列首列尾的空白歸零，並禁止終端標點與右括號出現在行首。
zh-CN、ja、ko 的 3× 仍用固定格逐字元換列，同樣的專名會被拆成兩段；ja 的括號專名（括號與其中的縮寫）在固定格也會在括號處斷成兩列。

## 2. 證據

來源：離線探針（`workplace/phase320/`，ignored），dosgolem `039727e` 的乾淨副本；正式 `text/manual.<lang>.tsv` 與各語言通道自己的發行字型，3×，在 Docker、`--network none`、唯讀輸入下執行。
放寬版（§3.1）的數字出自「探針副本」與審查者依 §3.1 原文另寫的參考實作兩份程式，結果逐段相同；探針副本不作為實作依據，實作以 §3.1 為準。

已證實：

1. **現行程式的預檢**（`enableManualE1` 對各語言通道自己的字型與 catalog 逐段建 plan 與 `TextLayer`）：zh-CN 39／39；ja 39／39；ko 0／39，錯誤是 `E1 connector U+002E is outside an identifier`（39 段都含 ASCII 句點）。
   zh-CN 與 zh-TW 的字元種類與計數完全相同（規格 053 的 39／39）。
2. **ko 的字元**（`text/manual.ko.tsv`，只記種類與計數）：諺文 5,231、空白 1,954、拉丁字母 559、數字 95、ASCII `.` 192（含 3 段共 4 處的 `...`）、`,` 156、`:` 29、`(` 38、`)` 38、`!` 6、`?` 1、`+` 13、`-` 9、`%` 3、`/` 2、`「` `」` 各 18。
   兩個 `/`：一個在拉丁識別字內（zh-TW 同位置也有），一個在兩個諺文詞之間。三種語言的 catalog 都沒有空白起首或結尾、連續空白、空白在標點之前（計數 0）。
3. **現行 plan 對 ASCII 標點的處理**（039727e）：`.` 與識別字之外的 `/` 是 connector 錯誤；`, : ! ?` 不是錯誤，而是獨立的半形 token（可以出現在行首、段首、空白之後）。ko 的預檢失敗只來自 `.` 與一個 `/`。
4. **放寬後**（§3.1）：四種語言預檢都 39／39；E1 列數不大於固定格列數（zh-CN 38 段相等、1 段少一列，同 zh-TW；ja 39 段相等，最大 13 列；ko 39 段相等，最大 13 列）。
   審查者用 §3.1 原文另寫的參考實作：zh-TW、zh-CN、ja 的 39 段 `CanonicalHash` 與 039727e 逐段相同；`apps/buckrogers` 全套件（設 `BUCK_OWNER_PROJECT`）無既有測試翻轉（456 PASS、0 FAIL、20 SKIP）。
5. 逐段 `Apply`、`Frame`、`Draw`（3×）：E1 與固定格的畫面相同／不同的段數：zh-TW 15／24（與規格 053 §2 相同）、zh-CN 15／24、ja 12／27、ko 13／26；四種語言都沒有缺字或未畫的段落，不同處的像素都在手冊清底矩形（x21 y216 w915 h336）內，矩形外零差。
   差異成因（審查者以固定格換列的啟發式分類，未逐項消融驗證，屬推論）：ko 的 26 段「不同」全部在列界上相鄰 ASCII 空白（空白歸零）；ja、zh 的「不同」除了拉丁詞與括號專名保護之外，也有行首禁則（終端標點不起頭）造成的差異。
6. 畫面（僅本機檢視）：ja 的括號專名在固定格被拆在兩列，E1 整組移到下一列。沒有溢出矩形。
7. 既有 `TestManualE1PlanRejectsOrphanASCIIConnectors` 的六個負例（`.RAM`、`RAM/`、`RAM++1`、`A - B`、`%RAM`、`RAM%%`）是 plan 的現行負面契約；§3.1 的實作仍全拒。
8. 離線快照與實機路徑的 E1 差異集合（審查者用逐段比對與畫格遮罩得出，只記 key 與計數；實作時以單元測試與畫格比對重新確認）：四種語言都「不同」的題共 16 題；現有唯一的離線快照（`phase12-before-question.state`，題為 `manual.page34.deimos_prison.word10`）
   在 zh-TW、zh-CN、ja 是「不同」，ko 是「相同」（k = k' = 3，位元組相同）；規格 053 的實機路徑（`path-repair.txt`）在 3060、3500 格顯示 `manual.page23.scots_alarm.word4`，四種語言都是「不同」。

未知：zh-CN、ja、ko 的 E1 在不同英文詞界的實機樣本（§5 補）；日後譯文改變使某段 E1 超過 14 列時（預檢失敗）該語言的 E1 整體關閉，目前沒有這種段落。

## 3. 契約

### 3.1 plan 的放寬（共用程式，`manual_e1_plan.go`）

實作位置：`manualE1PlanTokens` 的 else 分支與 `manualE1PlanMeasure` 的 default 分支**兩處**都要改（`manualE1PlanAppendTerminal` 會把 cluster 重新測量）；兩處共用同一個判斷函式，
`/` 的前一字元條件放在 `Tokens`（`Measure` 看不到上下文，對已折好的 cluster 只做半形測量）。

- **ASCII 終端標點** `.`、`,`、`:`、`!`、`?`：在 ASCII 識別字之外（識別字內的 `.`，例如 `3.5`，仍走現行 connector 規則）一律視為 terminal，折進前一個 token（成為 cluster），與現行的終端全形標點同類；連續的標點（`...`）逐個折進同一個 cluster。
  - 這是**新規則**：現行 039727e 對 `.` 報 connector 錯誤，對 `, : ! ?` 則當獨立半形 token（可在段首、空白後、左括號後出現，也可在行首）。
  - 拒絕條件：位置在段首、前一個 token 是空白、或位置在括號內部的第一個 token（沿用現行終端標點的 `begins paragraph` 錯誤）。對 `, : ! ?` 這是收緊；三種語言現行 catalog 在這些位置的出現次數為 0（§2 第 2 點），所以現有版面不變。
  - 行首禁則：終端標點（含上述五個）不得出現在行首（折進前一個 token 已保證）；既有的右括號、左括號禁則不變。
- **`/`**：在識別字之外，前一個字元存在且不是 ASCII 英數時，同上折進前一個 token（同樣的拒絕條件）；其餘情形（含 `RAM/`、段首）維持現行的孤兒 connector 錯誤。
  性質：`甲/RAM`、段尾 `甲/` 會被接受；`RAM/` 被拒。
- `+`、`-`、`%` 與其他字元的規則不變。
- 測量：cluster 的寬度是前一個 token 的寬度加上該標點的半形進位（`isHalfwidth` 路徑，`manualE1PixelLatin` = 12）；`TextLayer` 用半形字繪製（已證實無缺字）。
- **zh-TW、zh-CN、ja 的 plan 不變**：正式三份 catalog 共 117 段的 plan 版面與放寬前逐字相同（A、B 兩個乾淨匯出逐段比 `CanonicalHash`；另有單元測試凍結版面摘要，見 §5.1）；六個負例仍被拒。
  `manualE1LayoutDomain`（`-v2`）不改：沒有持久化的雜湊，且現有 catalog 的版面不變。

### 3.2 啟用條件

E1 在下列條件**全部成立**時啟用：語言通道為 zh-TW、zh-CN、ja 或 ko、倍率為 3×、載入時預檢全部通過（各通道用自己的字型與自己的 catalog，規格 053 §3.1 的預檢與 §3.2 的建立順序不變）。
`LangTest` 與英文（原版）不啟用；2× 一律不啟用。預檢任一段失敗，該通道的 `e1Base` 為 nil，通道照常運作（固定格）。通道之間互不影響（各自預檢、各自退路）。
每次載入的預檢成本由約 0.1 秒（zh-TW）變成約 0.4 秒（四個通道）。
實作位置：`manual_e1_live.go` 的 `setupManualE1`（語言條件）與 `manualE1Active`（寫死 zh-TW，只供關鍵字並存檢查使用，維持 zh-TW）、`live_lane.go` 的 `syncManual`（退路條件的 `l.lang == LangZhTW`）、`live_runtime.go` 的 DebugSummary；
`TestModeResetClassifiesEveryField` 是反射測試，新增任何 `liveLane` 或 `LiveRuntime` 欄位都要入表。

### 3.3 與本機英文關鍵字列

只有 zh-TW 通道有英文關鍵字列。規格 053 §3.4 的並存檢查（`checkManualE1Keyword`）只對 zh-TW 通道執行，行為不變；zh-CN、ja、ko 沒有關鍵字列，E1 不受它影響。

### 3.4 DebugSummary 與 runtime 退路

- zh-TW 區段的 `manual-e1=` 照舊。其餘通道在自己的區塊內（`lane[<lang>]={…}`）加 ` manual-e1=<status>`，位置在該通道的 `halfFontError()` 與 `counters()` 之間；狀態字串：`on`、`off(preflight:M)`、`off(runtime)`。`off(keyword:N)` 只會出現在 zh-TW。
  `LangTest` 通道沒有 E1，區塊內不出現 `manual-e1`。只有計數與固定代碼，不含譯文、錯誤原文、字元或 EventKey。診斷輸出現在最多有四處 `manual-e1=`（zh-TW 一處、其他通道各一處），以字串取單一值的腳本要逐區塊解析。
- runtime 退路（規格 053 §3.1）對所有啟用 E1 的通道一視同仁：3× 的 `Sync()` 回錯且該 presenter 的 `e1Base != nil` 時，該 presenter 改走固定格並再 `Sync()` 一次；第二次仍失敗照舊 `resets["manual"]++`、不再重試；
  只有第二次成功才標 `off(runtime)`。

### 3.5 不變量

1. 2× 的所有語言與 3× 的英文（原版）：`LiveRuntime` 合成 RGBA 與實作前逐位元組相同。
2. 3× zh-TW：與實作前逐位元組相同（規格 053 的輸出不因本規格改變）。
3. 3× zh-CN、ja、ko：與實作前相比，矩形外零差；矩形內可以相同也可以不同（zh-CN 15 段、ja 12 段、ko 13 段本來就相同；會不同的集合由單元測試列出，只記 key）。
4. 機器狀態（記憶體、CPU、indexed、palette、停止步數）與倍率及 E1 開關無關，逐位元組相同。
5. 離頁後手冊矩形與原版英文通道逐位元組相同（無殘字）；換題、返回的生命週期與現行相同。
6. 保留的英文專名（連續 ASCII 字母數字詞，含括號專名）不被列尾拆開；每列、全部字模與清除範圍都在既有安全矩形內。
7. 失敗隔離：任一通道預檢或 runtime 失敗只關該通道的 E1，不停用通道，不影響其他通道，不使手冊家族卡住。

## 4. 不在範圍

- 諺文的詞級（空白處）換行：E1 的 ko 維持字元級換列，斷行單位與規格 051 的固定格相同；與固定格的差異只有 E1 本來就有的三項：拉丁詞與括號專名整詞換行、列首列尾空白歸零、終端標點與右括號不起頭。
- 譯文改動、段落精簡（預檢全過，不需要）。
- 2×、`xlate` 共用層、字型、catalog、關鍵字列的版面。
- zh-TW 的任何行為變動。

## 5. 驗收

A、B 比對各自從**乾淨匯出**建置（A 是實作 commit 的父 commit，B 是實作 commit；用 `workplace/phase317/build-ab.sh` 的做法，不用從工作樹建的 `phase316/build-runner.sh`，否則會編進未入版控檔；記兩個 commit SHA 與兩個 binary 的 SHA-256），
同一份 `text/`、同一組發行字型（記 SHA-256）、同一個快照與腳本；測試套件也在乾淨匯出上跑。比對腳本改自 `phase317/offline.sh`、`live-ab.sh`、`compare-ab.py`（後者寫死 `L != "zh-TW" or sc != 3` 即判失敗，要改成依語言判定）。

1. 單元測試（dosgolem）。下列測試各自需要的環境變數：plan 與合成測試不需要；正式 catalog 預檢與啟用測試需要 `BUCKROGERS_CHT_ROOT` 與 `BUCKROGERS_{ZHTW,ZHCN,JA,KO}_FONT`（沿用 `ja_test.go` 的慣例）；
   沿用倚天字型的既有私有測試仍由 `BUCK_OWNER_PROJECT` 閘控。本規格新增的閘控測試必須 PASS 而不是 SKIP，其餘 SKIP 列入收據。
   - plan 放寬：終端 ASCII 標點在拉丁詞、諺文、數字、右括號之後折進前一個 token 且寬度為前者加半形進位；`...`、`...」`、`(甲...)`、`「甲.」`；`/` 的兩種位置（`甲/乙` 接受、`RAM/` 拒絕、`甲/RAM` 接受）；
     段首、空白之後、括號內第一個 token 的 `. , : ! ?` 與 `/` 被拒（對 `, : ! ?` 是新增的拒絕）；§2 第 7 點的六個負例仍被拒；`+`、`-`、`%` 的孤兒仍被拒。
   - zh-TW、zh-CN、ja 不變：三份正式 catalog 共 117 段的 plan 版面摘要與放寬前相同。摘要定義為（行號、token 種類、runes、x、advance）的雜湊，不含字型 seal（seal 隨字型重建而變）；
     版面對字型的依賴只剩全形括號的 advance，所以以發行字型為前提並由環境變數傳入，摘要在放寬之前以現行程式求得並寫死。
   - 啟用矩陣：{zh-TW, zh-CN, ja, ko, LangTest} × {2×, 3×}，只有前四種語言的 3× `e1Base` 非 nil（反轉規格 053 的矩陣與 `packaged_lanes_test.go` 的「非 zh-TW 的 `e1Base` 為 nil」斷言；`manualE1LiveLane` 輔助函式加語言參數）；各通道預檢 39／39。
   - 預檢失敗負例：各語言的合成 fixture（固定格剛好 14 列、E1 超過 14 列）使該通道 `e1Base` 為 nil、通道仍啟用、該通道區塊含 `manual-e1=off(preflight:`，其他通道不受影響；另一個含空譯文段落的非 zh-TW 通道：預檢略過該段、顯示走 `Missing`。
   - runtime 退路與 compose 防禦：對 zh-CN、ja、ko 各驗規格 053 的案例（注入尺寸不符的 `e1Base`；破壞 derived 字型後 `Compose(3)` 不 panic 且 `skips["manual"]` 加一）。
   - 逐段列出每個語言「E1 與固定格不同」的 key 集合與列數（k, k'）（只記 key 與數字）；位元組不變：2× 的五種語言與英文、zh-TW 3× 與實作前相同；2×／3× 交替位元組不變。
   - `TestPackagedLanes`：對四種語言各自的 `lane[<lang>]` 區塊（zh-TW 為頂層欄位）斷言含 `manual-e1=on`（逐區塊解析，不用整串 `Contains`，否則 zh-TW 的頂層欄位會滿足它），並直接檢查各 lane 的 `e1Base`；`LangTest` 通道沒有該欄位。
2. 離線同狀態重播（`phase317/offline.sh` 的手冊題時點，五種語言 × 2×、3×，runner 不傳 `-manual-english`）：A、B 的 live RGBA SHA-256：2× 全部相同、3× 的 zh-TW 與 en 相同；3× 的 zh-CN、ja 矩形外零差、矩形內不同；`memory_sha256`、`cpu_sha256` 相同。
   取樣時點記 `live_manual_visible_key`。現有快照（§2 第 8 點）的題在 ko 是「相同」，所以 **ko 的 3× 離線 A/B 預期是逐位元組相同**（有效的不變量檢查，不是 E1 的證據）；ko 的非真空證據由第 3 項實機承擔。
   若要補離線的 ko 非真空時點，新快照的題必須落在四種語言都「不同」的 16 題內（key 清單在審查者的 `sets-spec.tsv`，實作時由單元測試重新列出）。
3. 實機玩家路徑（`buckrogers-play`，`workplace/phase311/run.sh`，`path-repair.txt`，3×，zh-CN、ja、ko 各一次，zh-TW 作迴歸）：A、B 逐格比較（570 格）：機器雜湊相同；zh-TW 的 570 格 A、B **逐位元組相同**；zh-CN、ja、ko 的差異格僅限手冊頁矩形且矩形外零差；
   作答後清除那一格矩形與 en 逐位元組相同；之後轉場無殘字。該路徑顯示的題（`manual.page23.scots_alarm.word4`）四種語言都屬「E1 與固定格不同」，所以實機對四語都非真空；`buckrogers-play` 不輸出可見題 key，以 053 的畫格遮罩比對確認。
4. 詞界樣本：zh-CN、ja、ko 各至少三種不同情形的段落（括號專名、列尾專名、行首禁則各一）在離線或實機顯示，畫面僅本機檢視，不入 Git，也不描述手冊內容。
5. 打包：`tools/package.sh linux` 通過。
6. 文件：規格 053（上列被取代的條文處）、051、005 加註與 pointer；`docs/re/` 加收據；CONTEXT、WORKLOG、README 更新；Issue #40 逐項回報後關閉或標明剩餘項。

## 6. 風險

- 共用 plan 的規則改變影響所有語言：`.` 與 `/` 由錯誤變為接受（有條件），`, : ! ?` 由獨立 token 變為 terminal（段首、空白後、括號內首位變為拒絕）。以「117 段版面摘要不變」與「六個負例仍被拒」為閘門；三種語言現行 catalog 在這些位置沒有出現。
- `/` 只看前一個字元：日後 ja 或 ko 譯文若出現 `RAM/` 型態（拉丁詞後接斜線），該語言通道的 E1 預檢會失敗（整體關閉）；現行 catalog 沒有。
- 日後 ja、ko 譯文改變使某段 E1 超過 14 列時，該語言的 E1 整體關閉（`off(preflight:M)`）；單元測試每次列出 (k, k')，改譯文時即被發現。
- ko 維持字元級斷行：行首可能是助詞或詞尾的一部分（與固定格相同）；詞級斷行另案。
- 手冊題的具體詞界取決於玩家抽到的題；plan 預檢是靜態保證，實機樣本只能抽樣。
- 字型更換後預檢要重跑；預檢在載入時做，字型變動不會悄悄帶壞。
- 預檢對「沒有任何譯文的通道」是真空通過（`rows` 為空仍設 `e1Base`，DebugSummary 顯示 `on`）；目前不會發生（四個通道各 39 段）。
