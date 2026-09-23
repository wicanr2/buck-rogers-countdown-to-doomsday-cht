# 009 — 身體圖示畫面文字輸出端覆繪

狀態：DRAFT（禁止據此接入 production runtime）  
範圍：角色建立流程的身體圖示選擇、圖示確認與儲存詢問文字  
更新：2026-09-22

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

## DRAFT 顯示與生命週期契約

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

## DRAFT→READY 證據審查閘門

目前已具備（2026-09-23 完整 A000 觀察證據；獨立審查拒絕升 READY）：

- 七筆文字 identity、來源清冊、繁中 catalog 與七筆安全矩形已由獨立驗證器鎖定。
- Phase 48／49 已證實移動、拒絕、確認、儲存詢問的正常玩家 trace 與逐 byte 重播。
- 原版 `READY ACTION` 語意由 Phase 48 原版畫面證據核對，不以 hash 單獨猜測。
- 可丟棄 projection 已用 Phase 48 六份 A/B 收據精確重生 1／6／2 筆 request；但它不是
  runtime watcher，因現有 `MenuRequestWatcher` 不觀測 `1C41` 低階 glyph calls。
- 七筆低階 glyph 已逐筆證實 verified RETF、同 SS／SP+`0x12` 與逐 glyph 低位／高位 ABI
  契約。正常 move／refuse／confirm 固定排程已由 `Machine.Write8` 前的通用 A000 observer
  完整觀察，包含同值寫入；三組 A／B 逐 byte 相同，並訂正 confirmation／save prompt
  的 earliest pre-write 是 glyph store，而非稍後的 F3AA fill。可丟棄 typed-core 及
  2×／3×正式倚天 containment 已通過；正例只用暫存 READY fixture，正式 catalog 仍為
  DRAFT。

獨立審查確認仍需完成，未達 READY：

- 正式 watcher／dirty-state 路徑必須在任何 A000 writer 首次相交安全矩形前，依已證實
  identity 失敗即關閉地介入；並以提早寫入、未知 writer、錯 generation／key 與部分群組
  等反例證明不會留下半套 stamp。目前完整 observer 只證明固定合法排程的原版 first，
  尚未證明正式攔截路徑能安全處理該 first。
- move／refuse／confirm 的真實 receipt event 時序必須直接餵入 watcher，垂直驗證
  event→合法 group／transition→generation；現有 group 測試仍是人工序列，不足以替代。
- 完整 observer 證據只涵蓋三條固定排程；儲存詢問離開功能選單尚未量，不得納入 READY
  範圍。

完成證據審查後才可把本檔升為 READY、實作正式 runtime presenter。實作後另建立
正式、失敗即關閉的 `1C41` glyph watcher API，提供 catalog miss／drop／pending 收據；
不得直接把可丟棄 projection／typed-core 併入正式玩家路徑。並建立同狀態 2×／3×
A/B 收據：原版 bytes／輸入／檔案事件不變、七個矩形內可見差異、
矩形外零差異、圖示像素與動態欄零污染、所有轉場零殘字；通過後才能標為
CONFORMED。在此之前不得於 README 宣稱身體圖示畫面已中文化。

本檔是窄規格，不取代 `001` 的通用 renderer、`004` 的 host 前端或字型／倍率決策；它只
提供 body-icon adapter 可實作前必須滿足的 exact identity、幾何與生命週期條件。
