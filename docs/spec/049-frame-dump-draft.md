# 049 — 自動模式畫格輸出（實機錄影用）

狀態：**READY**（2026-10-01，一輪獨立審查，必修 6 項與建議 8 項已併入本版）；已實作並驗收（dosgolem `0bc270a`，[phase-311](../re/phase-311-frame-dump.md)）。
日期：2026-10-01
Issue：#35（留言追蹤）
決定：使用者 2026-10-01 要求「實際遊玩錄影版推廣影片」。前端沒有錄影功能，自動模式的 `-shot` 只輸出結束時的一格。
前置：規格 040（前端與 F4）、`cmd/buckrogers-play` 自動模式（`-frames`、`-script`、`-wav`）。

## 1. 為什麼要做

推廣影片要的是遊戲實際跑出來的連續畫面。三種取法比較：

| 做法 | 問題 |
|---|---|
| 互動模式加螢幕擷取（x11grab） | 畫格時間靠牆鐘；主機忙時掉格，影片速度與遊戲不一致。音訊要另外錄。 |
| 自動模式在腳本裡按 F12 | 腳本只有遊戲鍵與 `help`、`scale`、`lang`、`blur`、滑鼠動作，沒有截圖動作；F12 的截圖只在互動模式的 `hostInput`（`frames == 0`）處理。 |
| 自動模式每隔 N 格輸出一張 PNG | 畫格以遊戲畫格計，與主機速度無關；輸入由 `-script` 固定，可重跑；同一次執行可用 `-wav` 取得音訊（同步條件見 §3.6）。 |

採第三種。它只是把 `-shot` 的最後一格擴成「每 N 格一張」，不改任何遊戲或覆繪路徑。

## 2. 介面

| 旗標 | 預設 | 語意 |
|---|---|---|
| `-frame-dir DIR` | 空（關閉） | 須同時給 `-frames` > 0，否則用法錯誤。`DIR` 在啟動時（`RunGame` 之前）以 `MkdirAll` 建立；已存在且非空則報錯（避免新舊畫格混在一起）。腳本含 `scale` 動作時用法錯誤（見 §3.3）。 |
| `-frame-every N` | 未給（內部以 -1 表示） | 只在有 `-frame-dir` 時允許給；沒給 `-frame-dir` 卻給了，用法錯誤。範圍 1 至 60，超出用法錯誤；未給等於 2（主機 60 Hz 的一半，30 fps）。 |

旗標驗證抽成純函式 `checkFrameDump(frames int, dir string, every int, script map[int][]scriptAction) (effectiveEvery int, err error)`，供單元測試。`-frames` 為負值時（既有行為把它當成跑 1 格的自動模式）在 `-frame-dir` 存在時一併拒絕。

寫入時點：`finishFrame` 開頭，早於其結束判斷。`finishFrame` 在 `frames == 0` 時早退，因此新增獨立守衛 `frameDir != ""`。`Update` 的兩條路徑（一般與說明頁開啟）都經過 `finishFrame`，所以說明頁的畫格也輸出。`g.frame` 是畫格編號（第一個 `Update` 為 1）；`g.frame % every == 0` 時寫 `DIR/frame-%08d.png`（補 `g.frame`，8 位數；以遊戲畫格編號命名，方便依畫格範圍剪輯，跳號是正常的）。內容是 `g.composed()`，與當時玩家看到的相同。PNG 用 `png.BestSpeed`。

邊界行為：

- `Advance` 回報 `PhaseStopped` 的那一格直接回傳 `ebiten.Termination`，不經 `finishFrame`，該格不輸出（與 `-shot` 一致）。
- `composed()` 回 `ok == false`（尚無畫格，通常在開機最初幾格）：略過這一格，不報錯、不佔編號。這與 `-shot`（報錯）不同，因為連續輸出必然涵蓋開機。
- 寫檔用 `O_CREATE|O_EXCL`；任何一步失敗（編碼、寫入、關閉）刪除該半成品 PNG 並讓自動執行以錯誤結束。已完整寫入的畫格保留。
- 結束時印一行 `buckrogers-play: frame-dump dir=… every=N count=C first=F last=L`（`first`、`last` 為第一張與最後一張的畫格編號；沒有任何輸出時 `count=0`，`first`、`last` 為 0），供對齊音訊。

## 3. 不變量

1. 開關不改變遊戲：同一腳本與同一 `-frames`，有無 `-frame-dir` 的 `memory_sha256`、`cpu_sha256`、`indexed_sha256`、`palette_sha256`、`compose_sha256`（`reportCompose` 已印）、`-shot` 的 RGBA 與 `-wav` 內容逐位元組相同。`DebugSummary` 的計數（`Compose` 內的 `skips`、`resets` 等）會因多一次 `Compose` 而不同，不在此列。
2. `Compose` 次數不影響輸出：同一腳本以 `-frame-every 1` 與 `-frame-every 3` 各跑一次，兩次共有的畫格（編號為 3 的倍數）逐位元組相同。這同時檢查 `Compose` 的副作用沒有滲進後續畫面。
3. 畫格尺寸是當時 `320*scale` × `200*scale`。`scale` 動作在 `apply` 就生效，輸出尺寸會在中途改變，所以有 `-frame-dir` 時拒絕含 `scale` 的腳本。
4. 輸出畫格與同一畫格的 `-shot` 像素相同：`-frames` 為 `every` 的倍數時，最後一張 PNG 解碼後的像素值等於 `-shot` 的裸 RGBA（先解碼再比，不比檔案位元組）。
5. 檔名只含畫格編號，不含牆鐘；同一腳本、同一建置與 Go 版本重跑，PNG 位元組相同。
6. 與 `-wav` 同步的條件：說明頁開啟的畫格 `Advance` 與 `renderAudio` 都被跳過，畫面有輸出、音訊沒有樣本。錄影腳本不要用 `help`；用了就接受音畫漂移（本規格不修）。沒用 `help` 時，WAV 從第 1 格起連續收樣本，不因輸出略過的開機畫格而缺漏；畫格編號 `f` 對應 WAV 時間軸約 `f / 60` 秒（每格樣本數隨該格執行的機器步數而變，總長以實測核對，記入證據）。

## 4. 驗收

1. 單元測試（不需要原版）：`checkFrameDump` 的錯誤矩陣（沒給 `-frames`、負 `-frames`、`-frame-every` 超出範圍或沒給目錄、腳本含 `scale`、目錄非空）；檔名格式；`every` 的倍數規則；寫檔失敗刪除半成品；`ok == false` 略過。
2. 整合（需要原版，缺檔 skip；依 `AGENTS.md` 公開程式在原版缺席時明確跳過）：
   - `-frames 12 -frame-every 3` 產 4 張，編號 3、6、9、12；結尾 `count=4 first=3 last=12`（開機最初幾格若無畫格，`first` 可能較大，以實測為準並記入證據）。
   - 腳本含 `help` 時，說明頁開啟那一格的 PNG 與同一格無 `help` 的 `Compose` 不同。
   - 不變量 1、2、4、5。
3. 證據寫入 `docs/re/phase-311-frame-dump.md`，含磁碟用量實測（單張大小、每分鐘 30 fps 的總量）。

## 5. 邊界

- 不做 `-video`（不內建編碼；影片由外部工具合成）。
- 不輸出音訊（`-wav` 已有；互動模式的 `-wav` 行為不變，本規格不處理）。
- 畫格含原版美術。`DIR` 放在 `workplace/`（已 gitignore），不進 Git、不進發行包（`AGENTS.md`）。
- 編號 8 位數足夠 99,999,999 格；實務上受磁碟限制，`-frames` 不另設上限。
- 影片取材的內容限制（手冊題畫面、答案、授權）不屬本規格，由推廣片流程負責。
