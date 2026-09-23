# 第一百九十六階段：設定面板同批鍵盤不再漏入 DOS

日期：2026-09-24
狀態：**限縮 CONFORMED；只驗收正式 `Game.Update` 的面板鍵盤批次隔離。**

使用者已定案：設定面板開啟時，鍵盤只給 host；按 Apply 或 Cancel 收合的當回合仍不推進 DOS。第 194 階段已驗收 `Advance` 暫停閘門，但正式 `Game.Update` 先處理 pointer、再處理鍵盤。面板起點開啟時若同批 pointer Apply 先收合，後續 Enter 原可進 BIOS queue；既有測試明確記錄了這項反例。這是 host 分流缺口，不是原版遊戲規則。

獨立證據審查確認此邊界可由已定玩家決策、可注入的正式單回合輸入與現行反例單獨定義。本機 dosgolem fork 先建立 `docs/spec/232-linux-ebiten-panel-batch-keyboard-gate.md` 為 READY，之後才修改正式程式；提交為 `71f19cb`。`Game.Update` 在 pointer 路由前讀取面板起點；起點開啟或本批有 host 面板 transition 時，不轉送該批鍵盤。Apply／Cancel 仍正常收合、套用或取消倍率，下一個關閉回合可照常轉送鍵盤與推進。

正式套件測試覆蓋 Open／Select／Apply／Cancel 同批 Enter、Apply／Cancel 同批三個 mapped keys、BIOS queue 零輸入、host mouse 零轉送、面板／倍率終態及下一關閉回合恢復；關面板畫布＋Enter 保持可進 BIOS。故障後不再推進的既有測試仍通過。獨立實作審查未發現此範圍內的漏送／誤送。既有 `eob-remake-go:1.26.7-ebiten2.9.9`、Go 1.26.7、無網路 Docker／Xvfb 中，`go test ./frontend/ebiten ./host ./presentation -count=1`、相同套件的 `go vet` 與 `go test -race ./frontend/ebiten -count=1` 全部通過。

本階段未載入原版、字型或私有存態；不證明實體 X11 同一幀恰好收到 pointer 與 key，也不證明 DOS 指令數、完整 machine／DOS 同狀態、冷開機 typed session、存讀檔或可玩 Linux 入口。[規格 004](../spec/004-dosgolem-host-frontend-draft.md)與[規格 019](../spec/019-linux-frontend-session-turn-boundary-draft.md)仍是 DRAFT。原版、手冊、字型與私有測試產物維持 ignored 本機資料，不進 GitHub。
