# 第二百一十三階段：Exit 提示繁中候選與倚天字型 DRAFT 靜態收據

日期：2026-09-24
狀態：**DRAFT；只固定顯示候選並驗靜態字型 containment，未授權 TSV、watcher 或正式覆繪。**

## 來源與文案候選

依[第一百八十三階段](phase-183-post-join-exit-identity-corrigendum.md)的原版身分，及
[第一百八十八階段](phase-188-exit-prompts-draft-evidence.md)的正常 N／Y→Y 收據，處理兩個彼此獨立的
row 24 確認提示。原版輸入固定為 `START.EXE` SHA-256
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`、`GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，以及合法加入角色 state SHA-256
`1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。兩個 identity 均由 caller
`37F1:101E` 輸出於 row 24／column 0、背景／前景 `0/14`；長度與 SHA 不同，不共用 identity。

| Identity | 已證實摘要 | DRAFT 繁中候選 | 本輪決定理由 |
| --- | --- | --- | --- |
| q1 | 12 bytes；`c38a515358859a10e7a2104cab69fe10ee2d492d94024b7d8f17d69b1a409032`；安全矩形 `[0,96)×[192,200)` | 離開至 DOS | 沿用正式選單 `menu.exit_to_dos` 的既有譯詞，維持同一動作術語一致。 |
| q2 | 30 bytes；`35023ac3208312fb1c932ec15a737aae88817925d6cabb26d83281bf755bdcb8`；安全矩形 `[0,240)×[192,200)` | 遊戲尚未儲存。仍要離開？ | 沿用 phase 183 的第二問候選，保留未儲存警示與再次確認語氣。 |

以上是 DRAFT 顯示層用字，不進正式 `text/*.tsv`，不影響原版 Y/N 比較、消費或離開判定。q1 與
選單項用字相同，也不表示它們可共用 identity、generation 或生命週期。

## 倚天字型檢查

先在 Docker 內重跑 phase184 既有 `verify_exit_prompt_draft.py`：identity／正常 N 與 Y→Y branch／原字型檢查三項均通過。
再由忽略工作區 `workplace/phase213-exit-prompt-font/verify_exit_prompt_font.py` 檢查目前 local-only 倚天
`GOLEMFNT`（SHA-256 `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`；1,028 glyph），並直接
唯讀核對 `ASCFONT.15`、`SPCFONT.15`、`STDFONT.15` 的既有固定 SHA-256。只輸出不含原文、字模或影像的 JSON
收據 `workplace/phase213-exit-prompt-font/receipt.json`；原字型與原始倚天字型均不複製至研究工作區。

| 尺度 | 字形墨跡 | q1 / q2 安全矩形 | 後接原版六格尾碼保護區 | 結果 |
| --- | --- | --- | --- | --- |
| 2× | 16×16 | `[0,192)×[384,400)` / `[0,480)×[384,400)` | `[192,288)×[384,400)` / `[480,576)×[384,400)` | 兩句零缺字、零越界；尾碼 overlay diff 0。 |
| 3× | CJK 22×22 置於 24×24 格內、偏移 `(1,1)`；ASCII 維持 16×16 並置中 | `[0,288)×[576,600)` / `[0,720)×[576,600)` | `[288,432)×[576,600)` / `[720,864)×[576,600)` | 兩句零缺字、零越界；尾碼 overlay diff 0。 |

「尾碼 overlay diff 0」由原型採 body-only 墨跡寫入遮罩並斷言遮罩與六格保護區不相交；它是靜態原型
不變量，**不是**原版 runtime 擷取的像素差分。q1／q2 譯文 advance 均短於各自本體安全矩形。

## 限制與下一門檻

本階段只完成譯詞 DRAFT 與靜態倚天字型 containment。phase 188 所記尾碼是原版可見多色／反白選擇狀態；本收據
不替它決定正式保留或重繪方式。N 返回、Y→Y 終止、q1／q2 更新時機、terminal cleanup、色彩、原版／覆繪
同狀態 A/B 仍須另行證明與審查；目前不新增正式 catalog、不接 watcher，也不升 READY／CONFORMED。

Docker 工作使用既有 `nectaris-font-subset:20260821`，`--rm --network none`、目前 UID/GID、明確資源上限；倚天來源唯讀，
只有 ignored `workplace/` 作輸出。容器完成後已確認沒有本案執行中或停止容器，也沒有產生 root-owned 產物或 `.md` 目錄。
