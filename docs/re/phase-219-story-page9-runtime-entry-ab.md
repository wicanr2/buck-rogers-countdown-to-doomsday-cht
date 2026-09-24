# 第二百一十九階段：第九頁固定單行正式入頁 A/B

日期：2026-09-24
狀態：**固定入頁及後續 Ctrl+C 退出 DOS 的 Stop 清層均取得正式同狀態收據；僅此範圍限縮 CONFORMED，遊戲內自然離頁未量。**

## 固定輸入與範圍

本次只從合法第八頁存態 `page8-a.state`（SHA-256
`327dc1cb8baf4bee71cdcd0173538af123c47266c8bbf556b28f38d89355b0a9`）
於 machine step `351000000` 排入同一個 Enter，前進至 `352100000`。
原版 `GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
本機字型 GOLEMFNT SHA-256 為
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
位址與畫面矩形依[規格 022](../spec/022-story-page9-overlay-draft.md)；本次沒有
修改原版 EXE、規則、輸入、記憶體、存檔或防拷判定。原版、字型、
`.state`、RGBA、PNG 與完整 JSON 都留在 ignored `workplace/`。

正式接線新增 `apps/buckrogers/story_page9*.go` 的固定 READY catalog、
逐字 watcher、RGBA presenter 及 owner，並在
`cmd/buckrogers-text-receipt/main.go` 接入明示旗標。原版 20 字照常繪製；
只有第 20 個 guarded return、原文 SHA 與每格 64 筆合法 A000 pre-write
全通過，才啟用 `story.page9.line.001`。active 後第一筆相交的原版 A000
pre-write（包含同值）先清層；Stop／Restore／discontinuity 亦清層。
譯文僅供輸出，未送入原版 DOS 語意路徑。

## 獨立重播結果

以 Go 1.26.7、既有 `golang:1.26.7-bookworm` 與
`eob-remake-go:1.26.7-ebiten2.9.9` 映像，在限資源、無網路、唯讀
Docker 重跑 `StoryPage9` Go 負例、CLI 回歸與 `go vet`，均通過。
三份私有存態在正確掛入既有 `/orig` 唯讀原版目錄後，
`TestStoryPage9PrivateSameState` 讀回的完整 `machine.Snapshot`
為 `reflect.DeepEqual`，DOS `SaveState` bytes 相同；原始 gzip/gob
`.state` 檔 SHA 本身不穩定，連 control 自重播也不同，不拿它冒充
同狀態判準。第一次主代理重跑缺 `/orig/GAME.OVR` 掛載而在讀入前失敗，
補上唯讀掛載後同一比較通過；這是驗證容器設定錯誤，非產品失敗。

| 固定端點 | control | 繁中 2× | 繁中 3× |
| --- | --- | --- | --- |
| `indexed_sha256` | `fb65f3b36e019caa8d0e74d72aa71ab9908b76ec03fc1f5c301ca563473647b0` | 相同 | 相同 |
| 正規化 JSON（移除 `story_page9_overlay`） | 基線 | 完全相同 | 完全相同 |
| active key | 無 | 1 筆 | 1 筆 |
| RGBA 差異像素 | 不適用 | 矩形內 1,253、外 0 | 矩形內 2,615、外 0 |
| 缺字 | 不適用 | 0 | 0 |

正規化 JSON 亦包含相同的 `memory_sha256`、palette、排入 Enter、
FileOps tracking 零筆及檔案寫入零筆。主代理在唯讀 Docker 重跑
`workplace/page9-runtime/verify_final.py`，逐像素重算上述差異，
並核對 baseline／overlay RGBA 的 SHA、active key、indexed
與 control metadata；皆通過。最終私有 JSON SHA-256 依
`final-control`、`final-2`、`final-3` 次序為：

- `b8964cbe42bf2d631f0fe9ea14fbd91208a2b0d4a06fd440589bde0052080546`
- `727bbe7cde3553bbd0ab5a166aa0412ffe8aeeb404d5f5b359a5feb6aa78c292`
- `87e88734292e0d8b85c6bb55161e290ed90352f31af60c0af12cc146cbf449b0`

本次本機收據 runner SHA-256：
`1aa867364323f59e5498897f9ae9426a80559085d9ceacd3d2bd6e7a3c67af1c`；
私有驗證腳本 SHA-256：
`10e8deced723ebae07800eb9aa0076a8134654993f2cbe9ed34c93cffa717936`。
兩者與素材均未加入 Git。Go 測試與私有 A/B 重跑均使用
`--rm --network none`、明示 UID/GID、記憶體／CPU／PID 限額；
原版與工作樹唯讀掛載，容器結束即清理。

## 尚未取得的收據

本次 `352100000` 停點只證固定單行**入頁本體**可顯示且
DOS 同狀態；沒有觀測自然離開第九頁時的第一筆相交寫入、
實際清層後畫面、Restore 後重新進入、完整 Linux 視窗或
正常玩家路徑。合成負例證明守門邏輯，不可替代原版出口。
因此[規格 022](../spec/022-story-page9-overlay-draft.md)仍為限縮 READY，
[Issue #20](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/20)
維持 OPEN；下一個最小實驗是找到合法第九頁的真實相交 pre-write
及返回／離頁端點，再以 control／雙倍率做相同狀態 A/B。

## 2026-09-24 自然離頁的有界負收據

為核對上述未知，改從**合法第九頁原版狀態**
`workplace/page9-next-trace/page9-a.state`（SHA-256
`563ed40ba276c6857c57b05344949dec5891e4596ad783a9fc89b805eae8c2a4`）
起跑；原版 `GAME.OVR` SHA-256 仍為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
依[第一百一十二階段](phase-112-command-turn-manual-evidence.md)掃描手冊已明示的
方向鍵，僅試數字鍵盤 8（前進，`48:38`）與 2（後退，`50:32`），
各自從同一 state 於 step `361000000` 排入**一鍵**；不疊加鍵位。
先以 `362000000` 作中途檢查，再以 `370000000` 作本輪硬停止線，
沒有繼續延長或新增候選。

工具為 ignored dosgolem fork commit
`7930b7aedf3a3234630c38652ca2e6b583e97900` 加一次性、未追蹤的
`apps/buckrogers/story_page9_exit_probe_test.go`；probe SHA-256
`bd16566c0555f3cb6301cc601c2aaef05ab4a1b5f822a71bacefcfcd317b03cb`。
以 Go 1.26.7、`golang:1.26.7-bookworm`、無網路、有界 Docker
唯讀掛載 fork、原版與 state，執行
`STORY_PAGE9_ACTIVE_STATE=/private/page9-a.state go test ./apps/buckrogers -run TestStoryPage9BoundedExitPrewriteProbe -count=2 -v`。
`/private` 對應既有 `workplace/page9-next-trace/`，`/orig` 對應唯讀原版
`workplace/original/BRcdoom/`。probe 只輸出鍵位、步數、A000 位址／writer
及矩形像素變化數，不輸出原文字節或畫面。

兩輪獨立重播的四個分支結果逐項相同：8 與 2 都在 step
`361000150` 被 BIOS 讀取一次；至硬停止 step `370000000`，
`[8,168)×[136,144)` 的**第一筆相交 A000 pre-write 均不存在**，
故事矩形終點相對起點的 indexed 差異像素為 0，DOS `Exited=false`。
因此本窗口沒有可記錄的出口 writer、原版清除像素或 watcher／owner
在真實離頁時清層的先後。這是「在指定 state、單鍵及時窗內未觀測到」
的已證實負結果；第九頁自然離頁方式及其他玩家路徑仍為**未知**。

本輪到 `370000000` 即停止 Issue #20 的鍵位探針，Issue 維持 OPEN；
下一步須先從正常玩家流程或手冊／原版來源取得**另一個適用此 command state**
的明確出口候選，再另立窄實驗。沒有實際出口，不執行出口後
control／2×／3× 無殘字驗收，也不把規格 022 的限縮 READY 升為
完整生命週期 CONFORMED。

## 2026-09-24 Ctrl+C 退出 DOS 的正式 Stop 收據

上述方向鍵負收據保留為當時的結論，不代表所有出口均不存在。
後續查得中文 Data Card `2F3_SCAN1240_008.jpg` 印刷第 12 頁記載
「Ctrl+C：跳回 DOS」；來源 SHA-256 為
`28d1c1c21b3de5b2af7cb63e79ecbe9075e08a3bca1525cd5e4398947b959ea7`，
頁碼與掃描來源詳見[第一百一十二階段](phase-112-command-turn-manual-evidence.md)。
「Ctrl+C」對應 BIOS scan／ASCII `2e:03` 是本次**受控輸入假說**，
不是手冊寫出的鍵盤 word；以下原版執行結果才證實該候選在此 state 的行為。

先從合法第九頁 `page9-a.state`（SHA 見上一節）於 step `361000000`
送單鍵 `2e:03`，原版在 `361000150` 由 INT 16h AH=00 讀取，
`361000689` 退出 DOS；期間故事矩形沒有 A000 相交 pre-write。
接著正式收據從本節開頭的合法第八頁 state 出發，
於 `351000000` 送 Enter 進第九頁，於 `361000000` 送相同 `2e:03`；
control、繁中 2×、繁中 3× 使用相同原版 `GAME.OVR`、倚天 16×16
GOLEMFNT、輸入及 `370000000` 硬上限。正式 CLI 的第九頁 owner
在 `d.Exited` 時呼叫 `Stop()`，收據另以不含字模的計數記錄清層前後：

| 同次執行核對 | control | 繁中 2× | 繁中 3× |
| --- | --- | --- | --- |
| 原版停止 step | `361000689` | 相同 | 相同 |
| 第九頁 Stop 前／後 active 層 | 無 owner | `1 → 0` | `1 → 0` |
| 終態 indexed SHA-256 | `fb65f3b36e019caa8d0e74d72aa71ab9908b76ec03fc1f5c301ca563473647b0` | 相同 | 相同 |
| 終態覆繪／baseline RGBA | 不適用 | 完全相同，無殘層 | 完全相同，無殘層 |
| 排除覆繪／Stop metadata 後 JSON | 基線 | 完全相同 | 完全相同 |

三份私有正式 JSON 的 SHA-256 依 control、2×、3× 次序為
`ba3ef95ca46fa0a62e883d8f753941c610ec3facc632be1eda1ef7160a4623b5`、
`ae4659da0a931cb2c31d527e8c8c42338f327597a40c81daad958e2488deb621`、
`de8558c6a58b99971a0f0aa87ebaf7cb4f88cb0c087c71486411bcd5ef0e16b4`。
輸入 state、原版與字型 SHA 與本節開頭相同；`2e:03` 的原版
`key_reads` caller 亦與 control 相同。收據工具採本機 dosgolem 分支
commit `99584d897cebab28929c360962413f4ea68c795a`、
Go 1.26.7，以既有 `golang:1.26.7-bookworm` 在無網路、限資源 Docker
執行；原版、state、字型唯讀掛載，畫面與完整收據只在 ignored
`workplace/page9-runtime/`。JSON 比較以 Python 3.12 容器讀取，
只排除控制組不存在的 `story_page9_overlay`、`story_page9_stop`。
重播初次比較混用了舊 control 的 `-story-pixel-trace` 與輸入旗標，
造成兩個診斷欄位不同；改以相同旗標重生 control 後完全一致，
這不是原版或覆繪差異。

這份證據支持[規格 022](../spec/022-story-page9-overlay-draft.md)只將
「固定入頁＋Ctrl+C 退出 DOS 時 Stop 清層」限縮升為 CONFORMED。
原版退出時仍保留 indexed 故事畫面，但前端作用層已撤銷；
遊戲內自然離頁、其他出口、Restore 後重入、完整 Linux 視窗與
玩家存讀檔仍未知，Issue #20 保持 OPEN。
