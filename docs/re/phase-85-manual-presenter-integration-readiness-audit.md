# 第八十五階段：手冊繁中 presenter 整合就緒稽核

日期：2026-09-21  
狀態：完成；新 presenter 規格維持 DRAFT。

## 結論

手冊輸出已具備可驗證的 typed request、原版 lifecycle、正式 36×14／504 layout、2×／3×
RGBA 合成能力，以及可重生的字型需求清單；這些足以設計一個尺度明示的手冊 presenter。
它尚未取得 READY：現有 watcher 不會以帶 generation 的 presentation lifecycle 輸出 begin／clear，
也沒有 14 行手冊 layout adapter；正式 GOLEMFNT 亦尚未依 691 glyph 需求建置並回讀。

使用者本輪確認 host 倍率控制採「先選取，再按套用」（C）。此決定不阻擋手冊 presenter 對
2×／3× 的個別同狀態驗證；host backend 與其餘控制面仍由規格 004 處理。

## 固定輸入與工具

- dosgolem：`workplace/dosgolem` branch `buck-rogers-cht-output-overlay`，commit
  `8bfd5b4e5802f65d428d3fb439196b3c571c002b`，工作樹乾淨。
- 原版狀態：被 Git 忽略的 `workplace/probe/phase12-before-question.state`，起點
  #266,399,999；它由正常玩家路徑建立。
- 原版資料：本機 `workplace/original/BRcdoom` 只讀掛載到 state 預期的 `/orig`；未提交、未複製、
  未輸出其內容。
- 工具：一次性、無網路、`golang:1.24-bookworm` Docker 容器；以目前使用者 UID/GID 執行。
- 正式文字與幾何：`text/manual.zh-TW.tsv`、`text/manual-events.tsv`、
  `text/manual-ordinals.tsv`、`text/manual-overlay-layout.tsv`。

所有位址均為 dosgolem 實模式 `segment:offset`；未混入 IDA 位址空間。

## 重跑正常玩家收據

以 `cmd/buckrogers-receipt` 重播至 #266,600,000，沒有注入按鍵。結果與第 24 階段一致：

| 項目 | 已證實收據 |
| --- | --- |
| 題首 begin | #266,486,493，`2A33:01ED` |
| 局部 clear | #266,524,821，`026F:029C`；pending 仍有效 |
| 終端 post-call | #266,557,246，`2A33:0309` |
| 唯一 request | generation 1、`manual.page34.deimos_prison.word10`、`manual.log.49.deimos_prison`、73 runes |
| 停止步數 | #266,557,247 |

收據只含事件鍵、文字鍵、generation 與 rune 數，不含英文完整題目、中文段落全文或答案。

## 程式介面稽核

| 項目 | 分級 | 發現 |
| --- | --- | --- |
| request／語意隔離 | 已證實 | `manual.go` 的 `DisplayRequest` 不含答案、輸入或 renderer 欄位；`watcher.go` 不寫機器狀態。 |
| 新題移除時機 | 已證實 | `Collector.BeginEntry` 在精確題首即清空 visible；第 18 階段的錯答路徑證實不能等待整面清除。 |
| pending clear | 已證實 | `Collector.ClearEntry` 只使 completed visible 失效，保留 pending；正常第一題也在 terminal `word?` 前遇到 clear。 |
| xlate 可用能力 | 已證實 | `Layer` 可用 `Replace`／`Clear`／逐格指紋失效，並從 indexed framebuffer／palette 輸出 RGBA；不回寫 VRAM。 |
| 現成手冊 renderer | 已證實為否 | `RuntimeMenuOverlay` 是 single-row menu identity adapter，不載入手冊 layout、無 14 行 builder、無手冊 watcher 接線。 |
| 生命週期輸出介面 | 未知，阻擋 READY | `Watcher.Observations()` 的 begin／clear 沒有 generation，且沒有 callback／queue；只靠外部陣列輪詢會把未表達的時序假設帶入 presenter。 |
| 正式字型 binary | 未知，阻擋 READY | `catalog_font.py chars` 已由正式 22 筆譯文重生 691 碼點需求，SHA-256 為 `dc656f…6667f`；但尚未建立、載入並回讀相應 GOLEMFNT。 |

`text/manual-overlay-layout.tsv` 已確認正文 anchor `(16,72)`、每行 36 個 logical cell、共 14 行；
以一行一 stamp 的方式可以在 xlate 層保留每格的失效／定色行為。這是可實作的設計推論，
不是已完成畫面覆繪。

## 退出與後續

第八十六階段應先將 lifecycle event API 與手冊 row builder 寫成 DRAFT／READY 規格及負向測試；
不能直接沿用選單 presenter，不能藉 host 面板事件、DOS mouse 或鍵盤捷徑繞過 lifecycle。
正式手冊覆繪仍須在 READY 後實作，再以正常第一題與答錯重抽在 2×／3×做 A/B 收據。
