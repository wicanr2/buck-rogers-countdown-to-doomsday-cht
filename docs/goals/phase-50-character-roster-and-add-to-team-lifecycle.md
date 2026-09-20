# 第五十階段：角色名冊與加入隊伍生命週期

狀態：已完成

## 目標

沿用第四十九階段返回功能選單的 `NO` 與 `YES` 分支，從正常玩家路徑進入「加入角色」功能，
辨識新建角色是否出現在名冊、兩分支是否有可見差異，以及第一個可判定的加入隊伍結果。

## 範圍

- 由同一固定 state 走完整正常 BIOS 前綴，分別接受儲存詢問的預設 `NO` 與選取 `YES`，再從
  功能選單以正常方向鍵及 Enter 進入加入角色流程。
- 以事件次序、identity、完整 framebuffer 與必要的 overlay manifest 判斷名冊可見性及分支
  差異，不由選項文字推測記憶體內角色是否存在。
- 若名冊可操作，探測最小的一條選取／加入或返回路徑；只追到第一個穩定玩家可見邊界。
- 正式分支各從相同 state 獨立重播兩次，固定 BIOS 排程、事件 step、原版與命令雜湊及
  64,000-byte indexed framebuffer。
- 建立 dosgolem 診斷規格、content-safe 清冊、嚴格 verifier、正反例測試與研究文件。
- 完成後提交 dosgolem 本機分支、推送專案 `main` 並更新 GitHub Issues。

## 不在本階段

- 不推導完整角色資料或隊伍資料格式，不修改或散布原版素材。
- 不使用 direct-entry、記憶體注入或測試跳關。
- 不翻譯名冊或加入隊伍畫面、不接 renderer、不選定 2×／3×。
- 不將單一新角色的結果外推為完整六人隊伍或冒險開始流程。

## 成功定義

1. 正常輸入證實 `NO` 與 `YES` 後進入加入角色功能的可見結果及分支差異。
2. 若新角色可見，至少證實一條選取／加入或返回結果；若不可見，固定可重播的負面證據。
3. 正式分支各雙重重播逐 byte 相同；動態角色內容與靜態文字事件已分開分類。
4. verifier 對輸入、事件、step、identity、畫面、原版與命令雜湊漂移失敗即關閉。
5. dosgolem 規格達 CONFORMED；專案測試、正式 Go packages、`go vet` 與相關 race detector
   通過。
6. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 若 `NO`／`YES` 後的差異只存在記憶體而畫面不可判定，先保存可見負面證據，再開窄切片
  追蹤資料寫入與 consumer，不以欄位猜測代替玩家結果。
- 若加入角色需要尚未建立的磁碟存檔，記錄精確前置條件並停止該分支。
- 若進入下一個全新互動畫面，只追到第一個穩定邊界，另開切片處理後續操作。

## 完成結果

- 發現並修正收據命令未設定 `DOS.Scratch` 的證據缺口；spec 030 保留並標為 SUPERSEDED。
- dosgolem 收據命令新增失敗即關閉的 `-scratch` 與可選 content-safe `-file-ops` metadata。
- scratch-backed FileOps 證實 `NO`／`YES` 都 shadow `CHARS.DAX`，但沒有 DOS write；四份正式
  scratch manifest 只含內容等於 pristine 的 `CHARS.DAX`。
- 兩分支進入加入角色功能時都沒有角色列，並回到逐 byte 相同的功能選單；各雙重重播的
  316-event JSON、framebuffer 與 manifest 均一致。
- 專案 94 項測試與 dosgolem 正式 packages test／vet／race 全數通過，spec 031 已 CONFORMED。
- 本階段沒有推導角色資料格式、翻譯、接 renderer 或替使用者選定 2×／3×。

## 後續勘誤（第五十三階段）

- 本階段兩條所謂 `NO`／`YES` 收據的選項語意命名有誤；真正會保存的是預設 Enter，會建立
  `A.who` 與 `A.stf`。Left→Enter 才是本階段反覆量到的零寫檔路徑。
- 因此「兩分支皆無 DOS write」與由此推導的空名冊結論撤回；舊重播仍保留為不保存分支
  的有效負面收據，後續須用真正保存分支重驗 Add 正常玩家路徑。
