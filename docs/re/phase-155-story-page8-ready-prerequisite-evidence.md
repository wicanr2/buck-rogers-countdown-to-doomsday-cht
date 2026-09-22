# 第一百五十五階段：第八頁逐字返回與離頁 pre-write 證據

日期：2026-09-23  
狀態：**三次獨立審查與幾何勘誤後，第八頁固定四行限縮升 READY；正式 runtime 未接。**

## 輸入、工具與權利

entry 從合法第七頁私有終態 `workplace/page7-next-trace/page7.state`
（SHA-256 `e869b67264539aff95ca5929a9858c74475feea47e0c7b3a505ea9cd0aa9a460`）
於 step `341000000` 送正常 BIOS Enter，至 `350000000`。exit 從合法
`workplace/page8-next-trace/page8-a.state`（SHA-256
`327dc1cb8baf4bee71cdcd0173538af123c47266c8bbf556b28f38d89355b0a9`）
於 step `351000000` 送 Enter，
至 `360000000`。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
位址均為 dosgolem 實模式 `segment:offset`，不是 IDA 線性位址。

使用本機 dosgolem HEAD `d42567de27da30b003584a777c63a5f91e8e39d6`、
Go 1.26.7，在無網路、有界 Docker 內建置 `cmd/buckrogers-text-receipt`；
runner SHA-256
`8d2b62cebaa38857b0a263c65103467746f853a268ca651febfeccf7af86fa7e`。
前一次嘗試碰上另一代理尚未提交的第七頁 CLI 中間態，缺少
`StoryPage7Watcher.Generation()` 而無法編譯，沒有有效收據；待完整
CLI 原子提交後以本段精確 HEAD 乾淨重跑，未將暫時的編譯失敗當成
第八頁產品缺陷。原版 state、完整事件與畫面只在 ignored `workplace/`，
不得進 Git／GitHub／公開封包。

## 雙重原版收據

`workplace/page8-ready-atomic-core/entry-{a,b}.json` 逐 byte 相同，
SHA-256 `64a8b4ce555562e4a57e3f0429ffc64d9a39e558f5eef667db9267cd54846779`。
第八頁 row 17–20 四行長度 `38/37/33/22`、共 130 glyph；130/130 筆
均為 `0763:03D6`、RETF opcode `0xCA`、返回 `0763:04FF`、同 SS
`1841`、`SP:3D66→3D78`（相對 `+0x12`）、七 ABI word 高位遮罩 0，
mode/repeat `1/1`、背景／前景 `0/10`，column 連續。原文 length／SHA
與 `text/story-page8-events.tsv` 一致；這是原版控制流證據，不是中文畫面。

`workplace/page8-ready-atomic-core/exit-{a,b}.json` 逐 byte 相同，
SHA-256 `366ce7212188c93ea3bc1ecc84bd548cf3bc874e008ada0f0952dba99b3f1164`。
對 row 17–20 候選區，合法 page8→page9 Enter 的最早相交
pre-execution fill 位於 step `351154334`、`0CF4:1B3A`、
`ES:DI=A000:AA08`、`CX=304`，即 row 136、x=8 起；早於
[第一百三十一階段](phase-131-story-page8-enter-trace.md)所記首筆
執行後可見像素寫入 step `351154358`。後者不能冒充最早 pre-write。

## READY 前剩餘停止線

低階翻譯代理另從私有原版畫面逐行校對四行原文與
`text/story-page8.zh-TW.tsv`；現有「接駁艇／太空站／基本裝備／解散」
語意忠實、繁體用字一致，沒有為口吻改譯的必要。這只屬編輯審查，
不改變 DRAFT 狀態。

ignored `workplace/page8-ready-atomic-core/font-containment-receipt.json`
SHA-256
`a16590c89c9441682a85b0e0e9ce868ba8a2b5b7f3b6c729c3d68e37e4aac9f6`
綁定現行 TSV SHA-256
`252f4efba5c00361afd33a3ec4ebf011e4de5afca753fe4fc2a83b4ab4d78144`
與 GOLEMFNT SHA-256
`b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`。
四行最多 11 個中文字格的最小靜態候選矩形為 logical
`[8,96)×[136,168)`；2× 16×16 ink/cell 有 2,266 墨跡像素，
3×正式 24×24 cell／22×22 ink／offset 1 有 4,269 墨跡像素，兩者
零缺字、零越界且遠離右側動態區。可重跑工具／測試 SHA-256 分別為
`3a78de04b745993325ba82199b58ab05f652aee76d8f000c4aa2ab54894e8473`、
`9cd8a37c92f1fa49900a3ff556d555dbd064c4dd7e1a2de4ffcd359695721f78`；
Docker unittest 通過且第二次收據逐 byte 相同。這仍是靜態候選，
不是 runtime 安全矩形授權。

仍須可丟棄 typed-core 驗證
四行原子、七 ABI 高／低位映射、RETF／stack／step、partial／錯序／
duplicate、未知／不相交／相交 write、restore／discontinuity 等失敗
即關閉邊界；正式 catalog 目前仍為 DRAFT。完成獨立審查後才可
考慮限縮升 READY；正式 runtime、control／2×／3×同狀態 A/B、
離頁無殘字、正常玩家路徑及存讀檔尚未驗，不能稱已中文化。

## 2026-09-23 可丟棄 typed-core

ignored `workplace/page8-ready-atomic-core/typed-core-receipt.json`
SHA-256
`f0282f1335c24ae00ebbf2bd13999e0d574eae9d4416137ad2df9afa6bb7d9da`
綁定現行 event TSV SHA-256
`69793743b80025bfcd965898548dd98a2dd0e689117c5f5c6b903c6a977a6d90`、
譯文與字型雜湊如上。可丟棄 `page8_core.py`／測試 SHA-256 分別為
`9afb17e6a3512bd84f1a3b5c21a1aeaa895de4d8a0b46589233a37eee04494f6`、
`d75873a4d6ce9b17298faa34c3787911f89eb8b85b0d2b09ba6c3c9cf57d0a85`；
Docker 四項測試通過，第二次收據逐 byte 相同。

正式 DRAFT catalog 被拒；只用暫存 READY fixture 驗四行 exact identity、
130 glyph return／SS／SP、七 ABI 高／低位、hash／caller／guard／style、
relative step、partial／mixed／duplicate、presenter 原子性、restore／
discontinuity，以及候選半開矩形的未知／錯 ES／不相交／跨界／實測
pre-write。這補足 READY 前可丟棄模型，但**尚待另一位代理獨立審查**；
正式 TSV 維持 DRAFT，本段不授權 production。

首次獨立 READY 審查指出這份 typed-core 的證據鏈仍斷一節：測試只將
四個人工整行 identity 各呼叫一次 `observe()`，而 receipt writer 把
`glyph_returns=130` 與 exit step 當常數寫入，沒有直接讀取雙重 entry／
exit JSON。因此「四項測試通過」不能證明 130/130 glyph／return edge
逐筆配對、聚合 hash、ABI／stack／step 及最早相交 pre-write 都是由
原始收據推導。修正版 verifier 必須直接解析四份 JSON、重算所有統計與
定位，並以 mutation 驗各類 drift；完成第二次獨立審查前維持 DRAFT。

原代理其後依審查修正：新 `typed-core-receipt.json` SHA-256
`e87602146fe4bc0937f4dc7d54083e4a3b226549766058388daef5bc6400dba8`，
`page8_core.py`／測試／writer SHA-256 分別為
`581048ccae960bd74da81e4444f2495e6a9d2d2cedcb8e5e4d18a3abfb4026df`、
`0f9ea6152df0c4cf0548d4308e54fa1cc6e5b1d7dedd63119b65f5371f19233f`、
`eceb84e5e1f2f460b135f1312e16b8a1800952cd07d4dd7ecefd916c4ad1d660`。
verifier 現直接讀 entry／exit A/B 與同重播 legacy glyph-run JSON，逐筆
配對 130 edge、聚合四行並自行導出 earliest pre-write；mutation 直接
改原始 receipt data。Docker 5 項測試通過，第二次 receipt 逐 byte 相同。

既有 edge schema 未在每筆 edge 明文輸出 glyph low byte；該字節序列由
同一重播的 content-safe glyph-run SHA 承諾，再與四行 length／SHA 對應。
若要逐 edge 明文 low byte，需另擴 runner 診斷 schema；本輪未修改
production。此限制是否仍阻止 READY，交由第二次獨立審查判定；目前
正式 catalog 仍是 DRAFT。

第二次獨立審查一度接受上述端到端 verifier，建議以
`[8,96)×[136,168)` 限縮升 READY；主代理在撰寫正式規格時發現這個
矩形只包住最長 11 個中文字格，**無法清除最長 38 個英文 glyph**。
原文由 column 1 起，若只蓋到 x=95，右側仍會留下英文殘字，違反
輸出端覆繪目的。故撤回 READY 升級動作，正式 TSV 繼續 DRAFT。
須依原文完整列寬與原版畫面證據重訂清除／覆繪安全矩形（候選為
rows 17–20 的 `[8,320)×[136,168)`，右界仍須重生驗證），再同步重算
2×／3× containment、逐列 pre-write 與 typed-core mutation；不能用
「中文字模未越界」替代「英文原文已完整清除」。

原代理隨後保留舊窄矩形收據並新增勘誤收據。四行原文最長 38 glyph，
從 column 1 的 x=8 起共 `38×8=304` pixels；exit A/B 在 32/32 個
安全 scanline 也各記錄 x=8、`CX=304` 的原版 fill。因此最小已量
完整原文清除／覆繪矩形訂正為 **`[8,312)×[136,168)`**，不再使用
x=96，也不無證據外推到 x=320。

`font-containment-corrigendum-receipt.json` SHA-256
`03b13f401ef7f8be989108f778abcf1e2a9a78dd38427cc7ab79512b7ba21cc8`；
2×矩形為 x=16、y=272、608×64，3×為 x=24、y=408、912×96，
沿用正式 16×16 與 24-cell／22-ink／offset1 幾何，分別 2,266／4,269
墨跡像素、零缺字、零越界。
`typed-core-corrigendum-receipt.json` SHA-256
`dc5b46e364f955910cac31f3f55c6b727cd43dd7a437e89560a24021264924c3`
亦改用新半開矩形，自 exit 收據導出 32 列完整 fill 與 step
`351154334` 的首筆相交 pre-write，補右界不相交／交界 mutation。
兩份勘誤收據均 backlink 舊 SHA、第二次重生逐 byte 相同；六項 Docker
測試通過。第三次獨立 READY 審查尚未完成，正式 catalog 仍為 DRAFT。

## 2026-09-23 第三次獨立審查與限縮 READY

第三次審查在 Docker 重生兩份 corrigendum receipt，6/6 測試通過；
另驗 x=7 不交、x=8／311 交、x=312 不交，及 32/32 安全 scanline
完整 x=8／width=304 fill，破壞首／中／末任一列皆拒絕。舊
`[8,96)` 僅包譯文，明確由 `[8,312)×[136,168)` 取代，不得再當
英文清除範圍。

因此[規格 017](../spec/017-story-page8-overlay-ready.md)及四筆
`text/story-page8-events.tsv` 只在合法 page7 state→page8 四行、完整
英文清除矩形及 page8→page9 Enter pre-write 失效契約升 READY。
前述 DRAFT、兩次退回與窄矩形錯誤保留作形成史，不是現況宣告。
正式 watcher／loader／presenter／CLI、control／2×／3×中文畫面、
同狀態 A/B、離頁無殘字、完整玩家路徑與存讀檔仍未完成；不可稱
CONFORMED 或第八頁已中文化。
