# 第一百九十二階段：加入角色後選單第七列的清層執行期 A/B

日期：2026-09-23
狀態：**已量固定 row20 普通回寫的限縮生命週期；spec 018 仍為 READY，非整體 CONFORMED。**

## 同一原版起點與兩個完整事件停止點

沿用[第一百八十二階段](phase-182-post-join-menu-runtime-ab-partial.md)的原版與
READY 三份 TSV、倚天 GOLEMFNT，不改原版 EXE、輸入或存檔。原版
`GAME.OVR` SHA-256
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`；
合法 `workplace/phase54/a-joined.state` SHA-256
`1bb95276ccb4c1976175d381e0d03bc148a8b0f4da908fb155764a4b71bfd48d`；
本機字型 SHA-256
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
原版檔案唯讀掛載，所有 JSON／RGBA 與 runner 留在 ignored
`workplace/phase192-post-join-boundary/`。

dosgolem 本機 fork 基底為
`3092dade3aa5deaf86395864a6c539f4088bdf23`；此次只在同一 fork
增加回歸**測試**，未改 production watcher／presenter。Docker Go 1.26.7
建出的 `buckrogers-text-receipt` SHA-256 為
`5dfe8d70aab9da47b17175f76e05957b0cfb47371ea9029274e42a6d74618f14`。
本機 fork 的測試提交為
`f15157fa6b2daf2dca43c2914df8cc6a5dd41e49`，測試檔 SHA-256
`3003d8f1dc50b2a8dcbea4661afab79ee7bf86fb1a144956a4e0d7337eeefcb7`。
位址 `0763:184D` 是 dosgolem 實模式指令位址，A000 位址是線性視訊位址；
不可混用。

從 state step `122400000` 固定送 Right `122600000`、Enter `122800000`，
再於 `123300000` 至 `124700000` 每 200000 steps 送一次 Down，共八次。
兩個停止點均使用**相同十筆鍵**：

| 停止點 | 玩家可見／原版事件邊界 | 已收錄事件 |
| --- | --- | ---: |
| `124700001` | 最後一次 Down 已排入，row20 普通回寫尚未 entry；第七代繁中作用層仍在。 | 39 |
| `124713776` | row20 普通回寫 `124700613→124713775` 已完成，未知 row21 selected 尚未 entry。 | 40 |

[第一百八十階段](phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)
已獨立量到此代最早相交原版 glyph pre-write 為 step `124700875`、
`0763:184D`、像素 `(72,160)`、`15→0`。本輪未重新把該原版單步宣稱為
「同值」；同值 pre-write 的失敗即關閉契約另由下述正式 Go 測試驗證。

## 正式 CLI 的雙倍率／控制組結果

control、2× 與 3× 在各停止點的 JSON 逐 byte 相同，四個覆繪情況又
各自重跑一次，JSON、baseline RGBA、overlay RGBA 均逐 byte 重生：

| 停止點 | 三模式共同 JSON SHA-256 | 2× overlay／baseline SHA-256 | 3× overlay／baseline SHA-256 |
| --- | --- | --- | --- |
| 前 | `ff15d24ab09d5500bd3c0ede878d61d2099bd5a0fb08b223619a936e0cfaa8c0` | `a74fcd5f64e6794b845393ccf96d4c2c94269f6d7e0463f71b0022aac04a4bbd`／`dd3bb16308284652242773b2a33dba5c2b0048a83ea114c257a2c3f92133ffb9` | `e19f86ea21f575a0d4cb597c72d516565d10fdb59c7b49162e76081284984da2`／`3e76e3d7be9e890f91322885b32f26966622ac716ea1d0a9d2c05f4bf4164898` |
| 後 | `e95010ba286b9874f40b4207a16c448d591c12be5a5d6fe04394eb7d1934506c` | 兩者逐 byte 相等：`2b7b6010c7ea3abd9c7eb9d4f8f60d33ea226b6b39a1ea8d015b89c7c49929ce` | 兩者逐 byte 相等：`d351081915c298f11717356922fb74729d9170ec4b7ca8bace38efcdf0ac0d0b` |

前點 39 筆、後點 40 筆；兩端均排入十筆相同鍵。控制組與覆繪組
每一個已記錄欄位（包含事件、鍵盤排程、memory、indexed framebuffer、
palette SHA-256）都相同；這只證明**收據所涵蓋的欄位**，不是所有
DOS 內部狀態或檔案副作用。兩倍率後點覆繪 RGBA 完全等於各自
baseline，故此固定 row20 普通回寫**完成後**沒有七列繁中殘影。

## 同值首寫的正式元件回歸

在本機 dosgolem fork 的 `apps/buckrogers/post_join_menu_test.go` 新增
`TestPostJoinPresenterSameValuePrewriteClearsBothScales`。它用合成但 typed 的
七列作用層，對 2×／3× 各驗證：覆繪前確有可見差異；即使 A000 pre-write
的舊值與新值皆為 0，`RuntimePostJoinMenuOverlay.Prewrite` 仍立即把七列
active keys 清空；同一未變的 indexed/palette 畫面再投影時，RGBA
逐 byte 等於 baseline。這是**元件契約測試**，不能冒稱原版 step
`124700875` 是同值寫入。既有
`TestPostJoinWatcherInvalidatesSameValueBeforeRedraw` 同時確認 watcher
的 active flag 失效。定向測試、`go test ./apps/buckrogers -count=1`
及 `go vet ./apps/buckrogers` 在隔離 Docker 內通過。

## 停止線

正式 CLI 拒絕停在 dispatcher 尚 pending 的 `124700875／876` 並產生
「成功收據」，故本輪不能以兩張合法終態圖冒稱逐**指令** runtime
active→empty 已被觀測；精確首寫時序仍以第一百八十階段原版
pre-write 收據與正式元件測試交叉支持。未知 row21 selected 一旦 entry，
目前正式 watcher 會失敗即關閉，不能靠本輪補成 Exit 中文化。
真正 Exit Enter 後兩段提示、清除／terminal lifecycle、其他功能選項、
完整玩家開機與存讀檔仍未驗。spec 018 的七列限縮 READY 範圍
沒有擴張，整體仍非 CONFORMED。
