# 第二百四十一階段：技術技能離開問句的直播鏈正式 A/B

日期：2026-09-25  
狀態：**已證實／單次重播。** 範圍限技術技能頁問句本體、Escape→N／Y、
dosgolem 無頭 2×／3×。

## 到達技術技能頁

從第二百四十階段的 `point1.state` 接續，全程只用 BIOS 鍵：

1. `510000000` Escape，職業問句出現。
2. `510200000` 送 `y`，離開職業頁。`511000000` 存成 `tech511.state`
   （SHA-256 `de162387…7117a7b7f`）。畫面為技術技能表：通用點數 40、
   單項上限 30。
3. `511000000` Enter，首項 Points 0→1、Total 15、剩餘 39，算術閉合。
   `511200000` 存成 `tpoint1.state`（SHA-256 `b871fe51…86aee5cfc3e8`）。
4. `511200000` Escape，唯一 dispatcher 為 caller `37F1:101E`、34 字的
   技術頁問句，原文 SHA-256 開頭 `5592b4048986`，與正式 catalog 身分相符。

probe 與 runner 都由本機 dosgolem fork `d766dcf` 的乾淨 clone 建置。
probe SHA-256 `c814c5e6…312921728`；runner 同第二百四十階段
（`a710fb1d…1ef9bd9c`）。字型與 TSV 身分亦同第二百四十階段。

## A/B 結果

| 路徑 | until | BIOS 排程 |
|---|---:|---|
| active | 511400000 | `511200000:01:1b` |
| N | 512200000 | 上列＋`511400000:31:6e` |
| Y | 512200000 | 上列＋`511400000:15:79` |

- active：2× 差 2196 像素，logical 包絡 `[0,270)×[192,200)`；3× 差
  4211 像素，包絡 `[0,270)×[192,199)`。都在核准本體 `[0,272)×[192,200)`
  內，尾碼與其餘畫面零差。像素數與第二百零二階段技術頁相同。
- N：按鍵被讀取，無新 dispatcher。Y：離頁，FileOps 19,366 筆。
- 三條路徑的 control／2×／3× JSON 與 indexed 逐位元相等，包含 Y 的
  FileOps。JSON SHA-256：active `d2d002c9…52859bd3`、N
  `9df117f0…e911dabcc1`、Y `4238a6e9…5b64b9e4`。N／Y 終態 overlay
  RGBA 對 baseline 全畫面零差。

## 結論與限制

職業與技術兩頁的離開問句，正式覆繪都已在冷開機玩家按鍵鏈上成立。
尚未涵蓋：遊戲內存讀檔後的重現、正式 Restore／Discontinuity session
bridge、Linux 視窗（後兩項與 #18、#16 重疊）。

私有收據、probe、runner 與 `run.sh` 留在 ignored
`workplace/phase241-technical-live/`；兩個新 checkpoint 在 ignored
`workplace/checkpoints/`。

這條鏈的角色名是 Down／Up 誤輸入的 `28`（見第二百三十八階段）；問句本體不含名字，正常命名 `BUCK` 的重跑結果相同，見第二百四十三階段。
