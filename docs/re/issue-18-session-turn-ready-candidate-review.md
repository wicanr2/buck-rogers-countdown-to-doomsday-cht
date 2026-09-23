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
