# 第十三階段目標：39 筆手冊題目與繁中來源對照

狀態：完成  
日期：2026-09-20  
前置：[第十二階段題庫清冊](phase-12-manual-question-table-inventory.md)  
工作追蹤：[GitHub Issue #6](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/6)、
[#8](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/8)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可開始 OCR、掃描檢視或來源配對。本輪已重新載入專案規則、
復古遊戲路由、`reverse-engineer-retro-game-remake` 技能與規格閘門契約。第十二階段的
39 筆英文 metadata 是題庫權威清冊；中文掃描的頁面內容必須逐筆以可回查來源驗證。

## 目標

依 `text/manual-questions.tsv` 的 39 筆頁碼／標題／序數，建立繁中手冊來源對照。優先利用
掃描頁碼、目錄、條目編號與實際中文段落交叉核對；OCR 只作搜尋線索，不能單獨把相似文字
升格為唯一映射。成果應讓 dosgolem 日後能依原版題目鍵精確選出相符中文段落，同時不保存
英文答案、不自動作答、不修改原版驗證。

## 成功定義

1. 核對中文手冊 archive-order／檔名／印刷頁碼的頁面範圍及輸入雜湊，保留 OCR 工具版本。
2. 為 39 筆題目逐筆記錄 `confirmed`、`strong-inference` 或 `unknown`，並附可回查掃描定位；
   不以空白或未檢查狀態冒充 unknown。
3. 至少以已知 `Deimos Prison` 與第二個不同類型題目驗證配對方法；若中文手冊欠頁或
   原版頁碼對應不同冊別，必須明確記錄邊界。
4. 只有唯一確認的中文段落才可加入 `text/manual.zh-TW.tsv`；每筆保持來源 metadata，
   不納入整頁 OCR、原始掃描、英文答案或可自動通關資料。
5. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；在 Docker 內驗證 catalog、
   擁有權及容器清理後，推送 `main` 並更新 GitHub Issues #6、#8。

## 不屬於本階段

- 不實作 production 手冊覆繪 adapter，不升級 READY／CONFORMED。
- 不決定 2×／3× 倍率、正式字型、中文分頁或視覺樣式。
- 不翻譯中文手冊未提供的段落，不用英文原文自行補譯取代來源。
- 不解碼、顯示、保存或輸入原版答案欄。

## 退出條件

39 筆清冊每筆都有經實際檢查的來源狀態與定位；所有宣稱唯一確認的中文段落能回查掃描，
catalog 可被既有 lint 驗證，未解項目與手冊素材邊界明確且沒有猜補。

## 完成收據

- 39 筆均已實際檢查：35 筆 `confirmed`、3 筆 `strong-inference`、1 筆 `unknown`。
- 逐筆掃描 SHA-256 與既有解壓 manifest 一致；`Roll.` 因掃描只到印刷頁 87 而明記缺頁。
- `Deimos Prison` 旅程條目及 `Technical Skills` 附錄表格兩種頁型均完成回查。
- OCR JSON 只留在被忽略的 `workplace/`；未經逐字校訂的內容未加入中文 catalog。
- 9 項題庫／對照測試、實際 manifest 驗證與現有中文 catalog lint 全數通過。
