# 第八十四階段：dosgolem host 前端能力盤點

狀態：完成

## 目標

在不替使用者決定倍率選項的套用語意前，盤點目前 `workplace/dosgolem` 是否已有可重用的
視窗、host 滑鼠分流、輸出重繪與執行期倍率狀態能力；將可證實的通用層邊界與缺口寫成
DRAFT 證據，供後續 READY 規格使用。

## 已確認前提

- dosgolem 的 Buck Rogers 分支是 `buck-rogers-cht-output-overlay`，只可在本機使用，不能推送。
- 玩家以 host 視窗頂端滑鼠按鈕開啟設定面板；host hit event 必須在 DOS 座標轉換、BIOS、IRQ
  之前消費。
- 2×／3× 都必須在遊戲進行中可切換；點擊後立即套用或需確認仍是使用者未決的產品選擇。

## 範圍

- 查核 dosgolem README、CLAUDE、現有規格與原始碼中的前端、事件迴圈、輸出、倍率及輸入邊界。
- 以檔案、符號、測試與既有命令為證據，分級「可重用／需新增／未知」。
- 建立不含 Buck Rogers 特例、也不預設點擊語意的 DRAFT host 前端責任邊界。

## 不在本階段

- 不建立 production 視窗、不實作 host UI、不改 dosgolem 行為。
- 不把使用者尚未選擇的立即套用、面板關閉、Apply 按鈕或設定持久化寫成需求。
- 不改原版 EXE、DOS 滑鼠／鍵盤、手冊驗證、存檔或遊戲輸出語意。

## 完成條件

1. 可重用能力、缺口與未知都有原始路徑／版本與證據分級，且不把 headless CLI 誤稱為視窗前端。
2. DRAFT 文件明示通用 dosgolem 與 `apps/buckrogers/` 的責任界線，並記錄尚待使用者決定的唯一
   套用語意。
3. 不產生未授權的 production code；文件、`main` 推送與相關 GitHub Issue 回寫完成。

## 退出條件

- 若前端能力存在與既有 prototype 或規格矛盾，保留衝突證據並回到 DRAFT，不以推測拼接實作。
- 若後續設計需要決定玩家操作手感，停在共同決策前沿；可繼續的證據蒐集不因而停止。

## 完成收據

- 固定 dosgolem 本機 revision `8bfd5b4e5802f65d428d3fb439196b3c571c002b`，確認其是無頭觀測器；
  在已盤點的程式與依賴中未發現可重用視窗或 host pointer event loop。
- 已區分可重用的 xlate／RGBA compositing 與必須新增的通用 host presenter、pointer router、
  chrome layout；DOS 模擬滑鼠不會被拿來當 host UI。
- 相關 Go 套件在 Docker 的 Go 1.24.13 通過，並已建立不預設點選套用語意的 DRAFT spec 004。
