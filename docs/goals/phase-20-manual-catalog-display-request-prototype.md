# 第 20 階段：手冊 catalog 顯示請求 prototype

## 狀態

完成

## 本輪目標

把第十九階段的完整題目鍵接到現有 UTF-8 TSV 事件與繁中 catalog，建立可丟棄的顯示請求
prototype；證明只有精確、唯一且已校訂的命中才能輸出繁中段落，未命中與資料異常均不猜補。

## 範圍

- 讀取正式 `text/manual-events.tsv` 與 `text/manual.zh-TW.tsv`，不把譯文複製進程式碼。
- 以 `(page, heading, ordinal)` 精確查找事件，再以穩定文字鍵取得繁中段落。
- 將題目鍵、generation、文字鍵與繁中段落組成只供顯示端使用的 typed request。
- 驗證已收錄題目唯一命中，以及未收錄題目失敗即關閉。
- 驗證重複事件鍵、孤兒文字、重複文字鍵、無效 UTF-8 與跨 generation 請求均被拒絕。
- prototype 與測試只留在被 Git 忽略的 `workplace/phase20/`。

## 不在本輪範圍

- 不選擇 2× 或 3×。
- 不接入 dosgolem 正式 runtime，也不繪製畫面。
- 不修改原版輸入、答案檢查、題庫或存檔。
- 不將 catalog 譯文內嵌於正式程式碼。
- 不把未校訂或未收錄來源自動降級為模糊命中。

## 驗收條件

- 至少一筆第十九階段可表達的題目鍵能從正式 TSV 產生唯一繁中顯示請求。
- 至少一筆未收錄題目明確回傳不顯示，而非猜測相近標題或頁碼。
- 正反向測試涵蓋唯一性、孤兒、UTF-8、generation 與顯示／語意隔離。
- 專案測試與 dosgolem 正式 packages 測試通過。
- 完成 Docker 容器、擁有權與工作樹檢查。
- 推送 `main`，並更新 GitHub Issues #6 與 #8。

## 預定交付物

- `docs/re/phase-20-manual-catalog-display-request-prototype.md`
- `docs/spec/002-manual-paragraph-overlay-draft.md` 的 catalog lookup 契約增補
- `CONTEXT.md`、`WORKLOG.md` 與相關索引更新

## 完成紀錄

2026-09-20 完成。正式 TSV 的已收錄題目可產生唯一繁中顯示請求；未收錄題目與 12 類正反向
條件均依契約處理。另定位完整 ordinal bridge 缺口，規格維持 DRAFT，prototype 未進 production。
