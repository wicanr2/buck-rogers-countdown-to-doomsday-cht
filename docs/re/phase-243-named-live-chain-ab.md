# 第二百四十三階段：正常命名直播鏈與 A/B 重跑

日期：2026-09-26  
狀態：**已證實／單次重播。** dosgolem 無頭 2×／3×。

## 直播鏈

`skill504.state` 是 `Character name: ` 命名提示（見第二百三十六至
二百三十八階段）。本階段以正常名字重建之後的鏈，全程 BIOS 鍵：

| checkpoint | 步數 | 由上一站送出的鍵 | 畫面 |
|---|---:|---|---|
| `named506` | 506.0M | `BUCK`＋Enter（504M 起，每 0.2M） | 職業技能表，80 點 |
| `bpoint1` | 506.2M | Enter | Notice＋1 |
| `btech` | 507.2M | Escape、`y` | 技術技能表，40 點 |
| `btpoint1` | 507.4M | Enter | Repair Electrical＋1 |
| `bbody` | 508.4M | Escape、`y` | Loading 之後、圖示屏初畫之前 |
| `bbodyshown` | 509.8M | — | 身體圖示屏 |
| `bconf` | 509.85M | Enter | 圖示確認問句 |
| `bsave` | 510.4M | `y` | 存檔問句 `Save BUCK? `（11 字） |

checkpoint 都在 ignored `workplace/checkpoints/`，雜湊見該目錄 README。
probe 與 runner 都由本機 dosgolem fork `d766dcf` 的乾淨 clone 建置，
與第二百四十、二百四十一階段相同。

## A/B 結果

| 路徑 | 起點 | 2× 差異 | 3× 差異 | 其他 |
|---|---|---:|---:|---|
| 職業問句 active | `bpoint1` | 2071 | 4015 | 包絡在本體 `[0,264)` 內 |
| 職業 N／Y | `bpoint1` | 0 | 0 | Y 後 63 筆 dispatcher |
| 技術問句 active | `btpoint1` | 2196 | 4211 | 包絡在本體 `[0,272)` 內 |
| 技術 N／Y | `btpoint1` | 0 | 0 | Y 的 FileOps 19,366 筆 |
| 身體圖示 move | `bbody` | 3067 | 6486 | 矩形外 0、動態圖示 0、缺字 0 |
| 身體圖示 refuse | `bbody` | 3067 | 6486 | 同上 |

八條路徑的 control／2×／3× indexed 逐位元相等；overlay 收據與 control
的共同欄位全部相等，含記憶體、事件、按鍵讀取與 FileOps。

身體圖示 confirm 路徑未跑正式 A/B：存檔問句帶玩家名字，現行 catalog
以固定 SHA 鎖定研究時的 8 字版本，正式 watcher 會拒絕。使用者已選擇
保留名字的譯文格式，模板比對規格另案處理。

私有收據、`chain.sh`、`ab.sh` 留在 ignored
`workplace/phase243-live-chain-audit/`。
