# 第三百一十六階段：日文與韓文的手冊段落（規格 051，Issue #39）

日期：2026-10-02
狀態：規格 051 READY 並實作驗收；`text/manual.ja.tsv`、`text/manual.ko.tsv` 各 39 列。發行包尚未重發（見 §7）。
推論等級：**已證實**＝重跑並比對輸出；**未知**＝未量。
手冊題畫面不入 Git，也不描述其內容；本文只記雜湊、計數與判定。畫格只在 ignored 的 `workplace/phase316/`、`workplace/phase311/runs/p316-*`。

## 1. 輸入與工具版本（已證實）

| 項目 | 值 |
|---|---|
| Buck 工作樹 | `8d4f9a7`（規格 051 READY 與工具、資料） |
| dosgolem | 分支 `buck-rogers-cht-output-overlay` `503b79a`（執行期），`e992599`（只改 `ko_test.go`） |
| `text/manual.ja.tsv` SHA-256 | `b9a81a854b10ecc84c92973fbf66f10dfe6348af3e330d2c02dac844396a3e6a` |
| `text/manual.ko.tsv` SHA-256 | `8d04c8679639190aa95a4dfc8eb6440573c453872527ae5928bafe67b71eae5d` |
| 發行字型 ja／ko（`package.sh linux` 重建） | `87ea61ba7898e941…`／`aa271de20cb5ed2d…`（前 16 碼） |
| 離線 runner（`cmd/buckrogers-text-receipt`） | `5333bdd352df7328…`（前 16 碼） |
| 實機 `buckrogers-play` | `workplace/phase312/bin/buckrogers-play`，`c6924c7b84c459ac…`（前 16 碼） |

譯文由 zh-TW 段落轉譯（批次子代理翻譯，詞表為各語言的 `glossary`），英文原文不在輸入內。

## 2. 資料層（已證實）

- `tools/manual_lang.py check`：ja、ko 各 39 段通過。單位數（半形 1、其餘 2）平均 ja 353、ko 349，最大 ja 891、ko 886（各一段，逐字元換列後 13 列，其餘不超過 12 列）。
  zh-TW 最大 661 單位、10 列。全部在規格 051 §3.4 的安全上限內（13 列、960 單位）。
- 拉丁字母詞都是同列 zh-TW 的子集；數字多重集合與 zh-TW 同列相同；字集在 `charset.<lang>.txt` 內；ko 的標點除「」『』外只用 ASCII；ja 日文與拉丁字母之間無空白。
- 人物一致性：`name_glossary.py lint` 要求 zh-TW 該列有的人物譯文也要有。zh-TW 印刷本保留英文 `Scot.dos`，ja、ko 依詞表寫成片假名、諺文。
- 本機洩漏核對（對 ignored 的英文關鍵字摘錄實跑，一次性腳本，不入版控）：答案詞出現在譯文拉丁字母詞中的列數，ja、ko 與 zh-TW 三者相同（沒有比已公開的 zh-TW 多）。數字與詞都不記錄。
- `ja_check.sh`、`ko_check.sh`、`zh_cn_check.sh` 全部通過；`unittest` 71 項通過；期望值 5,453 列、5,445 個不同 key。
- `font/characters.ja.txt` 增 26 字、`font/characters.ko.txt` 增 3 字（由正式譯文重新產生）。

## 3. 載入層（已證實）

- `tools/package.sh linux`（含前置檢查與 `TestPackagedLanes`，要求 PASS 且無 SKIP）通過。`TestPackagedLanes` 斷言 `len(r.off)==0`，
  而通道建立（`live_lane.go`）對 `liveScales` 的每個倍率各建一個手冊 presenter，所以 2×、3× 的 `validateManualCatalogFont` 都已通過。
- 暫時的 Go 測試（`workplace/phase316/zz_p316_manual_render_test.go.txt`，未入版控）：真實 catalog、發行字型、真實版面，逐段在 2×、3× 畫出 ja、ko、zh-TW 各 39 段，
  沒有缺字、都畫出；逐字元換列最多 ja、ko 13 列（zh-TW 10 列）。最長一段的 ja 3×、ko 2× 畫格檢視：無裁切，段落停在版面內，Latin 專名（如全大寫的名稱）會在列尾被逐字元截斷換列（與 zh-TW 相同的既有行為）。
- dosgolem `apps/buckrogers` 套件測試：除了兩個未入版控的探針測試（`command_status_*_probe_test.go`）外全過。
  ko 名字比對測試 `TestKoNameMatchesAgreeWithZhTW` 原本把 `manual.ko.tsv` 的 3 列誤報「多人物 scot」（Go `Matches` 只認中文譯名，zh-TW 手冊列保留英文），
  改為排除手冊家族（commit `e992599`，比對列數仍為 5,414）。

## 4. 離線同狀態重播（已證實）

快照 `phase12-before-question.state`，停在步數 266,650,000（規格 040 的「手冊題」時點，不送按鍵），`workplace/phase316/run.sh`（`cases.sh`、`compare.py`）：
zh-TW、ja、ko、zh-CN、en 各跑 2×、3×，使用 `pkg-stage` 的發行字型與目前 `text/`。

| 檢查 | 2× | 3× |
|---|---|---|
| 記憶體雜湊 `7900785e700f2b88…`、CPU 雜湊 `425cf74500106e4b…`（五種語言相同） | 通過 | 通過 |
| indexed、palette、停止步數相同 | 通過 | 通過 |
| `-lang en` 的畫面等於原版 baseline | 通過 | 通過 |
| zh-TW、ja、ko、zh-CN 都畫出覆繪（不等於 baseline） | 通過 | 通過 |
| 四種覆繪語言的畫面互不相同 | 通過 | 通過 |
| 停止時的語言通道等於要求的語言 | 通過 | 通過 |

記憶體、CPU 雜湊與 `phase-301-ja.md` 手冊題時點的前綴（`7900785e`、`425cf745`）相同；當時 ja 的畫面等於 baseline（無段落），現在 ja、ko 畫出段落。

## 5. 實機重播（已證實）

`workplace/phase316/live.sh`、`live-en.sh`（轉 `workplace/phase311/run.sh`）：同一腳本 `path-repair.txt`（冷開機、進入手冊查詢題、正確作答、返回救世站），
第 5,700 格，`-frame-every 10`；zh-TW、ja、ko、en 各 2×、3×，共 8 次。

- 八次（含 en）的 `memory_sha256`（`fe5f8f9faf1ae7aab182ad81…`）與 `cpu_sha256`（`75e8fe4f03549be478178d66…`）完整 64 碼相同：語言與倍率不影響遊戲狀態，作答被接受，流程相同。
- 手冊頁（約第 3,100 至 3,980 格）：ja、ko 在 2×、3× 畫出完整段落、無裁切；頁面上方的題頭三行是原版英文（與 zh-TW 相同）。
- 離頁：作答後第 3,990 格，手冊矩形（邏輯座標 x7 y72 w305 h112）的像素在 zh-TW、ja、ko 與 en 逐位元相同（2×、3× 各自），
  第 3,970、3,980 格則 ja、ko、zh-TW 三者互不相同且不同於 en（覆繪存在）。之後轉場到救世站；ja、ko 各 2×、3× 四組的第 3,940 至 4,060 格接觸表（每 10 格）檢視，無殘字。
  救世站畫面的矩形因名單等本語言文字而不同，不能用來比殘字，所以以第 3,990 格為準。

## 6. 邊界與未知

- 母語者校對：未做。譯文是機器輔助，README、`讀我.txt` 已寫明。
- 韓文、日文拉丁字母詞在列尾被逐字元截斷換列：與 zh-TW 相同的既有版面行為，規格 051 §6 的風險，未做詞級換行。
- 只實機走過一題的手冊題路徑；其餘手冊題（39 題中的其他題）以載入層與逐段畫出（§3）涵蓋，未逐題實機。**未知**：其他題在實機上的離頁。
- 本機英文關鍵字列（規格 034）在 ja、ko 的行為不在本規格範圍，未驗。
- 規格 042 §3.9 所說「手冊題提示句為日文（引擎片段）」指哪一行字，本階段沒有重新量測（畫面上方題頭三行在所有語言都是原版英文）；`讀我.txt` 該句沿用舊敘述。
- 規格 042 §3.9 所說「手冊題提示句為日文（引擎片段）」指哪一行字，本階段沒有重新量測（畫面上方題頭三行在所有語言都是原版英文）；`讀我.txt` 該句沿用舊敘述。

## 7. 已改與未做

- 已改：`README.md`、`docs/release/讀我.txt` 中「手冊題的段落顯示原版英文」改為現況；`CONTEXT.md`、`WORKLOG.md`；規格 042、043 §3.9 加指向 051 的 pointer。
- 未做：已發行的 v1.1.0 發行包仍是舊狀態（ja、ko 手冊段落為原版英文）；zh 字型（規格 050）與本項都等下次發行才帶出，是否重發由使用者決定。
