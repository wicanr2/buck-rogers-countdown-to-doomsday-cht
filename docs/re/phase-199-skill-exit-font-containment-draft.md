# 第一百九十九階段：技能頁離開問句的雙倍率字型靜態檢查

日期：2026-09-24
狀態：**DRAFT 靜態驗證；不代表原版執行期已覆繪或生命週期已驗。**

沿[第一百九十七階段](phase-197-skill-exit-confirmation-prewrite-draft.md)已量的
職業問句 `[0,264)×[192,200)`、技術問句 `[0,272)×[192,200)`
logical 本體安全矩形，僅驗版控 TSV 與本機正式候選字型是否可排入；
原版六格多色尾碼各在矩形右側，保持原版、不參與譯文。

輸入 `text/skill-exit-confirmation.zh-TW.tsv` SHA-256 為
`48bf551e6b60c12fb672ebe6e27756069f8351bc763443447f80778c29c0e2c7`；
本機 ignored `workplace/current-font/buckrogers-eten-top-pad.golemfnt`
SHA-256 為
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
重用 ignored `workplace/phase162-post-join-menu-ready-candidate/verify_post_join_menu.py`
的 `load_font` 與 `contain` 靜態 raster 檢查，其檔案 SHA-256 為
`01aebe2dc13f6e1af75574623cb3d9ddb31d9b08b9707f884460e716068d2b79`。
在無網路、唯讀專案掛載的 `eob-remake-go:1.26.7-ebiten2.9.9`
Docker 中，先跑 `python3 tools/catalog_font.py lint text/skill-exit-confirmation.zh-TW.tsv`，
再固定兩個 exact key、`runtime-interface` 來源、各 17 個 Unicode 字元及
上述安全矩形呼叫 `contain`。兩步皆通過，缺字與墨跡越界均為零。

| 倍率 | 職業／技術安全矩形（輸出像素、半開） | 共同字錨 | 來源字模可見墨點 |
| --- | --- | --- | --- |
| 2× | `[0,528)×[384,400)`／`[0,544)×[384,400)` | `(0,384)` | 1211／1134 |
| 3× | `[0,792)×[576,600)`／`[0,816)×[576,600)` | `(1,577)` | 1211／1134 |

2×採 16×16 字格／墨跡；3×採 24×24 字格、22×22 墨跡及
`(1,1)` 偏移。表中的墨點是 16×16 來源字模的非零點數，
不是輸出後放大像素數。此檢查以字格／墨跡 containment 排除靜態
溢出，不能取代正常原版畫面、原版尾碼重畫或 N／Y 後含同值
A000 清層。故[規格 020](../spec/020-skill-exit-confirmation-overlay-draft.md)
仍為 DRAFT，不能接正式 watcher／presenter。
