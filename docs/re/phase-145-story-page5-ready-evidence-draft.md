# 第一百四十五階段：第五頁 READY 前最小證據

日期：2026-09-22
狀態：**READY；僅第五頁五行 typed adapter contract 與已量 Enter 離頁，未接 production、不是 CONFORMED。**

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

`tools/story_page5_catalog.py` 與其八個失敗即關閉測試在隔離的
`python:3.13-bookworm` Docker 容器重跑通過；它鎖定五筆 DRAFT 身分、UTF-8/NFC、
控制／格式字元、鍵值雙向覆蓋、39-cell 保守行寬，以及雜湊、狀態與 key 漂移拒絕。
現行五筆譯文的保守寬度依序是 `22/30/24/16/10` 格，均低於 39。此驗證器證明的
只是資料層幾何上界，**不**把上述強推論 rectangle 升格為正式資料。

本階段起草時所引 `workplace/phase128-font/` 的 page5 catalog SHA-256 是
`4b3dc682d78bc67634241b72fa25a5cec2bd2acd32c986d6a59f1391a5facb51`，已不等於現行
`text/story-page5.zh-TW.tsv` SHA-256
`cb640abad6d04c5db8e6f4662c799a90120ae11d21ee80cf646933252d06b728`；故其 1014-glyph
loader 收據不得再當作**現行**第五頁的涵蓋證據。已找到對應現行 SHA 的本機產物
`workplace/phase138-font/eten-subset.golemfont` 與 `manifest.json`：格式為
`GOLEMFNT 16x16 glyphs=1024`，產物 SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`，且 manifest 明列本
TSV 的現行雜湊。這只證明可追溯的本機建置輸入／輸出相符；本輪未以正式 loader 回讀該
1024-glyph 產物，亦未證明 2×／3×墨跡包含、執行期繪製或 A/B，因此不能以 manifest
取代那些收據。字型來源、產物及 manifest 均不可散布。

## 原 DRAFT 停止線（已由後續審查解除）

本階段起草時只補原版低階證據與資料核對，原先不能把 `text/story-page5-events.tsv` 的
`DRAFT` 升為 `READY`。當時要求的項目如下；其後續完成結果見下一節。

1. 將五行原子提交、完整 identity、RETF／stack／high-word、擬定 rectangle 與 pre-write
   失效規則寫成可丟棄 typed-core，並覆蓋 partial、duplicate、錯序、style、return edge、
   stack、non-zero high word、未知 write、non-READY catalog、restore/discontinuity 的失敗案例。
2. 審查正式 rectangle TSV、2×／3×字型 ink containment、原子清除與同狀態 control A/B
   驗收設計；不可用本輪字型 coverage 代替。
3. 由未參與收據生成者覆核 TSV、168 筆 return edge、half-open span 計算、舊可見差異訂正
   與本機／不可散布邊界。

完成前不得建立第五頁 watcher、presenter、正式安全矩形資料或任何 production path；此停止線
在下列可丟棄審查完成前有效。

## 獨立 READY 審查補證與結論（限縮）

**結論：第五頁五筆 catalog 已升為 `proven/READY`，只授權未來 typed adapter 實作；未改
dosgolem production watcher／renderer，亦不是 CONFORMED。**

以未參與 receipt 生成的審查角度，重核 168 筆 guarded return、half-open pre-write span、
現行 TSV 與字型。新增的 ignored `workplace/page5-ready-atomic-core/` 只讀五筆 TSV，三項
測試通過：完整五行才原子提交；DRAFT、partial、duplicate、錯序、identity、ABI、return、
relative stack、step、font miss、unknown／非相交／已量 write 與 discontinuity 皆失敗即關閉。
它的 pre-write 僅接受 `0CF4:1B3A`／`ES=A000` 且按實際 `DI/CX` 與
`[8,320)×[136,176)` 做 half-open 相交；不以固定 step、DI 或絕對 SS/SP 作 runtime identity。

現行 51 個譯文字元以既有 dosgolem `fontcheck` 對
`workplace/phase138-font/eten-subset.golemfont` 回讀為
`GOLEMFNT 16x16 glyphs=1024 coverage=51`、零缺字。直接解碼該字型的 static bitmap 收據
在 2×／3×各得 3255 ink pixels、safe rectangle 外零墨跡；收據只在 ignored `workplace/`，
不含原版素材，也不是 runtime A/B。

尚缺同 state control／2×／3× A/B、Enter 離頁同幀清除及無殘字、正常開機玩家路徑與遊戲內
存讀檔。它們是後續 CONFORMED 閘門，不得提前宣稱已中文化。正式契約見
[spec 014](../spec/014-story-page5-overlay-ready.md)。
