# 第一百二十六階段：手冊成功返回後的鍵盤 consumer 邊界

日期：2026-09-22
狀態：**已確認合法 Num Lock 前進鍵被原版取走，並走到該 consumer 的非零輸入分支；其玩家語意與通往選單路徑仍未知。**

## 受控輸入與原版觀測

從第一百二十三階段的私有 330M state（SHA-256
`d20cbc0bf0b7425ab29b26a59666b91bbd32c1e5776ee9593190b4cd8918fcb5`）排入 Data Card
明示的數字鍵盤前進鍵：step `331000000`、scan `48h`、ASCII `38h`。這是 Num Lock 條件下的
既有手冊輸入，不是新增猜測鍵。

本機 dosgolem `-key-trace` 診斷（預設關閉、只輸出鍵盤 metadata）確認：

- step `331000198`，原版經 `INT 16h/AH=00h` 從 BIOS BDA ring 取走字組 `0x4838`；終態
  `keys_pending=0`。
- `KeyRead` caller chain 是 dosgolem 實模式 `37F1:1116 ← 328E:1732`；INT handler 當下為
  `0C10:031C`。這些是 runtime `segment:offset`，不是 IDA 線性位址或檔案 offset。
- 至 340M 沒有新 dispatcher event、FileOps、未實作 DOS／BIOS 服務、indexed framebuffer 或
  palette 差異。這只證明玩家可見結果未變，不能說原版「忽略」或「拒絕」該鍵。

因此已排除「鍵未送達」與「鍵仍在佇列」兩個假說；尚未證實取鍵後的狀態轉移。

同一 state、同一顆鍵的第二次受控重播，以 step `331000180` 起的 160 個指令為上限，僅輸出
`CS:IP`、`AX`、FLAGS 與 `SS:SP`（不輸出原版 bytes 或畫面內容）。結果如下：

- step `331000224` 從 BIOS 路徑返回 runtime consumer `37F1:1116`，`AX=0x4838`；故取出的鍵值
  確實回交原版 consumer。
- 對應的 `37F1:111E` 條件跳轉後，下一個 IP 是 `37F1:113A`，表示本次沒有走零值的跳轉邊。
- `37F1:113A` 的下一個條件跳轉在 `37F1:113F` 執行後，下一個 IP 是 `37F1:118A`；這是已觀測的
  非零輸入邊。它只證實控制流，不足以為該分支命名或推論移動、隊伍、劇情、保存等語意。

追蹤在上限處停止，尚未看見 consumer 函式返回或選單轉場；因此不能由「非零分支」推論 Num Lock
`8` 已完成可見前進或有任何隱藏效果。

## IDA 對應與條件證據

依 `use-ida-pro-9-4` 契約，使用 `ida-pro-9.4-idapython:locked-v1` 的 IDA 9.4 一次性、
16-bit x86 資料庫分析唯讀 `GAME.OVR`。最小探針輸出存在且非空，輸入 SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，IDA kernel 版本為
9.4；所有 DB、原始 bytes 與 JSON 都只留在 `workplace/phase124-keytrace/`。

- **已確認**：runtime consumer 附近 32 bytes 的私有 prefix 唯一命中 `GAME.OVR` file offset
  `183158`；64-byte prefix 不相同，故不以較長 bytes 冒稱檔案完全等同 runtime。
- **強推論**：以此唯一 32-byte 對應，IDA 在 file offset `183158` 解碼到取鍵後先將 `AL`
  寫入 `byte_6B49`，再比較 `byte_8435` 是否為零並條件跳轉。此為 IDA 裸 OVR 的線性
  file-offset view；不得與上段 runtime 位址混用。
- **強推論**：依同一連續載入對應，`byte_8435` 的 runtime 候選位址讀值為 `255`，因此此
  次執行不是「值為零」的分支。但尚未以函式 entry／return trace 證明這個 candidate mapping
  或該值的遊戲語意；它維持未命名狀態 gate，不得稱為劇情、隊伍或保存旗標。

IDA 匯出同時保留每筆 offset、operand、instruction bytes SHA-256 與輸入 hash；沒有以推測性
名稱覆蓋原始定位。

## 保存／讀檔邊界與下一步

本證據仍未到主選單或隊員管理選單，未觀測 A–J 槽位、保存檔 write 或讀檔 consumer。第五十二
至五十四階段的建角保存／讀檔資料不可接到本分支。

下一個最小切片是以同一 330M state、同一筆已證實的 Num Lock `8`，將這條**已走到**
`37F1:118A` 的單一路徑追至 consumer 返回或下一次既有 key-poll（兩者任一先到即停止），只記錄
控制流 edge、必要 register result 與已對應狀態 gate 的讀／寫。它不送第二個鍵、不改 state，也
不假設 gate 語意。只有該 trace 證明一條原版正常轉場到主選單或隊員管理選單後，才可驗證手冊
規定的 save/load 路徑。

## 環境與清理

全部診斷在一次性、無網路 Docker 內進行；原版掛載唯讀，輸出只在 ignored `workplace/`。
IDA 授權與原始 bytes 未進版本庫。本階段不改遊戲規則、翻譯 catalog、正式 overlay 或原版
資料。
