# 第五十階段：角色名冊與加入隊伍生命週期證據

## 證據修正

第四十九階段的收據命令沒有設定 `DOS.Scratch`。dosgolem 在 scratch 空白時會讓寫入維持 DOS
成功語意但不落地，因此舊 overlay manifest 無法證明零副作用。spec 030 保留原畫面／事件
證據並標為 SUPERSEDED；spec 031 核准 scratch-backed 重驗。

## 已證實行為

- `NO` 與選取 `YES` 都以讀寫模式開啟並 shadow `CHARS.DAX`，但 FileOps 沒有任何 DOS write。
- 四次正式重播的 scratch 都只含 `CHARS.DAX`，大小 32,070 bytes，內容 SHA-256
  `22140498a21cc5f2074dbe2a766c808c0e54a8404181e1264f939f046d59e8b5`，等於 pristine。
- 兩分支返回功能選單後 Down→Enter；加入角色功能沒有產生角色列文字事件，隨即重建功能
  選單，兩個終點 framebuffer 逐 byte 相同。

## 正式收據

`NO` 與 `YES` 分支各為 316 events，各自獨立重播兩次；每對 JSON、64,000-byte framebuffer
與 scratch manifest 逐 byte 相同。verifier 固定 scratch 路徑、命令與原版雜湊、鍵盤排程、
兩條 305-event 基線、新增事件及 manifest。

## 證據限制

本階段只證實這條以未用技能點離開的角色建立路徑沒有產生可加入角色；沒有證實完整配置技能
後的合法角色是否會被保存，也沒有解析 `CHARS.DAX` 或外推完整隊伍規則。
