# 第五十二階段：合法保存後段事件對齊

## 輸入與工具

- 原版 `START.EXE` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`。
- 原版 `GAME.OVR` SHA-256：
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- dosgolem `buckrogers-text-receipt/main.go` SHA-256：
  `1101960dd2ea7f83fcc65860dbc388616c04e141756328cb795357e5abeb56fd`。
- 動態位址採 dosgolem 8086 執行期 `segment:offset` 或線性位址；IDA 證據採 IDA database
  linear address，兩者不混用。IDA Pro 9.4 image ID 為
  `sha256:6f6d59af49d0008c4109a5295b5f374bdc007e2d1ab28cb9de08779584de2780`。
- 原版素材唯讀；scratch、savestate、memory dump、framebuffer 與完整 JSON 只留在被 Git
  忽略的 `workplace/`。

## 已證實的玩家可見路徑

- 完整配置 80 點職業技能與 40 點技術技能後，Escape 不再顯示未用點數警告，而是進入
  `SELECT A BODY ICON. DONE`。
- 後續 checkpoint 依序為 `IS THIS ICON OK? YES NO`、`SAVE A? YES NO`；Left 確實把保存
  選項由預設 `NO` 移到 `YES`，Enter 後回到功能選單。
- 完整配置路徑的最後 26 筆 dispatcher identity 與第五十階段 `YES`→`ADD CHARACTER TO
  TEAM` 分支逐筆相同。Down→Enter 確實選到加入角色，但沒有角色列並返回功能選單。
- Right 先移動身體圖示只多一筆圖示重畫事件；後續保存、FileOps 與終點 framebuffer 不變。
- 功能選單只有 Create／Add／Load／Joystick-Mouse Initialize／Exit 五項；一度把 Down×3
  誤認為 Drop，實測進入的是 `MOUSE ON / JOYSTICK OFF / DISABLE BOTH`，已推翻該假說。

## DOS 與記憶體證據

- `-unimplemented` 正式雙重重播皆為空；37,021 筆 FileOps 沒有 DOS write。scratch 只含
  32,070-byte `CHARS.DAX`，SHA-256
  `22140498a21cc5f2074dbe2a766c808c0e54a8404181e1264f939f046d59e8b5`，等於 pristine。
  因此「有記錄但未實作的 DOS／BIOS 服務造成保存消失」已排除。
- 完整與未用技能點路徑在保存後的 DGROUP 只差 runtime `0EC0:388B` 一個 byte（`02`／
  `00`）；加入角色重播對該位址沒有任何讀寫。它不是已證實的名冊資格欄位，技能游標狀態
  只是假說。
- 排除 BDA、堆疊與 framebuffer 後，另有線性 `0x574BF..0x574F6` 四處 persistent 差異；
  加入角色只讀相鄰且兩路相同的 `0x574C9..0x574CD`，沒有讀取差異 bytes。不得把它們命名為
  角色資料或保存旗標。
- IDA Pro 9.4 對固定 START.EXE 的一次性 database 有 180 個函式；operand `0x388B` 無直接
  命中。這只排除 IDA 已辨識的直接定址，不排除 GAME.OVR 或暫存器／相對基址間接存取。

## 決定性與限制

- 兩次正式 JSON、framebuffer 與 scratch 逐 byte 相同；savestate gzip／gob bytes 不同，
  但回讀後完整 1 MiB memory 逐 byte 相同。壓縮封裝差異不列為機器狀態失敗。
- 空名冊根因仍未知：後段按鍵錯置、身體圖示未移動、未實作服務與目前找到的 persistent
  byte consumer 都已排除，但尚未證實原版保存條件或記憶體內角色生命週期。
- 本階段沒有修改原版規則、DOS 服務、角色資料、中文 renderer 或 2×／3× 倍率決策。
- dosgolem 診斷功能保存在本機分支 commit
  `4bb3cc9d83868ea2d827cff33b43e2585c7f16ac`，未推送其遠端。

## 第五十三階段勘誤

- 本文「Left 將預設 NO 移到 YES」已被同 state 檔案副作用實驗推翻：預設 Enter 會建立
  `A.who`／`A.stf`，Left→Enter 不會。本文正式重播走的是不保存分支，所以零 DOS write
  不能支持「合法角色仍無法保存」。
- 後段按鍵時點本身仍已對齊，但選項語意標籤錯誤；空名冊根因不再列為未知保存條件，改為
  尚未用真正保存分支重驗 Add。原始位址與收據保留，以免勘誤抹除錯誤來源。

## 第五十四階段關閉未知項

- 真正保存後的 Add 已列出角色，選取後完整讀取 `A.WHO`／`A.stf` 並從可加入名冊移除；
  因此本文的「原版保存條件／記憶體內角色生命週期未知」已由檔案 consumer 與正常玩家
  路徑解決。原空名冊根因是誤走不保存分支。
