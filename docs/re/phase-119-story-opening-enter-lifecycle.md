# 第一百一十九階段：首屏劇情 Enter 轉場 runtime lifecycle A/B

日期：2026-09-22
狀態：首屏五行的 **Enter→第二頁失效** 已由 dosgolem runtime A/B 驗證；規格 010 仍維持
**READY**，因存讀檔／restore 與完整開機玩家路徑尚未驗收。

## 範圍與可重播輸入

本階段從 `workplace/probe/phase12-before-question.state`（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）開始，載入既有本機
首屏 A/B receipt 的合法 BIOS 排程，於 step `281000000` 再送入一次正常 Enter，停止於
`282000000`。排程、手冊答案、原版 state、原版檔與字型均只留在被忽略的 `workplace/`。

2×／3×均使用最新本機倚天 997-glyph top-pad 字型（見[第一百一十八階段](phase-118-story-draft-font-rebuild.md)），
但僅載入 READY 的 `story-opening-events.tsv` 與 `story-opening.zh-TW.tsv`；page2、page3、page4
的 DRAFT catalog 沒有傳給 runtime。

## 同狀態結果

兩個覆繪倍率與一份無覆繪 control 重播的終態 metadata 相同：

- machine memory SHA-256：`91fadf20ef018bd82fc95916c61336fabb0bf955cfd4a75198ca6d017aaa9f12`
- indexed framebuffer SHA-256：`a42a876fb37666c3ef4bc27df13665399aec914ba024725c4129b906089e8af6`
- palette SHA-256：`fa97ee0c556490cc1c64f09cc0d9ead7b9836ff58c7c9ac965cd5e316757242c`

每個覆繪 receipt 都只記錄一筆 content-safe invalidation：step `281020548`、
instruction `0CF4:1B3A`、`A000:AA08`、`CX=304`、generation `2`、`active_keys_before=5`。
這表示完整首屏 group 尚存在時，adapter 在原版 `REP STOSB` 執行前偵測到 row-aware video-span
相交並清除 output-only layer。終態在兩倍率都是 `active_keys=[]`、`drew=false`，且 overlay RGBA
逐 byte 等於同 frame baseline；story rectangle 外差異為 0。第二頁沒有被 DRAFT 譯文覆蓋。

私有收據與 PNG 位於 `workplace/phase118-story-opening-lifecycle/{2x,3x,control}/`；其中僅
`receipt.json` 的 metadata 可供本機再檢查，任何原文、答案或輸入值都不進 Git。

## 勘誤與限制

這次將早期「row 137 是首筆 story-region write」訂正為「row 137 是首筆可見 indexed
pixel 差異」。更早的 row 136 write 可能填回相同色號，但它同樣覆蓋受批准 rectangle，故必須是
失效邊界。這也證明目前 watcher 的 generic `ES:DI`／`CX` span 判定是必要且正確；本階段沒有
把它縮窄成易漏掉 row 136 的硬編碼 step。

尚未驗證：在原版開機開始的完整玩家路徑、存檔／讀檔／state restore 後的 lifecycle，以及其他
離開首屏的路徑。因此不將規格 010 升為 CONFORMED，也不外推至後續故事頁。
