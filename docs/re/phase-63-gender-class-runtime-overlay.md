# 第六十三階段：性別與職業選單執行期繁中覆繪

日期：2026-09-21  
狀態：完成

## 結論

性別與職業的正式 exact request、繁中 catalog 與 text-safe rectangles 已接入 dosgolem
長存 `RuntimeMenuOverlay`。由功能選單正常進入性別、確認後進入職業，再按 Down 的完整路徑，
2×／3× 各兩次均決定性繪出繁中；性別 stamps 在轉場後消失，職業同原點 selected／normal
variant 不殘留。

本階段沒有設定產品預設倍率。手冊 Phase 62 的版面決策仍獨立等待使用者確認。

## 規格與實作

- dosgolem spec `036-buck-rogers-character-runtime-overlay`：READY 審查後實作，驗收後升
  CONFORMED。
- `buckrogers-text-receipt` 新增 `-gender-rects`、`-class-rects`；overlay 模式要求每個啟用
  catalog 都有同類 rect，拒絕孤兒 rect、缺表、部分旗標與非 2／3 倍率。
- 四類 rect 仍共用 `LoadMenuOverlayRects`／`MergeMenuOverlayRects`，沒有第二套 renderer；
  runtime identity 的 row／column／length 必須和 rect 完全一致。
- dosgolem 本機 branch `buck-rogers-cht-output-overlay` commit：
  `e1d2070`；依權利邊界未推送其遠端。

## 正常路徑收據

固定 state 為 `workplace/probe/after-bios-space-100m.state`，原版素材唯讀掛載到 `/orig`。
BIOS 排程：Enter #100,010,000、#100,240,000、#100,400,000，Down #100,650,000；停止於
#100,700,000。

| 收據 | 結果 |
| --- | --- |
| baseline JSON | `7e2cc671…1742f` |
| raw framebuffer | 五份皆 `49d8b036…cccc81c` |
| 2× JSON／RGBA | `0978effc…844b2`／`cd62698f…cc8c2`，兩次逐 byte 相同 |
| 3× JSON／RGBA | `74d3cac8…d0208`／`b769435f…e6725`，兩次逐 byte 相同 |
| 合併字型 | 77 glyphs，`3714d47c…7545ae` |

每份均為 24 events、24 requests、24 overlay actions、0 catalog miss／pending／drop；overlay
JSON 移除 presentation 欄位後逐欄等於 baseline。終態 active keys 只有八筆職業畫面輸出，
沒有性別 key 或舊 selected variant。

## 像素與目視驗收

- 2×：安全矩形內 3,288 個差異像素，外部 0。
- 3×：安全矩形內 6,225 個差異像素，外部 0。
- 原始解析度 `workplace/phase63/a2.png`、`a3.png` 已目視確認金框、文字列與 `XIT` 提示未被
  覆蓋，沒有半字、跨列或舊性別殘字。
- selected Warrior 仍使用原版 palette 的黑底黑字，故終態看不見該列中文；這是 Phase 41
  已證實的原版樣式，本階段沒有自行改色。

## 驗證與勘誤

- `tools/character_runtime_overlay_receipt.py` 固定輸入／輸出雜湊、雙重決定性、baseline
  projection、active keys、request/action 一對一、raw framebuffer 與像素 containment。
- 專案完整 Python 回歸由 103 增至 105 項，全數通過。
- dosgolem 全部正式 packages test／vet、`apps/buckrogers` 與 receipt command race detector
  通過。
- 第一次載入把 `workplace/original/` 掛到 `/orig`，但 state 需要檔案直接位於 `/orig`；改掛
  `workplace/original/BRcdoom/` 後解決。第二次誤用名稱相近的 `after-space-100m.state`，嚴格
  24-event 閘門以 23 events 拒絕；改回權威 `after-bios-space-100m.state` 後重生既有 24-event
  時序。兩次都保留為環境／輸入定位勘誤，沒有放寬產品期望。
