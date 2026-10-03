# 056 — 名字單元放不下時縮小字體

狀態：**限縮 CONFORMED**（2026-10-03；範圍：機制，即縮小等級的版面、繪製、字模衍生與 §3.8 的不變量，由單元測試、凍結副本差異（合成語料與 `text/` 語料）、trace A/B（限 NPC 加註）、重播閘門、合成截圖與突變表驗收，證據 docs/re/phase-322-name-unit-shrink.md；實機觸發路徑（後期名字、手札、修理表頭）未量，維持未知或強推論）。READY 於同日經兩輪獨立審查（第一輪 A 必修 6、建議 9，B 必修 19、建議 13；第二輪 C 必修 3、建議 11，D 必修 4、建議 8，應改皆已併入）；實作時補了 §3.3 的保底規則與 §5.8 的測試清單，修訂經過在 phase-322 §3。
日期：2026-10-03
Issue：#38
決定：使用者 2026-10-03 要求：「完整格式」（中文名加括號英文）放不下時，不退成只顯示中文或退回英文，改為縮小字體塞進對話框；只要機制有作到，#38 就關閉，不再做實機測量。
前置：規格 027（ECL 文字窗）、036（NPC 譯名）、038（玩家名顯示）、039（半形 ASCII）、042／043（日韓排版）、045（玩家名前導空白）、046（片段串接）、048（zh 甲板空白）、054（讀音續接）。
後續：使用者 2026-10-03 要求 ja 的濁音與 ko 的音節在 L2 要可分，依語言另開規格 057（ja）、058（ko），覆寫本規格 §3.2 的 ja、ko 的 L2 字模（規格 057 已限縮 CONFORMED，dosgolem `d73de94`；規格 058 READY，待實作；檔案 `057-ja-shrink-glyph-distinct-ready.md`、`058-ko-shrink-glyph-distinct-ready.md`）。
取代：036 §3.3 的 ECL 敘事窗三段退路與 038 §3.3 的玩家名退路，改為 §3.4 的順序（READY 時在兩份規格對應處加註）。

## 1. 為什麼要做

名字單元（036 的「中文(英文)」加註、038 的玩家名「中文(英文)」）比一般文字寬。ECL 敘事窗放不下時，現行依序退成「只加第一次」「不加」，玩家名退成「只中文」「英文原文」。
NPC 加註的降段在 phase-304 的離線重播中為 0（first 0、none 0；dosgolem `a324e33`，之後 046 至 054 改過 ECL 路徑，現行基準以 §5.6 的父 commit 重跑為準）。玩家名的退路不在離線重播涵蓋範圍（重播不帶玩家情境，phase-304 §6），觸發與否未知。兩者目前只有單元測試；後期的名字（劇情 NPC 入隊、太空戰鬥）可能觸發，但沒有狀態可量。
使用者的決定是改變退路本身：放不下時先把名字單元縮小，縮到下限仍放不下，才用現行的退路。

## 2. 證據

已證實（讀程式，dosgolem `72ce242`）：

- ECL 敘事窗：`EclTextWatcher.placeText` 對一次呼叫的 `attempt` 依序試 `NameGlossary.Variants` 的版本（全加、只加第一次、不加；與前一版相同的版本略去），每個版本呼叫 `layoutEclTextP`；046 的起點空白與 048 的甲板空白在 `attempt` 之外先試帶空白、再試不帶。玩家名由 `layoutPlayerName` 依序試完整、只中文，再試英文，並有帶前導空白的變體（045 §3.4）。放得下就採用；都放不下時整窗退回英文（027 §3.4，不在本規格範圍）。
- `layoutEclTextP` 在詞級 profile（ko，043 §3.4）先試詞級，失敗再整次改用字級；排版的 token 寬度一律由 `textUnits` 計。字級 token 會把名字單元之後的收尾標點併進同一 token，`joinOpening`（ja、ko）把開括號併進下一個 token，詞級會把單元與黏著的助詞或標點併成一個 token（放得下一列才併）。
- 版面資料：`EclTextLine{Row, Col, Text}`，`Col` 是半格單位（1 單位 = 4 邏輯像素，039 §3.4）；全形 2 單位、半形 1 單位；名字單元是 `NameUnit{Start, End}`，單元比一行寬時才在英文空白處斷開。
- 繪製：`EclTextOverlay.Sync` 以 `eclRowText` 把每列組成半格單位的 slots（後面的列覆蓋前面的列，超出該列起點到右界的字略過），再依全形、半形切成 `xlate.Stamp`（key 為 `<列>#<n>`，`CellW` 8 或 4 邏輯像素，`CellH` 8）。`Layer.Draw` 依 `Stamps` 順序，每筆先以底色填滿整個矩形再畫字；`GlyphX`、`GlyphY` 是輸出像素，字模畫在「格左上加偏移」，超出格緣的點不畫。
- 字型：半形由 16×16 底字型衍生（039 §3.2：2× 為 8×16、3× 為 12×24，填滿半格）；全形在 2× 是 16×16 填滿 16 實際像素的格，在 3× 由 `manualThreeXFont` 取得 22×22 放進 24 的格、四邊內縮 1（`manualGlyphOffset`）；字模皆為 1 位元。
- 一個語言通道只有一個 `EclTextWatcher`，2× 與 3× 的 presenter 共用同一份 `EclTextPage`，watcher 不持有字型。
- 手札的版面資料是字串列（`[][]string`），沒有承載字模大小的欄位。`layoutEclTextP` 也被手札（`logbook.go`）與 `LayoutEclAnnotatedLang`（`name_scan.go`）呼叫。
- 054 的句中玩家名走 `engine` key，`placeText` 不對它做名字單元查詢，句中名只顯示音譯、不加英文註。

未知（本規格不量）：後期路徑實際會不會走到這些退路；玩家名退路在任何現有收據中的觸發次數；縮小後的字在實機的可讀性（§5.5 只留合成截圖供使用者判斷）。

## 3. 契約

### 3.1 範圍

- 對象：ECL 敘事窗中的名字單元，即 036 的 NPC 加註單元，以及 038 的玩家名呼叫（單獨名字、續寫、帶前導空白）。語言：zh-TW、zh-CN、ja、ko。presenter：2× 與 3×。
- 縮小的是名字單元整體（中文或音譯名、括號、英文）；單元之外的文字（含前導空白、收尾標點、助詞、開括號）維持原大小。一次呼叫內所有名字單元用同一個等級。
- 不在範圍：054 的句中玩家讀音（`engine` key，沒有名字單元、沒有英文註）、手札、窄欄只顯示中文的家族（036／038 的設計：隊伍欄、戰鬥右欄、選單）、視窗整窗退回英文（027 §3.4）、`engine` 與 `passthrough` 通道。

### 3.2 等級

列高 R = 8 × presenter 倍率（2× 為 16、3× 為 24 實際像素）。全形字模框是正方形；半形字模框寬為全形格寬的一半、高為全形格寬。〔規格 057 §3.2 第 3 點改為幾何關係式：預設表（zh）仍是這樣，語言表的全形字模可以是矩形；ja、ko 的 L2 見規格 057、058。〕

| 等級 | 比例 | 邏輯像素：全形格寬、半形格寬 | 2× 全形：格寬／字模／內縮 | 2× 半形字模 | 3× 全形：格寬／字模／內縮 | 3× 半形字模 |
|---|---|---|---|---|---|---|
| L0 | 1 | 8、4 | 16／16／0 | 8×16 | 24／22／1 | 12×24 |
| L1 | 3/4 | 6、3 | 12／12／0 | 6×12 | 18／16／1 | 9×18 |
| L2 | 1/2 | 4、2 | 8／8／0 | 4×8 | 12／11／0 | 6×12 |

- L0 是現行值。L1、L2 的字模尺寸是 L0 字模佔格比例乘上等級比例後向下取整（3× L1：22/24 × 18 = 16.5，取 16）；內縮 = ⌊(格寬 − 字模) / 2⌋（3× L2：11 放進 12，內縮 0、右側空 1）。
- 單位：`CellW` 是邏輯像素（L1 全形 6、半形 3；L2 為 4、2），`CellH` 一律 8；`GlyphX`、`GlyphY` 是輸出像素。
- 單元寬度：全形字數 F、半形字數 H，W = 2F + H（半格單位）。L1 占 6F + 3H = 3W 邏輯像素，L2 占 2W 邏輯像素。單元佔用的格數 W_s = ⌈像素數 / 4⌉：L1 為 ⌈3W/4⌉，L2 為 ⌈W/2⌉。
- 單元的左緣在原本的半格欄 `Col`；單元內剩下的像素（4 × W_s 減單元像素數）是底色。
- 字模位置：`GlyphX` 全形為內縮、半形為 0；底對齊：全形的 `GlyphY` = R − 字模 − L0 的內縮（2× 為 0、3× 為 1），半形的 `GlyphY` = R − 半形字模高（等於全形格寬）。例：2× L1 全形 4、半形 4；3× L1 全形 7、半形 6；2× L2 全形 8、半形 8；3× L2 全形 12、半形 12。〔規格 057：全形 `GlyphY` = R − 字模高 − L0 的內縮，字模高 `FullGlyphH` 取代方形邊長；半形 `GlyphY` = R − 半形字模高 `HalfH`，語言表不要求 `HalfH` 等於全形格寬。〕
- 等級表是套件層級的 `var shrinkLevels`（不是 `const`，測試要能替換；含替換成空表，§5.8）。替換它的測試不得平行（套件內目前沒有 `t.Parallel()`）。`Shrink`、`NameShrunk`、`PlayerShrunk` 的索引一律是等級編號（L1 為 1、L2 為 2），不是表內位置；移除 L1 後 L2 仍記為 2。`shrinkLevels` 全語言共用。2× L2 的字模只有 8×8，可讀性待使用者看合成截圖判斷（§6）。〔規格 057：預設表仍是 `shrinkLevels`，語言可覆寫（`shrinkLevelsFor(lang)`，頁面帶 `Lang`），測試輔助 `withShrinkLevels` 會清空語言覆寫、`withLangShrinkLevels` 只換一個語言；ja 的 L2 見規格 057，ko 的 L2（格寬 5 邏輯像素）見規格 058，其中 ko 的單元寬度公式為 ⌈(5F + 2H) / 4⌉。〕

### 3.3 字模衍生

- 來源：全形縮小字的來源是 `NewEclTextOverlay` 收到的 16×16 `font`；半形縮小字的來源是 `halfFontsOf(font).For(2)` 的 8×16 半形字型（兩種 presenter 共用同一來源，3× 的 12×24 版本不當來源）。縮小等級不沿用 `manualThreeXFont` 對 U+00FF 以下字元的置中規則，一律用下列規則。
- 目標尺寸見 §3.2：全形為「字模」欄的正方形，半形為「半形字模」欄。來源寬 S_w、高 S_h，目標寬 T_w、高 T_h。以整數運算：橫向把來源每個像素視為 T_w 單位寬、目標每個像素視為 S_w 單位寬（縱向來源每像素 T_h、目標每像素 S_h），目標像素 (x, y) 的有墨面積 = 所有與它重疊的有墨來源像素的重疊面積總和；有墨面積 × 2 ≥ 目標像素面積（S_w × S_h）時該點亮，否則不亮。目標與來源尺寸相同時這個規則是原樣複製。〔規格 057：全形字模可為矩形，等級可帶面積門檻 `Thr`（預設與本節相同，為 1/2）；ja 的 L2 為 8×14／12×16，ko 的 L2 為 10×12／15×16、門檻 1/3。〕
- 保底（實作中補，2026-10-03）：面積規則使整個字模全空、但來源字模有墨（細筆畫，例如 `^`、`` ` ``、`.`）時，點亮有墨面積最大的目標像素（並列取列優先、再欄優先的第一個），使「來源有墨的字衍生後必有墨」。補這一條的原因：§5.1 的靜態檢查在沒有保底時發現 2× L1 與 L2 的 `^`、`` ` ``（所有字型）與倚天字型 2× L2 的 `.` 衍生後全空，依本節規則三個等級都會被移除。來源字模無墨（空白）時仍為空。面積規則本身（≥ 門檻）不變；保底只在整個字全空時才作用。
- 決定性：同一來源與目標尺寸產生同一位元組；衍生字型以名稱標明等級與 presenter。
- 版面與字型無關：watcher 不判斷字模是否可用。可用性由靜態檢查把關（§5.1 第 3 點）：所有可能出現在名字單元的非空白字元（名字表的譯名用字、音譯允許字集 `translit-chars`、ASCII 可列印字元）只要來源字模有墨，在每個 presenter 的 L1、L2 衍生後都不全空；不通過的等級必須從 `shrinkLevels` 移除。版面只有一份（2× 與 3× 共用同一個 watcher 與同一份頁面，W_s 與 presenter 無關），所以移除以兩個 presenter 與四種語言的聯集為準：任何一個不通過，該等級對所有語言與 presenter 一起移除。〔規格 057 §3.5：靜態檢查不通過的等級改為對使用該張表的語言移除，不再對所有語言一起移除。〕
- 執行期若某個非空白字在衍生字型沒有字模（來源字型缺字），`Sync` 把它回報為缺字，不默默畫出空白。現行缺字的後果是 `liveLane.syncEclText` 呼叫 `ObserveDiscontinuity`，兩個 presenter 的整個 ECL 頁面一起作廢，視窗顯示英文原文（`live_lane.go`）；所以靜態檢查必須是真的通過（§5.1 第 3 點），不能被 SKIP。
- 缺字：縮小等級與 L0 用同一組字元，不新增缺字；來源字型缺字時行為同現行。

### 3.4 試排順序

等級是最內層：每個「版本」先試 L0（現行 `layoutEclTextP` 完整流程，含 ko 的詞級再字級），失敗再試 L1，再試 L2；每個等級各自做「詞級 → 字級」。「L0 放得下」一律指現行 `layoutEclTextP` 成功（含字級退路）。

玩家名（`layoutPlayerName`，038 §3.3）：

- 無前導空白：完整（L0、L1、L2）、只中文、英文。
- 有前導空白（045 §3.4）：完整帶空白（L0、L1、L2）、只中文帶空白、完整不帶空白（L0、L1、L2）、只中文不帶空白、英文帶空白、英文。前導空白是單元外的獨立 token，不縮小。

NPC 加註（`placeText` 的 `attempt`，036 §3.3）：在 `attempt` 內依序試「全加（L0、L1、L2）」「只加第一次（L0）」「不加」。只加第一次不試縮小。046／048 的空白分支在 `attempt` 之外：帶空白版本的所有版本與等級先試完，才試不帶空白版本（現行順序不變）。

- 048 的甲板空白檢查（第一列是起點列且以空白開頭）套用在 `attempt` 回傳的結果上（第一個放得下的版本與等級），不逐等級檢查，與現行相同。
- 043 §3.4 的 ko 不變量（詞級加退回的 fits 與字級相同）在 L1、L2 也成立，§5.2 逐等級比較。
- 空白分支的優先序沿用現行：保住前導空白優先於保住單元大小（帶空白的縮小版本先於不帶空白的 L0）。因此舊版選了「不帶空白的全加／完整 L0」（記 `SpaceDropped`）的呼叫，新版可能改選帶空白的縮小版本；這是預期差異（§3.8 第 1 條）。045 現行「只中文帶空白」先於「完整不帶空白」的關係不變（§6 第 6 點）。

每一步用同一組游標與接續狀態；版面與繪製是純函式，失敗的嘗試不改任何狀態（同 036 §3.3）。第一個放得下的採用。

### 3.5 版面

- `layoutEclTextP` 的行為與簽名不變（手札、`LayoutEclAnnotatedLang`、凍結測試維持呼叫 L0）。新增一個接受等級的內部入口（暫名 `layoutEclTextLevel`），`layoutEclTextP` 是它在等級 0 的包裝；L0 永遠不把一列拆成多個 `EclTextLine`。
- 縮小等級下，名字單元是不可拆 token，不在英文空白處斷開（L0 才允許，維持現行）。
- 寬度函式：token 寬度 = 各縮小單元各自的 W_s 之和 ＋ 其餘字元的正常寬度（`textUnits`）（一個 token 可能含兩個單元：ko 詞級黏著段以開括號結尾時，`joinOpening` 會併入下一個單元 token）。字級的收尾標點、詞級的助詞與標點、`joinOpening` 併入的前一個 token（可能是以開括號結尾的整個詞），都維持原大小。排版內所有寬度判斷（放不放得下一列、`joinOpening` 合併、詞級「放得下一列才併」）都用這個寬度函式。`joinOpening(tokens [][]rune, width int)` 與 `prof.closing` 的簽名與 L0 行為不變（凍結測試直接呼叫），縮小等級另用能辨識單元的版本。
- 單元加附著字比一行寬時：詞級先退成「單元加收尾標點」（同現行）；單元加收尾標點仍比一行寬時，這個等級失敗（不斷開）。
- `EclTextLine` 新增 `Shrink uint8`（0 為一般，1、2 對應 L1、L2）。正規形：同一列內依 `Col` 排列；每個縮小單元一個 `EclTextLine`（`Text` 是單元的字元，`Col` 是起點，占 W_s 格）；列首到第一個單元、相鄰兩個單元之間、最後一個單元到列尾的一般文字各合成一個 `EclTextLine`（附著的標點、助詞、開括號屬於這些一般文字）；換列修剪尾端空白後為空的一般列不輸出（同現行）。沒有縮小單元的列與現行完全相同。
- 換列：單元的 W_s 放不進目前列的剩餘格就整個移到下一列（同現行不可拆 token）；禁則與 `isEclClosing` 規則不變。
- 游標：排版內的 `used`、回傳的 `endCol` 與下一個 token 的起點以 W_s 前進。`lastRune`、`lastReading`（054）、`owedSpace` 以實際字元計：依 (`Row`, `Col`) 順序串接所有 `EclTextLine` 的 `Text`，縮小列的字元照常參與。

### 3.6 繪製

- `eclRowText` 組列時，縮小單元以 W_s 個 slot 的佔用參與同一個「後寫覆蓋」流程：被它覆蓋到的全形字另一半同現行清除；任一 slot 被較晚的列覆蓋時，整個縮小單元不畫（空出的 slot 依 039 §3.1 補位）。縮小單元的 W_s 個 slot 必須落在「該列起點（頂列為 `TopCol`）到右界」之內，否則整個單元不畫、不裁切，而且不寫入任何 slot，等同不存在（不覆蓋較早的列）。縮小單元的字不放進一般列的 slots（不以正常大小再畫一次）；單元右緣與 W_s 格右緣之間的像素由同列 stamp 的補位填底色。
- 縮小單元另用縮小字模畫一組 stamp，**追加在該列所有一般段 stamp 之後**（後畫才不被底色蓋掉）；`EclTextOverlay` 的 `cols` 與每筆 stamp 同步追加（換色用）。stamp key 為 `ecl.<頁>.row.<列>#<n>`，n 接續該列一般段之後編號，`rowKeyOf` 與 `ActiveKeys` 的去重不變（仍只回原列 key）。
- stamp：以全形、半形切段（同 039 §3.3）；每段的邏輯 X = 該列起點 × 8 ＋（單元 `Col` − 該列起點半格）× 4 ＋ 單元內前面各段的 `Cells × CellW`（不一定是 4 的倍數，不得對齊到半格）；每段的 `CellW` 為該等級的全形或半形格寬，`CellH` 8，字型是該等級該 presenter 的衍生字型，`GlyphX`、`GlyphY` 依 §3.2，`GlyphScale` 1，前景與底色同頁面。
- 單元的繪製不跨列；頁面被後續原版寫入清除、`Gone`、`removeRows` 時，縮小 stamp 與同列一般 stamp 一起消失（以列為單位，`Sync` 略過 `!Shows(row)` 的列）。

### 3.7 計數

`EclTextStats` 新增 `NameShrunk [2]int`（NPC 加註呼叫採用 L1、L2 的次數）與 `PlayerShrunk [2]int`（玩家名呼叫採用 L1、L2 的次數）；用陣列使 `EclTextStats` 保持可用 `!=` 比較。縮小的完整玩家名照常 `PlayerNames++`，另加 `PlayerShrunk[等級 − 1]++`。只在該版面被採用時計數（同 `eclPlacement` 的慣例：縮小等級由 `eclPlacement` 帶回，054 的 `placeText` 讀音句失敗後再跑原句，只計採用的那一次）；帶空白版本全部失敗、不帶空白版本採用時只計後者。舊版會記 `SpaceDropped` 的呼叫，若新版改採帶空白的縮小版本，`SpaceDropped` 不增、`NameShrunk`／`PlayerShrunk` 增加。降段計數維持：只在實際退成「只加第一次」「不加」「只中文」「英文」時增加。`DebugSummary` 以 `%+v` 印整個 stats，字串會多出新欄位（可接受）。`-live-trace-out` 的欄位不變。

### 3.8 不變量

1. 舊版在它第一個試的空白狀態（欠空白時為帶空白，否則不帶）就以「全加 L0（玩家名：完整 L0）」放得下的呼叫，新版輸出（`EclTextLine` 的 `Row`、`Col`、`Text`，`Shrink` 為 0，`endRow`、`endCol`、各計數）與舊版相同。新舊輸出不同的呼叫，只能屬於兩類預期差異：(a) 舊版降段（只加第一次、不加、只中文、英文）而新版改成縮小；(b) 舊版捨棄空白（`SpaceDropped`、選不帶空白的全加／完整 L0）而新版改選帶空白的縮小版本。兩類都要求新版 `Shrink` 不為 0；比對時各自列清單與筆數。舊版降段或捨棄空白而新版沒有任何等級放得下者，輸出與舊版相同。
2. 縮小只改字模大小與位置，不改譯文、key、catalog、`text/`、字型檔；衍生字型在執行期產生，不進發行包。
3. 一次呼叫的所有縮小單元同一等級；一列內縮小單元與一般文字不重疊；縮小單元的像素都在視窗遮罩內。
4. 縮小等級的版面與繪製是純函式（同輸入同輸出，不修改傳入的 `units`、`text`），失敗的嘗試不留副作用。
5. `layoutEclTextP`、`layoutLogbookUnitsP` 的行為不變，pre-043 凍結摘要（`ko_layout_test.go`、`layout_freeze_test.go`）維持通過。

## 4. 不做什麼

- 手札面板的名字加註退路（資料模型是字串列）。
- 054 的句中玩家讀音、窄欄只顯示中文的家族、戰鬥右欄的原名格規則（029、038）、視窗整窗退英文。
- 單元之外的文字縮小；一次呼叫內混用等級；小於 L2 的等級；灰階或抗鋸齒（字模維持 1 位元）；`LayoutEclAnnotatedLang`（name-scan）回報 L1、L2（維持 L0 判斷）。
- 修改譯文、名字表、catalog 與字型檔。
- 後期路徑的實機測量：使用者決定不做（§5.7）。

## 5. 驗收

使用者 2026-10-03 決定 #38 以機制實作為關閉條件，不再實機測量。以下是機制的驗收；不聲稱任何未量到的路徑已量測。環境變數閘門的測試在預設 `go test` 會 SKIP；規格要求的 PASS 以 `-v` 輸出確認，收據（輸出、字型 SHA-256、`text/` 與 dosgolem commit）記入 phase 文件才算通過，SKIP 不算。

1. 字模衍生：
   - 單元測試：小尺寸已知答案（4×4 對 3×3 逐點驗算）、尺寸相同時原樣複製、決定性、衍生字型名稱。
   - 常數測試：§3.2 表逐格比對（2×、3× 各 L0／L1／L2 的格寬、字模、內縮、半形字模，`GlyphX`、`GlyphY`、W_s 公式）；L0 的值等於現行（`manualGlyphOffset`、半形衍生尺寸）。
   - 缺字與保底：縮小單元含來源字型缺字的字時，`Sync` 回報缺字、什麼都不畫；保底規則的案例（單點字衍生後有一個點、並列取第一個、面積規則保得住的字不被保底改動）；突變「保底規則被移除」被此測試與靜態檢查擋下。
   - 靜態可用性檢查（環境變數閘門）：字型集合為 zh-TW 的 `buckrogers-unifont.golemfnt` 與（本機存在時）`buckrogers-eten-top-pad.golemfnt`、zh-CN `buckrogers-zh-CN.golemfnt`、ja `buckrogers-ja.golemfnt`、ko `buckrogers-ko.golemfnt`（發行字型在 `workplace/pkg-stage/AppDir/font/`，不在 git；環境變數沿用 `BUCKROGERS_CHT_ROOT`、`BUCKROGERS_ZHTW_FONT`、`BUCKROGERS_ZHCN_FONT`、`BUCKROGERS_JA_FONT`、`BUCKROGERS_KO_FONT`，倚天另加 `BUCKROGERS_ZHTW_ETEN_FONT`，倚天字型只限本機）。以這些字型與 `text/` 的名字表、`translit-chars`、ASCII 可列印字元，驗證每個 presenter 的 L1、L2 衍生字模都不全空。不通過的等級從 `shrinkLevels` 移除並記入 phase 文件。同一檢查加入 `tools/package.sh` 的打包流程：字型子集建好後、封裝之前對剛建的字型執行（字型隨譯文重建，不能只在實作時通過一次）。檢查另輸出「衍生後字模相同的不同來源字」的對數與清單，記入 phase 文件，供使用者判斷是否移除 2× L2；不作為失敗條件。〔規格 057 §3.5 改：全形字模相同的不同字是硬性失敗條件（半形維持只報告）；ja、ko 的 L2 因此改表，驗收時兩者的全形相同組皆為 0。〕
2. 版面（建構的視窗與名字；視窗寬用 phase-304 §2 實測的 32 與 76 單位，其餘幾何以常數列出）：
   - 玩家名在 L0 放不下、L1 放得下：輸出的 `Shrink`、`Col`、W_s、`endCol`、計數（`PlayerNames++`、`PlayerShrunk[0]++`、降段計數不增）；只有 L2 放得下；三個等級都放不下時退成只中文（現行行為）且降段計數增加、縮小計數不增。
   - 同一呼叫兩個名字：第一個在 L0 放得下、第二個不行，兩個單元的 `Shrink` 相同；只有 L2 才放得下時兩個都是 2。
   - NPC 加註：全加 L1 放得下而 L0 放不下（`NameShrunk[0]++`）；單元換列；縮小等級下單元寬於一行時該等級失敗（不斷開）；只加第一次不試縮小；zh 收尾標點與 ja 開括號各一例（附著字維持原大小，併入相鄰一般文字的 `EclTextLine`）；ko 一個 token 含兩個單元的寬度。
   - ko 詞級（單元加助詞）：L0 詞級失敗、L0 字級成功時不縮小；L1、L2 逐等級的「詞級加退回的 fits 與字級相同」；接續（起點在列中間）；前導空白變體（帶空白的 L1 先於不帶空白的 L0，且此時 `SpaceDropped` 不增）；zh 甲板空白分支（檢查套在 `attempt` 回傳的結果上）；`bottom` 限制。
   - `lastRune`、`lastReading` 以單元字元計（依 (`Row`, `Col`) 串接）；`endCol` 以 W_s 計。
   - 純函式：同輸入呼叫兩次輸出逐位元組相同；L0、L1 失敗後 `units`、`text` 切片內容不變。
3. 不變量 §3.8 第 1 條的證明（兩層，各自注明範圍）：
   - 第一層：凍結副本。把 `72ce242` 的 `placeText`（整個方法）與 `layoutPlayerName` 原樣複製成 `placeTextPre056`、`layoutPlayerNamePre056`，只允許改名；`layoutEclTextP` 本身不變，直接沿用。語料維度：`spaceNeeded ∈ {false, true}`、`prevRune`（一般字、`' '`、0）、ko 的 `lead ∈ {0, 有尾音音節, 無尾音音節}`、`fullStop` 固定 false（「。」沒有名字單元）、甲板分支用一個最後一列以「甲板」結尾的合成頁且 `fresh=false`、`isPlayer ∈ {false, true}`；起點掃描每列、每個半格欄；視窗用 phase-304 §2 的 11 種幾何常數。拆成兩部分：
     - 合成語料（名字表片段加固定種子的合成句與玩家名，不閘門）：配摘要常數，只用來證明凍結副本忠實；摘要在 `72ce242` 計算。
     - `text/` 語料（環境變數閘門）：四種語言的 catalog 與 `NameGlossary.Variants`，含名字單元的句子全取，每語言每幾何至多 2,000 筆抽樣、固定種子 56，不設摘要常數（`text/` 會因校對改變），收據記錄 `text/` commit。逐筆比較新舊並分類：舊版第一個空白狀態的全加／完整 L0 → 必須逐位元組相同；不同的每一筆必須屬 §3.8 第 1 條的 (a) 或 (b) 且新版 `Shrink` 不為 0，各類筆數列入 phase 文件。比較函式必須同時比 `Shrink`（現有 `equalLines` 只比 `Row`、`Col`、`Text`，實作任務中擴充或另寫）。
   - 第二層：trace A/B（依賴原版重播紀錄，環境變數閘門）。A = 實作 commit 的父 commit，B = 實作 commit，兩邊從 `git archive` 乾淨匯出；若父 commit 不是 `72ce242`，第一層的摘要在父 commit 重驗。用新腳本（例如 `workplace/phase<N>/ab056.sh`，由 `cleantest.sh` 改成：匯出目錄為 A、B 各一份、gomodcache 唯讀、`GOPROXY=off`、掛載 `workplace/phase257-text-window-trace/cp` 唯讀、`BUCKROGERS_TRACE_*` 輸出）在 Docker 內跑同一個注入檔 `zz_056_invariant_test.go`（兩邊同一檔，SHA-256 記入 phase 文件）。注入檔只走 `ObserveEntry`、`ObserveInstruction`、`Page()`、`EclTextLine` 的 `Row`、`Col`、`Text` 與具名 Stats 欄位，流程照 `TestReplayPhase257Windows` 的 `parseW` 迴圈；輸出鍵為（語言、trace 檔、step）；`Shrink` 以 `reflect.ValueOf(l).FieldByName("Shrink")` 取值（欄位不存在印 `-`），使兩邊都能編譯；B 的 `Shrink` 非 0 筆數另列。也比對 `BUCKROGERS_TRACE_PAGES`、`BUCKROGERS_TRACE_ECL` 的逐訊息畫面與逐呼叫 TSV。兩邊同一份 `text/` 與字型，記錄 repo commit 與字型雜湊。此層 trace 不帶玩家情境（`parseW` 不設 `Player`），只覆蓋 NPC 加註；玩家名的不變量只由第一層證明。
4. 繪製（2×、3×；用 `NewEclTextOverlay` 與測試內建構的頁面）：縮小單元的所有墨點落在各自的字模框內、字模框在遮罩內；單元之外的像素與只畫一般文字時相同；單元內剩餘像素為底色；前景像素數等於衍生字模的墨點數；每段縮小 stamp 的字模框下緣（`GlyphY` ＋ 字模高 − 1）：全形等於同列 L0 全形（2× 為 15、3× 為 22），半形等於列底（2× 為 15、3× 為 23）；3× L1 全形左右各留 1 像素；同一列的一般文字與縮小單元不重疊；後寫的列覆蓋到縮小單元任一格時整個單元不畫；單元起點在頂列 `TopCol` 左側、單元右緣超過右界：整個單元不畫、不裁切、不寫入 slot；設 `Gone` 對應位元後縮小 stamp 消失；縮小 stamp 排在一般段之後、`cols` 同步；`ActiveKeys` 只回原列 key；縮小單元的字不以正常大小再畫一次。〔規格 057 §5.6：本條的繪製測試對預設表與每個語言表參數化重跑（ja、ko）。〕
5. 合成截圖（不做實機）：以 package 內、環境變數閘門的測試產生（例如 `BUCKROGERS_SHRINK_SHOTS=<workplace 目錄>`，缺就 skip）。用 `LoadLiveRuntimeOptions` 載入 `text/` 與 `workplace/pkg-stage/AppDir/font` 的正式字型，取得真實 catalog、`NameGlossary`、`PlayerNames`；字型取各語言通道的字型（`r.lanes[i].font`），zh-TW 對 unifont 與（本機存在時）倚天各出一組，檔名含字型名，倚天截圖只留本機。玩家名固定用預設隊員的真實名字（例如 CELESTE、FLAVIUS，合成長名未必能音譯），以 `eclPlayerEntry`、`eclCtx` 造帶 `PartySnapshot` 的 `EclTextEntry`，視窗取 `23 7 38 9`（32 單位）與 `1 17 38 22`（76 單位）；每次呼叫後以 `ObserveInstruction` 關閉（同 `eclSpaceRet`），用前一次呼叫推進起點欄，製造「L0 放不下、L1 放得下」與「只有 L2 放得下」；NPC 句子從 catalog 挑含名字者，起點欄由測試計算。`ObserveEntry` 後 `Sync`、`Draw` 到單色填滿的 indexed 緩衝（不用原版畫面當底，截圖不含原版素材），寫 PNG。測試同時斷言每張圖的 `Shrink` 等級符合預期，避免截到降段結果。2×、3× 各配 zh-TW、ja、ko，L1 與 L2 各一，另加 zh-TW 倚天一組，存 `workplace/phase<N>-shrink-shots/`，不入版控、不入發行包；phase 文件記錄檔名與 SHA-256，供使用者判斷可讀性。
6. 重播閘門與全套件：`TestReplayPhase257Windows`、`TestReplayPhase257EngineDispatch` 必須是 PASS 而非 SKIP（掛載 `workplace/phase257-text-window-trace/cp`，用 `-v` 輸出確認）。基準是父 commit 乾淨匯出在同環境重跑的輸出；既有 `t.Logf` 行的格式不動，縮小計數另起一行；比較方式：ECL 既有各行逐字相同（允許差異只有 §3.8 第 1 條 (b) 類造成的 `SpaceDropped` 減少，其減少數必須等於採用帶空白縮小的呼叫數），新行的縮小計數預期為 0，非 0 時逐筆列出且每筆都要屬預期差異；engine-dispatch 只比較命中、未命中、溢出。`PlayerShrunk` 在重播中恆為 0，不構成玩家名的證據。`apps/buckrogers` 全套件通過。
7. 沒有做的驗證與狀態：實機同狀態 A/B（#38 的後期名字、手札觸發點、修理表頭）。實作完成後本規格標為「限縮 CONFORMED：機制（版面、繪製、不變量）」，範圍外的實機觸發路徑仍為未知（先例：規格 055）。#38 的關閉留言、`CONTEXT.md` 與 README 只能寫「縮小機制已實作並以單元測試與合成截圖驗收；後期名字、手札觸發點、修理表頭的實機觸發未量或強推論」。AGENTS.md「只有同狀態收據覆蓋的路徑才稱已中文化」不變。
8. 既有測試的處置與突變：
   - 下列測試斷言「放不下就降段」，縮小生效後結果會變：`TestLayoutPlayerNameMatchesPre045WithoutSpace`、`TestLayoutPlayerNameOrder`（`ecl_player_space_test.go` 的「完整單元含空白放不下、不含空白放得下」案例會改選帶空白的 L1）、`TestEclPlayerNameSpaceKo`、`TestEclPlayerNameSpaceNotGluedLikeParticle`、`TestEclPlayerNameContinuationAndFallback`（`player_name_test.go` 內 486 的「弗拉維烏斯」、511 的「一二CELESTE」、519 的「fresh english」三個子案例）、`TestEclNameTiersFallback`（`name_glossary_test.go` 的「Down to no annotation」子案例；「All three overflow」在 L2 仍溢出，不翻）、`TestEclLastReadingChineseOnlyTier`、`TestZhDeckSpacePlayerNameStays`（實作時才發現，它的完整名字放不下時同樣改選縮小）。不翻的已手算：`player_name_test.go:497-499`、`ecl_inline_names_test.go:236-254`。`ko_test.go` 一帶只比 `layoutEclTextP` 對 pre-043 凍結副本，`layoutEclTextP` 不變，不受影響。處置原則：降段分支的覆蓋不能因此消失，每個受影響測試二選一：(a) 改用 L2 也放不下的輸入、維持原斷言；(b) 以 `shrinkLevels` 的空表 helper 跑原斷言。`TestLayoutPlayerNameMatchesPre045WithoutSpace` 改成空表下比對 pre-045，新順序由 §5.3 的凍結副本負責。另新增對應的「縮小生效」案例。直接把預期值改成縮小結果而不保留降段案例，不接受。〔規格 057 §3.2 第 7 點、規格 058 §5.9：以 zh-TW 目錄加 ja 或 ko 排版設定的夾具改以對應語言的目錄建構，保留的 zh-TW 目錄案例為控制組。〕
   - 新增與改寫的案例用能分辨等級的輸出 helper（例如把縮小列印成 `⟨1:…⟩`），不用只串接 `Text` 的 `eclRow`、`rowText`（縮小前後字串相同，無法分辨）；`lastLine` 取最後一個 `EclTextLine`，單元拆列後會拿到尾段，新案例改用 (`Row`, `Col`) 順序的明確索引。
   - 實作會動到的未帶欄名 literal 與比較（`NameUnit` 不改；`EclTextStats` 保持可比較）由實作者在 diff 中確認。
   - 突變表：每個突變由實作者在乾淨匯出上實際套用、跑對應測試、記錄 FAIL；表格三欄（突變、套用位置、應失敗的測試名），收據寫進 phase 文件，不是只宣稱。至少涵蓋：W_s 用 floor；`GlyphY` 改置中或頂對齊；3× 漏掉內縮；3× 用 2× 的衍生字型；縮小 stamp 排在一般段之前；縮小 stamp 未同步追加 `cols`；縮小單元的字仍放進一般列 slots；縮小單元越過 `TopCol` 仍畫；計數在失敗的嘗試也累加；同一呼叫各單元各自選等級；ko 助詞寬度也套縮小比例；「只加第一次」也試縮小；空白分支順序顛倒；保底規則被移除（單點字衍生後全空）；stamp key 衝突；`endCol` 以 W 計；`lastReading` 不含縮小列；空白或 U+3000 被要求字模；衍生門檻 ≥ 改 >；來源改取 12×24 半形；等級順序顛倒；單元在縮小等級可斷開。
   - 另列「實作 commit 的 diff 不含 `text/`、`font/`；`tools/package.sh` 產物清單與前一版比對無新增字型檔」。

## 6. 開放項目

1. 2× 的 L2（全形 8×8）可讀性：預設保留在等級表，使用者看合成截圖後可決定移除；靜態可用性檢查不通過時一律移除。
2. 縮小單元的左緣一律在原半格欄（現行），不置中於 W_s 格內。
3. 「只加第一次」不試縮小（現行設計，維持版本數與行為單純）。
4. 手札的字串列模型是否值得擴充（另開規格，不屬 #38）。
5. `LayoutEclAnnotatedLang`（name-scan）是否回報縮小可放得下（本規格不做）。
6. 玩家名有前導空白時，045 現行「只中文帶空白」先於「完整不帶空白」：完整格式拿掉空白就能以原大小放下時，畫面仍顯示只中文，與本規格「不退成只中文」的精神不盡一致。本規格維持現行（不是新行為）；使用者若要改，是把「完整不帶空白（L0、L1、L2）」移到「只中文帶空白」之前，§3.8 第 1 條與 §5.3 的預期差異要擴大。
