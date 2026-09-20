# 第十二階段目標：手冊題庫結構與可抽題清冊

狀態：完成  
日期：2026-09-20  
前置：[第十一階段手冊事件映射](phase-11-first-manual-check-event-map.md)  
工作追蹤：[GitHub Issue #6](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/6)、
[#8](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/8)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可搜尋原版題庫、轉換資料或擴充中文映射。本輪已重新
載入專案規則、復古遊戲路由、`reverse-engineer-retro-game-remake` 技能與規格閘門契約。
上一階段已證實單一題目及錯答重抽；本輪要建立可抽題的結構性清冊，不以反覆重擲代替
原始資料證據。

## 目標

從原版 `START.EXE` 或其執行期搬移資料中，找出手冊驗證題庫的紀錄邊界、欄位與選題消費者，
產生只含頁碼、標題、序數與證據定位的可重生清冊。中文掃描只做標題／條目對應；不把英文答案表建成
自動作答功能，不改原版題目抽選與判定。

## 成功定義

1. 重新核對 `START.EXE` 輸入檔名、SHA-256、工具版本與靜態／執行期位址空間。
2. 找出題庫記錄的起迄、紀錄數與 typed schema；對每個欄位保留原始 bytes／offset 與推論等級。
3. 找出至少一個選題消費者或執行期索引，並以第十一階段的兩個實際題目反向驗證清冊。
4. 產生可重生的 metadata 清冊；Git 內不保存手冊全文、整頁 OCR、掃描或可供自動通關的答案輸入表。
5. 對可明確配對的中文條目建立來源 metadata；無法唯一配對者標為未知，不用模糊命中猜補。
6. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；測試與 Docker／擁有權稽核後
   推送 `main`，並更新 GitHub Issues #6、#8。

## 不屬於本階段

- 不實作 production 手冊覆繪 adapter、不升級 READY／CONFORMED。
- 不顯示或自動填入英文答案，不繞過手冊驗證。
- 不決定 2×／3× 輸出倍率、正式字型或分頁視覺。
- 不把靜態字串鄰近關係單獨當成記錄 schema 或可抽題完整性證據。

## 退出條件

題庫的紀錄邊界、typed schema、消費者與可抽題清冊已有可回查的原始資料證據，且至少以
`Deimos Prison` 與 `Technical Skills` 兩個實際抽題驗證；中文對應與未知均有明確來源與等級。

## 完成收據

- 已證實 `0EC0:00C2..0553` 共 39 筆、每筆 30 bytes，並記錄欄位、解碼公式、原始位址、
  bytes 與推論等級。
- `tools/manual_questions.py` 只匯出頁碼、標題、序數及來源 offset；答案欄只檢查容量，
  不解碼、不輸出。
- 5 項單元測試通過；以真實執行期資料重生的 TSV 與 `text/manual-questions.tsv` 逐位元一致。
- 第 32、38 筆分別與正常玩家路徑的 `Deimos Prison`、`Technical Skills` 動態抽題一致。
- 中文來源僅 `Deimos Prison` 唯一確認；其餘明記未知，未以模糊比對猜補。
