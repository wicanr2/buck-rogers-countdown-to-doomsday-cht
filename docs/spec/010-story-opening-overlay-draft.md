# 010 — 首屏劇情文字輸出端覆繪

狀態：**READY（僅首屏五行；不得擴張至第二、三頁）**
日期：2026-09-22
前置：[第一百零五階段首屏劇情追蹤](../re/phase-105-first-story-screen-trace.md)、
[第一百一十四階段返回邊收據](../re/phase-114-story-return-edge-ready.md)、
[功能選單輸出端覆繪原則](001-menu-text-output-overdraw-draft.md)、
`text/story-opening-events.tsv` 與 `text/story-opening.zh-TW.tsv`。

## 目的、範圍與停止線

本規格只處理「手冊查閱題答對後」出現的**第一個**固定五行故事敘述。原版必須先完整畫出
英文；繁中只存在於 dosgolem 輸出端的 RGBA layer，絕不寫入 DOS VRAM、CPU／DOS 記憶體、
BIOS 鍵盤佇列、原版答案比對、檔案或存檔。

本規格排除：

- 第二頁及其後的劇情、右側角色姓名／數值、底部狀態列、肖像與所有動態欄位；第二頁追蹤
  只作為首屏 stamp 的轉場失效證據，不能把其原文或未建立 catalog 的字串納入譯表。
- 手冊題答案、作答按鍵、玩家輸入排程與任何原版全文。這些只保留於被 Git 忽略的
  `workplace/`。
- 改變原版敘事翻頁、Enter 消費、條件分支、亂數、存檔結構或文字來源。

所有位址均為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址。

## 已確認的原版身分與幾何

從本機 `phase12-before-question.state` 的合法手冊成功返回，首屏五行均由低階
`0763:026B` glyph primitive 畫出；每 glyph 的 guarded return 回到 `0763:04FF`，其實際 return edge
為 `0763:03D6` 的 `RETF imm16`（opcode `0xCA`）。七個 ABI word 僅以已證實的低位 byte 參與
顯示 identity；高位以 content-safe mask 診斷、絕不進 hash 或文字判定。兩次 content-safe
追蹤逐 byte 相同，沒有保存原文 bytes。正式候選必須同時命中全部欄位，不能只用 row、色彩或
hash 近似比對。

| event key | 原文長度／SHA-256 | caller／guard | bg/fg | logical origin |
| --- | --- | --- | --- | --- |
| `story.opening.line.001` | 37 / `a989ceac7d0b25ad1a02fca8d158c5c47ab25aa28faa329f99016bcbd22d89d2` | `0763:04FF`／`0763:026B` | 0/10 | col 1, row 17 |
| `story.opening.line.002` | 38 / `177bcfea0dd3bdba2390155791c7c48097736031d03e90eff9c1e594e7d24dc5` | `0763:04FF`／`0763:026B` | 0/10 | col 1, row 18 |
| `story.opening.line.003` | 33 / `c6a67dbd38752114fcf6761f59a57ed0970d0c75ac63696466c8f99d658a963b` | `0763:04FF`／`0763:026B` | 0/10 | col 1, row 19 |
| `story.opening.line.004` | 29 / `a0cb29721abfb85c6062169ef8d5c8a0d4e794570a007b472fc3f2c655dcd182` | `0763:04FF`／`0763:026B` | 0/10 | col 1, row 20 |
| `story.opening.line.005` | 23 / `f686b3355b648d95981ec5c128fc4e07f0950c983e9543c49a258fbcd1ea5d74` | `0763:04FF`／`0763:026B` | 0/10 | col 1, row 21 |

已確認的 clear／text-safe rectangle 為 logical
`[8,320)×[136,176)`，即 column `1..39`、row `17..21` 的半開聯集。每列的 text cell 是
8×8 logical pixels，寬度上限 39 cells、單列 `single-line-reject`；譯文不可換行、截斷、
縮寫或溢出到這個矩形以外。最長原文為 38 cells；最後一 cell 是畫布右緣前的候選餘裕，
實際 ETen 2×／3× containment prototype 已通過；Unicode 寬度近似僅作 catalog lint，不取代幾何收據。

右側動態資訊目前只在 row 2 與 row 4–9；底部狀態列是 row 24。因此其 y 區間分別不與
`136..176` 相交，這五行 stamp 不得涵蓋任何右側動態欄或 row 24。這是幾何排除，而非
「目前畫面看起來沒蓋到」的推論。

## 轉場與失效契約候選

首屏終態 state 在絕對 step `280000000`。正常 BIOS Enter 排於 `281000000` 後，第一個會改寫
story region 的原版指令是 `0CF4:1B3A`，step `281020572`，修改 bounding box
`[10,295)×[137,138)`。這是第二頁重繪第一條掃描線；二次重播一致。

因此候選 adapter 必須在下列順序運作：

1. 只在五行完整 guarded glyph run 均 exact-hit 後，原子建立一個首屏 stamp group；任一
   run miss、hash／長度／row／column／色號／caller／return guard 不符都必須失敗即關閉，
   不可顯示局部中文或 fallback。
2. 不得為此在每道 machine instruction 後掃描整個 story region。只在已確認的
   `0CF4:1B3A` 寫入指令 entry 讀取 `ES:DI` 與 `CX`，並以 row-aware 的 Mode 13h video-span
   intersection 判斷它是否實際碰到 `[8,320)×[136,176)`；命中時立即移除整組 stamp。偵測只讀
   registers／原版畫面，不能反寫 VRAM。已重播的首個實例是 `ES:DI=A000:AB48`、`CX=304`，
   即 row 137 的 x=`8..311`；它在 step `281020572` 寫入並與候選 story rectangle 相交。
   `0CF4:1B3A` 是通用 fill primitive，故 segment、destination 與 count 均為 fail-closed
   gate，不得只憑 code address 對所有呼叫一律失效。
3. 清除後不得因第二頁 glyph 或任何其他文字自動重建首屏 group。只有再次完整命中這五個
   exact identities 才可建立。

`026F:029C` 在此 Enter 路徑只清 row 24、欄 33..39，與 story region 無交集；它**不得**作為
劇情失效 hook。以「下一筆文字已輸出」判定舊劇情失效也同樣禁止。

## 擬定 typed runtime 介面

正式實作應置於 `workplace/dosgolem/apps/buckrogers/`，不把遊戲位址放進 `xlate` 或 host。
最小 API 必須有等價下列語意（確切 Go 名稱可在 READY 審查調整）：

```text
LoadStoryOpeningCatalog(eventsTSV, translationsTSV) -> StoryOpeningCatalog
NewStoryOpeningWatcher(catalog) -> watcher
watcher.ObserveGlyphEntry(caller, ss, sp, ABI args, step)
watcher.ObserveVerifiedGlyphReturn(entryStep, returnEdge, ss, sp, step) -> []StoryOpeningEvent
watcher.ObserveVideoWrite(at, es, di, cx, step) -> invalidated bool
NewRuntimeStoryOpeningOverlay(catalog, font, scale) -> presenter
presenter.Apply(event); presenter.Frame(indexed, palette); presenter.Draw(indexed, palette)
```

`StoryOpeningEvent` 必須只攜帶 event key、translation key、rune count、已證實的 palette
indices、generation／group identity；不可含英文 bytes、作答內容或 machine 指標。catalog lookup
只依 exact original identity 產生顯示 request；譯文絕不進入任何原版比較或存檔路徑。

2× 必須使用既有 16×16 top-pad 字模；3× 依已選定的產品規則把 CJK ink 放大至 22×22、置於
24×24 output cell，ASCII 維持既有樣式。兩倍率均不得改 320×200 indexed framebuffer。所有
正式譯文 glyph 必須先由本機 GOLEMFNT 完整覆蓋，缺一個即拒絕建立 presenter。

## READY 前置審查

READY 審查結果：

- [x] 五個首屏 glyph-run 的 exact identity、正常玩家起點、顏色、位置與雙重可重播收據。
- [x] 以實際第二頁重繪反證 row-24 clear，並確認 first story-region indexed write 的可觀測邊界。
- [x] 五行矩形與右側／狀態列的 y 軸不重疊分析。
- [x] `text/story-opening-events.tsv`、`story-opening.zh-TW.tsv` 經資料審查成為正式 catalog：嚴格
  TSV schema、唯一鍵、UTF-8／NFC、控制碼、逐列 39-cell 上限、來源分級及無孤兒 key 均要驗證。
  最長原文只有 38 cells；第 39 cell 餘裕已由實際 ETen containment 核可，不能僅由 Unicode
  寬度估算取代此結論。
- [x] 正式 990 glyph 的本機 top-pad union font 已重建，並以 production `xlate.LoadFont`
  回讀覆蓋五行譯文；字型 bytes／倚天來源仍只能留在 `workplace/`。
- [x] `StoryOpeningWatcher` 的 ABI entry／guarded post-call、連續 run、錯序、partial run、miss、
  stack guard、row-aware video-span intersection 與第二頁非重建的 synthetic tests；不能複用
  ActionBarWatcher 的 game-specific identity 或把 diagnostics 當 runtime。
- [x] 首屏→第二頁的正常 Enter 轉場已量到首筆 region write；其餘離開、存讀檔與 restore 不作
  首屏建立依據。READY 契約是任何 restore／未知 lifecycle 一律建立無 active stamp 的 watcher，
  只有五行重新完整 exact-hit 才可顯示；實際存讀檔玩家路徑保留在 CONFORMED 驗收。

已具備實作前所需契約，授權首屏 production adapter；第二、三頁與存讀檔不得隨此接線。

## CONFORMED 驗收

完成實作後，每個 2×、3× 都必須在同一 original state、同一合法 BIOS 輸入與同一停止點做
原文／繁中 A/B：

1. 原始 indexed framebuffer、CPU／DOS state、輸入、檔案操作與存檔（若路徑觸及）逐項一致；
   繁中只可出現在 RGBA output。
2. active 首屏的 RGBA 差異只能落在 `[8,320)×[136,176)` 放大後的區域；右側資訊、肖像、
   row-24 狀態列及外部所有像素必須為零差異。
3. 按 Enter 的第一筆 story-region 原始改寫後，group 必須在同一輸出 frame 失效；下一頁不得
   殘留首屏中文，亦不得出現未列入 catalog 的第二頁中文。
4. catalog miss、缺字、非法倍率、guard failure、state restore 後未重播 identity 都必須零繪製；
   不得以舊 RGBA layer 或舊 stamp 延續顯示。

只有以上收據通過，才能把本規格標為 CONFORMED，且完成聲明僅限首屏五行與已實測的轉場。

## 權利與散布邊界

本規格、event key、hash、座標、繁中譯文與驗證器可版控；原版遊戲、掃描手冊、英文原文、
合法答案、state、畫面、ETen 原始字型與衍生 GOLEMFNT 一律不進 Git、GitHub 或公開封包。
原版缺席時公開程式必須跳過原版驗證，不能宣稱已對拍。
