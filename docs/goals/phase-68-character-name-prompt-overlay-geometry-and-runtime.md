# 第六十八階段：角色姓名提示安全矩形與雙倍率執行期覆繪

狀態：已完成

## 目標

以第六十七階段已 CONFORMED 的姓名提示 exact request 為唯一文字來源，從正常玩家路徑的
原版 framebuffer 與後續輸入生命週期量出安全矩形，建立失敗即關閉的 rectangle catalog，
並在 dosgolem 既有長存 overlay 中完成明示 2×／3× 的繁中像素覆繪。

## 範圍

- 由修正後固定 state 重生未輸入姓名與輸入 `A` 的正常路徑 framebuffer，量測提示列的原版
  字墨、動態輸入起點、畫面邊界及可清除區域。
- 建立一筆 `character.name.prompt` text-safe rectangle；驗證繁中「角色姓名：」在 16×16
  字型、2×／3× 輸出下完整 containment，且不覆蓋玩家輸入欄。
- 將 rectangle catalog 成對接入既有 `RuntimeMenuOverlay`；catalog request 沒有 rectangle、
  rectangle 沒有 request、字型缺字或非法倍率都必須失敗。
- 對未輸入與輸入 `A` 路徑各做 baseline、2×、3× 同狀態驗證；原版 indexed framebuffer、
  events、BIOS keys 與動態姓名語意不得改變。

## 不在本階段

- 不翻譯玩家輸入，不改姓名長度、按鍵、Backspace、Enter、Escape、存檔或角色資料。
- 不選定產品預設倍率；2×／3× 都只由明示旗標啟用。
- 不處理手冊版面、手冊題目或其他姓名確認後畫面。

## 完成條件

1. 安全矩形有原版像素與動態輸入邊界證據，不以目測猜座標。
2. 正式 rectangle catalog、驗證器與 Go 正反例涵蓋 containment、孤兒 key、缺表及配對錯誤。
3. base 與輸入 `A` 在 2×／3× 各雙重重播決定性一致；矩形外零差異，輸入 `A` 像素不被覆蓋。
4. 無覆繪 baseline 與覆繪模式的原版 framebuffer、事件與輸入相同。
5. 專案回歸、dosgolem 正式測試／vet／相關 race detector 通過；dosgolem 只提交本機 branch，
   專案 `main` 推送並更新相關 Issues。

## 退出條件

- 若繁中提示無法在不遮住輸入欄的單列矩形內完整顯示，規格退回 DRAFT，不縮字、不截斷、
  不移動玩家輸入；先提出可丟棄版面對照再請使用者決定。
- 若後續輸入或清除會讓 overlay 殘字，先補足已證實的失效事件；不得以 event key 特例清畫面。
- 若兩倍率的同一邏輯矩形不能保持相同語意，停止 production 接線並保留差異證據。

## 完成摘要

- 已證實提示矩形為 `[0,128)×[192,200)`，玩家輸入從 x=136 開始；正式資料閘門禁止矩形
  侵入輸入欄。
- base／輸入 `A` 的 2×／3× 各雙重重播一致；2×／3× 差異分別為 941／2,038 pixels，
  矩形外及玩家輸入欄皆為 0。
- catalog／rectangle 已雙向集合驗證；缺少或孤兒 rectangle 都失敗即關閉。
- 原始解析度實圖已確認繁中提示完整且 `A` 保持可見。本階段仍未選定產品預設倍率或手冊
  版面。
