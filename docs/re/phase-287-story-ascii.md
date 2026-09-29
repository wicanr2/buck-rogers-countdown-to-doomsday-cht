# 第二百八十七階段：劇情逐頁家族改用原版英數字形（規格 031 §3.4）

日期：2026-09-29
狀態：定稿（主代理審閱，2026-09-29）；實作 dosgolem `2f67d69`
規格：031 §3.4（READY，commit 35dfb93）、§5 第 4 條。證據前提：phase-285 §4。

## 1. 實作範圍

| 檔案（dosgolem fork，分支 buck-rogers-cht-output-overlay，HEAD dd04345 之上的工作樹） | 內容 |
|---|---|
| `apps/buckrogers/story_font.go`（新） | 開場、第 2–9 頁 presenter 的 `SetFont(base)`：以同一建構子重跑倍率規則與缺字驗證（3× 22×22 衍生與名稱沿用；第 4 頁不衍生），全部通過才更新 presenter 字型與 layer 內既有 stamp 的 `Font`；失敗保留原字型 |
| `apps/buckrogers/live_story.go` | `storyFamily` 介面加 `setFont`；九個 family 實作（第 9 頁只對 `owner[i].Presenter`） |
| `apps/buckrogers/live_runtime.go` | `findOriginalASCII(v, story)`：搜尋條件擴為「通用家族有內容，或劇情 `needsApply()`」；劇情 apply 迴圈抽成 `applyStories`，迴圈前觸發搜尋；取得成功時通用家族照 §3.1 重建、劇情家族換字型；新增 `asciiStep`，`DebugSummary` 加 `orig-ascii-step=`（SetFont 失敗時另記 `orig-ascii-story-errs=`，不計入重設） |
| `apps/buckrogers/original_ascii.go` | 匯出 `OrigASCIIScanLimit` 供 runner 使用同一搜尋範圍 |
| `apps/buckrogers/story_font_test.go`（新） | §5.4 單元測試（合成字型與合成字形表） |
| `cmd/buckrogers-text-receipt/story_ascii.go`（新）、`main.go` | legacy 劇情路徑：劇情 apply 判斷前用 `buckrogers.FindOriginalASCII` 搜尋、自己的回掃計數與 60 格節流；各頁以自己的底字型 `OriginalASCIIFont` 後 `SetFont`（第 9 頁 `storyPage9Presenter` 即 `storyPage9Owner.Presenter`）；失敗不 fail；receipt 新增 `story_orig_ascii{found,searches,step,presenters,set_font_errors}` |

通用層（`xlate/` 等）未改。

## 2. 驗收結果

| 項目 | 狀態 | 差異位置 | 收據檔 | 推論等級 |
|---|---|---|---|---|
| §5.4 單元測試（取得前原字型；SetFont 後 layer 指標、stamp 數、generation 不變且 Draw 等同新字型 presenter；第 9 頁只換 Presenter；通用路徑取得時劇情換字型；劇情 needsApply 觸發且先於 apply；取得失敗沿用原字型、不中止、不增加重設、60 格節流） | 通過 | — | `test-all.txt`（`apps/buckrogers`、`cmd/buckrogers-text-receipt` ok） | 已證實 |
| 全套 `go test ./...` | 通過（除既有 cgo 環境問題 `cmd/buckrogers-play`、`frontend/ebiten` build failed；二者以 `GOOS=windows CGO_ENABLED=0` 交叉編譯型別檢查通過） | — | `test-all.txt` | 已證實 |
| 第 1 頁 A/B 2×（phase96＋opening 按鍵，281M） | 通過 | rows 17、21 的 15 個 ASCII 格，1,195 px；中文格逐位元組相同 | `check/p1-281m-2.json` | 已證實 |
| 第 1 頁 A/B 3× | 通過（字形與 2× 新結果逐點相同、偏移 (4,4)） | 同上 | `check/p1-281m-3.json` | 已證實 |
| 第 2 頁 A/B 2×／3×（phase104，290M） | 通過 | row 17 的 `NEO` 3 格，283 px | `check/p2-290m-{2,3}.json` | 已證實 |
| 第 6 頁 A/B 2×／3×（phase104，330M） | 通過 | rows 19、21 的 20 格，1,546 px | `check/p6-330m-{2,3}.json` | 已證實 |
| 第 6 頁 A/B 2×／3×（phase123 page5.state，321M Enter，330M） | 通過 | 同上 | `check/p6alt-330m-{2,3}.json` | 已證實 |
| 反向對照第 3、4、5、7、8、9 頁 2×／3×（300M…360M） | 通過：runner 該頁覆繪與 live RGBA 新舊逐位元組相同 | 無 | `check/p{3,4,5,7,8,9}-*.json` | 已證實 |
| receipt active 欄 | 通過：每個停止點新舊 runner 都只有預期頁 `active_keys` 非空，零缺字 | — | `ab/*.json` | 已證實 |
| 取得收據 | 通過：新 runner `story_orig_ascii.found=true, searches=1, presenters=9`；live `orig-ascii=true/1 orig-ascii-step=…`；`resets=map[]` | — | `ab/*-new-*.json`、`ab/*-new-*.log` | 已證實 |
| phase254 七腳本 rerun28 | 通過：七份 `rerun28-*.txt` 與 rerun27 逐字相同（SAME／DIFF 狀態不變） | — | `phase254-live-families-parity/rerun28-*.txt` | 已證實 |
| phase254 RGBA | 504 份中只有 `o280900000-{2,3}` 的 expect／live／opening 六份不同；其餘（含 story 三點、另五個腳本的 52 份 live 中 50 份）逐位元組相同 | opening 280.9M | `phase254-live-families-parity/rerun28/` | 已證實 |
| phase254 opening 遮罩 | 通過：三點 2×／3× 新遮罩與 rerun27 遮罩完全相同（2× 87 px、3× 1,043 px），超出「舊遮罩∪ASCII 格」0 px | — | `p254-mask.json`、`p254-baseline-rerun27/` | 已證實 |
| phase254 opening 280.9M 新舊 live | 差異 1,195 px，全在可見 ASCII 格，**但分布於 rows 17 與 21**（見 §4 待決） | rows 17、21 | `p254-mask.json` | 已證實 |
| phase254 opening 275M、282M 新舊 live | 逐位元組相同 | — | 同上 | 已證實 |

## 3. 取得時點

| 路徑 | runner（劇情觸發） | live |
|---|---|---|
| p1（phase96，281M） | step 275,652,511 | step 267,025,069（通用家族 ECL 先有內容，§3.1 路徑） |
| p2–p9（phase104） | step 287,243,280 | step 287,243,280（與 runner 同 step；強推論為劇情觸發） |
| p6alt（phase123） | step 329,839,410 | step 329,839,410 |

所有路徑搜尋 1 次即取得；沒有出現節流期間先以原字型畫出的情況。

## 4. 2× oracle 分配（逐字）

baseline oracle：翻譯中長度 ≥2 的英數連續段，在同一 baseline 畫面 rows 17–22 找到遮罩逐點相同的連續格，視為原版英文同字元格。
backup oracle：`p287check` 自行以 CRC-32＋SHA-256 從同狀態終態記憶體找出字形表，依 §2 索引放大 2 倍比對（不呼叫 `OriginalASCIIFont`；字形只在記憶體中）。所有字元另外也通過 backup 比對。

| 頁（停止點） | 字元（row,col） | oracle |
|---|---|---|
| 第 1 頁（281M） | `(`(17,8)、`)`(17,20) | backup |
| 第 1 頁 | `BUCK`(17,9–12)、`ROGERS`(17,14–19) | baseline（baseline 格 (33–36,17)、(1–6,18)） |
| 第 1 頁 | `RAM`(21,8–10) | baseline（(11–13,20)） |
| 第 2 頁（290M） | `NEO`(17,8–10) | baseline（(18–20,17)） |
| 第 6 頁（330M，兩條路徑相同） | `(`(19,7)、`)`(19,24) | backup |
| 第 6 頁 | `CARLTON`(19,8–14)、`TURABIAN`(19,16–23) | baseline（(1–7,19)、(9–16,19)） |
| 第 6 頁 | `NEO`(21,9–11) | baseline（(33–35,21)） |

3× 沒有 baseline oracle（原版英文是 3× 整數放大，字寬不同，§3.2 已接受）；3× 以 backup（16×16 置於 24×24 偏移 (4,4)）與同點 2× 新結果逐點交叉比對。

## 5. 截圖（2×，覆繪後）

`shots/page1-281m-2x-{old,new}.png`、`shots/page6-330m-2x-{old,new}.png`。

## 6. 未量到／限制

- 前端 `buckrogers-play`（ebiten）未實跑：本機 cgo 建置為既有環境問題，只做交叉編譯型別檢查。host presenter 經 `PresentationLayer()` 每幀複製 stamp，stamp 的 `Font` 已就地更新，屬強推論。
- phase254 story.sh 三個點（281.1M／281.5M／282.5M）沒有任何劇情頁 active，新舊相同只證明沒有副作用；第 2–9 頁的正向覆蓋由本輪 §5.4 A/B 提供。
- 取得失敗路徑只由單元測試覆蓋；實跑三條路徑都在第一次搜尋取得。
- 同一頁在節流期間先以原字型畫出、取得後換字的畫面轉換，未在實跑中出現，未量。

## 7. 待決

- 規格 031 §5.4 寫「opening 在 280.9M 的新舊 live 差異只在第 17 列可見 ASCII 格」。實測差異在 rows 17 與 21：第 1 頁第 5 行（row 21）譯文含 `RAM`，§3.4 本身也列出第 1 頁含 `RAM`。差異全在可見 ASCII 格，但與「只在第 17 列」字面不符；規格未改，請主代理決定是否修訂該句。
- 規格寫以 rerun26 為遮罩基準；本輪用最新的 rerun27（phase-286：rerun27 七份結果與 rerun26 逐字相同、52 份 live 逐位元組相同），基準副本存於 `p254-baseline-rerun27/`。
- `current-font` 在 rerun27（14:07）之後重建（14:23）。rerun28 除 opening 280.9M 外全部與 rerun27 逐位元組相同，故字型重建對這些輸出沒有影響。
- 既有行為（非本輪引入）：通用家族發生 reset 時以 `r.font` 重建 presenter，會回到倚天 ASCII（§3.1 範圍）。劇情家族出錯只 `clear()` 不重建，字型不受影響。

## 8. 檔案

`go.sh`、`sync.sh`（同步到 dosgolem-clean）、`ab.sh`／`ab-jobs.sh`／`ab-inner.sh`／`flags.sh`（A/B）、`check.sh`／`check-inner.sh`、
`p287check`（驗收工具；原始碼 `p287check-src/`，建置位置 `dosgolem-clean/workplace/p287check/`）、`p254.sh`（rerun28）、`p254-mask.py`。
runner：`runner-old`（= phase254 原 runner，SHA-256 前綴 `f432baa615809705`）、`runner-new`（`8233762fe18ec2c6`）；
phase254 原 runner 備份為 `runner-rerun27`，`runner` 已換成 `runner-new`。A/B 用的終態 state（含原版記憶體）驗收後已刪除，可用 `ab.sh` 重生。
