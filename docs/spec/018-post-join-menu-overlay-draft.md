# 018 — 加入角色後功能選單輸出端覆繪

狀態：**READY；僅限七項固定選單文字、已量初畫與逐列 Down 重畫。已有局部 runtime A/B，未達 CONFORMED。**
日期：2026-09-23

獨立審查與固定輸入見[第一百八十一階段](../re/phase-181-post-join-menu-ready-review-candidate.md)。
此 READY 僅授權 dosgolem 正式 loader、watcher、generation core 與 RGBA presenter 的限縮實作；
局部原版／繁中同狀態 A/B 見[第一百八十二階段](../re/phase-182-post-join-menu-runtime-ab-partial.md)，
逐幀失效與範圍外離頁仍缺，不能宣稱整個選單已中文化或 CONFORMED。

## 範圍、停止線與權利邊界

原版英文仍須先完整繪製；候選覆繪只能在 dosgolem RGBA 輸出端以原文 exact
identity 辨識、清除該列原版英文安全矩形後繪製繁中。不得修改 `GAME.OVR`、原版
記憶體、indexed framebuffer、BIOS 輸入、檔案、存檔、遊戲規則或比較／查找。

本候選只涵蓋正常「Right → Enter 離開名冊 → 功能選單」後的七項固定文字，及該
畫面從第 13 列依序 Down 到第 20 列的普通／反白重畫。舊收據中的 Enter
實際發生於 row 12 `Create New Character` 選取後，**不是** row 21 `Exit to DOS`；
真正 Exit Enter 尚未完成審查。其他項目的 Enter、row 12／17／21、上方動態角色資料、row 24 提示、
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
| 6 | `post_join_menu.option.show_characters_game` | 19 | 17 | 136 | 8 |
| 7 | `post_join_menu.option.begin_adventuring` | 20 | 17 | 136 | 4 |

兩份私有 `cycle-exit-a/b.json` 均為 SHA-256
`5b4c8f66ffd72651344c0dbb45de5946d273276b933dc9d4b902d69297841c36`，與其 framebuffer
`d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd` 相同；它們只支撐
本節的有限路徑，不證明其他選單行為。

## READY 幾何、錨點與溢位策略

每列使用半開 logical text-safe rectangle
`[72, 72+8×original_length) × [8×row, 8×row+8)`；draw anchor 是 `(72, 8×row)`。
矩形來自同一筆 original length，清除範圍保持英文寬度，不能為中文加寬。所有列均為
單列、8-pixel cell 對齊、`single-line-reject`；任何缺字、空譯文、超出 cell 容量、
非 8-pixel 高度或不在這七筆的 key 一律失敗即關閉，不能截斷、換行或自行改譯。

本機 `workplace/current-font/buckrogers-eten-top-pad.golemfnt` 現行 READY 字型 SHA-256 為
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。原先已審查的
1026-glyph SHA-256 `ef9fb6c9c2206a98286089888d3cf554a8fb491738f76fe0559bf7bcdcdbbc2d`
僅保留為歷史定位；加入主機介面 catalog 後曾暫停此 READY，完成新字型獨立重審才恢復。
現行字型對七筆譯文的靜態 raster containment 為零缺字、零墨跡外溢：
2×使用 16×16 cell／ink，safe rect 與 anchor 均乘 2；3×
使用 24×24 cell、22×22 ink、每 cell `(1,1)` offset，safe rect 乘 3、anchor 為
`(72×3+1, 8×row×3+1)`。這是 content-safe 靜態驗證，**不是**正式 runtime A/B。

## READY typed request 與 generation 契約

已審查的版控 `post-join-menu-events.tsv`、`post-join-menu-variants.tsv` 與
`post-join-menu.zh-TW.tsv` 僅作本限縮範圍的 immutable READY fixture；正式 loader
須固定第一百八十一階段的雜湊、逐筆驗證 schema 與 exact identity，任何變更都須回到 DRAFT
重審。可丟棄模型從私有 receipt 驗到下列有限序列：

1. 初畫原子 generation：七筆依 sequence 的 `37F1:15BD` 普通請求，再接 row 13 的
   `37F1:175D` 反白請求。
2. 每次已量 Down 原子 replacement：前一反白 row 的 `37F1:1856` 普通請求，緊接下一
   row 的 `37F1:175D` 反白請求；僅接受 row 13→14→15→16→18→19→20。
3. partial、duplicate、reordered、caller／style／identity 不符，或未證實 row 的請求都
   使 pending 與 active 全部失效；不得保留半組 stamp。

row 20 normal redraw 必須先失效第七代；不得以未收錄 row 21 selected 或稍後
row 12 Enter 的全選單 clear 讓舊 stamp 繼續作用。

此模型不推斷 Down 之後的 row 21／row 12，也不把 prompt row 24 重畫視為選單 lifecycle。

## 已量 row 12 Enter clear 與 active pre-write 失效契約

雙重原版事件顯示，row 21 `Exit to DOS` 於 step `124900535` 已回復普通，
row 12 `Create New Character` 於 `124909479` 反白；其後合法 Enter 由
`INT 16h AH=00` 於 step `125100053` 消費。原始短字串、檔案 offset 與
SHA 對照見[第一百八十三階段勘誤](../re/phase-183-post-join-exit-identity-corrigendum.md)。
step `125119490` 的 `026F:029C` 是第一筆與七列相交的全選單 clear；receipt 的含端點
格座標 `left=1, top=2, right=38, bottom=22` 換算成半開像素矩形
`[8,312)×[16,184)`。它保留為原版 clear 證據，但不是 complete cycle 的 active-generation
boundary，亦**不是** Exit Enter 的清除證據。完整 A000 observer 的勘誤見[第一百八十階段](../re/phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)：
每代最早相交 pre-write 都是更早的 `0763:184D` glyph write，包含同值寫入。正式 watcher
必須在任何相交 A000 pre-write 先失效，再僅依完整 exact variant generation 重建；不可只攔
`026F:029C` 或依 framebuffer diff。

Down 期間 prompt 清除格 `[25,40)×[24,25)`（像素 `[200,320)×[192,200)`）不相交，
不得讓它清除選單 overlay。restore、machine stop、execution discontinuity、未知 writer
或 generation 不一致均須失敗即關閉；READY 僅授權依此契約接入正式 `VideoWrite`
hook；正式接線已有局部收據，但未覆蓋真正 Exit Enter。

## READY 審查結果與實作後驗收

`workplace/phase162-post-join-menu-ready-candidate/verify_post_join_menu.py` 僅是 ignored
原型，從 phase 161 receipt 驗證 21 個 versioned identity（七初畫普通、七普通回寫、七反白），
七個 unit tests 包含 2×／3×字型 containment、zero-ink、partial、duplicate、reorder、
錯 caller／style、完整 A000 observer 與 row20→未知 row21 的負例。它的輸出
`receipt.json` 記錄輸入雜湊、逐列 safe rectangle／anchor、pre-write 邊界與拒絕條件。

主代理在 Docker 內獨立回讀 21 筆 variant、七筆譯文、phase 161 與權威 fork phase 180
雙重收據、字型雜湊，並重跑七項可丟棄正反例通過；第一百八十一階段固定審查輸入。
unknown row21、restore／stop、unknown A000 writer、mixed／partial generation 均明定為
失敗即關閉。正式 watcher、loader、generation core 與 presenter 是 READY 後的實作工作；
完成後才做 2×／3× runtime 同狀態 A/B、
矩形外零差、同幀 pre-write active→empty、row20→未知 row21／restore／stop／unknown writer
production failure matrix 與無殘字，符合者才可標 CONFORMED。其他功能選項、離頁／重入、
完整開機或存讀檔不在此限縮範圍，不能外推。完整 READY 獨立審查見
[第一百八十一階段](../re/phase-181-post-join-menu-ready-review-candidate.md)。

## 2026-09-23：真正 Exit 提示的 DRAFT 排除範圍

[第一百八十八階段](../re/phase-188-exit-prompts-draft-evidence.md)以雙重正常 N 與
Y→Y 原版重播確認 row 21 選取與兩個 row 24 提示的 exact identity，並量到
其間相交 A000 pre-write。row 24 的六格可見選擇尾碼另走 glyph path，具有
隨狀態變化的多色／反白段落；不能套用「快捷字母一律白色」的假設。
第二提示在 DOS 退出前沒有自然相交清除，終止時須另有失效契約。
這些仍屬 DRAFT，**不**擴張上述七列 READY fixture，也不授權提示 watcher、
譯文 TSV 或正式 Exit 覆繪。

## 2026-09-23：row20 普通回寫的限縮清層 A/B

[第一百九十二階段](../re/phase-192-post-join-menu-prewrite-runtime-ab.md)沿相同
合法加入角色 state 與十筆鍵，在 row20 普通回寫前、return 後但未知 row21
entry 前各停一次。control、2×、3× 的 JSON 在兩個停點逐 byte 相等；
回寫後 2×／3×覆繪 RGBA 均逐 byte 等於同畫面 baseline。正式元件測試
另固定同值 A000 pre-write 也清空作用層。這補足固定分支的**回寫後**
無殘字證據，仍不是逐指令 runtime active→empty 收據，更不覆蓋真正 Exit
Enter、兩個提示或其他選單分支；spec 018 繼續維持七列限縮 READY。
