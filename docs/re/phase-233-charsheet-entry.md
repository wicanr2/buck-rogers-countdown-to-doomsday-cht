# 第二百三十三階段：角色資料頁進入與 dispatcher 全表

狀態：**已證實／單次重播（字串表）；catalog 整合另案。**

## 實驗

由可重播 `workplace/checkpoints/class500.state`（500M 職業屏），
Enter（500.1M，BDA）進角色資料頁，`call-args 0763:0424`＋
`call-length-string` 捕捉 500–502M 共 96 筆 dispatcher
（ignored `workplace/phase233-charsheet-entry/enter-calls.txt`）。

## 字串表摘要（原文只列形狀，不作翻譯來源）

- 首筆 `37F1:1856` “Rocket Jock”（11 字，與既有 normal 收據逐位元同值）。
- 標籤群（`2368` 系呼叫者）：name／hp／race／ac／gender／thaco／
  career／level／status／experience／credit／age／movmnt／
  encumbrance／damage／weapon／armor／abilities／career skills，
  皆冒號短標，與第 64–65 階段 35 靜態標籤家族銜接（逐筆對帳另案）。
- 值群：Martian、Male、Rocket Jock、Okay、20、1,250、七圍 12／14／
  11／17／14／15／14、11／11、10、20、0、12、1d2——**證實此前
  路徑選擇（Martian、Male、Rocket）全數生效**。
- 技能列群：Notice、Maneuver in 0G、Use Jetpack、Pilot Rocket、
  Pilot Fixed Wing、Drive Ground Car、Pilot Rotor Wing、Drive Jetcar，
  先 0 後 24 兩輪（Pilot Rocket 首輪即 24，餘見表）；末筆
  `37F1:101E` “Reroll stats? ”提示。
- 終點 VRAM（`after-enter.vram`，`150dd9f5…`）為新屏，
  像素比對未做（字串表已足）。

## 邊界

- 本表只有呼叫者＋字串，無前景／背景／列欄——**不是**事件 TSV
  可直接收錄格式；`tools/*_catalog.py` 式交叉驗證與中文映射是
  Issue #4／#64–65／#71–73 的後續切片，不得以本表宣稱收錄。
- trans430.state 的重播發散（缺 scratch 掛載初判，補小寫檔後仍發散）
  另記：class500 可重播已證，trans430 原因未定，不作結論。
