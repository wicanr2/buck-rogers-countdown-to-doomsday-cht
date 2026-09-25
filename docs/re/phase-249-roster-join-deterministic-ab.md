# 第二百四十九階段：加入隊伍路徑的決定性 A/B

日期：2026-09-26  
狀態：**已證實／單次重播。**

## 輸入

- 本機 dosgolem fork `21f750c`（規格 237：暫存層檔案時間取虛擬時刻、大小寫收斂），
  乾淨 clone 建置，`vcs.modified=false`；runner SHA-256 `b704b778…719ae76df`，
  probe SHA-256 `b6132996…a3ce6f0`。
- `bsave.state` 以全新 scratch（原版 `CHARS.DAX` 用 `cp -p` 保留 mtime）回答 `y`，
  511.0M 存成 `menu511.state` 與 scratch 快照 `s0`。
- 路徑同第二百四十八階段：Down、Enter（加入角色）、Enter（選 `BUCK`），停在 512.6M。

## 結果

- 兩次 control 間隔 3 秒以上，加上 2×、3×，四組 `memory_sha256` 相同
  （`04b84a67…`）。收據欄位只有 scratch 目錄路徑字串不同。
- indexed、FileOps（2,602 筆）與 scratch 內容四組相同。scratch 只有
  `BUCK.stf`、`BUCK.who`、`CHARS.DAX` 與 `SAVE`，沒有大小寫重複檔。
- 覆繪差異：2× 966 像素、3× 2,064 像素，全在第 24 列，名冊名字列零差。

第二百四十八階段記錄的兩個非決定性來源都已消除。

私有收據留在 ignored `workplace/phase249-roster-deterministic/`。
