# 第三百二十六階段：v1.2.0 發行（手冊多語、縮小名字字形、連續 F4 切換的推廣片）

日期：2026-10-03
狀態：v1.2.0 已發行（2026-10-03）；內容、打包、冒煙與影片見本文。
推論等級：**已證實**＝重跑測試或腳本並比對輸出；**強推論**＝由程式或截圖推得、未實跑；**未知**＝未量。
發行包不含原版遊戲；本機自用完整版（`-with-data`）只留 `dist-all/`，不推 git、不上傳。

## 1. 決定

- 使用者 2026-10-03：「縮小字 ok 半形英文 ok 然後進版重新打包 release & 完整版 還有推廣影片需要有語言切換」。縮小字（規格 056、057、058）與半形英文字母相同組（另案）接受現況。
- 版本號 v1.2.0；推廣影片以實機錄影版加「同一畫面連續 F4 切換五種語言」；截圖投影片版不重做（畫面是舊字型與舊譯文的截圖，v1.1.0 的 Release 保留它）。

## 2. v1.1.0 之後的內容（已證實，細節見各階段文件與 WORKLOG）

| 項目 | 規格或階段 |
|---|---|
| zh-TW 改台灣來源 `unifont_t`、zh-CN 改預設 `unifont` | 規格 050，phase-313 |
| ja、ko 手冊段落 39 段 | 規格 051，phase-316 |
| 設定視訊模式時覆繪層整層失效 | 規格 052，phase-318 |
| zh-TW 的 3× 手冊 E1，之後擴及 zh-CN、ja、ko | 規格 053、055，phase-317、320 |
| ko 括號助詞依尾音；ko、ja 訊息句內隊員名音譯 | 規格 054，phase-319 |
| ja 74 列、ko 45 列譯文經兩輪模型校對（非母語者） | Issue #41，phase-321 |
| zh-TW 譯文修正 | Issue #37，phase-312 |
| 名字單元縮小；ja 濁音字形；ko 音節互異 | 規格 056、057、058，phase-322、324、325 |

## 3. 打包與冒煙（已證實）

- 標籤 `v1.2.0` 在 Buck repo `0518a26`（含本次推廣片分鏡的修改；標籤建立後、Release 建立前重建過一次）；dosgolem `beca734`（`buck-rogers-cht-output-overlay`，已推送）。
- `tools/package.sh all`（Linux AppImage、Windows zip、macOS zip）rc=0：`ja_check`／`ko_check`／`zh_cn_check` 全部通過；縮小字模可用性檢查（`TestShrinkFontAvailability`，含全形字模兩兩不同的硬性條件）對剛建的字型 PASS 且未 SKIP；外洩掃描三個平台包（254、249、253 個檔案，比對 237 個雜湊、268 個檔名）無命中。
- 以 `BUCKROGERS_WITH_DATA=1` 打出本機自用完整版三平台（含原版與倚天字型），只留 `dist-all/`，不上傳。確認包內有 `original/`、倚天字型與 `local/manual-english.tsv`。
- 發行冒煙：從發行 AppImage 解出（`unsquashfs`，Docker 內）的 `buckrogers-play`，在 Xvfb 內以 3 倍冷開機，五個語言（zh-TW、zh-CN、en、ja、ko）各看標題畫面：`播放(P) 示範(D)`、`播放(P) 示范(D)`、`PLAY DEMO`、`再生(P) デモ(D)`、`재생(P) 데모(D)`。
- 未做：Windows、macOS 的實機執行（Windows 以 Wine 驗收、macOS 只驗結構，同 v1.1.0）。

## 4. 推廣影片（已證實）

- 錄影：用發行 AppImage 內的二進位與 `text/`、`font/`（Unifont），固定輸入腳本重播 11,400 格逐格輸出（5,700 張，3 倍，每 2 格一張；`record.sh`，規格 049）。腳本取自 phase-311 的錄影腳本，只改 `lang` 動作：原本三次（7700、7775、7850）改為 7540、7610、7680、7750 四次，使同一個敘事頁依序切換繁體中文、簡體中文、英文原版、日文、韓文；8100 至 8190 再按四次回到日文，供後面的日文段使用。`lang` 不改變遊戲，手冊查詢題的畫格範圍仍是 3040 至 4040，與重錄前相同。作答只在 ignored 的 `workplace/`，不進 Git。
- 合成：`tools/promo/play-run.sh`（分鏡 `play-segments.tsv`，片頭文字加「F4 即時切換」），48.3 秒、1280×720、30 fps，配樂沿用 DOSBox-X 原版錄音（不同步，只當背景）。
- 檢查：手冊題畫面不在任何一段內；切換段逐格比對（繁體、簡體、英文原版、日文、韓文的敘事文字都正確）。
- 上傳：`BuckRogersCHT-v1.2.0-gameplay.mp4`，SHA-256 `a582f9c147cddb4b779196dc9efdb280038fa3f4a03bc24d90085e18422454ad`。

## 5. Release

https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/releases/tag/v1.2.0 ：三個平台包與實機錄影版推廣片，SHA-256 在發行說明。下載後的 AppImage 與本機檔的 SHA-256 相同；GitHub 顯示的四個檔案的 digest 與本機相同。

| 檔案 | SHA-256 |
|---|---|
| `BuckRogersCHT-v1.2.0-x86_64.AppImage` | `e5bdfa537351066f96c25e738da5ee7c1d0f01f296e9bb2508018281ef59cbb3` |
| `BuckRogersCHT-v1.2.0-win64.zip` | `3ba88371d3e93c9adbc736f27636a5e569eb012cd34bb53f10041e18c92d450e` |
| `BuckRogersCHT-v1.2.0-macos.zip` | `da0e5b51af12df4b191867046d98178e95a692a68132b5cb8c06ad8c01c4ecdc` |
| `BuckRogersCHT-v1.2.0-gameplay.mp4` | `a582f9c147cddb4b779196dc9efdb280038fa3f4a03bc24d90085e18422454ad` |

## 6. 未量與未知

- 縮小字在實機的可讀性（只有合成截圖）；後期名字、手札觸發點、修理表頭欄位的實機觸發。
- Windows、macOS 實機。
- 日文、韓文譯文與音譯規則未經母語者校對。
