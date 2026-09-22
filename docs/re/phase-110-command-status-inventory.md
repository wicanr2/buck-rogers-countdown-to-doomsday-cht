# 第一百一十階段：command/status 最小 inventory

日期：2026-09-22
狀態：**已完成兩次可比重播；目前沒有足夠證據建立固定繁中詞 catalog。**

## 比對範圍

沿 phase109 的正常返回終態，使用同一份
`workplace/phase104-post-return-enter-3/control.state`，只改變 Enter 的排程
時間，分別在 `300000000` 與 `301000000` 送出一次 BIOS Enter；兩次都執行至
`310000000`。收據位於被忽略的：

- `workplace/phase110-command-compare/a/receipt.json`
- `workplace/phase110-command-compare/b/receipt.json`

兩次均在 Docker 的既有 dosgolem 工具鏈執行，未改寫原版記憶體、規則或輸入
資料，也未把輸入排程或原版全文寫入 Git。

## 已證實 identity 與比對結果

兩次都只有同一筆 row 24 輸出：

| 欄位 | identity |
|---|---|
| 原文長度 | 21 |
| 原文 SHA-256 | `e920b38b45dd6a828b466a06f4c4c4f63645f1c6a82e488599dc3da46b5280f2` |
| caller | dosgolem 執行期 `0763:049B`（segment 1891、offset 1179） |
| 高階 caller | `0763:1307`（segment 1891、offset 4871） |
| 畫面範圍 | row 24、column `0..20`、背景 0、前景 10 |
| indexed framebuffer SHA-256 | 兩次皆為 `b3e68d7b8806a418fdd80011939d593fc57337378983dcf890a5d936d2ad97ce` |

兩次 glyph run 的 entry/post-call 步數不同，但 identity、長度、caller、顏色、
幾何與終態 indexed framebuffer 完全一致。這證實是穩定的 command/status
輸出 identity；但兩次沒有改變角色、回合、數值或命令選擇，因此只能把「固定
性待進一步比對」列為未知，不能把整行當成固定介面詞。

## 固定詞／動態欄位分類與停止點

- 右側角色名稱與數值區：現有畫面可見但屬玩家／狀態資料，維持原文與 miss，
  不建立翻譯 key。
- row 24：已知為命令／狀態路徑的 21-cell identity；尚未有第二種遊戲狀態，
  無法安全分割固定詞、數值與時間欄位，整筆維持 miss。
- 固定劇情 page4：沒有 `0763:04FF` 的 rows 17–21 glyph identity，仍不建立
  `story-page4-events.tsv` 或 `story-page4.zh-TW.tsv`。

因此本輪沒有可安全新增的繁中 TSV、validator 或安全矩形候選。下一個最小
研究步驟是取得一個合法且不同的 command/status 狀態（例如同一路徑的另一個
已證實命令結果），再以相同 caller、row、column 與 identity 比對固定欄位；
未取得前不得猜譯或接 runtime。
