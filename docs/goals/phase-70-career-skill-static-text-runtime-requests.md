# 第七十階段：職業技能配置靜態文字繁中請求

狀態：已完成

## 目標

沿第六十九階段已驗證的 `A`→Enter 正常路徑，從職業技能配置畫面事件中隔離固定標題、欄名
與技能名稱，建立正式 UTF-8 TSV exact catalog，並由 dosgolem runtime 產生繁中
`DisplayRequest`；所有剩餘點數、技能數值、加值與總計仍走原版動態顯示。

## 範圍

- 對照 `name-confirm-events.tsv` 與後續職業技能互動清冊，分類固定文字、選取 variant、動態
  數值及非 dispatcher 畫面文字；保留 caller、hash、長度、色號與座標。
- 固定文字譯名優先引用本目錄中文手冊與既有專案術語；無法唯一確認者維持 miss，不猜補。
- 建立 events TSV、繁中 catalog、來源反查驗證器及正反例測試；同一語意的 normal／selected
  variant 共用 text key，但保留不同 exact identity。
- 在 dosgolem 接入 loader 與成對命令列旗標，以 `A`→Enter 正常路徑驗證 request 順序、數量、
  動態值 miss 與原版 framebuffer 不變。

## 不在本階段

- 不建立文字安全矩形或繪製繁中像素，不翻譯非 dispatcher 的底部操作圖字。
- 不修改技能點規則、方向鍵、加減、完成、剩餘點數或角色資料。
- 不選定產品預設倍率，不處理手冊版面。

## 完成條件

1. 每個 catalog identity 均能回查正式事件清冊；靜態／動態分類具已證實證據。
2. 譯名有中文手冊或已核准術語來源；無來源的文字不進正式 catalog。
3. runtime 正常路徑只對核准靜態 identity 產生 request，所有數字事件維持 miss。
4. 正反例資料測試、dosgolem 正式測試／vet／相關 race detector與專案回歸通過。
5. dosgolem 只提交本機 branch；專案 `main` 推送並更新相關 GitHub Issues。

## 退出條件

- 若某事件的原文內容或角色不明，先以本機一次性探針精確核對；完整英文不得進正式 catalog。
- 若正常與 selected variant 無法證實同語意，不共用 text key，先保留 miss。
- 若譯名超出原文範圍，本階段仍只完成 request；幾何必須留待獨立 READY 規格，不縮寫硬塞。

## 完成摘要

- 已建立 14 個 exact identities：四個標題、八個一般技能列、注意力 selected 與無重力行動
  selected；技能譯名逐筆鎖定既有正式角色資料 catalog。
- base 正常路徑為 226 events／14 total requests／212 misses；Down 為 234／16／218，新增兩筆
  request 正是原版 normal→selected 重畫。
- control 與 catalog 各雙重重播一致，原版 events、BIOS keys、停止點與 framebuffer 不變。
- spec 209 已 CONFORMED；所有動態點數與未證實 selected variants 維持 miss，本階段未建立
  安全矩形或繪製繁中像素。
