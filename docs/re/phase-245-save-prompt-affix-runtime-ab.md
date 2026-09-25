# 第二百四十五階段：儲存詢問前後綴覆繪正式 A/B

日期：2026-09-26  
狀態：**已證實／各名字單次重播。** 對應[規格 025](../spec/025-save-prompt-name-affix-overlay-draft.md)。

## 實作與輸入

- 本機 dosgolem fork `4d2d259`：`TextRecorder.RegisterAffix`、身體圖示
  catalog 的六筆 exact 加一筆前後綴、成對 stamp 與成對失效、runner
  `-body-icon-affixes`。`go test -race ./apps/buckrogers ./cmd/buckrogers-text-receipt`
  與 vet 通過。全 module 測試只有 `frontend/ebiten` 因容器缺 X11 標頭無法編譯，
  該套件不使用本次改動的型別。
- runner 由乾淨 clone 建置，`vcs.modified=false`，SHA-256
  `04912f50…e590e377`。
- 主 repo：`text/body-icon-affixes.tsv` 新增；`body-icon-events.tsv` 剩六筆；
  譯文拆成「儲存」「？」；前綴矩形 `[0,40)`。Python 檢查 250 項通過，
  字元聯集不變，不需重建字型。
- 起點為各名字的 `*-body.state`（圖示屏初畫前），鍵序：圖示屏 Enter、`y`。

## 問句出現時

| 名字 | n | 2× 前綴／名字／後綴／後段 | 3× 前綴／名字／後綴／後段 |
|---|---:|---|---|
| `Z` | 1 | 298／0／47／0 | 650／0／117／0 |
| `BUCK` | 4 | 298／0／47／0 | 650／0／117／0 |
| `A 1.?` | 5 | 298／0／47／0 | 650／0／117／0 |
| `ABCDEFGHIJKLMNO` | 15 | 298／0／47／0 | 650／0／117／0 |

- 事件的 `slot_length` 等於名字長度；transition 為 body-selection →
  confirmation → save_prompt。
- 名字格與後綴之後的同列都是零差；矩形外零差、零缺字。
- 每個名字的 control／2×／3× indexed 逐位元相等，收據共同欄位全部相等，
  含 FileOps 17,640 筆。
- `BUCK` 的 move／refuse 回歸與改動前相同（3067／6486 像素）。

## 回答之後

- 沒有可寫存檔層時回答 `Y`：遊戲反覆找存檔目錄（5,059 次找不到），1.6M 步後
  畫面仍與問句畫面逐 byte 相同，stamp 仍 active 是正確狀態。
- 有 scratch 存檔層時回答 `Y`，或回答 `N`（回主選單）：出現 confirm 路徑外的
  新事件，watcher 失敗即關閉。離頁需要擴充路徑定義，規格 009 原本就排除此範圍，
  本階段未驗離頁無殘層。

私有收據與腳本留在 ignored `workplace/phase245-save-prompt-ab/`。
