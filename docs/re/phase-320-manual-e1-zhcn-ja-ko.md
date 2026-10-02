# 第三百二十階段：手冊 E1 擴及 zh-CN、ja、ko（規格 055，Issue #40）

日期：2026-10-02
狀態：規格 055 READY 並實作驗收（限縮 CONFORMED，範圍見 §6）；dosgolem `72ce242`。發行包尚未重發。
推論等級：**已證實**＝重跑並比對輸出；**未知**＝未量。
手冊題畫面不入 Git，也不描述其內容；畫格只在 ignored 的 `workplace/phase320/`、`workplace/phase311/runs/p320-*`。
各題在四種語言的列數與「E1 與固定格是否不同」見 [phase-320-e1-sets.tsv](phase-320-e1-sets.tsv)（只有 key 與數字）。

## 1. 輸入（已證實）

| 項目 | 值 |
|---|---|
| A（實作的父 commit） | dosgolem `039727e`，乾淨匯出；runner `b414cad47d3f1194…`、`buckrogers-play` `980ad5940dc64191…`（前 16 碼） |
| B（實作 commit） | dosgolem `72ce242`，乾淨匯出；runner `da34b8344f10307c…`、`buckrogers-play` `6031f2ceb864d545…` |
| 字型與譯文 | 發行字型 `workplace/pkg-stage/AppDir/font/`（zh-TW `buckrogers-unifont.golemfnt` SHA-256 `7675cf4e…`、zh-CN `2ac47096…`、ja `87ea61ba…`、ko `aa271de2…`），現行 `text/`（同一份給 A、B） |
| 離線快照 | `workplace/probe/phase12-before-question.state`，停在步數 266,650,000，不送按鍵，runner 不傳 `-manual-english` |
| 實機腳本 | `workplace/phase311/path-repair.txt`，5,700 格，3×，`-frame-every 10`，四種語言各一次，另一次 `-lang en` 作對照 |

建置腳本 `workplace/phase320/build-one.sh`（Docker、`--network none`、`GOPROXY=off`，從 `git archive` 的乾淨匯出建）。

## 2. 單元與套件測試（已證實）

- plan 放寬（`manual_e1_ascii_terminal_test.go`，3 項）：接受 `甲...`、`「甲...」`、`(甲...)`、`「甲.」`、`RAM.`、`甲,乙`、`甲/乙`、`甲/RAM`、`甲(RAM.)乙` 等；拒絕六個既有負例、段首與空白之後的 `. , : ! ? /`、括號內第一個 token 的標點，以及 `(.A)`、`(/A)`、`(.5)`、`（.A）`、`A（/1）`；
  折進前一個 token 的寬度（`甲...` = 24 + 3×12、`RAM.` = 3×12 + 12）與列首不出現標點（35 個全形字後的 `字,` 一起移到下一列）。
- 三個突變各被擋下：括號專名不要求首字英數、空白之後的標點不拒、`/` 不看前一字元。
- 啟用矩陣反轉（`manual_e1_live_test.go`）：{zh-TW, zh-CN, ja, ko, LangTest} × {2×, 3×}，只有前四種語言的 3× 啟用；zh-TW 以外的通道 `manualE1Active` 為假（關鍵字並存檢查只屬 zh-TW）。
  合成預檢失敗負例、runtime 退路（含非 E1 原因第二次仍失敗只計一次）對四種語言各驗一次；含空譯文段落的通道預檢略過、顯示走 `Missing`。
- 正式 catalog（`manual_e1_langs_live_test.go`，zh-CN、ja、ko 各一）：預檢 39／39；E1 列數與固定格 zh-CN 相同 38、較少 1，ja、ko 相同 39；2× 位元組不受 E1 開關影響；3× 差異只在手冊清底矩形內，E1 與固定格不同的段數 zh-CN 24、ja 27、ko 26；破壞 derived 字型後 `Compose(3)` 不 panic 且 `skips["manual"]` 加一。
- 版面摘要凍結（`manual_e1_formal_langs_test.go`）：zh-TW、zh-CN、ja 各 39 段的版面摘要（行號、token 種類、runes、x、advance）與放寬前相同；摘要綁定 catalog 與字型檔的 SHA-256，不符時 SKIP 並印出原因。
- 一次性證據：A、B 兩個乾淨匯出對 zh-TW、zh-CN、ja 共 117 段逐段比 `CanonicalHash`，**117／117 相同**；ko 在 A 是 39 段全報錯，在 B 是 39 段全成功。
- 乾淨匯出（不含未入版控檔）設 `BUCKROGERS_CHT_ROOT` 與 `BUCK_OWNER_PROJECT`：`go vet` 通過；`apps/buckrogers` A 455 項 PASS、B 463 項 PASS，各 0 FAIL、19 SKIP（缺 `BUCKROGERS_ZZ_DIR`、`BUCKROGERS_PKG_ROOT` 等）。
  另以 `BUCKROGERS_ZZ_DIR` 指向舊的 zz 測試資料（`workplace/phase299-zh-cn/zz`）跑一次：A、B 都有同一項失敗（`TestLiveRuntimeLanguageLoadFailureIsIsolated`，zz 資料的技能離開句寬度過期），與本規格無關，所以收據用不設 zz 的結果。
- `tools/ko_check.sh`、`ja_check.sh` 不受影響（沒改 TSV）；`tools/package.sh linux` 通過（dosgolem `72ce242`，`TestPackagedLanes` 對四種語言各自的區塊斷言 `manual-e1=on` 並檢查各 lane 的 `e1Base`，外洩掃描 254 個檔案、237 個雜湊、268 個檔名，無命中）。

## 3. 離線同狀態重播（已證實）

`workplace/phase320/offline.sh`（`cases.sh`、`compare-ab.py`）：zh-TW、zh-CN、ja、ko、en × 2×、3×，A、B 各跑（共 20 次重播）。

| 檢查 | 結果 |
|---|---|
| `memory_sha256`、`cpu_sha256`、indexed、palette、停止步數（A 對 B，十個組合） | 全部相同 |
| 2× 五種語言的 live RGBA | A、B 位元組相同 |
| 3× 的 zh-TW、en | A、B 位元組相同（zh-TW 的 E1 輸出不因放寬而變） |
| 3× zh-CN | 8,888 個像素不同，bbox (49,217)–(897,286)，在手冊清底矩形內 |
| 3× ja | 9,766 個像素不同，bbox (50,217)–(898,285)，在手冊清底矩形內 |
| 3× ko | A、B 位元組相同（預期） |

這個快照顯示的題是 `manual.page34.deimos_prison.word10`，在 zh-TW、zh-CN、ja 是「E1 與固定格不同」，在 ko 是「相同」（k = k' = 3），所以 ko 的離線 A/B 是不變量檢查，不是 E1 的證據；ko 的非真空證據在 §4。

## 4. 實機玩家路徑（已證實）

`workplace/phase320/live-ab.sh`（轉 `workplace/phase311/run.sh`）：`buckrogers-play`（Xvfb，`--network none`），3×，zh-TW、zh-CN、ja、ko 各跑 A 與 B，另跑一次 B 的 `-lang en` 作對照。

- 九次重播的 `memory_sha256`（`fe5f8f9faf1ae7aa…`）與 `cpu_sha256`（`75e8fe4f03549be4…`）全部相同，也與規格 051、053 的實機重播相同：E1 不影響遊戲狀態，作答被接受。
- 逐格比較（`pngdiff.py`，570 格）：zh-TW 的 A、B **570 格逐位元組相同**；zh-CN、ja、ko 各有 93 格不同，都在第 3,060 至 3,980 格（手冊頁），**矩形外有差異的格 0**；每種語言的差異格數大於 0（第一格與最後一格的差異像素：zh-CN 3,322、ja 13,026、ko 1,630），所以實機對三種語言都非真空。
- 離頁：作答後第 3,990 格，B 的手冊矩形與 `-lang en` 的畫格逐位元組相同（zh-TW、zh-CN、ja、ko 皆然），之後 A、B 逐格相同（差異格止於 3,980），無殘字。
- 該路徑顯示的題（`manual.page23.scots_alarm.word4`，以規格 053 的畫格遮罩比對確認，`buckrogers-play` 不輸出題 key）四種語言都屬「E1 與固定格不同」。

## 5. 詞界樣本（已證實，畫面僅本機檢視）

依固定格換列把「不同」的段落分成三類（拉丁識別字被拆開、括號專名被拆開、行首是終端標點或右括號），三種語言各類都至少找到一段；對照圖（固定格在上、E1 在下）本機檢視了 ko 兩張、ja 一張、zh-CN 一張：

- ko：固定格把識別字與括號專名拆在兩列、列首出現逗號；E1 整組移到下一列，標點留在前一個 token。
- ja：固定格把括號專名斷在括號處，人名與縮寫被拆開；E1 整組移到下一列。
- zh-CN：固定格把句號單獨留在一列；E1 讓它跟著前一個字，括號專名以窄括號整組換行（與 zh-TW 的 E1 相同）。

四張都沒有溢出矩形；逐段繪製的缺字計數全部為 0（§2）。其餘類別與語言的組合只由逐段繪製的像素檢查涵蓋，沒有逐張檢視。

## 6. 邊界與未知

- 實機只涵蓋一題（進入、作答、清除、返回）；存讀檔後不殘字與捲動未做。其餘手冊題由載入層預檢 39／39 與逐段 `Apply`／`Draw`（缺字 0、矩形外 0）涵蓋，沒有逐題實機。
- 差異成因（ko 的列首列尾空白歸零、ja 與 zh 的行首禁則）是啟發式分類，未逐項消融驗證：**推論**。
- 日後譯文改變使某語言某段 E1 超過 14 列時，該語言的 E1 整體關閉（`off(preflight:M)`），不影響其他通道；單元測試與 phase-320-e1-sets.tsv 會列出列數。
- 識別字後接斜線（`RAM/` 型態）在 ja、ko 譯文中出現會使該語言預檢失敗；現行 catalog 沒有（規格 055 §6）。
- 診斷輸出現在最多有四處 `manual-e1=`（zh-TW 一處、其他通道各一處），以字串取單一值的腳本要逐區塊解析。
- 發行包尚未重發。

## 7. 已改與未做

- 已改：dosgolem（`manual_e1_plan.go`、`manual_e1_live.go`、`live_lane.go`、`live_runtime.go` 與四個測試檔）；Buck 規格 055 READY 並標記驗收範圍；規格 053 被取代的條文標註、規格 051、005 加 pointer。
- 未做：發行包重發（zh 字形、ja／ko 手冊段落、E1 擴及三種語言、模式事件、助詞與句中玩家名都等下次發行）；ja、ko 母語者校對（#41）。
