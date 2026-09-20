# 第九階段目標：dosgolem 通用繁中覆繪基礎

狀態：已完成（dosgolem 遠端推送待明確授權）  
日期：2026-09-20  
前置：[第八階段功能選單繁中字型與版面 prototype](phase-8-menu-cht-font-layout-prototype.md)  
工作追蹤：[GitHub Issue #5](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/5)、
[#7](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/7)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可修改 `workplace/dosgolem`。本階段只建立與遊戲無關、且不依賴
2×／3×產品決策的 `xlate` 基礎；不接 Buck Rogers 位址、不建立正式 adapter、不改原版
EXE／資料／規則／存檔，也不把 psychic-war 的遊戲專屬內容帶入。

## 目標

在 `workplace/dosgolem/` 的 `buck-rogers-cht-output-overlay` 分支，從 psychic-war 已驗證的
dosgolem 工作樹移植通用 `xlate` package 與其規格／測試。逐檔核對來源與目前 dosgolem API，
保存來源 commit／差異；以 Docker 執行 package 測試與全儲存庫測試，確認沒有先把倍率、
字型或本作 hook 寫死。

## 成功定義

1. 完整讀取本機 dosgolem 的 README、CLAUDE、spec index／scope，以及來源 `xlate` 規格與
   全部 package 檔案；確認來源與目標 commit／branch。
2. 移植的通用層至少涵蓋 GOLEMFNT 載入、排版、stamp、定色、逐格／錨定格失效、捲動、
   snapshot／restore、透明格、`GlyphScale` 與 `LineTracker`；不含遊戲位址或譯文。
3. Docker 內執行 `go test ./xlate` 與 `go test ./...`；若既有非本輪失敗存在，保存精確分類，
   不把它冒稱本輪通過。
4. 在 workplace dosgolem 分支建立可追溯 commit；若遠端允許，推送該專用 branch。專案主 repo
   只保存來源、驗證與 commit 指標，不納入 dosgolem 的重複程式碼。
5. 更新 DRAFT、研究文件、`CONTEXT.md`、`WORKLOG.md` 與索引；完成 Docker／擁有權稽核，
   推送專案 `main` 並更新相關 Issues。

## 不屬於本階段

- 不選擇 2× 或 3×；不把任一 prototype 固化成正式玩家體驗。
- 不建立 `apps/buckrogers` production adapter，不升級 READY／CONFORMED。
- 不複製 psychic-war 的遊戲位址、狀態、譯文、倚天字模或完成聲明。
- 不建立 Release、發行包或加入原版／手冊素材。

## 退出條件

通用 `xlate` 在專用 dosgolem 分支可由測試重生，來源與差異可追溯，且專案文件明確記錄
它只解鎖下一階段的遊戲專屬 disposable adapter；未選倍率不阻礙本階段完成。

## 完成摘要

已把來源 commit `e515870` 的通用 `xlate` 最終狀態逐檔移植至本機 dosgolem 專用分支，
建立 commit `b33cfbf`；`xlate` 與全部正式 packages 均在 Docker 通過。來源的 3 倍倍率
限制已明列，沒有替使用者選定方案。遠端 dosgolem 推送因缺少明確外傳授權而未執行成功，
本機 commit 保留；專案主 repo 照常推送。
