# 021 — 加入角色後真正 Exit 確認問句本體覆繪

狀態：**限縮 CONFORMED（固定合法加入角色存態的 N／Y→Y、兩句問句本體及已量生命週期）；其他原版路徑與 Linux 玩家視窗未驗。**
日期：2026-09-24

[第二百一十五階段](../re/phase-215-exit-prompt-body-ready-review.md)已完成獨立
READY 前審查；本文較早的「候選」「待審查」措辭保存設計歷程，
以本段與審查文件的限縮核准範圍為準。
[第二百一十七階段](../re/phase-217-exit-prompt-full-body-writer-review.md)
以可重生探針及固定合法 Y→Y 雙重原版收據，對 q1／q2 pending 的完整本體八列
補充 writer 證據；它修訂下文第 6 點的已量 writer 範圍，不提高其他路徑或
正式 A/B 的完成狀態。舊首列型程式的 q1／N 暫時綠燈已撤回。
[第二百一十八階段](../re/phase-218-exit-prompt-runtime-ab.md)其後以正式
watcher／presenter 在固定合法存態完成 N 與 Y→Y 的 control／2×／3×
雙重同狀態 A/B、FileOps 零筆自證與正式生命週期軌跡；主代理及獨立
審查均已核對。此後的**現行結論**只在上述固定路徑及本體範圍升為
限縮 CONFORMED；下文較早的「待審查」「尚未實作」保留階段歷程，
不得覆蓋本段。

## 範圍、來源與證據等級

本規格只針對合法加入角色後的功能選單，選取真正 row 21 `Exit to DOS`、按 Enter
後出現的兩句 row 24 黃色確認問句。原版先照常繪製；候選繁中層只可在 RGBA
輸出端清除並覆繪**問句本體**。不改原版 EXE／OVR、DOS 記憶體、indexed
framebuffer、BIOS 鍵盤、Y／N 判定、檔案、存檔或退出流程。row 21 選單項及
[規格 018](018-post-join-menu-overlay-draft.md)的七列正式範圍不是本規格的覆繪目標；
row 12 Enter 舊清除也不是 Exit 清除。

原版 `START.EXE` SHA-256：
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；
`GAME.OVR` SHA-256：
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
合法 `a-joined.state` SHA-256：
`1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。
[第一百八十三階段](../re/phase-183-post-join-exit-identity-corrigendum.md)訂正 row 12／21
身分；[第一百八十八階段](../re/phase-188-exit-prompts-draft-evidence.md)以 dosgolem
fork `cb3ca77c66e4909c5f513b807840e885ab5cb4a3`、Docker
`golang:1.25.0-bookworm`／Go 1.25.0、固定合法存態，雙重重播 N 與 Y→Y。
原版完整收據留在 ignored `workplace/`，本規格不收錄可還原原文或字模。
`37F1:…`、`0763:…` 為 dosgolem 8086 實模式 `segment:offset`；
`GAME.OVR` offset 為檔案位置；A000 數字為線性視訊位址，不可混用。

| 問句 | 已證實 exact 輸出身分 | guarded entry → return（原版 step） | 本體安全矩形（320×200 logical，半開） | 保護的原版六格尾碼 |
| --- | --- | --- | --- | --- |
| q1 | `GAME.OVR@0x17B0D`；12 bytes；SHA-256 `c38a515358859a10e7a2104cab69fe10ee2d492d94024b7d8f17d69b1a409032` | `124811496 → 124820881` | `[0,96)×[192,200)` | `[96,144)×[192,200)`，column 12–17 |
| q2 | `GAME.OVR@0x17B1A`；30 bytes；SHA-256 `35023ac3208312fb1c932ec15a737aae88817925d6cabb26d83281bf755bdcb8` | `124906582 → 124929724`，只見於 Y→Y | `[0,240)×[192,200)` | `[240,288)×[192,200)`，column 30–35 |

兩筆皆由 `37F1:101E` 輸出於 row 24／column 0，`bg/fg=0/14`；即黃色本體，
不是[規格 020](020-skill-exit-confirmation-overlay-draft.md)技能頁的 `0/13`。
六格尾碼由 `0763:026B` 的 dispatcher 外 glyph path 繪製，具有隨輸入改變的
多色及反白分段。其存在、邊界與初態三段色彩已證實；逐格生命週期未全部解出。
本規格候選選擇**完全保留原版尾碼**：它不是 TSV 譯文、清除矩形或中文 layer，
不得固定重畫為白色，也不得推定尾碼顏色不變。每次 Draw 必須以保護區 sentinel
檢查尾碼 RGBA 零覆繪；尾碼外的畫面亦不得受中文層影響。

「真正 row 21 Enter 後出現」是上述原版收據的**已證實來源路徑**，不是
watcher 必須另行取得的 Enter 上下文 guard。`GAME.OVR` 同長度 byte window
掃描僅在上述檔案 offset 找到 q1 原文；已量 N／Y→Y 路徑也只見該 exact
顯示身分。其他未量玩家路徑絕不重用仍只是**強推論**，不得稱全域已證實。
即使另一合法路徑重用完全相同的原文、caller、座標與樣式，本限縮覆繪
只更換該顯示事件的本體，不改尾碼、輸入或判定；無須把未具備正式事件源的
row 21 Enter 另設為啟用前置。

[第二百一十三階段](../re/phase-213-exit-prompt-font-draft.md)提出 q1「離開至 DOS」、
q2「遊戲尚未儲存。仍要離開？」兩筆**DRAFT 顯示候選**。q1 與選單項譯詞相近
不表示可共用 key、identity、owner 或生命週期。第二百一十五階段已限縮
核准這兩句**顯示譯文**；正式 TSV 的獨立 key 仍待實作，譯文不得進入
原版語意路徑。任何改譯均須重新驗字型、矩形與尾碼邊界。

## 候選 watcher 與失效狀態機

這是依已量事件提出的**待審查實作契約**，不是原版已實作證據：

1. q1、q2 各自逐欄比對原文 byte 長度與 SHA-256、`37F1:101E` caller、
   row／column、`0/14` style，以及對應 generation。q1 不另要求
   row 21 Enter 事件作啟用 guard；q2 必須由同一 owner 先前已接受的
   q1 exact 事件與既定時序授權。字串相同、只有座標相同、partial 身分、
   混用技能頁 identity、錯序或重複 Entry 均不得啟用層。
2. 每筆 exact Entry 僅建立 pending；待**同一筆 guarded far-return** 及 generation
   檢查通過才建立本體 active。不可在 Entry 或初畫 A000 store 時提前顯示；
   初畫 first store 的完整時序未獲正式 watcher 驗證。q1、q2 與 row 21
   各有獨立 generation／layer，由同一 session 的生命週期 owner 協調；
   不得用單一互斥 token 代表三者。
3. 已啟用本體與原版 A000 任一**最早相交 pre-write** 同步失效，VGA 寫入前
   清空 watcher 與 presenter 對應層；同值 old→new 也算。q1 的 Y→Y 首筆為
   step `124906844`、`0763:184D`、線性 A000 `716800`、像素 `(0,192)`、
   `0→0`；N 首筆為 step `125251139`，同 caller／位置及 `0→0`。
   N 的全選單 clear `124905849` 不相交 q1，不能用它提早清問句。
4. N 返回時 row 21 於 `125241454 → 125250067` 已重新反白，而 q1 首筆
   本體 pre-write 要到 `125251139`；兩層可短暫共存，各自只按本身的
   exact 事件與相交範圍失效。Y→Y 的 q2 Entry 是 `124906582`，**早於**
   q1 首筆本體 pre-write `124906844`；因此 q2 pending 必須可與 q1 active
   短暫共存。該筆 pre-write 只清 q1，不得清掉 q2 pending；q2 的
   `124929724` guarded Return 只有在 q1 已失效後才可啟用 q2。把三者
   壓成單一互斥狀態，或先清 q1 才允許 q2 Entry，都與原版時序不符。
5. q2 在已量 Y→Y 分支直到 DOS `Exited=true`、step `125006324` 前**沒有**
   自然本體相交寫入；DOS Stop 須清掉所有 pending／active 層並把同一 owner
   轉為 terminal `Closed`，不得重啟。這不是虛構一筆 q2 A000 clear。
   第一百八十三階段舊 `125006330` 已由
   [第一百八十七階段](../re/phase-187-exit-stop-six-step-corrigendum.md)訂正；
   不可將舊值作可重生退出點。
6. `Restore` 清掉所有 pending／active 與 presenter，只有較大 generation
   的全新 exact Entry→guarded Return 可重建；`Discontinuity`、`Fault`、
   錯序／未知 identity、無法正規化的 VideoWrite 及待處理或作用中本體的
   未知 writer 均清層並轉 terminal `Failed`／poison，同一 owner 不得 rearm。
   固定合法 Y→Y 路徑的兩筆 exact 問句，在各自 pending Entry 至同世代
   guarded Return 前，對完整本體八列只量到 `0763:184D` 與
   `0763:1854` 兩個正常初畫 writer；各自 768／1,920 個本體像素均被
   收據覆蓋。這不是全域白名單：只有已辨識 pending、對應本體、對應
   generation 與時窗可接受這兩個 writer；其他相交 writer 仍失敗即關閉。
   q2 pending 與 q1 active 共存時，已量 q2 初畫寫入同時可以先清 q1，
   不能因此清除 q2 pending。未量其他路徑或新 writer 應回到證據審查，
   不以靜默白名單猜補。

VideoWrite 的 `Offset` 若為 A000 **段內** offset，先拒絕不在 `[0,0x10000)`
的值，再計算線性 `0xA0000 + Offset` 並以半開本體矩形判相交；線性值須落
`[0xA0000,0xB0000)`。不得直接把段內 offset 當成線性位址。
所有 Stop／Restore／Discontinuity／Fault 在 pending 階段也須清空，不能遺留
可在下次 Return 復活的舊 request。原版 q1、q2 的 entry／return 與 pre-write
時序為**已證實**；上述 owner、故障態與 guarded hook 的正式接線仍是**候選**。
[第二百一十四階段](../re/phase-214-exit-prompt-body-lifecycle-fake-draft.md)的
typed fake 必須涵蓋上述 q2 pending／q1 active 重疊與實際事件先後；
初版先清 q1 再送 q2 Entry 的綠燈已經訂正，不得作 READY 證據。
修正後七組測試通過，仍只證候選狀態機內部自洽，
不證原版 A/B 或正式事件來源。

## 字型、呈現與驗收門檻

譯文單行、固定 8-pixel logical 高度；超過本體安全矩形、缺字、零墨跡、
不合法控制碼或空譯文均拒絕，不能截斷、換行、縮字或伸入尾碼。
目前本機倚天 `GOLEMFNT` SHA-256
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
第二百一十三階段的**靜態**收據顯示兩句候選在 2×（16×16 ink）與
3×（24×24 cell 中的 22×22 CJK ink，偏移 `(1,1)`）皆零缺字、零本體
越界，尾碼遮罩零相交；正式 raster 仍須重驗。

| 倍率 | q1／q2 本體安全矩形 | q1／q2 尾碼保護矩形 |
| --- | --- | --- |
| 2× | `[0,192)×[384,400)`／`[0,480)×[384,400)` | `[192,288)×[384,400)`／`[480,576)×[384,400)` |
| 3× | `[0,288)×[576,600)`／`[0,720)×[576,600)` | `[288,432)×[576,600)`／`[720,864)×[576,600)` |

獨立 READY 審查已核對原版兩筆 exact identity、正常 N／Y→Y 的
entry→return、含同值首筆 pre-write、本體／尾碼分界、候選譯文、字型與
typed 負例，明列未量 writer 及 Restore／Stop 事件來源的接線界限。
只有上述已核准的限縮範圍才可新增正式 TSV、watcher 與 presenter。
正式 watcher 對本體相交須檢查八列，不能只檢查 y=`192` 首列；
第二百一十七階段的 writer 補充仍須接受正式同狀態 A/B 檢驗。
實作後以同一合法初始存態、同一輸入／受控亂數條件，重生 control／2×／3×
的 q1 active、N 返回選單、Y→Y q2 active 與 DOS Stop；每條至少雙重可重播。
逐點比對原版 machine／DOS 狀態、BIOS／FileOps、indexed framebuffer 與
palette；active RGBA 差異只准在當前問句本體，六格尾碼與矩形外零差。
檢查含同值 A000 首寫的同一步清層、q1／row21 短暫共存、q2 Stop
後零層且不能 rearm，以及 Restore／Discontinuity／Fault／未知 writer／
錯序／partial／越界的正式失敗即關閉矩陣。N、Y→Y 終態須無殘字；
若有存讀檔或 Linux 玩家路徑聲明，還要另外取得各自正常路徑收據。

目前正式 Exit watcher、presenter、TSV 與文字收據 CLI 已實作，
第二百一十八階段在一個合法加入角色存態完成 N／Y→Y 的雙倍率
同狀態與同一步清層／交疊軌跡，故僅此範圍**限縮 CONFORMED**。
Restore／Discontinuity／Fault 的正式 runtime 事件來源、其他初始狀態、
異境 exact 字串重用、遊戲內存讀檔及 Linux 玩家視窗未驗，不能外推
完整遊戲已中文化或可玩。原版遊戲、存態、字型與完整收據僅供本機研究，
不得放入 Git 或公開包。
