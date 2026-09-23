# 第一百八十二階段：加入角色後選單正式輸出覆繪局部 A/B

日期：2026-09-23  
狀態：**局部同狀態收據通過；spec 018 仍為限縮 READY，尚非 CONFORMED。**

## 權威輸入與執行邊界

本次沿用[規格 018](../spec/018-post-join-menu-overlay-draft.md)核准的 `a-joined.state`
（SHA-256 `1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`）
及原版 `GAME.OVR`（SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`）。
dosgolem 本機 fork 為 `cb3ca77c66e4909c5f513b807840e885ab5cb4a3`；
CLI 小切片從 `ab1731c` 接線、`35bd3fb` 釘選現行 1028-glyph 倚天字型 SHA、
`ce0cdb8` 修正 entry／return 同一 row gate、`157ec93` 只在覆繪 active 時監看
A000 pre-write。原版及字型只在 ignored `workplace/`，原版資料唯讀掛載；
測試在有界、無網路 Docker 內以目前使用者 UID/GID 執行。

`0CF4:1B3A` 曾於選單初畫、generation 1 建立前寫入 A000 row 13；
此時沒有中文覆繪可失效。generation 1 在 step `123150388` 的 row 13 selected return
後才 active；其後首筆相交 pre-write 仍是已由[第一百八十階段](phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)
核准的 `0763:184D`。因此 CLI 不把初畫期 writer 誤判為 active layer 的未知改寫；
active 後的未知 writer 仍失敗即關閉。這是接線時機勘誤，不是增加一個核准 writer。

## 同狀態 control／2×／3× 終態

三次使用同一合法 state、輸入與 `-until 124700000`。私有 JSON 收據分別為
`workplace/.phase182-control.json`、`.phase182-receipt2.json`、`.phase182-receipt3.json`；
三者逐位元組 SHA-256 均為
`b959cd9d43cf5affed94cbb22a30b8ee61b442db0299b8a03779bf48d4d34b81`。
`state_start=122400000`、`stopped_at=124700000`；machine memory SHA-256
`94f63d37be11bb68daf5f48a14b76177164bef7b0f835fbef97db6ee0bb20af1`、
indexed framebuffer `454375c9642d96f8c865c384687b373d3d878441ce293f1fd55685616e256fca`、
palette `3f85bab8365683af5d0e87c45bb6a6596ad3779ffd68694b39fcd894b4a587e6`
也逐次相同。這確認本次覆繪沒有改變該終態的原版語意層；不代表未量路徑。

以 320×200 原始畫布分別乘 2、3，逐 RGBA 像素比對 baseline 與覆繪：

| 倍率 | baseline SHA-256 | 覆繪 SHA-256 | 七列安全矩形內差異 | 矩形外差異 |
| --- | --- | --- | ---: | ---: |
| 2× | `dd3bb16308284652242773b2a33dba5c2b0048a83ea114c257a2c3f92133ffb9` | `a74fcd5f64e6794b845393ccf96d4c2c94269f6d7e0463f71b0022aac04a4bbd` | 6521 | 0 |
| 3× | `3e76e3d7be9e890f91322885b32f26966622ac716ea1d0a9d2c05f4bf4164898` | `e19f86ea21f575a0d4cb597c72d516565d10fdb59c7b49162e76081284984da2` | 13659 | 0 |

安全矩形使用 spec 018 七列各自的原文長度，逐列
`[72,72+8×length)×[8×row,8×row+8)`，再乘輸出倍率。
主代理另在 Docker 獨立回讀三份 JSON 與四份私有 RGBA，重算上述 SHA 與
2×／3×所有像素；沒有以子代理的摘要代替回讀。全部私有輸出 owner 為目前使用者，
不加入 Git、GitHub 或發行包。

## 已驗拒絕與剩餘門檻

沿相同正常路徑到 `-until 124800000`，原版已量的 row 21 selected
在 step `124714336` 進入未收錄 identity；CLI 以
`post-join fail-closed: unknown post-join identity` 退出碼 1 停止，沒有輸出新的 RGBA
或 JSON。這證實沒有把 row 21 猜補成中文，但尚無逐幀收據證明 row 20 普通回寫的
第一筆相交 pre-write 當幀就使 active→empty，也未完成 `EXIT TO DOS` Enter clear
後的無殘字比對。完整玩家前端、其他選單動作、重入與存讀檔均不在本次驗證。

因此 spec 018 保持 READY；下一個最小門檻是同狀態逐幀失效／Exit clear 收據，
而非擴大逆向或直接宣稱整個選單已中文化。
