# 第一百三十一階段：第七頁後合法 Enter 的第八頁 trace

狀態：**四行 content-safe identity 與同狀態畫面已確認；繁中候選維持 DRAFT，未接 runtime。**

## 重播與輸入

前置是既有第七頁合法終態 `workplace/page7-next-trace/page7.state`，SHA-256
`e869b67264539aff95ca5929a9858c74475feea47e0c7b3a505ea9cd0aa9a460`。使用 dosgolem
工作樹 commit `b4e1fb74b93fddabcde20c7ac07132604de04471`，由 state `340000000` 在
`341000000` 排入一筆正常 BIOS Enter（scan `0x1c`、ASCII `0x0d`），執行至
`350000000`。工具映像為既有 `eob-remake-go:1.26.7-ebiten2.9.9`，入口為
`go run ./cmd/buckrogers-text-receipt`，使用 `-glyph-trace`、`-glyph-return-edge-trace`、
`-clear-trace` 與 `-story-pixel-trace`。原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，只讀掛載；
原始 ZIP 與解出檔案均只在 ignored
`workplace/original/`，不進 Git。

兩次重播收據 `workplace/page8-next-trace/page8-a.json` 與 `page8-b.json` 逐 byte
相同，SHA-256 `3cd3a311f9aa35a90f60efdd8f72b79353c497efdf51e7620f8af9328b1fa8e7`。
兩份 indexed framebuffer 亦逐 byte 相同，SHA-256
`5fd1fa4c86b534eea4c3d89fd599dc837fe07bc8d1d0f1bd27dceddf18c4d8f8`；palette SHA-256
`67c6c8a8865c38679a5f904fb0950a97aedbe25b27e062a78defd78f37c55e88`。私有檢視裁切
`page8-story-rows17-20-4x.png` SHA-256
`79b48a505264bbbeb90983dc03d29094e6daa78d7b9f98f66c36db9b6c8147e8`；它不是散布素材。

## 已證實 identity 與排除範圍

故事區由四個連續的 `0763:04FF → 0763:026B` guarded glyph run 組成，均為
`mode/repeat=1/1`、背景／前景 `0/10`、column `1`，位於 row 17–20。完整
length／SHA-256／entry／post-call step 已鎖在 `text/story-page8-events.tsv`；檔案只保存
content-safe metadata，不保存原文或 glyph bytes。四行的 length 依序為 38、37、33、22。

第八頁第一筆 story-region 可見寫入發生於 step `341018680`，指令
`0CF4:1B3A`，`ES:DI=A000:AB48`、`CX=304`，變化 bounding box 為
`x=11..285, y=137`。這是前一頁覆繪失效的候選邊界，不是 runtime invalidation 授權。

同一收據另有 row 24、caller `37F1:0337`、背景／前景 `15/0` 的 33 glyph；它是右側
動態狀態列，明確排除。右側人物姓名也不加入本 catalog。沒有把第八頁推論成完整
玩家開機路徑、存讀檔或故事生命週期已驗收。

## DRAFT 資料與驗證

`text/story-page8.zh-TW.tsv` 依私有裁切與已證實 glyph identity 建立四行繁中候選，
來源標記為 `runtime-editorial`，只作編輯草稿，未授權 production overlay。候選以
保守 39 格寬度檢查、NFC、控制字元、key 雙向一對一及 metadata hash 固定；驗證器與
負向測試為 `tools/story_page8_catalog.py`、`tools/test_story_page8_catalog.py`。

全部 19 份繁中 catalog 以本機唯讀倚天 15 點來源重建私有 top-pad GOLEMFNT，得到
1025 個 16×16 字模，SHA-256 `c183b001995fabf58f1ac66f61447746b3991fee2f11c3ef4847a8c74913f881`；
dosgolem 正式 `cmd/fontcheck` 回讀，6175 個譯文字元零缺字。產物與來源 manifest 僅留
ignored `workplace/phase131-font/`，不可公開散布；字型覆蓋不等於 runtime 畫面驗收。

Docker 內驗證命令：

```text
PYTHONPATH=tools python3 -m unittest tools/test_story_page8_catalog.py
python3 tools/story_page8_catalog.py text/story-page8-events.tsv text/story-page8.zh-TW.tsv
```

本階段只完成原版 content-safe identity、私有畫面證據與 DRAFT catalog；第八頁仍須
READY 規格、正式 watcher／renderer、同狀態原文／繁中 A/B、清除／返回生命週期與正常
玩家路徑收據，方可稱為已中文化。
