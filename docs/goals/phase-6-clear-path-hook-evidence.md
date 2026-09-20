# 第六階段目標：清除路徑與失效 hook 證據

狀態：已完成（底層 fill 已排除；矩形清除 hook 候選與下一缺口已證實）  
日期：2026-09-20  
前置：[第五階段種族選擇返回生命週期](phase-5-pick-race-return-lifecycle.md)  
工作追蹤：[GitHub Issue #3](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/3)、[#4](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/4)

## 本輪開工讀取紀錄

本檔建立後必須讀回才可開工。本輪沿用已確認方向與工具配置：僅做 dosgolem 執行期輸出端
繁體中文化；使用被忽略的 `workplace/dosgolem/` 分支 `buck-rogers-cht-output-overlay`，不直接
修改原始 dosgolem 目錄，也不變更原版 EXE、資料、規則、手冊驗證或存檔語意。

## 目標

針對 Enter 向前與 Escape 返回兩條正常路徑都觀測到的 dosgolem 執行期寫入點
`0CF4:1B3C`，建立函式邊界、caller、原始指令與 VRAM 清除範圍的最小充分證據，判斷它是否
能支撐正式 overlay generation／invalidation hook。結果先回填研究文件與 DRAFT，不直接進入
production adapter。

## 成功定義

1. 從固定狀態重播至少一條既有正常轉場，於 `0CF4:1B3C` 保存暫存器、堆疊／控制流鄰域、
   執行期 segment bytes 與輸入／工具版本；所有位址明示為 dosgolem 實模式段:位移。
2. 由原始 bytes 與動態控制流辨識包含該寫入的最小函式或迴圈邊界、直接 caller／返回位置；
   無法證實的名稱只作假說，不覆蓋原始定位。
3. 量測該路徑在清除期間實際寫入的 VRAM 位址集合或界限，區分「單像素寫入端」、
   「矩形清除 primitive」與「上層畫面失效事件」；不得由兩個樣本像素直接外推全畫面。
4. 依證據更新 `docs/re/`、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；若正式 hook 仍缺條件，
   列出下一個最小缺口。完成後驗證 Docker 衛生、推送 `main` 並更新相關遠端 Issue。

## 不屬於本階段

- 不建立或啟用 `apps/buckrogers/` production hook，不繪製中文。
- 不以函式改名、單一像素、靜態反組譯或 DOSBox 圖片單獨宣稱通用清除語意。
- 不深挖與玩家可見覆繪失效無關的圖形 driver、硬體逐週期行為或完整 executable。

## 退出條件

成功定義均有可重生的 dosgolem 收據與推論等級文件支持時結束。若 `0CF4:1B3C` 只證實為
底層像素／byte primitive，必須明確否決把它當正式 invalidation hook，並把下一個上層事件
缺口留在 DRAFT；不得為了升格 READY 而擴張結論。

## 完成收據

[清除路徑與失效 hook 證據](../re/phase-6-clear-path-hook-evidence.md)保存 watchpoint IP
勘誤、IDA 9.4 非破壞性資料庫、`0CF4:1B2B` byte-fill、`026F:029C` Mode 13h 矩形公式，
以及 Enter／Escape 兩條正常路徑的動態首末列與呼叫數。
