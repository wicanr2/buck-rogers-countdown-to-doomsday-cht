# 第七十九階段：技能操作列配色中立 runtime 生命週期

狀態：完成

## 目標

將 Phase 78 的配色中立 stamp builder 包成 presentation-only runtime owner，驗證 normal／focus
同原點取代、局部／全域 clear、畫面 anchor 轉換與 frame 定色失效。constructor 必須由 caller
注入 normal 配色策略，沒有預設值；本階段不接正式 CLI，因此不替使用者決定產品配色。

## 範圍

- 建立 `RuntimeActionBarOverlay`，持有 action request catalog、exact rectangles、font、scale、
  caller-supplied normal style 與自己的 `xlate.Layer`。
- `Apply(ActionBarEvent, DisplayRequest, palette)` 必須重驗 exact identity，將同一 action 的舊
  normal／focus stamp group 原子取代，不影響同畫面其他 action。
- `ClearTextCells` 套用已證實的 `026F:029C` inclusive cell rectangle；相交 action group 整組清除。
- `ObserveAnchorEvent` 沿用 Phase 75 exact screen anchor／撤銷規則；離開技能頁即清除全部 action stamps。
- `Frame`／`Draw`／`ActiveKeys`／content-safe actions 供後續 CLI 接線使用，不暴露譯文正文。

## 不在本階段

- 不選 normal 配色，不提供 constructor 預設值，不把任一候選寫入 production CLI。
- 不升級 spec 215 為 READY，不產生正式正常玩家路徑 overlay 收據。
- 不修改原版 VRAM／framebuffer、輸入、技能點、焦點、存檔、disabled、產品預設倍率或手冊版面。

## 完成條件

1. 兩種候選 normal style 都通過相同 lifecycle 測試；nil／錯誤 style 在 constructor 或 Apply 拒絕。
2. normal→focus→normal 同 action 始終只有一組 active stamps；其他 action 保留。
3. clear、unrelated anchor 與 career↔technical anchor 切換依 exact 規則整組失效，無半個多色 stamp。
4. 2×／3× `Frame`／`Draw` 通過，缺字、identity drift、非法 clear 失敗即關閉。
5. 專案與 dosgolem 測試通過；專案 `main` 推送並更新相關 GitHub Issues。

## 退出條件

- 若原子 group lifecycle 需要修改通用 `xlate.Layer` 語意，先停下來補通用規格，不以 action 專屬
  hack 污染 engine。
- 若 exact anchor 無法證明離開／切換失效，維持 DRAFT 並只保留純核心，不用 timeout 猜測。

## 完成收據

- 兩候選 normal style 與 2×／3× 均通過 constructor、Apply、Frame 與 Draw 測試，沒有預設值。
- normal／focus 原子取代、partial clear 整組移除、screen anchor 切換與 shared-key 保留均通過。
- dosgolem 正式 package test、vet 及 Buck Rogers race 通過；既有 workplace probes 的全域 vet
  掃描衝突已記錄，未刪改其他研究資料。
- dosgolem 本機提交 `6d230a1`；spec 215 仍為 DRAFT，正式 CLI 等待使用者選擇 normal 配色。
