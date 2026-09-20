# 第 27 階段：功能選單文字事件清冊

## 狀態

完成

## 本輪目標

由 dosgolem 既有正常 Enter 路徑固定狀態，重生功能選單到 `PICK RACE` 的九筆
`0763:0424` 事件，建立不含原版全文的 typed metadata 清冊；補齊正式選單 catalog 在進入
純事件核心前所需的 caller、座標、色彩、長度與 guarded post-call 證據。

## 範圍

- 載入顯示／語意隔離與規格閘門契約，回讀第 2、4–8、24 階段既有證據。
- 由既有固定 state 以原本正常 BIOS Enter 路徑重播，不 direct-entry、不寫記憶體。
- 收據只保存穩定 key、原文 SHA-256／長度、caller、row／column、前景／背景、entry／post-call
  step 與 guard 結果；不把完整原版選單文字另存成 catalog。
- 若現有 dosgolem observer 缺少精確欄位，以遊戲專屬 `apps/buckrogers`／命令補足並測試；
  不擴張 `oracle` 持久化 state 公開 API。
- 回填 DRAFT 選單規格的已解項與仍未知邊界，推送專案 main 並更新 Issues #4、#5、#8。

## 不在本輪範圍

- 不建立 production `xlate.Stamp`、不畫中文、不選 2×／3×。
- 不把九筆樣本外推成全遊戲文字路徑，不翻譯劇情、戰鬥、物品或角色名稱。
- 不把固定 state 取代正常玩家路徑；它只縮短已由正常路徑建立的決定性重播。

## 驗收條件

- 九筆事件由同一固定輸入與 BIOS Enter 重生，entry 與 guarded post-call 一一配對。
- 每筆 metadata 可唯一連到 `menu.zh-TW.tsv` 的正式 key，沒有原文全文或語意 fallback。
- 清冊 schema、唯一性、bounds、SHA-256、事件順序與正式 TSV 覆蓋有自動測試。
- 未收錄、caller／座標／色彩不符、錯誤 guard 均失敗即關閉。
- dosgolem 正式 packages 與專案資料測試通過；兩個工作樹乾淨。
- dosgolem 只建立本機 commit、不推送其遠端；專案 main 推送並更新相關 Issues。

## 預定交付物

- dosgolem 選單事件 observer／收據工具與測試（若既有 API 不足）
- `text/menu-events.tsv` 或等價的 answer-free typed metadata 清冊
- `docs/re/phase-27-menu-event-inventory.md`
- 選單 DRAFT 規格、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

已完成。由 #99,999,999 固定狀態在 #100,010,000 排入 BIOS Enter，九筆 dispatcher entry
與 guarded post-call 全數重生並對齊既有正常路徑；正式 `menu-events.tsv` 只保存 key、
length／SHA-256、caller、色號與座標。真實 JSON receipt verifier、32 項專案資料測試、
dosgolem 正式 packages test／vet 與 Buck Rogers race detector 均通過。dosgolem 本機 commit
為 `98f3bec55d633cc2a69099f187848af4d765b7d1`，未推送其遠端；未選倍率、未繪製中文。
