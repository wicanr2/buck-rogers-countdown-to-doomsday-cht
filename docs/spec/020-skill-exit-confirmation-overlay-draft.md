# 020 — 技能頁離開確認提示的繁中輸出端覆繪

狀態：**限縮 READY（僅職業／技術兩句問句本體）；正式 watcher／presenter 與同狀態 A/B 尚未完成。**
日期：2026-09-24

## 玩家可見範圍與原版證據

本規格只處理角色建立流程中，職業技能頁與技術技能頁按 Escape、
尚有技能點未用時出現的確認問句。原版先照常繪製；dosgolem 僅在
RGBA 輸出端以 exact identity 清除問句本體、覆繪繁中。N／Y 的原版
判定、點數、後續畫面、BIOS 輸入、記憶體、indexed framebuffer、
檔案與存檔一律不改。

[第一百九十一階段](../re/phase-191-skill-exit-confirmation-translation-draft.md)
已用 `GAME.OVR` 原始 bytes 與正式事件表核對兩筆原文 SHA-256、
`37F1:101E`、row 24／column 0、`bg/fg=0/13`。
`GAME.OVR` SHA-256 是
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
職業問句檔案 offset `0x25A2B`、33 bytes；技術問句 offset `0x25A4D`、
34 bytes。檔案 offset **不是** dosgolem 實模式 callsite 位址。

[第一百九十七階段](../re/phase-197-skill-exit-confirmation-prewrite-draft.md)
從合法本機 state 量到兩問句各自的首次**變值** A000 相交寫入及
dispatcher 外六格原版選擇尾碼。原版與存態、glyph／A000 私有收據均
只留 ignored `workplace/`；工具版本、各 state／收據雜湊與位址空間見該階段。

[第一百九十九階段](../re/phase-199-skill-exit-font-containment-draft.md)
另用現行本機倚天字型確認兩筆 DRAFT 譯文在 2×／3×上述矩形
零缺字、零靜態墨跡越界。這只補足幾何候選，不驗原版清除或
正式執行期。
[第一百九十八階段](../re/phase-198-skill-exit-ny-all-store-prewrite-draft.md)
又量到 N／Y 各兩條合法重播中，本體與尾碼的最早含同值相交
A000 store；三筆首寫會被舊變值 watcher 漏掉。這只證明首筆時序，
不證明整個尾碼重畫、DOS 停止或正式 layer 清除。

| 頁面 | 問句 exact key | 本體安全矩形（logical、半開） | 原版尾碼保護矩形 |
| --- | --- | --- | --- |
| 職業 | `career.skill.exit.exit_confirmation_prompt.001` | `[0,264)×[192,200)` | `[264,312)×[192,200)` |
| 技術 | `technical.skill.exit.exit_confirmation_prompt.001` | `[0,272)×[192,200)` | `[272,320)×[192,200)` |

原句身分與初態尾碼幾何為**已證實**。兩筆繁中譯文目前是
`text/skill-exit-confirmation.zh-TW.tsv` 的**編輯性 DRAFT**；不得
讓譯文參與原版條件比較。N／Y 後問句應失效是由正常控制流與
終態畫面支持的**強推論**，尚無完整含同值 A000 清除證據。

## READY 輸出契約

1. exact event 必須同時比對原文長度、SHA-256、caller、row／column、
   背景／前景與頁面上下文；只用相同文字或座標不得啟用覆繪。
2. 只清除本體安全矩形；六格選擇尾碼完整保留原版的顏色與反白。
   不把尾碼併入譯文 TSV，亦不預設其顏色固定。使用者對中文
   快捷字母的白色規則不等於授權更改這個多色尾碼。
3. 兩句譯文單行顯示；現行候選字型的 2×／3× 靜態檢查已通過，
   正式實作仍須重驗墨跡完全落於本體安全矩形且不覆蓋尾碼。
   不得為遷就缺字改譯。
4. layer 只能在 exact dispatcher 已完成 guarded return 後建立；初畫的
   same-value first store 仍是未知，故不得以首次 A000 store 當成啟用條件。
   已啟用 layer 遇到原版對**本體**最早相交 A000 pre-write 必須先失效，
   包含同值寫入與任意 writer。N／Y 返回或離頁後不得殘字。Stop、Restore、
   Discontinuity、未知 writer、錯序、partial 身分與任何錯誤必須同步清除
   watcher 與 presenter，失敗即關閉。
5. lifecycle 僅觀察本體矩形；尾碼不是 watcher 的 identity 或清除條件。
   presenter 必須以尾碼 sentinel 證明每次 Draw 對尾碼保護矩形是零覆繪。
   尾碼逐格重畫／清除不屬本限縮 READY 的前置，亦不得由本契約假稱已知。
   本規格與 phase-197／198 的 `AF…` 位址均為**線性 A000**位址；正式接線若收到
   `machine.VideoWrite.Offset`，必須先拒絕不在 `[0,0x10000)` 的**段內 offset**，再
   正規化為 `0xA0000 + Offset`；正規化後的線性位址必在 `[0xA0000,0xB0000)`。
   不得把段內 `0xF0A8` 和線性 `0xAF0A8` 混比。

上述契約已由[第二百階段](../re/phase-200-skill-exit-body-only-lifecycle-fake-draft.md)
的 typed fake 與[第二百零一階段](../re/phase-201-skill-exit-body-only-ready-review.md)
的獨立審查限縮核准。它授權依此契約實作，不表示正式程式或原版 A/B 已驗。

## READY 證據與實作後驗收

兩頁問句的 exact dispatcher identity 與 entry→return 時序、兩頁 N／Y 本體最早
**含同值** A000 相交寫入與本體／尾碼分界已量到；guarded return 是依此時序
提出的 DRAFT watcher 機制，尚未被正式 hook 驗證。初畫的 same-value first store
仍未知，故 layer 必須在該 verified return 後才可啟用。technical Y 的本體首筆為
`103906680 AF0A8 0CF4:1B3A`，是 same-value；因此清層不得只接受
`0763:184D` 或變值寫入。尾碼逐格重畫／清除不要求作為 body-only READY
前置，但每次 presenter draw 必須以 sentinel 證明尾碼零覆繪。

現行倚天字型對兩筆 TSV 的 2×／3×靜態 containment、鍵值與字型 coverage
已通過；typed Entry／pending／Return、四條 N／Y 任意 writer 本體 pre-write、
Stop／Restore／Discontinuity／錯誤清層、段內 offset 正規化及雙倍率尾碼
sentinel 的 DRAFT fake 與獨立審查亦已通過。READY 只限兩句本體；正式
guarded-return hook、session bridge、raster 與同狀態 A/B 仍待實作及驗收。

依規格 019 的同一 session `Closed`／`Failed` 不得被新輸入復活契約，DOS Stop 在
本候選中必須同步清層並轉為 terminal `Closed`；同一 owner 不得以新 Entry／generation
rearm，新的合法 session 必須由新 owner 建立。Restore 只清空當前層，後續仍必須以
大於舊值的 generation 重走完整 exact Entry／Return；正式 restore hook 的來源與接線
仍是 DRAFT，不能由 fake 冒稱已驗。

Discontinuity 與 A000 範圍外／無法正規化的 VideoWrite 都是不可信事件；本候選要求
同步 clear 後轉為 terminal `Failed`／poison，同一 owner 不得 rearm。Stop、Restore、
Discontinuity、Fault 不只在 active layer，也必須在 pending Entry→Return 期間清除
pending 與 presenter；Restore 是唯一仍可由較大 generation 的完整 exact Entry／Return
重新建立 layer 的非 terminal bridge。

實作後分別由 dosgolem 從相同初態重生 control／2×／3× 的
Escape→N、Escape→Y；檢查原版 memory、indexed、palette、BIOS、
FileOps 與存檔語意不因繁中覆繪改變，差異只在核准本體像素，
返回／離頁無殘字。這些是後續 CONFORMED 條件，不能用目前的
DRAFT glyph 或終態控制組替代。
