# 023 — row 15／row 24 命令與狀態列輸出端

狀態：**DRAFT；不授權新增翻譯 TSV 或正式 watcher／presenter**
日期：2026-09-24

原版欄位與寫入證據見[第二百二十一階段](../re/phase-221-command-status-columns-draft.md)；
較早同路徑的停止線見[第一百一十](../re/phase-110-command-status-inventory.md)、
[第一百一十二](../re/phase-112-command-turn-manual-evidence.md)與
[第一百三十六階段](../re/phase-136-story-page10-enter-stop-line.md)。

## 玩家可見範圍與非範圍

候選只涵蓋已量玩家路徑上兩種命令／狀態輸出：第九頁後 row 15 col 17
的 12 格反覆重畫，以及手冊返回後 row 24 col 0 的 21 格 dispatcher／
33 格直接 glyph 路徑。它們不是第十頁故事，不處理右側姓名／數值、
row 17 劇情、手冊答案、原版輸入、規則、VRAM、存檔或完整 Linux 前端。
目前**沒有**核准繁中詞、文字 key、清除矩形或 renderer 幾何。

原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
兩份合法 state、dosgolem fork／Go 版本與 ignored probe SHA 均列於
第二百二十一階段。文中位址是 dosgolem 執行期實模式 `segment:offset`；
A000 offset 是 320×200 Mode 13h byte 位移，不與 IDA 位址混用。

## 證據分級

| 主張 | 等級 |
| --- | --- |
| row 15 六筆 `1FEB:2AF5 → 0763:0424`，各 12 格；同一存態中第 0 格變動，1–11 格 bytewise 相同 | **已證實，僅限該重播與時窗**；整串 SHA／欄位遮罩見第二百二十一階段。變動原因與穩定後綴的跨狀態語意未知。 |
| row 15 每次先呼叫 `026F:029C` 清 row 15 col 17..38，再有本體 A000 pre-write／dispatcher／glyph | **已證實，僅限六次重畫**；清除參數與首寫／writer 計數見第二百二十一階段。不能據此核准未來覆繪 22 格。 |
| row 24 Enter 的 21 格與 4／6 的 33 格分屬 `0763:1307 → 0763:0424` 及 `37F1:0337 → 0763:026B` | **已證實，僅限各固定路徑**；不可共用一個 identity 或把 33 格當 21 格延長。 |
| row 24 4／6 的 33 格兩次相同、逐格 A000 寫入；所見 `026F:029C` 只清 col 33..39 | **已證實，僅限這一對輸入**；它不是 0..32 文字本體的清層證據。 |
| row 15 的 1–11 格或 row 24 的任一欄是可翻譯固定詞 | **未知**；沒有不同遊戲狀態下的原文詞界與語意對照。 |
| 任何自然離頁、輸入或 row 24 右側 clear 足以使未來繁中層無殘字 | **未知**；沒有完整失效／安全矩形收據。 |

## 只供後續審查的 typed 候選

若取得可比的第二種合法狀態，應先將每條路徑分離為
`{caller,row,column,length,full-original-SHA,verified-return,style}`
的**整串 identity**，以及經跨狀態證實的固定欄範圍與動態欄範圍。
固定欄才可另設譯文 key；動態欄仍由原版顯示，不把譯文回寫原版記憶體、
比較、檔案或存檔。`row15`／`row24 dispatcher`／`row24 direct glyph`
必須是不同候選，不以相同畫面列號合併。這是待量測的資料模型，
**不是 READY loader 或實作規則**。

## 升 READY 前不可跳過的缺口

1. 從已證實玩家輸入取得至少一個**不同命令／狀態**但可比的合法
   初態，私下逐格比對原文與 state；標出固定詞、變動欄、詞界及
   其來源。單一 state 的六次時間重畫或 4／6 兩個相同輸出均不足。
2. 各路徑量到完整 entry→guarded return、原版文字本體的最早相交
   pre-write、清除與重畫先後、Stop／Restore／離頁；row 24 右側
   col 33..39 清除不能替代 0..32 本體失效。
3. 對每個**真正固定**欄定義不侵入動態資料的文字安全矩形、譯文
   容量與 2×／3× 字型實墨跡；建立 content-safe exact identity
   catalog、唯一 key／字型 coverage／負例及原文／繁中同狀態驗收。
4. 獨立審查 RE→DRAFT 後才可升 READY；在此之前 production 必須
   對 row 15／24 維持原版顯示與 miss，不做 fallback 猜譯。

停止線：不延長第九頁自然離頁時鐘、不把 row 15 雜湊變化猜成某
一數值語意、不從 row 24 相同 glyph 推出固定詞，也不把原版或
已購字型、私有存態／畫面加入 Git、GitHub 或公開封包。

## 2026-09-24 跨進度證據審查追加

[第二百二十一階段追加收據](../re/phase-221-command-status-columns-draft.md#2026-09-24-跨進度合法初態比對勘誤)
已用手冊成功返回與第九頁後兩個**既有合法玩家進度**雙重播：row 15
仍是同 caller／row／col，但 11／12 格身分、某些位置的 byte 確實改變；
各次 `026F:029C` 本體相交 clear 與其後 `0CF4:1B3A` 首寫也可重播。
這推翻「完全沒有第二個可比進度」的舊前提，**沒有**推翻 DRAFT：
比對結果是數字／空白／其他非 ASCII 英文字母 byte 的欄位形狀，
不變 byte 沒有已證實的固定英文詞界或來源。進度變化也不等於
已證實的命令選項、數值欄來源變化。row 24 在已查的既有收據中
仍只有各自同一個 21 格／33 格身分，沒有第二個可比的不同值。

故本輪**沒有 READY 候選或內容安全的正式譯文輸入清單**。
下一個最小解鎖證據是正常玩家流程中的已證實命令／狀態變更，
伴隨相同 caller／row／col 的不同原文；再以私有畫面與來源讀寫端
辨識詞界／動態欄，量完整返回與覆繪失效邊界。不得僅因 byte
相同就建立 catalog key，也不得把此 probe 接成 production。
