# 第六十四階段：角色資料靜態繁中執行期請求

日期：2026-09-21  
狀態：完成

## 結論

由第四十二階段 96 筆角色資料事件隔離出 35 個唯一靜態 identity：19 個固定欄位／標題、
7 個能力名稱、8 個太空船駕駛員專業技能及 1 個重擲提示。`text/character-sheet-events.tsv`
只保存長度、SHA-256、caller、色號與座標；`text/character-sheet.zh-TW.tsv` 保存繁中譯文。
姓名、角色身分、摘要值、能力值、技能值及重擲骰值均未進 catalog。

中文說明書 `SCAN0352_007.jpg` 至 `SCAN0352_010.jpg` 提供屬性、職業與專業技能術語；只有
畫面本身才有的欄位標為 `runtime-interface`，未冒稱手冊譯名。終態 framebuffer 人工核對了
各列英文意義，但 Git 中沒有保存可還原原版全文。

## dosgolem 實作

- spec 037 先達 READY，才新增 `LoadCharacterSheetCatalog`；實作及收據驗收後升為 CONFORMED。
- `buckrogers-text-receipt` 新增成對的 `-character-sheet-events`／
  `-character-sheet-translations`，沿用 `MenuRequestWatcher` 與 exact catalog，不建立第二套
  watcher 或 renderer。
- 本階段只產生 typed `DisplayRequest`，未接覆繪、未選 2×／3×，也未處理手冊版面決策。

## 正常路徑收據

固定 state 為 `workplace/probe/after-bios-space-100m.state`；四次 Enter 排於 #100,010,000、
#100,240,000、#100,400,000、#100,650,000，`Y` 另排於 #101,400,000，皆停於
#102,000,000。原版目錄唯讀掛載。

| 分支 | events／requests／misses | JSON SHA-256 | framebuffer SHA-256 |
| --- | --- | --- | --- |
| 四次 Enter | 118／43／75 | `8a9759ef…e7fc` | `1f3b8194…d4dd` |
| 再輸入 `Y` | 149／52／97 | `19702fb1…6f41` | `03d9bf1f…0f97` |

兩個分支各重跑兩次，JSON 與 framebuffer 均逐 byte 相同。43 筆不是 35 個 identity 的誤算：
原版在首次呈現內再次重畫八項技能；`Y` 分支又重畫八項技能並再次顯示重擲提示，因此增加九筆。
`tools/character_sheet_request_receipt.py` 由完整 event stream 逐筆 exact resolve，確認 request
順序、譯文字數與 miss 計數；兩個 framebuffer 雜湊也分別等於既有第四十二／四十三階段基準，
證實 watcher 沒有改動原版畫面。

## 限制

此完成聲明只涵蓋 request 層。角色紙中文安全矩形、動態值周圍的清除策略、逐格失效與實際繁中
像素仍待後續 READY 規格；不能以本階段宣稱玩家已看見中文角色紙。
