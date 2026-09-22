# 第一百二十四階段：第四頁首次 glyph trace 勘誤

日期：2026-09-22

狀態：**已確認第四頁六行的低階 glyph identity；catalog 維持 DRAFT，未接 runtime，未升 READY。**

## 勘誤範圍

第一百一十三與一百一十五階段正確保留了既有 page4 終態畫面與「當時沒有可用 caller／步數收據」的限制；它們沒有證明第四頁不存在 glyph path。本階段不覆寫該歷史。

原因已可重現：當時使用的 receipt 二進位未含後來 source 的 glyph-return-edge 診斷。以 dosgolem 工作樹 commit `9f6cac6c425a759024d7656dcf2a485049042465` 的現有 source 在容器暫存重建診斷工具後，同一合法前置 state 與同一輸入即可量到六行。未改動 dosgolem production watcher、原版 EXE／OVR、VRAM、輸入語意或任何 runtime overlay。

## 可重播輸入與決定性

- 前置 state：`workplace/phase104-post-return-enter-3/control.state`，SHA-256 `49d4bb0681269fca1954f3e02cb2cffe93bac48086d607dcfa5d975174750cc0`。
- 原版輸入：唯讀 `GAME.OVR`，SHA-256 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 在絕對步 `301000000` 排入一筆正常 BIOS Enter（scan `0x1c`、ASCII `0x0d`），執行至 `310000000`；這是既有 phase104 正常連續故事頁排程，不是新猜測的按鍵。
- 兩次無網路 Docker 重播均為同一 104,341-byte content-safe receipt，SHA-256 `ce16d1ff937d463a93728adea00397ccb2aff9ffedea20c06bddc4a1871819b5`。終態 machine／indexed framebuffer／palette SHA-256 分別為 `76f7360c4d973a357c872d9e8531473e3a51ecfac593a9e3c24722920ec40b48`、`4f9d1bb280724737ca72599c3e7d387c23c076f7e0a8637d8d3ebc9164514bf2`、`726d468223f5e24b68dae2a5c853f9280a9be3c40990b6e3102ac11968aaba08`。

私有 receipt 只在 ignored `workplace/page4-lowlevel-probe/`；其中不含原文 glyph bytes、答案、indexed pixels、截圖或 state bytes。

## 已證實的 identity

所有位址均為 dosgolem 實模式 `segment:offset` 位址空間。每行均由 caller `0763:04FF` 呼叫 glyph primitive `0763:026B`；mode／repeat=`1/1`，背景／前景色=`0/10`，column=`1`。每個 run 僅在 primitive return 的 caller、SS 與 `SP+0x12` guard 通過後才合併並雜湊；原始 bytes 隨即丟棄。

| 行 | row | length | SHA-256 | entry step | post-call step | 舊 visual 候選 |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| 1 | 17 | 34 | `70dcbd…d95bf` | 301110011 | 302556029 | 不符 |
| 2 | 18 | 37 | `b2005b…b6247` | 302599801 | 304177273 | 不符 |
| 3 | 19 | 33 | `41248d…cda7` | 304221261 | 305623148 | 不符（同長度、hash 不同） |
| 4 | 20 | 31 | `35b59e…00eda` | 305667022 | 306981257 | 不符 |
| 5 | 21 | 33 | `c83d64…b561b` | 307025461 | 308427356 | 不符 |
| 6 | 22 | 24 | `ab0a68…65066` | 308471572 | 309478931 | 相符 |

完整的 64 位 SHA-256 與六筆 entry／post 步數已回填 `text/story-page4-events.tsv`；驗證器拒絕 hash、caller／guard、步數或 DRAFT 狀態漂移。

## visual-transcription 的逐筆訂正

舊 screenshot-derived 目錄原本只以視覺轉寫得到候選。逐筆將其 length／SHA-256 與上述原版 trace 比對後，第一至五筆均不相同，只有第六筆同時符合 length 與 hash。故不能將舊前五筆的視覺轉寫冒稱為原版輸出身分，也不能以其存在推論中文候選已通過內容校對。

私有原圖逐行語意複核後，繁中 DRAFT 的第 3–6 行依新的原版 line order 修訂，避免將時代資訊錯接到「文明的搖籃」子句；來源仍是 `runtime-editorial`，不因這次修訂升格為已核定譯文或接入 runtime。它仍需獨立的 39-cell 寬度核對、文字安全矩形、下一頁清除／失效邊界，及同狀態 A/B，才有資格提 READY 審查。

## 停止線

本階段只解鎖身分資料：`confirmed` 不等於 READY，也不授權 production watcher、catalog request、renderer、字型產物或 Ebitengine layer。第四頁沒有 runtime 覆繪；第一百一十三與一百一十五階段的歷史限制仍保留，後續工作必須從本文件的已證實 identity 繼續，而不可回用已否定的前五筆 visual hash。
