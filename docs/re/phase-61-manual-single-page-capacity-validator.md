# 第六十一階段：手冊單頁容量失敗即關閉驗證

日期：2026-09-21  
狀態：完成

## 結論

`tools/manual_catalog.py` 現在以 `36×17＝612` 個 Unicode 字元為正式手冊譯文單頁上限。
612 字恰好通過，613 字明確拒絕；不截斷、不自動分頁、不送鍵，也不接管原版答案輸入。
目前 22 筆正式譯文全部通過，最長仍為 236 字。

這是資料進入 runtime 前的失敗即關閉驗證，不是手冊 renderer 或正常玩家路徑完成證據。
總體 spec 002 維持 DRAFT，正式倍率仍等待使用者選定 2×／3×。

## 證據與契約

- 第十七階段 prototype 的 `wrap()` 直接以 Python Unicode 字串切成每列 36 字，17 列為一頁；
  `xlate.Layout` 同樣採一個 Unicode 字元一格，因此容量計數語意一致。
- `MANUAL_PAGE_COLUMNS = 36`、`MANUAL_PAGE_BODY_ROWS = 17`，並由兩者導出
  `MANUAL_PAGE_CAPACITY = 612`，沒有散落第二個裸數值。
- 驗證只套用到已由 `manual-events.tsv` 精確映射的 catalog entry；未映射 key 原本就會拒絕。
- 超限錯誤包含 record、實際字數與 612 字上限，便於定位資料，不會降級為警告。

## 驗證收據

- 聚焦測試：`PYTHONPATH=/repo/tools python -m unittest tools/test_manual_catalog.py`，6 項通過。
- 正式資料：`python tools/manual_catalog.py ...` 通過。
- 完整回歸：`python -m unittest discover -s tools -p "test_*.py"`，103 項通過。
- 第一次聚焦命令未設定 `PYTHONPATH`，在測試收集階段因找不到 `manual_catalog` 失敗；以完整
  discovery 與上述正確命令重跑後乾淨通過，分類為驗證命令環境問題，不是產品缺陷。
- 本輪未修改 workplace dosgolem，沒有建立空提交，也未推送其遠端。
