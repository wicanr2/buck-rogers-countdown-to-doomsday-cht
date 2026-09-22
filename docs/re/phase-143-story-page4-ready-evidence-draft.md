# 第一百四十三階段：第四頁 READY 前最小證據

日期：2026-09-22
狀態：**原始 DRAFT；192 筆逐字返回與六行完整矩形的最早 pre-write 已證實。2026-09-22 獨立審查已據此限縮升為規格 013 的 READY；尚未接 runtime。**

> **勘誤（2026-09-22）**：本文件起草時把 `-story-fill-trace` 記下的第一筆
> step `310023777` 稱為六行 `[8,320)×[136,184)` 的「最早相交」。獨立審查
> 原始碼發現診斷函式 `storyFillIntersects` 的 bottom 固定為 `176`，只監測 rows
> 17–21；它可能漏掉 row 22-only 更早的寫入。因此該筆只證明前五行子矩形的
> 最早已記錄寫入，**不能**作為第四頁六行 overlay 的 READY 清除 gate。

## 問題與範圍

本文件只整理第四頁 row 17–22 六行固定劇情，要升為 typed adapter
`READY` 前所需的兩種低階證據：逐字真正 far-return，以及第四頁離頁到第五頁
時最早與文字安全矩形相交的原版 pre-execution 視訊寫入。右側姓名、row 24
與其他離頁方式都不在範圍內。

所有位址均為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址或檔案 offset。
原版 `GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
原版、state、畫面與完整 receipt 都只留在 ignored `workplace/`，本文不含原文
glyph bytes、畫面像素或玩家輸入內容。

## 可重播的已證實資料

從私有第三頁合法終態
`workplace/phase104-post-return-enter-3/control.state`（SHA-256
`49d4bb0681269fca1954f3e02cb2cffe93bac48086d607dcfa5d975174750cc0`）開始，
在 step `301000000` 送入既有的一筆正常 BIOS Enter，執行至 `310000000`。

以本機 dosgolem source revision `2f8c807fce5da477d5f228e4b571fa2fcf845d20`（Go
`1.26.5`、`golang:bookworm` Docker image）重建 content-safe runner；兩次收據逐 byte
相同，SHA-256 為
`66902bb00d7aa0dee648082ed88dea5331a85d87d4fbedcb3ccd38940a089342`。
私有檔案位於
`workplace/page4-ready-evidence/page4-full-return-current-{a,b}.json`。當次 source
工作樹狀態另保存於同一 ignored 目錄，僅用於重現，不視為 production commit。

| 項目 | 分級 | 證據 |
| --- | --- | --- |
| 六行 identity、順序、row、length、SHA-256、style、entry/post step | 已證實 | 192 glyph 聚合為六筆，逐欄等於 `text/story-page4-events.tsv`；詳細 identity 見[第一百二十四階段](phase-124-story-page4-first-glyph-trace.md)。 |
| 每個 glyph 的 `0763:03D6` opcode `0xCA` → `0763:04FF` 真實控制流 | 已證實 | 192/192 筆 `glyph_return_edges` 均有 `return_instruction=0763:03D6`、`return_opcode=0xCA`、`post_address=0763:04FF`；rows 17–22 計數依序為 `34/37/33/31/33/24`，反例零。 |
| ABI 低位與高位遮罩 | 已證實 | 192/192 為 mode/repeat `1/1`、背景/前景 `0/10`、`high_word_mask=0`；column 自 1 連續遞增。 |
| 每個 glyph entry SS 與 return SS 相同、return SP 相對 entry SP 增 `0x12` | 已證實 | 192/192 筆均有 `entry_ss=ss=1841h`、`entry_sp=3D66h`、`sp=3D78h`；逐筆驗算 `(sp-entry_sp) mod 65536 = 0x12`，並有 `entry < return < post-call`。絕對 SS/SP 只屬本次收據錨點，runtime 不得以它們作 identity。 |

這是第四頁自身的逐字 stack 收據，不以第三頁結論外推。

## 第四頁→第五頁的前五行診斷 pre-write 與可見差異

從私有第四頁合法終態
`workplace/phase104-post-return-enter-4/control.state`（SHA-256
`48885cadf2bc51d6c44c09e2f220a3bb80bb23487506c0494eecd977613bf07a`）開始，
在 step `310000000` 送入同一類正常 BIOS Enter，執行至 `320000000`。以相同 source
雙重重播，content-safe receipt 逐 byte 相同，SHA-256 為
`9cd3204e9887eda457c4a1b2b2f8880a2a49a777d8fd839e1e79f5c1b8385d6c`，位於
`workplace/page4-ready-evidence/page4-ready-current-{a,b}.json`。

此診斷在前五行子矩形 `[8,320)×[136,176)` 中記下的第一筆
**pre-execution** write 是 step `310023777` 的
`0CF4:1B3A`，`ES:DI=A000:AA08`、`CX=304`。其 Mode 13h half-open offset span
`[0xAA08,0xAB38)` 與前五行子矩形相交（起點正是 row 136、column 8）。
它是第四頁衍生層的**候選**失效點；現有收據不能排除 row 22-only 的更早寫入，
不得據此正式接線。收據共記錄 40 筆五行子矩形相交 span，未達 64 筆上限。

第一筆**可見** story-region pixel 差異較晚，為 step `310023801` 的同一指令、
`ES:DI=A000:AB48`、`CX=304`，bbox `x=10..270, y=137`；相差 24 steps，並早於
第五頁第一個 glyph entry `310025410`。因此不得將像素差異誤作最早寫入。

第四頁預定的六行 logical text-safe rectangle 應為
`[8,320)×[136,184)`（row 17–22，每行 8 logical pixels）；這是以已證實的 row/column
與各行最多 39 個原版 8px cells 推導的 **強推論**，尚未成為正式 rect catalog 或 runtime
契約。上列可見差異落在其中，但不授權清除 active overlay。

## 目錄／版面核對與審查停止線

現行 `tools/story_page4_catalog.py` 對六筆 DRAFT identity 與繁中 TSV 通過；其六個
負例測試也通過（hash／post step／key／evidence level／容量漂移均拒絕）。每行譯文的
保守 CJK cell 寬度不超過 39。上列 rectangle 是六個 39×8 logical cell 的最小包絡，
尚未建立正式 rect TSV；這不阻礙原版低階證據審查，但 adapter 實作前必須把它納入
READY contract 並檢查本機字型覆蓋。

起草時誤以為兩個低階缺口都補齊；獨立審查後，以下是原先規劃的 READY 項目，
其完成與訂正見下節：

1. 將 rectangle、原子六行提交、已量 pre-write 清除與 restore／discontinuity 失敗即關閉
   轉為可丟棄 typed-core 測試，包含 partial、duplicate、錯序、identity／style、return edge、
   entry stack、未知 write 與 non-READY catalog 的負例。
2. 以正式字型產物回讀第四頁譯文的 coverage，並在 READY 規格明示 2×／3× containment
   與同狀態 A/B 驗收；這些不是本次原版診斷自動證明的結論。
3. 由未參與本次收據產生的審查者覆核 TSV、192 筆 return edge、pre-write span 計算與
   散布邊界。完成前 catalog status 不能升級。

在此之前，`text/story-page4-events.tsv` 與譯文仍維持 `DRAFT`，不建立 watcher、renderer、
安全矩形正式資料或任何 production path。

## 獨立審查勘誤與剩餘唯一缺口

審查者以已提交的本機 dosgolem `564d53f`、Go 1.26.7／
`golang:1.26.7-bookworm` Docker 重建 content-safe runner，重新雙重驗證上述
192 筆 return 與五行診斷寫入，兩組既有 receipt SHA 均未變。原先關於 Go image
缺少編譯器的回報是工具調用錯誤，已訂正；不是本任務 blocker。

ignored `workplace/page4-ready-atomic-core/` 的可丟棄 typed-core 三項測試涵蓋六行
原子提交、DRAFT 拒絕、partial／duplicate、identity／style／return／stack／step、
缺字、未知或非相交寫入、已量寫入與 discontinuity；正式 GOLEMFNT loader 對第四頁
57 個譯文字元回讀零缺字，私有 coverage 收據留在同一工作區。這些只證明候選
契約可行，沒有接 production。

此處記錄的是當時停止線；後續六行補證見下節。

## 六行補證與目前閘門

本機 dosgolem 提交 `ac1f7fb4f52680f3a96c42c475667ec7a9dd6b2d`
加入受限的 `-story-fill-rows 6` 診斷。spec 229 僅授權此 content-safe
收據，不授權第四頁覆繪。測試確認 row 22-only 寫入會命中、row 23-only 不會，
非法列數拒絕，五行舊行為保持。從上述合法第四頁 state 與相同 Enter，
以固定程式重建後雙重重播；私有收據
`workplace/page4-ready-evidence/page4-six-row-ac1f7fb-{a,b}.json`
逐 byte 相同，SHA-256 均為
`4f1bd9940877601138f77e16dfa290d1243566506670db52344f707a94f20f3d`。
兩份均明記 `story_fill_rows=6`，48 筆 bounded span 全部與
`[8,320)×[136,184)` 相交，最早者仍為 pre-execution step `310023777`、
`0CF4:1B3A`、`A000:AA08`、`CX=304`；第一可見 pixel 差異為
`310023801`，第五頁首 glyph 為 `310025410`。因此前述五行診斷的
幾何缺口已補齊；原勘誤保留為發現過程，不撤銷。

第四頁正式資料目前仍為 DRAFT。接下來須獨立審查六筆繁中候選及 typed
原子提交契約，將矩形、失效、字型與 A/B 驗收寫入限縮 READY 規格；
在此之前不得接 watcher、catalog 或 renderer 的 production path。

## 獨立 READY 審查結果（2026-09-22）

未參與上述收據產生的審查，重算 `text/story-page4-events.tsv` 的六筆 identity、192 筆
return-edge 契約、rows=6 的矩形／pre-write 邊界，並重跑 catalog 與可丟棄 typed-core 的
失敗即關閉測試。結果通過：六行的 `catalog_status` 已改為 `READY`，但這不是 runtime 接線。

字型收據的兩個數字使用不同計數單位：phase 143 的 catalog 為 57 個譯文字元；phase 118 的
正式 loader 報告 page4 58 個 Unicode 檢查項。兩者均為缺字 0，且本次對現行 TSV 重算為 57 個
文字字元、53 個唯一 Unicode code point；因此不把計數差異誤寫成 coverage failure。限縮的
typed contract、字型／矩形、已量 Enter 清除與 CONFORMED 驗收已固定於
[規格 013](../spec/013-story-page4-overlay-draft.md)。其他離頁、完整開機與存讀檔仍為未知。
