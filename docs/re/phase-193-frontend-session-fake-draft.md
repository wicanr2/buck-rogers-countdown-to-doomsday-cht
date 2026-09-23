# 第一百九十三階段：面板暫停與前端 session 的可丟棄 fake 測試

日期：2026-09-23  
狀態：**DRAFT 契約實驗；不是正式前端、READY 或同狀態驗收。**

使用者已決定：設定面板展開時暫停 DOS，Cancel／Apply 收合當回合仍不推進，下一個關閉面板的回合才恢復。第 189 階段已在實體視窗量到此排程；第 190 階段則指出正式 `frontend/ebiten.Game` 尚無可保證該行為的 typed session 邊界。本階段只以 ignored `workplace/phase193-frontend-session-fake/` 的純 Go fake 檢查限縮的回合契約，未載入原版、字型或畫面。

## 可重生輸入與結果

- fake `session.go` SHA-256：`053150b102e5c2d04c53b87d634d68295155d2b23f7dd4d25f1a493225d0ee35`；`session_test.go` SHA-256：`f3da95f12e9789e1b0eeb970eed7278b74c85318223067aca9410d12429791c5`。
- 以既有 `eob-remake-go:1.26.7-ebiten2.9.9`、無網路、2 GiB／2 CPU／256 PID、目前 UID/GID 執行；`GOCACHE=/tmp/go-cache GOWORK=off GOPROXY=off go test -count=1 -v ./...` 通過。首次未設定可寫 Go 快取的重跑因容器根目錄不可寫而失敗，改設容器 `/tmp` 後同一測試通過；這是環境問題，不是前端產品缺陷。
- Open、Select、Cancel、Apply 各自的輸入回合回傳 `Steps=0`。面板持續展開時仍零步，收合後下一回合才消費明示 budget。
- host 消費的測試事件不改 fake BIOS／IRQ／mouse／VRAM／save 計數；明示的關閉面板 DOS 輸入才改 fake BIOS 計數。
- 注入 Deliver／Advance 故障後進入 Failed、Close 恰一次，之後拒絕 Advance。

## 審查界線

fake 的 `InputBatch`、phase、receipt 與計數器均非正式 API。它沒有驗證 Ebitengine 事件分流、同一批混合 host／DOS 輸入的實際分類、DOS 狀態、冷開機 preflight、observer 安裝、多作用層聚合、存讀檔或失敗後畫面。特別是 DOS 輸入在 fake 中被假定已先分類，不能據此宣稱 Apply 所在的真實輸入批次不會誤送原版。第 190 階段列出的 typed seam 與失敗矩陣仍須獨立審查，規格 004 保持 DRAFT；正式接線與正常玩家路徑留待 Issue #18、#16。

原版檔案、手冊、字型皆未參與本測試；ignored 原型不進 Git。Docker 任務完成後沒有留下本案容器。
