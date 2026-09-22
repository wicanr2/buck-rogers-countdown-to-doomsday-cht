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
