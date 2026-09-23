# 第一百九十五階段：加入角色後七列選單的逐寫入清層收據

日期：2026-09-24
狀態：**固定正常路徑限縮 CONFORMED；不含真正 Exit 或完整選單。**

沿用[第一百九十二階段](phase-192-post-join-menu-prewrite-runtime-ab.md)的合法 `a-joined.state` 與十筆 BIOS 鍵；原版 `GAME.OVR` SHA-256 為 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，state 為 `1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`，本機倚天字型為 `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。位址均為 dosgolem 8086 實模式 `segment:offset`，視訊偏移另標 A000；不能當成 IDA 或檔案偏移。

本機 fork `540a522` 在正式 `buckrogers-text-receipt` 的既有 A000 pre-write 回調中增加不含內容的 `post_join_invalidations` 收據。先呼叫 watcher、再呼叫 presenter 的順序未變；只在 watcher `active→inactive` 時記錄 step、`CS:IP`、A000 offset、write mode、watcher 狀態與 presenter key 數。它不記原文、寫入值或像素。正反單元測試確認沒有 transition 不多記，且 presenter 未清除時不得假報為零 key。

使用 Docker／Go 1.26.7 由這份正式原始碼建出的 runner SHA-256 是 `6aa8967ae288fdb6689e2a71576dfb1946be5b24cc617dda16faaa0dc8024d12`。原版資料唯讀掛載；在 `124713776` 停止，2×／3× 的 JSON 逐 byte 相同，SHA-256 同為 `c72eedf363ce79ab2cd76b147be0fda83e310da1f8ddd9ad2c9d2197f7cb25f2`。扣除新增欄位，既有 JSON 所有欄位與第 192 階段控制組逐 byte 相同。收據恰有七筆 watcher `true→false`、presenter keys `7→0`；最後一筆是 step `124700875`、`0763:184D`、A000 偏移 `51272`，早於 row20 普通回寫完成。

row20 回寫後，2× 的 overlay／baseline RGBA 逐 byte 同為 `2b7b6010c7ea3abd9c7eb9d4f8f60d33ea226b6b39a1ea8d015b89c7c49929ce`；3× 同為 `d351081915c298f11717356922fb74729d9170ec4b7ca8bace38efcdf0ac0d0b`。回寫前兩倍率確有覆繪差異；故後點相等不是原本未覆繪的假陰性。既有第 182 階段驗同路徑的 control／2×／3× 原版狀態與安全矩形；正式測試另覆蓋 row20→未知 row21 拒絕、未知 writer、同值 pre-write、execution discontinuity 及 presenter 故障。

獨立審查只核准：合法 `a-joined.state` 的 `Right → Enter → rows 13、14、15、16、18、19、20`，以及第七代 row20 普通回寫前的清層，止於未知 row21 selected entry 之前。原版程式與存檔未修改。真正 row21 `Exit to DOS`、row24 提示、重入、完整開機、遊戲內存讀檔及其他選單分支仍為 DRAFT／未驗；不得把整份[規格 018](../spec/018-post-join-menu-overlay-draft.md)或整個遊戲稱作完成。私有 JSON／RGBA 留在 ignored `workplace/phase192-post-join-boundary/`，不加入 GitHub。
