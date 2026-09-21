# 第八十五階段：手冊繁中 presenter 接線 READY 前稽核

狀態：完成

## 目標

盤點 dosgolem 中既有的手冊 typed request、xlate runtime overlay、clear／generation lifecycle 與
正常玩家路徑收據，確認哪些資料已足以支援一個倍率明示、只改 RGBA 的手冊 presenter，哪些
仍是 DRAFT blocker。此工作與 host 面板點選後的套用語意分離。

## 已確認前提與結果

- 手冊顯示請求只從已證實的 `word?` guarded post-call 產生；不含答案、輸入或原版狀態寫入。
- 中文正文固定為下方 `[7,312)×[72,184)`、36×14、504 字；原版頁碼、英文標題與序數保留。
- 2×與3×皆為正式輸出模式；使用者已選擇先選取倍率、再按套用（C）。
- 以正常玩家 state 重跑，#266,557,246 仍只產生一筆 answer-free 手冊 request；收據沒有
  證明中文已畫上畫面。
- `xlate.Layer` 足以作為只讀 framebuffer 的 RGBA layer，但現有 `RuntimeMenuOverlay` 是單列
  選單 adapter，不能直接承擔 14 行手冊段落。
- 新增 [規格 005](../spec/005-manual-runtime-presenter-draft.md) 與研究收據後確認：watcher 的
  presentation lifecycle callback／queue 與正式 691 glyph 字型仍是 READY blocker。

## 範圍

- 固定目前 dosgolem branch／revision，讀取手冊 core、runtime watcher、xlate 與既有 runtime
  overlay 的實際介面及測試。
- 對照手冊 metadata、layout TSV、字型與至少一條正常玩家路徑收據，建立 presenter 所需輸入、
  lifecycle、失敗即關閉規則與驗收缺口清單。
- 產出或更新 DRAFT 規格；僅在所有行為與驗收前提已證實時才可提出 READY 子規格，不直接實作。

## 不在本階段

- 不接 presenter、不改 dosgolem 程式、不修改原版輸入、答案判定、存檔或 host UI。
- 不將未校訂段落、`strong-inference`／`unknown` 題目或任何手冊全文加入正式輸出。
- 不替使用者選擇面板點擊的立即套用、保持開啟或 Apply 語意。

## 完成條件

1. 每個 presenter 前提均有 source path／revision、原版收據或資料驗證支持，並標示已證實、強推論、
   假說或未知。
2. 明確區分可獨立進入 presenter READY 的需求與仍由 host 控制決策阻擋的需求。
3. 無 production code 變更；文件、`main` 推送與相關 GitHub Issue 回寫完成。

## 退出條件

- 若手冊 request、clear 或 normal path 的既有收據不足以證明 lifecycle，維持 DRAFT 並回到
  dosgolem RE；不得由其他畫面 overlay 類推。
- 若發現 presenter 必須依賴未決 host 行為，記為 blocker，不以默認倍率或 DOS 輸入捷徑繞過。
