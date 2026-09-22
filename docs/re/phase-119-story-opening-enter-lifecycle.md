# 第一百一十九階段：首屏劇情 Enter 轉場 runtime lifecycle A/B

日期：2026-09-22
狀態：首屏五行的 **Enter→第二頁失效** 已由 dosgolem runtime A/B 重生；與 phase117
一併使規格 010 在固定五行及已量 Enter 路徑限縮 **CONFORMED**。

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

## phase160 重生、正規化比較與限制

本機 dosgolem `9f4c5f0` 補 strict catalog／generation／receipt gate、未知 epoch 清除及
2×／3× fail-closed matrix 後，以同一合法 state、既有私有 BIOS receipt 和同一程序 Enter
重生 control／2×／3×。Enter receipt SHA-256 為 control
`e136ba7dfd0d59e31ae4c5c35d669f5b3a8407cc9e5cf0ad0e27c6c80a97cc0d`、2×
`d842ce9479b9452b8fcd7f5ce0005eecdc631d750a313d6aade71595177c064f`、3×
`374a0b2ba95f068461fc6c94f2754d31a98c2ca06d8aab4a85765801e1372e2b`。兩覆繪組皆重得本階段
的 step／span／generation／active 5→0，終態 RGBA==baseline，且沒有 page2 overlay。
`state-compare` 對 control↔2×／3×均回 `equal=true`（machine
`90d7d987370c518e0a92b0aeeb1095eb884525b26808d987c3065c8bda089278`、DOS
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`）；raw `.state` bytes
不作比較。

## 勘誤與限制

這次將早期「row 137 是首筆 story-region write」訂正為「row 137 是首筆可見 indexed
pixel 差異」。更早的 row 136 write 可能填回相同色號，但它同樣覆蓋受批准 rectangle，故必須是
失效邊界。這也證明目前 watcher 的 generic `ES:DI`／`CX` span 判定是必要且正確；本階段沒有
把它縮窄成易漏掉 row 136 的硬編碼 step。

明確排除：在原版開機開始的完整玩家路徑、實際存檔／讀檔／state restore，以及其他離開
首屏的路徑。strict matrix 對未知 epoch 是 fail-closed，不等於上述實際玩家路徑；第二頁及
後續故事頁仍不在 spec010 CONFORMED 範圍。
