# 第七十八階段：技能操作列配色中立覆繪核心

日期：2026-09-21

## 結論

操作列 exact geometry 與覆繪建構已能在不選 normal production 配色下獨立驗證。正式
`skill-action-bar-text-safe-rects.tsv` 包含 16 個 normal／focus event keys；同一 action 的 variant
共享矩形，跨 action 不重疊，全部固定在已證實的 `y=192..200`。

dosgolem `BuildActionBarOverlay` 沒有 normal 預設值。normal caller 必須為譯文每個 rune 明示
palette 10 或 15；缺少、數量不符或其他色號均失敗。focus 不接受 normal style，固定使用原版
已證實的 palette 15 背景與 palette 0 前景。譯文、幾何及 event identity 仍由 Phase 74–76 正式
catalog 驗證，核心不接觸 machine、VRAM、輸入、規則或存檔。

## 驗證

- Python verifier 固定 16 identities、exact geometry、capacity、variant 一致及同畫面重疊規則；
  5 個負向測試涵蓋幾何、缺少／孤兒、容量與跨 action 重疊。
- 首字白／次字綠 `[15,10]` 與全綠 `[10,10]` 都由同一 API 在 2×／3× 通過 ink containment；
  只證明技術可行，不代表選定任何一種。
- 專案完整 149 項 Python 測試通過；dosgolem 完整 test、vet 與 Buck Rogers race detector 通過。
- spec 215 仍為 DRAFT；CLI／runtime presenter 未接線，需使用者確認 normal 配色後才可審查 READY。

dosgolem 本機分支提交為 `236cb3b`，依專案規範未推送遠端。
