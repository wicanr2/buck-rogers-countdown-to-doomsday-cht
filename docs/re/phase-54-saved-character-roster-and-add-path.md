# 第五十四階段：已保存角色的名冊與加入隊伍路徑

## 固定輸入與重播

- 起點為第五十三階段的 `save-before.state`，絕對 step `119,800,000`；原版輸入雜湊沿用
  第五十二階段，原版目錄唯讀。
- 每次重播都從只含 pristine `CHARS.DAX` 的獨立 scratch 開始。BIOS 排程固定為：
  `120,200,000` Enter（保存）、`121,000,000` Down、`121,200,000` Enter（Add）、
  `121,800,000` Enter（選取角色）。沒有 direct-entry、預製存檔或記憶體注入。

## 已證實的名冊與 consumer 鏈

- 保存分支於 step `120,205,401`／`120,205,903` 建立 259-byte `A.who` 與 124-byte
  `A.stf`。Add 於 `121,222,364` 開啟大小寫形式 `A.WHO`，先讀 offset 0 的 16 bytes，
  再讀 offset 194 的 1 byte；隨後文字 dispatcher 輸出 1-byte 角色名 `A`，證實檔案掃描、
  資格讀取與玩家可見名冊列已閉合。
- 名冊 Enter 後先以正常色重畫 `A`，再於 step `121,803,259` 輸出
  `Loading...Please Wait`。之後完整讀取 `A.WHO` 259 bytes，並把 `A.stf` 分成兩筆
  62-byte read；第三筆 62-byte read 在 EOF 得 0 bytes，均無 failed flag。
- 載入完成後 Add 畫面不再列出 `A`；事件只剩 3-byte 選項文字與底部 17-byte prompt。
  這與角色已從「可加入名冊」移入隊伍一致。本文只把它列為正常玩家路徑已加入的玩家可見
  結果，不推導保存格式欄位語意。
- `A.sfx` 不存在但讀取流程仍完成，且沒有未實作 DOS／BIOS 服務；本輪沒有 dosgolem
  production 缺口需要修補。

## 決定性收據

- 兩次由原始 state 與空白 scratch 完整重播都產生 18 個文字事件、2,611 筆 FileOps 與
  3 筆 write metadata。JSON 唯一原始差異是明示的 scratch 絕對路徑；正規化該欄後逐 byte
  相同，SHA-256 都是 `302f42b72a0536da4893892f0e79dc055a6b355ca70f98bb1f63b60380c9f68c`。
- 兩次終點 framebuffer 逐 byte 相同，SHA-256
  `0c43f315a772f9f10281eb1fe38ebcb43a9d0cdc0b106f3cb06f49f707e7d003`。
- 兩次 `A.who` SHA-256 都是
  `43b7dc3b227c7700d1a60cb3f17a43008e8beaa17ceec0c95873f3d18b34aa53`；`A.stf` 都是
  `90bd838048737e5be659fe81ca147174677e86228de8977bf0522e781944b1ab`。
- scratch 同時可見 `A.who` 與讀取時大小寫形式 `A.WHO`，內容與雜湊相同。這是可重播的
  overlay 表現；因未造成不同內容或玩家路徑錯誤，本階段不把它升格為 DOS 語意缺陷。

## 結論與邊界

- 第五十至五十二階段的空名冊不是角色資格失敗，也不是 dosgolem 吞掉寫檔；它來自誤走
  Left→Enter 不保存分支。真正保存後，Add 會列出、完整載入並移除已加入的角色。
- 本階段沒有翻譯新畫面、接 renderer、解析或散布角色內容，也沒有選定 2×／3×。
