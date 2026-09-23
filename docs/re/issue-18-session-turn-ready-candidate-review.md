# Issue #18：Linux session-turn 限縮 READY 候選審查紀錄

日期：2026-09-24
狀態：**候選待獨立審查；沒有正式 session、原版同狀態或 CONFORMED 收據。**

## 範圍與來源

本紀錄只審查[規格 019](../spec/019-linux-frontend-session-turn-boundary-draft.md)
的單一 Update 回合，不審查 Issue #18 其餘 cold-boot preflight、第一步前
observer、多作用層、discontinuity、正常玩家路徑或存讀檔。Issue #18
仍為 OPEN，[規格 004](../spec/004-dosgolem-host-frontend-draft.md)仍是 DRAFT。

來源是本機 ignored dosgolem fork commit
`a01e34253fa59cc92c3fde1bf4b33577e318e9e7`，Go 1.26.7，
既有 image `eob-remake-go:1.26.7-ebiten2.9.9`，ID
`sha256:39d6e05c9abc60a566e376cde6afd29c24aa21c30eeec1e1fd92c8b16e62aa60`。
原型 `workplace/phase193-frontend-session-fake/` 與
`workplace/dosgolem/workplace/phase211-session-receipt-candidate/`
均被 Git 忽略。合成 COM 位址為 `PSPSeg:0100h`，不屬於《拯救地球》；
本紀錄未載原版 EXE、手冊、字型、私有存態或畫面。

## 重跑與直接觀測

先確認掛載來源都是現有目錄、輸出目錄與規格檔屬目前 UID/GID，
再以 `timeout 90s docker run --rm --network none --read-only
--memory 2g --cpus 2 --pids-limit 256 -u "$(id -u):$(id -g)"`
及可執行 `/tmp` tmpfs 執行；`GOCACHE=/tmp/go-cache`、`GOWORK=off`、
`GOPROXY=off`。`phase193` 以唯讀 `/workplace` 掛載執行
`go test -count=1 ./...`，通過；`phase211` 以唯讀 `/dosgolem`
掛載執行 `go test -count=1 ./workplace/phase211-session-receipt-candidate`，
通過。兩次皆無網路、無原版素材、無正式程式變更。

| 缺口 | 已證實 | 候選契約及仍需正式驗證 |
| --- | --- | --- |
| 同批輸入 | 正式 `frontend/ebiten/game.go` 的 `readFrameInput` 同取 pointer edges 與鍵盤清單；`Update` 按 Down→Up→焦點清理→keys 處理，已有起點開啟／面板轉移整批鍵盤閘門。phase193 fake 的 Open／Apply／Cancel＋Enter 負例重跑通過。 | 規格 019 明訂沒有跨設備實際時間順序；先做整批可失敗 route 預檢，再按固定順序提交。正式 typed batch 尚未實作，pointer／鍵盤 route 失敗的原子拒絕仍待測。 |
| 實步／停止 | `Machine.RunUntil` 以 budget 限定呼叫，但 `Machine.Step` 在錯誤返回前可增加 `Machine.Steps`；raw `StopBudget` 可伴 error 或 DOS 正常退出。phase211 合成 COM 五組測試重跑通過，含退出前置、差分、error 優先。 | 規格 019 把 Steps 定義為嘗試數，定 epoch 為接納的 Update 序號，零預算先拒絕，逐類保存 raw stop 與 error。這些語意是審查候選；正式 session receipt／原版還未驗。 |
| `Draw`／Close | 正式 `Game.Draw` 無 error 回傳；可檢查失敗只寫 `g.err`，下一次 `Update` 才拒絕。phase207 fake 六階段故障與 Close 一次的控制流程已重跑。 | 規格 019 要求同 goroutine 的同步 `ReportDrawFault(error)` 回報唯一 session owner；正式通知、真實資源 Close 與下一次零步仍須在實作後驗證。 |

可實作性核對：`host.PanelController.Route` 會改面板狀態，
`host.MouseBridge.Handle` 在已允許的畫布點擊會直接呼叫 DOS mouse；
`presentation.KeyboardBridge.DeliverBIOSKey` 會排入 BIOS queue。
因此不能把這些正式物件直接跑一遍作預檢。下一切片需新增純資料
route plan 或等價暫態，先驗整批，再以現有 bridge 提交，並測後段
失敗時沒有先送的 DOS 鍵／滑鼠動作。現有 fake 只測 host 優先閘門，
尚未驗這個正式交付原子性。

`phase193` fake 的 epoch 仍按 budget 增加；它不能證明本候選的
Update 序號語意。`phase211` 的 `AttemptOrdinal` 與 `MachineStepsAfter`
刻意分開，也沒有定 epoch。規格所選的 epoch 是 session 狀態識別，
並非由這些測試推得的原版事實；獨立審查應檢查單回合一次接納、
暫停仍增加序號、故障不增加以及收據關聯。

本次沒有把 ignored fake、合成 COM 或 `Game.Draw` 的下一回合錯誤閘門
寫成正式 cold boot 成功。下一個可實作切片是通用 typed session owner
與 `Game` 的 adapter：先落實 batch 預檢、epoch、正預算及差分收據，
再接同步 Draw fault relay 與冪等 Close；以 synthetic machine 和
無原版 fake 測試逐個驗證。只有獨立審查核准 019 的限縮子契約後，
才能改 production；004 的其他 READY 前置仍各自待補。

## 獨立審查追加：尚未通過限縮 READY（2026-09-24）

本次核對的 fork HEAD 是 `a01e34253fa59cc92c3fde1bf4b33577e318e9e7`，
工作樹乾淨。規格 004 第 274–284 行的使用者定案、規格 019 第 151–158、
217–219、243–246 行，與正式 `frontend/ebiten/game.go` 第 186–209 行的
callback 排程一致：面板開啟、面板轉移及收合同回合暫停，下一個關閉回合
才可恢復。這項既有決定及 phase194 的限縮 CONFORMED **不是阻塞點**；
phase194 量到的是 callback 排程，仍不能充作 typed session 的 machine step 收據。

本次重跑勘誤：上文「`phase193` 以唯讀 `/workplace` 掛載」若只把
`workplace/phase193-frontend-session-fake/` 掛成 `/workplace`，
`go test -count=1 ./...` 會在 setup 失敗，原因是該原型 `go.mod` 第 7 行
`replace github.com/wicanr2/dosgolem => ../dosgolem` 找不到相鄰目錄。
改將**整個專案 `workplace/`**唯讀掛成 `/workplace`，並以
`/workplace/phase193-frontend-session-fake` 為工作目錄重跑，同一測試通過。
`phase211` 在 fork 目錄唯讀掛載下重跑
`go test -count=1 ./workplace/phase211-session-receipt-candidate`，亦通過。
兩次均使用現有 `eob-remake-go:1.26.7-ebiten2.9.9`、`--rm --network none
--read-only --memory 2g --cpus 2 --pids-limit 256`、目前 UID/GID、
可執行且有界的 `/tmp` tmpfs，以及 `GOCACHE=/tmp/go-cache GOWORK=off
GOPROXY=off`。首次掛載失敗是重跑環境錯誤，不是產品測試失敗。

目前阻塞限縮 READY 的是規格 019 第 177–188 行自行列出的審查矩陣
尚未以同一 typed 回合驗到，而非已定案的面板政策：

1. `phase193` 的 `session.go` 第 138–143 行在暫停時不增加 epoch，
   在執行時卻以 budget 增加；`lifecycle_fake_test.go` 第 34–38 行
   甚至斷言暫停回合 `Epoch=0`。`phase211` 的 `session.go` 第 29–43、
   61–67 行只有嘗試序號與 machine steps，`session_test.go` 第 110–122 行
   明言沒有 Epoch。因此現有綠色測試尚未驗證候選第 235–241 行所選的
   「每個成功接納 Update（含零步）增加一次、失敗不增加、單回合只消費一次」；
   零預算拒絕與完整 `TickReceipt` 也沒有在同一 typed session 測試。
2. 正式 `game.go` 第 173–194、222–240、266–272 行仍逐事件提交。
   `host.MouseBridge.Handle` 第 179–180、209–220 行可即時送 DOS mouse，
   `presentation.KeyboardBridge.DeliverBIOSKey` 第 74–85 行可即時排 BIOS key，
   而 `host.PanelController.Route` 第 72–110 行會改 host 狀態。
   現有 fake 只用 `DOSInputs` 計數，未測「先成功分類／提交一個
   pointer 或鍵，後段 route 失敗」時 DOS 零副作用。候選第 224–231 行
   已正確要求純資料 route plan 與提交前預檢，但尚無整批原子拒絕收據；
   也需固定提交階段的可失敗邊界，才能判斷是否真的不會部分送入。

另有正式接線後的驗收界線：`phase193/lifecycle_fake.go` 第 68–70、
103–108 行的 fake `Draw` 可以回 error；正式 `Game.Draw` 第 292–306 行
只設 `g.err`。現有測試可證抽象故障階段與 Close 計數，未驗候選
第 275–289 行要求的同步 `ReportDrawFault`、下一次 Update 零步、真實
資源只關一次及關閉錯誤保留。候選已明定正式接線須測這些行為；
這是實作後驗收條件，不能把 fake 當成已驗實作。

`Machine.RunUntil` 的原始停止碼與計數依據成立：fork
`internal/machine/probe.go` 第 125–142 行在 Step error 時也回
`StopBudget`；`internal/machine/machine.go` 第 1155–1167 行先增加
`Machine.Steps` 再可能回 error。`phase211` 的合成 COM 測試確實驗到
退出前置檢查、嘗試差分、error 優先及 predicate／breakpoint 區分。
這支持候選的判讀方向，但不填補上述整回合的缺口。本次結論是
**維持 READY 候選、不得升 READY 或據以修改 production**；補齊同一
typed session 的負例與正式接線證據後再獨立審查。原版素材未參與測試，
沒有新增可散布語料。

## READY 前可丟棄補證：fake 回合與純資料 route plan（2026-09-24）

延續上節阻塞，在 Git 忽略的 `workplace/phase193-frontend-session-fake/`
修改 fake；正式 dosgolem fork、規格 019 狀態與原版輸入均未更動。
此段是較新的補證，保留上節作為當時的獨立審查基線。

`Session.Deliver` 現在先對 host 轉移、pointer 候選、固定的合成 layout
token、焦點清理與鍵盤候選建立純資料 plan；所有候選驗完，才提交 host
轉移與 fake BIOS／mouse 計數。此 plan 不呼叫 `MouseBridge.Handle`、
`KeyboardBridge.DeliverBIOSKey` 或 `PanelController.Route` 作預檢。
成功接納的 batch 才增加 epoch 一次並建立待消費回合；暫停回合即使
budget 為零仍回 `Steps=0`，下一個關閉回合用明示正預算；未經
`Deliver`、重複 `Advance`、上回合未完成先 `Deliver` 均轉 Failed。
可執行回合的零預算在 fake 步進前拒絕，保留已接納 batch 的 epoch。

在現有 `eob-remake-go:1.26.7-ebiten2.9.9` 以整個 `workplace/`
唯讀掛入 `/workplace`，工作目錄設為
`/workplace/phase193-frontend-session-fake`，執行
`go test -count=1 -v ./...`：全部通過。容器參數為 `timeout 90s`、
`--rm --network none --read-only --memory 2g --cpus 2 --pids-limit 256`、
目前 UID/GID、512 MiB 可執行 `/tmp` tmpfs，並設
`GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`。
新增測試固定四個成功 Update 的 epoch `1,2,3,4`：Open、持續開啟、
Cancel 都零步，下一關閉回合才以 budget 7 前進；另外固定
`Advance` 恰一次、未經 `Deliver`／重疊 `Deliver` 故障、零預算拒絕。
四個混合批次負例（先有 canvas pointer 再遇未知鍵、後續非法 host
route、host Open 後遇未知鍵、後續 stale layout token）皆回錯，
`Epoch=0`、fake BIOS／mouse／IRQ／VRAM／save 計數全零，host 快照
不變，並只 Close 一次。合法 pointer＋鍵盤批次則提交 mouse／BIOS
各一次，epoch 為 1；舊的面板暫停與六階段故障測試也通過。

本次 ignored 來源 SHA-256：`session.go`
`3bb381259ae8631e64e81c84bde787db8ed25b45666fa901feb3f8c8b832ded0`；
`route_plan.go`
`9cc709e06f97496957502c7eac5f23549a1c5416efb25bc957467ab528946cfd`；
`ready_candidate_test.go`
`07fa5422011e31a59af836333897023d1744374c5c89223fad9c6dcc3c25ad50`；
更新的 `session_test.go`
`b5e128ebd81f2c20e488784c1adae8cf0643d385621b0851e2a22b215ff79d6c`；
`lifecycle_fake_test.go`
`6c78b26ca6a5100ed05c557947edd7fb216949713872e256b3288bdaa61fc2fd`。

上節 epoch 與整批路由的**fake 前置缺口**因此已有可重播補證；
它尚未把 phase211 的真實 `Machine.Steps`、raw stop／error 與此
typed Update owner 接成同一收據，也未驗正式 pointer／鍵盤橋接
的提交階段是否可能部分送入。合成 layout token 固定為 1，
fake mouse 只是計數器；不能外推真實 layout epoch、滑鼠狀態機、
Ebitengine `Draw` 同步 fault 或真實資源 Close。
故本次**不升 READY、不改 production**，仍須以正式 API 與同一
typed session 的 machine 差分負例完成獨立審查。
