# 第三十八階段：確認性別後的職業選擇文字路徑

## 結論

從既有 #99,999,999 固定 state 依序在 #100,010,000、#100,240,000、#100,400,000 排入
三個正常 BIOS Enter，原版接受預設種族與預設性別後，於 #100,410,301 開始輸出職業選擇
畫面。新畫面恰有七筆完成事件：一筆提示、五筆 normal 職業選項及 selected 第一選項。

兩次正式重播的 22-event JSON 與 64,000-byte indexed framebuffer 各自逐 byte 相同。這只
證實預設種族／預設性別的單一路徑；不同分支、職業方向鍵、Escape、確認職業後畫面及角色
規則仍未量測。

## 固定輸入與工具

- state SHA-256：`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`。
- `START.EXE`／`GAME.OVR` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`／
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- `cmd/buckrogers-text-receipt/main.go` SHA-256：
  `ed6e7b6537a9be3fe332f49821adee0d91c51a1f4510ca32648ed1b0f8fad5c9`。
- dosgolem spec 019 已依 READY→正式重播→CONFORMED；本機 commit：
  `371683b7f5793c7104e839202497c742ba3e13c0`，未推送 dosgolem 遠端。

所有 caller 皆為 dosgolem runtime `segment:offset`。正式資料只保存長度、SHA-256、caller、
色號、座標與語意鍵，不保存原版英文全文。

## 正常輸入與事件時間線

- #100,010,000：第一個 Enter，進入種族選擇。
- #100,240,000：第二個 Enter，接受預設種族並進入性別選擇。
- #100,400,000：第三個 Enter，接受預設性別。
- #100,400,451 → #100,403,706：原 selected 男性列先以 normal style 重畫。
- #100,410,301 → #100,580,245：職業提示、五個 normal 選項及 selected 第一選項完成。
- #101,000,000：固定停止；最後事件後沒有新增 dispatcher 完成事件。

## 七筆新事件

`text/post-gender-events.tsv` 保存完整 content-safe identity：

| event key | entry → post-call | caller | len／SHA-256 | bg/fg | row,col |
| --- | --- | --- | --- | --- | --- |
| `class.screen.prompt` | 100410301 → 100418147 | `37F1:158C` | 10／`ba7ebb6c…11cf2` | 0/13 | 2,1 |
| `class.option.rocket_jock` | 100437195 → 100447349 | `37F1:15BD` | 13／`0daed6fa…28df7` | 0/10 | 3,1 |
| `class.option.warrior` | 100464371 → 100469932 | `37F1:15BD` | 7／`5f06e4b5…afa06` | 0/10 | 4,1 |
| `class.option.medic` | 100491004 → 100498085 | `37F1:15BD` | 9／`703e3358…c1ed6` | 0/10 | 5,1 |
| `class.option.engineer` | 100517807 → 100525650 | `37F1:15BD` | 10／`c5d861df…9d682` | 0/10 | 6,1 |
| `class.option.rogue` | 100544697 → 100550258 | `37F1:15BD` | 7／`01889f0c…aa4bd` | 0/10 | 7,1 |
| `class.selection.selected.rocket_jock` | 100571639 → 100580245 | `37F1:175D` | 11／`86e1e1a3…555f1` | 15/0 | 3,3 |

一次性原版 bytes 反查與候選雜湊逐筆確認畫面提示與五個職業語意；臨時腳本已刪除，原文全文
沒有寫入 Git。normal 第一列含兩格縮排，selected 第一列去掉縮排，形狀與前兩個選單一致；
但在正常 Down／Up 實驗前，不能直接把其完整生命週期視為已證實。

## 決定性收據與驗證

- JSON SHA-256：`a3e195ebe6f43ffa2d9fdcfaeb92c8f68323da9bb487dc9c468095c3b012570b`。
- framebuffer SHA-256：`3a61cb542625bdb0fd353f1d337e87c68091bd2dd2185e9b2ba34dad7558012c`。
- `tools/post_gender_receipt.py` 固定輸入／命令雜湊、三鍵排程、前 15 筆既有證據、新七筆
  inventory、22 組 exact step／identity 與終點 framebuffer。
- 負向測試拒絕 identity、step、排程、筆數、schema、BOM、重複鍵、錯誤 hash／caller 大小寫、
  數值越界及缺列。
- 專案 58 項 Python 測試與真實 verifier 通過；dosgolem spec 索引 256 份、全部正式 packages
  test／vet 及相關 race detector 通過。

## 證據等級與下一步

- **已證實**：單一三 Enter 正常路徑、22 筆事件順序、七筆職業畫面 identity 與終點畫面。
- **已證實**：第一職業在固定終點為 selected style，五個選項語意已由雜湊核對。
- **強推論**：兩格縮排的 normal／selected 重畫可能沿用種族與性別選單模式。
- **未知**：職業選單 Down／Up／Escape、確認職業後畫面、其他種族／性別可用職業差異。

下一個最小切片應先量職業選單 selection／return lifecycle，再建立繁中 catalog 與 runtime
request；不得由相似 caller、色號或座標直接接 production renderer。

