# 第三百二十二階段：名字單元放不下時縮小字體（規格 056、Issue #38）

日期：2026-10-03
狀態：機制完成，規格 056 限縮 CONFORMED（版面、繪製、不變量）。後期名字、手札觸發點與修理表頭的實機觸發未量，維持未知或強推論。
推論等級：**已證實**＝重跑並比對輸出；**強推論**＝由程式或截圖推得、未實跑；**未知**＝未量。
本階段不使用原版畫面與存態；合成截圖由空白 indexed 緩衝畫成，不含原版素材。

## 1. 決定與範圍

- 使用者 2026-10-03 決定：完整格式（NPC「中文(英文)」加註、玩家名）放不下時，名字縮小字體塞進視窗；機制完成即關閉 #38，不再實機測量。
- 範圍：ECL 敘事窗的名字單元，四種語言（zh-TW、zh-CN、ja、ko），2× 與 3× 兩個 presenter。視窗整窗溢出退英文（規格 027 §3.4）、窄欄只顯示中文、手札、054 的句中玩家讀音都不動（規格 056 §3.1、§4）。
- 實作在 dosgolem 本機分支 `p056-shrink`（沒有另推遠端），實作 commit `bba48d9`（父 commit `72ce242`；非測試程式碼自 `f56458e` 起沒有變動，其後的 commit 只加測試）；`buck-rogers-cht-output-overlay` 已快轉並推送到同一 commit。
- 與 `72ce242` 的差異（已證實，`git diff --name-status`）：非測試程式碼是 `shrink.go`（新）、`ecl_text.go`、`ecl_text_overlay.go`、`halfwidth.go`；沒有 `text/`、`font/` 的變動。
  衍生字型只在記憶體（`shrink.go` 沒有 `WriteFile`、`os.Create`），發行包的產物清單不變。`tools/package.sh` 只多一個測試步驟（§4.2）。

## 2. 機制摘要（已證實）

| 項目 | 內容 |
|---|---|
| 等級 | L0 正常；L1 為 3/4（全形 6、半形 3 邏輯像素）；L2 為 1/2（全形 4、半形 2）。單元占 W_s = ⌈像素 / 4⌉ 個半格。等級表是 `var shrinkLevels`。 |
| 試排順序 | 每個版本先 L0，再 L1、L2。玩家名：完整（L0、L1、L2）、只中文、英文，有前導空白時帶空白的版本先於不帶空白。NPC：全加（L0、L1、L2）、只加第一次（不縮小）、不加。 |
| 版面 | 縮小的單元換成 W_s 個私用區占位字元（`U+F0000` 起），既有的 token 化、詞級、禁則、`joinOpening` 原樣執行，排完再展開成「每個縮小單元一個 `EclTextLine`（`Shrink` 為等級）加上一般文字的 `EclTextLine`」。一次呼叫的單元同一等級。 |
| 繪製 | `eclRowTextShrink` 讓縮小單元用 W_s 個 slot 參加後寫覆蓋；越過列起點或右界的單元不畫、不占 slot。縮小 stamp 追加在同列一般段之後，字模底對齊，key 接續 `<列>#<n>`。 |
| 字模衍生 | 全形取 16×16 底字型，半形取 `halfFontsOf(font).For(2)` 的 8×16，面積規則（有墨面積 × 2 ≥ 目標像素面積）縮小；§3 的保底規則另述。 |
| 計數 | `EclTextStats.NameShrunk`、`PlayerShrunk`（`[2]int`，索引為等級 − 1），只在採用的版面計數。 |

## 3. 實作期間的規格修訂（已證實）

規格 056 READY 之後，實作時做第一次靜態可用性檢查（`TestShrinkFontAvailability`，規格 §5.1），原規格的衍生規則（只有面積規則）沒有通過：

| 字型 | 倍率、等級 | 衍生後全空的字 |
|---|---|---|
| 四個語言的字型（zh-TW Unifont、zh-CN、ja、ko） | 2× L1 | `^` |
| 四個語言的字型 | 2× L2 | `` ` `` |
| 四個語言的字型 | 3× L2 | `^` |
| 倚天（本機） | 2× L2 | `.` |

- 原規格的後果：任何字型、倍率的任何字不通過，該等級對全語言與 presenter 一起從 `shrinkLevels` 移除。2× L1、2× L2、3× L2 都有不通過者，L1 與 L2 都會被移除，機制等於沒有做。
  玩家名由玩家輸入，允許的字元集沒有量過，`.`、`^` 可能出現，不能用「名字不會出現這些字」略過。
- 修訂（規格 056 §3.3 的「保底」）：面積規則使整個字模全空、但來源字模有墨時，點亮有墨面積最大的目標像素（並列取列優先、再欄優先的第一個）。面積規則本身與其他字的衍生結果不變；來源無墨的字仍為空。
  修訂同時改了規格 §3.3 的缺字說明、§5.1 的缺字與保底案例、§5.8 的測試清單與突變表一列（「衍生函式對單點字回傳全空」改為「保底規則被移除」）。
- 修訂只加一個作用於「整個字全空」的條件，沒有再送獨立審查；範圍與後果在這裡與規格內文列明，需要覆核時以這一節為準。
- 可重跑的收據：突變 `derive-empty`（移除保底）在乾淨匯出上使 `TestShrinkFontAvailability` 與 `TestDeriveShrinkFontKeepsThinStrokes` 失敗（§4.7）。
- 另一個實作時才發現的差異：`TestZhDeckSpacePlayerNameStays` 在縮小生效後也改選縮小，規格 §5.8 的清單原本沒有它，已補。

## 4. 驗收收據

環境：`eob-remake-go:1.26.7-ebiten2.9.9`，`--network none`，唯讀掛載原始碼、`text/`、字型、trace，`GOPROXY=off`。腳本在 ignored 的 `workplace/phase322/`（`exp.sh` 乾淨匯出、`cleanrun.sh`、`ab056.sh`、`fullsuite.sh`、`runmut.sh`、`final056.sh`）。
輸入身分：Buck repo `text/` 的 tree 為 `3ac90be6aaf48e34a30196ec7526919b56194fcc`（Buck commit `7bfabf5` 之下，`text/` 無變動），字型 SHA-256：

| 字型 | SHA-256 |
|---|---|
| `buckrogers-unifont.golemfnt` | `7675cf4e97986985cbeb4b5ed447a2a56d68f4c5bdaf29f6f650164179042697` |
| `buckrogers-zh-CN.golemfnt` | `2ac47096396778646b9309a59c71d7bba80cf64584d93a782d3b57162cbadd14` |
| `buckrogers-ja.golemfnt` | `67fd7ac928120b50b0ba701def0741921c8c18110d6ba083a3df821e5adb1c06` |
| `buckrogers-ko.golemfnt` | `dea3568a0f764b604764e835083dbc45e1c9ff3569bbf9f46d9a1a58f4ae674a` |
| `buckrogers-eten-top-pad.golemfnt`（本機） | `ebe7f0458ebc19ec113ec2c4cd8f0a66d145eac21e6aa8dff6273594f1b1fdc3` |

### 4.1 單元測試（已證實）

`shrink_test.go` 的案例：等級表逐格（2×、3× 的格寬、字模、內縮、半形字模、`GlyphY`、W_s，L0 等於現行值）、4×4 對 3×3 的逐點已知答案、保底、半形與全形的字模來源、版面（單一單元、單元不可拆、兩個單元同一等級、ja 開括號、ko 詞級與逐等級的詞級與字級 fits 相同、`bottom`）、玩家名（L1、L2、只有 L2、三級都放不下退只中文、前導空白變體）、NPC（全加縮小、只加第一次不縮小、甲板空白、ko 前導空白）、`lastRune`／`lastReading`、純函式、
繪製（墨點只在字模框內、單元之外像素與只畫一般文字相同、字模框下緣、3× L1 左右各留 1、後寫覆蓋、越界、`Gone`、stamp 順序與 `cols` 同步、key 唯一、`ActiveKeys`）。

既有八個斷言「放不下就降段」的測試加了 `noShrink(t)`（空等級表）維持原斷言，各自另有「縮小生效」的對應案例：`TestLayoutPlayerNameShrinks`（取代前兩個版面測試的新順序，舊順序由 §4.3 的凍結副本差異負責）、`TestEclPlayerNameSpaceKoShrink`、`TestEclPlayerNameSpaceNotGluedShrink`、`TestZhDeckSpacePlayerNameShrinks`、`TestEclLastReadingShrunkUnit`、`TestEclNameShrinkWatcher`、`TestEclPlayerNameShrinkWatcher`。降段分支的覆蓋沒有消失。`equalLines` 改為同時比 `Shrink`。

### 4.2 靜態可用性檢查（已證實）

`TestShrinkFontAvailability`（環境變數閘門，用 `-v` 確認 PASS）：每個字型、倍率（2×、3×）、等級（L1、L2）檢查 ASCII 可列印字元、`•`、該語言名字表的譯名用字、音譯允許字集（zh-CN 為 zh-TW 字集經 `translit-zh-CN-map.tsv`）。
來源字模有墨的字在衍生後全空者為 0（共檢查 14,788 個「字、字型、倍率、等級」）。`•` 在 ja、ko 的來源字型沒有字模，L0 也沒有，不屬縮小。

同一檢查已接入 `tools/package.sh` 的 `smoke_shrink`：字型子集與倚天字型建好之後、封裝之前，對剛建的字型跑，必須 PASS 且不得 SKIP。腳本只做語法檢查（`bash -n`）並以 `workplace/pkg-stage/common` 的上一版發行包字型手動跑過一次（PASS，13,064 個檢查）；整個打包流程沒有重跑。

衍生後字模相同的不同來源字（規格 §5.1 要求列出，不作為失敗條件）：

| 字型 | 檢查字數 | 2× L1 | 2× L2 | 3× L1 | 3× L2 |
|---|---|---|---|---|---|
| zh-TW Unifont | 431 | 1 組 | 3 組 | 0 | 1 組 |
| zh-TW 倚天 | 431 | 0 | 3 組 | 0 | 0 |
| zh-CN | 431 | 1 組 | 3 組 | 0 | 1 組 |
| ja | 183 | 1 組 | 6 組 | 0 | 5 組 |
| ko | 2,223 | 1 組 | 315 組（1,232 對） | 0 | 143 組（148 對） |

非 ko 的組：2× L1 為 `H`／`M`；2× L2 為 `1`／`l`、`0`／`O`、`[`／`|`（Unifont 與 zh-CN、ja），倚天為 `,`／`;`、`c`／`o`、`i`／`l`，ja 另有 `ィ`／`ォ`、`ブ`／`プ`、`ボ`／`ポ`；3× L2 為 `H`／`M`，ja 另有 `カ`／`ガ`、`ケ`／`ゲ`、`サ`／`ザ`、`ホ`／`ボ`（濁點在 L2 的字模，2× 為 8×8、3× 為 11×11，消失）。
ko 的 2× L2（8×8）有 315 組不同音節衍生成同一字模，3× L2 有 143 組。清單在 ignored 的 `workplace/phase322/shrink-identical-glyphs.tsv`。這是供使用者判斷是否移除 L2 或 2× L2 的資料，見 §6。

### 4.3 不變量第一層：凍結副本差異（已證實）

`ecl_pre056_freeze_test.go` 是 `72ce242` 的 `placeText` 與 `layoutPlayerName` 原樣複製（只改名）。`ecl_pre056_corpus_test.go` 的合成語料（固定種子，無遊戲文字）：四種語言、11 種視窗幾何（phase-304 §2）、每列的半格欄、空白欠缺與前一字（一般字、空白、無）、ko 的接續音節（無、有尾音、無尾音）、zh 的甲板分支、玩家名各語言 3 至 5 個。

- 摘要：在 `72ce242` 的乾淨匯出上計算，真函式與凍結副本的摘要相同，387,666 次呼叫，SHA-256 `0684a4231742fbc32ba65bbb3bb85871e2905e04fb2204a903267be2bcd4c78c`；摘要常數寫在 `TestPre056FreezeDigest`。
- 差異（`TestShrinkInvariantSynthetic`）：舊版第一個空白狀態就以完整 L0 放得下的呼叫，新版輸出（含 `Shrink`）逐位元組相同；不同者只屬兩類，且新版 `Shrink` 不為 0。違反 0。

| 合成語料 | 呼叫 | 第一狀態 L0（相同） | 降段或溢出而輸出相同 | 類 a（降段改縮小） | 類 b（捨棄空白改縮小） |
|---|---|---|---|---|---|
| NPC（`placeText`） | 333,686 | 302,791 | 20,027 | 10,849 | 19（ja） |
| 玩家名（`layoutPlayerName`） | 53,980 | 52,055 | 1,012 | 913 | 0 |

- `text/` 語料（`TestShrinkInvariantFormalText`，環境變數閘門，固定種子 56，每語言每幾何 2,000 筆；四語言含名字單元的句子 174、174、174、176 句，玩家名各 51 個）：

| 語料 | 呼叫 | 第一狀態 L0（相同） | 降段或溢出而輸出相同 | 類 a | 類 b |
|---|---|---|---|---|---|
| NPC | 88,000 | 60,359 | 24,303 | 3,338 | 0 |
| 玩家名 | 88,000 | 80,983 | 3,129 | 3,888 | 0 |

違反 0。類 b（舊版捨棄空白、新版保住空白並縮小）只在合成語料的 ja 出現 19 次，`text/` 語料沒有出現。

### 4.4 不變量第二層：trace A/B（已證實，限 NPC 加註）

A 為 `72ce242`，B 為 `bba48d9`，兩邊從 `git archive` 乾淨匯出，注入同一個 `zz_056_invariant_test.go`（SHA-256 `36c4d0e811f113a95c5a68aea98e1a7019b18d22bcfb84964c60f49b62aa07f7`），重播 phase257 的 W 紀錄（3,886 次呼叫，四個語言通道，共 15,544 列）。

| 輸出 | A 與 B |
|---|---|
| 逐呼叫的頁面列（`Row`、`Col`、`Shrink`、`Text`）與計數變化 | 逐位元組相同（A 的 `Shrink` 欄位不存在，印 `-`，比對前正規化為 0）；B 的縮小列 0 |
| `BUCKROGERS_TRACE_ECL`（逐呼叫 TSV） | 逐位元組相同 |
| `BUCKROGERS_TRACE_PAGES`（逐訊息畫面） | 逐位元組相同 |
| `BUCKROGERS_TRACE_ENGINE` | 逐位元組相同 |

這一層不帶玩家情境（紀錄沒有），玩家名的不變量只由 §4.3 證明。離線重播中名字加註的降段為 0（phase-304），所以重播中縮小不被觸發，這一層證明的是「沒有名字單元放不下時，新程式與舊程式輸出相同」。

### 4.5 重播閘門與全套件（已證實）

`TestReplayPhase257Windows`、`TestReplayPhase257EngineDispatch`（`-v`）在基準與實作都是 PASS 而非 SKIP。重播輸出的各 `t.Logf` 行（去行號、不含新增的縮小行）逐字相同；新增的縮小行在四個語言都是 `NameShrunk [0 0]、PlayerShrunk [0 0]、SpaceDropped 0`。

`apps/buckrogers` 全套件（`-v`，乾淨匯出，`BUCKROGERS_CHT_ROOT`、四個語言字型、`BUCKROGERS_TRACE_DIR` 皆有設定；本機倚天字型另掛，供靜態檢查使用）：

| | PASS | FAIL | SKIP |
|---|---|---|---|
| 基準 `72ce242` | 465 | 0 | 17 |
| 實作 `bba48d9` | 496 | 0 | 18 |

多出的一個 SKIP 是 `TestShrinkSyntheticShots`（需要 `BUCKROGERS_SHRINK_SHOTS`，§4.6 另跑）；其餘 SKIP 與基準相同。`TestShrinkInvariantFormalText`、`TestShrinkFontAvailability` 在這次全套件中是 PASS。

### 4.6 合成截圖（已證實，不含原版素材）

`TestShrinkSyntheticShots`（環境變數閘門）以真實 `text/` 與字型載入各語言通道，玩家名用 CELESTE，視窗 `23 7 38 9`（32 單位，起點在最後一列由測試計算）；NPC 句子取該語言含名字單元的最長句，視窗 `1 17 38 22`（76 單位）。每張圖斷言頁面的縮小等級符合預期。
2×、3× 各配 zh-TW（Unifont）、ja、ko 的 L1 與 L2 共 12 張，另有 zh-TW 倚天 4 張（只留本機）。圖與 `manifest.tsv` 在 ignored 的 `workplace/phase322/out/shrink-shots-final/`，不入版控、不入發行包。

| 檔名 | SHA-256 | 玩家名、起點欄 | NPC 句 key、起點欄 |
|---|---|---|---|
| `shrink-zh-TW-unifont-2x-L1.png` | `850edf19adb6d6b4e2837d1ba434c2c94379f121e6e96e78ef03b784268ef7fe` | CELESTE、31 | `ecl.4.64.01511`、2 |
| `shrink-zh-TW-unifont-2x-L2.png` | `fd1faab3e81c87ce3184fd2ac30f95e3396750546f9230574fa5820c2d64c109` | CELESTE、33 | `ecl.1.17.02061`、1 |
| `shrink-zh-TW-unifont-3x-L1.png` | `97adaa6709bc7809d27150ae2cc7bc75f46e51bcff92b10f75e8a318cb57a056` | CELESTE、31 | `ecl.4.64.01511`、2 |
| `shrink-zh-TW-unifont-3x-L2.png` | `0ca2c7bac4065e5d666ea8906ba0a311e1d0da806a98a126ab932ff637768466` | CELESTE、33 | `ecl.1.17.02061`、1 |
| `shrink-ja-2x-L1.png` | `af3486191cfbe62d15266c93ec713ecf1496a5c39806d6e551c7bf0ad0d81964` | CELESTE、31 | `ecl.3.50.03469`、1 |
| `shrink-ja-2x-L2.png` | `8a9bb17571005ab92d770df9c9a4581370dc0da412df7822467d7f85e9f2facb` | CELESTE、33 | `ecl.3.49.02603`、1 |
| `shrink-ja-3x-L1.png` | `8ac0c0831e5932077c4294c9e8a6c62542d2bc1ba01d189dd1d047709a9d3294` | CELESTE、31 | `ecl.3.50.03469`、1 |
| `shrink-ja-3x-L2.png` | `d000a9893c5d3168e8387320d7b67da7a5d1aa39ed540e92cb16b2499a491923` | CELESTE、33 | `ecl.3.49.02603`、1 |
| `shrink-ko-2x-L1.png` | `6ef3238bf3b3265b326ebfe42713eb81c0755766be4bf78f03bd60fcb9be0207` | CELESTE、31 | `ecl.5.82.06145`、1 |
| `shrink-ko-2x-L2.png` | `e3650dfe64ecda09f28d6716952c4cfd5fd7a235830194f2e14df79594866ea3` | CELESTE、33 | `ecl.3.49.01526`、1 |
| `shrink-ko-3x-L1.png` | `bd7d6df7b0196ca03e625351e3e197a28889b040532f4285ff554368bb57c789` | CELESTE、31 | `ecl.5.82.06145`、1 |
| `shrink-ko-3x-L2.png` | `029e116880246d2fcb18c55ab1131b5cc79b7f18836e149aaa7aea54c79bb1de` | CELESTE、33 | `ecl.3.49.01526`、1 |
| `shrink-zh-TW-eten-2x-L1.png` | `907ac757030ce48d1c3ff321bd2622c5320a6f1c32ea6b9ed4b289247a6678b7` | CELESTE、31 | `ecl.4.64.01511`、2 |
| `shrink-zh-TW-eten-2x-L2.png` | `3c48090239567e9b39075089fd325b802dcabb21ab9f4cff7e463abbcb1b4969` | CELESTE、33 | `ecl.1.17.02061`、1 |
| `shrink-zh-TW-eten-3x-L1.png` | `b20aa9734f859946b5ad49bc3b70b661b65bae6d21430907db8d80526e68fcff` | CELESTE、31 | `ecl.4.64.01511`、2 |
| `shrink-zh-TW-eten-3x-L2.png` | `26886c176e9196f8995200bd2b98916b7eb6e80f67959039eb999926997dd90a` | CELESTE、33 | `ecl.1.17.02061`、1 |

觀察（強推論，由截圖目視）：L1 在 Unifont 與倚天都清楚；zh-TW、ja 的 L2 全形可辨；ko 的 2× L2 的諺文只剩約 8×8，音節不可辨；半形英文在 2× L2 為 4×8，`1`／`l`、`0`／`O` 同形（§4.2）。

### 4.7 突變表（已證實）

在實作 commit `bba48d9` 的乾淨匯出上逐一套用，跑縮小相關測試（`TestShrink*`、`TestShrunk*`、`TestLayoutEclTextLevel*`、`TestLayoutPlayerName*`、`TestEclPlayerName*`、`TestEclName*`、`TestEclLastReading*`、`TestZhDeck*`、`TestDeriveShrink*`、`TestResample*`、`TestPre056*`）。每個突變的舊字串在檔內恰好出現一次（`workplace/phase322/mut/muts.py`）。
第一輪在 `6aac902` 跑 25 個突變，24 個被擋下，`half-source-x3`（半形來源改 12×24）存活，因為沒有測試比對衍生字模與來源字型；補 `TestShrinkFontsSources` 後在 `bba48d9` 整張表重跑。

| 突變 | 套用位置 | 結果 | 失敗的測試 |
|---|---|---|---|
| wfloor | `shrink.go` `shrinkUnitUnits`：進位改 floor | KILLED | `TestShrinkInvariantSynthetic`、`TestShrinkUnitUnits`、`TestLayoutEclTextLevelSingleUnit`、`TestLayoutEclTextLevelAtomicUnit` 等 12 項 |
| glyphy-top | `shrink.go` 等級表 2× L1：`FullGlyphY`、`HalfGlyphY` 改 0（頂對齊） | KILLED | `TestShrinkLevelTable`、`TestShrunkUnitPixels` |
| glyphy-center | `shrink.go` 等級表 2× L1：`FullGlyphY`、`HalfGlyphY` 改 2（置中） | KILLED | `TestShrinkLevelTable`、`TestShrunkUnitPixels` |
| inset3x | `shrink.go` 等級表 3× L1：`FullInset` 改 0 | KILLED | `TestShrinkLevelTable` |
| x3-as-x2 | `shrink.go` `metrics`：3× 取 2× 的數值 | KILLED | `TestShrunkUnitPixels` |
| stamps-before | `ecl_text_overlay.go` `Sync`：縮小 stamp 放在一般段之前 | KILLED | `TestShrunkUnitPixels` |
| cols-unsynced | `ecl_text_overlay.go` `Sync`：縮小 stamp 不追加 `cols` | KILLED | `TestShrunkUnitPixels`、`TestShrunkUnitLifetimeAndColors` |
| unit-in-slots | `ecl_text_overlay.go` `eclRowTextShrink`：縮小單元處理後不 `continue`，字也進一般 slots | KILLED | `TestShrunkUnitPixels`、`TestShrunkUnitSlots` |
| cross-border-draws | `ecl_text_overlay.go` `eclRowTextShrink`：越界的縮小單元仍加入單元清單 | KILLED | `TestShrunkUnitSlots` |
| count-failed | `ecl_text.go` `attempt`：每試一個等級就累加 `NameShrunk` | KILLED | `TestEclNameShrinkWatcher`、`TestEclNameFirstOnlyIsNotShrunk`、`TestZhDeckSpaceShrinks`、`TestEclNameSpaceKoShrink` 等 5 項 |
| per-unit-level | `shrink.go` `expandShrinkLines`：第二個單元用高一級 | KILLED | `TestShrinkInvariantSynthetic`、`TestShrinkInvariantFormalText`、`TestLayoutEclTextLevelTwoUnits`、`TestEclNameShrinkWatcher` |
| ko-particle-scaled | `shrink.go` `layoutEclTextLevel`：單元寬度連後一個字（助詞）一起縮 | KILLED | `TestLayoutEclTextLevelSingleUnit`、`TestLayoutEclTextLevelAtomicUnit`、`TestLayoutEclTextLevelTwoUnits`、`TestLayoutEclTextLevelKoWord` 等 8 項 |
| first-only-shrinks | `ecl_text.go` `attempt`：「只加第一次」版本也試縮小 | KILLED | `TestEclNameFirstOnlyIsNotShrunk` |
| space-order-npc | `ecl_text.go` `placeText`：帶空白分支先試不帶空白 | KILLED | `TestShrinkInvariantSynthetic`、`TestShrinkInvariantFormalText`、`TestZhDeckSpaceOtherLanguagesUnchanged`、`TestEclNameSpaceKoShrink` |
| space-order-player | `ecl_text.go` `layoutPlayerName`：帶空白的版本不先試 | KILLED | `TestEclPlayerNameSpaceKo`、`TestEclPlayerNameSpaceNotGluedLikeParticle`、`TestLayoutPlayerNameOrder`、`TestShrinkInvariantSynthetic` 等 8 項 |
| derive-empty | `shrink.go` `shrinkGlyph`：移除保底（單點字衍生後全空） | KILLED | `TestShrinkFontAvailability`、`TestDeriveShrinkFontKeepsThinStrokes` |
| key-collision | `shrink.go` `shrinkStamps`：key 從 0 起編 | KILLED | `TestShrunkUnitKeysUnique` |
| endcol-by-W | `shrink.go` `layoutEclTextLevel`：`endCol` 加上 W 與 W_s 的差 | KILLED | `TestLayoutEclTextLevelSingleUnit`、`TestLayoutEclTextLevelAtomicUnit`、`TestLayoutEclTextLevelTwoUnits`、`TestLayoutPlayerNameShrinks` 等 6 項 |
| lastreading-skips-shrunk | `ecl_text.go` `ObserveEntry`：`lastReading` 不含縮小列 | KILLED | `TestEclLastReadingShrunkNPC` |
| blank-needs-glyph | `shrink.go` `missingShrinkRunes`：空白也要字模 | KILLED | `TestShrunkUnitBlankNeedsNoGlyph` |
| threshold-gt | `shrink.go` `resampleGlyph`：門檻 `>=` 改 `>` | KILLED | `TestResampleGlyphKnownAnswer` |
| half-source-x3 | `shrink.go` `shrinkFontsOf`：半形來源改 12×24 | KILLED | `TestShrinkFontsSources` |
| level-order-reversed | `shrink.go`：`init` 把等級表顛倒（L2 先於 L1） | KILLED | `TestShrinkLevelTable`、`TestShrinkUnitUnits`、`TestDeriveShrinkFontKeepsThinStrokes`、`TestLayoutPlayerNameShrinks` 等 12 項 |
| unit-breakable | `shrink.go` `layoutEclTextLevel`：不把單元傳給 `layoutEclTextP`（單元可斷開） | KILLED | `TestLayoutEclTextLevelAtomicUnit`、`TestLayoutEclTextLevelJaOpening` |
| l0-skipped | `ecl_text.go` `layoutPlayerName`：L0 放得下仍往下試縮小 | KILLED | `TestLayoutPlayerNameMatchesPre045WithoutSpace`、`TestEclPlayerNameSpaceKo`、`TestEclPlayerNameSpaceNotGluedLikeParticle`、`TestLayoutPlayerNameOrder` 等 13 項 |

25 個突變全部在乾淨匯出上被擋下（無存活、無編譯失敗）。

## 5. 未量與未知

| 項目 | 狀態 |
|---|---|
| 後期名字（ECL5 之後的 Zane、劇情 NPC 入隊）、太空戰鬥的名字單元是否放不下 | 未知；縮小機制已有，觸發與否未量 |
| 玩家名的完整格式在實機放不下的次數 | 未知（重播不帶玩家情境，`PlayerShrunk` 在重播中恆為 0，不構成證據） |
| 手札觸發點 28、54 與 ECL3 至 6 的 4、8、10、14、22、27、29、30、34、35、39、44、45、46、52、55、63、66、68、70、71 | 未量；手札的資料模型是字串列，縮小機制不處理手札 |
| 修理結果表頭（`frag.0ddcc5022a9c`）欄位 0、17、32 | 強推論；縮小機制不處理 |
| 縮小字在實機的可讀性 | 只有合成截圖與字模相同清單，未實機判讀 |
| 存讀檔、捲動後縮小單元不殘字 | 未做同狀態實機 A/B；繪製的生命週期由單元測試涵蓋（`Gone`、後寫覆蓋、`removeRows` 與頁面消失） |

AGENTS.md 的規定不變：只有被 dosgolem 同狀態收據覆蓋的輸出路徑才稱為已中文化。

## 6. 待使用者決定

- ja 在 L2 的濁點與半濁點消失（`カ`／`ガ` 等）；ko 在 2× L2 有 315 組音節同形。可選擇移除 L2、只移除 2× L2，或維持現狀。目前 `shrinkLevels` 全語言共用，各語言各自的等級表要另改規格。
- 規格 056 §6 第 6 點：045 現行「只中文帶空白」先於「完整不帶空白」，維持現行。
