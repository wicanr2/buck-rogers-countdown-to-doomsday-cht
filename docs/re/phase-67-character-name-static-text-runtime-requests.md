# 第六十七階段：角色姓名靜態提示執行期請求

## 結論

姓名輸入畫面只有固定提示可安全翻譯為「角色姓名：」；玩家鍵入內容是另一條動態回顯路徑，
不得進入翻譯 catalog。本階段只產生顯示請求，沒有覆繪像素。

## 原始定位與推論等級

| 項目 | 原始定位 | 證據 | 等級 |
|---|---|---|---|
| 姓名固定提示 | `0763:0826`，row 24／column 0，bg 0／fg 13 | 長度 16，SHA-256 `246a64eabf869f90773d848870a32766bc838b7e766d88fce33dfa4e99d06676`；#101,919,217→#101,931,640 | 已證實 |
| 玩家 `A` 回顯 | `0763:09AF`，row 24／column 17，bg 0／fg 15 | 長度 1，SHA-256 `ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb` | 已證實 |

輸入為原版 DOS 檔案與第六十六階段 state；EXE／資料檔雜湊沿用專案輸入清冊。工具為本輪
dosgolem `buck-rogers-cht-output-overlay` branch；位址均為 dosgolem 執行期 `CS:IP`。

## 正常路徑收據

- 起點為 `workplace/phase66/fixed-after-bios-space-100m.state`；鍵序為四次 Enter、`N`，正例再
  輸入 `A`。
- 基線路徑：183 events／1 request／182 misses。輸入 `A`：184／1／183。
- 兩路各雙重重播；收據 SHA-256 分別為
  `bca0dfeca6a1eb4bb3abb9dff4a7be16f72eebf3d1a11eb9a464345891b0bbd0`、
  `46eb6480a7f29c4ed8dd93fa4e6513cc93662bf10b66c8843b2d3492ab4788fd`；終態 framebuffer
  分別為 `55da7c0e296b882f99c7c8ba2550743debe93a8bc480d1a0fc8fbb1dc514a6bb`、
  `bd3d779926df3b0e2979f5317f718480057bc01f36768610ac1378aa4c8feec6`。

## 邊界

本收據不證明姓名提示安全矩形、繁中像素覆繪、2×／3× 產品倍率或手冊版面。
