# 第九十四階段：倚天字型本機建置與對齊 prototype

狀態：完成（DRAFT；待使用者選定對齊）

## 目標

依使用者確認的已購買光碟授權，將倚天 15 點字模做為**本機遊戲**的正式候選來源，完成可丟棄的
16×15／8×15→16×16 `GOLEMFNT` 對齊 prototype 與真實手冊覆繪比較。此階段要讓使用者依實際畫面
選定對齊策略；在選定前不接入正式 runtime。

## 已確認前提

- 使用者已明確授權：其以前購買的倚天字型可直接放入本機遊戲。此授權解鎖本機讀取、轉換與使用，
  不擴張為 GitHub 或公開發行包的再散布許可。
- `ET353S/FILES/STDFONT.15`、`SPCFONT.15`、`ASCFONT.15` 已覆蓋正式手冊 691 glyph；候選雜湊、
  Big5 分區與空白字元例外見 spec 007。
- `RuntimeManualOverlay` 只接受 16×16／32-byte glyph，正式手冊正文保持 `[7,312)×[72,184)`、
  36×14、504 字，2×／3× 都是正式支援倍率。

## 範圍

- 在 Docker 從使用者本機候選唯讀提取正式 691 glyph，將原生 16×15 CJK 與 8×15 ASCII 依明示、
  可重現的 padding 方案轉為 16×16；所有候選 `GOLEMFNT`、PNG 與 manifest 僅寫入被忽略的
  `workplace/phase94/`。
- 以同一個固定手冊 state、同一份 catalog、同一 scale 產生至少兩個垂直對齊 variant 的並列 RGBA
  對照；驗證每 variant 的 header、691 glyph 回讀、缺字、文字安全矩形 containment 與矩形外零差異。
- 將使用者「已購買光碟可供本機遊戲使用」的決定與公開散布限制記入 current truth／DRAFT spec；
  不以不存在的授權檔重新阻擋本機 use，也不宣稱公開散布權。

## 不在本階段

- 不把倚天原檔、GOLEMFNT、字模圖片、完整媒體、完整 README 或授權文字加入 Git、GitHub Issue、
  Release 或公開封包；不建立公開散布結論。
- 不接 `RuntimeManualOverlay` 到 command／遊戲 loop、不改 DOS VRAM、BIOS input、答案、存檔、
  原版 EXE 或 host frontend；不把 prototype 視為玩家路徑中文化完成。
- 不代替使用者決定 CJK／ASCII 的 16th-row、水平或垂直對齊；prototype 只縮小決策，不成為正式規格。

## 完成條件

1. 至少兩個真實倚天對齊 variant 可由固定來源、雜湊與 formal 691 glyph 清單決定性重生，且所有產物
   都只在 `workplace/phase94/`。
2. 各 variant 的 `GOLEMFNT` 皆為合法 16×16／691 glyph、全量回讀，並通過 2×／3× 手冊幾何與
   矩形外零差異驗證。
3. 提供同狀態、同倍率的可丟棄畫面對照及明確取捨，讓使用者選擇對齊策略；選前維持 DRAFT。
4. 文件、測試、main 推送與 GitHub Issue 回寫完成；dosgolem 本機 branch 不推送，正式 runtime 不宣稱完成。

## 完成收據

- Docker 從已固定 SHA-256 的 `STDFONT.15`、`SPCFONT.15`、`ASCFONT.15` 重生 `bottom-pad` 與
  `top-pad` 兩份本機 `GOLEMFNT`。兩者皆為 25,583 bytes、16×16、691 glyph，並逐字回讀；其
  SHA-256 分別為 `4ea9692120712c5666de359e84ff855e668e82086aae2d9dc23fa1096b790a84` 與
  `78c10dec8055110764013007899c4455b91256a78f94e212294ac9c51c01364e`。產物、預覽與重生器皆只在
  被忽略的 `workplace/phase94/`。
- 以固定原版 state 從 #266,399,999 重生至 #266,557,247，畫面雜湊為
  `d53948dc2a75e255691e5c44287fe2e76cf7a630196f6d1546ac18c4730bd495`，並以已證實的
  `manual.page34.deimos_prison.word10`／`manual.log.49.deimos_prison` 顯示請求（request）透過
  `RuntimeManualOverlay` 作四張 2×／3×預覽。每張缺字為零，清除矩形外變更為零。
- 原版正文區原本全黑，現有 presenter 尚無可取樣的本地前景色。為讓本階段只比較字型對齊，預覽僅在
  `Layer.Frame` 的私有取樣副本中每行放入一個原版題目區已見的色盤索引 10；`Draw` 仍以未改的
  原版 VRAM 為基準（baseline），沒有寫入 DOS、接入迴圈（loop）或宣稱正式配色已完成。正式繪製器
  （renderer）仍須有經規格
  審查的前景色來源。
- 使用者尚未選定「底部補空白列」或「頂部補空白列」，因此對齊與正式解析器（parser）／執行期（runtime）仍為
  DRAFT；本階段只完成可逆的證據與選擇素材。

## 退出條件

- 若真實字模或轉換後 glyph 不通過 format／coverage／containment，記錄精確缺口並停止，不以 fallback
  或近似字型取代倚天。
- 若 prototype 已完成但使用者尚未選定對齊，結束本階段的可逆證據工作並保持 DRAFT；後續 production
  接線另開階段。
