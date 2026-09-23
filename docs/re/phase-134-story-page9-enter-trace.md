# 第一百三十四階段：第八頁後合法 Enter 的第九頁 trace

日期：2026-09-22
狀態：**一筆 content-safe identity 與同狀態畫面已確認；繁中候選維持 DRAFT，未接 runtime。**

## 重播與輸入

本輪從既有第八頁合法終態 `workplace/page8-next-trace/page8-a.state` 開始，輸入 state
SHA-256 為 `327dc1cb8baf4bee71cdcd0173538af123c47266c8bbf556b28f38d89355b0a9`。在
`351000000` 排入一筆正常 BIOS Enter（scan `0x1c`、ASCII `0x0d`），執行至
`360000000`。原版 `GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，只讀掛載。

使用 dosgolem `buckrogers-text-receipt`（工作樹 commit `b4e1fb74b93fddabcde20c7ac07132604de04471`），
成功收據由現有 `golang:1.26.7-bookworm` Docker image 的 `go run ./cmd/buckrogers-text-receipt`
產生；
開啟 `-glyph-trace`、`-glyph-return-edge-trace`、`-clear-trace` 與
`-story-pixel-trace`。兩次重播收據與 indexed framebuffer 逐 byte 相同：

- receipt：`workplace/page9-next-trace/page9-a.json`、`page9-b.json`
- receipt SHA-256：`2512d6b4c9f62089bee99afd57029fed548ab2a1d148fa704fa366f2ce576962`
- indexed SHA-256：`fb65f3b36e019caa8d0e74d72aa71ab9908b76ec03fc1f5c301ca563473647b0`
- memory SHA-256：`fb64b0051d215b3c4a5bab64cc0f89bdc235a66e2d9194110b438c6a076b4325`
- palette SHA-256：`6ff2334f924ec0eeb8d96fdddd074ba4a74ed43aab6036c32e48805870f3633d`

私有檢視裁切 `workplace/page9-next-trace/page9-story-rows16-21-4x.png` SHA-256
為 `d6f56ad6297a763161f3e5b3758cee2503bbf80b049c2bf540d3a65adbf8dc91`，只供人工核對，
不進 Git。兩次收據均記錄同一個 story-region 首次寫入：step `351154358`、指令
`0CF4:1B3A`、`ES:DI=A000:AB48`、`CX=304`，bounding box `x=11..301,y=137`。

## 已證實 identity 與排除範圍

固定故事區只有一個連續的 `0763:04FF → 0763:026B` guarded glyph run，為
`mode/repeat=1/1`、背景／前景 `0/10`、row 17、column 1、長度 20。完整 length／
SHA-256／entry／post-call step 已鎖在 `text/story-page9-events.tsv`；該檔只保存
content-safe metadata，不保存原文全文或 glyph bytes。兩次收據也確認其 20 個字元均有
同一 `RETF` return edge。

同一終態另有 row 24、caller `37F1:0337`、背景／前景 `15/0` 的 33 個 glyph，屬右側
動態狀態列，明確排除；右側人物姓名同樣不加入 catalog。本輪只證明第九頁固定敘事，
不外推完整開機玩家路徑、存讀檔或故事生命週期已驗收。

## DRAFT 資料與驗證

`text/story-page9.zh-TW.tsv` 只有一筆 `runtime-editorial` 繁中候選，依私有裁切與
已證實 glyph identity 建立；這是編輯草稿，不是已完成覆繪。
人工校對時將帶有強制拘押意味的「押送」修正為不增加該語意的「列隊離開」，原文只供本機
檢視、不加入版控。`tools/story_page9_catalog.py`
檢查 identity、key、來源、NFC、控制字元與 39 格寬度；`tools/test_story_page9_catalog.py`
涵蓋 hash drift、key drift、控制字元等失敗案例。

全部 20 份繁中 catalog 由本機唯讀倚天 15 點來源重建私有 top-pad GOLEMFNT，得到
1026 個 16×16 字模，SHA-256 `dd7d650ce1ebf56d0f43fe55dce0ecc43f99486925b44d795064504bb0a6eb49`；
dosgolem 正式 `cmd/fontcheck` 回讀，6182 個譯文字元零缺字。產物與來源 manifest 僅在
ignored `workplace/phase134-font/`，不公開散布；字型覆蓋不構成中文畫面驗收。

Docker 內驗證命令：

```text
PYTHONPATH=tools python3 -m unittest tools/test_story_page9_catalog.py
python3 tools/story_page9_catalog.py text/story-page9-events.tsv text/story-page9.zh-TW.tsv
```

本階段只完成原版 content-safe identity、私有畫面證據與 DRAFT catalog。第九頁仍須
READY 規格、正式 watcher／renderer、同狀態原文／繁中 A/B、清除／返回生命週期與正常
玩家路徑收據，方可稱為已中文化。

## 2026-09-23 READY 前置重生與離頁停止線

以本機 dosgolem commit
`c0f6d76b0eb60caa72e74a619c1b981c91b340a5` 在無網路、有界 Docker 內建置固定
`buckrogers-text-receipt`；runner SHA-256 為
`d150746873eb8e0f715baffca27cd26523d8cf132e3915aaf338845bf3725b52`。
原版仍為上述 `GAME.OVR` 雜湊；位址皆為 dosgolem 實模式 `segment:offset`，不是
IDA 線性位址。私有 runner、state、完整收據與 framebuffer 僅在 ignored
`workplace/page9-ready-atomic-core/`，不得加入 Git 或公開封包。

從合法 page8 state（SHA-256
`327dc1cb8baf4bee71cdcd0173538af123c47266c8bbf556b28f38d89355b0a9`）於 step
`351000000` 送 Enter，縮短執行至 `352100000`，兩份 entry JSON／stdout 逐 byte
相同，SHA-256 均為
`0d27b6948399aff772aa2533a2b0b8ca19b5b9495c1c51bee94cd197eeec3873`；兩份
indexed framebuffer 亦相同，SHA-256
`fb65f3b36e019caa8d0e74d72aa71ab9908b76ec03fc1f5c301ca563473647b0`。
兩次皆直接記錄 row 17、columns 1–20 的 20 筆 glyph entry 與 20 筆 verified
return edge：返回指令 `0763:03D6`、opcode `0xCA`、caller `0763:04FF`、entry／return
同 SS `1841`、SP 相對增加 `0x12`，七個 ABI word 的 high-word mask 均為零；首筆
entry `351155910`、末筆 post-call `351988536` 與正式 DRAFT identity 一致。這補強
逐字 return／ABI 證據，但不自行把 catalog 升 READY。

離頁側從既有合法 page9 state（檔案 SHA-256
`563ed40ba276c6857c57b05344949dec5891e4596ad783a9fc89b805eae8c2a4`）開始；此值不得與
phase134 的 memory SHA-256 混用。
在 step `361000000` 送 Enter、執行至 `370000000` 的兩份 exit JSON／stdout 逐 byte
相同，SHA-256
`bc1c11cba16bf57bda6bc3f5370a5c8be9279f99e8343a38c6b9abddb9541ab6`；indexed
framebuffer SHA-256 均為
`0aba8869b347eb07683bf3a74825ccfc36eecbf8feaf96b20cd2ac50c1745df0`。
兩份收據均沒有 `story_fill_writes` 或 `story_pixel_write`，所以沒有可證的 page9
故事區最早相交 pre-write。

另以有界 key／instruction probe（收據 SHA-256
`1ef70fafc346989fed6dfc4e8f36eb5415825ac6c9053b06ff74a907eccd01b2`）確認該 Enter
不是未被消費：step `361000150` 由 BIOS `INT 16h AH=00` 讀取，step `361111822`
起出現 row 15、caller `0763:049B` 的 command/status glyph。這個轉場只重畫
command/status，沒有改寫 row 17 的第九頁故事文字；因此不能把該 Enter、row 15
glyph 或「沒有第十頁」誤當成覆繪失效事件。

結論與停止線：第九頁 entry identity／逐字 return／ABI 已確認，但故事區真正被清除或
覆寫的合法後續玩家動作、state 與最早相交 pre-write 仍未知。未取得該證據前不得建立
宣稱可升 READY 的 typed-core、不得接 production watcher／renderer，也不得稱第九頁
已中文化；`text/story-page9-events.tsv` 與本頁狀態保持 DRAFT。

## 2026-09-23 手冊明示數字鍵盤 4／6 的最小生命周期邊界

依[第一百一十二階段](phase-112-command-turn-manual-evidence.md)的中文手冊原圖證據，
數字鍵盤 4／6 分別是左／右轉；本輪只使用這兩個已明示的正常玩家控制，未送 Esc、
Alt+Q、數字鍵盤 2 或任何猜測鍵。它們是檢驗第九頁故事區失效的候選，並不因手冊標為
轉向就被預設為可離開故事頁。

從上述合法 page9 state（SHA-256
`563ed40ba276c6857c57b05344949dec5891e4596ad783a9fc89b805eae8c2a4`）開始，兩鍵均在
step `361000000` 排入，固定跑到 `361100000`。使用的是本階段先前已鎖定、未重建的
`buckrogers-text-receipt`（build provenance dosgolem commit
`c0f6d76b0eb60caa72e74a619c1b981c91b340a5`、runner SHA-256
`d150746873eb8e0f715baffca27cd26523d8cf132e3915aaf338845bf3725b52`）；原版維持唯讀，
位址仍是 dosgolem 實模式 `segment:offset`。收據只記錄 content-safe metadata，位於
ignored `workplace/page9-lifecycle-search/`。

- 數字鍵盤 4（`4B:00`）的兩次獨立收據
  `key4-a.json`、`key4-probe.json` 逐 byte 相同，SHA-256 均為
  `c0a17ffc923bd0c627c14d601c91e95ec9f8d0909cb6bec5015561d9aadbc4b3`。
- 數字鍵盤 6（`4D:00`）的 `key6-a.json`、`key6-b.json` 也逐 byte 相同，SHA-256 均為
  `9522cef7f52f7494c02c8448c77df12b5a7ef28cbeab8298e65443a6989bdd5a`。
- 四份收據都在 step `361000150` 由 BIOS `INT 16h/AH=00h` 消費相應鍵值，唯一 clear 是
  step `361028641` 的 text row 24（`top=bottom=24,left=33,right=39`），其後只有 row 24、
  columns 0–32 的 33 glyph command/status run。這與第九頁故事區 `[8,168)` 不相交。
  每份的 `story_fill_writes` 與 `story_pixel_write` 都是空值，indexed framebuffer 與
  palette 的 SHA-256 分別仍是
  `fb65f3b36e019caa8d0e74d72aa71ab9908b76ec03fc1f5c301ca563473647b0`、
  `6ff2334f924ec0eeb8d96fdddd074ba4a74ed43aab6036c32e48805870f3633d`。

因此，這兩個已證實控制只重畫 row 24 command/status，沒有提供故事區 clear、fill、
pixel pre-write 或可授權的覆繪失效邊界。第九頁保持 DRAFT，未接 production。下一個
候選必須先由手冊證實為適用於這個 page9 command state 的**不同**玩家動作；在取得該
適用性證據前，不再擴大 scan-code 探索。

### Num Lock 8 的下一輪詢停止線

上述手冊也明示數字鍵盤 8 為前進，且本輪已量到 page9 的 4／6 與第一百二十六階段的
8 都進入同一 `0C10:031C`／`37F1:1116 ← 328E:1732` keyboard consumer。因此 8 是
可送入此 command state 的合法候選，但「前進」的玩家可見結果仍是未知，不能由較早
state 的結果外推。

從同一 page9 state 於 step `361000000` 排入單鍵 Num Lock 8（`48:38`），設定
`0C10:0305` 且 `stop-after-step=361000200` 為第一個後續輪詢停止點，`362000000` 只作
safety cap；沒有第二鍵或延長。固定 runner 與原版 provenance 同上。`key8-a.json`、
`key8-b.json`（ignored `workplace/page9-lifecycle-search/`）逐 byte 相同，SHA-256 均為
`fdb75c61c2a5f1d6c800be4088bea9ff92a4378b4ac51560b96cd685a17112a2`。兩次都在 step
`361000150` 由 BIOS `INT 16h/AH=00h` 取走 `0x4838`，並精確停於 step `361000605`；
`events`、`clears`、glyph、return edges 均為零，`story_fill_writes`／`story_pixel_write`
均空，indexed／palette SHA-256 仍為上節數值。

這證實合法 8 在下一次輪詢前沒有清除、填入、重畫或觸及 page9 故事矩形，且沒有
command/status 輸出；它不證明 8 的遊戲語意為無效。依預先設定的停止條件，不延長這條
分支，也不再猜鍵。現有手冊明示的 4／6／8 都未給出第九頁失效邊界，故 page9 保持
DRAFT，沒有 READY 或 production 授權。

## 2026-09-24 限縮範圍勘誤：入頁單行 READY 候選

前述「沒有自然離頁相交 pre-write，因此整個第九頁不可升 READY」的停止線
對完整生命週期仍有效；它未考慮僅核准**已量入頁單行本體**、並用機器層
任何相交 A000 byte pre-write 與 Stop／Restore 失敗即關閉的更窄契約。
現有 `machine.ObserveVideoWrites` 在 `VGA.Write` 前回呼所有 A000 byte，
包括同值寫入；這是 dosgolem 目前工作樹的 API 能力，並非本輪新量到
一筆第九頁自然離頁。據此提出[規格 022](../spec/022-story-page9-overlay-draft.md)
作**限縮 READY 候選待獨立審查**。本節保留先前收據與結論形成脈絡；
`text/story-page9-events.tsv` 仍為 DRAFT，正式 watcher／renderer、
2×／3× 幾何及同狀態 A/B 均未接通。Enter、4、6、8 的 row 15／24 重畫
仍不得被解釋為故事區退出。

### 入頁原文寫入與本體幾何補證

本輪對上述合法 page8 state 以原排程於 step `351000000` 送 Enter、
固定跑至 `352100000`，在現有 `machine.ObserveVideoWrites` 掛 content-safe
一次性 probe；`GAME.OVR` 雜湊與位址空間同本頁前述，工具為
`golang:1.26.7-bookworm` 的 Go 1.26.7、dosgolem 工作樹
`a01e34253fa59cc92c3fde1bf4b33577e318e9e7`（另有下列一次性未追蹤
測試檔）。probe 與私有輸入只在
ignored `workplace/dosgolem/apps/buckrogers/story_page9_candidate_prewrite_test.go`
及 `workplace/` 原始資料；probe SHA-256
`46a2980172a55ada9f5d4aa8b1713d6cb2dfa178b9bc998cefea251afb8d63f3`，
沒有匯出原文 bytes 或 framebuffer。
`351155910..351988536` 的 20 個 glyph entry／return frame 內，安全矩形
`[8,168)×[136,144)` 有 **1,280 筆 A000 byte pre-write**，每 frame 64 筆，
frame 外 0、錯字格 0；首筆 `351156027`，末筆 `351988519`，writer
`0763:184D` 1,028 筆、`0763:1854` 252 筆。因此「相交 A000 寫入
連 pending 一律清掉」會把正常原文建構誤判為離頁，不能作 READY 契約。
[規格 022](../spec/022-story-page9-overlay-draft.md)已把 pending 的已證實
glyph frame 寫入與 active 後任何相交寫入分開；後者仍未量到自然離頁。

另用既有本機 GOLEMFNT（SHA-256
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`）
與正式 `xlate.Layer.Draw`／`manualThreeXFont`，在合成畫布對
「你們列隊離開。」量到 2×／3× 矩形外零差、零缺字，右側 x=168
邊界未被改動。一次性
`workplace/dosgolem/apps/buckrogers/story_page9_candidate_geometry_test.go`
SHA-256 為
`0afb4bb32a79fbdf700a6efb2ff60448f52e6169c3842cd1282b791355a76379`。
這補上候選的字型幾何，不是原版 A/B，也不升格
`text/story-page9-events.tsv` 的 DRAFT 狀態。

## 2026-09-24 獨立證據審查：固定單行入頁本體

結論：**規格 022 的合法 page8→page9、row 17／column 1 固定 20-glyph
入頁本體，可限縮升 READY，准許依該規格接正式 watcher／presenter；
不核准完整第九頁、自然離頁、正常玩家路徑或 CONFORMED 聲明。**
此審查不把尚未量到的自然離頁誤寫成已證實。若後續轉場沒有相交 A000
pre-write，也沒有 Stop／Restore，現有契約不能保證即時清除覆繪；該出口
仍須返回 RE／DRAFT。Enter、4／6／8 的既有短窗及 row 15／24 重畫
不得充當該出口收據。

審查核對原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`、
合法 page8 state SHA-256
`327dc1cb8baf4bee71cdcd0173538af123c47266c8bbf556b28f38d89355b0a9`、
entry A/B 收據 SHA-256
`0d27b6948399aff772aa2533a2b0b8ca19b5b9495c1c51bee94cd197eeec3873`、
indexed SHA-256
`fb65f3b36e019caa8d0e74d72aa71ab9908b76ec03fc1f5c301ca563473647b0`。
位址均為 dosgolem 實模式 `segment:offset`；A000 是視訊 byte offset。
本次重跑的 dosgolem 工作樹含 ignored 一次性 probe；probe SHA-256
`46a2980172a55ada9f5d4aa8b1713d6cb2dfa178b9bc998cefea251afb8d63f3`。
`golang:1.26.7-bookworm`／Go 1.26.7、無網路、有界 Docker 重跑得到
20 個 frame 各 64 筆相交 pre-write、總數 1,280、frame 外／錯字格 0；
writer `0763:184D` 1,028 筆及 `0763:1854` 252 筆。這些寫入都在
guarded return 以前建構原文，必須容許於 pending；第 20 筆返回後才
能啟用 active。active 後任一相交 byte pre-write，包括同值寫入，應在
原版 write 前清 event／stamp；Stop／Restore／epoch 中斷亦清層。

目前正式第九頁 TSV 的 SHA-256 分別為 events
`7813dc686a398c0355040387cd60f41140d7b2649ea1e89607c4bd8d18fe63b5`、
譯文 `baf9ba8b56757261ba1e022e69c2df34c971c5679b593c83a694c0b4b809cb2e`；
本機現用 1,028 字倚天 top-pad GOLEMFNT SHA-256
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`，
其 manifest 鎖住本筆譯文雜湊與三份唯讀來源字型雜湊。它與本頁前段
1,026 字的舊字型是不同版本；幾何驗證採**現用 1,028 字版**。
`PYTHONPATH=tools python3 -m unittest tools/test_story_page9_catalog.py`
六項通過，catalog lint 通過。一次性幾何 probe SHA-256
`0afb4bb32a79fbdf700a6efb2ff60448f52e6169c3842cd1282b791355a76379`
以正式 `xlate.Layer.Draw`／`manualThreeXFont` 測得 2×／3× 零缺字且
核准矩形外零差；這只證明合成畫布的 containment，並非原版同狀態 A/B。
規格 022 已訂正一處幾何語意：`xlate.Stamp` 每個 rune 實際前進一個
8-pixel 邏輯字格，TSV 的中文字元兩格僅是保守 lint。

正式實作最小清單：先鎖單筆 TSV／譯文／字型版本，再驗 20 筆逐字
caller、guard、style、座標、bytes SHA、ABI、`0763:03D6`／`0xCA`、
SS／SP 與時間次序；pending 每 frame 僅准上述兩個 writer 在當前字格
的 64 筆 pre-write，異常即清；第 20 筆 verified return 才原子提交；
active 後任何相交 A000 byte pre-write、Stop、Restore 或 epoch 中斷
清 watcher、queued event 及 RGBA stamp；2×／3× presenter 只畫核准矩形。
正式 typed 假資料失敗矩陣及合法 page8 state 的 control／2×／3×
同狀態 A/B 仍是接線後必過的 CONFORMED 閘門，不是本次 READY 證據。

### 審查後 catalog 狀態同步

主代理依上述獨立審查，僅將固定入頁單行的規格 022 與
`text/story-page9-events.tsv` 從 DRAFT 升為**限縮 READY**，正式接線得以開始；
譯文未改。升級後 events TSV SHA-256 為
`1acc41cf8f904e3363e1f22d753c91a75ba00767fe531d4152bb1ad618bdd735`，
譯文仍為 `baf9ba8b56757261ba1e022e69c2df34c971c5679b593c83a694c0b4b809cb2e`。
原先 DRAFT 檔案雜湊保留於上節，作為審查當時的輸入，不可誤認為現行 TSV。
READY catalog lint 七項測試通過，其中一項明確拒絕退回 DRAFT status；
這不表示 watcher、原版 A/B、自然離頁或整頁中文化已完成。
