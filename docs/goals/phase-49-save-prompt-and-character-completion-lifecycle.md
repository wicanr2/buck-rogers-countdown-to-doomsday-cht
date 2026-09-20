# 第四十九階段：儲存詢問與角色建立完成生命週期

狀態：已完成

## 目標

沿用第四十八階段正常 Enter→`Y` 路徑進入儲存詢問，辨識 `Y`／`N` 的實際結果，並追到
角色建立完成後第一個穩定玩家可見畫面，建立 content-safe、可重播且失敗即關閉的正式收據。

## 範圍

- 由同一固定 state 走完整正常 BIOS 前綴到儲存詢問，再由相同基線獨立探測 `Y` 與 `N`。
- 原版輸入保持唯讀；若 `Y` 會寫檔，先在忽略版控的明確 writable overlay 複製原版資料，
  並固定寫前／寫後檔案清冊與雜湊，不修改 pristine original。
- 以事件次序、identity、完整 framebuffer、DOS 結束狀態與檔案差異判斷結果，不猜測
  「儲存」或「完成」語意。
- 每條正式分支各從相同 state 與相同 overlay 基線獨立重播兩次；固定 BIOS 排程、事件 step、
  原版與命令雜湊及 64,000-byte indexed framebuffer。
- 建立 dosgolem 診斷規格、content-safe 清冊、嚴格 verifier、正反例測試與研究文件。
- 完成後提交 dosgolem 本機分支、推送專案 `main` 並更新 GitHub Issues。

## 不在本階段

- 不推導完整存檔格式，不修改或散布原版素材與產生的存檔。
- 不使用 direct-entry、記憶體注入或測試跳關。
- 不翻譯儲存詢問或後續畫面、不接 renderer、不選定 2×／3×。
- 不將角色建立完成外推為整款遊戲正常可玩。

## 成功定義

1. 正常輸入證實儲存詢問 `Y` 與 `N` 各自可判定的結果及第一個穩定玩家可見邊界。
2. 若發生寫檔，pristine original 雜湊維持不變，overlay 檔案差異可重播且已明確分類。
3. 正式分支各雙重重播逐 byte 相同；靜態文字事件與檔案副作用已分開分類。
4. verifier 對輸入、事件、step、identity、畫面、檔案差異、原版與命令雜湊漂移失敗即關閉。
5. dosgolem 規格達 CONFORMED；專案測試、正式 Go packages、`go vet` 與相關 race detector
   通過。
6. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 若 `Y` 寫檔而現有收據工具無法安全導向 overlay，先補足 dosgolem 的最小安全能力，
  不改寫 pristine original，也不把寫檔失敗當作遊戲語意。
- 若任一分支進入新互動畫面，只追到第一個穩定玩家可見邊界，另開切片處理其互動。
- 若分支依賴尚未支援的 DOS 服務，記錄精確缺口並回填 dosgolem，不以 DOSBox 收據替代。

## 完成結果

- 已證實儲存詢問不是字母 `Y`／`N` 對話框：直接 `Y` 無作用，直接 `N` 接受預設 `NO`。
- 真正的 `YES` 路徑為 Left→Enter；`NO` 與 `YES` 均回到逐 byte 相同的功能選單終點。
- 兩條接受分支共四份 overlay manifest 皆等於 pristine manifest，沒有磁碟檔案副作用。
- 三條正式分支各雙重重播逐 byte 相同；兩份清冊、嚴格 verifier 與正反例測試已建立。
- 專案 92 項測試與 dosgolem 正式 packages test／vet／race 全數通過，spec 030 已 CONFORMED。
- 本階段沒有翻譯、接 renderer、推導存檔格式或替使用者選定 2×／3×。

## 後續勘誤（第五十階段）

- 本階段收據命令當時未設定 dosgolem `Scratch`；無 scratch 時寫入會維持成功語意但不落地，
  因此「overlay manifest 相同證明沒有檔案副作用」的結論已撤回。
- 畫面、輸入與事件結論仍有效。檔案副作用已由 spec 031 使用 scratch-backed 收據重驗：
  兩分支確實沒有 DOS write，且名冊結果相同。
