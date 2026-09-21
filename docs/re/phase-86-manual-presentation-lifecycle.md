# 第八十六階段：手冊 presentation lifecycle 接線

日期：2026-09-21  
狀態：完成；dosgolem lifecycle 子規格已 CONFORMED，手冊 renderer 仍未實作。

## 結論

dosgolem 手冊 watcher 現在可輸出只含 presentation metadata 的 `ManualPresentationEvent` queue。
精確題首產生 `begin`、處於 manual pending 或 visible context 的 exact clear 產生 `clear`、只有
exact catalog hit 產生 `request`；三者都帶 generation。queue 不持有 machine、oracle、renderer 或
input reference，accessor 回傳 value-copy。

此實作不畫中文、不建字型、不改原版 indexed framebuffer、VRAM、DOS／BIOS input、答案驗證、
存檔或 host UI。它只解除手冊 presenter 所需 lifecycle 接線缺口；14 行 RGBA presenter 與字型仍由
規格 005 的下一個 READY gate 管理。

## 固定來源與版本

- dosgolem branch：`workplace/dosgolem` 的 `buck-rogers-cht-output-overlay`。
- lifecycle 實作 commit：`47397ebd18e63a0daa4cb54bd593c5fbfd549ada`，僅留在本機 branch，未推送。
- dosgolem 規格：本機 `workplace/dosgolem/docs/spec/216-buck-rogers-manual-presentation-lifecycle.md`，
  狀態 CONFORMED；該工作樹依權利與分支規範不在本 repository 散布。
- 正常玩家 state：被 Git 忽略的 `workplace/probe/phase12-before-question.state`，起點 #266,399,999；
  原版資料只讀掛載為 `/orig`，未輸出或提交其內容。
- 工具：`golang:1.24-bookworm` 的一次性無網路 Docker 容器，以目前使用者 UID/GID 執行。

所有 DOS 位址皆為 dosgolem 實模式 `segment:offset`；沒有混入 IDA 線性位址。

## Queue 契約與失敗即關閉

| 事件 | 已證實來源 | queue 行為 |
| --- | --- | --- |
| `begin` | `2A33:01ED` 的精確題首 | 追加 step、generation；未來 presenter 可先移除舊段落。 |
| `clear` | `026F:029C`，且 collector clear 前仍 pending 或 visible | 追加同 generation；不清除 collector pending，沒有 active manual context 時不追加。 |
| `request` | `2A33:0309` 的 guarded post-call 與 exact catalog hit | 追加同 generation 的 `DisplayRequest`；catalog miss、nil catalog、poison、錯誤 guard、nested／stale frame 均不追加。 |

`ManualPresentationEvent` 只有 step、kind、generation 與 value-type `DisplayRequest`。後者仍只含
generation、event key、text key、translation；沒有英文原文、答案、輸入、機器狀態或 renderer。
metadata receipt 只投影 request 的 key 與 rune count，不序列化 translation。

## 正常玩家重播

以與第 24／85 階段相同 state、TSV、唯讀 `/orig` 重播至 #266,600,000，沒有注入按鍵：

| 項目 | 收據 |
| --- | --- |
| 停止步數 | #266,557,247 |
| 原有 request | generation 1、`manual.page34.deimos_prison.word10`、`manual.log.49.deimos_prison`、73 runes |
| presentation queue | #266,486,493 begin；#266,524,821 pending clear；#266,557,246 request；三筆皆 generation 1 |

移除新增的 `presentation_events` 後，既有 metadata request 與第 85 階段相同。程式碼只有 observer
value state 與 JSON projection，沒有任何 machine write／input API；本階段的同 state 結論僅限這條
metadata lifecycle，不宣稱中文字幕像素已完成。

## 驗證

- `go test ./apps/buckrogers` 通過；新測試涵蓋 pending／visible clear、catalog miss、無 manual context
  clear、guard failure、nested／stale frame，以及 queue 與內嵌 request 的 defensive copy。
- `go vet ./apps/buckrogers ./cmd/buckrogers-receipt` 與 `go test -race ./apps/buckrogers` 通過。
- 本專案 154 項 Python 測試、`manual_overlay_layout.py` 與 `catalog_font.py lint` 均通過；原版與
  手冊掃描均未進 Git。
