# 第三十階段：種族選單反白與文字安全矩形生命週期

日期：2026-09-20  
狀態：selection lifecycle 已證實；玩家可見繁中覆繪仍為 DRAFT。

## 結論

原版種族選單的方向鍵反白不是外部游標或 palette-only 效果。正常 BIOS Down 會先以
`bg/fg=0/10` 重畫舊選項內容，再以 `bg/fg=15/0` 重畫新選項；Up 以相反的兩筆重畫回復。
四筆都經 `0763:0424` dispatcher 與 return address／SS／SP guarded post-call 完成。

相同 #100,600,000 終點逐位元比較證實：steady 與 Down-only 只差
`(24,24)–(79,39)` 兩列、832 pixels；Down→Up 後的 64,000-byte indexed framebuffer 與
steady 完全相同。故 selection lifecycle 是「舊列 normal redraw → 新列 selected redraw」，
不能只在首次進畫面畫一次中文，也不能等矩形清畫面才重建。

## 固定輸入與位址空間

- 起點：被 Git 忽略的 `workplace/probe/after-bios-space-100m.state`，#99,999,999。
- 輸入排程：Enter #100,010,000、Down `scan=0x50/ascii=0` #100,240,000、
  Up `scan=0x48/ascii=0` #100,300,000。
- 終點：#100,600,000；原版素材唯讀掛載於 `/orig`。
- caller 均為 dosgolem runtime `segment:offset`，不是 IDA 線性位址或檔案偏移。
- 兩次事件收據 SHA-256 同為
  `b36385b232cc70cf2b3bf7baf96615f3863d0871ea562907c915d4d5819f3dc5`。

## 四筆 selection 事件

完整 content-free identity 位於 `text/race-selection-events.tsv`。

| phase | role | entry → post-call | caller | text key | len | bg/fg | row,col |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| Down | unselect-old | 100240549 → 100245328 | `37F1:1856` | `race.terran` | 6 | 0/10 | 3,3 |
| Down | select-new | 100245727 → 100251268 | `37F1:175D` | `race.martian` | 7 | 15/0 | 4,3 |
| Up | unselect-old | 100300594 → 100306135 | `37F1:1856` | `race.martian` | 7 | 0/10 | 4,3 |
| Up | select-new | 100306502 → 100311281 | `37F1:175D` | `race.terran` | 6 | 15/0 | 3,3 |

Terran／Martian 的 SHA-256 分別沿用已觀測內容 identity；repo 不保存原文全文。上述四筆中，
重新選取 Terran 與既有 `race.heading.terran` identity 相同；其餘三筆尚未加入 production
`menu-events.tsv`，所以現行 `MenuCatalog` 對它們會失敗即關閉。必須先擴充 event variants
與 lifecycle adapter，不能用 text key 或座標模糊命中。

## framebuffer 收據

| 畫面 | SHA-256 |
| --- | --- |
| steady，#100,600,000 | `d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd` |
| Down-only，同終點 | `efaa3d88ea3c1f05aff308b86f796c4634845304c63eb5c92cc7e1d0a1a278d0` |
| Down→Up，同終點 | `d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd` |

原始 64,000-byte indexed buffers 與 JSON 留在被 Git 忽略的 `workplace/phase30/`。
`tools/race_selection_receipt.py` 驗證兩次事件逐欄一致、固定輸入、四筆 identity、guarded
順序、三份 framebuffer 雜湊、832 pixels 與差異 bbox。

## logical text-safe rectangle

`text/menu-text-safe-rects.tsv` 對第 27 階段九個 event key 一對一定義 320×200 logical
清除矩形、draw anchor、單行容量及 `single-line-reject` overflow policy。矩形的
`x/y/width/height` 必須精確等於 `column×8 / row×8 / original_length×8 / 8`。

動態事件解出一個重要排版差異：一般種族選項從 col 1 輸出含兩格縮排的原文；被選取內容
則從 col 3 重畫不含縮排的文字。因此一般選項必須清除從 col 1 起的完整原文矩形，但中文
draw anchor 固定為 col 3。現有最長繁中譯文 4 格，小於最窄 6 格容量；所有矩形均在
320×200 內、8-pixel 對齊、單列且不侵入相鄰 row。此 logical contract 對 2×／3× 都成立，
不構成倍率選擇。

## 工具與驗證

- dosgolem `buckrogers-text-receipt` 新增嚴格、可重複的 `-bios-key-at` 排程與
  `-screen-out` 64,000-byte indexed framebuffer；diagnostic spec 011 已 CONFORMED。
- 專案 39 項 Python schema／receipt／geometry 測試全數通過。
- dosgolem 全部正式 packages test／vet 與 Buck Rogers／receipt command race detector 通過。
- dosgolem 本機 commit：`d55a4c84c3474034257cddf58d6fa32cff3d60d4`；未推送其遠端。

## 尚未完成

本階段沒有把三筆新增 variant 接入正式 catalog，沒有建立 selection overlay lifecycle adapter，
也沒有載入字型或繪圖。2×／3× 仍待使用者決定；中文像素 A/B 前不得宣稱選單已中文化。
