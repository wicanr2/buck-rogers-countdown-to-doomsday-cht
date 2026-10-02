# 005 — 手冊繁中輸出端 presenter 整合

狀態：**CONFORMED（明確 presenter 範圍）**。本狀態只涵蓋 39／39 catalog 與字型預檢、
14 行 renderer、2×／3× RGBA，以及已量測的首題、錯答換題、第三題與成功返回同狀態收據。
**不包含 39 題逐題正常玩家路徑、存檔／讀檔或正式互動視窗；39／39 catalog 不等於
39／39 runtime 驗收。**
> 2026-10-02：E1 已由規格 053 接入正式玩家路徑（zh-TW 3×，限縮 CONFORMED，證據 phase-317）；下列為當時的狀態。

2026-09-25 新增的 3× E1／14px adapter 分支僅為 **READY 契約**，尚未實作或取得新版
原版同狀態收據；上方 CONFORMED 不外推至 E1。
日期：2026-09-23
現況訂正（2026-09-23）：第九十六至一百零四階段與 dosgolem spec 216、217、220、221、
222 已推翻本文件早期的「正式字型候選」「前景色未知」「尚未接 runtime」及「尚未驗證
遊戲內返回」狀態。現行本機正式字型含 961 個 glyph，已量原版色彩事件，並完成下列
明確範圍的 2×／3× 同狀態驗收。其餘 38 題不可因 catalog 靜態預檢而宣稱逐題 runtime
完成；存讀檔與正式互動視窗也仍在本規格範圍外。
前置：[手冊段落覆繪](002-manual-paragraph-overlay-draft.md)、
[手冊事件 adapter](003-manual-event-adapter.md)、[第十八階段 lifecycle 證據](../re/phase-18-manual-generation-invalidation.md)、
[第八十五階段整合稽核](../re/phase-85-manual-presenter-integration-readiness-audit.md)、
[第八十六階段 lifecycle 接線](../re/phase-86-manual-presentation-lifecycle.md)、
[第八十七階段多行 presenter 核心](../re/phase-87-manual-multiline-presenter-core.md)、
[第八十八階段字型來源稽核](../re/phase-88-manual-formal-font-subset.md)、
[第九十階段 queue consumer 純核心](../re/phase-90-manual-presentation-queue-consumer.md)、
[第九十一階段 watcher snapshot bridge 純核心](../re/phase-91-manual-watcher-snapshot-bridge.md)、
[第九十二階段候選 manifest 驗證](006-formal-font-candidate-manifest-validator.md)、
[第九十三階段倚天候選輸入盤點](007-eten-15-font-candidate-intake-draft.md)。

> 2026-10-02：E1 的啟用語言由 zh-TW 擴及 zh-CN、ja、ko（規格 055，同時放寬 plan 對 ASCII 終端標點的處理，zh-TW 的 plan 版面不變）。

## 目的與邊界

本規格定義 `apps/buckrogers` 手冊 presenter 的輸出端接線。它只把既有
`DisplayRequest` 轉為 2×或3× RGBA 的繁中段落；不修改 DOS VRAM、原版記憶體、BIOS
輸入、答案比較、檔案或存檔，也不處理 host 設定面板。

原版頁碼、英文標題與序數保持可見。唯一可繪製正文區為正式
`manual-overlay-layout.tsv` 的 `[7,312)×[72,184)`；文字 anchor 是 `(16,72)`，固定
36 欄×14 行、504 Unicode 字元上限。這不是整框替換、中文題目重寫或手冊攻略顯示。

## 已證實前提

| 前提 | 分級 | 證據／結論 |
| --- | --- | --- |
| typed 顯示請求 | 已證實 | `apps/buckrogers/manual.go` 的 `DisplayRequest` 只有 generation、event key、text key、translation；`Catalog.Resolve` 是精確身分查找，不含答案或輸入。 |
| presentation lifecycle queue | 已證實／CONFORMED | dosgolem spec 216 與第 86 階段已將 exact begin、active-context clear、catalog-hit request 以 generation 輸出；queue value-copy 不持有 renderer、machine 或 input 參照。 |
| 正常玩家事件 | 已證實 | 第 85 階段以 `phase12-before-question.state` 在 #266,557,246 得到 `manual.page34.deimos_prison.word10`；完整事件順序及固定 state 見研究收據。 |
| 新題／局部 clear 邊界 | 已證實 | `2A33:01ED` 題首開始新 generation；`026F:029C` 可在 pending 中途出現；只有 `2A33:0309` 的 guarded post-call 可提交 request。第 18 階段的答錯重抽反例排除了「等全畫面清空」與「及早顯示新段落」。 |
| 正式正文幾何與容量 | 已證實 | `text/manual-overlay-layout.tsv`、`tools/manual_overlay_layout.py`；39 筆正式譯文全部通過 504 字元上限。這是 catalog／layout 預檢，不是 39 題逐題 runtime 證據。 |
| 2×／3× RGBA 基礎 | 已證實 | `xlate.Layer` 與 `ScaleIndexedRGBA` 只讀 indexed framebuffer／palette，建立 RGBA；既有 runtime overlay constructor 已拒絕 2、3 以外的倍率。 |
| 手冊多行 presenter | 已證實／CONFORMED | dosgolem spec 217、222 與第 87、96 至 104 階段：唯一 layout loader、14 個背景＋14 個文字 stamp、2×／3×、generation state 與 RGBA containment，並已接入正常玩家 instruction loop。 |
| presentation queue consumer | 已證實／CONFORMED（純核心） | dosgolem spec 220 與第 90 階段：只接受 `PresentationEvents()` append-only value snapshot，先驗證完整已消費 prefix，僅在 `Apply` 成功後推進 cursor；未接 watcher callback、command 或遊戲 loop。 |
| watcher snapshot bridge | 已證實／CONFORMED（純核心） | dosgolem spec 221 與第 91 階段：只將 `PresentationEvents()` defensive snapshot 轉送給 consumer，沒有第二份 cursor；未接 command、frame loop 或玩家畫面。 |
| 字型需求與正式本機字型 | 已證實／CONFORMED（本機使用） | 正式 catalog 與目前 story／UI 需求已重生為 961 glyph 本機 GOLEMFNT；第 100、102、104 階段的 coverage／fontcheck 均為零缺字。此結論不授權公開散布字型。 |
| 候選 manifest 驗證器 | 已證實／CONFORMED（候選審查工具） | project spec 006 的 `validate-candidate` 以 strict manifest 驗證 source／license SHA、既有 parser coverage 與 character-list SHA，無寫入字型路徑；它不採用候選或判定可散布。 |
| 正式字型 | 已證實／CONFORMED（本機使用） | project spec 008 與第 96、100、102、104 階段：本機倚天 15 點字型採 `top-pad` 轉成 16×16 GOLEMFNT，已接 runtime；2× 維持 16×16，3× 的 CJK ink 為 22×22、置於 24px cell 並偏移 1px，ASCII 維持 16×16。不得公開散布原字型或衍生字模。 |
| 可直接重用的手冊 presenter | 已證實為否 | `RuntimeMenuOverlay` 驗證的是單列 `MenuOverlayRects`／`TextEvent` 幾何；它沒有讀取手冊 layout TSV、14 行段落分格或手冊 lifecycle 接線。可重用的是其 RGBA／`xlate.Layer` 模式，不是該 adapter。 |

上表的 dosgolem 實作與測試版本分別由所引 spec 216、217、220、221、222 的 provenance
欄位固定；不可再以本規格起草時的單一舊 commit 代替各階段收據。位址為 dosgolem 實模式
`segment:offset`，不是 IDA 線性位址。

## 擬定 presenter 契約

1. 建立 `RuntimeManualOverlay(layout, catalog, font, scale)` 時必須讀取並驗證唯一正式 layout，
   要求 16×16 字型、所有正式 translation 均有 glyph，且 `scale` 僅為 2 或 3。任一檢查
   失敗時不建立 presenter、不得局部顯示。
2. 每筆 translation 按 Unicode rune 以 row-major 填入 36 欄×14 行；每行建立一筆
   8 logical-pixel 高的 stamp，x=`16`、y=`72 + 8×row`、36 格。未用格仍覆蓋為同一行的
   背景色，以清除該行原版英文墨跡；字形只限於各格的 scaled 邊界內。
3. presenter 必須持有自己的手冊 layer。收到確認的 `begin(generation)` 時，立即丟棄該
   layer 的所有舊段落；這只改 presentation state，不寫回機器。收到確認的
   `request(generation, DisplayRequest)` 時，僅當它屬於現行 pending generation 才原子加入
   14 行段落。收到確認的 `clear` 時，只移除目前已顯示段落；若當前 generation 仍 pending，
   不得捏造 request 或重設 collector metadata。
4. 每個原版 frame 先以同一 indexed framebuffer／palette 呼叫 `Layer.Frame`，再以同一倍率
   將 RGBA baseline 與手冊 layer 合成。任何 scale 只改 output 像素大小，不改 320×200 原始
   framebuffer 或 DOS 狀態。
5. 請求、文字鍵、generation、原版題目 identity 與手冊資料均由既有 watcher／catalog 提供；
   presenter 不重新比對英文、不接受原始答案，也不以未命中或近似條目補譯。

## 現行接線與證據邊界

dosgolem spec 216、217、220、221、222 已把 `PresentationEvents()` 的 exact begin、
active-context clear 與 catalog-hit request，經唯一 snapshot bridge／consumer 接到
`RuntimeManualOverlay` 與正式 instruction loop。generation、完整 prefix、成功後才前進 cursor、
14 行原子 Apply、缺字／非法倍率／不連續事件失敗即關閉等契約都有定向測試；presentation 路徑
不寫 machine、鍵盤、答案比較或 DOS input。

正式 constructor 會預檢 39 筆 catalog translation 與 glyph coverage。2× 保持 16×16；3× 使用
24px cell，CJK ink 為 22×22 並偏移 1px，ASCII 維持 16×16。正常玩家收據已覆蓋首題、答錯後
generation 清除與第二題 exact hit、第三題 exact hit，以及答對成功返回後清除；2×／3× A/B 的
安全矩形外差異為零，相關原版 indexed frame、machine／DOS state 亦依各收據相等。

上述證據只足以 CONFORM 這個明確 presenter 範圍。39／39 catalog 是靜態資料、layout 與字型預檢，
不能替代其餘 38 題逐題正常玩家 runtime；存檔／讀檔與正式互動視窗也未納入本次驗收。倚天字型
及衍生 GOLEMFNT 只獲准本機使用，不得公開散布。

2026-09-24 的[首題前後雙側收據](../re/phase-223-manual-first-question-host-mixed-script-draft.md#2026-09-24-首題-request-前後的同狀態邊界)
從合法原版 checkpoint 量到 begin→clear 後、request 前 2×／3×
皆無正文作用層與像素差；request 後中文只改正文安全矩形，
machine／DOS 同值。request 前收據使用 ignored DRAFT CLI clone
處理通用 recorder 的 pending 終態，正式 CLI 仍拒絕該停點；
此補證不擴張本規格的 CONFORMED 範圍至完整 Linux 玩家路徑。

## 2026-09-25 手冊 3× 混排決定與 DRAFT 邊界

使用者看過首題的現行 3× 固定字格、全中文示意與緊縮英文原型後，
選擇**保留中文印刷手冊中的 RAM、Deimos、Stockade 等英文專名，
改善中英混排與英文詞界**；未核准的全中文新譯名不得進入正式
`manual.zh-TW.tsv`。目前 `manualRows` 以 36 欄×14 行逐 rune
切行，3× 每字固定 24px advance；因此既有 16px ASCII 墨跡
呈現疏距，英文詞也可能被行尾拆開。緊縮字母的 D 原型只改墨跡
位置，尚未處理跨行詞界；這些原型都不是新版正式收據。

[Issue #21](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/21)
負責以**可丟棄原型**量測 3× 英文 advance、英文詞／括號換行、
39 段容量及安全矩形，再經證據審查決定限縮 READY 契約。
2× 原有排版與 RGBA 必須逐位元不變；原版題目、判定、存檔與
手冊 catalog 文字鍵也不得改。正式 3× 混排尚未完成 READY
審查與 production 同狀態驗證，本節僅 DRAFT；前文固定字格的 CONFORMED 範圍不自動
轉移到新演算法。[第二百二十三階段追加的 E1／E2 原型](../re/phase-223-manual-first-question-host-mixed-script-draft.md#2026-09-25-保留英文專名的變動字距-e1e2-原型)
已用整行共同游標對照 14px／16px 英文 advance，兩案均保留專名、
39 段靜態可容納、安全矩形外零差、2× 正式 RGBA 不變；實際
advance 已由使用者選定 **E1／14px**，排除 E2／16px；這仍不是
production 同狀態驗收。READY 審查須先確認 E1 的 token 化與
全 39 段、標點／括號、超長詞拒絕、字模安全矩形、清層／還原及
雙層 owner 身分，再授權正式 3× presenter 實作；2× 不得變動。

獨立審查已確認目前**尚不足以升 READY**：E1 只在 test-local
RGBA compositor 繪製；共用 `xlate.Stamp` 的字首座標乘以 3×，
不能表示精確 14px advance。正式 owner 又以 36-rune
`manualRows` 核對每列身分，不能只替換畫筆而保留舊快照契約。
現行原型也尚未對 39 段的數字、`./+-%`、中英標點、括號配對、
每字 ink bbox、行首行尾禁則及逐段 round-trip 建立完整負例。
因此下一個 READY 前提是補 tokenizer／immutable layout plan、
字型幾何、共用像素精度 API 與 owner
生命週期契約；不得讓 test-local 最終 RGBA 直接旁路正式清層。
使用者隨後已選**擴充 dosgolem 共用繪字引擎**，排除 Buck 手冊
專用像素層。這只確定架構邊界：共用 API 必須能封存實體像素
字首位置／advance，驗來源與 layout plan，並讓既有固定字格
覆繪及 2× 輸出逐位元保持原樣；擴充方式與負例矩陣尚待獨立
審查，不得直接把 DRAFT compositor 作正式捷徑。
共用 API 的限縮候選是在既有 `xlate.Stamp` 上增加**可選**的
物理像素 glyph plan 與綁定倍率；舊 stamp 無新欄位時保持原
Draw／Snapshot bytes。新 glyph 只承擔位置與 source crop，
原 `Cells`／`CellW` 仍承擔清除、指紋、錨定與透明格；封存需
同時驗 base16、derived22 字型身分。test-local 最小幾何原型
已驗 14px 字首與 partial transparent，但 Snapshot／Restore／
封存／owner 尚未驗，不能因原型通過而升 READY。

全 39 段的 test-local 詞界計畫已補英數與 `./+-%`、短括號
英文詞、長中文引號，以及正式字型最大 ASCII 墨跡 8px
的測量；但獨立檢查收據仍有 3 個行首、11 個行尾空白 token，
且 `…` 尚未納入不可行首標點集合。因此此輪只能將「字詞不拆
與 rune round-trip」列為已驗 DRAFT，不能把 39 段版面列為
READY。下一版須用 soft separator 保存原文空白但不將其繪成
行界空白，並補標點／跨 run 負例；只有通過獨立審查後，
才能固定不可變 3× layout plan，接進共用 API。

後續 test-local 修訂已讓原 3 行首／11 行尾 ASCII 分隔符以
zero-width soft separator 保留 source-span／rune round-trip，
不再形成可見行界空白；補了 `…` 禁行首與跨 ASCII run
碰撞測試，39／39 段私有收據重驗通過。這訂正上述排版
缺口，**不**將 DRAFT tokenizer 自動升為正式 immutable plan。
dosgolem fork 的 `docs/spec/234-xlate-physical-pixel-glyph-plan.md`
已獨立審查至 READY（僅 API 契約），可先實作共用層；
本手冊 adapter 的 owner／雙字型封存／正式 A/B 仍需另審。
共用核心第一段已在 ignored fork 本機提交 `8f56d0e`，
checked 字首繪製與 optional Snapshot／Restore 的定向
測試通過；仍未把本規格的 3× 手冊版面計畫送進正式
`ManualSnapshotOwner`，也未做正式原版同狀態 A/B。

## 2026-09-25：3× E1 adapter（**無頭限縮 CONFORMED**）

本節是 Issue #21／#14 的 adapter 契約。它把已確認的 E1
14px、39／39 私有 catalog tokenization 收據，以及共用 `xlate`
規格 234 的 READY API 邊界，收束成可實作的 typed immutable layout plan。
本節已經獨立 READY 複審，准許進入 production 實作；它不改寫本文件
先前固定格 presenter 的 CONFORMED 範圍，不得以本節或其定向測試宣稱 3× E1 已
CONFORMED。

### 輸入與不可變輸出

每個 catalog hit 在 `request(generation, DisplayRequest)` 後，僅可由
adapter 以該 request 的已驗 `eventKey`、`textKey`、UTF-8 translation、
正式 layout、當前 3× E1 字型登錄，建立一個新的
`ManualE1ImmutablePlan`。此 plan 是值物件：所有 rune slice、token、
glyph crop、字型身分與 hash 必須深複製並在建立後不可由 caller、catalog、
font map 或 renderer 修改；它不是 `RuntimeManualOverlay`、`xlate.Layer`
或 `ManualFrameTicket` 的別名。

最小型別語意如下（欄位名稱可按 Go 慣例調整，但語意與 hash 編碼不可改）：

```text
ManualE1ImmutablePlan {
  Generation, EventKey, TextKey
  TranslationUTF8, TranslationRuneCount
  Scale = 3, LatinAdvancePx = 14
  ClearRectPhysical = [21,936) × [216,552)
  TextRectPhysical  = [48,912) × [216,552)
  Base16Font{Name, FontSealSHA256}
  Derived22Font{Name, FontSealSHA256}
  Lines[14] ManualE1Line
  CanonicalLayoutSHA256
}
ManualE1Line { Row, YPhysical, UsedPixels, Tokens[] }
ManualE1Token {
  Kind, SourceRuneStart, SourceRuneEnd, Runes, XPhysical, AdvancePixels,
  Glyphs[] ManualE1GlyphSpec
}
ManualE1GlyphSpec {
  Rune, FontRole, FontName, FontSealSHA256,
  SrcX, SrcY, SrcW, SrcH, XPhysical, YPhysical
}
```

`CanonicalLayoutSHA256` 須涵蓋上述每個決定繪製或 source-span 的欄位，
使用下列固定、非 map 的二進位編碼：先寫 ASCII domain
`buckrogers-manual-e1-layout-v1\\x00`，再依序寫 `Scale`、
`LatinAdvancePx`、`ClearRectPhysical` 的 X、Y、W、H、`TextRectPhysical` 的
X、Y、W、H、固定值 `14`（line count），皆為 little-endian u32；每一列依
row 0 至 13 寫 `Row`、`YPhysical`、`UsedPixels` 與 token count（u32）；每個 token 固定寫
`Kind` UTF-8 byte length（u32）與 bytes、`SourceRuneStart`、
`SourceRuneEnd`、`XPhysical`、`AdvancePixels`（u32；負值在編碼前拒絕）、
rune count（u32）及每一碼點（u32）、glyph count（u32）；每個 glyph 依序寫
`Rune`（u32）、`FontRole` UTF-8 length＋bytes、`FontName` UTF-8 length＋bytes、
32-byte `FontSealSHA256`、`SrcX`、`SrcY`、`SrcW`、`SrcH`、`XPhysical`、
`YPhysical`（u32；負值或不合法 crop 在編碼前拒絕）。最後寫 plan 的
`Generation`、`EventKey` UTF-8 length＋bytes、`TextKey` UTF-8 length＋bytes、
`TranslationRuneCount`（u32）、`TranslationUTF8` byte length（u32）與 bytes，
以及 base-16／derived-22 各自的 name UTF-8 length＋bytes 和 32-byte hash。
這些數值欄位的順序是 hash 契約；不得使用 `%v`、JSON 或 Go map。

`FontSealSHA256` 固定來自 `presentation.FontFingerprint`，其輸入包含
`Font.Name`、尺寸與排序後的 glyph bytes，是 adapter／封存群組的字型身分。
它**不是** `xlate-font-v1` canonical bytes hash：後者只由 `xlate.Snapshot`／
`Restore` 驗證實體 glyph 的可還原來源；兩種 hash 必須分欄儲存與核對，不得
混稱或互相取代。`ManualE1GlyphSpec` 是純值，不得含 `*xlate.Font`、map、layer、ticket 或
其他可變指標。它的 `X/Y` 是最終 RGBA 的絕對實體像素，crop 是非空半開
source rect。owner 只可在建立 text stamp 時，從私有、已驗的字型 registry
以 `FontRole`＋`FontName` 解出 `*xlate.Font`，再核對 `FontSealSHA256`；
這個解出的指標不得回寫或逃逸到 plan。ASCII glyph 使用已封存 base-16，CJK
與全形標點使用已封存 derived-22；不得只比較字型名稱，亦不得讓後續的
`manualThreeXFont` 重建結果悄悄取代 plan 所封存的身分。

同一 token 有多個非 ASCII glyph 時，每個 glyph 的 `XPhysical` 必須是其
各自的共同 cursor 位置，不可全部復用 token 起點。CJK 依 24px advance
逐字前進；窄全形括號依已量測 bbox advance 前進；其餘全形標點依其 token
measure 前進。每筆 glyph 的 crop 與 X/Y 都必須可單獨驗證，不可把「同一
token 的寬度正確」當成逐 glyph 不重疊的證據。

每一列仍以既有 logical parent text stamp `[16,304)×[y,y+8)` 作為
clear／anchor／失效語意的 parent，背景 stamp 仍清除
`[7,312)×[72,184)`。實體 glyph 必須完全落入該 parent 的 3× 範圍，
並經 `Layer.ValidatePixelGlyphPlan(3)` 與 `DrawChecked(..., 3)` 的全層
預檢；不得以直接 RGBA compositor 旁路清層、Snapshot 或 Restore。
2× 不建立也不消費此 plan，必須維持現有 2× stamp、Snapshot JSON 與
RGBA 位元組。

14 列中有 source token 的列必須建立 `PixelScale=3` 且非空
`PixelGlyphs` 的 physical text stamp；無 token 的尾端列必須建立
`PixelScale=0`、無 `PixelGlyphs`、無 `Text` 的 legacy empty stamp，不能以
空 physical plan 充數。owner 一律封存 14 列；Snapshot／Restore 後須保留
每列是否 physical 的身分，並在投影前再驗。

### E1 token 化與版面不變量

- 識別字為 ASCII 英數，連接符 `.`、`/`、`+`、`-` 只可夾在兩個英數
  run 之間；`%` 只可作該識別字的尾碼。整個識別字不可拆行。確證
  advance 是第一個 ASCII glyph 16px、後續 glyph 各 14px；不是 14px
  字寬的猜測。
- 配對 `（）、()、「」、『』、【】、《》、〈〉` 必須巢狀正確且不拆開。
  短括號識別字是一個 token；其餘配對把開括號併到第一個內部 token、
  閉括號併到最後一個。未配對開／閉括號失敗即關閉。
- `、，。！？：；…` 不可在可見行首，必須併到前一 token；開括號不可
  在可見行尾。這包含已補證的 `…`，不能沿用舊 prototype 漏列的集合。
- source 的 ASCII space 必須原樣保存在 `SourceRuneStart/End` 與
  `TranslationUTF8` round-trip；首尾或連續 space 拒絕。若換行使 space
  位於行首或行尾，它是 `soft_separator`：glyph 數為零、advance 為零、
  不產生可見墨跡，卻仍參與 source-span 與 canonical hash。39／39
  私有收據已確認共有 3 個此類行首及 11 個行尾 separator；該數量是
  該固定 catalog／字型版本的 audit anchor，不是一般演算法常數。
- 每列由左至右使用共同實體像素 cursor，範圍 `[48,912)`，高 24px，
  最多 14 列，行距 24px。CJK cell advance 24px；一般 interior space
  advance 8px；窄全形括號以 derived-22 實際 ink bbox 加兩側各 2px
  導出。若 `bboxW + 4 > 20`，必須失敗即關閉；不可 clamp 成 20、裁切
  墨跡或把 glyph 推到 parent 外。合法窄括號 advance 為 `[8,20]`，不得以
  未量測常數代替。每個 ASCII glyph
  實際 ink bbox 都須在其 token range 內，且相鄰 run ink 不得重疊。
- 任何空 translation、未知 glyph、空／越界 crop、無法容納的 token／
  paragraph、溢位座標或尺寸、非 3× scale、字型 hash 不符、canonical
  hash 不符、或建立後可觀測的 plan 變造，皆不得交付部分 plan、部分
  layer 或 RGBA。

### owner lifecycle 與失敗收束

`ManualSnapshotOwner` 必須從「重算 36-rune `manualRows`」改為驗證已
封存 `ManualE1ImmutablePlan`，但僅在 E1 3× owner。它必須同時驗
generation／event identity／text identity／layout hash／兩個字型 hash／
scale，並把 plan 與 14 background + 14 text parent stamps 封存成同一
group。`PrepareFrame` 前、`Snapshot` 前、Restore 後與投影前均重驗；
任一不符即回錯、使 ticket 失效且不產生 RGBA。

`begin`、accepted `clear`、新 request、`SetStyle`、Restore、來源不連續、
stop／Close、scale replacement 與 consumer prefix error 都必須退休舊
plan 和所有 ticket；不能讓舊 E1 glyph 在 clear 後復活。新 request 只在
完整 immutable plan、兩層 layer 與 seal 均成功後才可原子可見。owner
仍是同 machine-step goroutine 的唯一可變持有者；frontend 不得取得
plan 內部 slice、layer、font map 或可重畫 ticket。

### READY 審查收據與實作後驗收矩陣

| 面向 | READY 前無原版素材已驗 | 待 implementation／oracle 驗收 |
| --- | --- | --- |
| 39 段輸入 | 固定 39／39 私有 catalog 逐段建立 immutable plan，以現行本機 base／derived 字型的 `presentation.FontFingerprint` seal 檢查 source span、canonical hash 重算、crop 與位置；3 行首＋11 行尾 soft separator 必為零寬 | 不把 private translation、font 或 receipt 加入 Git；由審查者在本機重生 anchor |
| E1 幾何 | 14px ASCII 字首、16px 首 glyph、22px CJK、窄括號實際 ink-bbox `SrcX/SrcY/SrcW/SrcH` crop、token bbox、跨 run ink collision、14×24px 行界與安全矩形 | 每段以 spec 234 `ValidatePixelGlyphPlan`／`DrawChecked` preflight；對 14 列 Snapshot／Restore 再繪製，驗 legacy 尾端空列與 physical 非空列均保留 |
| 字串規則 | 英數及 `./+-%`、巢狀括號、`…` 與其餘禁行首標點、超寬 token、來源首尾／連續 space 全有正反例；每個 token 的連續 source rune span 重組必須逐 rune 等於 UTF-8 原文，包括零寬 soft separator | 將 token source-span 與固定 domain／欄位／長度前綴的 canonical encoding 交叉檢查，拒絕 mutation／hash drift |
| owner | 共用 sealed group 的 generation／epoch 變造在讀影格前拒絕；E1 plan 純值／hash／來源位置的合成變造在轉 xlate 前拒絕 | 正式 owner 的 generation、clear、換題、Restore、Close、stale ticket、雙字型同名異 bytes、跨倍率均失敗即關閉；2× 不變 checkpoint 逐 byte 回歸 |
| 同狀態 | 不以 unit test 冒稱原版 parity | 合法首題、答錯換題、成功返回的 3× E1 A/B；indexed、machine、DOS、input、save 同值，RGBA 差異僅在核准 clear rect |

READY 複審已確認固定編碼、純值 plan 與字型封印、39／39 現行本機字型
preflight、窄括號過寬拒絕、14 列 Snapshot／Restore，以及 spec 234
production 共用 API；主代理於 Docker 獨立重跑 39／39 私有 catalog 的
`-race -count=2` 通過。這些收據只准許建立 production plan／改動
`ManualSnapshotOwner`；owner 全生命週期負例與表中同狀態收據完成後，
才可將 E1 分支稱為 CONFORMED。被忽略的
`manual_ascii3_wordwrap_draft_test.go` 只提供無原版素材的定向測試與
私有 audit，不是 production test suite。

### 2026-09-25 E1 implementation 後局部驗收（狀態仍 READY）

本機未推送的 dosgolem fork `c39f72a` 與 `5fcc1d6` 已實作
正式 3× E1 plan／owner；正式 39／39 私有字型 preflight、
checked draw、Snapshot／Restore、2× 合成 golden bytes，
以及換題／清除舊 ticket 失效負例均通過。以現行 catalog
及既有合法原版 checkpoint，首題終態、錯答換題、答對返回的
2×／3× 新版 owner 同狀態測試均通過：原版 indexed／palette／
記憶體、輸入排程與正規化 machine／DOS 狀態相同；RGBA 只在
核准手冊矩形內有變化，返回清除後零差且不可再建立可見 ticket。
兩條後續情境的 2× RGBA 與舊收據逐位元相同。完整量測及
原始 `.state` 非決定性序列化的比較勘誤，見
[第二百二十三階段研究紀錄](../re/phase-223-manual-first-question-host-mixed-script-draft.md)。

這些是固定 checkpoint 的無頭局部收據，不包含正式 Linux
session 的冷開機玩家視窗、其餘 36 題逐題重播或其他段落專名的
runtime 樣本；當時因此 E1 分支不升 CONFORMED。後續完整重跑與
獨立複審見下節判定。

另以既有合法第三題 checkpoint 驗 `manual.log.57.acidic_victory`
中的 `RAM`：正式 3× plan 保持單一 token／同一行，字首各距
14px；2×／3× 同狀態及安全矩形外零差通過。舊第三題 2×
截圖使用 101 字譯文，現行為 104 字，不可作逐位元相等基準。
這是另一段英文詞界的局部證據，仍未覆蓋其他專名的玩家視窗。
其後手冊第 9–12 筆中文印刷本修訂已由使用者選定**中文印刷本優先**
正式入版（`manual.zh-TW.tsv` SHA-256
`186b0844b7040a461c2e06f2a3e670e86dd28f3773cc46c3a6516e340c773f0b`），
本機 1,046 字倚天子集（`font/characters.txt` SHA-256
`e6973763953ba738854376bdcc049a87b76540616b6626405ed1fb5489073b0b`，
GOLEMFNT `14fca041…`）重建後，正式 39／39 E1 plan 的 checked draw／
Snapshot／Restore 再以 `-race` 通過；上述四條本機 owner
oracle 亦用定版字型重跑，首題 2×／3× RGBA 與定版收據一致。
字型來源身分見[規格 024](024-manual-layer-group-font-identity-ready-candidate.md)。
首題三英文專名（3× RAM、括號 Deimos、行尾 Stockade）另有正式量產
斷言 `TestManualE1PlanDeimosPrisonEnglishTokens`：各落單一 sealed
token 且 ASCII 相鄰字首皆 14px，Docker 無網路 `-race` 通過。

### 2026-09-25 E1 無頭限縮 CONFORMED 判定

主代理以定版 catalog＋定版 1,046 字字型，在無網路 Docker
（`eob-remake-go:1.26.7-ebiten2.9.9`、`--network none`、
原版唯讀掛載 `/orig`）重跑 READY 矩陣：`TestManualE1Plan*`
全數（含 39／39、`-race`）、`TestManualSnapshotOwner*` 全數
（含雙字型生命週期負例、2× golden bytes、`-race`）、
首題／換題（target-002）／返回（return-clear）／第三題
（target-003）oracle 雙倍率 `-race` 全綠；control／2×／3× 的
indexed、palette、記憶體、輸入排程與正規化 machine／DOS 同值，
RGBA 差異僅在核准矩形，返回後零差、舊 ticket 不可復活、
零檔案寫入。獨立審查員以同條件獨立重跑 token 斷言與三案
lifecycle oracle 通過，並核對無 Linux／36 題冒稱
（`ses_f29819a80ffeaVLQyp1podIrbq` 收據只留審查結論，
無原版素材）。

因此 E1 分支升為**無頭限縮 CONFORMED**，範圍僅：首題、
錯答換題、答對返回、第三題的固定 checkpoint 同狀態收據，
39／39 plan 靜態斷言，以及 2× 逐位元不變。以下明確排除，
不得外推：正式 Linux 冷開機玩家視窗（#16）、其餘 36 題逐題
重播、遊戲內存讀檔、39 段之外的文字路徑。Issue #21 與 #14
仍保持 OPEN，直到上述排除項完成。

## 與 host 倍率控制的關係

使用者已選擇「先選取，再按套用」（選項 C）。手冊 presenter 只接收明示的 2 或 3，因此可在
兩種倍率各自驗證，不依賴 host 點選事件；host 的 selected scale 只有在 Apply 成功後才可成為
新的 presenter scale。dosgolem spec 219 已 CONFORM 這個 selected／active 的純 state core；
正式 Linux session 尚未把 host 倍率事件接成手冊 presenter 的完整玩家路徑。Go／Ebitengine、
Apply 後自動收合、只保留本次遊戲期間與每次啟動預設 2× 均已在
[規格 004](004-dosgolem-host-frontend-draft.md)定案，不得混入 Buck Rogers adapter。

## READY 前置與 CONFORMED 驗收

明確 presenter 範圍已完成：

- [x] dosgolem spec 216 的 lifecycle queue、generation、begin／clear／request 負向測試及正常玩家 metadata 收據。
- [x] dosgolem spec 217 的 layout loader、14 行 row-major builder、504／505 邊界、缺字與非法倍率的失敗即關閉純核心測試。
- [x] dosgolem spec 220 的 append-only queue consumer、prefix 漂移／縮短拒絕、partial-failure cursor 與純核心測試。
- [x] dosgolem spec 221 的 watcher snapshot bridge、單一轉送、consumer error propagation 與純核心測試。
- [x] project spec 006 的候選 manifest、source／license hash、coverage 與無寫入驗證工具測試。
- [x] project spec 008 的本機倚天 `top-pad` builder、現行 961 glyph GOLEMFNT 回讀與零缺字驗證。
- [x] 正常首題、答錯換題、第三題及答對成功返回的 2×／3× same-state output 收據；request 前、
  catalog miss、pending clear 與返回後都不得畫中文。
- [x] 39／39 catalog／layout／glyph 預檢；此項明確不代表 39 題逐題正常玩家 runtime 驗收。
- [x] 範圍排除已記錄：其餘 38 題逐題 runtime、存檔／讀檔與正式互動視窗不在本次 CONFORMED 聲明內。

CONFORMED 時，原文／繁中 A/B 必須使用同一 state、原版資料、輸入與受控亂數條件（如有）；
原版 indexed framebuffer、記憶體、輸入、答案驗證、檔案及存檔必須一致，差異只可出現在
`[7,312)×[72,184)` 的核准 RGBA 像素。另須證實答錯重抽會在新題 begin 先移除舊段落，並於
新題完整 `word?` 後才顯示新段落，沒有殘字。

第 96、97、102、103、104 階段的收據已在上述明確範圍滿足這些條件；未列入的玩家路徑仍須
另行取得同狀態收據後，才能擴張本規格的 CONFORMED 範圍。

## 2026-09-24：實體 host 中英混排的可見限制

[第二百二十三階段](../re/phase-223-manual-first-question-host-mixed-script-draft.md)
用同一已驗首題原版終態，把正式 `ManualSnapshotOwner` 的 2×／3×
RGBA 交給真正 Ebitengine 視窗；面板實際 Apply 可切換，兩倍率的
每張 owner 快照皆逐 byte 等於既有同狀態收據。這是終態影格顯示，
不是正式 Linux session 的直播接線。

視窗顯示的拉丁字母來自正式繁中 TSV 內保留的英文專名，**不是**
原版英文清除失敗。3× 固定 24px 字格讓這些半形字母過於分散，
部分詞與括號跨越固定 36-rune 行界；這是本規格既有安全矩形／
語意隔離同狀態收據未涵蓋的閱讀品質問題。本規格明確 presenter
範圍的 CONFORMED 判定不外推到「手冊中英混排已定版」；正式譯文
與混排策略等待使用者就專名保留或繁中化作取捨，不可偷偷改正式
catalog 或把可丟棄像素後處理搬進 production。

## 2026-09-24 字型數量勘誤

本規格前文的 961 glyph 是第 100／102／104 階段當時的本機
收據，不是現行譯文全集的字型數量。現行 24 份繁中 TSV 的
`font/characters.txt` 為 1,016 字；最新字型與 manifest 身分
見[規格 024 的勘誤](024-manual-layer-group-font-identity-ready-candidate.md)。
正式 Linux session 仍須在啟動前按當次 catalog 驗證本機字型，
不能沿用 961／1,028／1,025／1,023 的歷史數量。
