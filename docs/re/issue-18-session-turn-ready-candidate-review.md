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

## READY 前可丟棄補證：同一 typed owner 的 Machine 收據（2026-09-24）

在 ignored `workplace/dosgolem/workplace/phase211-session-receipt-candidate/`
新增 `turn_owner.go` 與 `turn_owner_test.go`。`TurnOwner` 在一個物件內持有
合成純資料路由、接納批次序號、pending 回合、phase、合成 BIOS／mouse 計數，
以及**真實** dosgolem `Machine`／`DOS`。它用合成 COM 載入，透過
`Machine.RunUntil` 取得 raw stop／error，直接以呼叫前後 `Machine.Steps`
計算嘗試數。路由 token（`LayoutEpoch=1`）和交付計數仍是可丟棄模型，
不代表正式 bridge 或《拯救地球》的輸入語意。

重播環境：本機 ignored dosgolem fork HEAD
`a01e34253fa59cc92c3fde1bf4b33577e318e9e7`；Go 1.26.7；既有
`eob-remake-go:1.26.7-ebiten2.9.9` image ID
`sha256:39d6e05c9abc60a566e376cde6afd29c24aa21c30eeec1e1fd92c8b16e62aa60`。
確認 `/home/anr2/cht/golden_box/拯救地球/workplace/dosgolem` 為既有目錄後，
以其唯讀掛載 `/dosgolem`，工作目錄 `/dosgolem` 執行
`/usr/local/go/bin/go test -count=1 ./workplace/phase211-session-receipt-candidate`。
容器使用 `timeout 90s docker run --rm --network none --read-only --memory 2g
--cpus 2 --pids-limit 256 -u "$(id -u):$(id -g)"`、512 MiB 可執行
`/tmp` tmpfs、`GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`；全套通過。
格式化時同 image 暫以工作樹可寫掛載，寫後抽查兩檔皆為 UID/GID
`1000:1000`。兩個新 ignored 檔 SHA-256 分別為
`79ea27ded94fe91b6d387328aeabee209cd46a5a85fa269d8f1502f68b21087d` 與
`0d175e42a51b912dcb9e0e32a319738371a12bda692f662d52d14275e1ecc366`。

同一 owner 的測試實測：Open、保持開啟、Close 三個成功接納批次的 epoch
為 1、2、3，皆 `PanelPaused`、零 `Machine.Steps`、零合成 BIOS；下一
關閉批次 epoch 4 以 budget 2 執行真實兩步，前後 Steps 為 0→2，
raw `StopBudget`、`BudgetExhausted`。epoch 5 的 predicate 提早停止於
2→3，raw `StopPredicate` 與 `PredicateStopped` 分離；另一回合的 breakpoint
亦保留 raw `StopBreakpoint` 與兩步差分。晚到的非法鍵、非法 pointer、
stale layout token 及 host transition 後非法鍵都在接納前拒絕，epoch、
Machine 步數及合成 BIOS／mouse 計數維持零。重疊或重複 Advance、
零或超過原型上限的 budget 均使 owner `Failed` 且沒有新增步數。
DOS 正常退出即使 raw stop 為 `StopBudget` 仍回 `ProgramStopped`；
已退出的起點零步且不呼叫 `RunUntil`。非法 opcode 的 machine error
伴 raw `StopBudget` 時，故障收據仍保留 0→2 的兩次嘗試，phase 為
`Failed`，再次輸入被拒。

此補證閉合先前「epoch／budget／phase 與真實 Machine 差分從未同處一個
typed owner」的**合成原型**缺口；它不把規格 019 升 READY。原型的
`TurnBatch` 沒有正式 `readFrameInput` payload、實際 layout epoch 或
`PanelController`／`MouseBridge`／`KeyboardBridge` 提交，因此提交階段能否
在無部分 DOS 交付下失敗仍待正式橋接證明。合成 owner 也未接
`Game.Draw` 同步 `ReportDrawFault`、下一次 `Update` 的零步閘門、真實資源
Close 一次與 close error 保存；這些維持實作後驗收邊界。原版素材與
正常玩家路徑完全未參與，不能聲稱原版同狀態或中文化完成。

## READY 前可丟棄補證：真實橋接的後段 route 失敗（2026-09-24）

本輪唯讀核對同一 fork 的正式 API：`host/mouse_bridge.go` 的
`MouseBridge.Handle` 回 `MouseRoute` 而非 error，成功的 canvas Down
立即呼叫 `MouseOutput.MoveMouse`／`PressMouse` 並改自己的 pressed state；
Up／focus loss 可立即 Release。`host/panel.go` 的 `PanelController.Route`
在 Open／Select／Apply／Cancel 成功時立即改面板或倍率狀態，時序或倍率
錯誤則回 error。`presentation/keyboard.go` 的
`KeyboardBridge.DeliverBIOSKey` 先呼叫該 Route，允許時立即呼叫
`DOS.PushKey`；`DOS.PushKey` 先試 BDA 環形緩衝，滿載退入 DOS 自有 queue，
其簽名無 error。`MouseBridge.ApplyLayout` 可因無效或未遞增的 epoch
回 error；`Game.refreshLayout` 目前在呼叫它前還會改 frontend layout
並呼叫 `ebiten.SetWindowSize`。因此路由預檢與正式提交不得混用，也不能
把已送的 DOS 動作視為可回滾。

在同一 ignored `phase211-session-receipt-candidate/` 新增
`real_bridge_batch_test.go`，以**真實** `PanelController`、
`MouseBridge`、`KeyboardBridge`、DOS mouse 與 BIOS queue 重播合成
canvas Down → 非法 Apply（面板仍關閉）。逐事件直接提交時，後段
`Panel.Route` 回錯，但 `MouseBridge.Pressed()` 與 `DOS.Mouse.Buttons`
左鍵位已設，證明部分 DOS 副作用。另一組先用**獨立的暫態**
`PanelController` 與 `MouseBridge`（後者接計數 sink）預檢相同批次，
在任何真實橋接提交前拒絕；真實 DOS mouse button 與
`DOS.KeysPending()` 均為零。合法 canvas Down＋BIOS key 批次則於
預檢後經正式橋接成功提交，DOS button 設定且 pending key 為 1。
這些測試不執行原版 EXE，也沒有觸及私有素材。

重跑命令及容器限制沿用上節；`go test -count=1
./workplace/phase211-session-receipt-candidate` 全套通過。新 ignored
測試檔 SHA-256 為
`6dd2bb45a622260cd96f0d8aefecc483fa805043267905339b22135cbc903380`，
UID/GID `1000:1000`。初次編譯因測試誤將 `dos.KeyForRune` 當成單一回傳
值而失敗，改為接收 `(Key, bool)` 後以同一容器、同一測試命令乾淨重跑；
這是測試原型的編譯錯誤，不是橋接產品缺陷。

此原型**只從新建、關閉、未按住滑鼠的狀態**開始。正式最小改動應在
同一 typed session／單一 goroutine 建立完整批次的純資料 route plan：
從當前 `PanelState`、`MouseBridge` 的 pressed／pressedEpoch／hostCaptured、
current layout 與焦點狀態複製到獨立暫態；按 Down→Up→focus loss→有序
鍵盤順序驗證每個 route、layout epoch、host transition、鍵盤 transport
與 payload，並產出不可變提交清單。`pressedEpoch` 現為私有欄位，
不能靠現有公開 `Pressed()`／`HostCaptured()` 完整重建；可在通用 host
層新增唯讀狀態快照及無輸出 route evaluator，或讓 `MouseBridge`
本身提供使用相同內部狀態的純預檢方法。正式提交前需確認 plan 的
來源狀態／layout 仍一致，且提交階段不再執行可失敗的分類、
`ApplyLayout` 或 payload 判定；若仍可能出現普通錯誤，必須證明它
發生在第一個 DOS 動作之前，否則不可宣稱整批原子拒絕。

READY 閘門因此是：以實際前端擷取 batch 和正式 bridge 在已按鍵、
host capture、layout 切換、focus loss、混合 pointer＋鍵盤及後段
非法 route 中驗證「拒絕時 DOS button／座標／callback queue／BIOS queue
皆無新增副作用」，並核對成功 plan 的提交次序及結果與預檢相符。
此處的「原子」只指已列出的普通、可回報路由錯誤；不主張記憶體耗盡
或程序中止等不可恢復情境有交易保證。正式 production 未更動，
規格 019 繼續維持 READY 候選。

## 整批提交契約審查補記（2026-09-24）

依上節真實橋接負例，已在[規格 019](../spec/019-linux-frontend-session-turn-boundary-draft.md)
的限縮 READY 候選下追加「整批純路由預檢與單次 DOS 提交」待審契約。
本輪只改規格與本審查紀錄，沒有修改 `workplace/dosgolem` 正式
`host`、`presentation`、`frontend`、page9 程式或原版素材。

唯讀重核的現行順序是：`Game.Update` 取得一次 `frameInput`，先 Down、
Up、失焦清理，再按有序鍵盤清單處理；`routePointer` 的 host hit
先呼叫 `MouseBridge.Handle`，後呼叫可能回錯的 `PanelController.Route`，
一般 pointer 則忽略 `MouseRoute.Reason`。`MouseBridge.Handle` 的
Down／Up 可立即改 DOS mouse；`KeyboardBridge.DeliverBIOSKey` 在
`Panel.Route` 成功後立即 `DOS.PushKey`，其普通呼叫無 error 回傳。
`MouseBridge.ApplyLayout` 可回無效／非遞增 epoch error；目前
`Game.refreshLayout` 在呼叫它之前已改 frontend layout 並設定視窗大小。
因此僅把後段錯誤處理改成 fail-close，不能回復已發生的 DOS 動作。

新契約把擷取 batch、panel／mouse／frontend layout 來源快照、逐事件
值狀態預檢、不可變 DOS action 清單、提交前狀態核對及單次提交階段
分開。mouse 快照必含 `pressedEpoch`；現行公開 getter 缺此欄，不能
從 `Pressed()`、`HostCaptured()`、`Layout()` 還原跨 epoch Up 路由。
預檢需涵蓋 Down→Up→失焦→keys，並列清 host 消費、DOS 轉送、
既有可接受 no-op 與整批拒絕；失焦無 pressed 時雖可能回
`unmatched-up-rejected`，仍必須清 host capture。正式 bridge 的
`duplicate-down-rejected`、`outside-canvas-rejected`、普通 unmatched Up
目前被 `Game` 忽略，其 fail-close 或 no-op 政策須由 READY 審查定案，
不能只靠 reason 字串推測。

最小通用改動候選：host 層提供 mouse 完整唯讀狀態及與正式
`Handle` 共用判讀的純預檢，panel 層提供同樣的值狀態 transition；
兩者的已驗計畫在單一 owner、來源狀態一致時交由不再執行可失敗
路由的提交操作，session adapter 才將已驗 mouse 操作與 BIOS／IRQ
payload 送 DOS。若沿用現行 `Route`／`Handle` 逐筆重播，還需以
正式測試證明其每個提交步驟都不會產生新的普通拒絕；目前沒有
這份證據。`Game.refreshLayout` 的可失敗驗證和外部視窗尺寸變更
必須在第一個 DOS action 前處理或隔離，不能夾在提交清單中。

目前仍阻塞限縮 READY 的具體項目：完整既有 mouse state 的可觀測
快照／純 evaluator、提交階段不再出現後段普通拒絕的證明、實際
`readFrameInput` adapter 對 layout／未映射鍵的定案，以及規格 019
矩陣中已按鍵、host capture、跨 epoch Up、失焦、混合鍵鼠、後段
錯誤與來源 token 改變的正式 bridge 收據。上節合成新建狀態原型
不能替代這些收據；規格 019 不升 READY。拒絕時的零新增 DOS
副作用只針對可回報的普通路由錯誤，不推及記憶體耗盡或程序中止。

## 真實 `Game.Update` 同批後段鍵盤錯誤負例（2026-09-24）

再依規格 019 的限縮 READY 候選與現行 frontend 實作獨立審查：
規格首行仍明示「候選、尚不授權 production」，整批純路由預檢
尚無正式 host mouse 完整快照（尤其 `pressedEpoch`）、panel／mouse
純 evaluator、提交前來源狀態核對與不再可失敗的提交證明。因此本輪
**只新增專用負例測試，不修改正式 `Game.Update`、host 或
presentation bridge，也不升 READY**。

ignored dosgolem fork 的
`frontend/ebiten/route_plan_pre_fix.go.txt`（當時檔名為
`route_plan_draft_test.go`）新增
`TestDraftUpdateLateKeyboardTransportErrorLeavesDOSMouseDown`，SHA-256
`967ccb3d621ccda339d5a6d90ea67bb519217ab969d7e763c90782ebeae33c5d`。
它用無原版素材的合成 `frameInput`，但走真正的
`Game.New`／`Game.Update`、`MouseBridge`、`DOS` mouse 與
`KeyboardBridge`：`NewKeyboardBridge` 是合法建構，卻未配置 BIOS
transport；同一 `Update` 擷取 canvas Down＋Enter。固定順序先將
Down 送到 DOS mouse，後段 `DeliverBIOSKey` 因缺 BIOS transport
回普通 error。實測 `Game.Update` 回錯並鎖存；DOS 左鍵位已設、
`MouseBridge.Pressed()` 仍為 true，BIOS pending、`Machine.Steps`
與 `Advance` 次數均為 0。再呼叫 `Update` 回相同錯誤且無新增步數，
但先前左鍵副作用仍在。這比僅直接呼叫 bridge 的前述負例更接近
現行實際 batch adapter，仍不是正常玩家輸入或原版同狀態驗證。

這個負例可由 `Game.New` 對鍵盤 transport 做早期驗證消去其**特定**
觸發條件，但不能單靠該檢查推出整批零 DOS 部分副作用：後段
layout／panel route、mouse stale epoch、已按鍵與 host capture 等
仍須依規格 019 的純資料 plan、提交前核對及完整矩陣審查。
本輪維持 DRAFT／READY 候選，不以一個補丁替代正式整批契約。

## 純資料 route evaluator 的可丟棄差分原型（2026-09-24）

延續上節 `Game.Update` 的同批部分提交反證，在 ignored dosgolem
fork 的 `frontend/ebiten/route_plan_candidate_test.go` 建立**僅測試用**
的值狀態 evaluator，SHA-256
`d00b74781c5a065cbdd1fb620e32f5d194030e7ca0ca45de645b35ee6c5f413e`。
它的來源狀態明列 panel `Open`／active／selected scale、完整
`MouseLayout`（含 epoch）、mouse current／hasCurrent／pressed／
`pressedEpoch`／hostCaptured；事件按目前 `frameInput` 的 Down、Up、
focus loss、有序鍵盤候選展開。純預檢只改這份值拷貝，產出定序
`move`／`press`／`release`／`bios` 動作清單，不碰正式
`PanelController`、`MouseBridge`、DOS 或視窗。若模擬 panel
Open／Select／Apply／Cancel，僅在正式 `refreshLayout` 會改佈局的
Open／Apply／Cancel 時增加 layout epoch；已按住時保留原
`pressedEpoch` 以處理跨 epoch Up。這是從現行正式程式抽出的
**DRAFT 差分模型**，不是已授權的通用 host API。

受限、無網路、唯讀 Docker/Xvfb 中，`TestDraftPureRoutePlan*` 四組測試
通過：canvas Down 後的非法 Apply、缺 BIOS transport、stale Up
三種**後段普通錯誤**，都在第一個 DOS 動作前拒絕整批，DOS button、
BIOS pending、`Machine.Steps` 仍為零；合法 canvas Down＋Enter
先完整計畫後交付，DOS mouse 座標／按鍵、BIOS pending 與真實 bridge
逐項同值。來源 token 被測試改動時，原型在提交前拒絕且 DOS 不變。
2× Open→Select 3×→Apply 的各回合 panel／layout／mouse 末態與
現行 `Game.Update` 相同；已按住跨 epoch Up 的單次 Release、按住
失焦的 Release，以及 hostCaptured 失焦不產生多餘 Release，均與
真實 `MouseBridge` 回傳／sink 觀測相符。`go test -count=1 -v
./frontend/ebiten` 與 `go vet ./frontend/ebiten` 全套通過；專用
實驗沒有載原版遊戲、存態或私有素材。

**尚未閉合 READY，規格 019 狀態不變。** 原型的來源狀態由測試
顯式建造；正式 `MouseBridge` 尚無包含私有 `pressedEpoch` 的完整
唯讀快照。原型 `draftCommitIfCurrent` 只比對呼叫端傳入的值，沒有
從正式 panel／mouse／frontend 一次取一致 token，亦不能更新真實
bridge 的內部末態；`draftCommitDOS` 直接按清單寫 DOS，只驗目前
無普通 error 回傳的動作，不能證明正式 bridge 的提交不會重做可失敗
路由。非法 Apply 是明示注入的 host 候選，不冒稱目前
`readFrameInput` 同批可自然擷取兩次 Down。未映射鍵、重複 Down、
畫布外 Down、普通 unmatched Up 仍依現行 `Game` 的無動作行為
建模，但玩家可見拒絕／略過政策待獨立 READY 審查，不能由此原型
自行定案。正式可行的下一個最小切片仍是通用 host 的完整快照與
純 evaluator／已驗計畫提交 API，然後用真實 bridge 量完規格 019
矩陣；本輪不改 production、不請求自行核准 READY。

## 完整來源快照與版本 token 負例（2026-09-24）

本輪唯讀核對正式 `host.PanelController`／`MouseBridge`：前者的
`Snapshot` 可取得 open、active／selected 值，後者內部還有
`current`、`hasCurrent`、`pressed`、`pressedEpoch`、`hostCaptured`，
但公開 getter 不含 `pressedEpoch`。`PanelController.Route` 與
`MouseBridge.Handle` 都是可直接呼叫的 mutator，後者可即時寫
`MouseOutput`；目前不存在能把兩者及 frontend layout／phase 一次
擷取的正式來源 token。`ApplyLayout` 另有普通錯誤，不能留到已送出
DOS 動作後才呼叫。

ignored fork 新增**僅測試用**
`host/route_source_token_draft_test.go`，SHA-256
`7cac0cf53f00b394943fc0db819f377255f9933c6d72758c095a647829ed8e16`。
它以同 package 的測試權限擷取私有 mouse 欄位，並以可丟棄 wrapper
模擬單調版本，不改正式 host API。三項測試證實：跨 layout epoch
按住時，完整快照必須同時保留舊 `pressedEpoch` 與新 current epoch；
Open→Cancel 及真實 MouseBridge 的 Down→Up 後，**逐欄完整值快照
可與預檢前完全相同**，但 DOS sink 已有 move／press／move／release，
只比值會遭遇 ABA；wrapper 版本改變時，過期計畫在任何新輸出前拒絕。
反向負例再直接繞過 wrapper 呼叫 `MouseBridge.Handle` 完成 Down→Up：
版本未變、值也復原，測試用提交會錯誤接受舊計畫。這是候選 wrapper
安全性不足的**正向重現**，不是正式產品預期成功行為。

以現有 `eob-remake-go:1.26.7-ebiten2.9.9` 執行
`timeout 90s docker run --rm --network none --read-only --memory 2g
--cpus 2 --pids-limit 256 -u "$(id -u):$(id -g)"`，唯讀掛載
`workplace/dosgolem:/dosgolem:ro`、可執行 `/tmp` tmpfs，設定
`GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`，在 `/dosgolem`
執行 `go test -count=1 ./host && go vet ./host`，全套通過。
第一次 `/tmp` 未顯式指定 `exec`，測試二進位出現 permission denied；
同一測試改用 `--tmpfs /tmp:rw,exec,nosuid,size=1g` 後乾淨重跑通過，
屬容器設定問題，非產品失敗。既有 frontend 純 evaluator 的後段
非法 Apply／缺 BIOS transport／stale Up 零新增 DOS 負例仍是前節
證據；本輪另以同一唯讀 Docker／可執行 tmpfs，容器內直接啟動
`Xvfb :99` 並設 trap，重跑 `go test -count=1 -run
TestDraftPureRoutePlan -v ./frontend/ebiten && go vet ./frontend/ebiten`
通過。`xvfb-run` 首試因映像缺 `xauth` 失敗，改用直接 Xvfb 後通過，
是容器啟動方式問題。本輪沒有把 test-only wrapper 當正式整批提交。

審查候選的最小通用變更是：由**同一 host route owner** 管理
panel／mouse 的完整快照與所有 mutator 的單調 generation；前端
layout／phase／pending 也納入同一來源核對；對值拷貝純預檢整批；
`Commit` 核對 generation 與完整起點後安裝已驗 host 末態、交出定序
DOS 動作，不能再呼叫可失敗的 `Route`／`Handle`／`ApplyLayout`。
提交與動作交付區間必須排除重入；否則需把交付收進同一 owner。
規格 019 已補此限縮契約，但**尚未達 READY**：共同 owner／不可繞過
mutator、正式 `readFrameInput` adapter、鍵盤未映射政策與完整矩陣
尚無正式 bridge 收據，須交獨立審查，不得由本測試自行升級。

## 連續 host／滑鼠輸入鏈的差分補證（2026-09-24）

ignored `frontend/ebiten/route_plan_player_chain_draft_test.go` SHA-256
`86f0a5f09d590382de1a23b83d6d0afb5177534ed6fd49ca9ec5dadc42cba283`
在無原版素材的合成 `Game.New` 上，將測試用純資料 route plan 與**現行正式**
`Game.Update` 逐回合比對。固定鏈涵蓋 2× 畫布按下、畫布外放開、同一
`Update` 內 Down＋Up、Open、暫選 3×、Apply、3× 畫布按下後失焦釋放，
再 Open、暫選 2×、Cancel。每回合對 panel、layout epoch、mouse
current／pressed／host capture 與 DOS mouse 動作種類逐項比對，
17 回合均同值。這補強候選 evaluator 對**已接受**連續事件的狀態模擬，
不檢查 mouse 座標值，也沒有原版 DOS／遊戲輸入。

既有 `eob-remake-go:1.26.7-ebiten2.9.9` 的唯讀、無網路、有界
Docker／直接 Xvfb 中，`go test -count=1 ./frontend/ebiten` 與
`go vet ./frontend/ebiten` 通過。此差分不能證明拒絕批次的原子性：
現行正式 `Game.Update` 仍會在後段錯誤前先送 DOS mouse，測試用
plan 也無正式共同來源 generation 或不可失敗的 commit；規格 019
維持限縮 READY 候選，不改 production。

## BIOS transport 建構前檢的可變別名反證（2026-09-24）

為縮小上述已量到的「Down 已送、Enter 才因缺 BIOS 回錯」來源，
本機 fork 新增 `docs/spec/233-ebiten-bios-transport-preflight-draft.md`
作限縮 DRAFT 候選；正式程式未更動。獨立審查首先指出
`Config.Panel` 與 `KeyboardBridge.panel` 可為不同指標，故單純
`ValidateBIOS()` 不能保證面板隔離一致；候選已改要求同一 panel。

第二次審查指出 `internal/dos.DOS.M` 為公開可寫指標，建構時即使
與橋接器 machine 同一，之後仍可改指他台。ignored
`presentation/keyboard_machine_alias_pre_fix.go.txt`（當時檔名為
`keyboard_machine_alias_draft_test.go`）SHA-256
`a92d3e28bcfeb2cb00be348ef0205441fecd91f639effdd36697e693639e80fa`
在無原版合成環境把它改指第二台，實測現行 `DeliverBIOSKey`
無錯且將鍵排入**第二台** BIOS queue，第一台仍為零。無網路有界
Docker 的該測試與 `go vet ./presentation` 通過；這是正式 API
可變別名的反證，不是原版遊戲輸入收據。

規格 233 因此新增 `Game.New`、每個 `Game.Update` 路由前的
panel／BIOS machine 前檢，以及 `DeliverBIOSKey` 自身交付前
重驗的窄契約，仍待獨立複審。若在已前檢的同批中透過回呼或
競態再改 `DOS.M`，交付前檢可阻止錯送鍵，不能回滾已送的滑鼠；
完整來源獨占與整批零部分副作用仍是規格 019 的 READY 阻塞，
不得因限縮修補而宣稱 session 原子性或 Linux 可玩。

## BIOS transport 前檢限縮 CONFORMED（2026-09-24）

前述兩份修正前反證保留原始 SHA-256，已移作 `.go.txt`，不再編入現行
Go 測試。dosgolem fork `docs/spec/233-ebiten-bios-transport-preflight-draft.md`
經獨立 READY 審查後，正式 `KeyboardBridge.ValidateBIOSForPanel`、
`Game.New`、`Game.Update` 與 `DeliverBIOSKey` 完成建構前、回合前、
交付前三層檢查；有效輸入順序未改。獨立實作審查確認檢查位置
與 `DOS.M` 可變別名防線，並要求補測在 `Game.New` 前改機的零副作用
負例；已連同無 BIOS、不同 panel、同包無效私有欄位、建構後改機
及有效路由正例驗收。

既有 Go 1.26.7／Ebitengine 2.9.9 Docker／Xvfb，無網路、資源上限、
唯讀原始輸入下，`go test -count=1 ./presentation ./frontend/ebiten`、
`go vet ./presentation ./frontend/ebiten`、
`go test -race -count=1 ./presentation ./frontend/ebiten` 均通過。
此為已證實錯誤配置的窄修補；相同批次中的其他後段錯誤、並發改指、
滑鼠橋與鍵盤橋同機、完整 session owner、原版同狀態及正常玩家
路徑仍未驗，規格 019 不升 READY，Issue #18 保持 OPEN。

## 滑鼠／鍵盤目標分裂及前檢後改指（2026-09-24）

正式 `Game.New`→`Game.Update` 的兩個合成負例已量到前節未覆蓋的
提交目標身分：滑鼠橋可接 DOS A，鍵盤橋可接 DOS B，同批 Down＋Enter
分別改動 A 的滑鼠及 B 的 BIOS queue；若先共用同一 DOS，回合前檢
後再改公開的 `DOS.M`，鍵盤交付前會正確拒絕，但已送出的 Down
仍留下位置 `(100,32)` 與左鍵按下，兩台 machine 均無新鍵／步數。
前態均為空滑鼠／鍵盤佇列。ignored 測試檔
`workplace/dosgolem/frontend/ebiten/route_commit_target_alias_draft_test.go`
SHA-256 `c73093b27b5d5b362fd7833ed9c674503965bf9c28287519e457ae5a986cd8bc`；
主代理在無網路、唯讀 Docker／Xvfb 獨立重跑 2/2 與 `go vet` 通過。
只用合成機器，沒有原版遊戲素材或玩家路徑。

因此共同來源版本不只管理 host panel／mouse 值與 layout，也須釘住
兩個 DOS 輸出 bridge 的共同 DOS／machine 身分、變更來源與整批排他性。
規格 019 已增補此停止線；規格 233 的限縮 BIOS 前檢仍有效，但不能
被誤寫成完整回合原子性。Issue #18 保持 OPEN。

## 共同目標／版本／單次提交的合成原型（2026-09-24）

ignored `frontend/ebiten/route_commit_owner_draft_test.go` SHA-256
`a750e68ea6a299d6ba04f48afd7b025876214df59f4fa6277cba3b3c78c12069`
以合成 DOS 建立「純預檢→釘住同一 DOS／machine 與 generation→
一次提交」的最小模型。不同目標、後段預檢錯誤、rebind ABA 與
提交前公開 `DOS.M` 改指皆零新增滑鼠／BIOS／step，成功只交付一次；
重入 owner rebind 與重播計畫被拒。主代理在 Go 1.26.7／Ebitengine
2.9.9 的唯讀、無網路 Docker／Xvfb 重跑定向測試及 `go vet` 通過。
本模型直接寫合成 DOS，未接正式 bridge；外部仍能改 `DOS.M`，
故未消除正式回合阻塞，也不升 READY。

## 提交期間公開 `DOS.M` 改指的獨立反例（2026-09-24）

獨立子代理於 ignored
`workplace/dosgolem/frontend/ebiten/route_commit_target_alias_draft_test.go`
新增 `TestDraftPublicDOSMRebindInsideCommitEscapesOwnerGuard`；整檔
SHA-256 `5e59fb921e7964d7b99898c957c03b408166c043eb864430f0c6f29ca9afb2ca`。
`draftBoundOwner` 的純預檢及提交起點核對均成功，且 owner 自己的
`rebind` 被提交中閘門拒絕；但 reentrant hook 直接改公開的 `d.M`
後，原型仍完成提交、epoch 增至 1。滑鼠座標 `(100,32)` 與左鍵留在
原 DOS，BIOS 鍵卻送至另一台 machine。兩台 machine 的 Steps 均為零。
主代理沒有將這個合成反例解讀為原版遊戲已發生改指；它證明目前
owner **不能保證**提交全程目標排他。子代理在有界、唯讀、無網路
Docker／Xvfb 重跑新舊定向 Go 測試通過；正式 bridge 仍未接共同
owner，規格 019 保持 DRAFT／限縮 READY 候選。
主代理亦在同一唯讀 Docker／Xvfb 獨立重跑新反例與既有共同
owner 正反例，全部通過。

READY 前必須能核對 MouseBridge 實際輸出與 KeyboardBridge 的
BIOS transport 指向同一 DOS／machine，並在完整提交區間封閉所有
公開 `DOS.M` 改指及其他來源變更。只在開始前比指標、只禁止
owner 自身 rebind、或提交後再檢查，都不能倒銷已交付的 DOS 副作用。

## 同一 DOS 指標下仍可分裂 callback 與 BIOS（2026-09-24）

子代理於同一 ignored
`workplace/dosgolem/frontend/ebiten/route_commit_target_alias_draft_test.go`
補上滑鼠 Handler 啟用與逐動作核對反例；新全檔 SHA-256
`1f12ac86a696d18969ea2764e98ee85cc3cd4b63693271341fb05ab6e84b8768`。
主代理逐行檢視後，以唯讀、無網路 Go 1.26.7／Ebitengine 2.9.9
Docker／Xvfb 獨立重跑五項定向測試與 `go vet ./frontend/ebiten`
通過。以下皆為**合成提交原型**，不證明原版遊戲實際改指。

- 同一 `*DOS`、滑鼠 Handler 同時監看 move／left-down：先 move，
  再在提交中直接改公開 `DOS.M`，接著 press 與 BIOS key。原 machine
  得到一個 move callback；另一 machine 得到一個 press callback
  與一個 BIOS key。DOS 滑鼠座標為 `(100,32)`、左鍵按下；兩台
  machine 均未 Step。故「兩橋同一 DOS 指標」**不足以**固定實際
  callback／鍵盤目標。
- 若在每筆 action 前補 `DOS.M` 核對，分別於 move 後與 press 後
  改指，可得到晚期拒絕；但原 machine 已有 1／2 個 callback，
  且 DOS 滑鼠位置或按鍵已改。拒絕時 epoch 雖不增加，仍不滿足
  「零 DOS 副作用」；逐動作檢查不是整批原子提交。

最短 READY 缺口因此不是再多加一個指標比較，而是能強制的單一
session owner：固定 DOS／machine 的私有擁有權、兩橋同源建立、
提交期間排除外部 `DOS.M` 改指或直接呼叫 bridge mutator，完整批次
先純預檢，再以固定目標提交所有已知不會失敗的動作。若仍允許
任意外部程式直接改公開 `DOS.M`，目前 owner 自己的 mutex 或
generation 無法保證整批排他。拒絕收據須核對滑鼠、callback、
BIOS／IRQ 佇列、machine steps 及 epoch 全無新增副作用；正式 API
未具備此契約前，規格 019 維持 DRAFT。

## 私有目標 session 的限縮可行性原型（2026-09-24）

子代理在同一 ignored 測試檔新增 `draftSealedSession`；全檔 SHA-256
`b6f65715f70f32e0486e1fa15adae80f707cf0c4a7691b2378ada30df64a186b`。
主代理逐行審閱，並於唯讀、無網路、有界 Docker／Xvfb 獨立重跑
六項定向測試與 `go vet ./frontend/ebiten`，均通過。全模組非測試
Go 檔未找到 `.M =` 寫入，但 `DOS.M` 仍是公開可寫欄位；搜尋
陰性不是外部呼叫者無法改指的證據。

原型由單一工廠自建 DOS、machine、panel、滑鼠橋及鍵盤橋，不接受
或回傳這些可變指標；只允許合成 canvas Down＋Enter。完整純路由
預檢後，正式兩橋把滑鼠 `(100,32)`、左鍵、兩個滑鼠 callback 與
一個 BIOS 鍵交給同一 machine，步數零、epoch 增一；後段預檢錯誤
及舊計畫在首個 DOS 動作前拒絕，滑鼠、事件、callback、BIOS／IRQ、
步數與 epoch 均無新增。owner 改指請求與重入亦被拒絕。

這只證實「不外洩原始目標」可成為限縮契約的設計方向，不是現有
`Game.New(Config)` 的保證。測試程式本身仍持有私有欄位、提交路徑
只支援一種批次，且以 panic 表示純計畫與橋接器分歧；正式程式
尚無完整滑鼠 pressed epoch 快照、全部輸入矩陣、故障／資源關閉、
原版同狀態與視窗玩家路徑收據。故規格 019 整體維持 DRAFT，
不得把此可丟棄原型當成完成的原子提交。

## 完整路由矩陣與推進故障鎖存複審（2026-09-24）

獨立子代理新增 ignored
`workplace/dosgolem/frontend/ebiten/route_sealed_matrix_gap_draft_test.go`
（SHA-256 `26a1353598b9655f42c533929cfc85ad9006fca39f732ddbfcf8446fb5af4e56`）。
純路由計畫可接受同批 Down＋Up、Open＋Enter、失焦、多鍵，與已按下後跨
layout epoch 的 Up；但目前 `draftSealedSession.prepare` 對這五類合法批次
全部拒絕，因其硬編三筆 move／press／BIOS 動作。提交前的目標或 layout
漂移可在首筆 DOS 動作前拒絕，尚未證明提交期間排他、完整滑鼠狀態與
實體 `Game.Update` 的整批原子性。此處仍只有合成 DOS，無原版玩家收據。

另一獨立審查發現 ignored typed `TurnOwner` 首次 machine 故障後的重試
雖零新步，卻把 `OriginalFault` 與原始 error 遺失成 `Failed`／nil。
代理只在 ignored 原型修補 terminal 鎖存：
`workplace/dosgolem/workplace/phase211-session-receipt-candidate/turn_owner.go`
SHA-256 `11ed3fd23a81bb5ca951d2135f137a1b6ea701be71c00da51c5147775edd9899`，
測試檔 SHA-256 `63827dc0e4dc8570288f3782c2c2f8ade8193c487b5383b0666b9988728127ae`。
首次非法 opcode 收據為 `OriginalFault`、`Steps=2`、raw `StopBudget`；
再次 `Advance` 保留同一根因與停止碼，`Before=After=2`、`Steps=0`，
不呼叫 `RunUntil`、不增加 epoch。主代理逐行審閱，於 Go 1.26.7
專用無網路、唯讀、有界 Docker 獨立重跑該 package 全測試與 `go vet`
通過，並核對三檔雜湊。修正只使推進收據原型可再審；正式 session
尚無共同私有 owner、整批提交或 Draw 故障收束，規格 019 不升 READY。
