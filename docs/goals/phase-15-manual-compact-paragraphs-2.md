# 第十五階段目標：第二批短篇繁中手冊段落校訂

狀態：完成  
日期：2026-09-20  
前置：[第十四階段首批短篇段落](phase-14-manual-compact-paragraphs.md)  
工作追蹤：[GitHub Issue #6](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/6)、
[#8](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/8)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可裁切掃描、校字或修改 catalog。本輪已重新載入專案規則、
復古遊戲路由、`reverse-engineer-retro-game-remake` 技能與規格閘門。沿用第十四階段的
事件／來源／catalog 驗證契約，不把 OCR 當作校訂文字。

## 目標

再選八筆來源為 `confirmed`、可由單一段落表示的題目：`Damage`、`Terrine`、
`Scot's Alarm`、`Meeting with Robot`、`Robot and Buck`、`Buck's Speech.`、
`Desert Ape Pilots`、`Talon's Speech`。從原圖校訂繁中內容，加入事件表與 catalog，
不處理答案、不改原版判定。

## 成功定義

1. 以原始掃描重生八張校字裁切並記錄 SHA-256，逐張目視核對標題與段落。
2. 八筆 `event_key → text_key` 與原版 record、頁碼、標題、序數完全一致，來源均為
   `confirmed`。
3. 新增繁中內容後，事件表與 catalog 一對一、無孤兒鍵，既有 9 筆不退化。
4. 記錄新增段落的字元數；不藉字數決定分頁、2×／3× 或 production 版面。
5. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；Docker 測試及衛生稽核後
   推送 `main`，並更新 GitHub Issues #6、#8。

## 不屬於本階段

- 不實作 production dosgolem 覆繪，不升級 READY／CONFORMED。
- 不處理長章節、表格、跨頁內容、`strong-inference` 或 `unknown`。
- 不解碼、保存、顯示或自動輸入英文答案。

## 退出條件

第二批八筆均完成原圖校訂、來源／事件／catalog 精確綁定與測試；正式資料仍不含 OCR 誤字、
答案或未決分頁格式。

## 完成收據

- 第二批八張半頁裁切由唯讀原圖在 Docker 內重生、逐張目視校訂並記錄 SHA-256。
- 事件表與 catalog 由 9 筆增至 17 筆；新增八筆均通過 confirmed 來源及題庫身分驗證。
- 新增內容長度為 31–216 Unicode 字元；未據此決定頁數、倍率或 production 版面。
- 19 項測試、catalog lint 與真實題庫／來源／事件／文字交叉驗證通過。
