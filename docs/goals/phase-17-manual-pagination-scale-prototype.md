# 第十七階段目標：手冊查詢分頁與倍率對照 prototype

狀態：完成  
日期：2026-09-20  
前置：[第十六階段第三批手冊段落](phase-16-manual-compact-paragraphs-3.md)  
工作追蹤：[GitHub Issue #6](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/6)、
[#8](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/8)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回，才可量測畫面、撰寫 prototype 或產生對照圖。本輪已重新載入
專案規則、復古遊戲路由、`reverse-engineer-retro-game-remake` 技能、規格閘門與
`grilling` 共同決策技能。依共同決策規則，只做可丟棄對照，不替使用者決定 2×／3×。

## 目標

從 dosgolem 的真實手冊查詢畫面收據量出文字安全矩形，使用既有已校訂段落建立 2× 與
3× 的可丟棄分頁 prototype。兩種方案必須共用相同文字、邊界與分頁規則，產生可目視比較
的畫面與容量資料，作為後續倍率決策的證據。

## 成功定義

1. 回查手冊查詢畫面的 dosgolem 原始收據，記錄畫面雜湊、尺寸及安全矩形來源；不得憑
   其他遊戲或人工想像座標。
2. prototype 只放在被忽略的 `workplace/`，不得成為 production adapter、正式資料格式或
   READY 規格。
3. 2×／3× 使用同一段正式繁中內容，具有確定的字寬、行高、內距、每頁行數、換行及
   最後頁規則；兩者都不得越出安全矩形。
4. 產生各倍率的逐頁圖片、頁數／容量／剩餘空間報告及可重生命令，並逐張目視檢查。
5. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；Docker 測試及衛生稽核後
   推送 `main`，更新 GitHub Issues #6、#8，再提出一個有證據的倍率決策問題。

## 不屬於本階段

- 不把 prototype 接入正式 dosgolem 執行路徑，不升級 READY／CONFORMED。
- 不決定 2×／3×，也不把 agent 建議寫成使用者決策。
- 不改原版題目、答案輸入、錯答重抽、generation 失效或存檔語意。
- 不建立長章節／表格的正式 schema；它們須等倍率與分頁互動定案後另行處理。

## 退出條件

真實畫面安全矩形有可回查證據，2×／3× 對照均可重生、無越界且已目視檢查；永久文件只
記錄事實、限制與待決選項，不把任一倍率升格為正式方案。

## 完成收據

- 真實 VRAM 證實安全矩形為 `[7,312)×[7,184)`；共同正文格線為 36×17、每頁 612 字。
- 正式 236 字段落在兩案均為 7 行／1 頁；708 字明示壓力樣本均為 20 行／2 頁。
- 六張逐頁圖片已目視檢查；每張安全矩形外變更均為 0 px，輸入、工具與輸出 SHA-256
  已記錄於研究收據。
- 已揭露 2× 需擴充 `xlate.Draw`、3× 字體相對較小，以及 ASCII 每字一格的共同限制；
  沒有替使用者作倍率決策。
