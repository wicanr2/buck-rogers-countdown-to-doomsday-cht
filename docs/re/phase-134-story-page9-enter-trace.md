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
