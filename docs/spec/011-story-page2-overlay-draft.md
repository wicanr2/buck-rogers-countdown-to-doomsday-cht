# 011 — 第二頁劇情文字輸出端覆繪

狀態：**READY（僅第二頁四行 typed adapter contract；尚未接 production，亦非 CONFORMED）**
日期：2026-09-22
前置：[第一百零七階段第二頁 DRAFT catalog](../re/phase-107-story-page2-draft.md)、
[第一百三十二階段 READY 審查](../re/phase-132-story-page2-ready-review.md)、
`text/story-page2-events.tsv`、`text/story-page2.zh-TW.tsv`。

## 目的、範圍與停止線

本規格只處理首屏正常 Enter 後的第二頁四行固定敘事。原版必須先畫英文；繁中只可在
dosgolem RGBA output layer 顯示，不得寫 DOS VRAM、CPU／DOS state、BIOS key queue、原版條件比較、
檔案或存檔。

本規格不涵蓋首屏、第三頁及其後、right-side 人物姓名／數值、row 24 status、手冊答案、任何
玩家輸入或原版全文。所有位址均是 dosgolem 實模式 `segment:offset`。它授權實作**第二頁
typed adapter**，但不授權把未審查頁面、未知離頁路徑、restore 語意或 host frontend 一併接入。

## READY 審查結果：通過

原版側的四行 identity、真實 far-return、相對 SS/SP shape，以及 page2→page3 pre-write exit
均已確認；它們足以收斂下列 typed contract。早先 DRAFT core 的「wrong order」測試曾錯把
第 1、2、3、4 行的合法完整 sequence 當作錯序，故審查曾撤回其過早的綠燈聲明。該可丟棄測試現已
訂正為 partial 後 row drift、從第 2 行開始的真正 order inversion、以及 far-return 的
previous address、`RETF` opcode、return caller、relative SS、relative SP 各自不符；同時保留 hash、
相對 step 倒退、restore、未知 video write、duplicate 與 page3 non-revival。

獨立審查於無網路、`--rm`、UID/GID `1000:1000` Docker，以版控
`text/story-page2-events.tsv` 執行 `go vet ./...` 與未快取 `go test ./... -count=1 -v`，均 exit 0。
這重新建立 pure-core synthetic failure coverage，連同原版 receipt 的 identity／far-return／pre-write
證據，已足以升 READY typed adapter contract。不得為了通過測試把固定 receipt step 或
`SS=1841h/SP=3D66h` 寫成 runtime identity；production 與 A/B 仍是下一閘門。

## 輸入資料與已確認原版證據

四筆 event 必須 exact-match `story.page2.line.001` 至 `.004`，順序為 1..4，均為
`0763:04FF` caller／`0763:026B` guarded glyph primitive、mode/repeat `1/1`、背景／前景 `0/10`、
column 1、rows 17..20。四行 glyph count 為 37／31／38／37。identity 的原文只在 watcher
內暫存到完成 SHA-256 驗證，絕不進 exported event、receipt、presenter 或譯文資料。

固定原版 receipt 的 original length、SHA-256、entry/post step、caller、guard、色彩及 row／column
都是可回查證據錨點。**絕對 entry/post instruction step 不是 runtime identity。** runtime 只能比較
length／SHA-256、caller／guard、mode／repeat、style、row／column、四行 order，以及完成 return 的相對
順序 `entry < post < next entry`；不得用 `281…`／`287…` 等固定步數錯拒正常玩家路徑。

每個 glyph completion 的已確認 control-flow shape 是：pending `0763:026B` entry 後，緊前指令必為
`0763:03D6`／opcode `0xCA`（`RETF imm16`），且當前 `CS:IP` 實際回到 pending caller，`SS` 與 entry
時相同、`SP = entry SP + 0x12`，才是 verified far-return。receipt 中 `SS=1841h`、entry
`SP=3D66h`、return `SP=3D78h` 僅證明這一次合法重播的 shape；**它們不是 runtime 常數或身份鍵。**
不得以「稍後碰到 `0763:04FF`」或只憑 SS/SP 當作 return。

logical text-safe rectangle 固定為 `[8,320)×[136,168)`；每列 39 cells、8×8 logical pixels，overflow
為 `single-line-reject`。right-side 動態欄位及 row 24 與此 y range 不相交，且不在 catalog。譯文必經
UTF-8 TSV schema／NFC／控制字元／唯一 key／雙向 coverage 驗證及本機字型完整覆蓋。

`text/story-page2-events.tsv` 的四筆 identity 已在相同欄位、順序、雜湊與譯文 coverage 下審核為
`confirmed/READY`；production loader 只能接受此狀態，其他狀態失敗即關閉。這個資料準入不把
fixed receipt steps 變成 runtime identity，也不代表第二頁覆繪已通過同狀態驗收。

## typed adapter contract

### 輸入與狀態

adapter 的最小輸入等價於：

```text
GlyphEntry { guard, caller, ss, sp, abiWords[7], entryStep }
VerifiedFarReturn { previousAddress, previousOpcode, at, ss, sp, postCallStep }
PreExecutionVideoWrite { at, es, di, cx, step }
ExecutionDiscontinuity { restore | stop | unobserved-control-handoff }
```

`GlyphEntry` 只在目前 `CS:IP=0763:026B` 時取得；其 `caller` 和七個 ABI word 由 pending entry 的
真實 stack 讀取。顯示 identity 只取 ABI word 的已證實 low byte：mode、glyph、repeat、background、
foreground、row、column；高位不得進 hash 或匹配。 `entryStep`／`postCallStep` 是 `uint64` 的順序資料，
不是固定數值 gate。

watcher 狀態只能是：空閒、帶有 entry-time `SS/SP` 的 pending glyph、正在收集的一行 bytes、已完成的
0–3 行候選，或一個不可變的四行 active generation。每次新 glyph entry 在仍有 pending 時，或任一
可驗證中斷，都必須丟棄 pending／候選；active generation 不會被重複 glyph 建立第二次。只有再次從
第一行完整 exact-hit，才可能建立新的 group。

### 轉移與失敗即關閉規則

1. adapter 只在 `previousAddress=0763:03D6`、`previousOpcode=0xCA`、`at=pending.caller`、
   `SS=pending.SS`、`SP=pending.SP+0x12` 且 `postCallStep>entryStep` 時提交一個 glyph。任何一項不符、
   未驗證 return、caller/guard/style/column drift、hash miss、partial line、錯行或相對步序倒退都丟棄
   整個候選，零 partial event、零 partial draw。
2. 每行只在 length 完全相等後計算 SHA-256；四行 identity 必須依 TSV sequence 1..4，且下一行
   `entryStep > 前一行 postCallStep`。四行都 exact-hit 才原子發出一個 group；相近 hash、座標、色彩或
   單獨一行均不足以發出 request。
3. exported `StoryPage2Event` 只能含 generation、event/translation key、已核對 length/SHA、palette
   indices、row、column、entry/post 的 runtime ordering metadata。它不得含英文 bytes、ABI word、高位、
   machine pointer、手冊答案、輸入或存檔資料。presenter 只接受完整四 event 的同一 generation，且只用
   translation key 查 UTF-8 catalog。
4. catalog／translation／font 缺失、非 READY data status、非法倍率、重複 key、非 NFC、控制字元、39-cell
   overflow、缺字或 presenter 收到非完整 generation 時，必須拒絕建立或繪製。不得 fallback 英文、猜譯文、
   截斷、換行或保留舊 RGBA。

## lifecycle、退出與 restore

已量到的 page2→page3 exit 只是一條原版合法 Enter 路徑：pre-execution `0CF4:1B3A` 的
`ES:DI=A000:AA08`／`CX=304` span 在 step `291020464` 與 `[8,320)×[136,168)` 相交，早於 page3
first glyph entry `291022040`。固定 step、DI、CX 是 receipt anchor；runtime gate 是 **同一**
`0CF4:1B3A`、`ES=A000`，且以實際 `DI/CX` 作 Mode 13h row-aware half-open span intersection。命中時
必須在原版 write 前移除整個 active page2 group，清空 pending/candidate，並使同 frame output RGBA 回到
baseline；不得寫 VRAM 或以「下一筆文字」、row 24、像素差異或 fixed step 當 proxy。

未知 video write 沒有 lifecycle authority：不可憑任意 write 清除、重建或猜測 page transition。未量到的
合法離頁路徑也不能靠本規格外推。state restore、machine stop、未觀測到的 control-flow handoff，或任何
無法證明 pending frame 仍連續執行的事件，必須建立新的空 watcher／presenter generation（active、pending、
candidate 與 RGBA layer 全部清除）；只有四行再次完整 exact-hit 才可重畫。這是 fail-closed boundary，
不是對原版 restore／未知離頁語意的宣稱。

## 輸出與 presenter

未來 adapter 位於 `workplace/dosgolem/apps/buckrogers/`；遊戲位址不得放入 `xlate` 或 host。其最小 API
可採等價語意：

```text
LoadStoryPage2Catalog(eventsTSV, translationsTSV) -> StoryPage2Catalog
NewStoryPage2Watcher(catalog) -> watcher
watcher.ObserveGlyphEntry(...)
watcher.ObserveVerifiedFarReturn(...) -> []StoryPage2Event
watcher.ObservePreExecutionVideoWrite(...) -> invalidated
watcher.ObserveExecutionDiscontinuity(...)
NewRuntimeStoryPage2Overlay(catalog, font, scale) -> presenter
presenter.Apply(completeGeneration); presenter.Frame(indexed, palette); presenter.Draw(indexed, palette)
```

2× 使用既有 16×16 top-pad 字模；3× 依既有規則將 CJK ink 放大至 22×22、置於 24×24 output cell，
ASCII 維持既有樣式。兩倍率都不得改 320×200 indexed framebuffer；RGBA 差異只能出現在放大後 safe
rectangle。

## CONFORMED 驗收（實作後）

本 READY 規格不是中文化完成聲明。實作後必須以相同私有合法 state、完整 BIOS 排程和停止點，
做 control、2×、3×的 dosgolem A/B：

1. 在 page2 四行完成的 stable frame，原始 machine memory、indexed framebuffer、palette、CPU/DOS state、
   BIOS input、file operations、writes 與未實作服務 digest 都必須相同；RGBA 僅在 `[8,320)×[136,168)`
   的放大範圍不同，且四行繁中可讀、零缺字、零右側／row24 差異。
2. page2→page3 的已量 Enter 路徑中，命中 pre-write span 的同一 output frame 必須清除四行 group；後續
   RGBA 與 baseline 逐 byte 相同，沒有 page2 殘字，也不得顯示 page3 或未列 catalog 的中文。
3. 2×與3×分別驗 catalog/hash/caller/guard/mode/repeat/style/order/return failure、partial、duplicate、
   非 READY TSV、font miss、未知 video write、restore 與 execution discontinuity；它們都必須零繪製或
   清空而不復活舊 group，且不改原版 state。

只有這些同狀態收據由 dosgolem 重生，才能將本規格標為 CONFORMED；結論仍只限第二頁四行與已量到的
page2→page3 Enter exit。

## 權利與散布邊界

本規格、event key、hash、座標、繁中譯文與驗證器可版控；原版遊戲、掃描手冊、英文原文、合法答案、
state、畫面、ETen 原始字型與衍生 GOLEMFNT 一律不進 Git、GitHub 或公開封包。原版缺席時公開程式必須
跳過原版驗證，不能宣稱已對拍。
