# 第七十二階段：技術技能配置靜態文字繁中請求

狀態：完成

## 目標

從第四十七階段已證實的正常玩家路徑，隔離技術技能配置畫面的固定標題與技能名稱，
建立 content-safe exact identity、UTF-8 繁中 catalog 與 dosgolem runtime display requests；動態點數、
加值、總計及未實測選取 variant 維持 catalog miss。

## 範圍

- 以第四十七階段入場與 Down 收據為原版證據，盤點固定標題、一般色技能列與已實測 selected identities。
- 技能譯名必須反查現有角色資料正式 catalog 或中文手冊證據；不以未分級自由翻譯補齊。
- dosgolem 新增技術技能 catalog loader／成對旗標，共用既有 guarded post-call watcher。
- 入場 base 與 Down 各做 control／catalog 雙重重播，比對 events、requests、misses、BIOS keys 與 framebuffer。

## 不在本階段

- 不建立 text-safe rectangle，不繪製繁中像素，不選定 2×／3× 預設倍率。
- 不修改技能點規則、加減、離開條件、存檔或原版任何語意。
- 不擴張到未實測選取列、底部操作文字或手冊覆繪。

## 完成條件

1. 正式 event TSV 只保存雜湊、長度、位址／callsite、座標、色號與證據引用，不收錄完整英文。
2. 事件與譯文 key 雙向完整，重複／孤兒／來源漂移／動態值誤納均失敗即關閉。
3. base／Down 的 exact request 計數與 normal／selected 重畫順序符合原版事件收據。
4. catalog 與 control 的 presentation 欄位外 JSON 及 64,000-byte framebuffer 相同，每路雙重重播決定性一致。
5. 專案回歸、dosgolem test／vet／相關 race 通過；dosgolem 只提交本機 branch，專案 `main` 推送並回寫 Issues。

## 退出條件

- 若同一原文 identity 可能同時是動態值或語意路徑，該筆維持 miss，不以畫面相似推定。
- 若技能譯名沒有可追溯中文來源，停在 DRAFT 並記錄缺口，不自行定案。
- 若 runtime 命中會改變原版比較、輸入、狀態或 framebuffer，不接入 production path。

## 完成收據

- 13 個技術技能譯名已逐筆回到中文手冊 `SCAN0352_012.jpg` 第 19–20 頁原圖校訂。
- 首次合併發現兩個標題與 career catalog 是同一 exact identity；規格退回 DRAFT 後改為
  共享既有 identity，technical catalog 只新增 17 個不重複 identities，並以旗標關係失敗即關閉。
- base 雙重重播為 289 events／32 requests／257 misses；Down 為 297／34／263。
- control／catalog 的 presentation 欄位外 JSON 與 64,000-byte framebuffer 相同；每路 A／B 逐位元一致。
- 專案 131 項 Python 測試、dosgolem 正式套件 test／vet 與本輪改動套件 race 全數通過。
