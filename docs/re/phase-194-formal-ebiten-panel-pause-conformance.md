# 第一百九十四階段：正式 Ebitengine 面板暫停推進閘門

日期：2026-09-24
狀態：**限縮 CONFORMED；只驗收正式 `Game.Update` 對 `Advance` 的呼叫排程。**

使用者已決定設定面板開啟時暫停 DOS；Cancel／Apply 收合的當回合仍暫停，下一個關閉面板的更新回合才恢復。第 189 階段提供真實 X11 原型，第 193 階段提供 fake 回合模型；獨立審查後，先在本機 dosgolem fork 建立 READY 規格 `docs/spec/231-linux-ebiten-panel-pause-gate.md`，再修改正式前端。這不把專案[規格 004](../spec/004-dosgolem-host-frontend-draft.md)整體升格。

本機 fork 提交 `c273db6` 在 `frontend/ebiten.Game.Update` 記錄面板回合起點、終點及本回合 host transition。任一條件要求暫停，即不呼叫注入的 `Advance`；路由、版面或 `Advance` 失敗後亦不再推進。正式 `Game.Update` 的可注入輸入測試涵蓋 Open、Select、Cancel、Apply、持續展開、同回合開又關、下一關閉回合、混合 BIOS／畫布事件及故障邊界。

在既有 `eob-remake-go:1.26.7-ebiten2.9.9` 映像、無網路、Docker／Xvfb 中，正式 `Game.Update` 的 opt-in 實體 X11 測試以合成畫布跑完 2×、3× 各一輪 Cancel 與 Apply。四個收合回合為 `88／157／196／264`，第一個恢復推進回合為 `89／158／197／265`；面板期間的 `Advance` 呼叫數均為零，最後倍率回到 2×。受影響套件的 Go 測試、靜態檢查與前端／收據命令的競態檢查通過；獨立實作審查核對了局部範圍。正式規格與可重跑測試均留在 ignored 本機 fork，未包含原版遊戲或倚天字型。

此收據只證實 callback 呼叫排程，**未載入原版**，不證明 DOS 實際指令數或完整 machine／DOS 狀態不變，也不證明冷開機、中文多作用層、存讀檔或可玩 Linux 入口。Apply 與 Enter 同一更新回合時，既有滑鼠先於鍵盤的路由仍可將 Enter 排進 BIOS，雖然當回合不會 `Advance`；完整輸入批次政策留待前端 session 規格。規格 004、Issue #16／#18 仍未完成。
