# 第五十六階段：保存、名冊與加入隊伍執行期繁中顯示請求

## 結論

第五十五階段 catalog 已接入 dosgolem 正式 `MenuRequestWatcher`。完整保存→功能選單→名冊→
加入正常玩家路徑產生 18 筆 guarded post-call 事件、14 筆繁中 `DisplayRequest` 與四筆
catalog miss；四筆 miss 精確對應動態角色姓名，沒有空白請求、沿用前值或內容特例。

## 資料責任

- `text/menu-events.tsv` 擴充至 21 個唯一 identity；五筆原先缺漏的功能選單譯文回到唯一
  `text/menu.zh-TW.tsv` 權威來源。
- `text/save-roster-join-runtime-events.tsv` 只保存 `roster.add_prompt` 與 `roster.loading` 兩個
  新 identity；相同 add prompt 在路徑中出現兩次，但 catalog 不重複 identity。
- `text/save-roster-join-events.tsv` 保留 18 筆完整、依時間排序的證據清冊及靜態／動態分類。
- dosgolem `LoadRosterCatalog` 只提供檔名語境；解析、驗證、合併與 resolve 全部沿用既有
  exact catalog 核心，沒有第二套 watcher。

## 原版 oracle 收據

兩次由 #119,800,000 `save-before.state` 與 fresh scratch 起跑，固定送出保存 Enter、Down、
Add Enter、名冊 Enter，停在 #122,400,000：

- 18 events、14 requests、4 misses、3 writes、2,611 FileOps；零 pending、drop、未實作服務。
- request 順序為 11 筆功能選單、一次加入提示、一次載入提示、再一次加入提示。
- 正規化 JSON 逐 byte 相同，SHA-256：
  `898963d5fc705518705b887e849fda87bc42bd07743274b13c7ff8fe57b19299`。
- 事件、BIOS 排程、writes、FileOps 與停止步數逐項等於第五十四階段無 catalog baseline。
- framebuffer SHA-256 仍為
  `0c43f315a772f9f10281eb1fe38ebcb43a9d0cdc0b106f3cb06f49f707e7d003`；259-byte `A.who`
  與 124-byte `A.stf` 雜湊亦未改變。

## 驗證與邊界

`tools/save_roster_join_request_receipt.py` 從完整事件清冊、menu catalog 與 roster projection
重建預期 request 序列，並拒絕 identity、schema、request、miss 或 FileOps 漂移。專案 100 項
測試通過；dosgolem 全部正式 packages test／vet 與相關 race detector 通過。spec
`034-buck-rogers-save-roster-join-runtime-display-requests` 已達 CONFORMED。

本階段仍只產生輸出端 typed request；沒有載入字型、清除英文、繪製繁中像素或選定
2×／3×，所以不宣稱玩家已看到中文。

