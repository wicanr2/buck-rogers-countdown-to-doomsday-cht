# 第二十九階段：功能選單執行期顯示請求 watcher

日期：2026-09-20  
狀態：request watcher 子規格 CONFORMED；玩家可見覆繪仍為 DRAFT。

## 結果

dosgolem 現可在原版 `0763:0424` 每筆 guarded post-call 完成時，直接把 content-free
`TextEvent` 送入 exact `MenuCatalog`，產生繁體中文 `DisplayRequest`。不再需要先匯出
Phase 27 JSON 才離線解析，但事件收據仍保留作獨立回查。

實作前先建立 `docs/spec/010-buck-rogers-menu-runtime-request-watcher.md` READY 規格；固定
狀態與全部驗收通過後標為 CONFORMED。watcher 只組合既有 recorder 與 catalog，不複製
identity 邏輯，也沒有 renderer、鍵盤、原版記憶體或機器控制能力。

## 狀態與失敗即關閉

- dispatcher entry 只建立 recorder pending frame，不做 catalog lookup。
- 只有 return address、SS 與 `SP == entry SP + 0x10` 完整通過，使 recorder 新增事件時，
  才做一次 lookup；每筆完成事件最多一筆 request。
- 未知 identity 只增加 catalog miss；不產生空白請求，也不沿用前一筆。
- nil catalog 保留純 recorder 模式，不把每筆事件誤算為 miss。
- 錯誤 SS／SP、重疊 entry、未完成 frame 沿用 recorder 既有 drop／pending 契約。
- `Events()` 與 `Requests()` 回傳副本，呼叫者不能改寫 watcher 內部狀態。

## 正常玩家路徑收據

輸入與第 27 階段完全相同：

- 起點：`workplace/probe/after-bios-space-100m.state`，#99,999,999；
- #100,010,000 排入正常 BIOS Enter；
- 終點：#100,230,000；原版素材唯讀掛載於 `/orig`；
- 收據：被 Git 忽略的 `workplace/phase29/menu-request-receipt.json`。

結果為九筆完成事件、九筆 request、零 drop、零 pending、零 catalog miss。request 順序逐筆
等於正式 `menu-events.tsv`；第 3 筆 `race.option.terran` 與第 9 筆
`race.heading.terran` 各有不同 event key，但共用 `race.terran` text key。

收據每筆 request 只含 `event_key`、`text_key`、`translation_runes`，不含英文原文、繁中
全文、原版 pointer、答案、輸入、renderer 或記憶體寫入。新增
`tools/menu_request_receipt.py` 逐筆核對事件 identity、guard 順序、request key、譯文字數與
零 miss，並拒絕任何額外全文欄位。

## 驗證與交付

- 專案 34 項 Python 資料／收據測試全數通過。
- dosgolem 全部正式 packages `go test ./...`、`go vet ./...` 通過。
- `apps/buckrogers` 與 `cmd/buckrogers-text-receipt` race detector 通過。
- dosgolem 本機分支 commit：`c6a963dafaf3f060a43816f8a6acbda90aa8b7a0`；未推送其遠端。

## 未完成

本階段沒有選 2×／3×、載入 GOLEMFNT、建立 `xlate.Stamp`、清除英文或繪製中文。畫面失效、
反白、text-safe rectangle 與同狀態像素 A/B 尚未通過，因此不得宣稱玩家可見選單已中文化。
