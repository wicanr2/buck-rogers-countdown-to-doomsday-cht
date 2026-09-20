# 第 27 階段：功能選單文字事件清冊

日期：2026-09-20  
狀態：完成 typed observer 與清冊；玩家可見覆繪仍為 DRAFT

## 結論

由 `after-bios-space-100m.state` 的正常功能選單固定狀態，在絕對步數 #100,010,000 排入
BIOS Enter；原版沿既有正常路徑重生九筆 `0763:0424` entry 與九筆三重 guard 通過的
post-call。新 `text/menu-events.tsv` 只保存事件鍵、正式文字鍵、原文長度／SHA-256、caller、
色號與文字格座標，不保存原版全文。

這證明八個正式繁中 key 已有九個 exact runtime identity；不證明任何中文字已畫進玩家畫面。

## 輸入與位址空間

- 固定 state：被 Git 忽略的 `workplace/probe/after-bios-space-100m.state`，起點
  #99,999,999；由既有正常玩家路徑建立。
- 輸入：#100,010,000 排入 `Enter(scan=0x1c, ascii=0x0d)`；舊收據證實原版於
  #100,010,174 取走。
- 原版素材：唯讀掛載於 state 保存的 `/orig`。
- dispatcher／caller：dosgolem 執行期實模式 `segment:offset`，不是 IDA linear address。
- 收據：被 Git 忽略的 `workplace/phase27/menu-receipt.json`，不含原文或譯文。

## 重播結果

| seq | event key | text key | entry → post-call | caller | len | bg/fg | row,col |
| ---: | --- | --- | --- | --- | ---: | --- | --- |
| 1 | `menu.transition.old.create_new_character` | `menu.create_new_character` | 100010490 → 100025943 | `37F1:1856` | 20 | 0/10 | 12,9 |
| 2 | `race.screen.prompt` | `menu.pick_race` | 100033190 → 100040266 | `37F1:158C` | 9 | 0/13 | 2,1 |
| 3 | `race.option.terran` | `race.terran` | 100059989 → 100066316 | `37F1:15BD` | 8 | 0/10 | 3,1 |
| 4 | `race.option.martian` | `race.martian` | 100086713 → 100093802 | `37F1:15BD` | 9 | 0/10 | 4,1 |
| 5 | `race.option.venusian` | `race.venusian` | 100113524 → 100121377 | `37F1:15BD` | 10 | 0/10 | 5,1 |
| 6 | `race.option.mercurian` | `race.mercurian` | 100140424 → 100149030 | `37F1:15BD` | 11 | 0/10 | 6,1 |
| 7 | `race.option.tinker` | `race.tinker` | 100167402 → 100173735 | `37F1:15BD` | 8 | 0/10 | 7,1 |
| 8 | `race.option.desert_runner` | `race.desert_runner` | 100194132 → 100205792 | `37F1:15BD` | 15 | 0/10 | 8,1 |
| 9 | `race.heading.terran` | `race.terran` | 100221773 → 100226552 | `37F1:175D` | 6 | 15/0 | 3,3 |

完整 SHA-256 在 `text/menu-events.tsv`。九筆 hash／length 已逐一對回
`workplace/probe/phase8-string-01.bin` 至 `09.bin` 的長度前綴 payload；兩個 Terran 顯示
雖共用 `race.terran` 譯文鍵，仍由不同 caller、長度、hash、色號與座標形成不同事件身分。

## dosgolem 觀測工具

- `apps/buckrogers.TextRecorder` 在 entry 只計算 SHA-256 並保存 typed metadata，不保留
  `original []byte`。
- 只有 return address、相同 `SS`、`SP == entry SP + 0x10` 同時成立才提交。
- 錯誤 SS／SP、巢狀 frame 與不相關 IP 均有失敗即關閉測試。
- `cmd/buckrogers-text-receipt` 只使用 dosgolem internal state；未擴張 `oracle` 公開的
  持久化 state API，也沒有輸入翻譯、renderer 或記憶體寫入能力。
- dosgolem 本機 commit：`98f3bec55d633cc2a69099f187848af4d765b7d1`；未推送其遠端。

第一次重播把 Enter 在 state 載入後立刻排入，九筆事件雖正確但整體提前 9,971 道指令；
它不符合舊收據的固定輸入，未採為正式結果。工具改成明確的 `-bios-enter-at 100010000`
後乾淨重跑，所有 entry step 與既有第 4／7 階段證據一致。

## 資料與驗證

- `tools/menu_events.py`：精確 header／欄數、UTF-8、連續 sequence、key／identity 唯一、
  SHA-256、caller 格式、色號／座標 bounds，以及事件與 `menu.zh-TW.tsv` 雙向覆蓋。
- `tools/menu_receipt.py`：拒絕額外原文欄位，逐筆比對 JSON 與 TSV，並驗證 entry／post-call
  嚴格順序、執行範圍與固定 BIOS 輸入。
- 專案正式 Python 測試共 32 項通過；真實 receipt verifier 通過。

## 能力邊界

本階段只完成一條正常 Enter 路徑的 typed identity inventory。正式覆繪仍須等待：

- 使用者決定 2×／3×；
- 每個中文欄位的 text-safe rectangle 與選取反白策略；
- `xlate.Stamp` 接線後的原文／繁中同狀態像素 A/B；
- 存讀檔、更多選單、訊息捲動及其他文字路徑的獨立生命週期證據。
