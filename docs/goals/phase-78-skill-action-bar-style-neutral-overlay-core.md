# 第七十八階段：技能操作列配色中立覆繪核心

狀態：完成

## 目標

在 Phase 77 normal 配色尚待使用者確認時，完成不依賴該選擇的安全矩形資料、失敗即關閉驗證
與 dosgolem 覆繪核心。核心必須明示接收配色策略，不能內建或默認「首字白／次字綠」或
「全綠」；因此不會越過共同決策閘門，也不會接上 production CLI。

## 範圍

- 建立 16 筆 normal／focus exact event key 的正式安全矩形 TSV；相同配置的兩個 variant 共用
  x／y／width／height，但保持獨立 key。
- 以 Phase 74 事件清冊及 Phase 76 譯文雙向驗證 schema、幾何、容量、重疊群組與 coverage。
- 在 dosgolem 建立 action-bar 專用 rectangle loader／coverage validator。
- 建立 style-neutral overlay builder：focus 固定使用已證實黑字白底；normal 必須由 caller 明示
  提供「每 rune 的前景色」，缺少、過多或非法策略皆拒絕。
- 純核心測試同時驗證兩個候選 normal 策略，證明架構不偏向任一選項。

## 不在本階段

- 不選擇 normal production 配色，不修改 spec 215 的 DRAFT 狀態。
- 不將 action request 接入 `buckrogers-text-receipt` runtime presenter，不產生正式 overlay 收據。
- 不修改原版 framebuffer、輸入、技能點、焦點、存檔、disabled 行為、產品預設倍率或手冊版面。

## 完成條件

1. 正式 TSV 與事件／譯文雙向覆蓋，16 identities 幾何固定且只有同配置 variant 可重合。
2. Python verifier 及負向測試拒絕缺少、孤兒、重複、漂移、跨配置重疊與容量不足。
3. dosgolem loader、coverage 及 style-neutral builder 測試覆蓋 2×／3× containment、缺字與策略錯誤。
4. 兩種候選 normal 配色都能由同一 API 建出合法 stamp，但沒有 production 預設值。
5. 專案與 dosgolem 測試通過；專案 `main` 推送並更新相關 GitHub Issues。

## 退出條件

- 若核心無法在不選配色的前提下保持 typed API，停止實作並等待使用者，不以隱性預設繞過。
- 若正式矩形需要超出 Phase 77 已證實的 exact band，退回 DRAFT 幾何研究，不擴張安全區。

## 完成收據

- 16 筆正式 exact rectangles 與事件／譯文雙向驗證完成，5 個負向案例通過。
- style-neutral builder 在 2×／3× 同時接受 `[15,10]` 與 `[10,10]`，但 normal 缺少明示策略即拒絕。
- 專案 149 項 Python 測試與 dosgolem 完整 test／vet／Buck Rogers race 通過。
- dosgolem 本機提交 `236cb3b`；spec 215 保持 DRAFT，production 配色與 CLI 接線仍等待使用者。
