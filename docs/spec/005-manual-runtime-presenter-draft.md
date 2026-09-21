# 005 — 手冊繁中輸出端 presenter 整合

狀態：DRAFT  
日期：2026-09-21  
前置：[手冊段落覆繪](002-manual-paragraph-overlay-draft.md)、
[手冊事件 adapter](003-manual-event-adapter.md)、[第十八階段 lifecycle 證據](../re/phase-18-manual-generation-invalidation.md)、
[第八十五階段整合稽核](../re/phase-85-manual-presenter-integration-readiness-audit.md)、
[第八十六階段 lifecycle 接線](../re/phase-86-manual-presentation-lifecycle.md)、
[第八十七階段多行 presenter 核心](../re/phase-87-manual-multiline-presenter-core.md)。

## 目的與邊界

本規格定義未來 `apps/buckrogers` 手冊 presenter 必須補齊的輸出端接線。它只把既有
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
| 正式正文幾何與容量 | 已證實 | `text/manual-overlay-layout.tsv`、`tools/manual_overlay_layout.py`；22 筆正式譯文全部通過，最長 236 字。 |
| 2×／3× RGBA 基礎 | 已證實 | `xlate.Layer` 與 `ScaleIndexedRGBA` 只讀 indexed framebuffer／palette，建立 RGBA；既有 runtime overlay constructor 已拒絕 2、3 以外的倍率。 |
| 手冊多行純核心 | 已證實／CONFORMED（純核心） | dosgolem spec 217 與第 87 階段：唯一 layout loader、14 個背景＋14 個文字 stamp、2×／3×、generation state 與 synthetic RGBA containment；尚未接入正常玩家 runtime。 |
| 字型需求清單 | 已證實 | 由正式 `manual.zh-TW.tsv` 重生的未追蹤清單有 691 個碼點，SHA-256 為 `dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f`。 |
| 可直接重用的手冊 presenter | 已證實為否 | `RuntimeMenuOverlay` 驗證的是單列 `MenuOverlayRects`／`TextEvent` 幾何；它沒有讀取手冊 layout TSV、14 行段落分格或手冊 lifecycle 接線。可重用的是其 RGBA／`xlate.Layer` 模式，不是該 adapter。 |

上表的 dosgolem source 均固定為本機 branch `buck-rogers-cht-output-overlay` 的
`21c9295c90fac44b5852fd5934a6d027342cde24`；位址為 dosgolem 實模式
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

## 現有接線缺口

第八十六階段已在 dosgolem spec 216 實作並 CONFORM `PresentationEvents()`：exact begin、
active-context clear、catalog-hit request 皆帶 generation，且 accessor 回傳 value-copy。它只提供
presentation metadata，沒有 machine write、鍵盤或 DOS input 路徑；receipt 也只投影 key／rune count。
第八十七階段的 `RuntimeManualOverlay` 已將此 value 型別消費為純核心，並以兩個 layer 完成 14 行
background／text 合成；它仍沒有 callback 或 command 接線。未來 runtime 必須消費這條 queue，不得
倒回 `Observations()` 猜測世代。

此外，目前只有字元需求清單；正式字型檔的來源、授權告知與每個 glyph 的實際回讀仍須按
`font/README.md` 完成。不能以缺字回呼後的部分畫面當作可接受輸出。

## 與 host 倍率控制的關係

使用者已選擇「先選取，再按套用」（選項 C）。手冊 presenter 只接收明示的 2 或 3，因此可在
兩種倍率各自驗證，不依賴 host 點選事件；host 的 selected scale 只有在 Apply 成功後才可成為
新的 presenter scale。host 面板的 backend、套用後是否自動收合與跨重啟持久化仍屬
[規格 004](004-dosgolem-host-frontend-draft.md)，不得混入 Buck Rogers adapter。

## READY 前置與 CONFORMED 驗收

進入正式程式前必須完成：

- [x] dosgolem spec 216 的 lifecycle queue、generation、begin／clear／request 負向測試及正常玩家 metadata 收據。
- [x] dosgolem spec 217 的 layout loader、14 行 row-major builder、504／505 邊界、缺字與非法倍率的失敗即關閉純核心測試。
- [ ] 可重生且已授權的手冊 GOLEMFNT 子集，以及 691 glyph 的回讀驗證。
- [ ] 正常第一題及答錯換題的 2×／3× same-state output 收據；request 前、catalog miss 與
  pending clear 時都不得畫中文。

CONFORMED 時，原文／繁中 A/B 必須使用同一 state、原版資料、輸入與受控亂數條件（如有）；
原版 indexed framebuffer、記憶體、輸入、答案驗證、檔案及存檔必須一致，差異只可出現在
`[7,312)×[72,184)` 的核准 RGBA 像素。另須證實答錯重抽會在新題 begin 先移除舊段落，並於
新題完整 `word?` 後才顯示新段落，沒有殘字。
