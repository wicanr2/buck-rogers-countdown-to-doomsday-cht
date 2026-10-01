# 第三百零六階段：原版單獨畫出的句號改全形

日期：2026-10-01
狀態：規格 047 的實作與第一版證據。dosgolem `2d8723d`（只加觀測）、`e972d06`（凍結 `6680221`）、`43a1e27`（行為）；離線重播差分、單元測試、104 個前後對照時點、phase254 七條回歸完成。
推論等級：**已證實**＝重跑測試或腳本並比對輸出；**強推論**＝由程式或截圖推得、未實跑；**未知**＝未量。
原版遊戲與英文原文只在 ignored 的 `workplace/`，本文只記數字、key 與判定。

## 1. 實作內容（已證實）

| 項目 | 內容 | 位置 |
|---|---|---|
| ECL 單獨句點 | zh-TW、zh-CN、ja：passthrough 的呼叫原文恰為 `.` 或 `. `、前面是我們畫的頁、不是玩家名時改畫 `。`（`. ` 的空白不顯示）。`。` 放不下（排版失敗，或結束列不等於起點列）時退回原文，不使頁失效 | `ecl_text.go` |
| 語言進 watcher | `EclTextCatalog.lang`（載入時設定，空字串為 zh-TW），`fullStop()` 為 zh-TW、zh-CN、ja；不看排版 profile，也不看字型有沒有 `。`（ko 字型沒有 U+3002） | `ecl_text.go` |
| 計數與紀錄 | `EclTextStats.FullStop`（進入本節處理的次數）、`FullStopDropped`（其中退回原文者）；`ecl` 紀錄列追加 `dFullStop`、`dFullStopDropped` | `ecl_text.go`、`replay_trace.go` |
| zh 範本欄位 | zh-TW、zh-CN：來源為 `_`、值為數字加句點、且範本內有該 `{i}` 時去掉句點，句尾不是終止標點就補 `。`；ja、ko、zz 走改動前的程式 | `joining.go`（`fillTemplateZh`）、`engine_text.go` |
| 離線重播輸出 | `BUCKROGERS_TRACE_ECL`（每次 ECL 呼叫一列 `ecl`）、`BUCKROGERS_TRACE_TRANSLATE`（W 紀錄全部不同原文的各語言 `Translate` 結果）；缺字硬線擴到全部語言 | `trace_replay_test.go` |
| 譯文 | zh-TW 三條以 `第` 結尾的 ECL 譯文改成 `甲板` 結尾（`ecl.2.32.03956`、`ecl.2.32.09000`、`ecl.2.33.08985`）；zh-CN 由生成器重產 | `text/ecl-text.zh-TW.tsv`、`text/ecl-text.zh-CN.tsv` |

## 2. 單元測試（已證實）

| 測試 | 保證 |
|---|---|
| `TestEclFullStopLoneCall` | zh-TW、zh-CN、ja、空字串語言碼：`DECK `、數字、`.` 或 `. ` 得 `甲板5。`，`FullStop` 為 1、`FullStopDropped` 為 0，`Hits`、`Misses`、`Passthrough` 與對照語言相同，`key` 仍為 `passthrough`；ko、zz 與對照逐位元相同 |
| `TestEclFullStopNeedsAPageOfOurs`、`TestEclFullStopPlayerNameStays` | 前面是未翻譯英文、fresh、玩家名為 `.` 的情形不處理 |
| `TestEclFullStopRoom` | 剩 2 單位得 `。`；剩 1、0 單位、末列退回原文，頁與未啟用語言逐位元相同，溢出數相同，`FullStopDropped` 為 1 |
| `TestEclFullStopGate` | `5.`、`...`、`!`、`?`、`x.`、`  .`、` .` 等呼叫：zh-TW、zh-CN、ja、ko 的頁與全部 `Stats` 與對照語言逐位元相同 |
| `TestEngineJoinZhDifferenceIsTemplateDigitPeriod` | zh-TW、zh-CN：3,033 個引擎字串中，與凍結的 pre-046 副本不同的恰為 14 個「範本且有數字加句點欄位」的字串，期望值由凍結副本加獨立規則產生，逐筆相同；其餘 3,019 個與凍結副本逐筆相同。語料含 `tpl.needs`、`tpl.destroyed`、`tpl.drop`、中段欄位與已有終止標點的情形 |
| `TestFrozenTranslateLine046MatchesRealAtFreeze`、`TestEngineJoinJaKoUnchangedBySpec047` | 以 `6680221` 的 `translateLine` 凍結副本（摘要 ja `d4816978…`、ko `c02e0975…`，取自該 commit 的真實函式）證明 ja、ko 輸出不變 |
| `TestEngineJoinUnchangedForOtherLanguages` | 語言清單縮為 zz（`""` 就是 zh-TW），摘要仍是 pre-046 的 `b7b9bc5f…` |
| `TestTemplateFieldPeriod` | zh-TW 兩列期望依規格改：`編號 38。`、`對5使用解毒劑。` |

dosgolem `apps/buckrogers` 全套在 Docker 內以完整環境（`BUCKROGERS_CHT_ROOT`、四語字型、`BUCKROGERS_TRACE_DIR`，離線重播實際執行）執行：除 phase-305 §8 記錄的兩個既有字型雜湊失效測試（`TestScopedMenuRuntime*IfAvailable`）外全過，並排除 dosgolem 工作樹中未追蹤的 `TestCommandStatus*` 探針檔。

## 3. 離線重播差分（已證實）

基準 `post046-2`（`6680221` 加只加觀測的 commit，行為相同，與 `post046-1` 的畫面與引擎檔逐位元相同），對照 `post047-1`，`diff047.py`：

| 語言 | 畫面變動 | calls／hits／misses／overflows 不同的訊息 | `ecl` 列命中欄不同 | `FullStop` | `FullStopDropped` | 半形句點畫面 前→後 | 替換規則對不上 |
|---|---|---|---|---|---|---|---|
| zh-TW | 18 種（84 則） | 0 | 0 | 76 | 0 | 18→0 | 0 |
| zh-CN | 18 種（84 則） | 0 | 0 | 76 | 0 | 18→0 | 0 |
| ja | 11 種（76 則） | 0 | 0 | 76 | 0 | 11→0 | 0 |
| ko | 0 | 0 | 0 | 0 | 0 | 不適用 | 0 |

- 「半形句點畫面」：畫面中的 ASCII `.`（不含 `...`），前後不同時為拉丁字母，排除 `SCOT.DOS`。
- 引擎呼叫（`replay-engine.tsv`）與基準逐位元相同；引擎層字串（`baseline-translate.tsv`）zh-TW、zh-CN 各恰 7 個手札記錄句不同（`…編號 N.` 變 `…編號 N。`），ja、ko 0 個。
- 每則變動畫面只來自三種替換（`第N.` 變 `甲板N。`、單獨 `.` 或 `. ` 變 `。`、`編號 N.` 變 `編號 N。`），其餘位元組相同。
- ECL 溢出 0（四個語言）；缺字 0（zh-TW 用出貨用的倚天字型、zh-CN 用現行簡體字型）。
- 各視窗頁尾餘列：以 `2d8723d` 與現行樹用同一份（新）資料各跑一次，兩份 `各視窗頁尾餘列` 與 `ECL：` 紀錄行完全相同。
- 單獨句點呼叫起點欄最大 58，`。` 的退回門檻是 77，`FullStopDropped` 在實例中為 0，退回分支只由單元測試覆蓋。

zh-TW 與 zh-CN 的 A 型（deck 提示）因 `第` 變 `甲板`、`.` 變 `。`，問句起點右移 3 單位，改後最大列尾 55，距上限 78 還有 23 單位；ja 右移 1 單位，列尾 67。

## 4. 前後對照收據（已證實）

舊版：`6680221` 的 runner 加規格 047 之前的 `text/`（`d1f93b1`）；新版：現行 runner 加現行 `text/`。同一狀態、同一組按鍵，104 個時點：五個時點（ecl、hmenu、logbook、manual、join）× {zh-TW、zh-CN、ja、ko} × 2×、3× 共 40，加 16 個家族時點 × 四個語言（2×）共 64。

| 結果 | 數字 |
|---|---|
| 機器狀態（記憶體、CPU、indexed、palette、停止步數）舊新相同 | 104／104 |
| 畫面（live RGBA）舊新相同 | 98 |
| 畫面不同 | 6：join 時點（步數 `26334000000`，deck 提示）的 zh-TW、zh-CN、ja × 2×、3×，全部是預期 |
| ko 的全部時點 | 畫面與機器狀態相同 |
| 失敗 | 0 |

join 時點 2× 畫面（ignored 的 `workplace/phase306/join-*-2x*.png`）：zh-TW 由 `…你們身處第5.你們要往哪裡去？` 變 `…你們身處甲板5。你們要往哪裡去？`；ja 由 `…デッキ5.どこへ行く？` 變 `…デッキ5。どこへ行く？`。

phase254 七條回歸（`rerun40`，新 runner）：見 §5。

## 5. phase254 七條回歸

新 runner（`rerun40`，現行 `text/`）的七份文字輸出（story、opening、manual、post、skill、action、body）與 `rerun39`（及其對照的 `rerun36`）逐位元組相同，行數 6、6、8、8、8、10、6；七條都是 zh-TW 預設語言，不含 deck 提示。

## 6. 資料與工具檢查（已證實）

| 項目 | 結果 |
|---|---|
| `zh_cn_convert.py` 產生、`--check`、`zh_cn_check.sh` | 通過；`text/zh-CN-term-review.tsv` 的 `ecl.2.32.03956` 列的 `zh_tw_sha256` 改為新譯文的雜湊（`63360d45…`） |
| `catalog_font.py chars` zh-TW、zh-CN、ja、ko | 與版控的字元清單逐位元組相同（字元集合不變） |
| `catalog_font.py lint`、`name_glossary.py lint` | 通過 |
| `ja_check.sh`、`ko_check.sh` | 通過 |
| `eten_font.py build` 重建倚天字型 | 輸出與現行字型逐位元組相同（`ebe7f045…`），只有 manifest 的 `ecl-text.zh-TW.tsv` 雜湊不同；已換 manifest（舊檔留為 `pre047.json.bak`），`eten_font.py verify` 通過 |
| `ecl_translation_merge.py --check-only` | 21 批、譯文 2,544、錯誤 0；`workplace/ecl-l10n/done/` 內三條舊值已同步 |

## 7. 未做與後續

1. `ecl.4.66.08710`（`巡邏至第`）、`ecl.4.66.08952`（`入侵者位於第`）與 ja 的 `ecl.4.66.01705`、`ecl.4.66.02870` 仍以 `第` 收尾，trace 沒有後續呼叫（規格 047 §5）。
2. zh-TW、zh-CN 的 `甲板5。` 數字與漢字之間沒有空白，與靜態譯文 `第 3 層甲板`、範本 `編號 38。` 不同（規格 047 §5，需決定是否為 zh 加呼叫起點補空白）。
3. 規格 047 §3.6 (7) 重新抽審：對 A、B、C、D 型畫面新舊對照，以上第 3、4 節已逐筆列出變動畫面，沒有另派審查者。
4. 規格仍為 READY：§4 的 1 到 5 項已達成，未升 CONFORMED 的原因與規格 046 同（雙語抽審、水平選單放寬、Windows／macOS 打包模擬等整體項目未做）。
