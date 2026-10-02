# 第三百一十七階段：手冊 E1 接入玩家路徑（規格 053，Issue #21）

日期：2026-10-02
狀態：規格 053 READY 並實作驗收；dosgolem `48ca958`（實作）、`c695eb4`（測試補齊）。發行包尚未重發（見 §7）。
推論等級：**已證實**＝重跑並比對輸出；**未知**＝未量。
手冊題畫面不入 Git，也不描述其內容；畫格只在 ignored 的 `workplace/phase317/`、`workplace/phase311/runs/p317-*`。本機英文關鍵字列的內容與計數不記錄。

## 1. 輸入（已證實）

| 項目 | 值 |
|---|---|
| A（實作的父 commit） | dosgolem `e992599`，乾淨匯出（`git archive`）；runner `0624e887c33936b2…`、`buckrogers-play` `4748b2197a6e336b…`（前 16 碼） |
| B（實作 commit） | dosgolem `48ca958`，乾淨匯出；runner `85cc80973d1a6fb7…`、`buckrogers-play` `d4b644f851f44cb5…` |
| 字型與譯文 | 發行字型 `workplace/pkg-stage/AppDir/font/`（zh-TW `buckrogers-unifont.golemfnt` SHA-256 `7675cf4e…`）、Buck `8d4f9a7` 之後的 `text/`（同一份給 A、B） |
| 離線快照 | `workplace/probe/phase12-before-question.state`，停在步數 266,650,000，不送按鍵，runner **不傳** `-manual-english` |
| 實機腳本 | `workplace/phase311/path-repair.txt`（冷開機、進入手冊查詢題、正確作答、返回救世站），5,700 格，zh-TW 3×，`-frame-every 10` |

建置腳本 `workplace/phase317/build-ab.sh`（Docker、`--network none`、`GOPROXY=off`）。

## 2. 單元與套件測試（已證實）

- `manual_e1_live_test.go` 11 個測試（合成 catalog 與字型 7 個，正式 catalog 4 個）全過：啟用矩陣（只有 zh-TW 3× 的 `e1Base` 非 nil）、跨列英文詞 E1 與固定格不同、預檢失敗保留固定格（固定格 13 列、E1 15 列的 fixture）、
  關鍵字列並存與 k' > k 時整體關閉、runtime 退路（注入尺寸不符的 `e1Base`；非 E1 原因的失敗只計一次 reset）、`SetStyle` 後 `Clear` 成功、derived 未命名時預檢失敗、compose 對 `Draw` 回 nil 不 panic 且 `skips["manual"]` 加一、
  2×／3× 交替位元組。
- 正式 catalog 預檢：39／39 段成功；E1 列數 k' 與固定格 k：38 段相等、1 段較少、0 段較多，所以關鍵字列並存條件成立。
- 2×／3× 交替（模擬 F2，正式 catalog）：39 段中 E1 與固定格相同 15、不同 24；2× 位元組在 E1 開關下 39／39 不變；3× 的差異像素都在手冊清底矩形（x21 y216 w915 h336）內。
- 乾淨匯出（B，不含未入版控檔）設 `BUCKROGERS_CHT_ROOT` 與 `BUCK_OWNER_PROJECT`：`go vet` 通過；`apps/buckrogers` 401 項 PASS、0 FAIL、19 SKIP（`TestPackagedLanes` 因缺 `BUCKROGERS_PKG_ROOT` 而 SKIP，由 `package.sh` 執行）。
- `tools/package.sh linux` 通過；`TestPackagedLanes` 新增斷言 zh-TW 的 `DebugSummary` 含 ` manual-e1=on`，且其他語言通道的手冊 presenter 的 `e1Base` 為 nil。

## 3. 離線同狀態重播（已證實）

`workplace/phase317/offline.sh`（`cases.sh`、`compare-ab.py`）：zh-TW、ja、ko、zh-CN、en × 2×、3×，A、B 各跑。

| 檢查 | 結果 |
|---|---|
| `memory_sha256` `7900785e…`、`cpu_sha256` `425cf745…`、indexed、palette、停止步數（A、B、五種語言） | 全部相同 |
| 2× 五種語言、3× 的 ja、ko、zh-CN、en 的 live RGBA | A、B 位元組相同 |
| 3× zh-TW | 9,384 個像素不同，bbox (49,217)–(897,286)，在手冊清底矩形內；矩形外零差 |

## 4. 實機玩家路徑（已證實）

`workplace/phase317/live-ab.sh`（轉 `workplace/phase311/run.sh`）：`buckrogers-play`（Xvfb，`--network none`），zh-TW 3×，A、B 各兩組：不帶摘錄、帶同一份本機摘錄（唯讀掛載，`-manual-english`）。

- 四組的 `memory_sha256`（`fe5f8f9faf1ae7aa…`）與 `cpu_sha256`（`75e8fe4f03549be4…`）相同，也與規格 051 實機重播（phase-316 §5）的值相同：E1 與關鍵字列都不影響遊戲狀態，作答被接受。
- B 的 `DebugSummary`：不帶摘錄 `manual-e1=on`；帶摘錄 `英文列=on(35) manual-e1=on`（E1 與關鍵字列並存）；A 沒有 `manual-e1` 欄位。
- 逐格比較（`pngdiff.py`，570 格）：A、B 有差異的格都在第 3,060 至 3,980 格（手冊頁），共 93 格，**矩形外有差異的格 0**；不帶摘錄與帶摘錄結果相同。第 3,990 格之後（作答後清除與轉場）A、B 逐格位元組相同。
- 離頁：作答後第 3,990 格，B 的手冊矩形與原版英文通道（`-lang en` 的實機錄影，phase-316）逐位元組相同（不帶摘錄、帶摘錄皆然），無殘字。
- 帶摘錄時 B 的關鍵字列在段落之下、不與段落重疊（畫格僅本機檢視）。
- 詞界樣本：離線首題時點與實機作答時點是兩段不同的手冊段落，兩者 E1 都與固定格不同；E1 畫面中保留的英文專名（括號專名、列尾專名）整詞移到下一列，沒有拆開（僅本機檢視）。

## 5. 與規格 053 驗收項的對照

| 驗收 | 結果 |
|---|---|
| §5.1 單元測試 | 完成（§2）。「39 段中 E1 與固定格不同的 key 集合」只以計數記錄（15／24），沒有把 key 清單寫進文件 |
| §5.2 離線同狀態 | 完成（§3）。receipt 已加入 `live_manual_visible_key`（只放 event key，B 的五種語言收據都有）；本次取樣的時點屬於「E1 與固定格不同」的集合（3× 差異像素 9,384 證明） |
| §5.3 實機 | 完成（§4） |
| §5.4 詞界樣本 | 完成（兩段不同段落） |
| §5.5 打包 | `package.sh linux` 通過，`TestPackagedLanes` 斷言 `manual-e1=on` |
| §5.6 文件 | 規格 005、034 加 pointer；本文；CONTEXT、WORKLOG |

## 6. 邊界與未知

- 只有 zh-TW 的 3×；zh-CN、ja、ko 的 E1 另開 Issue（ja、ko 的容量要依整詞換行重算，規格 051 的 13 列上限是固定格的算法）。
- 實機驗證是 `buckrogers-play` 在 Xvfb 內以腳本輸入跑一題手冊題，不是人手操作的視窗；其餘手冊題以載入層的 39／39 預檢與逐段 `Draw` 涵蓋，沒有逐題實機。
- 完整版的倚天字型由打包依現行譯文重建，本次沒有重打完整版；預檢是載入時的唯一閘門（本機倚天字型 39／39 已由審查探針驗過）。
- 日後譯文改變使某題 E1 列數大於固定格時，完整版的 E1 會整體關閉（`manual-e1=off(keyword:N)`）；單元測試每次列出 (k, k')。
- 不涵蓋 F2 在實機視窗內即時切換（單元測試以 `Compose(2)`／`Compose(3)` 交替模擬）。

## 7. 已改與未做

- 已改：dosgolem（`manual_e1_live.go`、`live_lane.go`、`live_runtime.go`、`manual_english.go`、`packaged_lanes_test.go`、`manual_e1_live_test.go`、text-receipt 的 `live_manual_visible_key`）；Buck 規格 053 READY 並標記驗收範圍。
- 未做：發行包尚未重發（zh 字形、ja／ko 手冊段落與本項都等下次發行）。
