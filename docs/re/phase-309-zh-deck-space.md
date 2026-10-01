# 第三百零九階段：甲板提示後的數字補空白（規格 048）

日期：2026-10-01
狀態：規格 048 的實作與第一版證據。dosgolem `53fe5a4`；單元測試、離線重播差分、104 個前後對照時點、phase254 七條回歸完成。
推論等級：**已證實**＝重跑測試或腳本並比對輸出；**強推論**＝由程式或截圖推得、未實跑；**未知**＝未量。
原版遊戲與英文原文只在 ignored 的 `workplace/`，本文只記數字、key 與判定。

## 1. 實作內容（已證實）

| 項目 | 內容 | 位置 |
|---|---|---|
| 條件 | zh-TW、zh-CN 的 ECL 續接呼叫：非 fresh、已有頁面、非玩家名（含音譯失敗落入 passthrough）、本次輸出文字以 ASCII 數字起首、起點欄不是左欄、頁面最後一行畫出的文字以 `甲板` 結尾，才在數字前補一個半形空白 | `ecl_text.go` 的 `zhDeckSpace()`、`zhDeckDigitCall()` 與 `ObserveEntry` 的 `!done` 區塊 |
| 放不下 | 先排含空白的文字；排版失敗，或第一個畫出的列不在起點列、不以空白起首（空白把數字推到下一列），退回不含空白，退回後成功則 `SpaceDropped` 加一 | 同上 |
| 不新增頁面狀態 | `owedSpace`、`lastRune` 仍只有詞級 profile（ko）使用；ja、ko、zz 不變 | 單元測試以反射凍結 `EclTextPage` 欄位 |

## 2. 單元測試（已證實）

`ecl_zh_deck_test.go`（13 個）：基本四次與三次呼叫（`甲板 5。你們要往哪裡去？`）、與測試語言「`5` 映射為 ` 5`」的等價對照、十二種不補的情形（前一次以編號、`。`、拉丁字母、`第` 結尾、本次字母或中文起首、第二個數字、譯文自帶尾端空白、原版自畫空白、起點在左欄、fresh、`p == nil`）、多列與 `甲`、`板` 被換列拆開、玩家名四種結果（拿掉 `!isPlayer` 時第四種失敗，已做負對照）、合成 catalog 譯文以數字起首（含 `SetNames`、長句跨列）、引擎翻譯、R=4／3／2／1 的窄寬行為（與審查者推演相同）、ja／zz／ko 三種 profile 的字面期望、頁面狀態未設定與欄位清單、語言碼表、資料閘門（zh-TW、zh-CN 以 `甲板` 結尾的譯文 key 恰為 `ecl.2.32.03956`、`ecl.2.32.09000`、`ecl.2.33.08985`）。
`fullstop_test.go` 兩處期望依規格改：`TestEclFullStopLoneCall`（zh-TW、zh-CN、空字串得 `甲板 5。`，ja 維持 `甲板5。`）、`TestEclFullStopGate` 序列 0。dosgolem `apps/buckrogers` 與 `xlate/...` 全套在 Docker 內以完整環境執行全過（排除既有的 `TestScopedMenuRuntime*` 與未追蹤探針檔）。

## 3. 離線重播差分（已證實）

基準 `post308-1`（dosgolem `65333e2`），新 `post309-1`（`53fe5a4`）：`replay-engine.tsv`、`replay-ecl.tsv`、`baseline-translate.tsv`、`replay-report.tsv` 逐位元組相同；只有 `replay-pages.tsv` 的 `shown` 欄位不同，其餘欄位（calls、hits、misses、overflows）0 列不同。

| 語言 | 變動訊息 | 不重複畫面 | 與預期形式不符 |
|---|---|---|---|
| zh-TW | 74 | 9 | 0 |
| zh-CN | 74 | 9 | 0 |
| ja、ko | 0 | 0 | 不適用 |

預期形式（規格 048 §2）：`r17.36:5 | r17.37:。 | r17.39:你們要往哪裡去？` 變 `r17.36: 5 | r17.38:。 | r17.40:你們要往哪裡去？`，74 則逐則吻合；`SpaceDropped` 0 實例（退回分支只由單元測試覆蓋）。

## 4. 前後對照收據（已證實）

舊：dosgolem `65333e2` 的 runner；新：`53fe5a4` 的 runner；同一份 `text/` 與字型。104 個時點（組成同 phase-308 §4）：機器狀態 104／104 相同、menu 畫面 104／104 相同、live 畫面 100 相同；不同的 4 個是 join 時點（甲板提示）的 zh-TW、zh-CN × 2×、3×，與預期完全一致；ja、ko 全部相同；失敗 0。
目視（ignored 的 `workplace/phase309/png/join-zh-TW.png`）：`…你們身處甲板5。你們要往哪裡去？` 變 `…你們身處甲板 5。你們要往哪裡去？`。

## 5. phase254 七條回歸（已證實）

`rerun42`（新 runner，腳本取自 `rerun40`）：action、body、manual、opening、post、skill、story 七份文字輸出與 `rerun40` 逐位元組相同（行數 10、6、8、6、8、8、6）。

## 6. 未做與後續

1. 字母與漢字相鄰的呼叫邊界、`第`、`編號`、`持有` 結尾的譯文之後的數字、水平選單 `你目前在甲板`、引擎片段 `受到1點傷害`（規格 048 §5）。
2. 規格 048 維持 READY，不升 CONFORMED（整體項目同規格 047）。
