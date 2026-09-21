# 第五十八階段：執行期繁中覆繪證據固化與交接

狀態：完成

## 目標

將第 57 階段已通過實跑的 2×／3× dosgolem 輸出端繁中覆繪，完整固化為可追溯的
CONFORMED 規格、研究紀錄、目前狀態與工作歷程，完成全面測試、兩個工作樹提交、專案
`main` 推送與 GitHub Issue 回寫。

## 範圍

- 保留首輪舊 stamp 失敗與 spec 退回 DRAFT 的訂正歷史。
- 記錄 `026F:029C` 清除矩形、`xlate.Layer.Clear`、同原點 `Replace` 與 adapter 接線的證據邊界。
- 固定四份 fresh-scratch 正常路徑收據：18 events、14 requests、4 dynamic misses、14 actions，
  終態只保留 `roster.add_prompt`。
- 驗證同倍率決定性、原版 framebuffer／FileOps／writes／存檔同狀態、安全矩形差異與
  動態姓名列不受覆繪。
- 執行專案全套測試與 dosgolem 正式套件 test／vet／相關 race detector。
- dosgolem 只提交於本機 `buck-rogers-cht-output-overlay` 分支；專案提交並推送 `main`，
  然後回寫相關 GitHub Issues。

## 不在本階段

- 不替使用者選定 2× 或 3× 產品預設。
- 不擴張到尚未有 exact catalog 的畫面，不翻譯動態姓名，不改原版語意或手冊驗證。
- 不推送 dosgolem 遠端，不發佈 Release 或原版素材。

## 完成條件

1. spec 035 的 DRAFT 退回、READY 復審與 CONFORMED 收據完整且與實作一致。
2. 第 57 階段研究紀錄已建立並掛入 `docs/re/README.md`；`CONTEXT.md` 與 `WORKLOG.md` 已更新。
3. 專案與 dosgolem 的全部適用測試通過，差異檢查、權限／root-owned 檢查與 Docker 清理通過。
4. dosgolem 本機分支與專案 `main` 各有一筆可追溯提交；專案 `main` 已推送。
5. GitHub 相關 Issues 已以收據、commit 與未決邊界回寫，遠端 repository 仍為 private。

## 退出條件

- 任一全套測試或同狀態檢查失敗時，不得宣告 CONFORMED；回到 DRAFT 保留失敗證據。
- 若提交差異含原版、手冊、字型二進位或其他受限素材，停止推送並修正邊界。
