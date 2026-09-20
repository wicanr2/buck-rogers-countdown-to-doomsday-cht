# 第十九階段：手冊題目事件收集器 prototype

日期：2026-09-20  
狀態：可丟棄 prototype 已通過正反向測試；正式規格仍為 DRAFT。

## 目的與邊界

第十八階段已證實錯答後的新題不是先清空再重畫。本階段只驗證一個不依賴字級倍率的事件
狀態機：題首開新世代，後續 guarded post-call 依序累積題目身分，完整題尾才產生可供 catalog
查詢的鍵。prototype 位於被 Git 忽略的 `workplace/phase19/`，不接入 dosgolem、不畫中文、
不讀取或保存答案。

## 輸入與工具收據

- 原版事件來源：[第十八階段時間線](phase-18-manual-generation-invalidation.md)
- Python：`python:3.13-bookworm`，無網路、一次性容器
- `manual_event_collector.py` SHA-256：
  `4220352a6e88edfc24ea893ef8a3185688819ecb08ae3e467dd497ef42f02c61`
- `test_manual_event_collector.py` SHA-256：
  `b41eb7c1c2e30aa78d9b2395e1d5b543f9448615248b2ebf5e97945db8312b0f`

位址均為 dosgolem 執行期實模式 `segment:offset`。prototype 的事件資料只含 caller、可見字串
與 adapter 自行配置的 generation，不含原版答案。

## Typed lifecycle

狀態為 `idle | pending(generation, stage, page?, heading?, ordinal?) | visible(key)`：

1. `begin-entry(2A33:01ED, "In the Log Book on page")`：generation 加一，清除既有 visible
   與 pending，建立新的 pending。
2. 同 generation 的 guarded post-call 必須依序為：
   `021B page → 0231 following → 027A heading → 02A5 question → 02E2 ordinal → 0309 tail`。
3. `page` 僅接受 1–999 的 ASCII 十進位；兩個固定提示與 `word?` 必須精確相符；heading
   與 ordinal 去除多餘空白後不得為空。
4. `026F:029C` clear entry 立即清除 visible，但保留尚未完成的 pending；它不建立或提交題目。
5. 只有 `0309` 的 `word?` guarded post-call 完成且三欄齊全時才提交
   `QuestionKey(page, heading, ordinal)`；提交後 pending 消失。
6. caller、順序、常值或欄位驗證失敗時，該 generation 進入 poisoned 狀態；只有下一個精確
   begin-entry 能復原。generation 不相符的延遲 post-call 一律忽略。

第 1、2、4、5 項的事件順序有第十八階段原版收據支持，屬於**已證實輸入順序＋DRAFT
adapter 設計**；欄位範圍、poisoned 與復原規則是**失敗即關閉設計**，不是原版內部狀態的
宣稱。

## 真實事件結果

將第十八階段六筆題目 fragment 依原順序送入，並在第三與第四筆之間送入矩形清除，得到：

```json
{"answer_data_stored": false, "generation": 1, "question": {"heading": "Technical Skills", "ordinal": "second", "page": 41}, "visible": {"heading": "Technical Skills", "ordinal": "second", "page": 41}}
```

此鍵與原版題庫第 38 筆及第十八階段畫面一致。這證明 prototype 可消費已取得的事件，不證明
其他版本、其他入口或正式 runtime hook 已完成。

## 負向測試

9 項測試全部通過，其中負向案例涵蓋：

- 缺少題尾不提交。
- heading 提前出現使該 generation 失敗。
- 重複 page 使該 generation 失敗。
- 未知 caller 使該 generation 失敗。
- 舊 generation 的延遲 post-call 不污染新 pending。
- 非數字與 0 頁碼失敗即關閉。
- 非精確題首不建立 generation，也不誤刪現有 visible。

## 結論與下一步

typed lifecycle 已有可執行 prototype 與反例測試，可作正式 adapter 測試設計的輸入；但 DRAFT
spec 仍缺使用者的 2×／3× 決定、正式 hook、catalog 接線、原版／繁中同狀態 A/B 與分頁輸入。
因此 prototype 不升格、不搬入 production package，規格不標 READY。
