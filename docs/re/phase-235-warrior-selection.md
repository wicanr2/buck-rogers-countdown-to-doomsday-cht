# 第二百三十五階段：warrior 選取態補錄

狀態：**已證實並收錄；測試全綠。**

## 實驗

由 `workplace/checkpoints/class500.state` 連按 Down×2
（500.1M／501.1M，BDA），dispatcher 吐四筆完整生命週期：
rocket 普通 → medic 選中 → medic 普通 → **warrior 選中 "Warrior"**
（7 字，SHA-256 `eaf0fe0a…`）；終點 VRAM 第 5 列白底、第 4 列回普通。
收據留 ignored `workplace/phase235-warrior-selection/`。

## 收錄

- `text/class-events.tsv` 追加序列 11／12：
  `class.selection.selected.warrior`（175D，白底）與
  `class.selection.normal.warrior`（1856，前景 10），
  皆第 5 列第 3 欄、長 7、同雜湊，`text_key` 為修正後的
  `class.warrior`（戰士）。
- `text/class-text-safe-rects.tsv` 追加兩筆一對一矩形
 （24,40,56×8，容量 7）。
- `tools/class_events.py` 筆數錨改為十二筆連續；其餘交叉
  （post-gender 前七、lifecycle 四組）位置不動。
- down-down 新生命週期路徑未建模（`class-selection-events.tsv`
  仍只含 down-up 與 escape），另案。

驗證：catalog 交叉＋矩形一對一＋全套 249 項通過。
