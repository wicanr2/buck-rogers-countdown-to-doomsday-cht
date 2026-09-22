# 第一百四十五階段：第五頁 READY 前最小證據

日期：2026-09-22
狀態：**DRAFT；第五頁五行的低階 return／ABI 與已量 Enter 離頁 pre-write 已補齊，仍待獨立 READY 審查，未接 production。**

## 範圍與散布邊界

本文件只處理第四頁合法終態 Enter 後的第五頁 row 17–21 五行固定敘事，以及從第五頁
合法終態 Enter 到第六頁時第五頁衍生層的最早失效候選。右側人物姓名、row 24 command/status、
其他離頁方式、watcher、renderer 與中文 A/B 均排除。

所有位址均為 dosgolem **實模式** `segment:offset`，不是 IDA 線性位址或檔案 offset。
原版 `GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
state、原版、完整 JSON receipt、字型與畫面均只留在 ignored `workplace/`；本文件不保存
原文 glyph bytes、原版像素或玩家輸入內容。

## 第五頁逐字 RETF／stack／ABI 收據

輸入為私有第四頁合法終態
`workplace/phase104-post-return-enter-4/control.state`（SHA-256
`48885cadf2bc51d6c44c09e2f220a3bb80bb23487506c0494eecd977613bf07a`）。在 step
`310000000` 排入既有的一筆正常 BIOS Enter，執行上限為 `320000000`。工具是本機
dosgolem branch `buck-rogers-cht-output-overlay` 的 commit
`9a9b769f355942ce9ff4c258f842e1f138938b3e`，以 Go 1.26.7、
`golang:1.26.7-bookworm` 的無網路 Docker 重播。

兩次 content-safe receipt 逐 byte 相同，SHA-256 均為
`9cd3204e9887eda457c4a1b2b2f8880a2a49a777d8fd839e1e79f5c1b8385d6c`，位於
`workplace/page5-ready-evidence/page5-entry-{a,b}.json`。

| 項目 | 分級 | 已確認結果 |
| --- | --- | --- |
| 五行 identity 與行長 | 已證實 | 168 glyph，rows 17–21 分別 `34/38/35/36/25`，逐項等於 `text/story-page5-events.tsv`。 |
| 真實 return control flow | 已證實 | 168/168 皆為 guarded `0763:026B` entry，緊前 `0763:03D6` opcode `0xCA`（`RETF imm16`），實際返回 caller `0763:04FF`。 |
| entry／return stack | 已證實 | 168/168 均有 `entry_ss == return_ss`、`(return_sp-entry_sp) mod 65536 = 0x12`，且 `entry < return < post-call`。絕對 SS/SP 只屬收據錨點，不得作 runtime identity。 |
| 顯示 ABI 與高位遮罩 | 已證實 | 168/168 的 mode/repeat 為 `1/1`、背景/前景為 `0/10`、七個 ABI word 的 `high_word_mask=0`；後續實作須在轉為 byte 前拒絕任何非零高位。 |

這是第五頁自身的逐字收據，沒有把第三、四頁的結論外推到第五頁。

## 第五頁→第六頁最早安全矩形 pre-write

輸入為私有第五頁合法終態
`workplace/phase123-story-page6-enter/page5.state`（SHA-256
`dcd08e37d9f394d47b1985b5891f0f3c70ba55d2c345bf9296867657f8ee65f6`）。在 step
`321000000` 排入既有正常 BIOS Enter，執行上限 `330000000`。兩次 content-safe receipt
逐 byte 相同，SHA-256 均為
`66928b27576ac4e7c2354adff44d3c25b01455053efd79aac297213034d75f6e`，位於
`workplace/page5-ready-evidence/page5-ready-{a,b}.json`。

第五頁擬定 logical safe rectangle 為 `[8,320)×[136,176)`：這是 rows 17–21、column 1
與每行最多 39 個原版 8-pixel cells 所導出的**強推論**，尚非正式 rectangle TSV 或
runtime 契約。在此 half-open rectangle 下，最早相交的原版 **pre-execution** Mode 13h
fill 是：

```text
step 321118382, 0CF4:1B3A, ES:DI=A000:AA08, CX=304
offset span [0xAA08,0xAB38)
```

它從 row 136、column 8 開始，故若未來規格升 READY，衍生層必須在此寫入**前**失效。
收據共保存 40 筆與 diagnostic story window 相交的 fill metadata，未達 64 筆上限。

這訂正並細化[第一百二十八階段](phase-128-story-page6-enter-trace.md)的敘述：該頁記錄的
step `321118406`／`A000:AB48` 是第一筆**可見** story-region pixel 差異，並不是最早的
安全矩形相交寫入；兩者相差 24 steps。此訂正保留舊收據與其觀測目的，不將可見差異誤稱
為 pre-write。

## TSV 幾何與字型核對

`tools/story_page5_catalog.py` 與其八個失敗即關閉測試通過；它鎖定五筆 DRAFT identity、
UTF-8/NFC、控制／格式字元、鍵值雙向覆蓋、39-cell 保守行寬，以及 hash、狀態與 key
漂移拒絕。此驗證器證明的是資料層幾何上界，**不**把上述 strong-inference rectangle
升格為正式資料。

私有 `workplace/phase128-font/buckrogers-eten-top-pad.golemfnt`（SHA-256
`16e0e8cd687bbcd0f12b8330a47a7eed9519dd861063c41c01388f9ffc41d024`）由 dosgolem
正式 loader 回讀為 `GOLEMFNT 16x16 glyphs=1014 coverage=51`，第五頁現行 51 個譯文字元
零缺字。字型來源及產物不可散布；coverage 不構成 runtime 繪製、containment 或 A/B。

## READY 前停止線

本階段只補原版低階證據與資料核對，不能把 `text/story-page5-events.tsv` 的 `DRAFT` 升為
`READY`。獨立審查仍必須：

1. 將五行原子提交、完整 identity、RETF／stack／high-word、擬定 rectangle 與 pre-write
   失效規則寫成可丟棄 typed-core，並覆蓋 partial、duplicate、錯序、style、return edge、
   stack、non-zero high word、未知 write、non-READY catalog、restore/discontinuity 的失敗案例。
2. 審查正式 rectangle TSV、2×／3×字型 ink containment、原子清除與同狀態 control A/B
   驗收設計；不可用本輪字型 coverage 代替。
3. 由未參與收據生成者覆核 TSV、168 筆 return edge、half-open span 計算、舊可見差異訂正
   與本機／不可散布邊界。

完成前不得建立第五頁 watcher、presenter、正式安全矩形資料或任何 production path。
