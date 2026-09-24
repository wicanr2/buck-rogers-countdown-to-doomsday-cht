# 022 — 第九頁固定單行劇情輸出端覆繪

狀態：**限縮 CONFORMED（合法 page8→page9 固定單行入頁，及 Ctrl+C 退出 DOS 時的 Stop 清層）；遊戲內自然離頁仍未知。**
日期：2026-09-24

[第二百一十九階段正式入頁 A/B](../re/phase-219-story-page9-runtime-entry-ab.md)
已把 watcher／presenter 接到 dosgolem，固定合法 state 的 control／2×／3×
machine、DOS、indexed 同狀態，RGBA 差異只在核准單行矩形；
續以同一合法起點重播 Ctrl+C 退出 DOS，正式 owner 在同次執行中由
active 1 層清至 0 層，終態雙倍率 RGBA 與各自 baseline 一致；詳見
[第二百一十九階段的追加收據](../re/phase-219-story-page9-runtime-entry-ab.md#2026-09-24-ctrlc-退出-dos-的正式-stop-收據)。
因此僅此已量入頁及 Stop 路徑升為限縮 CONFORMED；遊戲內自然離頁、
Restore 後重入與完整玩家視窗並未因此通過。

[第一百三十四階段獨立審查](../re/phase-134-story-page9-enter-trace.md#2026-09-24-獨立證據審查固定單行入頁本體)
已核准本單行入頁本體進入正式實作；下文較早的「候選」「待審查」
字樣保存形成歷程，以本段限縮 READY 範圍為準。自然離頁、完整生命週期、
正常玩家路徑、存讀檔及整頁 CONFORMED 均未核准。

## 範圍與證據等級

本候選只處理合法第八頁 Enter 後，第九頁 row 17、column 1 的固定 20 字原文單行。
原版先照常繪製；繁中只在 dosgolem 的 RGBA 輸出層清除該行原文墨跡並覆繪。
原版 `GAME.OVR`、CPU／DOS 記憶體、A000 indexed framebuffer、鍵盤、規則、檔案與
存檔均不得改動。右側姓名／數值、row 15／24 command/status、第十頁、完整開機與
實際存讀檔不在範圍內。

原版 `GAME.OVR` SHA-256：
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
起點是合法 page8 終態 `page8-a.state`，檔案 SHA-256
`327dc1cb8baf4bee71cdcd0173538af123c47266c8bbf556b28f38d89355b0a9`。
原版位址均是 dosgolem 實模式 `segment:offset`；A000 offset 是 Mode 13h
320×200 視訊 byte offset，不是 IDA 線性位址。主要證據及 runner／Go 版本、
輸入排程、雙重收據與 SHA 見[第一百三十四階段](../re/phase-134-story-page9-enter-trace.md)。
第八頁的上游生命週期見[規格 017](017-story-page8-overlay-ready.md)，首屏顯示
隔離與字型幾何先例見[規格 010](010-story-opening-overlay-draft.md)。

| 主張 | 等級與根據 |
| --- | --- |
| 合法 Enter 於 step `351000000` 從第八頁到達此單行；雙重入頁重播 indexed 與 JSON 一致 | 已證實；第一百三十四階段的 `entry-a/b` 私有收據 |
| `0763:04FF → 0763:026B` 的 row 17／column 1，`mode/repeat=1/1`、`bg/fg=0/10`，連續 20 glyph | 已證實；`text/story-page9-events.tsv` 與雙重 glyph trace |
| 20 筆均從 `0763:03D6` 的 `0xCA` 返回；同 SS、相對 `SP+0x12`，七個 ABI high-word mask 皆零 | 已證實；第一百三十四階段的兩份 entry return-edge 收據 |
| 原版入頁單行的安全矩形是 `[8,168)×[136,144)` | 由已證實的 col 1、row 17、20×8×8 text cells 推得；正式 renderer／現用字型的合成 2×／3× 實字墨跡 containment 已驗，原版同狀態 A/B 待驗 |
| Enter、數字鍵盤 4／6，以及 8 的已量短窗未改寫故事矩形 | 已證實，**僅限各收據停止點**；row 15／24 重畫不是離頁事件 |
| 入頁 20 個 glyph frame 內共有 1,280 筆相交 A000 pre-write，各 frame 64 筆；writer 為 `0763:184D`／`0763:1854` | 已證實；合法 page8 state 的有界逐 byte probe，細節見下節；這些是**建構原文**，不能清 pending |
| Ctrl+C 退出 DOS 時，本行原版畫面不先相交改寫，正式 owner 由 active 1 經 Stop 清為 0 | 已證實；第二百一十九階段追加的同次執行、雙倍率 A/B；不推及遊戲內自然離頁 |
| 其他離頁必定由某一 A000 相交寫入、Stop 或 Restore 清層 | 未知；不以本收據聲稱全部出口安全 |

文字事件唯一身分為 `story.page9.line.001`、原文長度 `20`、SHA-256
`39a751ca9f384a77491b1e4399c0a72afb8b1ef146a77db2623394590ff1ca78`、
首筆 entry step `351155910`、末筆 post-call step `351988536`。步數是這份原版
收據的錨點及 catalog 固定版核對值，不可當作未來每次顯示的硬編碼時鐘。
正式 watcher 必須以逐字 bytes 的 SHA、連續座標、caller、guard、style、
實際 guarded return 與同一執行 epoch 來辨識；不能只憑 step、位置或譯文。

## 單行 typed 候選與失敗即關閉

`text/story-page9-events.tsv` 的單筆身分已依獨立審查標為 READY；
`text/story-page9.zh-TW.tsv` 的單筆譯文不另設 status 欄。正式 loader 只能
接受這一筆 READY identity 與精確譯文 key。現行譯文
「你們列隊離開。」是 `runtime-editorial`，不代表手冊逐字引文；任何改譯
都要重新跑字型與幾何驗證。

建議的 typed 輸入是固定版 `StoryPage9Identity`、20 筆 `GlyphEntry`／
`VerifiedReturn`、`machine.VideoWrite`、`Stop`／`Restore`；輸出僅為不含原文
bytes 的 `StoryPage9Event{key,generation,row,column,entryStep,postCallStep}` 和
RGBA stamp。狀態依序為 `idle → pending(1..20) → active`；只有第 20 筆
guarded return 通過 SHA 才原子提交一筆事件。partial、錯序、重複、錯
caller／guard／style／座標、ABI high word、返回 opcode／SS／SP／時間、
缺 key／譯文／字模、未知 epoch、非 READY catalog 或錯倍率，均清空
pending／active 並零 stamp。原文字節只在 watcher 的短暫 hash accumulator；
不得回寫至任何 DOS 語意路徑，也不得把它加入公開收據。

`machine.ObserveVideoWrites` 現有 API 在每一筆 A000 byte 送入 `VGA.Write`
**之前**回呼，包含同值寫入；`machine.VideoWrite.Offset` 是單 byte offset。
候選必須區分「原文正在建構」與「中文層已啟用」：

1. `pending` 期間，第 1–20 筆 exact glyph 的各自 Entry→guarded Return
   只容許當前 glyph frame 的 `0763:184D`／`0763:1854` A000 寫入，
   位置限該字格 `[column×8,(column+1)×8)×[136,144)`；每格 64 筆。
   寫入必須綁在同一 frame／generation。不同 writer、錯格、frame 外相交
   寫入或筆數不符，均失敗即關閉，清掉 pending，不可從後續字元續接。
   `pending` 尚無中文層，不能把這 1,280 筆正常原文寫入誤作「離頁」。
2. 第 20 筆 verified Return 完成後才原子啟用 RGBA 層。`active` 期間，
   **任何**相交 A000 byte pre-write，不論 caller、值是否改變，都須在
   原版 write 前清掉 watcher active／queued event 及 presenter 整行 stamp，
   遞增 generation。不能只認 `0CF4:1B3A` fill、可見像素變化或按鍵。
3. `Offset >= 64000` 等非法值要失敗即關閉。矩形外寫入不清層：
同列 x=7／168、相鄰 row 135／144、row 15／24 都是負例；x=8／167、
row 136／143 是正例。單 byte callback 不用把連續 fill 的 caller 或
`CX=304` 當成唯一合法 writer；已量第八頁→第九頁的 fill 可作入口前的
交叉核對，但不能冒稱第九頁已有實際離頁 pre-write。

上述 pending 例外由 ignored `workplace/dosgolem/apps/buckrogers/`
`story_page9_candidate_prewrite_test.go` 的一次性本機 probe 補證：
同一合法 page8 state、同一 step `351000000` Enter、固定跑到 `352100000`；
20 個 entry／return frame 各 64 筆相交寫入，frame 外 0、錯字格 0。
首筆 step `351156027`、末筆 `351988519`，writer `0763:184D` 為 1,028 筆、
`0763:1854` 為 252 筆。使用 `golang:1.26.7-bookworm`、Go 1.26.7、
無網路 Docker 及現有 `machine.ObserveVideoWrites`；原版、state、完整
receipt 不進版控。這個補證修正了初稿「任何相交寫入連 pending 也清」
會阻止 20/20 命中的錯誤；初稿結論不可作實作依據。

`Stop`、`Restore`、machine epoch 不連續、callback 訂閱中斷或不明狀態
均立即清 pending／active／event／RGBA layer；Restore 後只能重新完整命中
20 筆 exact entry 才可再顯示。這是安全的執行期規則候選，不是原版自然離頁
已被證實。不得用 Enter、4、6、8 的按鍵消費、row 15／24 clear 或
command/status glyph 當作 page9 exit；它們已量的短窗並未碰本行。

## 幾何、字型與驗收界線

邏輯畫面只覆繪 `[8,168)×[136,144)`，單行 20 cells；現有
`xlate.Stamp` 的 `CellW=8` 讓每個 rune 前進一個邏輯字格。TSV 將中文字元
保守計為兩格僅供容量 lint，不代表 renderer 的實際 advance；本行不換行、
截斷或溢出。2× 輸出矩形為
`[16,336)×[272,288)`；3× 為 `[24,504)×[408,432)`，沿用倚天
top-pad 16×16 字模及既有 3× 的 22×22 ink／24×24 cell 規則。
`tools/story_page9_catalog.py` 已收緊為 20 格的 READY catalog lint，且有
20／21 格失敗邊界測試；Unicode 寬度近似**不足以**證明實字墨跡安全。
本輪使用 ignored `workplace/current-font/buckrogers-eten-top-pad.golemfnt`
（SHA-256 `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`）
及正式 `xlate.Layer.Draw`／`manualThreeXFont`，以本機一次性
`story_page9_candidate_geometry_test.go` 畫該筆正式候選譯文。2× 的
RGBA 差異 4,663 pixels、矩形外 0，範圍 `[16,336)×[272,288)`；
3× 差異 10,649 pixels、矩形外 0，範圍 `[24,504)×[408,432)`；
兩倍率均零缺字，右側 x=168 邏輯邊界外為零差。此測試用合成
indexed／palette，證明字型與 renderer 的本體 containment，**不**是
原版畫面的同狀態 A/B。獨立審查已確認來源、唯一鍵、NFC、控制字元、
現用字型版本及本機測試可重生；任何譯文或字型更動都要重跑。

正式接線的測試須用**純 content-safe typed fake**檢驗上述狀態機：
假 20 bytes、相對時序與合成 SHA，不含原版 bytes／字型；
測試 19/20 不顯示、20/20 才啟用、每 frame 64 筆預期字格寫入、
pending 錯 writer／錯字格／frame 外寫入清空、錯返回／hash／ABI 清層、
active 後邊界相交與同值 pre-write、row 15／24 非相交、
Stop／Restore 後不可重現舊層。
fake 只能證明候選內部契約，不能當原版對拍或正式程式完成收據。

限縮入頁本體的獨立審查與接線已完成：從同一合法 page8 state 與
同一 Enter 排程重生 control／2×／3×；正規化 machine、DOS、indexed、
palette、鍵盤及 FileOps 相同，RGBA 差異只在核准矩形，兩倍率零缺字。
另須以原版實際後續相交寫入或 Stop／Restore 收據，證明清層後下一 frame
無殘字；目前**已有 Ctrl+C 退出 DOS 的 Stop 收據**，但沒有遊戲內自然離頁的
此種收據，故不得聲稱全部出口、正常玩家路徑或整個第九頁已中文化。
若一條實際離頁只改變非相交區域、
沒有 Stop／Restore，仍須回到 RE／DRAFT 補該出口的可觀測失效條件，
不能擴大按鍵掃描或以 row 24 重畫補洞。

原版遊戲、掃描手冊、原文全文、合法 state、完整收據／畫面、倚天來源
與衍生 GOLEMFNT 僅留在 ignored `workplace/`。版控只含 content-safe
metadata、譯文、規格與測試；公開缺原版時須明確跳過原版驗證。
