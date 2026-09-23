# 020 — 技能頁離開確認提示的繁中輸出端覆繪

狀態：**DRAFT；尚未授權 watcher／presenter 正式接線。**
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

## DRAFT 的候選輸出契約

1. exact event 必須同時比對原文長度、SHA-256、caller、row／column、
   背景／前景與頁面上下文；只用相同文字或座標不得啟用覆繪。
2. 只清除本體安全矩形；六格選擇尾碼完整保留原版的顏色與反白。
   不把尾碼併入譯文 TSV，亦不預設其顏色固定。使用者對中文
   快捷字母的白色規則不等於授權更改這個多色尾碼。
3. 兩句譯文單行顯示；現行候選字型的 2×／3× 靜態檢查已通過，
   正式實作仍須重驗墨跡完全落於本體安全矩形且不覆蓋尾碼。
   不得為遷就缺字改譯。
4. watcher 須在原版對本體最早相交 A000 pre-write 前失效，包含
   同值寫入；N／Y 返回或離頁後不得殘字。未知 writer、錯序、
   partial 身分、restore／stop／discontinuity 必須失敗即關閉。

以上第 3、4 項的精確失效點與驗收矩陣仍未達 READY，不能將此候選
直接搬進正式程式。

## READY 前置與實作後驗收

兩頁問句本體與尾碼在相同合法原版 state、相同 N／Y 排程下的最早
**含同值** A000 相交寫入已量到；仍須確認初畫及必要重畫邊界、
尾碼每格重畫／清除與 DOS 終止清理。現行倚天字型對兩筆 TSV 的 2×／3× 靜態
containment、鍵值與字型 coverage 已通過；仍須獨立審查 typed watcher／presenter
的 generation、失敗矩陣與保存狀態影響；合格才可升 READY。

實作後分別由 dosgolem 從相同初態重生 control／2×／3× 的
Escape→N、Escape→Y；檢查原版 memory、indexed、palette、BIOS、
FileOps 與存檔語意不因繁中覆繪改變，差異只在核准本體像素，
返回／離頁無殘字。這些是後續 CONFORMED 條件，不能用目前的
DRAFT glyph 或終態控制組替代。
