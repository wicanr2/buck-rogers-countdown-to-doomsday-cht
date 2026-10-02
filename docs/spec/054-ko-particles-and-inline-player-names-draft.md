# 054 — 韓文助詞依尾音與句中玩家名

狀態：**DRAFT**（2026-10-02，第二版；第一輪獨立審查的 7 項必修與 9 項建議已併入，待複審）。
日期：2026-10-02
Issue：#39
決定：使用者 2026-10-02 選定 #39 的剩餘項目全做（ko 助詞依尾音、引擎片段內嵌玩家名、ko 範本逗號），母語者校對拆成獨立 Issue。範本逗號已於 2026-10-02 改措辭並提交（`text/engine-template.ko.tsv`、`.ja.tsv` 的 `tpl.logbook` 以句點分句）。
前置：規格 027（ECL 文字窗）、029（引擎片段）、036（NPC 譯名）、037／038（玩家名音譯與顯示）、043（韓文）、044／045（日韓玩家名音譯）、046（片段串接）。

## 1. 為什麼要做

1. **助詞**：韓文的主格、受格、與格助詞隨前一詞的尾音不同（`은／는`、`이／가`、`을／를`、`와／과`、`으로／로`）。譯文為執行期才知道前詞的情形留了括號並列形標記（`은(는)`、`이(가)`、`을(를)`、`와(과)`、`(으)로`；規格 043 的資料中以 `은(는)` 為主，約 220 列；`(으)로` 在現行 ko 資料中 0 列）。
   前詞若是韓文（怪物名、物品名、玩家名音譯），尾音其實可以決定，標記就可以換成正確的助詞。
2. **句中玩家名**：戰鬥與探索的訊息句裡，隊員名目前保持原版英文（ko `FLAVIUS은(는) 자신의 전술 판정을 한다.`；ja `FLAVIUSは自分の戦術判定を行う。`），而同一個畫面的右欄與 ECL 敘事裡同一個人是音譯（`플라비우스`、`설레스트(CELESTE)`）。

## 2. 證據

來源：證據蒐集（2026-10-02，dosgolem `e992599`，在 Docker 內以 `cp/*.state` 重播並與原 trace 逐列比對 W／D 序列；`workplace/phase317-evidence/REPORT.md`，ignored；重播 71 批中 66 批逐列相同，不一致者已排除）與獨立審查（`workplace/review054/REVIEW.md`）。
語料只有同一支隊伍（六位隊員）。本文與所有收據只列譯文、呼叫端鍵與計數，不列原版英文句子。

已證實：

1. 句中隊員名不是「原版畫名字、覆繪畫片段」：型態 B（24 筆）原版以**一次** ECL 印字呼叫（`0763:056C`）印出整句，覆繪層整句重畫，名字是引擎範本把 `_` 槽的原文原樣填入（`engine_text.go:539-544` `translateLine` 的 `default` 分支，`monsterSlot` 沒命中時 `zh[i] = p.Text`）；
   這條路徑不經 dispatcher `0424`，沒有 `MemberAt` 可用的字串指標（堆疊上組好的整句）。呼叫端（完整 overlay unit 鍵）：`OVR:27BBE:0AE5`（18）、`OVR:1CA15:1E42`（5）、`OVR:00904:2813`（1）。
2. 型態 D（6 筆）：dispatcher `0763:1282`（主程式，非 overlay）畫整句（`<名字>` 率領 `<怪物名>` 的句型），已在 `engine-dispatch-callers.tsv` 的 `allow`，但 `NeedsParty` 對 allow 呼叫端一律先回 false（`engine_dispatch.go:133-138`）。
3. 型態 A（36 筆）：ECL 敘事把名字當一次獨立 `056C` 呼叫（`OVR:00904:0B79`／`0B4A`），後面 `0B4A` 續印片段；其中 35／37 已被規格 038 §3.3 處理成「音譯(英文)」。片段呼叫的起始欄恰等於名字結尾欄（逐字形 36／36 同列且欄差 1）。
   執行期 ko 輸出的 `설레스트(CELESTE) | 은(는) 서서히 …` 中 `은(는)` 沒有依尾音選擇。
4. 型態 C（3 筆，同一檔）：物品頁標題（`<名字>` 的裝備，由三次 dispatcher 呼叫組成），名字呼叫現行保留英文；型態 E（1 筆）：名字黏在原版字串尾端沒有呼叫邊界（規格 038 §4 排除）。兩者不在本規格範圍。
5. 現行取隊伍快照的範圍：ECL 呼叫端 `0B79`、`0B4A`（`live_runtime.go:735-740`，經 `r.party.refresh`）與 dispatcher 名字呼叫端（235A 在 `names` 時、`21DE`、`0388`，`live_runtime.go:566-571`）；`0AE5`、`1E42`、`2813` 與 dispatcher `1282` 沒有快照。
6. `partyTracker.refresh`（`player_name.go:147-160`）讀取成功就改共用的 `t.last`，讀取被拒時回傳 `t.last`；`DebugSummary` 的 `party={taken=… rejected=…}`（`live_runtime.go:964`）計數也由它更新。
7. 三支語言通道（zh-TW、zh-CN、ja／ko）都會建 `players`（`live_lane.go:692-722`），所以 `players != nil` 不能用來區分語言。zh-TW 真實 catalog 的型態 B 句，`Decompose` 的 `_` 槽恰為隊員名（探針）：zh 一旦拿到名字解析器輸出就會變。
8. 句中名的判定不能靠指標：型態 B／D 的字串指標指向堆疊上的整句。可用的訊號是「`_` 槽的文字（去掉兩側空白與句尾標點後）等於隊伍快照的某位隊員名」；語料中名字都是全大寫，前後為空白或標點。
9. 怪物名在範本槽已被 `monsterSlot` 翻譯：`monster-name.ko.tsv` 49 列中 48 列以韓文音節結尾（24 列有尾音），`item-word.ko.tsv` 53 列全部以韓文結尾（ko 輸出的怪物名後接標記也會被本規格解析，無關快照）。NPC 名走規格 036 的加註（英文在譯名之後）。
10. `koWordMarks`（`joining.go:24-30`）刻意不含單獨的 `이`；解析成單獨 `이` 後 `koGlue(')', "이 …")` 為假，而 `koGlue(')', "이(가) …")` 為真。ECL 續接以 `koGlue(prevRune, text)` 決定要不要補空白（`ecl_text.go:491`）。
11. 表格列路徑（`engine_text.go:448-463`）先用 `stringUnits(front)` 算補白再把末欄靠右，所以標記解析必須在這之前（`은(는)`→`는` 少 4 個半形單位）。
12. 離線重播的 `replay-pages.tsv` 沒有隊伍快照，句中名在其中一律是英文；本規格的驗收要用有隊伍快照的執行期重播，不可只看離線頁面表。ja 音譯普遍比英文寬（`フラビウス` 10 單位對 `FLAVIUS` 7）；ko 也有變寬的。
13. hmenu 有 79 列 `은(는)`、2 列 `을(를)`、1 列 `이(가)`（ko TSV），不在本規格範圍。

未知：劇情 NPC 入隊、角色死亡後、太空戰鬥的句中名（語料未涵蓋）；`_` 槽含名字以外的字（名字前有未知前綴）時的覆蓋率（語料中型態 B 只見三種句型）；玩家名含小寫字母時 `fragKey` 是否把名字一部分吃成片段（風險，§6）。

## 3. 契約

範圍只含 ko 與 ja。zh-TW、zh-CN、en、zz 的所有輸出位元組不變（規格 046 §3.1 的凍結範圍）。

### 3.1 助詞標記解析（ko）

純函式 `koResolveMarkers(s string) string`：

- 標記與選擇：`은(는)`→ 前詞有尾音 `은`，無則 `는`；`이(가)`→`이`／`가`；`을(를)`→`을`／`를`；`와(과)`→ 有尾音 `과`，無則 `와`；`(으)로`→ 無尾音或尾音為 ㄹ 用 `로`，其餘 `으로`。
- 前詞的「讀音音節」：標記前一個 rune 若是韓文音節（U+AC00 至 U+D7A3），取它；若是 `)` 且括號內是 0x20 至 0x7E 的可列印 ASCII 且不含 `(`、`)`（名字單元的英文加註，規格 038 §3.3；玩家名可含 `'`、`.`、`-`、數字、空白等），且括號之前緊接韓文音節，取括號前的音節；
  其餘情形（拉丁字母、數字、標點、字串開頭）**不改**，保留標記。
- 只認標記本身的字串；不碰其他助詞。尾音依 Unicode 的韓文音節分解：`(code - 0xAC00) % 28`，0 為無尾音，8 為 ㄹ。
- `(·)` 形式的 `(으)로` 在現行資料中沒有列；其測試只能用合成資料。

### 3.2 套用位置

1. **同一次呼叫的組句**：`EngineTextCatalog.translateLine` 的 ko 分支在 `fillTemplateKoJa` 回傳（`engine_text.go:552`）與 `joinKo` 回傳（`engine_text.go:566`）兩處套 `koResolveMarkers`。開頭的 `monsterSlot(s)` 整串命中（`:515-517`）不需要套（怪物名譯文沒有標記）。
   `Translate` 的表格列路徑（`:449`、`:457`）因此拿到的是解析後的前段，補白用解析後的寬度；座標列路徑（`:443-446`）不受影響。解析在 ECL 與 dispatcher 兩條路徑的同一次呼叫內都生效；不套用的只有**跨呼叫**的情形（例如 235A 名字之後另一次呼叫的片段，dispatcher 逐呼叫）。
2. **ECL 頁的跨呼叫**：`EclTextPage` 新增 `lastReading rune`（最後一次畫出的文字的讀音音節，規則同 §3.1，由實際畫出的最後一個 rune 與其前的加註決定）。更新點與 `lastRune` 相同（`ecl_text.go:542-553`）：沒畫出任何字的呼叫保留前值；新頁（`fresh` 或 `p == nil`）為 0；
   最後一字是空白、標點、拉丁字母、數字時為 0；玩家名退回英文（`playerEnglish`）時為 0（續接的標記保留，這是預期行為）。玩家名呼叫（規格 038 §3.3）的 `lastReading` 取音譯本身（不含加註）的最後音節。
   續接呼叫（`p != nil && !fresh`）的譯文以標記開頭時，以 `lastReading` 解析前導標記後才排版。**是否補空白（`spaced`、`koGlue`）一律用解析前的譯文判定**；判定完才把前導標記換成解析結果，再交給 `attempt`（否則解析成單獨 `이` 會使 `koGlue` 為假，在名字與助詞之間多插空白）。
   啟用條件為 `w.catalog.lang == LangKo`。
3. 其他路徑（靜態譯文、dispatcher 跨呼叫、hmenu、選單等）不套用；靜態譯文中的標記由 Python 檢查器（規格 043）管。

### 3.3 句中玩家名（ko、ja）

- **語言閘門**：名字解析器 `names`（型別 `PartyNameFunc`，`func(core string) (reading string, ok bool)`）只在 lane 語言為 ko 或 ja 且 `players != nil` 時建立；其他語言一律傳 nil。`TranslateParty` 本身在 `c.lang` 不是 `LangKo`／`LangJa` 時也忽略 `names`（雙重防護）。`Translate(s)` 等於 `TranslateParty(s, nil)`，行為不變。
- **隊伍快照**：新增的取快照點 `OVR:27BBE:0AE5`、`OVR:1CA15:1E42`、`OVR:00904:2813` 與 dispatcher `0763:1282` **直接呼叫 `ReadPartySnapshot`**，讀取被拒就不比對名字（`names` 為 nil）；它們**不經** `r.party.refresh`，不更新 `partyTracker` 的 `last`、`Taken`、`Rejected`，既有呼叫端（235A、`21DE`、`0388`、`0B79`、`0B4A`）的取快照方式與回退值不變。
  只有至少一條 ko 或 ja lane 的 `players != nil` 時才讀。`1282` 宣告成程式常數（像 `partySelectedCaller`），在 `NeedsParty` 對 allow 清單的提前回傳**之前**判斷；ECL 的三個呼叫端在 `observeEclText` 另立判斷，結果放進 `EclTextEntry.Party`（新欄位）。
- **名字槽**：`EngineTextCatalog.TranslateParty(s string, names PartyNameFunc)`。`translateLine` 的 `_` 槽：先照現行試 `monsterSlot`（怪物名優先，現行行為不變）；沒命中且 `names != nil` 時，槽文字去掉兩側空白與句尾 `.,!?` 後若**逐字等於**快照中某隊員名，換成該隊員的音譯（`PlayerNames.Chinese(name, gender)`，lane 自己的語言），
  保留原有的前後空白與句尾標點（ko 句點、ja `。` 的規則與 `monsterSlot` 相同；ja 的名字槽原有前後半形空白照舊保留，這是刻意保留，與現行英文名一致）。不等於任何隊員名者照舊。
- **顯示與退路**（只顯示音譯，不加英文註；理由：訊息句由片段組成、版面逐呼叫固定；右欄「窄欄只顯示中文」的決定相同）。順序為：
  (1) 帶句中名音譯的譯文；(2) 放不下時改用 `names == nil` 的譯文，也就是現行輸出（ko 仍套 §3.1 標記解析）；(3) 再放不下才走現行退路（ECL 整頁丟棄、dispatcher 記 miss）。
  ECL 是 `attempt` 失敗，dispatcher 是 `stringUnits(zh) > 2*n`，兩者都要先走 (2) 才進入 `eclPrompt`、`pending`、`Overflows` 等後續步驟。
- **計數器**（先定義，收據才有數可記）：`EclTextStats` 與 `EngineDispatchWatcher` 的統計各加 `InlineNames`（有幾句換成音譯）、`InlineNameFallback`（(2) 用了幾次）；`EclTextStats` 另加 `MarkersResolved`（ECL 跨呼叫解析了幾次）。
  `replay_trace.go` 的 `engineUnits` 用不帶名字的 `Translate`，trace 的單位數欄不反映句中名（註明，不改）。
- 順序：名字槽換成音譯後，§3.2 第 1 項的標記解析才套用（所以 `플라비우스` 後的 `은(는)` 解成 `는`）。

### 3.4 不變量與預期差異

1. zh-TW、zh-CN、en、zz 的合成 RGBA 與現行逐位元組相同；機器狀態（記憶體、CPU）不變；`partyTracker` 的 `last`／計數與現行相同。
2. ja 在 `names == nil` 時與現行逐位元組相同（`Translate` 不變）。ko 在 `names == nil` 時，只有「括號標記前一字可定讀音」的字串與現行不同，差異恰為把標記換成 §3.1 的結果，其餘位元組相同；
   測試以「現行輸出套 §3.1」當預期，在整份語料上比對差集（做法同 `engine_zh047_test.go`）。（`TestEngineJoinJaKoUnchangedBySpec047` 對本規格是真空的：凍結 catalog 的 ko 譯文沒有標記，不能當 ko 回歸證據。）
3. 變動只出現在：含括號標記且前詞可定音節的 ko 畫面（§3.2），以及句中槽等於隊員名的 ko、ja 畫面（§3.3）。ja 的預期差異另含：名字換成片假名後，名字與前後片段之間因 `engineAlnum` 判定而消失的半形空白。變動集合由測試列出並與預期比對（規格 046 §4 的做法）。
4. 型態 C、E、治療表欄、hmenu 與右欄名字的行為不變。
5. 標記無法解析時（前詞是拉丁字母、數字、標點、前一個型態 A 名字呼叫沒被規格 038 接住使 `lastReading` 為 0）保留標記，與現行相同。

## 4. 不在範圍

- 型態 C（物品頁標題，需在 `partyPanelAt` 補列並處理其後片段的位置）、型態 E（黏接）、治療表欄。
- hmenu 的標記（79 列 `은(는)`、2 列 `을(를)`、1 列 `이(가)`）。
- zh-TW、zh-CN 的句中玩家名（目前凍結，英文）。
- 數字（漢數詞讀音）與拉丁字母詞後的標記解析（無法由字串決定）。
- dispatcher 跨呼叫的標記解析（證據顯示整句都是單一呼叫）。
- 母語者校對（拆成獨立 Issue）。

## 5. 驗收

1. 單元測試：
   - `koResolveMarkers`：五個標記 × 有／無尾音 × ㄹ 尾音（`(으)로`，合成資料）；括號加註（`설레스트(CELESTE)` 後的標記取 `트`；加註含 `'`、`.`、數字）；前詞為拉丁字母、數字、標點、字串開頭時保留；與其他助詞（`의`、`에`）相鄰不誤改。
   - `TranslateParty`：名字槽等於隊員名（含前導空白、句尾標點）→ 音譯；不等於→ 英文；怪物名優先；`names == nil` 與 `Translate` 逐字相同；ko 結果的標記已解析；ja 無標記解析。以 `q1_occurrences.json` 中型態 B 的 3 種簽章與型態 D 的簽章（只記片段鍵）在真實 ko、ja catalog 上組合成字串並測，預期名字槽換成音譯。
   - **語言閘門**：`TranslateParty(s, names)`（`names` 非 nil，至少涵蓋四位隊員）對 zh-TW、zh-CN、zz、空語言，在 `engineFreezeCorpus()` 全部字串上與 `Translate(s)` 逐字相同；ECL 與 dispatcher 各以 zh-TW、zh-CN watcher 餵入帶 `Party` 的 `0AE5`、`1282` 合成呼叫，頁面與 `Lines()` 與不帶快照時相同。
   - ECL：玩家名呼叫（音譯加註）接標記開頭的續接呼叫 → 標記已解析且續接呼叫的起點不變；**有尾音的名字加 `이(가)` 開頭續接，`spaceNeeded` 為真時，名字與 `이` 之間沒有空白**；前一呼叫是英文 passthrough 時保留標記；`lastReading` 在清除、換頁後重置。
   - 型態 B（三個呼叫端）與型態 D（`1282`）的合成呼叫：有快照時句中名為音譯，無快照時與現行逐位元組相同；`0B79`／`0B4A` 的既有行為與計數不變；新取快照點不改變 `partyTracker` 的 `last`、`Taken`、`Rejected`。
   - 寬度：音譯放不下時 (2) 用現行輸出（`InlineNameFallback` 加一），仍放不下才走現行退路。
   - 差分測試：zh-TW、zh-CN、zz 凍結副本（沿用 `layout_freeze_test.go` 的做法）逐位元組不變；ko 的 `names == nil` 差集測試（§3.4.2）。
2. 執行期重播（有隊伍快照；從 `cp/*.state` 起跑的執行期，不是離線頁面表）：A（實作 commit 的父 commit）與 B（實作 commit）各自從乾淨匯出建置（不含除錯鉤；差別只在少了除錯輸出）。
   每個時點的 `-until` 取目標呼叫返回後第一個 retrace，並以 trace 確認該頁仍在畫面上（`plans.txt`、`plans2.txt` 的 UNTIL 是為 trace 涵蓋率挑的，不保證如此）。
   預期矩形：ECL 取目標呼叫 `ecl` 列的視窗（`Left..Right`、`Top..Bottom` 換算成 ×8×scale）；dispatcher `1282` 取該呼叫所在的列，跨整列寬。
   每個時點跑 zh-TW、zh-CN、en、ko、ja 五種語言 × A、B：記憶體、CPU 雜湊相同；zh-TW、zh-CN、en 的 live RGBA SHA-256 與 A 相同。
   **非真空條件**：ko 與 ja 各至少有一個型態 A、一個型態 B、一個型態 D 的時點，B 在預期矩形內與 A 不同；否則該項驗收不成立。畫面僅本機檢視，收據只記雜湊與推導出的計數、呼叫端鍵（不複製 trace 的 `eng` 欄，它印出原版位元組）。
3. 全套件測試（乾淨匯出）與 `go vet` 通過；`ja_check.sh`、`ko_check.sh` 通過（本規格不改 TSV）。
4. 文件：規格 043、044 §3.8、045、046 加指向本規格的 pointer；`docs/re/` 加收據（呼叫端、計數、驗證，不列原版英文句子）；README、CONTEXT、WORKLOG 更新；Issue #39 逐項回報。

## 6. 風險

- 句中名只比對「槽文字逐字等於隊員名」：槽含其他字時不處理（英文保留）；新句型要補證據。玩家名含小寫字母時，`fragKey`（`engine_text.go:196-203`）可能把名字一部分吃成片段；名字與大寫物品詞（`.uc` 鍵）相同時可能被切成 `I`。這兩種情形名字不會被換掉，維持現行英文。
- 玩家把隊員取成與怪物名相同的字串時，怪物名優先（現行行為）；機率低，記為已知。
- 音譯寬度：ja 與部分 ko 音譯比英文寬，放不下時 (2) 退回現行輸出，不比現行差。
- ECL 的 engine 鍵不給名字單位：ja 是字級版面，拉丁字串整段不斷行，片假名名字則可能在行尾被拆開（可讀性風險；以畫格檢視記錄，必要時另案讓 `TranslateParty` 回傳名字區間給版面）。
- 同一畫面右欄（只譯名）、ECL 敘事（譯名加註）與訊息句（只譯名）三種寫法並存，是三種版面限制的結果。
- 取隊伍快照增加 `0AE5`、`1E42`、`2813`、`1282` 呼叫的讀取量：每次進入多讀隊伍鏈（約七筆記錄），只在 ko、ja lane 存在時需要。
