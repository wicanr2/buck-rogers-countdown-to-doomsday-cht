# 第七十七階段：技能操作列安全矩形與雙倍率執行期覆繪

狀態：等待使用者確認 normal 配色

## 目標

將 Phase 76 已 CONFORMED 的技能操作列繁中 `DisplayRequest` 接入 dosgolem 長存輸出覆繪層。
先以真實 framebuffer、既有 16×16 點陣字及 2×／3× 明示倍率量測底列可用區域，再把通過
證據審查的安全矩形與失效規則實作為 runtime overlay；原版英文、繁中像素與動態畫面不得殘疊。

## 範圍

- 量測 career／technical 操作列上方內容、底列英文墨跡與 16×16 繁中文字模所需高度。
- 比較至少兩個可丟棄版面：以原標籤中心定位，以及使用底部 16-pixel command band；不靠裁切
  或縮小字模掩蓋溢出。
- 建立以 exact event key 綁定的文字安全矩形；normal／focus 共用幾何，狀態只改語意色彩。
- 補齊 clear、焦點移動、頁面轉換與離開技能頁的 active-stamp 失效契約。
- 在明示 2×／3× 各重播 career／technical 的 base 與焦點移動代表路徑，驗證像素 containment、
  A/B 決定性、原版 framebuffer 與非顯示語意不變。

## 不在本階段

- 不替使用者選定產品預設 2×／3×。
- 不改手冊題目版面、原版輸入、技能點、焦點判定、存檔或 disabled 行為。
- disabled variant 仍為 unknown，不以 normal／focus 猜補。
- 不複製 PC-98 美術、邊框、配色或文案；只採用 CJK 整數倍率、16×16 cell 與命令區分離的
  可重用版面原則。

## 完成條件

1. 以真實畫面證明每個安全矩形可容納正式譯文，且不侵入技能列、動態數值或畫面邊界。
2. dosgolem 規格依 `RE → DRAFT → READY → implementation → same-state → CONFORMED` 完成。
3. loader 對缺少、孤兒、重複、越界、重疊或容量不足矩形失敗即關閉。
4. normal／focus 取代、clear 與技能頁轉場均沒有英文殘字、繁中殘字或 stamp 堆疊。
5. 2×／3× 正常玩家路徑雙重播一致；核准矩形外零差異，原版 indexed framebuffer 與
   control 相同，譯文不進入語意路徑。
6. 專案與 dosgolem 測試通過，專案 `main` 推送並更新相關 GitHub Issues。

## 退出條件

- 若 16×16 字模在原版底部 8-pixel band 無法不侵入上方內容，先保留 prototype 與量測證據，
  回到版面決策；不得用裁字、非整數縮放或擴大未證實清除區硬接 production。
- 若失效需辨識尚未證實的畫面事件，退回 DRAFT 補 runtime 證據，不以逾時清除猜測。
