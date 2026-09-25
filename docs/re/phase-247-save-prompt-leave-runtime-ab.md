# 第二百四十七階段：儲存詢問離頁正式 A/B

日期：2026-09-26  
狀態：**已證實／每組單次重播。** 對應[規格 026](../spec/026-save-prompt-leave-handoff-draft.md)。

## 輸入

- 本機 dosgolem fork `c4aa3ee`（confirm 路徑完成後交接），乾淨 clone 建置，
  `vcs.modified=false`，runner SHA-256 `9d35e976…3a79da853`。
- 起點 `bbody.state`（`BUCK`，508.4M）。鍵序：509.8M Enter、510.0M `y`
  （確認圖示），510.4M 回答 `y` 或 `n`。每組使用全新 scratch，起始只放原版
  `CHARS.DAX`。
- 中間態取在沒有進行中 dispatcher 呼叫、第 24 列尚未改寫的時間點：
  Y 510.624M、N 510.61M。規格原寫的 510.6M 兩條都落在呼叫中途，runner 拒絕出收據。

## 結果

| 組 | 交接後事件 | 2× active／矩形內差 | 3× active／矩形內差 | overlay＝baseline |
|---|---:|---|---|---|
| Y 中間 | 5 | 前後綴／345 | 前後綴／767 | 否（只在矩形內） |
| Y 511.0M | 7 | 無／0 | 無／0 | 是 |
| N 中間 | 5 | 前後綴／345 | 前後綴／767 | 否（只在矩形內） |
| N 511.0M | 7 | 無／0 | 無／0 | 是 |

- 矩形外差異全部為零。
- 前後綴成對失效的步數：Y 510,643,228、N 510,635,017，分別緊接在第 24 列新提示的
  dispatcher 進入（510,642,966、510,634,755）之後。
- 每組 control／2×／3× 的 indexed 逐位元相等；收據欄位只有 scratch 目錄路徑字串
  不同（每組刻意分開目錄），其餘全部相等。FileOps：Y 17,649、N 17,640。
- Y 的 scratch 寫出 `BUCK.stf`、`BUCK.who`，三組內容雜湊相同；N 只有原版 `CHARS.DAX`。

私有收據與腳本留在 ignored `workplace/phase247-save-leave-ab/`。
