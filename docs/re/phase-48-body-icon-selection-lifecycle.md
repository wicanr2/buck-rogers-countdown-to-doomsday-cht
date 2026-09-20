# 第四十八階段：角色身體圖示選擇生命週期證據

## 範圍與輸入

本階段從固定 state 經完整正常角色建立 BIOS 路徑，到達角色身體圖示選擇畫面。原版資料
唯讀掛載；沒有 direct-entry、記憶體注入或流程跳關。

## 已證實行為

- Left、Right、Up、Down 都會改變選取圖示與 framebuffer；正式收據以 Right 固定一條移動。
- Enter 與 Escape 產生逐 byte 相同的圖示確認提示；本階段以 Enter 作正式輸入。
- Enter→`N` 重建圖示畫面，終點逐 byte 等於操作前基線。
- Enter→`Y` 進入儲存詢問畫面，這是本階段第一個穩定玩家可見邊界。

## 正式收據

移動、拒絕與確認分支分別為 297／302／298 events。三條分支各獨立重播兩次，JSON 與
64,000-byte framebuffer 均逐 byte 相同；清冊只保存 identity、step、位置、色彩與證據等級。

## 證據限制

本階段沒有回答儲存詢問、沒有推導全部圖示語意，也沒有翻譯、接 renderer 或選定 2×／3×。
