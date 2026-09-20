# 第四十四階段：角色姓名輸入生命週期

## 結論

從相同固定 state 經四次 Enter、`N` 接受能力值到達姓名提示後，#102,050,000 的 `A` 與
#102,150,000 的 `B` 各產生一筆長度 1 的回顯事件，column 由 17 增至 18；
#102,250,000 的 Backspace 沒有 dispatcher 事件，但終點 framebuffer 證實第二字元被清除、
第一字元保留。這證明文字事件清冊不能單獨涵蓋編輯生命週期，畫面收據是必要證據。

另一分支輸入 `A` 後按 Enter，原版進入職業技能點配置畫面；本階段停在該第一個穩定終點，
沒有配置技能。Escape probe 只重印姓名提示且終點畫面不變，空字串 Backspace 也沒有事件或
像素差異，因此沒有證據支持 Escape 具有取消語意。

## 固定輸入與收據

- state SHA-256：`cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`。
- `START.EXE`／`GAME.OVR` SHA-256：
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`／
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 收據命令 SHA-256：`363fc8045519fe4b70184a756549e5eade8917320ae9eff65a5e78ff38538231`。
- 共用前綴為四次 Enter 與 `N`；基線固定為第 43 階段 183-event 收據 SHA-256
  `f9ed6a8ef55bc3503d427a04f2788b55c959b35e3e1af31b0c52058d27117bff`。
- 編輯分支：兩份 185-event JSON SHA-256
  `863440bcee78552f70d86cc1d086ef5953d6f993ceaa3798cfc48170060ee9e3`；framebuffer SHA-256
  `bd3d779926df3b0e2979f5317f718480057bc01f36768610ac1378aa4c8feec6`。
- 確認分支：兩份 226-event JSON SHA-256
  `52e50460281115f677e0ab73dc94c206a8d7af5d6713977d912d28ecd4281d3d`；framebuffer SHA-256
  `a1cd728cecaa720357f680f2be66e857f401ee5b0113f9959b23143e0fae95f7`。

兩條正式分支的 JSON 與 64,000-byte framebuffer 各自逐 byte 相同。編輯終點相對姓名提示
基線有 111 個不同像素，bounding box `(136,192)–(151,199)`；確認終點有 11,338 個不同
像素，bounding box `(0,9)–(318,199)`。

## 事件結構與證據邊界

`text/name-edit-events.tsv` 保存 `A`、`B` 兩筆回顯 identity；Backspace 的效果由固定終點畫面
證明，不虛構一筆不存在的文字事件。`text/name-confirm-events.tsv` 保存一筆玩家輸入回顯與
42 筆技能配置畫面事件。短測試姓名只用於輸入驗證，不是譯文，也不會寫入正式 catalog。

姓名提示與技能配置內容的正式檔案只保存 length、SHA-256、caller、色號、座標、step 與
語意角色，不保存原版英文全文。技能點規則、加減操作、可用點數及確認流程全都仍是未知，
不能因畫面已出現就宣稱該子系統完成。

## 驗證與下一步

`tools/name_input_receipt.py` 固定輸入雜湊、183-event 基線、兩組 BIOS 排程、完整新事件與終點
framebuffer；負向測試拒絕基線、schema、role、step、排程、事件數與 identity 漂移。
dosgolem 規格 `025-buck-rogers-character-name-input-lifecycle` 保存 READY→正式重播→CONFORMED
契約。

下一個不依賴倍率的最小切片是技能點配置的方向鍵／加減／確認／返回生命週期；角色資料與
技能畫面的繁中靜態標籤應和動態數值分離後再接 catalog。
