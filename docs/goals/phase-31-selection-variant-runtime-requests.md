# 第三十一階段：反白 variant 的執行期繁中請求

## 狀態

完成

## 本輪目標

將第 30 階段已由兩次正常 Down／Up 重播證實的三筆新 selection identity 納入正式
`menu-events.tsv` 與 dosgolem exact `MenuCatalog`，使 Enter→Down→Up 的 13 筆 guarded
post-call 全部直接產生正確 normal／selected 繁中 `DisplayRequest`。

## 範圍

- 先在 dosgolem 建立獨立 READY 子規格，固定新增 identity、event key、共用 text key、
  selection 順序、失敗模式與 13-request 驗收，再修改正式資料或程式驗證。
- 擴充 `menu-events.tsv` 為 12 個唯一 identity：既有 9 筆，加 normal Terran、selected
  Martian、normal Martian；回選 selected Terran 必須重用既有 identity，不複製 catalog row。
- `race-selection-events.tsv` 明列每筆 runtime event 對應的正式 event key；Down／Up 四筆中
  可重複使用同一 catalog identity。
- 同步擴充 text-safe rectangle 一對一資料；選項／selection variants 共用已證實的 logical
  清除矩形與 col 3 draw anchor。
- 調整 Phase 27／29 的九事件 verifier，使它們驗證明確的初始九筆子序列，不把新增 inventory
  誤當舊收據缺事件，也不得讓任意截斷收據通過。
- 由同一固定狀態重生 catalog-enabled Enter→Down→Up 收據，要求 13 events、13 requests、
  零 drop／pending／catalog miss，並逐筆核對 event／text key。
- dosgolem 建立本機 commit、不推其遠端；專案 main 推送並更新 Issues #5、#8。

## 不在本輪範圍

- 不選 2×／3×、不載入字型、不建立 `xlate.Stamp`、不清除或繪製畫面。
- 不處理滑鼠 selection、確認種族、角色建立 transaction、其他選單或訊息捲動。
- 不以 text key、座標或色號單欄模糊命中；所有 request 仍須完整 identity。

## 驗收條件

- 正式 inventory 恰有 12 個唯一 identity／event key；所有 text key 有翻譯且無孤兒。
- 第 30 階段四筆 selection 事件依序映射：normal Terran、selected Martian、normal Martian、
  既有 selected Terran；不新增重複 identity。
- 初始 Enter 收據仍嚴格驗證九筆，Enter→Down→Up 收據嚴格驗證 13 筆 request，零 miss。
- 任一新增 hash、caller、色號、座標、event key、text key 或順序變更均失敗即關閉。
- dosgolem 全部正式 packages test／vet、相關 race detector、專案資料測試通過。
- Docker 清理與擁有權檢查正常；兩個工作樹乾淨，main 已推送，Issues #5、#8 已更新。

## 預定交付物

- dosgolem READY／CONFORMED selection variant catalog 規格與正式測試
- 擴充的事件、selection lifecycle、text-safe rectangle 資料與 verifier
- catalog-enabled 13-request 真實收據
- `docs/re/phase-31-selection-variant-runtime-requests.md`
- 選單覆繪 DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

2026-09-20 完成。正式 inventory 已擴充為 12 個唯一 identity；固定 Enter→Down→Up
兩次重生均得到逐位元相同的 13-event／13-request 收據，且零 drop、pending、catalog miss。
舊九事件收據仍嚴格核對前九筆。專案 41 項 Python 測試、正式收據 verifier、dosgolem
正式 packages test／vet 與 Buck Rogers race detector 全數通過。dosgolem 變更只建立本機
commit `79ecc2b9585f02339eef181ecb88b752bee4c2aa`，未推其遠端；本階段沒有選
2×／3×，亦未接 renderer。
