# 第六十四階段：角色資料／重擲畫面靜態繁中請求

狀態：完成

## 目標

由第四十二、四十三階段已證實的角色資料／重擲正常路徑，建立靜態玩家可見文字的 exact
identity、繁中 catalog 與 dosgolem runtime `DisplayRequest`；動態能力值、技能值、亂數結果
與玩家資料保持原文語意且不得進入 catalog。

## 範圍

- 重新核對 96 筆新增事件及 `Y` 重擲／`N` 接受分支，分類靜態標籤、固定提示、動態值與
  重畫事件。
- 使用中文手冊已證實術語；找不到直接來源的介面動詞明示為 `runtime-interface`。
- 建立正式 UTF-8 TSV、雙向 verifier、失敗即關閉測試及字型字元清單。
- 先建立 dosgolem READY 子規格，再把 exact catalog 接到既有 `MenuRequestWatcher`；只產生
  typed request，不在本階段接 renderer。
- 以正常四次 Enter 到重擲畫面，以及至少一條 `Y`／`N` 分支重生決定性 request 收據。
- dosgolem 變更只提交本機 branch；專案 `main` 推送並更新 GitHub Issues。

## 不在本階段

- 不翻譯姓名、種族／性別／職業動態摘要、能力值、技能點、骰值或其他 runtime 數值。
- 不改亂數 seed、重擲規則、`Y`／`N` 輸入、原版記憶體、存檔或控制流。
- 不接玩家可見 renderer、不選定 2×／3×，不處理手冊版面決策。

## 完成條件

1. 每個 catalog identity 均可由原始 event length／SHA-256／caller／色號／row／column 回查；
   動態資料沒有誤入 catalog。
2. 譯詞來源、唯一 key、容量與字型覆蓋可驗證；未知或不安全文字失敗即關閉。
3. dosgolem spec 先達 READY，再實作 exact loader／merge／watcher；request 不含數值、輸入或
   狀態寫入欄位。
4. 正常玩家路徑收據決定性，request／miss 分類與正式清冊完全一致；原版 framebuffer、輸入
   與事件不因 watcher 改變。
5. 專案與 dosgolem 測試通過，兩個儲存庫依權利邊界提交，專案 `main` 已推送並更新 Issues。

## 退出條件

- 若同一文字 hash 同時服務靜態標籤與動態語意，先拆 identity 證據，不以字串全文模糊分類。
- 若譯詞會改變規則含義或手冊來源不足，保留未翻譯並標記證據等級，不猜補。
- 若事件清冊不足以分辨重擲重畫與新畫面，先補正常路徑收據，禁止用終態畫面倒推事件。
