# 第二百三十六階段：技能配置屏到達與檢查點入庫

狀態：**已證實／單次重播（到達）；逐列對帳另案。**

## 路徑

class500 ＋Enter→角色頁（`sheet502.state`，502M，與 phase-233
同雜湊零差異）＋N（接受屬性）→技能配置屏（`skill504.state`，
504M，VRAM `c58d13c2…`，重播同雜湊）。全程 BDA 定時鍵，
零 checkpoint 跳躍（新檢查點由此鏈存出）。

## 畫面

第 2–4／6–7 列混合標題（前景 10＋白 15 段）、第 8／13 列金線、
第 14–16 列技能列、第 24 列前景 13 指示列；結構符合
`career-skill-screen-events.tsv` 家族（逐列身分對帳另案，
 Issue #71 系）。

## 資產

`workplace/checkpoints/` 新增 `sheet502.state`、`skill504.state`
（SHA-256 見該目錄 README）；本階段收據留 ignored
`workplace/phase236-skill-screen/`。存檔含原版記憶體，不得公開。
