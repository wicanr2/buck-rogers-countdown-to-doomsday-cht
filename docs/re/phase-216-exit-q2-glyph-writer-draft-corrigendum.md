# 第二百一十六階段：真正 Exit 第二問繪字寫入勘誤

日期：2026-09-24
狀態：**DRAFT；僅固定合法 Y→Y 路徑的原版寫入證據，不授權擴張 writer 白名單、改規格 021 或宣稱正式 A/B 通過。**

## 問題與固定輸入

正式 control／2×／3× 同狀態 A/B 的 Y→Y 試跑在第二問（q2）尚待 guarded Return 時失敗即關閉：step `124928251`，`0763:1854`，A000 段內 offset `F0E2`。既有[第一百八十八階段](phase-188-exit-prompts-draft-evidence.md)只保留每層最早相交寫入；它沒有宣稱整個 glyph run 只會由 `0763:184D` 寫入。因此這筆新觀測須回到原版證據，而不能以未知 writer 直接加入正式允許集合。

固定輸入與來源：`START.EXE` SHA-256 `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；`GAME.OVR` SHA-256 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；合法 `a-joined.state` SHA-256 `1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`。原版與存態均為本機 ignored 輸入。執行器為 dosgolem 固定隔離複本 `cb3ca77c66e4909c5f513b807840e885ab5cb4a3`，原 probe SHA-256 `bc59d13ac98f012e1a5a13561443c05f015bca744781928b1a77894f2c55e388`；Docker image `golang:1.25.0-bookworm`，Go `go1.25.0`。兩次探針均在無網路、原版唯讀、目前 UID/GID、`--rm --memory 2g --cpus 2 --pids-limit 512` 容器中，從同一合法存態及 phase188 原有鍵盤排程重播至 DOS 退出 step `125006324`。

位址基準：`0763:…` 是 dosgolem 8086 實模式 `CS:IP`；`F0E2` 是 A000 段內 offset，線性位址為 `0xAF0E2`（十進位 `717026`），320×200 mode 13h 像素為 `(226,192)`。以下數字不可與 `GAME.OVR` 檔案 offset 混用。

## 雙重原版收據

只對 q2 dispatcher Entry `124906582` 起、guarded Return `124929724` 前，A000 段內 `[F000,F0F0)`（q2 本體首列 x=`[0,240)`、y=`192`）聚合 pre-write；包括同值寫入。`workplace/phase188-exit-prompts-draft/writer-set-yy-a.json` 與 `-b.json` 的 SHA-256 均為 `3bfc017ca3751d955b1e2f87bdc26f1ec10d5e355a19b0247ead788e02047d72`，位元組完全一致。

| `CS:IP`（實模式） | 寫入數 | 此範圍首筆 step | 證據範圍 |
| --- | ---: | ---: | --- |
| `0763:184D` | 237 | `124906844` | 本體首列背景／清除類寫入，包含既有 q1 首筆同值失效。 |
| `0763:1854` | 3 | `124928251` | 同一 q2 繪字期間的前景色寫入。 |

更窄的 `workplace/phase188-exit-prompts-draft/writer-yy-a.json` 與 `-b.json` SHA-256 均為 `6a9826ea7fa4f9421fefd2194249acb0f32b277f93455eafcd6f28622e95329e`，固定 step 鄰域逐筆一致：`124928242` 的 `0763:184D` 在 `(225,192)` 寫 `0→0`；`124928251` 的 `0763:1854` 在 `(226,192)` 寫 `0→14`；`124928259`／`124928267` 同一 `0763:1854` 依序在 `(227,192)`／`(228,192)` 寫 `0→14`。目標像素位於 q2 本體 `[0,240)×[192,200)`，未進六格尾碼 `[240,288)×[192,200)`。

既有、未覆寫的 `identity-YY-a.json`／`-b.json` SHA-256 均為 `bf93258e0264b2f334ec75b3d7b4127602e0e41d6fffe6d817e9059c83e156ad`；`yy-a.json`／`-b.json` 均為 `9f77ac3462d3fb4c2c47ad0421d17dad806776145212cf82cbe39452aff9ec94`。其 q2 exact dispatcher 事件為 Entry `124906582` → Return `124929724`，row 24、column 0、長 30、`bg/fg=0/14`；dispatcher 外 glyph run 由實模式 `0763:049B` 呼叫，從 `124906727` 連續至 `124929631`，同樣 row 24／column 0、長 30、`0/14`。目標 step 及其相鄰寫入均落在這個 run 內，且 `0→14` 對應該 run 的前景色。結合確切時序、座標、連續像素與顏色，可將目標寫入**已證實**為此固定路徑 q2 正常繪字的一部分；此判定不是依 `1854` 的名稱或位址猜測。q2 此時仍為 pending，待 `124929724` 的 guarded Return 後才可啟用覆繪層。

## 勘誤邊界

第一百八十八階段與[規格 021](../spec/021-post-join-exit-prompt-body-only-draft.md)所列 `0763:184D` 是**最早相交** pre-write；不得再把它讀成 q2 本體的唯一正常 writer。上述兩個寫入點的集合只涵蓋固定 Y→Y 路徑、q2 Entry→Return 與本體**首列** `[F000,F0F0)`；其餘七列、其他重播路徑、重入、Restore、正式 watcher 的接受條件均未知。這份 DRAFT 只為失敗診斷提供可審查證據，尚未批准程式修補、全域白名單或 CONFORMED 聲明；若正式接線要接受 `0763:1854`，應在既有 READY 契約的實作審查中確認只作用於已辨識 q2 的 pending 繪字期間，並重新取得正式雙倍率 A/B 收據。

原版、狀態、原文、完整收據與本次窄幅探針產物均留在 ignored `workplace/`，本文件不保存可還原內容。暫改的 phase188 原 probe 已還原並核對原 SHA-256；原釘選收據未覆寫。
