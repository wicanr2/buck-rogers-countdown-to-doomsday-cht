# 018 — 加入角色後功能選單輸出端覆繪

狀態：**DRAFT；僅為 READY 審查候選，不授權正式實作。**  
日期：2026-09-23

## 範圍、停止線與權利邊界

原版英文仍須先完整繪製；候選覆繪只能在 dosgolem RGBA 輸出端以原文 exact
identity 辨識、清除該列原版英文安全矩形後繪製繁中。不得修改 `GAME.OVR`、原版
記憶體、indexed framebuffer、BIOS 輸入、檔案、存檔、遊戲規則或比較／查找。

本候選只涵蓋正常「Right → Enter 離開名冊 → 功能選單」後的七項固定文字，及該
畫面從第 13 列依序 Down 到第 20 列的普通／反白重畫。只量到 `EXIT TO DOS` 的
Enter 離頁；其他項目的 Enter、row 12／17／21、上方動態角色資料、row 24 提示、
重新進入選單、存讀檔與完整開機都在範圍外。七項操作語意也仍為未知，這些譯文僅是
顯示層候選。

原版、savestate、雙重 receipt、截圖和倚天字型都只留在 ignored `workplace/`，不得
加入 Git、GitHub 或公開包。

## 原版證據與 identity

依[第一百六十一階段](../re/phase-161-post-join-menu-selection-and-exit.md)，原版
`GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；合法起點
`a-joined.state` SHA-256 為
`1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。工具為
dosgolem `1dafb0a857c42fbda7058157b7615e214a64ec64`、Docker 內 Go 1.24.13，位址是
dosgolem 8086 實模式 `segment:offset`。

七筆 base identity 位於 `text/post-join-menu-events.tsv`；21 個持久 exact variants 位於
`text/post-join-menu-variants.tsv`，每列各有 initial normal `37F1:15BD`／`0/10`、normal
redraw `37F1:1856`／`0/10`、selected `37F1:175D`／`15/0`。三種 caller 不能互換。
每一請求必須同時驗證 length、SHA-256、caller、色號、row、column；不得只按雜湊或
座標匹配。row 20 normal redraw 雖已證實，隨後的 row 21 selected 仍未收錄，必須 fail-closed。

| sequence | event key | row | 原版欄數 | 原文安全寬度 | 繁中 rune 數 |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | `post_join_menu.option.purge_character` | 13 | 15 | 120 | 4 |
| 2 | `post_join_menu.option.modify_character` | 14 | 16 | 128 | 4 |
| 3 | `post_join_menu.option.join_a_game` | 15 | 11 | 88 | 4 |
| 4 | `post_join_menu.option.view_character` | 16 | 14 | 112 | 4 |
| 5 | `post_join_menu.option.remove_character_from_team` | 18 | 26 | 208 | 7 |
| 6 | `post_join_menu.option.show_characters_game` | 19 | 17 | 136 | 7 |
| 7 | `post_join_menu.option.begin_adventuring` | 20 | 17 | 136 | 4 |

兩份私有 `cycle-exit-a/b.json` 均為 SHA-256
`5b4c8f66ffd72651344c0dbb45de5946d273276b933dc9d4b902d69297841c36`，與其 framebuffer
`d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd` 相同；它們只支撐
本節的有限路徑，不證明其他選單行為。

## DRAFT 幾何、錨點與溢位策略

每列使用半開 logical text-safe rectangle
`[72, 72+8×original_length) × [8×row, 8×row+8)`；draw anchor 是 `(72, 8×row)`。
矩形來自同一筆 original length，清除範圍保持英文寬度，不能為中文加寬。所有列均為
單列、8-pixel cell 對齊、`single-line-reject`；任何缺字、空譯文、超出 cell 容量、
非 8-pixel 高度或不在這七筆的 key 一律失敗即關閉，不能截斷、換行或自行改譯。

本機 `workplace/current-font/buckrogers-eten-top-pad.golemfnt`（SHA-256
`ef9fb6c9c2206a98286089888d3cf554a8fb491738f76fe0559bf7bcdcdbbc2d`）對現有七筆 DRAFT 譯文的靜態 raster containment
候選為零缺字、零墨跡外溢：2×使用 16×16 cell／ink，safe rect 與 anchor 均乘 2；3×
使用 24×24 cell、22×22 ink、每 cell `(1,1)` offset，safe rect 乘 3、anchor 為
`(72×3+1, 8×row×3+1)`。這是 content-safe 靜態驗證，**不是**正式 runtime A/B。

## DRAFT typed request 與 generation 候選

可丟棄模型只接受記憶體中的「已審查 READY fixture」；版控 TSV 是 DRAFT，必須遭
正式 loader 拒絕。它從私有 receipt 驗到下列有限序列：

1. 初畫原子 generation：七筆依 sequence 的 `37F1:15BD` 普通請求，再接 row 13 的
   `37F1:175D` 反白請求。
2. 每次已量 Down 原子 replacement：前一反白 row 的 `37F1:1856` 普通請求，緊接下一
   row 的 `37F1:175D` 反白請求；僅接受 row 13→14→15→16→18→19→20。
3. partial、duplicate、reordered、caller／style／identity 不符，或未證實 row 的請求都
   使 pending 與 active 全部失效；不得保留半組 stamp。

row 20 normal redraw 必須先失效第七代；不得以未收錄 row 21 selected 或稍後 `EXIT TO DOS`
clear 讓舊 stamp 繼續作用。

此模型不推斷 Down 之後的 row 21／row 12，也不把 prompt row 24 重畫視為選單 lifecycle。

## EXIT TO DOS 的 DRAFT pre-write 失效候選

在選取 `EXIT TO DOS` 後，合法 Enter 由 `INT 16h AH=00` 於 step `125100053` 消費。
step `125119490` 的 `026F:029C` 是第一筆與七列相交的全選單 clear；receipt 的含端點
格座標 `left=1, top=2, right=38, bottom=22` 換算成半開像素矩形
`[8,312)×[16,184)`。它保留為原版 clear 證據，但不是 complete cycle 的 active-generation
boundary。完整 A000 observer 的勘誤見[第一百八十階段](../re/phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)：
每代最早相交 pre-write 都是更早的 `0763:184D` glyph write，包含同值寫入。候選 watcher
必須在任何相交 A000 pre-write 先失效，再僅依完整 exact variant generation 重建；不可只攔
`026F:029C` 或依 framebuffer diff。

Down 期間 prompt 清除格 `[25,40)×[24,25)`（像素 `[200,320)×[192,200)`）不相交，
不得讓它清除選單 overlay。restore、machine stop、execution discontinuity、未知 writer
或 generation 不一致均須失敗即關閉；這些是候選 adapter 契約，尚未授權接入正式
`VideoWrite` hook。

## 可丟棄驗證與 READY 缺口

`workplace/phase162-post-join-menu-ready-candidate/verify_post_join_menu.py` 僅是 ignored
原型，從 phase 161 receipt 驗證 20 個已接受 request（七初畫普通、初始反白、六組
Down normal/selected），四個 unit tests 包含 2×／3×字型 containment、zero-ink、partial、
duplicate、reorder、錯 caller／style 與非相交 prompt clear 的負例。它的輸出
`receipt.json` 記錄輸入雜湊、逐列 safe rectangle／anchor、pre-write 邊界與拒絕條件。

主代理已在 Docker 內獨立回讀此原型並重跑四項測試；本候選仍維持 **DRAFT**，
但不以正式 watcher／presenter 或 runtime A/B 作為 READY 的前置條件。真正仍缺的
READY 證據是：

- 21-row table、可丟棄 validator 與完整 A000 observer 已取得；仍待獨立審查把 source／
  receipt hashes、variant 表與「先失效、後 exact 重建」串為狹窄契約。DRAFT TSV 不得直接
  成為 production loader 輸入。
- 正式 watcher 尚未證明能在所有 observed／unknown A000 writer 的同幀 pre-write fail-closed；
  混合／部分 generation、row20→未知 row21、restore／stop 負例也尚未進 production matrix。
- 前述字型靜態 containment 與來源 SHA 已取得，但需由獨立審查把版控文字、變體身分、
  幾何、原版收據及失敗矩陣串成一份狹窄可實作契約。

若這些證據通過，才可把**固定七項與已量 Exit 路徑**限縮升 READY，接著實作正式
watcher／presenter；完成後再做 2×／3× runtime 同狀態 A/B、矩形外零差、離頁無殘字與
production failure matrix，符合者才可標 CONFORMED。其他功能選項、離頁／重入、
完整開機或存讀檔不在此限縮範圍，不能外推。
