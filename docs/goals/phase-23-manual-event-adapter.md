# 第 23 階段：手冊事件 adapter 規格與正式核心

## 狀態

完成

## 本輪目標

將已由第 18–21 階段證據驗證的「手冊題目 generation、欄位收集、序數橋接與 catalog
唯一命中」切成不含版面倍率的獨立規格；完成證據審查並達 READY 後，才在 workplace
dosgolem 的 `apps/buckrogers` 實作可測試、尚未接入執行器 hook 的正式核心。

## 範圍

- 回讀 GitHub Issues #6、#8 的遠端權威狀態與現有 DRAFT 規格。
- 建立獨立 adapter 規格，記錄 typed inputs、狀態轉移、輸出、失敗模式、位址空間、證據等級、
  測試矩陣、權利邊界及停止線。
- 只有證據審查確認該獨立範圍達 READY 後，才新增 `apps/buckrogers` 的純狀態核心。
- 將第 19、20 階段 prototype 的同世代、跨世代、亂序、重複、未知 caller、poisoned 復原、
  catalog 未命中與 ordinal 未命中案例轉為正式 Go 測試。
- 在 dosgolem 工作分支建立本機 commit；未獲額外授權前不推送 dosgolem 遠端。

## 不在本輪範圍

- 不選定 2× 或 3×，也不改任何版面、分頁或字型設定。
- 不把 adapter 接到 `oracle.OnCall`、renderer 或正式玩家路徑。
- 不送鍵、不自動作答、不讀取或輸出答案、不改寫 DOS 記憶體與原版返回值。
- 不把仍為 DRAFT 的完整手冊覆繪規格宣稱為 READY／CONFORMED。

## 驗收條件

- 獨立規格在 READY 前具備完整證據、typed transition、失敗即關閉規則與測試矩陣。
- 正式 Go 核心只接受已證實事件與精確 TSV 資料，輸出不含答案、輸入或 renderer 狀態。
- 正反向測試覆蓋第 19、20 階段既有案例，且所有 dosgolem 正式 packages 通過。
- workplace dosgolem 工作樹乾淨並有本機 commit；不推送其遠端。
- 專案測試、資料重生與文件索引通過；Docker 與擁有權檢查完成。
- 推送專案 `main`，更新 GitHub Issues #6 與 #8。

## 預定交付物

- workplace dosgolem `docs/spec/007-buck-rogers-manual-event-adapter.md`（唯一實作權威）
- `docs/spec/003-manual-event-adapter.md`（產品整合邊界與權威規格指標）
- workplace dosgolem `apps/buckrogers` 程式、測試與本機 commit
- `docs/re/phase-23-manual-event-adapter.md`
- `CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

- dosgolem READY 規格與 `apps/buckrogers` 純核心已完成，本機 commit：
  `8ce092f29d000ea7e6765c4f3389fe484aefa555`。
- 正式 TSV、正反向狀態機、`go vet`、race detector 與全部正式 packages 通過。
- 未推送 dosgolem 遠端；未接 runtime hook／renderer，也未選定 2×／3×。
