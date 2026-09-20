# 第 24 階段：手冊 runtime watcher 與真實事件收據

日期：2026-09-20  
狀態：完成

## 結論

workplace dosgolem 的 `apps/buckrogers.Watcher` 已把原版 `0763:0424` dispatcher entry
接到第 23 階段 READY Collector／Catalog。只有 return address、`SS` 與
`SP == entry SP + 0x10` 同時吻合，片段才會在 post-call 提交；自然 fall-through、stale
hook、錯誤堆疊與巢狀 frame 都不會產生顯示請求。

此階段仍只觀測並產生 typed `DisplayRequest`，沒有建立 `xlate.Stamp`、沒有選 2×／3×、
沒有送鍵、沒有答案資料、沒有寫原版記憶體，也沒有改變原版驗證與存檔。

## 規格與實作

- dosgolem READY 規格：`docs/spec/008-buck-rogers-manual-runtime-watcher.md`
- 正式 watcher：`apps/buckrogers/watcher.go`
- 固定狀態收據工具：`cmd/buckrogers-receipt`
- 固定狀態工具只使用 dosgolem `internal/state`；沒有把持久化 state 加進 `oracle` 公開 API。
- 正式 runtime 使用 `Watcher.Install(*oracle.Oracle)` 的 `OnCall` 接線；收據工具與正式接線
  共用 `ObserveDispatchEntry`／`ObserveInstruction` 的 guard 核心。
- dosgolem 本機 commit：`38585dcd9e3861b6fa64a1b89dbec19e5a038dd7`；依授權邊界未推送 dosgolem 遠端。

## 真實原版重播

輸入為被 Git 忽略的 `workplace/probe/phase12-before-question.state`，它由第 11 階段正常玩家
路徑建立；state 起點 #266,399,999。原版素材唯讀掛載到 state 保存的 `/orig`，三份 catalog
使用目前正式 `text/` TSV。重播未注入任何按鍵，於 #266,557,246 完成第一題：

| 項目 | 收據 |
| --- | --- |
| begin | #266,486,493，caller `2A33:01ED` |
| 六個 guarded post-call | `2A33:021B`、`0231`、`027A`、`02A5`、`02E2`、`0309` |
| clear | #266,524,821，`026F:029C`；pending 題目維持有效 |
| event key | `manual.page34.deimos_prison.word10` |
| text key | `manual.log.49.deimos_prison` |
| translation 長度 | 73 Unicode 字元 |

收據只記上述 metadata，不保存中文段落、英文完整題目或答案。另以正式 catalog 缺少
`41 / Technical Skills / second` 的單元案例驗證 `catalog-miss`：題目可完成，但請求數為 0。

## 驗證

- watcher 單元測試涵蓋有效 return、自然 fall-through、stale hook、錯誤 caller／SS／SP、
  巢狀 frame 與 catalog miss。
- dosgolem 所有正式 packages（排除被忽略的 `workplace/`）通過 `go test` 與 `go vet`。
- `apps/buckrogers` 通過 race detector。
- 直接執行 `go test ./...` 時，既有 `workplace/fd2-input-parity-20260907` 因三個診斷程式重複
  宣告 `main` 而失敗；正式 packages 已以同一容器、同一原始碼排除該非正式目錄後乾淨重跑。

## 能力邊界

這份收據證明「真實原版事件可決定性產生繁中顯示請求」，不證明繁中已畫上畫面。
玩家可見 overlay、分頁輸入與 2×／3× 產品選擇仍須各自通過規格閘門及同狀態 A/B。
