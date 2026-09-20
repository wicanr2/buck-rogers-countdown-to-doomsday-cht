# 第八階段：功能選單繁中字型與版面 prototype

日期：2026-09-20  
狀態：prototype 已完成；產品字型與倍率仍待使用者決定。

## 證據與譯名

由固定狀態 `after-bios-space-100m.state` 經正常 BIOS Enter 重播，於九次
`0763:0424` entry 傾印來源，證實依序為 `Create New Character`、`Pick Race`、Terran、
Martian、Venusian、Mercurian、Tinker、Desert Runner 與 Terran 標題。前一階段已證實
第一筆背景／前景色號 0／10、row 12、column 9、20 個 8×8 格。

中文說明書掃描 `SCAN0352_006.jpg` 至 `SCAN0352_007.jpg` 明列譯名：地球人、火星人、
金星人、水星人、萬能工匠、沙漠跑者；這些名稱已寫入 `text/menu.zh-TW.tsv`。`Pick Race`
採介面動詞「選擇種族」，`Create New Character` 採「建立新角色」。兩者是 DRAFT 介面譯文，
不是手冊逐字摘錄。

原始 dump、掃描與 prototype PNG 只留在被忽略的 `workplace/`，不進 Git。

## 參考專案與授權邊界

- psychic-war 證實可重用的架構是：原版先照常畫英文，在整數放大畫布以背景色清除同一
  text-safe rectangle，再畫中文；生命週期由 post-call、指紋與明確清除事件管理。
- 該專案的 `xlate` 是遊戲無關的 `GOLEMFNT`／layout／stamp 層，可作後續 dosgolem 分支
  移植來源；其遊戲位址、譯文、倚天字模與完成聲明均不可直接搬用。
- curse_of_the_azure_bonds 的可重用經驗是 text-safe rectangle、字形涵蓋測試與閱讀字級／
  介面字級分離；其 PC-98／remake 畫面與資產不屬於本作輸出端 patch。
- 倚天 16×15／24×24 的散布權未確認；本階段不納入版控。Noto Sans TC 雖為 SIL OFL，
  既有小尺寸點陣化結果有斷筆。prototype 使用 GNU Unifont `unifont.hex.gz`，授權依
  `sangokushi/fonts/LICENSE-unifont.txt`；字型檔本身未複製進本 repo。

## 兩個可重生候選

共同基線是 raw 320×200 色號畫面；先最近鄰整數放大，才在輸出端覆繪。批准的邏輯矩形是
`x=72..231, y=96..103`，輸出矩形隨倍率等比放大。兩案都先完整填背景色號 0，因此原文
20 格全數清除；「建立新角色」六字只使用前六格，沒有越界或濾波。

| 候選 | 輸出 | 字模／格 | 配置 | 本機收據 SHA-256 |
| --- | --- | --- | --- | --- |
| A | 640×400（2×） | Unifont 16×16／16×16 | 字模填滿格，高度與其他 2× 英文一致 | `d95adc5739a0f2ad150f0929791aa3d2d20a349234e03d548af3c7cca44d2bbe` |
| B | 960×600（3×） | Unifont 16×16／24×24 | 四邊各留 4 px，字較小但保留 3× 輸出 | `7332e1aaf3a0b5732039cfb5deccde5f056556a2f0d358ea05321090c1b125f0` |

重生工具為 `tools/prototype_menu_overlay.py`。A 的中文視覺尺寸與相鄰英文相稱；B 延續
psychic-war 的 3× 畫布，但 16 點字置中後顯得較小。這是玩家可見取捨，尚未固化。

## 結論與限制

功能選單第一筆已具可追溯繁中、合法候選字型、text-safe rectangle 與兩種整數倍率收據；
因此可進入下一階段的 adapter prototype。尚未證實其他 dispatcher 的全部色彩／幾何，
也尚未把 `xlate` 移入本作 dosgolem 分支；本文件不宣稱 production、READY 或全遊戲完成。

