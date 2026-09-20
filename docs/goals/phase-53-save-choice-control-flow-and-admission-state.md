# 第五十三階段：保存選項控制流與名冊接納狀態

狀態：進行中

## 目標

從第五十二階段 `SAVE A? YES NO` 的同一份 dosgolem state 分別執行 YES 與 NO，定位兩條
原版控制流的首次分歧、重新匯合點與狀態寫入，判定 YES 是否建立了後續 Add 流程會消費的
角色接納狀態，或目前對保存選項的理解仍有缺口。

## 範圍

- 固定同一個原版輸入雜湊、savestate、scratch 初始內容與 BIOS 輸入時點，只改變保存選項。
- 先用被 Git 忽略的可丟棄探針比對執行期 `CS:IP`、記憶體寫入與玩家可見事件；所有位址均
  明示 dosgolem 執行期位址空間。
- 找出首次分歧與重新匯合區間後，再縮小到被寫入的候選狀態及其至少一個 consumer；不得以
  欄位名稱或相鄰位址取代讀寫證據。
- 保持原版素材唯讀，所有 trace、savestate、memory dump 與 framebuffer 只留在
  `workplace/`。
- 若證據指出 dosgolem 行為缺口，先建立 DRAFT 規格與最小重現；證據審查成 READY 前不改
  production code。
- 完成後推送專案 `main` 並更新 GitHub Issues；dosgolem 只有在本階段產生合規正式修改時
  才建立本機分支 commit，仍不得推送其遠端。

## 不在本階段

- 不翻譯保存、名冊或加入隊伍畫面，不接中文 renderer，也不選定 2×／3×。
- 不偽造角色、直接注入接納旗標、改寫原版條件或以 direct-entry 取代正常建立角色流程。
- 不因 YES／NO 的單一差異 byte 就宣稱找到保存旗標；未找到 consumer 的欄位保持未知。

## 成功定義

1. YES 與 NO 從同一 state 各可獨立重播兩次，輸入排程、事件與 trace 具有可稽核收據。
2. 首次控制流分歧與重新匯合點以原始 `CS:IP` 及指令 bytes 記錄，且不同位址基準不混用。
3. 分歧區間的狀態寫入已列出；至少一項候選有寫入來源及後續讀取 consumer，或誠實證明目前
   無法建立該鏈。
4. 證據足以判定下一步應追原版接納規則、overlay／間接存取，或 dosgolem 缺口；不得用假說
   直接進正式實作。
5. 研究文件、目前狀態與 Issues 已更新，專案 `main` 已推送，Docker 與工作樹乾淨。

## 退出條件

- 若 YES 只影響玩家可見返回流程而沒有可持續狀態，記錄反證並轉追更早的角色完成條件。
- 若找到明確狀態但 Add 不消費，保留完整讀寫鏈，另立窄任務追真正 consumer。
- 若 trace 暴露 CPU、DOS、overlay 或 savestate 語意差異，回到 RE → DRAFT → READY，不以
  probe 特例修補 production path。

## 2026-09-21 進度收據

- 已證實預設 Enter 會建立 `A.who`／`A.stf`，Left→Enter 不保存；第 49–52 階段的分支標籤
  與零寫檔推論已追加可追溯勘誤。
- 兩路 IP trace 各自雙重一致，首次 Left 分歧與保存 DOS 呼叫已有 runtime 位址收據；保存檔
  大小與 SHA-256 亦雙重一致。尚待以真正保存分支接續 Add，因此本 Goal 保持進行中。
