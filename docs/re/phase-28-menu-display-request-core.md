# 第二十八階段：功能選單顯示請求純核心

日期：2026-09-20  
證據等級：正式 TSV schema 與固定狀態事件為已證實；玩家可見覆繪仍是 DRAFT。

## 結果

dosgolem 的 `apps/buckrogers` 現有獨立 `MenuCatalog`。它嚴格載入
`text/menu-events.tsv` 與 `text/menu.zh-TW.tsv`，只在完整 `TextEvent` identity
精確命中時回傳繁體中文 `DisplayRequest`。此層不讀英文全文、不繪圖、不送輸入，也不
修改原版記憶體或狀態。

READY 契約位於 workplace dosgolem：
`docs/spec/009-buck-rogers-menu-display-request.md`。它在程式實作前建立，固定輸入雜湊為：

- `menu-events.tsv`：`38bc0fa693fa5ee4bed3209548a0dc67c1270b28657f0801e42645b70fd370e9`
- `menu.zh-TW.tsv`：`ca3319830adb7b34a048b498d8d0466b38b8fb6f418e5244a3a467e77ea68077`

## 精確比對邊界

identity 由原文字節長度、原文 SHA-256、DOS runtime caller、背景色、前景色、row 與
column 組成。`sequence` 與執行步數不參與匹配；步數只用來拒絕尚未完成 guarded
post-call 的事件。沒有完全命中時失敗即關閉，不退回模糊字串、單一 caller、座標或固定
延遲。

Terran 選項與 Terran 標題是兩個不同 event key，因畫面 identity 不同而可分辨，但合法
共用 `race.terran` 翻譯鍵。選單沒有手冊題目 generation，因此其請求明示
`Generation=0`，不得拿來驅動手冊生命週期。

## 驗證收據

- 第 27 階段固定狀態 `workplace/phase27/menu-receipt.json` 的九筆真實完成事件，全數解析
  成非空 event key、text key 與繁中譯文。
- 正向測試確認九筆正式 TSV 與兩個 Terran event；負向測試涵蓋未完成事件與 identity
  七個欄位逐一變更。
- 載入反例涵蓋 sequence 跳號、雜湊／位址大小寫、數值越界、重複事件鍵、重複 identity、
  缺少／孤兒／重複翻譯；共用翻譯鍵則明確允許。
- Docker 內 `go test ./...`、`go vet ./...` 與 `go test -race ./apps/buckrogers` 全數通過。
- workplace dosgolem 本機分支 commit 為
  `0be85255d9cd5428c6b55a813410dcacbfd73a4f`；依授權邊界未推送 dosgolem 遠端。

## 尚未完成

本階段沒有載入字型、建立 `xlate.Stamp`、清除原文矩形或產生玩家可見畫面。2×／3× 仍是
使用者尚未決定的產品取捨；在倍率、矩形失效及同狀態畫面 A/B 通過前，選單 production
整合規格維持 DRAFT。
