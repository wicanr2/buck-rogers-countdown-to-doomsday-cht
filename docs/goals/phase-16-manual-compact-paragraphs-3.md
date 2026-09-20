# 第十六階段目標：第三批已證實繁中手冊段落校訂

狀態：完成  
日期：2026-09-20  
前置：[第十五階段第二批短篇段落](phase-15-manual-compact-paragraphs-2.md)  
工作追蹤：[GitHub Issue #6](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/6)、
[#8](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/8)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回，才可盤點候選、裁切掃描、校字或修改 catalog。本輪已重新載入
專案規則、復古遊戲路由、`reverse-engineer-retro-game-remake` 技能、規格閘門，以及
dosgolem 的能力與專案規範入口。

## 目標

從尚未映射且來源狀態為 `confirmed` 的手冊題目中，選取最多八筆可由單一連續段落完整
表示的內容，以原始掃描逐字校訂繁中內容，加入事件表與 catalog。選取結果必須由目前
題庫、來源對照、既有事件表及原圖共同證明，不預先假定標題或頁型。

## 成功定義

1. 以題庫、來源對照與既有事件表產生尚未映射候選清單，只接受 `confirmed` 來源。
2. 對每個入選項目由原始掃描重生校字裁切、記錄 SHA-256，並逐張目視核對標題與完整段落。
3. 每筆 `event_key → text_key` 與原版 record、頁碼、標題、序數完全一致；事件與 catalog
   一對一、無孤兒鍵，既有 17 筆不退化。
4. 若某項實際為長章節、表格、跨頁或無法由單一段落完整表示，必須排除並記錄原因，不得
   為湊數截斷內容。
5. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；Docker 測試及衛生稽核後
   推送 `main`，並更新 GitHub Issues #6、#8。

## 不屬於本階段

- 不實作 production dosgolem 覆繪，不升級 READY／CONFORMED。
- 不決定 2×／3×、正式分頁或玩家介面。
- 不納入 `strong-inference`、`unknown`、缺頁、表格或跨頁內容。
- 不解碼、保存、顯示或自動輸入英文答案。

## 退出條件

最多八筆符合條件的候選完成原圖校訂、精確事件映射、來源與 catalog 驗證；若不足八筆，
研究收據須逐項說明排除理由。正式資料仍不含 OCR 誤字、答案、未證實來源或截斷段落。

## 完成收據

- 18 筆尚未映射的 confirmed 候選中，5 筆符合內容完整、非表格且非跨頁的範圍，均完成
  原圖校訂、裁切 SHA-256 與精確事件映射。
- 其餘 13 筆已逐項記錄長章節、跨頁、清單或表格排除理由，沒有為湊足八筆截斷內容。
- 事件與 catalog 由 17 筆增至 22 筆；新增內容長度為 35–190 Unicode 字元。
- 19 項測試、catalog lint 與真實題庫／來源／事件／文字交叉驗證通過。
