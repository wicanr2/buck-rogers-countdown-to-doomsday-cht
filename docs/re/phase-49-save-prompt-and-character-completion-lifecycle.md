# 第四十九階段：儲存詢問與角色建立完成生命週期證據

## 範圍與輸入

本階段從固定 state 經完整正常角色建立 BIOS 路徑，到達角色圖示確認後的儲存詢問。`NO`
與 `YES` 使用由同一 pristine original 複製的隔離 writable overlay；沒有 direct-entry、記憶體
注入或流程跳關。

## 已證實行為

- 儲存詢問採選項操作；直接字母 `Y` 沒有 dispatcher 事件或 framebuffer 變化。
- 預設反白為 `NO`；直接字母 `N` 接受該選項並離開角色建立，回到功能選單。
- Left 改變反白但沒有 dispatcher 事件；後續 Enter 接受 `YES`，同樣回到功能選單。
- `NO` 與 `YES` 的終點 framebuffer 逐 byte 相同；四份寫後 overlay manifest 都逐 byte 等於
  pristine manifest。本段實測沒有磁碟檔案副作用，不能由選項文字外推成已寫檔。

## 正式收據

字母 `Y`、預設 `NO` 與選取 `YES` 分支分別為 298／305／305 events。三條分支各獨立重播
兩次，JSON 與 64,000-byte framebuffer 均逐 byte 相同；兩條接受分支另固定完整檔案 manifest。

## 證據限制

本階段只證實角色建立流程離開至功能選單；沒有證實角色是否已加入任何記憶體內名冊，也沒有
推導存檔格式、翻譯畫面、接 renderer 或選定 2×／3×。
