# 第六十階段：手冊覆繪 READY 前置稽核

日期：2026-09-21  
狀態：完成

## 結論

手冊 runtime watcher、精確題目身分、序數橋接、來源分級與正式 catalog 的實作前契約均已
具備。總體規格 `002` 目前唯一尚未完成的 READY 前置，是使用者尚未選定正式輸出倍率
2×／3×；正常玩家路徑覆繪、錯答重抽、像素 containment 與同狀態 A/B 都是 renderer 接線後
才能產生的 CONFORMED 收據，不再循環列為 READY 前置。

## 資料邊界

| 資料 | 筆數／結果 | SHA-256 |
| --- | --- | --- |
| `manual-questions.tsv` | 39 筆原版題目 metadata | `3793e7af…6da6912` |
| `manual-source-crosswalk.tsv` | 35 confirmed、3 strong-inference、1 unknown | `4e078342…58fc6` |
| `manual-events.tsv` | 22 筆正式事件 | `bbf9c905…092963efb6f` |
| `manual.zh-TW.tsv` | 22 筆正式譯文；最長 236 字 | `cea5474e…97d1bb` |
| `manual-ordinals.tsv` | 10 筆已證實序數 | `fbf643ff…0b538e` |

目前 22 筆譯文全都小於 36×17＝612 字的單頁容量，所以本批不需要玩家分頁輸入。剩餘
17 題不等同 17 題來源未知：其中 13 筆來源已證實但尚未逐字校訂或不適合本批短篇 catalog，
另有 3 筆強推論與 1 筆未知。它們一律 catalog miss、保留原版英文；不模糊比對、不猜補，
也不把「來源已證實」誤當成「譯文已核准顯示」。

## READY 稽核矩陣

| 前置 | 權威／驗證 | 結果 |
| --- | --- | --- |
| 39 題 metadata 與來源對照一致 | `manual_crosswalk.py`＋原始解壓 manifest | 通過 |
| 顯示事件只引用 confirmed 來源 | `manual_catalog.py` | 22 筆通過 |
| 題目身分與序數精確唯一 | `manual_catalog.py`、`manual_ordinals.py` 與負向測試 | 通過 |
| generation、caller、guarded post-call 失敗即關閉 | dosgolem spec 007／008 與 `apps/buckrogers` 測試 | 通過 |
| 真實事件可產生顯示請求 | 第 24 階段固定狀態收據 | 通過 |
| catalog miss 不產生請求 | `41 / Technical Skills / second` 收據與測試 | 通過 |
| 本批內容不需分頁輸入 | 最長 236 字，小於 612 字 | 通過 |
| 正式輸出倍率 | 第 17、25、59 階段 2×／3× 證據 | **等待使用者選擇** |

## 驗證收據

- 專案基準 commit：`c90509c3f53dbf91be84f1af228518f7d1280a38`。
- dosgolem 本機分支 commit：`b2fb8556c40f1509965b558ff2d5f97bb02fc6a0`，未推遠端。
- `manual_crosswalk.py --manifest ...` 與 `manual_catalog.py ...` 通過。
- 專案 `python -m unittest discover -s tools -p "test_*.py"`：101 項通過。
- dosgolem `go test ./apps/buckrogers ./cmd/buckrogers-receipt` 與
  `go test -race ./apps/buckrogers` 通過。

以上只證明 renderer 接線前的資料與 watcher 契約；尚未證明手冊中文段落已畫到正常玩家
路徑。使用者選定倍率後，仍須依 spec 002 的 CONFORMED 清單產生正式同狀態收據。
