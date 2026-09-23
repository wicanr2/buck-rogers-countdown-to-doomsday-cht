# 第二百零三階段：Linux session 同批輸入 fake 勘誤與 READY 缺口

日期：2026-09-24
狀態：**DRAFT 證據；只驗可丟棄 fake，規格 004／019 仍未升 READY。**

## 本輪問題與更正

[第一百九十三階段](phase-193-frontend-session-fake-draft.md)的 `InputBatch.DOSInputs`
預先假設「已分類、面板關閉」；但同一回合若先由 Apply／Cancel 收合面板，
再檢查此候選輸入，舊 fake 會因結束時面板已關閉而把 Enter 計入 BIOS。
這與規格 019 的批次起點焦點規則不符。此處訂正的是 fake 的模型與收據，
不推翻第 193 階段已量的個別面板暫停結果，也不改正式 dosgolem 程式。

本輪將 fake 中的 `DOSInputs` 明定為**同批候選鍵**。`Deliver` 先保存批次起點
面板狀態；若起點展開、批次中有任一 host 面板轉移，或結束時仍展開，
候選鍵不進 fake BIOS。測試固定三個混合批次：關閉→Open＋Enter、
展開→Apply＋Enter、展開→Cancel＋Enter。三者當回合 fake BIOS／IRQ／
mouse／VRAM／save 計數全為零、`Steps=0`；收合後的**下一個**關閉回合
才允許一筆明示 DOS 候選鍵及七步 budget。原有 Open、Select、Cancel、
Apply 個別暫停與 Deliver／Advance 故障後拒絕再推進測試亦通過。

正式 `Game.Update` 的同批鍵盤隔離另有[第一百九十六階段](phase-196-ebiten-panel-batch-keyboard-gate.md)
收據；本 fake 不替代正式路由，更不能證明實體 X11 的 pointer 與 key
會落在同一個 Update。

## 可重生收據

| 輸入 | 固定值 |
| --- | --- |
| fake | ignored `workplace/phase193-frontend-session-fake/`；`session.go` SHA-256 `70e1dbc01da452e62a7cf35543b84a6c38674f3623da51c493b0af8a6fdd0070`；`session_test.go` SHA-256 `7c3c290339490f231f2a41b71e4bbfcc9fdc51f83579b2ac1a09cbafdc8261aa`；`go.mod` SHA-256 `f846467461a6a3baba222db69eddb7efecf1120a0b3ca93dc282b42dd0bf9e44`。 |
| 本機 dosgolem 來源 | `workplace/dosgolem` commit `57436f23688ce034d8265e293bde830829d374b6`，測試時 worktree 為乾淨。 |
| 工具 | 已存在的 `eob-remake-go:1.26.7-ebiten2.9.9`，image ID `sha256:39d6e05c9abc60a566e376cde6afd29c24aa21c30eeec1e1fd92c8b16e62aa60`；容器內 `go1.26.7 linux/amd64`。 |
| 執行 | 將本專案 `workplace/` 唯讀掛至 `/workplace`，工作目錄 `/workplace/phase193-frontend-session-fake`；`--rm --network none --read-only --memory 2g --cpus 2 --pids-limit 256 -u 1000:1000 --tmpfs /tmp:rw,exec,nosuid,nodev,size=512m`，`GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off`，執行 `/usr/local/go/bin/go test -count=1 -v ./...`。四組頂層測試及其子案例全通過。 |

第一次容器測試把 `/tmp` 掛成不可執行，Go 測試二進位啟動時回報
`permission denied`；只修正容器 tmpfs 的 `exec` 旗標後，同一測試通過。
這是驗證環境錯誤，不能記成產品缺陷。此實驗未載原版、手冊、字型、
存態或畫面；無原版位址空間與同狀態 A/B 可引用。fake 維持 ignored，
不加入 Git 或公開素材。

## 對 Issue #18 的判定

此收據補強 Issue #18 完成條件 1 的**混合批次**負例，尚不足以讓規格 019
的完整 typed session 回合升 READY。最短的未驗項是：真實 batch→typed
`Deliver` 邊界、明示 budget 對應**實際** machine 指令數與停止原因、
`Snapshot`／`Draw`／observer 故障的單調 phase 與 Close 一次、epoch
定義及全部負例。Issue 完成條件 2 另需 cold-boot root preflight、
第一步前 observer 安裝、多層順序及 discontinuity 的可丟棄負例與獨立審查。
正式冷開機、正常玩家路徑與原文／繁中同狀態收據仍屬後續實作驗收；
本輪沒有將 callback 次數冒充 DOS 指令數。
