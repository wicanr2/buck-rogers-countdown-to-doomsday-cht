# 009 — 身體圖示畫面文字輸出端覆繪

狀態：CONFORMED（只涵蓋固定 move／refuse／confirm 三條正常路徑）
範圍：角色建立流程的身體圖示選擇、圖示確認與 confirm 路徑的儲存詢問文字
更新：2026-09-23

本規格沿用 [001 功能選單文字輸出端覆繪](001-menu-text-output-overdraw-draft.md) 的
「原版完整繪製、輸出端另建覆繪層、清除／轉場使 stamp 失效」原則；本規格只補上
身體圖示畫面的事件、矩形與動態圖示邊界，不複製或改寫 001 的通用 dispatcher 契約。

證據入口：

- [第一百零一階段身體圖示文字目錄](../re/phase-101-body-icon-text-catalog.md)
- [第四十八階段身體圖示選擇生命週期](../re/phase-48-body-icon-selection-lifecycle.md)
- [第四十九階段儲存詢問與角色完成生命週期](../re/phase-49-save-prompt-and-character-completion-lifecycle.md)
- [第六階段清除路徑與失效 hook 證據](../re/phase-6-clear-path-hook-evidence.md)
- `text/body-icon-events.tsv`
- `text/body-icon-text-safe-rects.tsv`

## 玩家可見範圍與排除項

正式候選只包含七個固定介面文字：確認詢問、儲存詢問、舊／新標籤、舊／新狀態標籤、
以及選擇說明。四個畫面群組是 `confirmation`、`save_prompt`、`body_icon` 與 `selection`；
不同群組可重用相同 row／column，但不可視為同一幀同時存在。

以下內容明確排除：

- 身體圖示本身的像素、選取位置與任何角色／姓名／數值；它們不是文字 catalog。
- 原版儲存判定、`CHARS.DAX`、輸入按鍵、角色規則與任何 DOS／CPU 狀態。
- 依相同 hash、相似座標或相似 caller 模糊擴張出的其他字串。
- 儲存詢問離頁、實際存讀檔／restore、完整開機、固定三條重播以外的輸入路徑，以及
  未觀察到的 writer；它們須另取原版證據後才能擴充 READY 範圍。

## 已證實的輸出事件與矩形

`body-icon-events.tsv` 是唯一 exact identity 入口；每筆必須同時命中原文字格長度、SHA-256、
caller、色號、row 與 column。`body-icon-text-safe-rects.tsv` 由同一 identity 導出：

| 畫面 | 文字鍵 | logical 矩形 | 色彩事實 | 動態邊界 |
|---|---|---|---|---|
| `confirmation` | `body.icon.confirmation` | `[0,192)–[136,200)` | 原版 `0/13` | 只覆蓋詢問文字 |
| `save_prompt` | `body.icon.save_prompt` | `[0,192)–[64,200)` | 原版 `0/13` | 不碰選項反白／存檔 |
| `body_icon` | `body.icon.old.label`／`old.action` | `[64,48)–[88,56)`／`[24,80)–[136,88)` | 原版 `0/15` | 不碰舊圖示像素 |
| `body_icon` | `body.icon.new.label`／`new.action` | `[64,96)–[88,104)`／`[24,128)–[136,136)` | 原版 `0/15` | 不碰新圖示像素 |
| `selection` | `body.icon.selection.instruction` | `[0,192)–[160,200)` | 原版 `0/13` | 不碰圖示選取區 |

矩形均為半開區間，8-pixel logical cell 對齊，單列且 overflow policy 為
`single-line-reject`。同一畫面群組內矩形必須不重疊；不同群組的相同座標不是同時顯示證據。

## CONFORMED 顯示與生命週期契約

1. 原版事件必須先完整執行；覆繪只接受七個 exact identity，並以原版矩形清除其底色後
   在同一矩形內繪製繁中。不得送鍵、修改原版記憶體、改變圖示選取或儲存結果。
2. `0763:0424` 的確認／選擇文字與 `37F1:101E` 的詢問文字，以及 `1C41:2708`、
   `1C41:2729`、`1C41:274A`、`1C41:276B` 的圖示畫面事件，必須各自通過既有
   post-call／glyph candidate 的完整 identity；不可只依 row、caller 或文字長度。
3. 任何已證實的原版矩形清除若與 active stamp 相交，必須使該 stamp 失效；不得把「下一筆
   新文字事件」當成前畫面已清除的證據。尚未量到身體圖示專用清除 hook 前，實作者只能
   先採整組畫面失效，不得保留可能殘留的 confirmation／body-icon／save-prompt stamp。
4. 角色身體圖示畫面的 Left／Right／Up／Down 只改變圖示與 framebuffer；文字覆繪不得
   寫入圖示區，也不得把動態圖示像素加入文字 A/B 差異。Enter／Escape 進入確認詢問時，
   先使 `body_icon`／`selection` stamp 失效，再允許 confirmation stamp；`N` 返回圖示畫面
   時先清除 confirmation，再由新事件重建圖示文字。確認後進入儲存詢問時，先清除舊群組，
   只允許 save prompt；儲存詢問離開至功能選單時，save prompt 必須失效。
5. 原文與繁中 A/B 必須使用同一 savestate、同一正常 BIOS 輸入與同一停止點；原版 indexed
   framebuffer、CPU／DOS／檔案事件與輸入事件必須逐項一致，RGBA 差異只能落在本表核准矩形。
   2×／3× 都需各自檢查矩形外零差異及清除／重建後零殘字。

## DRAFT→READY 證據審查結論

目前已具備（2026-09-23 完整 A000 觀察證據與第二次獨立審查）：

- 七筆文字 identity、來源清冊、繁中 catalog 與七筆安全矩形已由獨立驗證器鎖定。
- Phase 48／49 已證實移動、拒絕、確認、儲存詢問的正常玩家 trace 與逐 byte 重播。
- 原版 `READY ACTION` 語意由 Phase 48 原版畫面證據核對，不以 hash 單獨猜測。
- 可丟棄 projection 已用 Phase 48 六份 A/B 收據精確重生 1／6／2 筆 request；但它不是
  runtime watcher，因現有 `MenuRequestWatcher` 不觀測 `1C41` 低階 glyph calls。
- 七筆低階 glyph 已逐筆證實 verified RETF、同 SS／SP+`0x12` 與逐 glyph 低位／高位 ABI
  契約。正常 move／refuse／confirm 固定排程已由 `Machine.Write8` 前的通用 A000 observer
  完整觀察，包含同值寫入；三組 A／B 逐 byte 相同，並訂正 confirmation／save prompt
  的 earliest pre-write 是 glyph store，而非稍後的 F3AA fill。可丟棄 typed-core 及
  2×／3×正式倚天 containment 已通過。
- 真實 move／refuse／confirm return-event 收據已依 step 直接餵入 watcher，分別驗證
  body-selection→selection-redraw、body-selection→confirmation→body-selection、
  body-selection→confirmation→save-prompt 的原子群組與 generation。
- A000 dirty-state 原型把完整 span 與 event commit 依 recorded step 合併；任何 first
  intersecting write 都先使完整 active generation 原子失效。同值寫、未知 writer／key、
  提早或缺失 first、錯 generation、partial／mixed／duplicate、跨 group 與 span 跨 commit
  均有失敗即關閉負例。14 項 typed-core 測試通過，receipt SHA-256 為
  `982e29362e5b98d812f91ba481b21fb8388932acee28f108d70d47444b7b1985`。

第二次獨立審查判定上述證據足以形成**限縮 READY**。尚未接 production 不是 READY
阻擋，而是下一階段 implementation 的工作；實作不得擴張以下邊界：

- 只接受七個 exact identity 與固定 move／refuse／confirm 的已驗群組及 generation；任何
  未知、部分或混合事件都不得安裝 stamp。
- 正式 watcher／dirty-state 必須保留 prototype 的 pre-write 順序與整代原子失效契約；
  不得以像素是否改變跳過同值寫入，也不得把稍後 F3AA fill 當成 glyph-store first。
- 完整 observer 證據只涵蓋三條固定排程及其已量 step 視窗。儲存詢問離頁、restore、
  完整開機、其他輸入路徑與未觀察 writer 仍排除，不得由本 READY 外推。

## Implementation→CONFORMED 驗收結果

dosgolem 本機分支 commit `ae36f540ee6097ab77c135d12d4c05c7520c315a` 已實作正式、
失敗即關閉的 watcher、A000 pre-write dirty-state 原子失效與 2×／3× presenter。固定
move／refuse／confirm 各自建立 control／2×／3× A／B，共 18 份 production 收據；摘要
SHA-256 為 `befbe1e11ffba4334dae1122da6e549b415f7d3b3583f3e374cd00007b6659a0`。

三條路徑的 control／2×／3× machine／memory、DOS、37,021 筆 file ops、輸入、完整事件、
indexed framebuffer、palette、transition 與 A000 aggregate 均相等；同條件 A／B 的完整
JSON、畫面與 RGBA 逐 byte 相同。2×／3× missing glyph 為零，差異只落在核准安全矩形，
安全矩形外與動態圖示區污染均為零；每個已量 transition 的 first-write 清除與 active
generation 生命週期均通過。正式 app／CLI 的 test、race、vet 及獨立收據審查亦通過。

收據 runner 與最終 commit 只差 `LoadBodyIconCatalog` 的「正式 catalog 必須恰為七列」
防禦 guard；收據已驗證輸入恰為七列且 SHA 固定，此分支對有效輸入不可達，獨立審查判定
無須重跑全量收據。

因此本規格只在固定 move／refuse／confirm、七個 exact identity 與已量 step 視窗標為
CONFORMED。不得由此宣稱儲存詢問離頁、實際存讀檔／restore、完整開機、其他輸入路徑或
未觀察 writer 已完成；擴充其中任一路徑必須重新走證據與規格閘門。

本檔是窄規格，不取代 `001` 的通用 renderer、`004` 的 host 前端或字型／倍率決策；它只
提供 body-icon adapter 可實作前必須滿足的 exact identity、幾何與生命週期條件。
