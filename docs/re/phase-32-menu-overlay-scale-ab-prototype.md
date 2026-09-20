# 第三十二階段：功能選單覆繪倍率 A/B prototype

## 結論

以第 30／31 階段的同一 steady／Down 原版 indexed framebuffer、正式繁中 catalog、正式
text-safe rectangles 與同一份 GOLEMFNT，dosgolem `xlate.Draw` 已各產生 2×、3× 功能選單
覆繪。兩批完整重生逐檔相同；四份收據均為零缺字、零矩形重疊、零安全矩形外差異，所有
ink rectangle 都落在核准範圍內。

這是**已證實的離線 prototype**，不是 runtime renderer 完成證據。正式倍率仍待使用者確認；
未選定前，選單覆繪 DRAFT 不升為 READY。

## 原版與工具證據

- steady indexed framebuffer SHA-256：
  `d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd`。
- Down indexed framebuffer SHA-256：
  `efaa3d88ea3c1f05aff308b86f796c4634845304c63eb5c92cc7e1d0a1a278d0`。
- 8-bit RGB palette SHA-256：
  `045796505f7ec3115cec8632ca7a29e6391687a2a013198e38dd68dd5b3564eb`。
  此 `.pal` 是 dosgolem `cmd/probe.writeShot` 的 `machine.Palette()` 輸出，不是 raw 6-bit DAC；
  初版 prototype 曾誤作第二次 6→8 轉換，目視前已依原始碼契約訂正並重生全部收據。
- GOLEMFNT SHA-256：
  `553df09b6accd101995a2781819ba9bee84a6220f0db5bba4437df1ccc458fe7`。
- 事件／矩形／譯文 SHA-256：`973a6a1e…da2e`／`3e37efca…982f`／`ca331983…8077`。
- dosgolem 診斷命令 commit：`09f580877b0d1e34ef00fa44eddefa12898b7e53`；規格
  `013-buck-rogers-menu-overlay-scale-prototype` 已為 CONFORMED，未推送 dosgolem 遠端。

所有動態畫面都是 dosgolem 320×200 Mode 13h indexed buffer；本階段不引用 IDA 位址，亦
不把 event key 當成原版符號名稱。

## 同狀態畫面集合

steady 與 Down 各覆繪七個目前可見事件：提示、一筆 selected variant、其餘 normal 選項。
普通選項的 text-safe rectangle 從 col 1 清除縮排原文，中文 draw anchor 在 col 3；診斷命令
以兩個全形空白格表達 offset，讓既有 `xlate.Stamp` 清除完整矩形而只從正式 anchor 畫字。

固定終點中的 selected row 在原版畫面本來就是黑底黑字：steady 隱藏 Terran，Down 隱藏
Martian。prototype 忠實沿用 event 色號與同一 palette，因此中文 selected row 同樣不可見；
這不是缺字或漏接，也沒有為了展示效果自創高亮色。正式 runtime 若要保留原版閃爍／反白
時間行為，仍須在選定倍率後以連續幀驗證，不能從本階段單一終點外推。

## 2×／3× 比較

| 維度 | 2× | 3× |
| --- | --- | --- |
| 輸出 canvas | 640×400 | 960×600 |
| 原版 8×8 格 | 16×16 px | 24×24 px |
| 16×16 glyph ink | 填滿格 | 置中，四邊 4 px |
| 三字選項整體 ink 寬 | 47 px | 63 px（字間 8 px） |
| 四字選項整體 ink 寬 | 63 px | 87 px（字間 8 px） |
| glyph ink 高 | 16 px | 16 px |
| 安全矩形外差異 | 0 px | 0 px |
| 缺字／矩形重疊 | 0／0 | 0／0 |

2× 的 640×400 canvas、約 16×16 CJK cell 與 PC-98 Golden Box 多作品常見密度一致；3×
保留更高輸出解析度，但 glyph ink 仍為 16×16，視覺上較小且每字間留 8 px。比較來源包含
[Champions of Krynn PC-98](https://www.mobygames.com/game/833/champions-of-krynn/screenshots/pc98/)、
[Death Knights of Krynn PC-98](https://www.mobygames.com/game/2219/death-knights-of-krynn/screenshots/pc98/)
及 Forgotten Realms 四作的 PC-98 畫面；只採用 canvas、CJK cell 與資訊階層模式，未複製
框線、配色、圖像或文字。

Codex 建議仍是 **2×**：同一邏輯容量下字級較大、字距緊密，且與既有 Golden Box CJK
閱讀密度更接近。這是建議，不是已採用決策；改選 3× 也不需改遊戲狀態或 catalog，但正式
畫面收據、layout 規格與後續玩家驗收會以不同 canvas 重做。

## 可重生收據

被 Git 忽略的輸出位於 `workplace/phase32/output/`：`a/`、`b/` 是兩批完整重生，並列圖為
`menu-scale-ab-contact-sheet.png`。並列圖每列由左至右是原版 3× 最近鄰、2× 繁中原生圖置中
於 960×600 黑底、3× 繁中原生圖；上列 steady、下列 Down，沒有對 2× 圖做 1.5 倍插值。

| 收據 | JSON SHA-256 | 繁中 PNG SHA-256 |
| --- | --- | --- |
| steady 2× | `ae796fc1edaee8643591a81a8700749e693033e198b9c49cf36b9b7c44aeed13` | `f9cd4c3aa93123b3a228527d2f98509e89df0c688b9991ef16af889a8b0766df` |
| steady 3× | `06c342ab67bc2c4b549adf10af1c9d38feafa40f3446ad9b9f9df6d6b8497140` | `eebe4739c87e83b00334bf55005ea245560d7474ffb1843aeea347d4ce4c7e12` |
| Down 2× | `0e9ee862bf06bc99c05701cca8f675e63f482727fbde20f295aca036414e66d3` | `e958394bb72f987b410c54622b61db9c5cec3a48cb1c707e7d4f7e8e7ca50c16` |
| Down 3× | `2c0dd1d027a4f99c34b6746d0a48fbc446d4af6d3c33962a930ddcbbfaaed758` | `237e2f10b37d2abad859fa082f2c8e579e65c8999917e57c4d148bf2844b2f5a` |

並列圖 SHA-256：`c03f865e0d9b2f122a99f6d9007d7f12e2e9adaf83e0fb906b501b13e17babc1`。

## 驗證與停止線

- dosgolem 全部正式 packages test／vet、`apps/buckrogers` 與診斷命令 race detector 通過。
- 四份 PNG 已按原生像素實際檢視；2×／3× 都無半字、裁切或相鄰列碰撞。
- 本階段不驗證連續幀 blink、runtime `Layer.Frame` 定色／失效、轉場清除、手冊分頁輸入或
  存讀檔後重建。這些必須在使用者確認倍率、規格升為 READY 後進行。
