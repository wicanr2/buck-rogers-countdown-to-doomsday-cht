# 第一百五十三階段：第七頁 READY 前逐字返回與離頁診斷

日期：2026-09-23  
狀態：**診斷、三輪獨立審查及勘誤後，第七頁固定六行限縮升 READY；正式 runtime 未接。**

## 固定輸入與工具

entry 從合法第六頁私有終態 `workplace/phase123-story-page6-enter/page6.state`
（SHA-256 `d20cbc0bf0b7425ab29b26a59666b91bbd32c1e5776ee9593190b4cd8918fcb5`）
於 step `331000000` 送正常 BIOS Enter，至 `340000000`。exit 從合法第七頁
私有終態 `workplace/page7-next-trace/page7.state`（SHA-256
`e869b67264539aff95ca5929a9858c74475feea47e0c7b3a505ea9cd0aa9a460`）
於 step `341000000` 送 Enter，至 `350000000`。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
地址均為 dosgolem 實模式 `segment:offset`，非 IDA 線性地址或檔案 offset。

在無網路、有界 Docker 中使用本機 dosgolem branch
`buck-rogers-cht-output-overlay`、HEAD
`0ce49482d3e47a30ebadd530c56c7a02303b10e7`、Go 1.26.7；
`cmd/buckrogers-text-receipt` runner SHA-256
`6039c6d97d57a6cc30efc1e03bee28b2e4a817e5bbae9d1dc2fd982149a35e66`。
原版、state、逐字事件、倚天字型與畫面均只在 ignored `workplace/`，不得
加入 Git／GitHub 或公開封包。

## 雙重原版收據

`workplace/page7-ready-atomic-core/entry-{a,b}.json` 逐 byte 相同，SHA-256
`988d1810c04c7834962def089d56b7444941f616c2efe2efd2fd7284ded85e8a`。
第七頁 row 17–22 共六行 190 glyph，長度為 `36/36/37/38/38/5`。
190/190 筆記錄 `0763:03D6`、RETF opcode `0xCA`、返回 `0763:04FF`、
同 SS、相對 SP `+0x12`、mode/repeat `1/1`、背景／前景 `0/10`；七個 ABI word
的 `high_word_mask` 均為 0。這些是原版逐字控制流證據，不是正式覆繪驗收。

`workplace/page7-ready-atomic-core/exit-{a,b}.json` 逐 byte 相同，SHA-256
`2c30f5dae5b499d29b871c39e7609a2a927d68da2cff20ef65d5d63cf6d16acc`。
六行候選矩形的最早相交原版 pre-write 位於 step `341018656`、
`0CF4:1B3A`、`ES:DI=A000:AA08`、`CX=304`。它是合法 Enter 離頁的
失效候選錨點；其他離頁與存讀檔生命週期仍未知。

## 可丟棄核心與字型

`typed-core-receipt.json` SHA-256
`2c6658f7ef5c35b78687e9ab3f36714999b0d5f0c60645ceaa391c796185016c`
記錄正式 `confirmed/DRAFT` catalog 被拒絕；只用暫存 READY fixture 驗證
六行原子提交、length／SHA、caller／guard／style／order、七個 ABI 高位、
RETF／stack／step、partial，以及未知／不相交／相交 pre-write。
當前本機倚天 GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`，
16×16、1024 glyph；第七頁 52 個不同字元均有字模。候選
`[8,320)×[136,184)` 在 2×有 3,149 個墨跡像素且零越界；
3×改用正式 `manualThreeXFont` 幾何：22×22 中文墨跡、offset 1、
24×24 output cell，共 5,981 墨跡像素且零越界；
`font-containment-receipt.json` SHA-256
`57f5a91f65a27d27e0309e429718a35037850165475074e97999bf486c6c5881`。
上述 JSON 均位於 ignored `workplace/page7-ready-atomic-core/`。

## 停止線

審查當時正式六筆 `text/story-page7-events.tsv` 仍為 DRAFT。須由獨立審查者核對
原版收據、候選矩形、離頁 pre-write、譯文與失敗即關閉邊界，才可考慮
限縮升 READY；其後還要 dosgolem 正式 runtime 的 control／2×／3×
同狀態 A/B、離頁無殘字與負例，才可聲稱已中文化或 CONFORMED。

首輪獨立審查已確認上述原版 identity 與離頁候選，但指出兩項缺口：
可丟棄核心未驗 ABI 低位 mapping／drift，3× 靜態 containment 未使用
正式 renderer 幾何。Terra 其後在 ignored 工具補上七個 ABI word
`mode, glyph, repeat, background, foreground, row, column` 的低位綁定與
逐欄 drift fail-closed 負例，並以正式 3× 字模幾何重算；上述新收據雜湊
對應修正後版本。**獨立複審尚未完成，catalog 仍為 DRAFT。**
舊[第一百二十九階段](phase-129-story-page7-enter-trace.md)
把 `331026808` 稱為首筆寫入也已追加勘誤；最新雙重收據的首筆是
`331026784`，不抹除當時紀錄。

第二次獨立複審證實前述 ABI 與 3× 幾何缺口已補，但找到一個新的
失敗即關閉反例：可丟棄 `Watcher.prewrite()` 把 row 137 左 margin
`DI=137*320, CX=8`（只含 x=0..7，不相交候選 x=8..319）誤判為
相交而清除作用中六行。須改成逐列半開區間相交判定並驗證跨列邊界，
才能限縮升 READY；目前仍不授權正式 runtime。

Terra 其後修正 ignored `page7_core.py` 為逐列半開區間判定，新增
row 137 左 margin、row 136 左邊界、row 184 之後及跨行相交等測試；
上述 `typed-core-receipt.json` 是修正後重生的收據。主代理回讀完整
SHA-256，正式獨立末次審查仍在進行；不把「原型測試通過」逕稱 READY。

## 2026-09-23 末次獨立審查與限縮 READY

獨立審查者回讀 `typed-core-receipt.json` 完整 SHA-256
`2c6658f7ef5c35b78687e9ab3f36714999b0d5f0c60645ceaa391c796185016c`
並在 Docker 重跑測試。row 137／136 的 x=0..7 不相交寫入不清 group；
跨行真正碰到安全矩形的寫入清 group；row 184 亦不清。
原版雙重 entry／exit、190 glyph 逐字 return／ABI、正式 catalog identity、
2×／3×字模 containment 和失敗即關閉反例均通過審查。

因此[規格 016](../spec/016-story-page7-overlay-ready.md)與六筆
`text/story-page7-events.tsv` **只在合法 page6 state→page7 六行及
page7→page8 Enter 離頁升 READY**。前述 DRAFT 與缺口紀錄保留作
審查形成史，不是現況宣告。正式 dosgolem watcher／presenter／CLI、
control／2×／3×同狀態 A/B、離頁同幀無殘字及雙倍率失敗矩陣仍未完成；
不得稱 CONFORMED 或第七頁已中文化。
