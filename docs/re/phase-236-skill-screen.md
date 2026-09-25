# 第二百三十六階段：命名提示到達與檢查點入庫

狀態：**已證實／單次重播。**

## 路徑

class500 ＋Enter→角色頁（`sheet502.state`，502M，與 phase-233
同雜湊零差異）＋`n`（接受能力值）→角色頁以擲出的能力值重畫，
最後一筆 dispatcher 為 `0763:0826` 的 `Character name: ` 命名提示
（`skill504.state`，504M，VRAM `c58d13c2…`，重播同雜湊）。
全程 BDA 定時鍵，零 checkpoint 跳躍。

## 畫面

命名提示疊在角色頁上；角色頁的職業技能列仍在畫面中。
`skill504` 這個檔名沿用舊稱，內容是命名提示，不是技能配置屏。

## 資產

`workplace/checkpoints/` 有 `sheet502.state`、`skill504.state`
（SHA-256 見該目錄 README）；收據留 ignored
`workplace/phase236-skill-screen/`、`workplace/phase243-live-chain-audit/`。
存檔含原版記憶體，不得公開。

勘誤紀錄：WORKLOG 2026-09-25「直播鏈命名提示勘誤」。
