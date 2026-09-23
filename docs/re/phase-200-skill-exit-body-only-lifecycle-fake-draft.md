# 第二百階段：技能離開問句 body-only lifecycle fake

日期：2026-09-24
狀態：**DRAFT typed fake；不授權 production watcher／presenter、READY 或 CONFORMED。**

後續狀態：[第二百零一階段](phase-201-skill-exit-body-only-ready-review.md)
已在補齊 Entry caller CS／IP 負例並獨立審查後，將[規格 020](../spec/020-skill-exit-confirmation-overlay-draft.md)
的**兩句本體**限縮升 READY；本 fake 本身仍非正式實作或同狀態收據。

## 目的與證據邊界

本收據將規格 020 收斂成可審查的最小 body-only 候選。它引用第一百九十一階段已證實的
exact dispatcher identity 與 entry→return 時序、第一百九十七階段的本體／尾碼矩形、第一百九十八階段的
N／Y all-store pre-write，以及第一百九十九階段的字型 containment；它不載入原版、
字型、私有 state、原文或 framebuffer。

已證實：career／technical 的 N、Y 都有本體相交 all-store；technical Y 的首筆是
step `103906680`、`AF0A8`、`0CF4:1B3A`，且為 same-value。故 fake 的 `VideoStore`
只以 A000 本體位址判定，不讀 old/new value、不限制 writer CS:IP。初畫的
same-value first store 仍是未知。fake 提出的 guarded-return 是基於已證實 entry→return
時序的**候選機制**，尚非已接線的正式 watcher 行為；正式 layer 只能在該候選 guard
實際驗證後啟用。

## 可丟棄 typed model

ignored `workplace/phase200-skill-exit-body-only-lifecycle-fake/` 的 Go fake 有 typed
`Entry`／pending／`Return`：每筆含 SHA-256、length、caller、row、column、bg、fg、page
與 generation。只有 expected identity 的 Entry 與同 generation、全欄相同 Return 才 arm。
partial、重複、錯序、錯頁或錯 generation 會 poison 並同步清 watcher／presenter，之後
不可再 arm。這是由 phase191 entry→return 時序推導的候選 guard，非正式 hook 已證實行為。

`VideoWrite` fixture 固定 step、A000 位址、CS:IP、old/new。body pre-write 的清層只看
目前 generation 與本體相交位址，刻意不依賴 old/new 或 writer；因此 technical Y 的
`103906680 AF0A8 0CF4:1B3A old==new` 也會在 Draw 前清層。單一 `Lifecycle` owner
處理 Stop／Restore／Discontinuity／Fault：同 generation 同步 clear 兩者，舊 generation
只回錯、不清新層；VRAM 範圍外 offset 則失敗即關閉。收據中的 `AF…` 都是線性
`0xA0000+offset`；正式 `machine.VideoWrite.Offset` 接線必須先做此正規化並拒絕
`[0,0x10000)` 外的段內 offset，不能把 `F0A8` 與 `AF0A8` 直接比較。它不觀察尾碼
store，也不對尾碼寫入。

依 spec019 的 session `Closed`／`Failed` 不得復活，fake 現將同一 session 的 DOS Stop
鎖為 terminal Closed：Stop 後同 owner 的任何新 Entry／generation 都被拒絕，新 session
必須由新 owner 建立。Restore 只清層、不 Closed；它要求下一筆完整 exact Entry／Return
使用較大 generation。正式 restore hook 如何發出這個 bridge 事件仍是 DRAFT。

本輪 fake 將 lifecycle bridge 擴至 pending Entry→Return：Stop、Restore、Discontinuity、
Fault 都必須清 pending 與 presenter。Stop 轉 Closed；Discontinuity 及無法正規化／超出
A000 範圍的 VideoWrite 轉 terminal Failed／poison；Fault 同樣 poison。Restore 是唯一
clear-only 事件，可由較大 generation 的完整 exact Entry／Return 重建候選層。這是 typed
DRAFT contract，非正式 lifecycle owner 已接線的證明。

fake 固定下列測試：

1. partial SHA、錯誤 length／row／column／bg／fg／頁面／caller CS 或 IP、錯 generation、重複
   Entry 與錯序 Return 都不得 arm；
   identity error poison 後不得再 arm。
2. career N／Y、technical N 與 technical Y `AF0A8` 的完整 `VideoWrite` fixture 都在
   pre-write 清層；technical Y 的 writer 是 `0CF4:1B3A`、`old==new`，不可只接受
   `0763:184D` 或變值。
3. verified return 後 2×／3× RGBA 僅本體改變；career `[0,264)` 與 technical
   `[0,272)` 外的六格尾碼 sentinel 每次 Draw 都逐 RGBA byte 不變。
4. `machine.VideoWrite.Offset` normalizer 的正例 `F0A8→AF0A8` 與 `>=10000` 拒絕均
   有 typed test。尾碼 store 與另一頁本體區的 write 不得猜測清目前本體。Stop、Restore、
   Discontinuity、Fault 在 pending 與 active 同 generation 都同步清 watcher／presenter，且
   clear 後 Draw 必為零層；Stop Closed、Discontinuity／越界 write／Fault Failed，均不得
   rearm；Restore 後只有較大 generation 的完整 exact Entry／Return 可重建。

此 fake 只證明 DRAFT state machine 自洽，不能取代 dosgolem 同狀態 A/B 或宣稱原版
N／Y 全尾碼生命週期已量到。執行命令與結果記於 ignored README；測試不含原作素材。

## READY 候選仍須

READY 審查只須核對：phase191／197／198 的 identity、entry→return、linear A000 與
same-value pre-write 證據是否足以支撐本 typed contract；Entry／Return、normalizer、
pending／active lifecycle、terminal phase、2×／3× body-only tail sentinel 與完整失敗矩陣
是否由可重生 fake 固定；以及獨立審查是否接受其停止線。建立本 fake 當時仍待審查；
後續結論見第二百零一階段。READY 本身不要求 production hook、正式 raster 或 session
owner 已接線。

正式 session owner 的建構、Close 資源釋放及 restore hook 來源仍未接線；但同一 session
DOS Stop 的 terminal Closed 規則已由 spec019 約束。正式實作及 CONFORMED 驗收須核對
bridge 確實做到同一 owner 不復活，不能用 fake 通過代替 production 證據。

## CONFORMED 後驗收

待 READY 授權後，production implementation 必須把 typed watcher、normalizer、
single lifecycle owner 與 presenter 接線；其後才以相同合法 state 的 control／2×／3×
Escape→N、Escape→Y runtime A/B 驗證原版 machine、DOS 與未核准像素不變。它們是
implementation／CONFORMED 條件，不是本 body-only READY 候選的前置。
