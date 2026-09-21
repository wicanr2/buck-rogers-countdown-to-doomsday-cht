# 第六十五階段：角色資料頁安全矩形與雙倍率執行期覆繪

狀態：完成

## 目標

將第六十四階段 35 個靜態繁中 `DisplayRequest` 接到 dosgolem 既有明示倍率
`RuntimeMenuOverlay`，以角色資料頁的實際動態值座標建立不互相覆蓋的 text-safe rectangle，
並用 2×／3× 正常玩家路徑完成同狀態與像素 containment 驗證；不替使用者選定產品倍率。

## 範圍

- 由第四十二／四十三階段事件座標及真實 framebuffer 推導每個靜態欄位的安全右界；中文清除
  範圍不得覆蓋姓名、角色身分、摘要、能力值、技能值、重擲回答或金框。
- 建立 `character-sheet-text-safe-rects.tsv`、嚴格 verifier、負向測試與字型覆蓋輸入。
- 先建立 dosgolem READY 子規格，再擴充 receipt command 的 character-sheet rect 旗標；沿用
  現有 renderer、typed clear、同原點 replace 與 frame clock。
- 四次正常 Enter 到角色資料頁，以及 `Y` 重擲後回到同一頁，2×／3× 各 fresh 重播兩次。
- 比較無覆繪 baseline：原版 events、BIOS keys、indexed framebuffer 不變；差異像素只在核准
  安全矩形內，動態數值與重擲回答不得被清除。

## 不在本階段

- 不選 2×／3× 作產品預設，不變更字級、美術、色彩、規則、亂數、存檔或原版資料。
- 不翻譯動態姓名、種族／性別／職業值、摘要值、能力值、技能值或玩家輸入。
- 不處理手冊查詢版面決策，也不把角色資料頁矩形套用到技能配置等後續畫面。

## 完成條件

1. 35 個 event key 均有唯一、可回查、單列且容量足夠的安全矩形；矩形彼此不重疊，也不碰觸
   已證實動態欄位或金框。
2. dosgolem 規格依 READY→實作→同狀態驗收→CONFORMED；character-sheet catalog 在 overlay
   模式必須成對提供 rect，缺表或孤兒表失敗即關閉。
3. base 與 `Y` 分支的 request／action 一一對應，typed clear／重畫後 active keys 與當下畫面
   一致，沒有殘字、缺字、pending、drop 或非預期 catalog miss。
4. 2×／3× 各兩次 JSON／RGBA 決定性；raw framebuffer 與 baseline 一致，安全矩形外差異為零，
   並以原始解析度 PNG 人工檢視文字、數值、提示、回答與金框。
5. 專案與 dosgolem 測試通過；dosgolem 只提交本機 branch，專案 `main` 推送並更新 Issues。

## 退出條件

- 若任一譯文在不覆蓋動態欄位的矩形內無法容納，保留 request 而停止該 renderer 分支，不截斷
  或縮寫正式譯文。
- 若同一 row 的靜態與動態輸出生命週期無法由現有 typed clear 分離，規格退回 DRAFT 並先補
  事件證據，不以終態畫面硬刪 stamp。
- 若雙倍率呈現造成不同的幾何語意，保留兩份原型供使用者決策，不自行設定預設倍率。
