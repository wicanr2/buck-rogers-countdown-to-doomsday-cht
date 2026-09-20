# 第 21 階段：手冊序數詞橋接證據

## 狀態

完成

## 本輪目標

以 dosgolem 動態記憶體與 IDA Pro 9.4 為主，找出原版將題庫數字序數轉成可見英文序數詞的
資料或控制流，建立可回查的 ordinal word→number 橋接，補足第二十階段定位的 READY 缺口。

## 範圍

- 回讀第十二、十八與二十階段既有題庫、consumer 與動態事件證據。
- 在原版執行期記憶體或 overlay 中定位序數詞資料與 `2A33:02E2` 的來源鏈。
- 以 IDA Pro 9.4 保存原始位址、bytes、operand 與交叉參照；語意另列推論等級。
- 只登記由原版 bytes、consumer 或動態輸出支持的對照。
- 若只需 1–10 的有限表即可涵蓋 39 筆題庫，驗證表邊界與所有現有 catalog ordinal。
- 建立可版本控制的 ordinal bridge 資料與失敗即關閉驗證器，前提是證據足夠。

## 不在本輪範圍

- 不選擇 2× 或 3×。
- 不修改原版亂數、題庫、答案或玩家輸入。
- 不逐行反組譯無關的 overlay 程式。
- 不以一般英文常識或 LLM 生成內容取代原版證據。
- 不接入正式 dosgolem runtime renderer。

## 驗收條件

- 證據能說明序數詞表的原始位置、格式、索引 consumer 與位址空間，或誠實記錄仍未知。
- 每筆加入 bridge 的對照都有原版資料與至少一個 consumer／動態錨點支持。
- 現有 22 筆 catalog 所需 ordinal 全數可橋接；否則明列仍未涵蓋值並維持失敗即關閉。
- 新資料與驗證器通過正反向測試，且不包含答案。
- 專案測試與 dosgolem 正式 packages 測試通過。
- 完成 Docker 容器、擁有權與工作樹檢查。
- 推送 `main`，並更新 GitHub Issues #6 與 #8。

## 預定交付物

- `docs/re/phase-21-manual-ordinal-bridge-evidence.md`
- 證據足夠時新增 `text/manual-ordinals.tsv` 與驗證器／測試
- `docs/spec/002-manual-paragraph-overlay-draft.md`、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

2026-09-20 完成。IDA Pro 9.4 與 dosgolem runtime dumps 證實 1–10 序數表及其 consumer；
已建立可重生 TSV、7 項測試，且現有 22 筆 catalog 所需 ordinal 全數涵蓋。正式 adapter
與 renderer 仍受 DRAFT spec 及倍率決策約束。
