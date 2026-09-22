# 016 — 第七頁固定劇情輸出端覆繪

狀態：**CONFORMED；僅第七頁固定六行與已量合法 Enter 進出。**
日期：2026-09-23

正式 runtime、同狀態 A/B、同程序 active→clear 與雙倍率失敗矩陣的
限縮驗收見[第一百五十六階段](../re/phase-156-story-page7-runtime-ab-pending-failure-audit.md)。
完整開機、其他離頁及遊戲內存讀檔不在此狀態範圍。

## 玩家可見範圍與權利

原版英文由 DOS 正常繪製；繁中只能由 dosgolem 輸出端 RGBA layer 覆繪。
不得改 `GAME.OVR`、原版記憶體、indexed framebuffer、BIOS 輸入、
檔案／存檔、規則、查找或比較。原文事件身分是穩定 key；譯文不得
回流原版語意路徑。

只涵蓋第七頁 row 17–22、column 1 的固定六行。右側動態人物資訊、
row 24、其他第七頁文字、第八頁、手冊、其他入口／出口及遊戲內
存讀檔均排除。原版程式／資料、完整事件、畫面、state、倚天字型與
衍生字型只能留在 ignored `workplace/`，不得進 Git、GitHub 或公開包。

## 原版證據、位址與推論等級

原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
工具為本機 dosgolem HEAD
`0ce49482d3e47a30ebadd530c56c7a02303b10e7`、Go 1.26.7；
runner SHA-256
`6039c6d97d57a6cc30efc1e03bee28b2e4a817e5bbae9d1dc2fd982149a35e66`。
地址均為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址或
檔案 offset。完整私有收據及重播條件見
[第一百五十三階段](../re/phase-153-story-page7-ready-prerequisite-diagnostics.md)。

已證實：合法第六頁 state SHA-256
`d20cbc0bf0b7425ab29b26a59666b91bbd32c1e5776ee9593190b4cd8918fcb5`
於 step `331000000` 接受正常 BIOS Enter，六行 190 glyph 的長度為
`36/36/37/38/38/5`。`text/story-page7-events.tsv` 的六筆原文
length／SHA、step、row／column 是 exact identity。逐字 caller
`0763:04FF`、glyph guard `0763:026B`；190/190 筆皆由
`0763:03D6` opcode `0xCA` 返回 `0763:04FF`，同 SS、相對
`SP+0x12`，mode／repeat `1/1`、背景／前景 `0/10`。七個 ABI word
的高位皆零；低位依序映射
`mode, glyph, repeat, background, foreground, row, column`。
entry A/B 原版收據逐 byte 相同。

上述 TSV 的絕對 entry／post step 是**固定排程原版收據的精確來源定位**，
不是正常玩家 runtime 必須等於的全域時鐘。玩家在不同時刻合法按 Enter
仍應看到相同繁中；runtime 的 step gate 是每筆 entry<post、跨 glyph／
行嚴格遞增，以及執行不連續即清空，不能用絕對步數鎖死合法路徑。
TSV loader 仍須核對六筆固定觀測步數，防止 catalog provenance 漂移。

已證實：從合法第七頁 state SHA-256
`e869b67264539aff95ca5929a9858c74475feea47e0c7b3a505ea9cd0aa9a460`
於 step `341000000` 接受 Enter，最早與六行安全矩形相交的
原版 pre-execution write 是 step `341018656`、`0CF4:1B3A`、
`ES:DI=A000:AA08`、`CX=304`。exit A/B 收據逐 byte 相同。
這只證明該合法離頁的候選失效錨點，其他轉場未知。

## READY typed contract

邏輯安全矩形為半開 `[8,320)×[136,184)`。2×每中文字模 16×16；
3× output cell 24×24，中文墨跡 22×22、offset 1。本機
GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`
對本頁 52 個不同字元零缺字；2×／3×靜態墨跡分別 3,149／5,981
像素，均未越出對應放大矩形。譯文來自
`text/story-page7.zh-TW.tsv` 的 `runtime-editorial`，不是手冊逐字引文。

只有六筆均以 sequence 1..6 完整命中原文 length／SHA、caller／guard、
style、row／column、逐字 return、SS／SP、step 順序、七 ABI word
高／低位與對應字模後，才可原子提交一個 group。非 READY catalog、
缺 key、缺字、partial／duplicate／錯序、identity／style／ABI／
return／stack／step drift、未知回呼與 execution discontinuity，
一律不得產生局部繁中 stamp。
此處 `step drift` 指 runtime entry／post 逆序、重複或跨事件倒退，
不是與固定收據絕對步數不同。

僅在 `0CF4:1B3A`、`ES=A000` 的 Mode 13h `DI/CX` 寫入半開 span
**逐列實際相交**安全矩形時，於原版執行前清除 active／pending group。
row 137 `x=0..7`、row 184 及其他不相交寫入沒有清除權；跨行 span
只有碰到安全列的 x≥8 區段才算相交。restore、machine stop 與
不連續 handoff 清空 group。這些邊界已在可丟棄 typed-core 驗證；
正式 runtime 尚須重驗。

## CONFORMED 驗收閘門

正式 dosgolem watcher／presenter／CLI 完成後，從同一合法原版
state、同一 BIOS Enter 排程重生 control、2×、3×。六 key 需命中、
無缺字；RGBA 差異只在安全矩形內，原版 CPU／DOS／BIOS／
檔案操作、indexed framebuffer 與 palette 必須相等。
在已量 Enter 離頁，最早相交 pre-write 同幀清除，離頁終態 RGBA
與 baseline 逐 byte 相同且無殘字。正式 2×／3×應各有完整
失敗即關閉矩陣，尤其 ABI 高／低位、hash 最後 glyph、字型缺字、
return／stack／step、未知／不相交／相交 write、非 READY catalog
及恢復後不復活。未完成這些驗證前不可標 CONFORMED 或稱已中文化。
