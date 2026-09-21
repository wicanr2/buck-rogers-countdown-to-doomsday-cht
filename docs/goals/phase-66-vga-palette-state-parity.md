# 第六十六階段：角色資料頁 VGA palette 狀態對拍與可讀性

狀態：已完成

## 目標

釐清第六十五階段終態 color index 15 在 dosgolem RGBA 呈黑、但 raw indexed framebuffer 仍含
動態值的原因；依 VGA DAC 公開契約與遊戲實際 I/O／savestate 證據，判定原版行為、state 保存
或 dosgolem 模擬缺口，必要時以 READY 規格修正 dosgolem，讓角色資料頁的原版動態值與繁中
靜態覆繪可同時正確顯示。

## 範圍

- 從權威 state 與正常四次 Enter 路徑輸出終態 256×RGB palette，固定 index 0、10、13、15 的
  值與 SHA-256；同時核對 phase 11 已保存 palette，但不假設兩個遊戲狀態必須相同。
- 盤點 dosgolem VGA DAC port `03C7`／`03C8`／`03C9` 實作、6-bit→8-bit 轉換與 savestate
  序列化／反序列化；平台語意依 VGA 規格，不從遊戲 executable 重新推導。
- 必要時以 content-safe I/O trace 回答遊戲何時、以何值寫入 palette index 15；只追遊戲選擇的
  register/value/call timing，不展開無關圖形 driver。
- 若證實 dosgolem 缺口，先建立 READY 規格與負向測試，再修正並重生第六十五階段全部
  base／`Y` × 2×／3× baseline、overlay 與 containment 收據。
- 若證實原版在此終態確實將 index 15 設黑，保留結果並找正常 frame／input lifecycle；不可用
  任意 palette override 美化收據。

## 不在本階段

- 不改翻譯、字型、角色資料安全矩形、遊戲規則、亂數或玩家輸入。
- 不為 palette 可讀性選定 2×／3×，不處理手冊版面或其他尚未接通文字路徑。
- 不以 phase 11 palette 強行覆寫目前終態，也不把 DOSBox 截圖當最終 dosgolem 收據。

## 完成條件

1. index 15 黑色的來源有可重生證據：state、遊戲 I/O 或 dosgolem 實作／序列化至少一條完整鏈，
   並區分已證實、強推論與未知。
2. 若為 dosgolem 缺口，修正經 READY→實作→同狀態驗收→CONFORMED，且不破壞既有 palette、
   savestate、framebuffer 或其他正式套件測試。
3. 修正後角色資料頁 dynamic value 的 RGBA 可見性以實際像素／PNG驗證；中文 overlay 仍只有
   安全矩形內差異，raw framebuffer 與輸入不變。
4. 若非缺口，正式證據需界定正常可見時機或明確限制，不把不可見動態值冒稱完成。
5. dosgolem 只提交本機 branch；專案 `main` 推送並更新 GitHub Issues。

## 退出條件

- 若權威 state 缺少重生 palette 所需資訊，先建立最小可重生前置 state 或 palette trace，不以
  外部 palette 檔替代正式執行。
- 若問題只剩真實 VGA DAC 時序而不改玩家可見結果，依平台停止線採規格近似；不得深入逐週期。
- 若修正會改動所有 dosgolem 遊戲的 palette 行為，必須以通用 VGA 測試與至少既有 Buck Rogers
  收據交叉驗證，不做遊戲專屬硬編碼。
