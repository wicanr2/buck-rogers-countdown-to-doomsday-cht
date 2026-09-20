# 第 28 階段：功能選單顯示請求純核心

## 狀態

完成

## 本輪目標

以第 27 階段九筆 content-free runtime identity 與正式 `menu.zh-TW.tsv` 為唯一輸入，在
dosgolem `apps/buckrogers` 建立 READY 的選單 catalog／resolver 純核心；真實事件只有完整
精確命中時才產生繁中 `DisplayRequest`。

## 範圍

- 先在 dosgolem 建立獨立 READY 子規格，列明 schema、typed identity、exact-match、失敗
  模式、語意隔離、測試矩陣與權利邊界；證據審查通過後才實作。
- 嚴格解析 `menu-events.tsv` 與 `menu.zh-TW.tsv`，拒絕 BOM、錯誤 header／欄數、重複 key／
  identity、無效數值／SHA／caller、漏譯與孤兒譯文。
- resolver 只接受 `TextEvent`，使用 length／SHA-256、caller、色號與 row／column 完整匹配；
  不使用模糊文字、中文內容、sequence、entry step 或固定延遲作語意判定。
- 由第 27 階段真實 JSON receipt 重播九筆事件，驗證全部產生預期 event／text key 與繁中
  請求；負向案例必須失敗即關閉。
- dosgolem 建立本機 commit、不推送其遠端；專案 main 推送並更新 Issues #5、#8。

## 不在本輪範圍

- 不選 2×／3×、不載入字型、不建立 `xlate.Stamp`、不畫中文或改畫面。
- 不改原版記憶體、輸入、判定、檔名、存檔或 dispatcher 行為。
- 不把九筆選單事件外推到其他文字路徑，也不宣稱玩家可見中文化已完成。

## 驗收條件

- READY 規格在 implementation 前完成，且只核准純 catalog／resolver 子層。
- 正式 TSV 與第 27 階段 receipt 產生九筆請求；兩個 Terran 事件共用 text key 但保有不同
  event key，不發生 identity collision。
- 任一 hash、length、caller、色號、座標或 TSV 關聯被修改時不產生請求或載入失敗。
- `DisplayRequest` 不含輸入、答案、原版指標、記憶體寫入、renderer 或存檔欄位。
- dosgolem 全部正式 packages test／vet、Buck Rogers race detector、專案資料測試通過。
- 兩個工作樹乾淨，專案 main 已推送，相關 Issues 已更新。

## 預定交付物

- dosgolem READY 規格、選單 catalog／resolver 與測試
- 真實第 27 階段 receipt → 九筆 `DisplayRequest` 驗證器或測試
- `docs/re/phase-28-menu-display-request-core.md`
- 選單 DRAFT 整合邊界、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

- 先建立 dosgolem READY 規格 `009-buck-rogers-menu-display-request.md`，再實作
  `MenuCatalog`；沒有越過規格閘門。
- 正式 TSV 固定雜湊通過，Phase 27 真實 JSON receipt 的九筆完成事件全數產生繁中
  `DisplayRequest`；兩個 Terran 事件保留不同 event key 並共用 `race.terran`。
- identity 任一欄位變更均拒絕命中；sequence、SHA／caller 格式、數值、唯一性、漏譯與
  孤兒譯文反例均失敗即關閉。
- Docker 內全部正式 packages test／vet、Buck Rogers race detector 通過；本階段沒有
  選倍率、載入字型或繪圖。
- dosgolem 本機 commit 為 `0be85255d9cd5428c6b55a813410dcacbfd73a4f`，未推送其遠端。
