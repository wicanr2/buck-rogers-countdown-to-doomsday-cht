# 第一百四十二階段：第三頁五行 typed adapter 的 READY 審查

日期：2026-09-22
結論：**獨立審查通過，僅第三頁五行 typed adapter contract 升 READY；尚未接 production、不是 CONFORMED。**

## 審查輸入與位址基準

原版 `GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
第二頁合法終態 state `workplace/phase104-post-return-enter-2/control.state` SHA-256
`b15abdf487f59d982657d1d097c0b38fe3668ca3fd6d15e49c310a5486e238e2`；
第三頁合法終態 `workplace/phase104-post-return-enter-3/control.state` SHA-256
`49d4bb0681269fca1954f3e02cb2cffe93bac48086d607dcfa5d975174750cc0`。
工具為本機 dosgolem branch `buck-rogers-cht-output-overlay` commit `a9f2afd`
的 content-safe return-edge runner；review 時 branch 後續只增加第二頁測試／loader，
不改該第三頁診斷語意。Go 1.26.7、Docker image `golang:1.26.7-bookworm`。
文中 `segment:offset` 均為 dosgolem 實模式位址，不是 IDA 線性位址。

## 通過項目

1. [第 108 階段](phase-108-story-page3-draft.md)兩次私有 glyph-run 收據與
   `text/story-page3-events.tsv` 的五筆 row／length／SHA-256／entry/post step／caller
   逐欄一致；固定故事 rows 17–21 為 `34/37/31/37/5`，right-side 與 row 24 排除。
2. [第 139 階段](phase-139-story-page3-return-edge.md)新增的 entry-stack 雙重收據
   逐 byte 相同，SHA-256
   `11427a055910594f3ecce309a3d0f6d7802e93ad728113c0adf5c13be5531943`。
   144 筆全部有 `0763:03D6`／opcode `0xCA` → caller `0763:04FF`，每筆
   `entry_ss=return_ss`、相對 SP 增 `0x12`、entry<return，columns 逐字連續；
   不以一次性的絕對 SS/SP 作 runtime key。
3. [第 138 階段](phase-138-story-page3-exit-prewrite.md)雙重收據逐 byte 相同，
   SHA-256 `b707af7a80fb2322769edb7fdd7aca41afcaa05000afa5173db54ff9ac84df6c`。
   最早與安全矩形相交的原版 pre-write 是 step `301108549`、`0CF4:1B3A`、
   `ES:DI=A000:AA08`、`CX=304`，早於可見像素差與第四頁 glyph；runtime
   只能用位址、段與實際 half-open span，不得以固定 step／DI 當身份。
4. 第三頁 `[8,320)×[136,176)` 的五行各 39 cell；現行繁中候選保守寬度
   `22/22/22/22/6` cell。正式 20 份 TSV 與本機倚天 manifest 雙向一致；
   `cmd/fontcheck` 回讀 `GOLEMFNT 16x16 glyphs=1024 coverage=6179`、零缺字。
   字型與私有 PNG 只在 ignored `workplace/phase138-font/`，不得散布。
5. 可丟棄的 `workplace/phase140-page3-atomic-core/` 只讀正式五筆 TSV，不接
   production；Docker `go vet ./...`、`go test ./... -count=1 -v` 通過。
   正例完整五行才原子建 group；負例包含 partial、真錯序、duplicate、length／hash、
   caller／guard／mode／repeat／style／row／column、RETF predecessor／opcode／
   return-caller、相對 SS/SP、step order、非 READY TSV、font miss、未知 write、
   已量 pre-write、非相交 span 與 restore／stop／handoff 後不復活。

審查後，五筆 `text/story-page3-events.tsv` 的內容身份／順序未變，僅
`catalog_status` 由 DRAFT 升 `READY`；`tools/story_page3_catalog.py` 改為只接受
READY，並有 DRAFT 拒絕負例。`story-page3.zh-TW.tsv` 仍是編輯性譯文，
不是中文手冊逐字來源。

## 未完成且不可外推

READY 只授權下一步實作第三頁 typed watcher／presenter。尚缺 2×／3×同狀態
control A/B、真實可讀畫面、page3→page4 同幀清除與無殘字、正常玩家路徑抽測。
其他合法離頁、完整開機、遊戲內存讀檔、其餘故事頁及整款遊戲中文化均未證實。
