# 第三十三階段：種族選取列閃爍與色盤生命週期

## 結論

在 dosgolem 正常 Enter 與 Enter→Down 路徑中，selected row 的 indexed pixels 並未消失：
selected Terran 是 290 個色號 15 背景像素加 94 個色號 0 glyph 像素；selected Martian 是
339 個色號 15 加 109 個色號 0。兩個色號在整個 #100,220,000–#109,990,000 取樣窗口內
RGB 都是 `(0,0,0)`，因此原版選取列是穩定的黑底黑字、玩家看不見，而非文字漏畫。

978 點內完整 palette 只有一個 SHA-256，完成重畫後 row region 也只有一個 SHA-256，且沒有
新文字事件。因此已**證實**本窗口內不存在 palette-only blink 或週期性 pixel redraw。
窗口以外保持 unknown；本結論不冒稱整場遊戲永久不變。

## 輸入、工具與位址空間

- state：`after-bios-space-100m.state`，SHA-256
  `cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`，起點
  #99,999,999。
- 正式事件資料 SHA-256：
  `973a6a1e247e7d9e16518a1a66266f340666d32e785f3f6f6652a890e830da2e`。
- dosgolem 診斷規格 `014-buck-rogers-selection-blink-receipt` 已 CONFORMED；本機 commit
  `41917c85007efe17154cb92422cba3fe6539ad88`，未推送 dosgolem 遠端。
- dispatcher `0763:0424` 與 caller 均為 dosgolem runtime `segment:offset`，不是 IDA 線性位址。
- 原版 `START.EXE`／`GAME.OVR` 根目錄唯讀掛載；收據不保存原文或譯文全文。

## 固定排程與取樣

兩條路徑都在 #100,010,000 排入 BIOS Enter。steady 不再送鍵；Down 路徑於 #100,240,000
排入 BIOS Down。自 #100,220,000 起每 10,000 steps 取樣，停止於 #110,000,000；每條恰
有 978 點，最後一點 #109,990,000。

每點保存完整 palette hash、色號 0／10／13／15 RGB、selected contrast、row 3
`[24,72)×[24,32)` 與 row 4 `[24,80)×[32,40)` 的 hash／色號計數，以及完成事件數。
palette SHA-256 全程固定為
`045796505f7ec3115cec8632ca7a29e6391687a2a013198e38dd68dd5b3564eb`：

| 色號 | RGB | 角色 |
| ---: | --- | --- |
| 0 | `(0,0,0)` | selected glyph／一般背景 |
| 10 | `(85,255,85)` | normal option glyph |
| 13 | `(255,85,255)` | prompt glyph |
| 15 | `(0,0,0)` | selected background |

色號 0 與 15 雖是不同 indexed value，顯示 RGB 相同，所以 `selected_contrast=false` 為
978／978。這也解釋第 32 階段繁中 prototype 為何忠實畫出不可見 selected row。

## Pixel／事件時間線

| 路徑與穩定起點 | row 3 | row 4 | 完成事件 |
| --- | --- | --- | ---: |
| steady，自 #100,230,000 | selected Terran `75ed8459…62c7`，`15:290, 0:94` | normal Martian `7f09284d…9ba7`，`0:339, 10:109` | 9 |
| Down，自 #100,260,000 | normal Terran `0b66513f…334a`，`0:290, 10:94` | selected Martian `5d6fe02f…43f`，`15:339, 0:109` | 11 |

第 30 階段細粒度事件仍提供重畫邊界：selected Terran 於 #100,221,773 entry、
#100,226,552 post-call；Down 後 normal Terran 為 #100,240,549–#100,245,328，selected
Martian 為 #100,245,727–#100,251,268。先前每 1,000 steps 的研究 probe 觀察到各 glyph
逐步把 normal 色號改成 selected 色號；正式長窗口收據則釘住完成後不再變動。

## 決定性與 verifier

- steady 兩次 JSON 逐 byte 相同，SHA-256 均為
  `4bacd03889f182070a826880be353cb998ffcb7c17219eeb7d33f92d43bef83f`。
- Down 兩次 JSON 逐 byte 相同，SHA-256 均為
  `339b6920ac26428514b4ca2eb4ac09769cac08d8a4bbfa707f15a1fbd8e67569`。
- `tools/selection_blink_receipt.py` 驗證 schema、輸入 hash、978 個 exact steps、palette 唯一、
  RGB、contrast、穩定 region hash、事件 identity／順序與零 pending／drop。
- 44 項專案 Python 測試通過；dosgolem 全部正式 packages test／vet、Buck Rogers 與診斷
  命令 race detector 通過。

## 對 runtime 覆繪的限制

未來 renderer 必須沿用原版 selection style：normal redraw 顯示繁中，selected redraw 在此
palette 下清除原文後呈現黑底黑字。不得因「選取項看不見」而自行換成白底、反色、游標或
取消 selection redraw；那會改變原版玩家體驗。若要改成較易辨識的現代高亮，必須另由
使用者做明確產品決策，不能混入忠實中文化路徑。

本階段沒有選 2×／3×，也沒有接入 `xlate.Layer.Frame`。正式 runtime 還需在選定倍率後驗證
post-call 建立 stamp、normal／selected 交替、矩形清除與 Escape 返回不殘字。
