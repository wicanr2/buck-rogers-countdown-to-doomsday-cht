# 第二百三十四階段：職業 warrior／medic 標籤錯位訂正

狀態：**已證實（功能性）並修復；測試全綠。**

## 發現

phase-231 留下疑問：第 4 列選中態 dispatcher 字節為 "Medic"（5 字），
而 catalog 把第 4 列記為 warrior。判別實驗（`class500.state`＋Down＋Enter
進角色頁）：角色頁 `career:` 值為 "Medic"（`2368:0407`），且 Enter 確認
前第 4 列普通重畫亦為 "Medic"。**選第 4 列＝醫生，功能性定案。**

連帶吻合：初畫選項長 13／7／9／10／7 ＝ ROCKET JOCK＋2／MEDIC＋2／
WARRIOR＋2／ENGINEER＋2／ROGUE＋2（選項填充兩空格模式與種族／性別
屏一致）；選取態為去填充短名。顯示順序實為
Rocket／Medic／Warrior／Engineer／Rogue，第 4／5 列標籤互換。

## 修復範圍（量測欄位不動，只換標籤）

- `text/class-events.tsv`：第 4 列三筆（初畫／選中／普通）改 medic，
  第 5 列初畫改 warrior（含 `text_key`）。
- `text/class-selection-events.tsv` 第 2／3 筆事件鍵改 medic。
- `text/post-gender-events.tsv` 第 4／5 筆初畫改 medic／warrior。
- `text/class-text-safe-rects.tsv` 事件鍵跟隨改名（幾何不動）。
- `tools/test_class_events.py`、`tools/character_runtime_overlay_receipt.py`
  的鍵名跟隨；`test_post_gender_receipt.py` 的替換對仍成立，不動。
- `text/class.zh-TW.tsv` 譯文本體正確，不動；字元聯集不變，無需重建字型。

驗證：`tools/class_events.py` 交叉驗證＋全套 249 項 Python 測試通過。
舊文件不改寫，以本階段為準。後三項（warrior 選取態等）仍待 Down×2
捕捉，另案。
