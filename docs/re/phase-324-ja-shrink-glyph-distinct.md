# 第三百二十四階段：ja 縮小字模的濁音字形（規格 057、Issue #42）

日期：2026-10-03
狀態：機制完成，規格 057 限縮 CONFORMED（表、衍生、版面不變量、繪製）。縮小字的實機可讀性、後期名字與手札觸發點的實機觸發未量，維持未知。
推論等級：**已證實**＝重跑並比對輸出；**強推論**＝由程式或截圖推得、未實跑；**未知**＝未量。
本階段不使用原版畫面與存態；合成截圖由空白 indexed 緩衝畫成，不含原版素材。

## 1. 決定與範圍

- 使用者 2026-10-03 看過規格 056 的收據後要求：「ja L2濁音 有獨立字體 カ 和 ガ 要能區分」「依照語言開對應規格」。Issue 各開一個（#42 ja、#43 ko），ja 的格寬維持 8（版面不變）。
- 範圍：ja 通道的 L2 全形字模，2× 由 8×8 改 8×14、3× 由 11×11 改 12×16；ja 的 L1、半形字模、`FullLP`／`HalfLP`、`W_s`、版面、試排順序與計數不變。其他語言的輸出不變。同時建立規格 058（ko）沿用的通用機制。
- 實作在 dosgolem 本機分支 `p057-ja-shrink`，實作 commit `d73de94`（父 commit `bba48d9`；非測試程式碼只有 `shrink.go`、`ecl_text.go`、`ecl_text_overlay.go`，其後沒有變動）。診斷與驗證用的批次腳本在 ignored 的 `workplace/phase322/`、`workplace/phase324/`。

## 2. 機制摘要（已證實）

| 項目 | 內容 |
|---|---|
| 語言表 | `shrinkLevelsFor(lang)`：有覆寫的語言（現為 ja）讀自己的表，其餘讀預設表 `shrinkLevels`（規格 056 的值）。`""` 視同 zh-TW。 |
| 取表的唯一來源 | watcher 讀目錄的語言（`levels()`）；`EclTextPage` 新增 `Lang`，建頁時填入；overlay 的 `Sync` 與 `eclRowTextShrink` 讀頁面的 `Lang`。換語言（F4）不重建任何表。 |
| 等級規格 | `shrinkSpec` 加 `Thr`（面積門檻 n/d，零值為 1/2，只作用於全形字模，不合法值在衍生入口 panic）；`shrinkMetrics` 的全形字模改為矩形（`FullGlyphW`、`FullGlyphH`）。 |
| 純函式 | `layoutEclTextLevel(prof, levels, …)`、`layoutPlayerName(prof, levels, …)` 收表為參數，不讀全域。 |
| 衍生字型快取 | 快取鍵含底字型、完整等級規格與倍率；字型名稱含尺寸與門檻。 |
| 測試輔助 | `withShrinkLevels` 清空所有語言覆寫；`withLangShrinkLevels` 只換一個語言並在 `t.Cleanup` 還原。 |
| ja 的 L2 | `FullLP` 4、`HalfLP` 2、`Thr` 1/2；2× 全形字模 8×14（`GlyphY` 2），3× 12×16（`GlyphY` 7，內縮 0）；半形字模不變。 |

## 3. 實作期間的處置（已證實）

- ko 在規格 057 實作時尚未改表，新的「全形字模兩兩不同」硬性條件對 ko 的 2× L2（312 組）、3× L2（142 組）會失敗。靜態檢查（`TestShrinkFontAvailability`）為 ko 記一個有文字說明、有組數上限的暫時例外，由規格 058 的實作移除；ko 以外的語言沒有例外。
- 規格 057 §3.5 要求「失敗時訊息列出相同組的字」；實作把判定抽成 `shrinkDistinctProblems`，以合成報告測試判定本身（相同組失敗、空字失敗、半形組只報告），否則「把相同當只報告」的突變無法被負向對照殺死。
- 合成截圖的 ja L2 兩張改用 `GILBERT`（音譯為 `ギルバート`，含 `ギ`、`バ`），測試斷言頁面的縮小單元含濁音或半濁音；其餘各張維持 `CELESTE`。
- 突變表第一輪（`23ec66d`）有 3 個存活。`overlay-rowtext-no-lang`、`overlay-miss-no-lang`（overlay 的兩處取表沒有測試分辨）：補 `TestShrunkUnitSlotsFollowPageTable`、`TestShrinkSyncMissingRunesFollowPageTable` 後在 `d73de94` 重跑，兩者被殺。`compare-report-only`：原先寫的突變把條件改成 `known == "" && false`，else 分支仍會報出相同組，所以是不忠實的突變；改成把相同組清單清空（`rep.FullGroups[:0]`）後在 `d73de94` 重跑，被 `TestShrinkDistinctSynthetic` 殺。第一輪的輸出保留在 `workplace/phase322/out/m57-*.at-23ec66d.txt`。

## 4. 驗收收據

環境：Docker 映像 `eob-remake-go:1.26.7-ebiten2.9.9`，`--network none`，目前 UID/GID，原始碼唯讀乾淨匯出（`git archive`），`BUCKROGERS_CHT_ROOT`＝本 repo 的 `text/`（commit `c004c1d`）、四個語言字型與倚天字型（SHA-256 見 phase-322 §4）、`BUCKROGERS_TRACE_DIR`。環境變數閘門的測試以 `-v` 確認為 PASS，不是 SKIP。

### 4.1 表與機制單元測試（已證實）

| 測試 | 內容 |
|---|---|
| `TestShrinkLevelTable` | 預設表與 ja 表逐格比對；幾何關係式（格寬＝`FullLP` × 倍率、字模寬高在格內與列內、內縮、`GlyphY`、框下緣）對預設表與 ja 表各跑一次；L1、L2 順序與 `FullLP`／`HalfLP` 遞減；`Thr` 合法；沒有表的語言（`""`、zh-TW、zh-CN、en、test）讀預設表 |
| `TestResampleGlyphRectAndThr`、`TestShrinkThrAndCacheKey` | 矩形目標已知答案（4×4 對 3×2）、`Thr` 1/3 與 1/2 的差異像素、零值為 1/2、`Thr` 不影響半形、保底規則在矩形目標、不合法值 panic、快取鍵含完整規格 |
| `TestShrinkLevelsHelpers` | `withShrinkLevels` 清空語言覆寫、`withLangShrinkLevels` 只換一個語言、空表關閉、還原 |
| `TestShrinkInjectedTable` | 對 ja 注入 L2（`FullLP` 5、`HalfLP` 3、`Thr` 1/3）：watcher 的 `endCol`、`Shrink`、overlay 的 stamp 寬度與字型尺寸都依注入表；zh-TW、zh-CN、`""` 仍依預設表；載入順序不影響各語言結果 |
| `TestShrinkMissingLevelDrawsNothing`、`TestShrunkUnitSlotsFollowPageTable`、`TestShrinkSyncMissingRunesFollowPageTable` | 表缺等級時單元不畫、不寫 slot、不回報缺字；單元占用的 slot 數與缺字檢查取頁面語言的表 |
| `TestShrinkLanesShareNoTable`（閘門） | 同一個 `LiveRuntime` 載入四語言：各通道 watcher 取自己語言的表；順序與逆序的版面摘要皆等於單獨載入該語言的版面摘要 |
| `TestZhDeckSpaceNoPageState` | 頁面欄位清單加 `Lang` |
| `TestShrunkUnitPixels` 等繪製測試 | 對 `{預設表, ja 表}` 參數化，在 2×、3×、L1、L2 實際 `Sync`／`Draw`：墨點在字模框內、框下緣（全形 2× 15、3× 22；半形 15、23）、單元右緣補底色、`W_s` 格內剩餘像素、stamp 順序與 `cols` 同步、key 唯一 |

### 4.2 ja 的清濁對（已證實）

正式 `buckrogers-ja.golemfnt`（SHA-256 `67fd7ac928120b50b0ba701def0741921c8c18110d6ba083a3df821e5adb1c06`），名字字元集全形且來源字模有墨者 88 字。

| 等級、倍率 | 全形字模 | 全形字模相同組 | 31 個清濁對的最小差異像素數 |
|---|---|---|---|
| L1 2× | 12×12 | 0 | 1（`シジ`） |
| L2 2× | 8×14（056：8×8） | 0（056：3 組） | 2（`ビピ`） |
| L1 3× | 16×16 | 0 | 4（`ビピ`） |
| L2 3× | 12×16（056：11×11） | 0（056：4 組） | 2（`ビピ`） |

- L2 的 31 對每一對都至少有一個差異像素落在字模框上半部右半（判定式 y < ⌊H/2⌋ 且 x ≥ ⌊W/2⌋，濁點所在處）。
- 點陣快照（凍結）：`ガ` 在 2× 8×14 與 3× 12×16 各一個，見 `shrink_ja_test.go` 的 `jaGa2x`、`jaGa3x`。
- 固定探測字集（31 對共 62 字加 `セレステ`）在每個（等級、倍率）的全形衍生字模，依碼點排序串接（含寬高）的 SHA-256（凍結）：

| 等級、倍率 | 摘要 |
|---|---|
| L1 2× | `198dd133b09f4df03180b521811b18ed03f6fcd56626555d6aae0c86e67f47ec` |
| L1 3× | `717f99335a3f3bc4c5804b9e74979f339863cc8f10dc6ab0da96bd9b4082c124` |
| L2 2× | `f078369bd22c89743454f09c4cf10d8f5952c364d78848675dad79800eeaa559` |
| L2 3× | `34da08e12217259dbaa9aa1c5a60dced5137fcfc550a9e2e69502a0ddd243985` |

### 4.3 靜態可用性檢查（已證實）

`TestShrinkFontAvailability`（閘門，`-v` PASS；已接入 `tools/package.sh` 的 `smoke_shrink`，腳本未改）：每個字型、倍率、該語言表的每個等級，名字字元集中來源字模有墨的字衍生後全空者為 0，**全形字模兩兩不同為硬性條件**；預期等級集合（每個語言含 L1 與 L2）與全形字數下限（ja ≥ 88、ko ≥ 2,128、zh-TW 與 zh-CN 各 ≥ 336）寫在測試中。共檢查 14,788 個（字、字型、倍率、等級）。

| 字型 | 檢查字數 | 全形相同組（2× L1／L2、3× L1／L2） | 半形相同組（2× L1／L2、3× L1／L2） |
|---|---|---|---|
| zh-TW Unifont | 431 | 0／0、0／0 | 1／3、0／1 |
| zh-TW 倚天 | 431 | 0／0、0／0 | 0／3、0／0 |
| zh-CN | 431 | 0／0、0／0 | 1／3、0／1 |
| ja | 182 | 0／0、0／0 | 1／3、0／1 |
| ko | 2,222 | 0／**312**、0／**142** | 1／3、0／1 |

- ko 的 312 與 142 組是規格 058 要處理的對象，此階段以有上限的暫時例外記錄（§3），不是本規格的結果。
- 負向對照（證明比較函式有效）：合成字型的精確組數不受 `text/` 影響（`TestShrinkDistinctSynthetic`）；正式 ja 字型加規格 056 的 ja L2 表跑同一個函式，回報含 `カ`／`ガ` 的組（2× 3 組、3× 4 組，數字沿用 phase-323 §3）。
- 半形相同組維持只報告：Unifont、zh-CN、ja 為 `H`／`M`（2× L1）、`1`／`l`、`0`／`O`、`[`／`|`（2× L2）、`H`／`M`（3× L2）；倚天為 `,`／`;`、`c`／`o`、`i`／`l`（2× L2）。另案。

### 4.4 版面不變量（已證實）

- 縮小生效版面摘要（`TestShrinkLayoutDigest`）：規格 056 §5.3 的合成語料（四語言，`placeText` 與 `layoutPlayerName`，含 `Shrink`、`endRow`、`endCol` 與各計數）的 SHA-256 與呼叫數。常數在 `bba48d9` 的乾淨匯出上算出，`d73de94` 的輸出與之相同：

| 語言 | 呼叫 | SHA-256 |
|---|---|---|
| zh-TW | 80,231 | `5a8819d18d023f0b853b4131faac274f9d9737301e63802b584b7b9740d013e1` |
| zh-CN | 78,347 | `66019f0eb63effa30b894944c492622f44f11fe21a8d2e3da880a982c75c960e` |
| ja | 59,971 | `15213337fe31a8b9a53361654a70a4aa4a5ce80285d0d14048d020f49a9eb3a9` |
| ko | 169,117 | `26c3d75bced46b168b0a26049f6c867e67c96a0999724218ffd8db461725d74c` |

- ja 新舊表（`withLangShrinkLevels` 換回 056 的表）逐位元組相同：合成語料 59,971 次呼叫（`TestShrinkJaLayoutSameUnderOldTable`）、`text/` ja 語料 44,000 次呼叫（`TestShrinkJaFormalLayoutSameUnderOldTable`，閘門，每幾何 2,000 筆、種子 56）。
- `text/` 語料逐語言數字與 `bba48d9` 的記錄（`workplace/phase324/baseline-bba48d9-formal.txt`）完全相同（`TestShrinkInvariantFormalText`，違反 0）：

| 語言 | 語料 | 呼叫 | 第一狀態 L0（相同） | 降段或溢出而輸出相同 | 類 a | 類 b | 縮小 L1／L2 |
|---|---|---|---|---|---|---|---|
| zh-TW | 句子 174 | 22,000 | 15,833 | 5,332 | 835 | 0 | 420／415 |
| zh-TW | 玩家名 51 | 22,000 | 20,533 | 707 | 760 | 0 | 377／383 |
| zh-CN | 句子 174 | 22,000 | 15,833 | 5,332 | 835 | 0 | 420／415 |
| zh-CN | 玩家名 51 | 22,000 | 20,533 | 707 | 760 | 0 | 377／383 |
| ja | 句子 174 | 22,000 | 14,228 | 6,809 | 963 | 0 | 368／595 |
| ja | 玩家名 51 | 22,000 | 19,495 | 920 | 1,585 | 0 | 577／1,008 |
| ko | 句子 176 | 22,000 | 14,465 | 6,830 | 705 | 0 | 315／390 |
| ko | 玩家名 51 | 22,000 | 20,422 | 795 | 783 | 0 | 354／429 |

- `TestPre056FreezeDigest`、`TestShrinkInvariantSynthetic`、`TestShrinkInvariantFormalText` 對 `72ce242` 凍結副本的分類結果維持通過。

### 4.5 衍生字型的位元組對照（已證實）

`TestShrinkFontBaseline`：每個通道字型、等級、倍率的全形與半形衍生字型，以 `sha256("shrinkfont1" ‖ 寬 ‖ 高 ‖ 字數 ‖ 依碼點排序的 (碼點, 字模))` 計（不含名稱），基準值是 `bba48d9` 乾淨匯出上算出的 40 列（`apps/buckrogers/testdata/shrink_fonts_baseline.tsv`，以字型檔 SHA-256 對表；表中沒有的字型 SKIP 並說明）。本機含倚天字型時 40 列中 38 列與基準相同；改變的兩列是 ja L2 全形（2×、3×），摘要等於凍結值：

| 列 | 基準 `bba48d9` | `d73de94`（凍結） |
|---|---|---|
| ja L2 2× 全形 | `d04ee0e1c6c27d0bc89c7521e0224ba43501acdd6c92a2fad137566d46840799` | `cc863e36c0578ef3c6900b6c8d1558fb86082bd66e9440a0586569ec58750a6c` |
| ja L2 3× 全形 | `bb10b143d985c65d9e694c5c03ffbe1039d6ca3aca739ffc7303479ae4d17988` | `2a2f0234a2f4ccfb58936f61d1522c228eab0f1302e0331f899d93e2512ba019` |

### 4.6 trace A/B 與重播閘門（已證實，限不縮小的路徑）

A 為 `bba48d9`，B 為 `d73de94`，兩邊從 `git archive` 乾淨匯出，注入同一個 `zz_056_invariant_test.go`（SHA-256 見 phase-322 §4.4），重播 phase257 的 W 紀錄（15,544 次呼叫、縮小列 0）。四份輸出逐位元組相同：

| 輸出 | SHA-256（A＝B） |
|---|---|
| 逐呼叫頁面列與計數（`ab-*.tsv`） | `20855139083f4db2ad42484674309a0e79370db0250ee082e28b0432fa3ed497` |
| `BUCKROGERS_TRACE_ECL` | `c059ad3abcca7faae34fbeda82be5eb4277a596c49b39779acf0ffe4f6d2d5c9` |
| `BUCKROGERS_TRACE_PAGES` | `8642edcf6f64aad8cce3f1f0c1257a3169a83f5a8cb8193470481f568215e9ee` |
| `BUCKROGERS_TRACE_ENGINE` | `9712dfe3ec10fc8da90d97bc92a6d62fc9bbaa262e992126323d6b7aa1b686d8` |

`TestReplayPhase257Windows`、`TestReplayPhase257EngineDispatch`（`-v`）在 A、B 都是 PASS。離線重播中名字加註的降段為 0，縮小不被觸發；這一層只證明不縮小的路徑不受影響，不證明繪製正確（繪製由 §4.1、§4.7 負責）。

### 4.7 全套件與合成截圖（已證實，不含原版素材）

`apps/buckrogers` 全套件（`-v`，乾淨匯出，倚天字型另掛）：

| | PASS | FAIL | SKIP |
|---|---|---|---|
| 基準 `bba48d9` | 496 | 0 | 18 |
| 實作 `d73de94` | 512 | 0 | 18 |

SKIP 的集合與基準逐項相同（18 個；其中 `TestShrinkSyntheticShots` 需要 `BUCKROGERS_SHRINK_SHOTS`，下方另跑，其餘 17 個在基準就已 SKIP）。實作多出的 16 個 PASS 全是本階段新增的測試：`TestResampleGlyphRectAndThr`、`TestShrinkDistinctSynthetic`、`TestShrinkFontBaseline`、`TestShrinkInjectedTable`、`TestShrinkJaFormalLayoutSameUnderOldTable`、`TestShrinkJaLayoutSameUnderOldTable`、`TestShrinkJaProbeDigests`、`TestShrinkJaSnapshots`、`TestShrinkJaVoicedPairs`、`TestShrinkLanesShareNoTable`、`TestShrinkLayoutDigest`、`TestShrinkLevelsHelpers`、`TestShrinkMissingLevelDrawsNothing`、`TestShrinkSyncMissingRunesFollowPageTable`、`TestShrinkThrAndCacheKey`、`TestShrunkUnitSlotsFollowPageTable`；基準的 PASS 沒有任何一項消失。`TestShrinkInvariantFormalText`、`TestShrinkFontAvailability`、`TestShrinkLayoutDigest` 等閘門測試在這次全套件中是 PASS，不是 SKIP。

`TestShrinkSyntheticShots`（閘門）：zh-TW（Unifont）、ja、ko 的 2×、3×、L1、L2 共 12 張，另有倚天 4 張（只留本機）。ja L2 的玩家名改用 `GILBERT`（`ギルバート`）。重拍的只有 ja L2 兩張，其餘 14 張的 SHA-256 與 phase-322 §4.6 逐一相同：

| 檔名 | SHA-256 | 玩家名、起點欄 |
|---|---|---|
| `shrink-ja-2x-L2.png` | `6c144e004b1dcd45cd5b1ac8223681f138b8dcd11306b3bfe712f28458c63461` | GILBERT、32 |
| `shrink-ja-3x-L2.png` | `0c4cc1eba719d04e1493ff80ea94cf8db7a3db1731e43b6f26e076ece5c5df01` | GILBERT、32 |

每張圖斷言頁面的縮小等級，並斷言每個縮小單元的 stamp 從單元的欄起接續、字寬加總與 `W_s` 一致，占用 `W_s` × 4 × 倍率像素。

觀察（強推論，由截圖目視）：`ギルバート` 的濁點在 8×14 與 12×16 是獨立像素；8 像素寬的片假名整體仍粗糙（`セ` 近似 `ヒ`、`テ` 近似 `ヲ`），見 §6。

### 4.8 既有測試的處置

- 簽名跟著改（`layoutEclTextLevel`、`layoutPlayerName` 收表）：`ecl_player_freeze045_test.go`、`ecl_player_space_test.go`、`ecl_shrink_invariant_test.go`、`shrink_test.go`。
- 頁面欄位清單加 `Lang`：`ecl_zh_deck_test.go`。
- 斷言 056 的 ja L2 數值者改為新值，並保留預設表為控制組：`TestShrinkLevelTable`、繪製測試的表參數化。
- 以 zh-TW 目錄加 ja 或 ko 排版設定的夾具：ja 的縮小案例以 `LangJa` 目錄建構（`eclFixtureLang`），zh-TW 目錄的案例保留為控制組；ko 的對應改動在規格 058。

### 4.9 突變表（已證實）

在乾淨匯出上逐一套用（第一輪在 `23ec66d`，它與 `d73de94` 只差 §3 的兩個新增測試；存活的 3 項在 `d73de94` 重跑，結果取重跑的），跑縮小相關測試（`TestShrink*`、`TestShrunk*`、`TestLayoutEclTextLevel*`、`TestLayoutPlayerName*`、`TestEclPlayerName*`、`TestEclName*`、`TestEclLastReading*`、`TestZhDeck*`、`TestDeriveShrink*`、`TestResample*`、`TestPre056*`、`TestEclNameFirstOnly*`、`TestDeck*`，環境變數閘門的測試皆有掛載）。表由 `workplace/phase322/mut057/muts.py` 定義，執行腳本 `runmut057.sh`。

| 突變 | 說明 | 結果 | 失敗的測試 |
|---|---|---|---|
| h-eq-w | ja L2 高度改回等於寬 | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` |
| wh-swap | 字模寬高對調 | KILLED | `TestShrinkFontBaseline` `TestShrinkJaVoicedPairs` |
| ja-glyphy-old-2x | ja 2× GlyphY 用舊值 8 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| ja-glyphy-old-3x | ja 3× GlyphY 用舊值 12 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| ja-3x-no-c0 | ja 3× 漏減 L0 內縮（GlyphY 8） | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| ja-inset-1 | ja 2× 內縮 1 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |
| thr-on-half | Thr 套到半形 | KILLED | `TestShrinkThrAndCacheKey` |
| thr-swapped | Thr 分子分母對調 | KILLED | `TestShrinkFontBaseline` `TestShrinkDistinctSynthetic` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkJaSnapshots` `TestShrinkJaProbeDigests` `TestShrinkThrAndCacheKey` `TestShrinkFontsSources` |
| thr-zero-raw | Thr 零值不正規化（得 0/0） | KILLED | `TestShrinkFontBaseline` `TestShrinkDistinctSynthetic` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkJaSnapshots` `TestShrinkJaProbeDigests` `TestShrinkThrAndCacheKey` |
| thr-gt | Thr 門檻 ≥ 改 > | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkJaSnapshots` `TestShrinkJaProbeDigests` `TestResampleGlyphRectAndThr` `TestResampleGlyphKnownAnswer` |
| thr-not-validated | Thr 不合法值不 panic | KILLED | `TestShrinkThrAndCacheKey` |
| cache-key-no-spec | 快取鍵只含底字型、等級編號與倍率 | KILLED | `TestShrinkDistinctSynthetic` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkThrAndCacheKey` |
| cache-key-no-thr | 快取鍵不含 Thr | KILLED | `TestShrinkThrAndCacheKey` |
| watcher-default-table | watcher 取預設表 | KILLED | `TestShrinkInjectedTable` `TestShrinkLanesShareNoTable` |
| player-ignores-table | layoutPlayerName 不取傳入的表 | KILLED | `TestShrinkInjectedTable` |
| overlay-rowtext-no-lang | eclRowTextShrink 不取頁面語言 | KILLED | `TestShrunkUnitSlotsFollowPageTable` |
| overlay-miss-no-lang | Sync 的缺字檢查不取頁面語言 | KILLED | `TestShrinkSyncMissingRunesFollowPageTable` |
| overlay-stamps-no-lang | Sync 的 stamp 不取頁面語言 | KILLED | `TestShrinkInjectedTable` `TestShrunkUnitPixels` |
| page-lang-unfilled | 建頁漏填 Lang | KILLED | `TestShrinkInjectedTable` |
| ja-table-unregistered | ja 表沒有登記 | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkJaSnapshots` |
| ja-table-empty | ja 表為空 | KILLED | `TestShrinkLayoutDigest` `TestShrinkFontAvailability` `TestShrinkJaSnapshots` |
| helper-no-clear | withShrinkLevels 不清空語言覆寫 | KILLED | `TestShrinkLevelsHelpers` |
| table-pollution | 取語言表時改寫預設表（載入順序污染） | KILLED | `TestShrinkFontBaseline` `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` `TestShrinkThrAndCacheKey` `TestShrinkLevelsHelpers` `TestShrinkInjectedTable` `TestShrinkLevelTable` |
| compare-no-full | 比較函式不比較全形字模 | KILLED | `TestShrinkDistinctSynthetic` `TestShrinkFontAvailability` |
| compare-report-only | 相同組只報告不失敗 | KILLED | `TestShrinkDistinctSynthetic` |
| compare-skips-l1 | 比較函式只比最後一級（不比 L1） | KILLED | `TestShrinkDistinctSynthetic` |
| charset-truncated | ja 字元集載入不全 | KILLED | `TestShrinkFontAvailability` `TestShrinkJaVoicedPairs` |
| ja-l1-halfy | ja L1 的 3× 半形 GlyphY 被改動 | KILLED | `TestShrinkLevelTable` `TestShrunkUnitPixels` |

28 個突變：被擋下 28、存活 0、編譯失敗 0。

## 5. 未量與未知

- 縮小字在實機的可讀性：本階段只保證字模互異與清濁對的最小差異像素數，不宣稱讀者看得出。
- 後期名字、手札觸發點 28／54 與 ECL3 至 6、修理表頭欄位 0／17／32 的實機觸發：同 phase-322 §5。
- 半形英文字母的相同組與高度比（全形變高後半形與全形的高度比為 4:7 與 6:16）：所有語言共有，另案。
- 發行包：不含本階段的變動，未重發。

## 6. 待使用者決定

- ja 的 L2 若要更清楚：格寬改 5 邏輯像素（10 像素）、字模 10×12、`Thr` 1/3，名字字元集 0 組相同、清濁對最小差異 3 個像素，`セ`／`ヒ` 的差異從 5 個像素增為 19 個；代價是 ja 的 L2 單元變寬（`W_s` = ⌈(5F + 2H) / 4⌉），需要新規格與同規格 058 的差異分類。使用者 2026-10-03 選擇維持格寬 8。
- 2× 的 8×14 比 L1 的 12×12 更高更窄；8×12 與 L1 等高，但 `ブ`／`プ`、`ボ`／`ポ` 只差 1 個像素。
