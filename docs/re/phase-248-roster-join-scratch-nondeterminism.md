# 第二百四十八階段：加入隊伍路徑的暫存層非決定性

日期：2026-09-26  
狀態：**已證實／多次重播。**

## 路徑

`bsave.state` 以全新 scratch（起始只放原版 `CHARS.DAX`）回答 `y` 存檔，511.0M 存成
`menu511.state`，同時保留當下 scratch 為 `s0`。之後 511.0M Down、511.6M Enter
（加入角色）、512.2M Enter（選 `BUCK`），停在 512.6M。dispatcher 依序為：功能選單
重畫與提示、名冊 `BUCK` 列、加入提示、載入中、加入標記 `* BUCK`、再一次加入提示，
與第五十六階段的形狀相同。

## 覆繪結果

control／2×／3× 的事件、request、indexed、FileOps（2,602 筆）與 scratch 內容全部相同；
2× 差 966 像素、3× 差 2,064 像素，全在第 24 列 `[0,124)×[192,200)`，名冊名字列零差。

## 非決定性

- 三組的 `memory_sha256` 不同。只換 scratch 目錄名的三次 control 相同；
  間隔 3 秒的兩次 control 不同。與覆繪無關。
- 來源：dosgolem `internal/dos/find.go` 的 `dosDateTime` 讀主機 mtime。暫存層在執行中
  新建的檔（`BUCK.WHO`、`CHARS.dax`）帶主機建檔時刻，程式經 DTA 讀到後存進記憶體。
- 同一路徑的暫存層出現大小寫重複：`CHARS.DAX`／`CHARS.dax`、`BUCK.who`／`BUCK.WHO`，
  內容相同。第五十七階段的 scratch 也有同樣現象。原因是寫時複製只做精確大小寫比對。

修正規格：dosgolem `docs/spec/237-scratch-determinism-draft.md`。

私有收據留在 ignored `workplace/phase248-roster-join/`。
