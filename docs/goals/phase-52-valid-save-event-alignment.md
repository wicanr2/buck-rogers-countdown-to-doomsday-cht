# 第五十二階段：合法保存後段事件對齊

狀態：已完成

## 目標

以第五十一階段已證實的完整技能配置路徑，逐事件對齊第四十八至第五十階段的圖示確認、
儲存詢問與加入角色流程，判定空名冊究竟來自按鍵時點、原版角色資格條件，或 dosgolem
尚未支援的檔案語意。

## 範圍

- 從相同 #99,999,999 state 與正常 BIOS 輸入重播完整 80 點職業技能、40 點技術技能配置。
- 以 dispatcher identity、事件 step、畫面與 BIOS 消費時點比對既有 phase 48–50 收據；
  不只比較終點 framebuffer。
- 在圖示確認、儲存詢問、功能選單與加入角色畫面各取得一個穩定 checkpoint，確認輸入實際
  落在哪個玩家可見狀態。
- 使用空白、隔離、可寫 scratch，保存 content-safe FileOps 與檔案大小／SHA-256 差異；
  pristine original 維持唯讀。
- 若證據顯示 DOS 服務缺口，先建立 DRAFT 規格並取得可重現最小案例；證據不足前不修改
  dosgolem production code。
- 完成後推送專案 `main` 並更新 GitHub Issues；dosgolem 只有在本輪確有 READY 實作時才
  建立本機分支 commit，仍不得推送其遠端。

## 不在本階段

- 不翻譯技能、圖示、保存或名冊畫面，不接 renderer，也不選定 2×／3×。
- 不解析或散布角色完整內容，不以記憶體注入、direct-entry、跳關或未用點數確認取代正常路徑。
- 不因終點名冊為空就先假定寫檔缺口，也不為了讓測試通過而偽造角色資料。

## 成功定義

1. 第五十一階段後段每一個 BIOS 輸入均能對回實際玩家可見狀態與事件邊界。
2. 圖示確認與儲存詢問至少各有一份可視、可重播 checkpoint，並與既有 phase 48–50 identity
   對齊或明確記錄合法角色路徑的新差異。
3. 保存後的 FileOps、scratch manifest 與加入角色結果可判定，且證據足以分類根因。
4. 相同輸入由空白 scratch 獨立重播兩次，JSON、framebuffer、manifest 與雜湊逐 byte 相同。
5. 研究文件誠實區分已證實、強推論、假說與未知；若需實作，必須先有 READY 規格。
6. 專案文件、測試與必要 verifier 通過，`main` 已推送、Issues 已更新，Docker 與工作樹乾淨。

## 退出條件

- 若後段輸入只是時點錯置，修正診斷排程並重生收據，不修改 dosgolem 行為。
- 若原版明確拒絕此角色，保留拒絕條件證據，不把它改造成成功保存。
- 若出現未實作或錯誤 DOS 服務，先回到 RE → DRAFT → READY；不得由 probe 直接進 production。

## 2026-09-21 進度收據

- 圖示完成、圖示確認、保存預設／YES、返回功能選單及 Add 選取均已有正常玩家路徑
  checkpoint；後 26 筆事件與第五十階段既有分支完全對齊，已排除後段按鍵時點錯置。
- 新增並驗收 `-unimplemented` 與 `-state-out`；spec 032／033 已 CONFORMED。雙重正式重播
  的 JSON、framebuffer、scratch 逐 byte 相同，回讀後 1 MiB memory 亦逐 byte 相同。
- 未實作 DOS／BIOS 服務、身體圖示未移動，以及目前找到的 persistent memory 差異 consumer
  均已排除為空名冊根因；原版保存條件／記憶體內角色生命週期仍未知，本 Goal 保持進行中。

## 2026-09-21 第五十三階段勘誤

- 本階段把預設 Enter／Left→Enter 分別命名為 NO／YES 的判讀已推翻；預設 Enter 才會建立
  `A.who`／`A.stf`，Left→Enter 不保存。因此本階段零寫檔與空名冊只證明不保存分支，不能
  用來推論合法角色保存失敗。完整控制流與檔案收據移交第五十三階段。

## 2026-09-21 關閉收據

- 第五十四階段以真正保存分支證實角色名冊、保存檔 consumer 與加入結果；空名冊根因已
  分類為選項語意誤標，不是按鍵時點、資格條件或 dosgolem 檔案服務缺口。
