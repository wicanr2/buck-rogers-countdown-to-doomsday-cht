# 第二百四十階段：職業技能離開問句的直播鏈正式 A/B

日期：2026-09-25  
狀態：**已證實／單次重播。** 範圍限職業技能頁問句本體、Escape→N／Y、
dosgolem 無頭 2×／3×。

## 起點

`point1.state` 由冷開機按鍵鏈到達（TANDY→title→種族→性別→職業→
角色頁→命名→技能配置→加 1 點，見第二百二十七至二百三十九階段），不是
第二百零二階段的固定研究 state。SHA-256
`48e1c1079ea9ffe9c84bf59b7de7f16774e1329a5fe5a474cc277f932e6d6cfa`。

runner 由本機 dosgolem fork `d766dcf` 的乾淨 clone 建置：
Go `1.26.7`、`vcs.modified=false`，binary SHA-256
`a710fb1d7b2d6388047b598b179621007522e5e1f7fe7d5f6a82196e1ef9bd9c`。
倚天字型為現行 1,046 字版，SHA-256
`14fca041c98198f778b06552a2a2fc34773b1fbdcf9e6683e72ea244228d4dca`。
三份 TSV 的雜湊與第二百零二階段相同。control 與 overlay 都帶
`-file-ops -key-trace`。

| 路徑 | until | BIOS 排程 |
|---|---:|---|
| active | 510200000 | `510000000:01:1b` |
| N | 511000000 | 上列＋`510200000:31:6e` |
| Y | 511000000 | 上列＋`510200000:15:79` |

## 觀測結果

- 三條路徑都只有一筆問句事件：caller `37F1:101E`、33 字、原文
  SHA-256 `65108526…9bc07a9`。entry 在 `510001144`。
- active：2× 差 2071 像素，logical 包絡 `[0,262)×[192,200)`；
  3× 差 4015 像素，包絡 `[0,262)×[192,199)`。都在核准本體
  `[0,264)×[192,200)` 內，尾碼與其餘畫面零差。像素數與第二百零二
  階段職業頁相同。
- N：`510200200` 讀到 N，本體 8 列改回，無新 dispatcher。
- Y：同步讀到 Y，離頁並出現 63 筆 dispatcher。
- 三條路徑的 control／2×／3× JSON 與 indexed 逐位元相等。JSON
  SHA-256：active `9c78c8db…20b5b6ec`、N `26197aeb…51ad732a8`、
  Y `9b376620…afeb2d`。N／Y 終態 overlay RGBA 對 baseline 全畫面零差，
  沒有殘層。三條路徑 FileOps 皆 0 筆。

## 結論與限制

職業技能頁問句的正式覆繪在冷開機玩家按鍵鏈上成立，行為與固定研究
state 一致。以下仍未涵蓋：技術技能頁問句的直播鏈、遊戲內存讀檔、
正式 Restore／Discontinuity session bridge、Linux 視窗。

私有收據、runner 與 `run.sh` 留在 ignored
`workplace/phase240-exit-live-ab/`，未進 Git。

這條鏈的角色名是 Down／Up 誤輸入的 `28`（見第二百三十八階段）；問句本體不含名字，正常命名 `BUCK` 的重跑結果相同，見第二百四十三階段。
