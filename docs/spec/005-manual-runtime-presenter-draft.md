# 005 — 手冊繁中輸出端 presenter 整合

狀態：**CONFORMED（明確 presenter 範圍）**。本狀態只涵蓋 39／39 catalog 與字型預檢、
14 行 renderer、2×／3× RGBA，以及已量測的首題、錯答換題、第三題與成功返回同狀態收據。
**不包含 39 題逐題正常玩家路徑、存檔／讀檔或正式互動視窗；39／39 catalog 不等於
39／39 runtime 驗收。**
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
