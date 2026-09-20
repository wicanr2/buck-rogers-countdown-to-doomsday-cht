# 第三十一階段：反白 variant 執行期繁中請求

## 結論

第 30 階段由正常方向鍵路徑證實的三個新 selection identity，已加入正式
`text/menu-events.tsv`。dosgolem 的 exact `MenuCatalog` 現在載入 12 個唯一 identity；固定
Enter→Down→Up 重播的 13 個 guarded post-call 全部產生對應 `DisplayRequest`，沒有模糊
比對、漏接或重複 catalog row。

證據等級：上述 catalog 對應、事件順序與 request 結果為**已證實**；玩家可見繁中覆繪、
2×／3× 倍率與其他選單的適用性仍是**未知／未實作**。

## 輸入與位址空間

- 原版輸入、狀態與工具版本沿用第 30 階段收據；動態位址均為 dosgolem runtime
  `segment:offset`，不可當成 IDA 線性位址。
- 正式事件清冊 SHA-256：
  `973a6a1e247e7d9e16518a1a66266f340666d32e785f3f6f6652a890e830da2e`。
- selection lifecycle SHA-256：
  `055f77591bcc4fc238138c59e837be4aeeae625c7f9970105242374773176828`。
- text-safe rectangle SHA-256：
  `3e37efcae4222ffb9ea11b19ea93dc5b016e11df974253d58da797365f6c982f`。

## Exact identity 擴充

既有 sequence 1–9 不變；新增三筆為 normal Terran、selected Martian、normal Martian。
Up 最後的 selected Terran 重用既有 `race.heading.terran`，因此 inventory 是 12 筆而非 13
筆。穩定 event key 不作破壞性改名；normal／selected variants 可共用繁中 text key，但
仍以長度、原文 SHA-256、caller、色號及 row／col 完整 identity 精確解析。

`race-selection-events.tsv` 新增 `event_key` 後，四步依序為：

1. `race.selection.normal.terran`
2. `race.selection.selected.martian`
3. `race.selection.normal.martian`
4. `race.heading.terran`

## 真實重播收據

同一 #100,600,000 終點的 Enter→Down→Up 排程重生兩次，兩份 JSON 逐位元相同，SHA-256
均為 `eb619b596f312aa61a2e5ea335c3c57157a0cd7cb2cf6350e03aaaaf03748b2f`。每份均有 13 個
完成事件與 13 個 request；recorder drop、pending、catalog miss 都是零。request 10–13
依序對應上述四步，且收據只保存 event key、text key、譯文字數與必要 metadata，不保存
原文或譯文全文。

Phase 27／29 的既有收據仍被要求恰為九筆，逐筆核對擴充 inventory 的 sequence 1–9；
verifier 不會因 catalog 增長而放寬成任意前綴。

## 驗證與限制

- 專案 41 項 Python 單元測試、舊九事件／九 request、新 selection lifecycle 與新 13-request
  收據 verifier 全數通過。
- dosgolem 排除既有非正式 `workplace/fd2-input-parity-20260907` 草稿後，全部正式 packages
  的 test／vet 通過；`apps/buckrogers` race detector 通過。
- 初次直接 `go test ./...` 只因該既有草稿同一 package 含三個 `main` 失敗，不是產品或
  Buck Rogers 缺陷；正式驗證明確排除 `workplace/`。
- 本階段未載入字型、未清除原文、未繪製繁中，也未替使用者選擇 2×／3×。因此不能宣稱
  玩家可見中文化已完成。
- dosgolem 變更保存在指定本機分支 commit
  `79ecc2b9585f02339eef181ecb88b752bee4c2aa`，依授權未推送其遠端。
