# 第四十三階段：重擲提示輸入與動態欄位重畫生命週期

## 結論

從第四十二階段相同 #99,999,999 state 及四次 Enter 正常路徑，到達角色資料頁後於
#101,400,000 排入 BIOS `Y`，原版重畫七項能力值、摘要／職業技能衍生值，最後再次輸出同一
重擲提示。排入 BIOS `N` 則重建角色資料內容後，停在角色姓名輸入提示。兩條分支
都沒有 direct-entry、記憶體注入或規則修改。

Space 與 Escape 各只新增一筆相同重擲提示，終點 framebuffer 逐 byte 等於按鍵前基線；
Enter 與 `N` 的終點 framebuffer 相同，但事件 step 不同。據此，`Y` 重擲與 `N` 接受是
**已證實**；Enter 採用接受分支是**強推論**，不把它冒稱為與 `N` 逐指令相同。

## 固定輸入與收據

- state SHA-256：`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`。
- `START.EXE`／`GAME.OVR` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`／
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 收據命令 SHA-256：`363fc8045519fe4b70184a756549e5eade8917320ae9eff65a5e78ff38538231`。
- 前四鍵：#100,010,000、#100,240,000、#100,400,000、#100,650,000 Enter；分支鍵
  #101,400,000；固定停止點 #102,000,000。
- `Y`：兩份 149-event JSON SHA-256
  `132cf0078289064e7ccba27a5dafe346df1b0e78c35e051afaa5461392ed5eb5`；framebuffer SHA-256
  `03d9bf1fcdd871055949c5545eaf102fecb7aa6ef0f3b3e09a2dcf6e95050f97`。
- `N`：兩份 183-event JSON SHA-256
  `f9ed6a8ef55bc3503d427a04f2788b55c959b35e3e1af31b0c52058d27117bff`；framebuffer SHA-256
  `55da7c0e296b882f99c7c8ba2550743debe93a8bc480d1a0fc8fbb1dc514a6bb`。

每條分支兩次 JSON 與 64,000-byte framebuffer 各自逐 byte 相同。`Y` 相對基線有 58 個不同
像素，bounding box 為 `(65,10)–(300,174)`；`N` 終點的 indexed framebuffer 相對基線只有
最下方提示列不同，共 385 個像素，差異 bounding box 為 `(1,192)–(159,199)`。中間事件雖
重畫角色資料內容，終點主區域色號已回到與基線相同；不能由終點差異反推中間清除範圍。

## 事件結構與亂數邊界

`text/reroll-yes-events.tsv` 保存 `Y` 分支 31 筆新事件：七筆能力值、六筆摘要重畫、八組
技能標籤／值、另一筆摘要重畫及重擲提示。`text/reroll-no-events.tsv` 保存 `N` 分支 65 筆
轉場事件，最後一筆為姓名提示。兩份清冊只含 step、長度、雜湊、caller、色號、座標與語意
角色，不含英文全文。

同一 snapshot 的兩次 `Y` 結果一致，證實 snapshot 已包含足以重生這次重擲的原版狀態；
本階段沒有定位 seed、亂數公式或呼叫次數，也沒有反覆重擲挑選結果。因此收據不能外推自然
開局、其他職業或後續連續重擲的骰序。

## 驗證與下一步

`tools/reroll_lifecycle_receipt.py` 固定輸入、第四十二階段 118-event 基線、五鍵排程、兩分支
完整 step／identity、JSON 與 framebuffer 雜湊；負向測試拒絕基線、schema、role、證據等級、
step、排程、筆數及 identity 漂移。dosgolem 規格
`024-buck-rogers-reroll-input-lifecycle` 保存 READY→正式重播→CONFORMED 契約。

下一個不依賴倍率的最小切片是姓名輸入提示的編輯、確認與返回生命週期；角色資料頁靜態文字
翻譯與動態值隔離應另開規格，不得把兩種事件混成同一 catalog。
