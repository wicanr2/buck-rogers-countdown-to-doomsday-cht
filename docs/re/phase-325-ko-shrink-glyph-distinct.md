# 第三百二十五階段：ko 縮小字模的音節互異（規格 058、Issue #43）

日期：2026-10-03
狀態：機制完成，規格 058 限縮 CONFORMED（表、衍生、版面不變量、繪製）。縮小字的實機可讀性、後期名字與手札觸發點的實機觸發未量，維持未知。
推論等級：**已證實**＝重跑並比對輸出；**強推論**＝由程式或截圖推得、未實跑；**未知**＝未量。
本階段不使用原版畫面與存態；合成截圖由空白 indexed 緩衝畫成，不含原版素材。

## 1. 決定與範圍

- 使用者 2026-10-03 看過規格 056 的收據後要求：「ko 在 2× L2 有 315 組音節字模相同 不同意, 需要完善 korean 發音」「依照語言開對應規格」。規格 058 把「發音」解讀為諺文音節在縮小後仍可彼此分辨；音譯規則（規格 045）與讀音續接（規格 054）不改。
- 範圍：ko 通道的 L2。邏輯像素格寬由 4 改 5（`W_s` = ⌈(5F + 2H) / 4⌉），2× 全形字模由 8×8 改 10×12、3× 由 11×11 改 15×16，面積門檻由 1/2 改 1/3；ko 的 L1、半形字模與 `HalfLP`、試排順序、計數不變。其他語言的輸出不變。
- 前置：規格 057 的實作（通用機制）與其收據（phase-324）。
- 實作在 dosgolem 本機分支 `p058-ko-shrink`，實作 commit `beca734`（父 commit `d73de94`，即規格 057 的實作 commit）；非測試程式碼只多了 `shrink.go` 的 ko 表與登記。

## 2. 機制摘要（已證實）

ko 的 L2：`FullLP` 5、`HalfLP` 2、`Thr` 1/3。

| 倍率 | 全形格寬 | 全形字模 寬×高 | 內縮 | 全形 `GlyphY` | 半形字模 | 半形 `GlyphY` |
|---|---|---|---|---|---|---|
| 2× | 10（056：8） | 10×12（056：8×8） | 0 | 4（056：8） | 4×8（不變） | 8（不變） |
| 3× | 15（056：12） | 15×16（056：11×11） | 0 | 7（056：12） | 6×12（不變） | 12（不變） |

## 3. 實作期間的處置（已證實）

- 規格 057 為 ko 記的暫時例外（312／142 組）與其上限檢查隨本規格移除；`shrinkDistinctProblems` 不再有例外參數。
- 規格 057 的兩個 overlay 取表測試（`TestShrunkUnitSlotsFollowPageTable`、`TestShrinkSyncMissingRunesFollowPageTable`）加 ko 案例。
- 以 zh-TW 目錄加 ko 排版設定的夾具改以 `LangKo` 目錄建構：`koPlayerCallLang`（`ecl_player_space_test.go`；`koPlayerCall` 保留為 zh-TW 目錄的控制組）、`TestEclPlayerNameSpaceKoShrink`、`TestEclPlayerNameSpaceNotGluedShrink`（兩個目錄各跑，`도(DOE)` 在兩張表的 L2 都是 4 單位）、`TestEclNameSpaceKoShrink`（ko 目錄用 ko 表，另跑換回規格 056 表的控制組）。
- `TestEclNameSpaceKoShrink` 的原句 `가자 벅(BUCK)이 왔다`：新 L2 為 17 單位，沒有 16 單位視窗可容納，故 8 欄視窗改為退到不加註；另補句 `이왔다`（L2 16 單位）涵蓋 L2 生效的視窗。

## 4. 驗收收據

環境同 phase-324 §4（`BUCKROGERS_CHT_ROOT`＝本 repo 的 `text/`，commit `c004c1d`）。ko 字型 `buckrogers-ko.golemfnt`，SHA-256 `dea3568a0f764b604764e835083dbc45e1c9ff3569bbf9f46d9a1a58f4ae674a`。

### 4.1 表與機制（已證實）

- `TestShrinkLevelTable`：ko 的 L1 等於預設 L1、L2 逐格等於上表；幾何關係式與表層級約束對預設、ja、ko 三張表各跑一次。
- `TestShrinkUnitUnitsKo`：`W_s` 的 F、H 組合與進位（`셀레스트(CELESTE)` L2 為 10、`벅(BUCK)` 為 5、`도(DOE)` 為 4 等）；ko L2 比預設 L2 最多寬 ⌈F/4⌉ 個半格且不寬於 L1。
- `TestShrinkInjectedTable`：未注入時各語言的結果（ko：`endCol` 12、字模 10×12、`CellW` 5、2；ja 與 zh 維持）；對 ja 與對 ko 各注入 `FullLP` 5、`HalfLP` 3 的 L2，watcher、頁面與 overlay 都依注入表，其他語言不受影響；載入順序不影響各語言結果。
- `TestLayoutEclTextLevelKoWord`、`TestLayoutEclTextLevelKoTwoUnits`：ko 詞級加退回字級的 fits 與字級相同（預設表與 ko 表各驗）；一個 token 含兩個單元的寬度逐級驗算；ko 的 L2 在 16 單位視窗放不下 17 單位的文字。
- 繪製測試（`TestShrunkUnitPixels` 等）對 ko 表參數化：格寬 10／15 放字模寬 10／15、字模高 12／16、`GlyphY`、框下緣、單元右緣補底色與 `W_s` 格內剩餘像素。
- `TestShrinkLanesShareNoTable`（閘門）：四語言載入的版面摘要（順序、逆序）等於單獨載入。

### 4.2 音節互異（已證實）

| 等級、倍率 | 全形字模 | 名字字元集 2,128 字的字模相同組 |
|---|---|---|
| L1 2× | 12×12 | 0 |
| **L2 2×** | **10×12**（056：8×8） | **0**（056：312 組） |
| L1 3× | 16×16 | 0 |
| **L2 3×** | **15×16**（056：11×11） | **0**（056：142 組） |

負向對照：正式 ko 字型加規格 056 的 ko L2 表跑同一個比較函式，2× 回報 312 組、3× 回報 142 組，並含 `게`／`계`（2×）、`갠`／`갱`（3×）。半形字模相同組維持只報告（2× L2 為 `0`／`O`、`1`／`l`、`[`／`|`；3× L2 為 `H`／`M`），另案。`tools/package.sh` 的 `smoke_shrink` 沒有改，它跑的 `TestShrinkFontAvailability` 已不含 ko 例外。

### 4.3 易混音素家族、代表組與凍結值（已證實）

家族以初聲 L、中聲 V、終聲 T 分解（終聲為空也算一種），取兩音節在該位置以外相同的所有對；表內為名字字元集內該家族所有對的最小差異像素數（`TestShrinkKoFamilies`，對數與下限、代表對都在測試中斷言）：

| 家族 | 對數 | 2× L2 10×12（下限） | 代表對 | 3× L2 15×16（下限） |
|---|---|---|---|---|
| `ㅏ`／`ㅣ` | 112 | 1（≥ 1） | `가기` | 2（≥ 2） |
| `ㅔ`／`ㅐ` | 112 | 2（≥ 2） | `게개` | 3（≥ 3） |
| `ㅔ`／`ㅖ` | 112 | 2（≥ 2） | `겍곅` | 3（≥ 3） |
| `ㅓ`／`ㅔ` | 112 | 17（≥ 17） | `걸겔` | 34（≥ 34） |
| 終聲 `ㅁ`／`ㅇ` | 266 | 2（≥ 2） | `감강` | 3（≥ 3） |
| 終聲 `ㄴ`／`ㅇ` | 266 | 8（≥ 8） | `곤공` | 13（≥ 13） |
| 初聲 `ㄷ`／`ㅌ` | 152 | 3（≥ 3） | `다타` | 5（≥ 5） |
| 初聲 `ㄱ`／`ㅋ` | 152 | 3（≥ 3） | `각칵` | 4（≥ 4） |

- 規格 §1 的代表組 `게`／`계`、`네`／`녜`、`겍`／`곅`、`갠`／`갱`、`독`／`톡` 在 L1、L2、兩個倍率的字模都不同（`TestShrinkKoRepresentativePairs`）。
- 點陣快照（凍結）：`셀` 在 2× 10×12 與 3× 15×16 各一個（`ㅔ` 的兩根豎筆保留，與 `설`、`샐` 相差至少 2 個像素），見 `shrink_ko_test.go` 的 `koSel2x`、`koSel3x`。
- 固定探測字集（八個家族的代表對共 16 字、§1 的代表組、`셀레스트`、`플라비우스`、`마리온`、`알키메데스`）在每個（等級、倍率）的全形衍生字模摘要（凍結）：

| 等級、倍率 | 摘要 |
|---|---|
| L1 2× | `ae7571c58f8b417c5c5ba15b3d1ad125d6fa61a04989b1d478d01f2ed5d35d3c` |
| L1 3× | `01e6032ceb0e1acbf8ac8127125825e57244129db5bd25add9b93bfaf075647a` |
| L2 2× | `ea264b3f550cb7d03900c0ae3555baa5940b14a61e74ca2f636ea83e52dbc976` |
| L2 3× | `9596abe34128579a65808bfbfb8e2b1a36b62eb9a619b149db3baa68dec7e2b2` |

### 4.4 版面不變量（已證實）

同一份程式、ko 通道換回規格 056 的 L2 表（`withLangShrinkLevels`）得到舊輸出，與新輸出逐呼叫比對並依規格 058 §3.4 分類（`TestShrinkKoClassifySynthetic`、`TestShrinkKoClassifyFormalText`）。第 3 條與 2c 皆為 0，違反 0。2b 的落點只有「舊 L2 → 新版只中文（`NameTierNone`）」與少量「舊 L2 → 新版只加第一次（`NameTierFirst`）」；玩家名為「完整格式 → 只中文」（`kind=1`），帶空白與不帶空白各一。

| 語料 | 呼叫 | 第 1 條相同 | 2a-i | 2a-ii 換列 | 2a-ii 斷行不同 | 2b | 2c | 第 3 條 | 舊 L1／L2 | 新 L1／L2 |
|---|---|---|---|---|---|---|---|---|---|---|
| 合成 `placeText` | 147,525 | 145,674 | 1,251 | 87 | 39 | 474 | 0 | 0 | 1,662／1,851 | 1,662／1,377 |
| 合成 `layoutPlayerName` | 21,592 | 21,394 | 132 | 0 | 0 | 66 | 0 | 0 | 165／198 | 165／132 |
| `text/` 句子 176 | 22,000 | 21,610 | 260 | 11 | 47 | 72 | 0 | 0 | 315／390 | 315／318 |
| `text/` 玩家名 51 | 22,000 | 21,571 | 319 | 0 | 0 | 110 | 0 | 0 | 354／429 | 354／319 |

2b 落點明細：合成 `placeText` 474 筆全為「舊 L2 → 只中文」；合成玩家名 44 筆不帶空白、22 筆帶空白（完整 → 只中文）；`text/` 句子 68 筆舊 L2 → 只中文、1 筆舊 L2 → 只加第一次、1 筆帶續接標記（`marker`）舊 L2 → 只中文、2 筆 `SpaceDropped` 為 1 的舊 L2 → 只中文；`text/` 玩家名 64 筆不帶空白、46 筆帶空白。`Stats` 的各計數器由這些欄位推得（`NameShrunk`、`PlayerShrunk`、`NameFirstOnly`、`NameUnannotated`、`PlayerNameChineseOnly`、`SpaceDropped`），差異就是上表的「舊 L2」減少量與 2b 落點。2a-i 的位置由測試依單元的 F、H 另算（Δ = ⌈(5F + 2H) / 4⌉ − ⌈(4F + 2H) / 4⌉），不呼叫被測程式；2a-ii 以不變式 (a) 至 (d) 驗證，對舊輸出也跑同一組。

- 縮小生效版面摘要（`TestShrinkLayoutDigest`）：zh-TW、zh-CN、ja 的常數與規格 057 相同；ko 重新記錄，呼叫數不變：

| 語言 | 呼叫 | SHA-256 |
|---|---|---|
| ko（`bba48d9` 與規格 057） | 169,117 | `26c3d75bced46b168b0a26049f6c867e67c96a0999724218ffd8db461725d74c` |
| ko（本規格） | 169,117 | `0d621fc6595f43d5ad9ab880cd4e6aac7dc4aa642d64b4c9b84b32ea5f7e00ae` |

- `text/` 語料 zh-TW、zh-CN、ja 的筆數與規格 057 實作時記錄的逐語言數字相同（`TestShrinkInvariantFormalText`，違反 0）；ko 的第一狀態 L0、輸出相同、類 a 與縮小 L1／L2 與 `bba48d9` 記錄的差異如下：

| ko 語料 | 呼叫 | 第一狀態 L0 | 降段或溢出而輸出相同 | 類 a | 縮小 L1／L2 |
|---|---|---|---|---|---|
| 句子 176（`bba48d9`） | 22,000 | 14,465 | 6,830 | 705 | 315／390 |
| 句子 176（本規格） | 22,000 | 14,465 | 6,902 | 633 | 315／318 |
| 玩家名 51（`bba48d9`） | 22,000 | 20,422 | 795 | 783 | 354／429 |
| 玩家名 51（本規格） | 22,000 | 20,422 | 905 | 673 | 354／319 |

### 4.5 衍生字型的位元組對照（已證實）

`TestShrinkFontBaseline`：除 ko L2 全形外，所有通道、等級、倍率的衍生字型與基準相同（ja L2 全形以規格 057 凍結的值為準，其餘為 `bba48d9`）。本機含倚天字型時 40 列中 36 列與基準相同，改變的四列是 ja L2 全形（2×、3×）與 ko L2 全形（2×、3×）：

| 列 | 基準 `bba48d9` | 本規格（凍結） |
|---|---|---|
| ko L2 2× 全形 | `497f6aefd497991eecb676bea6f9dbcd54a7637cf28fea51008e5c92a0c8e9a7` | `022926e95a68edd0590bdf891eaf90418a05042352e9ef9866c5457a5fb2731d` |
| ko L2 3× 全形 | `dfced2e373563abc621a3c74064d2ae65027cbd1fdd0508645df1c9ac8274f41` | `1fa0b12845617d77e65fc1783c4b902106f077a8ef4cb388bd8dc0ef3f0022ce` |

### 4.6 trace A/B 與重播閘門（已證實，限不縮小的路徑）

A 為規格 057 的實作 commit `d73de94`，B 為本規格的實作 commit `beca734`，沿用 phase-324 §4.6 的做法。四份輸出逐位元組相同：

| 輸出 | SHA-256（A＝B） |
|---|---|
| 逐呼叫頁面列與計數 | `20855139083f4db2ad42484674309a0e79370db0250ee082e28b0432fa3ed497` |
| `BUCKROGERS_TRACE_ECL` | `c059ad3abcca7faae34fbeda82be5eb4277a596c49b39779acf0ffe4f6d2d5c9` |
| `BUCKROGERS_TRACE_PAGES` | `8642edcf6f64aad8cce3f1f0c1257a3169a83f5a8cb8193470481f568215e9ee` |
| `BUCKROGERS_TRACE_ENGINE` | `9712dfe3ec10fc8da90d97bc92a6d62fc9bbaa262e992126323d6b7aa1b686d8` |

`TestReplayPhase257Windows`、`TestReplayPhase257EngineDispatch` 在 A、B 都是 PASS。

### 4.7 全套件與合成截圖（已證實，不含原版素材）

`apps/buckrogers` 全套件（`-v`，乾淨匯出，倚天字型另掛）：

| | PASS | FAIL | SKIP |
|---|---|---|---|
| 基準 `d73de94` | 512 | 0 | 18 |
| 實作 `beca734` | 520 | 0 | 18 |

SKIP 的集合與基準逐項相同（18 個，與規格 057 的全套件相同）。實作多出的 8 個 PASS 全是本階段新增的測試：`TestLayoutEclTextLevelKoTwoUnits`、`TestShrinkKoClassifyFormalText`、`TestShrinkKoClassifySynthetic`、`TestShrinkKoFamilies`、`TestShrinkKoProbeDigests`、`TestShrinkKoRepresentativePairs`、`TestShrinkKoSnapshots`、`TestShrinkUnitUnitsKo`；基準的 PASS 沒有任何一項消失。閘門測試（`TestShrinkInvariantFormalText`、`TestShrinkFontAvailability`、`TestShrinkLayoutDigest`、`TestShrinkKoClassifyFormalText` 等）在這次全套件中是 PASS，不是 SKIP。

`TestShrinkSyntheticShots`：只重拍 ko 的 2×、3× L2 兩張，其餘 14 張（含 ko L1 兩張與規格 057 重拍的 ja L2 兩張）的 SHA-256 與規格 057 實作後的清單逐一相同：

| 檔名 | SHA-256 | 玩家名、起點欄 |
|---|---|---|
| `shrink-ko-2x-L2.png` | `eefaf345428a5bcdf17712fe05ed7231e00efa31d60c37b2b9396fdd58663c70` | CELESTE、33 |
| `shrink-ko-3x-L2.png` | `68decfc19df116634d36d08267c08b64dda1bb955211ca51e59cf4334ac1d3bf` | CELESTE、33 |

每張圖斷言頁面的縮小等級與每個縮小單元占用 `W_s` × 4 × 倍率像素。

### 4.8 突變表（已證實）

在乾淨匯出上逐一套用，跑縮小相關測試（同 phase-324 §4.9）。44 個突變分三組平行跑：28 個在 `0cd8171` 的匯出上（它與 `beca734` 的差別只有兩個 overlay 取表測試，見 §3），16 個在 `beca734` 的匯出上（`overlay-miss-no-lang` 因匯出目錄被後來補跑的一組覆寫，實際跑的是 `beca734`）。第一組曾因 `compare-report-only` 的舊字串在 058 的測試中不存在（`shrinkDistinctProblems` 去掉例外參數後寫法變了）而沒有套用，改寫該突變後整組在 `beca734` 重跑。測試只增不減，在較早的匯出上被擋下的突變在 `beca734` 仍被擋下。

表由 `workplace/phase322/mut058/muts.py` 定義：規格 057 的通用機制突變在本規格的測試集上重跑，加上 ko 專屬的突變。

| 突變 | 說明 | 結果 | 失敗的測試 |
|---|---|---|---|
| h-eq-w | ja L2 高度改回等於寬 | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` |
| wh-swap | 字模寬高對調 | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` |
| ja-glyphy-old-2x | ja 2× GlyphY 用舊值 8 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| ja-glyphy-old-3x | ja 3× GlyphY 用舊值 12 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| ja-3x-no-c0 | ja 3× 漏減 L0 內縮（GlyphY 8） | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| ja-inset-1 | ja 2× 內縮 1 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| thr-on-half | Thr 套到半形 | KILLED | `TestShrinkFontBaseline` `TestShrinkThrAndCacheKey` |
| thr-swapped | Thr 分子分母對調 | KILLED | `TestShrinkFontBaseline` `TestShrinkDistinctSynthetic` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkJaSnapshots` `TestShrinkJaProbeDigests` `TestShrinkKoFamilies` `TestShrinkKoRepresentativePairs` `TestShrinkKoSnapshots` `TestShrinkKoProbeDigests` `TestShrinkThrAndCacheKey` `TestShrinkFontsSources` |
| thr-zero-raw | Thr 零值不正規化（得 0/0） | KILLED | `TestShrinkFontBaseline` `TestShrinkDistinctSynthetic` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkJaSnapshots` `TestShrinkJaProbeDigests` `TestShrinkKoRepresentativePairs` `TestShrinkKoProbeDigests` `TestShrinkThrAndCacheKey` |
| thr-gt | Thr 門檻 ≥ 改 > | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkJaSnapshots` `TestShrinkJaProbeDigests` `TestShrinkKoRepresentativePairs` `TestShrinkKoProbeDigests` `TestResampleGlyphRectAndThr` `TestResampleGlyphKnownAnswer` |
| thr-not-validated | Thr 不合法值不 panic | KILLED | `TestShrinkThrAndCacheKey` |
| cache-key-no-spec | 快取鍵只含底字型、等級編號與倍率 | KILLED | `TestShrinkDistinctSynthetic` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkKoRepresentativePairs` `TestShrinkThrAndCacheKey` |
| cache-key-no-thr | 快取鍵不含 Thr | KILLED | `TestShrinkThrAndCacheKey` |
| watcher-default-table | watcher 取預設表 | KILLED | `TestShrinkLayoutDigest` `TestShrinkKoClassifySynthetic` `TestShrinkKoClassifyFormalText` `TestShrinkInjectedTable` `TestShrinkLanesShareNoTable` `TestEclPlayerNameSpaceKoShrink` `TestEclNameSpaceKoShrink` |
| player-ignores-table | layoutPlayerName 不取傳入的表 | KILLED | `TestShrinkLayoutDigest` `TestShrinkKoClassifySynthetic` `TestShrinkKoClassifyFormalText` `TestShrinkInjectedTable` `TestEclPlayerNameSpaceKoShrink` |
| overlay-rowtext-no-lang | eclRowTextShrink 不取頁面語言 | KILLED | `TestShrunkUnitSlotsFollowPageTable` |
| overlay-miss-no-lang | Sync 的缺字檢查不取頁面語言 | KILLED | `TestShrinkSyncMissingRunesFollowPageTable` |
| overlay-stamps-no-lang | Sync 的 stamp 不取頁面語言 | KILLED | `TestShrinkInjectedTable` `TestShrunkUnitPixels` |
| page-lang-unfilled | 建頁漏填 Lang | KILLED | `TestShrinkInjectedTable` |
| ja-table-unregistered | ja 表沒有登記 | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkJaSnapshots` |
| ja-table-empty | ja 表為空 | KILLED | `TestShrinkLayoutDigest` `TestShrinkFontAvailability` `TestShrinkJaSnapshots` |
| helper-no-clear | withShrinkLevels 不清空語言覆寫 | KILLED | `TestEclLastReadingChineseOnlyTier` `TestShrinkLevelsHelpers` |
| table-pollution | 取語言表時改寫預設表（載入順序污染） | KILLED | `TestShrinkLayoutDigest` `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkKoClassifySynthetic` `TestShrinkKoClassifyFormalText` `TestShrinkKoRepresentativePairs` `TestShrinkThrAndCacheKey` `TestShrinkLevelsHelpers` `TestShrinkInjectedTable` `TestShrinkLanesShareNoTable` `TestShrinkLevelTable` `TestShrinkUnitUnits` `TestLayoutEclTextLevelSingleUnit` `TestLayoutEclTextLevelKoWord` `TestLayoutEclTextLevelKoTwoUnits` `TestLayoutPlayerNameShrinks` `TestEclPlayerNameSpaceKoShrink` `TestEclNameFirstOnlyIsNotShrunk` `TestEclNameSpaceKoShrink` |
| compare-no-full | 比較函式不比較全形字模 | KILLED | `TestShrinkDistinctSynthetic` `TestShrinkFontAvailability` |
| compare-skips-l1 | 比較函式只比最後一級（不比 L1） | KILLED | `TestShrinkDistinctSynthetic` |
| charset-truncated | ja 字元集載入不全 | KILLED | `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkKoFamilies` |
| ja-l1-halfy | ja L1 的 3× 半形 GlyphY 被改動 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| compare-report-only | 相同組只報告不失敗 | KILLED | `TestShrinkDistinctSynthetic` |
| ko-fulllp-4 | ko L2 FullLP 改回 4 | KILLED | `TestShrinkLayoutDigest` `TestShrinkKoClassifySynthetic` `TestShrinkKoClassifyFormalText` `TestShrinkInjectedTable` `TestShrinkLevelTable` `TestShrinkUnitUnitsKo` `TestLayoutEclTextLevelKoWord` `TestLayoutEclTextLevelKoTwoUnits` `TestEclPlayerNameSpaceKoShrink` `TestShrunkUnitPixels` `TestEclNameSpaceKoShrink` |
| ko-glyph-8x8 | ko 2× 字模改回 8×8 | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkKoFamilies` `TestShrinkKoRepresentativePairs` `TestShrinkKoSnapshots` |
| ko-glyph-11x11 | ko 3× 字模改回 11×11 | KILLED | `TestShrinkFontBaseline` `TestShrinkKoFamilies` `TestShrinkKoSnapshots` |
| ko-thr-half | ko Thr 改回 1/2 | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkKoFamilies` `TestShrinkKoSnapshots` `TestShrinkKoProbeDigests` `TestShrinkLevelTable` |
| ko-thr-quarter | ko Thr 改 1/4 | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkKoFamilies` `TestShrinkKoSnapshots` `TestShrinkKoProbeDigests` `TestShrinkLevelTable` |
| ko-glyphy-old-2x | ko 2× GlyphY 用舊值 8 | 未跑 | |
| ko-glyphy-old-3x | ko 3× GlyphY 用舊值 12 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| ko-3x-no-c0 | ko 3× 漏減 L0 內縮（GlyphY 8） | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| ko-inset-1 | ko 2× 內縮 1 | 未跑 | |
| ws-f-coeff-4 | W_s 的 F 係數用 4 | KILLED | `TestShrinkLayoutDigest` `TestShrinkKoClassifySynthetic` `TestShrinkKoClassifyFormalText` `TestShrinkInjectedTable` `TestShrunkUnitSlotsFollowPageTable` `TestShrinkUnitUnits` `TestShrinkUnitUnitsKo` `TestLayoutEclTextLevelSingleUnit` `TestLayoutEclTextLevelAtomicUnit` `TestLayoutEclTextLevelTwoUnits` `TestLayoutEclTextLevelKoWord` `TestLayoutEclTextLevelKoTwoUnits` `TestLayoutPlayerNameShrinks` `TestEclPlayerNameShrinkWatcher` `TestEclPlayerNameSpaceKoShrink` `TestShrunkUnitPixels` `TestLayoutEclTextLevelJaOpening` `TestEclNameSpaceKoShrink` `TestEclPlayerNameSpaceNotGluedShrink` `TestZhDeckSpacePlayerNameShrinks` |
| ws-h-coeff-3 | W_s 的 H 係數用 3 | KILLED | `TestShrinkLayoutDigest` `TestShrinkKoClassifySynthetic` `TestShrinkKoClassifyFormalText` `TestShrinkInjectedTable` `TestShrinkUnitUnits` `TestShrinkUnitUnitsKo` `TestLayoutEclTextLevelSingleUnit` `TestLayoutEclTextLevelAtomicUnit` `TestLayoutEclTextLevelKoWord` `TestLayoutEclTextLevelKoTwoUnits` `TestLayoutPlayerNameShrinks` `TestEclPlayerNameSpaceKoShrink` `TestEclNameFirstOnlyIsNotShrunk` `TestEclNameSpaceKoShrink` |
| ko-table-is-ja | ko 通道誤取 ja 表 | KILLED | `TestShrinkLayoutDigest` `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkKoClassifySynthetic` `TestShrinkKoClassifyFormalText` `TestShrinkKoFamilies` `TestShrinkKoRepresentativePairs` `TestShrinkKoSnapshots` |
| ja-table-is-ko | ja 通道誤取 ko 表 | KILLED | `TestShrinkLayoutDigest` `TestShrinkFontBaseline` `TestShrinkJaSnapshots` `TestShrinkJaProbeDigests` `TestShrinkJaLayoutSameUnderOldTable` `TestShrinkJaFormalLayoutSameUnderOldTable` `TestShrinkInjectedTable` `TestShrinkLevelTable` |
| ko-table-empty | ko 表為空 | KILLED | `TestShrinkLayoutDigest` `TestShrinkFontAvailability` `TestShrinkKoClassifySynthetic` `TestShrinkKoClassifyFormalText` `TestShrinkKoFamilies` |
| ko-table-unregistered | ko 表沒有登記 | 未跑 | |
| ko-l1-halfy | ko L1 的 3× 半形 GlyphY 被改動 | KILLED | `TestShrinkLevelTable` `TestShrinkUnitUnitsKo` `TestShrunkUnitPixels` |

44 個突變：被擋下 41、存活 0、編譯失敗 0。

## 5. 未量與未知

- 縮小字在實機的可讀性：本階段只保證字模互異與易混家族的最小差異像素數，不宣稱讀者看得出。門檻 1/3 讓筆畫變粗，2× 的右緣欄有墨的字占 74%，相鄰字間距只剩 1 像素，比 L1 緊。
- 後期名字、手札觸發點 28／54 與 ECL3 至 6、修理表頭欄位 0／17／32 的實機觸發：同 phase-322 §5。
- 半形英文字母的相同組與高度比（2× 8:12、3× 12:16）：所有語言共有，另案。使用者提到的 315 組中的 3 組屬此。
- 發行包：不含本階段的變動，未重發。

## 6. 待使用者決定

- ko 的 L2 比規格 056 寬約 F/4 個半格，部分呼叫多降一段（§4.4 的 2b）；若要保持原寬，音節仍有相同組（格寬 8 時最少 17 對），與本規格的目標衝突。
- 字模高度與 `Thr` 可在不動版面的前提下替換（10×13 門檻 1/3 的家族最小差異為 1、2、2、20、2、8、3、3），可讀性未驗證。
