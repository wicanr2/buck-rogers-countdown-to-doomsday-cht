# 第二百五十三階段：即時覆繪接上全部已完成家族

日期：2026-09-26  
狀態：**已證實（receipt runner 並行比對）；Linux 視窗的實體互動未驗。**

## 內容

dosgolem fork 分支 `buck-rogers-cht-output-overlay`：

| commit | 內容 |
|---|---|
| `089d017` | 身體圖示屏家族（含存檔問句名字前後綴）接入 `LiveRuntime` |
| `4af0a58` | 手冊題目段落家族 |
| `479ce12` | 開場與劇情第 2–9 頁家族 |
| `7cf0b43` | 技能頁動作列家族 |
| `c79a1ef` | 劇情套用改為世代前進才讀 palette（效能） |

`apps/buckrogers/live_runtime.go` 的 `LiveRuntime` 依 runner 的觀測順序分派：
劇情 far-return 驗證、動作列 post-call、選單 dispatcher、手冊、glyph entry、
`0CF4:1B3A` 清除寫入、劇情與動作列套用。A000 寫入前失效與回掃畫格也照 runner
的家族順序轉發。

與 runner 的差異是故障處理：runner 對任一家族故障失敗即關閉；即時執行期只清掉
該家族並重建，其他家族繼續（`Resets()` 記錄次數）。選單家族擁有共用 recorder，
故障仍視為致命。

兩個家族同時作用時，後寫入者優先：`yieldMenu` 在其他家族套用時清除與其安全矩形
相交的選單戳記，避免加入後離開問句與選單第 24 列疊字。

## 驗證方法

runner 以 `-live-text-dir`、`-live-rgba-out`、`-live-scale` 並行驅動完整
`LiveRuntime`。預期畫面 = 選單 overlay + 各家族 overlay 對 baseline 的差分層
（`workplace/phase254-live-families-parity/compose.py`）。七組腳本、2×／3× 各一：

| 家族 | 時間點 | 結果 |
|---|---|---|
| 技能離開問句 | 職業／技術頁問句與 n、y 後 | 8/8 相同 |
| 加入後選單與離開問句 | row 20、問句、n | 6/6 相同；`yy` 2 組差異見下 |
| 技能頁動作列 | 初畫、Down、加點 | 10/10 相同 |
| 劇情頁 | 281.1M、281.5M、282.5M | 6/6 相同 |
| 開場 | 275M、280.9M、282M | 6/6 相同 |
| 手冊 | 266.65M、266.9M、275M | 6/6 相同；266.56M 2 組差異見下 |
| 身體圖示屏 | 移動、拒絕、確認 | 6/6 相同 |

兩組差異都出在預期畫面，不在即時執行期：

- `yy`：離開問句與選單第 24 列重疊。差分層疊加無法表達「後寫入者清掉前者」，
  預期合成本身是錯的；即時畫面以 `yieldMenu` 規則正確顯示問句。
- 手冊 266.56M：runner 在收據收尾時多送一次 `Frame`，家族狀態比即時執行期多前進
  一格。

效能修正後重跑七組，結果與修正前逐項相同。

## 效能

headless `cmd/buckrogers-session`、250M 步、完整家族：

- 修正前 65 秒。profile：`LiveRuntime.BeforeStep` 自身 22.6%，其中劇情套用閘門在
  每個 glyph entry 讀整份 palette（`Machine.Palette` 3.4%、`logicalRGB` 3.1%）。
- 修正後 33 秒。無觀測器約 21–28 秒。

## 限制

- `LiveMenuRuntime.Observe` 仍佔約 14%，逐步快速路徑還有空間。
- 加入後選單 row 21 之後、row 15／24 指令狀態列仍為英文。
- 劇情第 9 頁之後進入遊戲本體，敘事窗、探索、戰鬥與對話全為英文，
  見[第二百五十四階段](phase-254-in-game-text-inventory.md)。
