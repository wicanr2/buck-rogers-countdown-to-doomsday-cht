# 第九階段：dosgolem 通用繁中覆繪基礎

日期：2026-09-20  
狀態：通用 package 已移植並通過正式 package 回歸；dosgolem 遠端分支尚未推送。

## 範圍與來源

目標工作樹為 `workplace/dosgolem/`，分支 `buck-rogers-cht-output-overlay`，移植前基準
`d9c0c27ca9af8239c7e96272a7165e03d7da04bf`。來源是 psychic-war 的 dosgolem 工作樹
`psychic-war/r5-text` commit `e51587059a89bf250fba9dc6cd3f7e3644478482`。

來源 `xlate` 歷史不是一個可安全整體 cherry-pick 的 commit：首筆 `cf95985` 同時修改
`oracle` 與 `cmd/step`，其後另有 Frozen、Scroll、watcher、部分重疊、逐格失效、舊快照、
錨定格及 SwapColors 修正。因此本階段只逐檔移植最終 `xlate/` package、規格 202／203
與測試；沒有搬入 psychic-war 位址、譯文、狀態、字型或 adapter。

目標分支 commit 為 `b33cfbf`。`xlate/` 與來源相比，程式碼唯一刻意差異是 package 註解
移除 `apps/psychicwar` 例名；規格 202 的前置說明改成此分支可獨立成立，並記錄完整來源
commit。規格索引已同時加入 202／203，沒有形成無入口文件。

## 已移植能力

- `GOLEMFNT` 載入與錯誤檢查；
- 固定格排版與 overflow；
- stamp 定色、逐格指紋、透明格、部分重疊與錨定格整筆失效；
- `Frozen`、捲動、`SwapColors`、缺字回呼；
- snapshot／restore、舊快照相容、字型名稱失敗即關閉；
- `LineTracker`；
- 以畫面色號圖塊觸發的 watcher。

這些都是遊戲無關能力；Buck Rogers 的 `0763:0424`、`026F:029C` 與翻譯鍵仍只存在本專案
DRAFT／研究證據，尚未接入 dosgolem production path。

## Docker 測試收據

- image：`golang:1.24-bookworm`，實際 Go `1.24.13 linux/amd64`；無網路、UID/GID 1000:1000。
- `go test -count=1 -json ./xlate`：全部通過，package `ok`，0.006 秒。
- `go test -count=1 ./...`：所有正式 package 與 `xlate` 通過；唯一失敗是被忽略的歷史研究
  目錄 `workplace/fd2-input-parity-20260907`，其 `lockprobe.go`、`probe.go`、`seekprobe.go`
  同包各宣告 `main`。完整 JSON 收據 SHA-256：
  `ad1e33271d933c9cacd850f654ea9c7f9cdcac2f62b1aa6d6ddf7728d4910542`。
- 以明確 package roots 排除 research workplace 後重跑：根 package、`apps/...`、`cmd/...`、
  `internal/...`、`oracle`、`runtime/...`、`xlate` 全數 exit 0；CPU 語料 77.104 秒。

歷史 research workplace 的多 `main` 不是本輪回歸，也未為求全綠而改寫其他專案收據。

## 已知限制與下一閘門

來源規格 202 的 `Draw` 目前要求輸出倍率為 3 的倍數；因此它可直接支援第八階段 B 案，
但不代表已替使用者選定 3×。若使用者選 A（2×），必須先提出並審查一份「明示
`GlyphScale` 時允許非 3 倍」的規格修訂，再改通用 package；不得在 adapter 偷繞限制。

向 `https://github.com/wicanr2/dosgolem.git` 推送專用 branch 的操作因尚無明確外傳授權而被
安全審核拒絕。本機 commit 完整保留；沒有繞過審核。中文化專案的 private repo 仍照本輪
授權推送文件與指標。

