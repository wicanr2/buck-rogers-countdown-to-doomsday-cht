# 第 19 階段：手冊題目事件收集器 prototype

## 狀態

完成

## 本輪目標

以第十八階段已證實的事件順序，建立可丟棄的手冊題目世代收集器 prototype；用真實 dosgolem
事件與合成反例驗證舊題失效、完整題目提交及失敗即關閉行為，不依賴尚未決定的 2×／3× 倍率。

## 範圍

- 定義題首、頁碼、標題、序數與題尾的 typed event。
- 題首事件開啟新 generation，立即丟棄舊題 metadata。
- 只有完整且順序正確的同世代事件可提交題目身分。
- 以第十八階段真實事件時間線驗證 `Technical Skills` 第 2 字。
- 驗證缺欄、順序錯誤、重複欄位、未知呼叫端及跨世代資料均不產生顯示請求。
- prototype 與測試只放在被 Git 忽略的 `workplace/phase19/`；正式契約只寫入研究文件與 DRAFT spec。

## 不在本輪範圍

- 不選擇 2× 或 3×。
- 不接入 dosgolem 正式執行路徑。
- 不繪製中文、不處理分頁輸入。
- 不自動回答手冊問題，不解碼或保存答案。
- 不把單一路徑外推為所有版本或所有手冊入口均已證實。

## 驗收條件

- prototype 可由第十八階段收據重建唯一題目鍵，並留下決定性輸出。
- 至少涵蓋缺欄、亂序、重複、跨世代及未知事件的負向測試。
- 每項狀態轉移均可回指原版事件或明確標示為失敗即關閉設計。
- 專案測試與 dosgolem 正式 packages 測試通過。
- 完成 Docker 容器、擁有權與工作樹檢查。
- 推送 `main`，並更新 GitHub Issues #6 與 #8。

## 預定交付物

- `docs/re/phase-19-manual-event-collector-prototype.md`
- `docs/spec/002-manual-paragraph-overlay-draft.md` 的 typed lifecycle 增補
- `CONTEXT.md`、`WORKLOG.md` 與相關索引更新

## 完成紀錄

2026-09-20 完成。真實事件重建出唯一題目鍵，9 項正反向測試涵蓋既定失敗模式；typed
lifecycle 已增補至 DRAFT spec。prototype 仍留在被忽略的 workplace，未進 production。
