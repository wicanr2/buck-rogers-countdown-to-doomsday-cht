# 第一百二十九階段：第六頁後合法 Enter 的第七頁 trace

狀態：**六行 content-safe identity 與同狀態畫面已確認；繁中候選維持 DRAFT，未接 runtime。**

從私有 `workplace/page7-next-trace/next.json` 與 `next-b.json` 萃取；兩份 receipt 逐 byte 相同，SHA-256 `f517b01f23e12df2d5719827e36b74a51e9df3e7adaa2f810b4039854c20e1b7`。兩者均由既有第六頁 state、step `331000000` 的正常 BIOS Enter 重播至 340M。

row 17–22 六筆均為 dosgolem 實模式 `0763:04FF → 0763:026B`、mode/repeat `1/1`、背景/前景 `0/10`、column `1` 的 guarded run。完整 hash、length、entry/post 步數在 `text/story-page7-events.tsv`；右側人物名與 row24狀態列排除。

再次從相同第六頁 state 與 BIOS Enter 重播，原版 indexed framebuffer SHA-256 為 `4d7ea3dc2efc3cd41c8541b7742c5f9868940d1a379fe1232998d39902c4cc76`，色盤為 `67c6c8a8865c38679a5f904fb0950a97aedbe25b27e062a78defd78f37c55e88`，與前述雙收據一致。由同一 state 產生的原版 PNG SHA-256 為 `ed35b4e7f50fbaa395416bb4f595c3585fa1e025e614bfd9af2cbdaaf3b00056`；僅裁切六行並放大四倍的私有檢視圖 SHA-256 為 `914db56fa8fa36b7efb25be30e3504f57867c83db19967d71ac742ce3d4560af`。檢視後逐行核對 catalog；原圖、裁切、state 與完整收據均留在 ignored `workplace/page7-next-trace/`。這些是原版辨識證據，不是中文覆繪的 A/B。

`text/story-page7.zh-TW.tsv` 收錄六行繁中候選，保留原文行序；`runtime-editorial` 表示依同狀態私有畫面與 glyph identity 編輯，並非已完成覆繪驗收。`tools/story_page7_catalog.py` 檢查 identity、key、來源、NFC、控制字元與 39 格寬度；相應單元測試在 Docker 內通過。第七頁仍須 READY 規格、runtime 接線與同狀態原文／中文 A/B，方可稱已中文化。

字型覆蓋另以本機唯讀倚天 15 點來源重建全部 18 份 catalog 的私有 GOLEMFNT 子集：1022 字模，SHA-256 `9c6ba4007ef02cb40b73cd21dbac5e98dd5dfa290f28e7899615c43cba47a1ba`；dosgolem 正式 `cmd/fontcheck` 回讀，6136 個譯文字元零缺字。產物與 manifest 僅留 ignored `workplace/phase129-font/`，不得公開散布。這只證明字型覆蓋，不是玩家畫面驗收。

第七頁首 glyph 前的首個 story-region 原版寫入是 step `331026808`、`0CF4:1B3A`；這是第六頁 stamp 的候選失效邊界，非 runtime 實作授權。本階段不建立新幾何、watcher、renderer、A/B 或 READY 宣稱。

## 2026-09-23 勘誤：最早相交 pre-write

上段「首個原版寫入」不正確。後續同一起點的雙重逐字／fill 收據
`workplace/page7-ready-atomic-core/entry-{a,b}.json` 均先記錄 step
`331026784` 的 pre-execution `0CF4:1B3A`、`ES:DI=A000:AA08`、
`CX=304`；`331026808` 是下一筆 fill，不是第一筆。先前觀察不得
取代新的寫入事件順序。第六頁已量離頁採前者作最早相交失效錨點，
證據與適用範圍見[第一百四十九階段](phase-149-story-page6-ready-prerequisite-diagnostics.md)；
第七頁自身仍待 READY 審查，見[第一百五十三階段](phase-153-story-page7-ready-prerequisite-diagnostics.md)。
