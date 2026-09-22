# 第一百一十三階段：第四頁劇情勘誤與 screenshot-derived DRAFT

日期：2026-09-22
狀態：**勘誤 phase109–112；page4 確認為固定六行劇情畫面，已建立 screenshot-derived DRAFT，runtime identity 仍待重播補證。**

## 勘誤

既有 `phase104-post-return-enter-3/baseline.png` 是第三頁固定劇情；
`phase104-post-return-enter-4/baseline.png` 下方則是另一個固定劇情畫面，包含
全息影像與地球背景。phase109–112 只在目前 dosgolem 重播的 301M 後段抓到
row 24，因而錯誤地把 page4 判成「沒有固定劇情」。該結論保留在原文件中作為
歷史紀錄，本文件是追加勘誤，不覆寫舊收據或舊推論。

目前已知的差異是：phase104 page4 的既有 indexed framebuffer SHA-256 為
`4f9d1bb280724737ca72599c3e7d387c23c076f7e0a8637d8d3ebc9164514bf2`，而從現有
280M state 重新執行三次 Enter 得到 `b3e68d7b8806a418fdd80011939d593fc57337378983dcf890a5d936d2ad97ce`。
這表示原收據與目前重播至少存在 state／時間／路徑差異；不能用目前 row24 trace
否定既有 page4 PNG。

## screenshot-derived DRAFT

只從被忽略的 page4 PNG 讀取六行畫面，保存每行候選原文的 SHA-256、長度、row
與 column；不把原文全文寫入 Git。候選事件位於
`text/story-page4-events.tsv`，繁中候選位於 `text/story-page4.zh-TW.tsv`，
由 `tools/story_page4_catalog.py` 失敗即關閉驗證。

此六筆目前的證據等級是 `visual-transcription`，不是 dosgolem glyph trace
確認；caller、glyph guard、entry/post 步數保持 `unknown/0`，故不得接 runtime。
翻譯來源統一標為 `runtime-editorial`，表示依畫面語意的 DRAFT 意譯，不冒稱
手冊逐字內容。

## 下一個 exact identity 缺口

需找回產生 `4f9d1bb…` page4 frame 的精確輸入 state／版本與停止點，再以
dosgolem glyph trace 取得六行真正的 caller、原文長度／hash、步數與清除邊界。
在此之前，page4 catalog 僅供字型 coverage 與翻譯審查，不得進入 production
overlay；row 24 command/status 仍維持原文與 miss。
