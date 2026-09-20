# 第四十七階段：技術技能配置的選取、加減與離開生命週期

狀態：已完成

## 目標

沿用第四十六階段正常 Escape→`Y` 路徑進入技術技能配置畫面，辨識技能列選取、一次合法
加點與減點、未用點數離開確認及下一個穩定玩家可見終點，建立 content-safe、可重播且
失敗即關閉的正式收據。

## 範圍

- 由同一固定 state 走完整正常 BIOS 前綴到技術技能畫面，再分支探測 Down、Enter、
  Enter→Right→Enter、Escape→`N` 與 Escape→`Y`。
- 以事件次序、identity、色彩、座標與完整 framebuffer 判斷選取、點數與轉場，不猜規則。
- 正式驗證至少涵蓋技能列移動、一次合法加點後減回，以及一條可判定的離開／拒絕路徑。
- 每條正式分支各從相同 state 獨立重播兩次，固定 BIOS 排程、事件 step、原版與命令雜湊及
  64,000-byte indexed framebuffer。
- 建立 dosgolem 診斷規格、content-safe 清冊、嚴格 verifier、正反例測試與研究文件。
- 完成後提交 dosgolem 本機分支、推送專案 `main` 並更新 GitHub Issues。

## 不在本階段

- 不自動配置全部 40 點，不推導技術技能上限、bonus、total 或職業限制。
- 不使用 direct-entry、記憶體注入、點數寫入或測試跳關。
- 不保存原版英文全文，不把動態數值或不可見反白文字當作譯文。
- 不翻譯技術技能畫面、不接 renderer、不選定 2×／3×。

## 成功定義

1. 正常輸入證實技能列移動、合法加減，及 Escape 後至少一條可判定結果。
2. 正式分支各雙重重播逐 byte 相同；動態點數與靜態文字事件已分開分類。
3. verifier 對輸入、事件、step、identity、畫面、原版與命令雜湊漂移失敗即關閉。
4. dosgolem 規格達 CONFORMED；專案測試、正式 Go packages、`go vet` 與相關 race detector
   通過。
5. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 若技術技能操作與職業技能不同，只保存實測差異，不套用上一畫面規則。
- 若 Escape→`Y` 進入後續畫面，只追到第一個穩定玩家可見邊界，另開切片處理其互動。
- 若離開會寫入檔案，只在唯讀原版與明確可寫 overlay 下重播。

## 完成結果

- 已證實 Down 選取移動、Enter 加點、Right→Enter 減回、Escape→`N` 回復及 Escape→`Y`
  進入角色身體圖示選擇畫面。
- 四條正式分支各雙重重播逐 byte 相同；四份清冊、嚴格 verifier 與正反例測試已建立。
- 專案 88 項測試及 dosgolem 正式 packages test／vet／race 全數通過，spec 028 已 CONFORMED。
- 本階段沒有翻譯、修改技能規則、接 renderer 或替使用者選定 2×／3×。
