# 第十二階段：手冊題庫結構與可抽題清冊

## 結論

原版手冊驗證題庫共有 39 筆固定長度紀錄，位於執行期主資料段 `0EC0:00C2..0553`，每筆
30 bytes。已建立只含頁碼、標題及序數的可重生清冊；答案欄雖為界定 schema 所必須，工具
只驗證其長度界線，不解碼、不輸出，也不提供自動作答。

## 輸入與工具

- `START.EXE`：67,619 bytes；SHA-256
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`。
- `GAME.OVR`：210,071 bytes；SHA-256
  `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
- 執行期 `0EC0:0000` 64 KiB 傾印：SHA-256
  `28a0563b647ebe75a70e19648502e3fb9dc9379ada35bd397d99b104a4ce7c60`。
- 執行期 `2A33:0000` 8 KiB overlay 傾印：SHA-256
  `7a2d9a3806d6ae49e5f8aa47a36767a38a0c1d1cbe744400e0525a98c4c2682c`。
- 主反組譯工具：IDA Pro 9.4，`pc` 處理器、16-bit database；image
  `ida-pro-9.4-idapython:locked-v1`，image ID
  `sha256:6f6d59af49d0008c4109a5295b5f374bdc007e2d1ab28cb9de08779584de2780`。
- IDA raw database 位址 `0x0000` 對應 dosgolem 執行期 `2A33:0000`；以下不得與
  `START.EXE` 靜態線性位址混用。

## 固定顯示契約與 schema

| 原始定位 | 附加語意 | 等級 | 證據 |
| --- | --- | --- | --- |
| `0EC0:00C2 + index*0x1E`，index `0..38` | 39 筆題目紀錄，stride 30 | 已證實 | `2A33:01AD..01C9` 以 39 為亂數上界，結果加一後乘 30，再加 `00A4`；實際索引為 1..39，因此首筆為 `00C2` |
| record `+00` | 手冊頁碼 `u8` | 已證實 | `2A33:0203` 讀取並轉成顯示字串；動態第 32 筆顯示 34 |
| record `+01`；`+02..+13` | 標題長度；18-byte 編碼區 | 已證實 | `2A33:002D..00AB` 解碼分支及 `2A33:0246..0275` 顯示呼叫 |
| record `+14` | 第幾個字，範圍 1..10 | 已證實 | `2A33:02B7..02CE` 乘 19 後索引序數字串表；第 32 筆動態顯示 tenth |
| record `+15`；`+16..+1D` | 答案長度；8-byte 編碼區 | 已證實，但禁止匯出 | `2A33:00AD..012B` 解碼分支及 `2A33:030E..03BC` 比較流程 |
| 每個編碼 byte | `decoded = encoded - 6 + field_length` | 已證實 | 兩個解碼迴圈的 `sub ax,6`、`add ax,dx`；39 筆標題皆可得 ASCII |

IDA 輸出保留 `database_ea`、`raw_file_offset`、`runtime_offset`、原始 bytes 與反組譯；本表
只附加語意，不改名取代原始定位。`workplace/ida/phase12-decoder.json` 與 `.i64` 是本機
可重生證據，不納入 Git。

## 動態反向驗證

- 第 32 筆位於 `0EC0:0464`：頁 34、`Deimos Prison`、序數 10。它與第十一階段正常玩家
  路徑第一次抽題完全一致。
- 錯答後第 38 筆位於 `0EC0:0518`：頁 41、`Technical Skills`、序數 2。它與同一路徑
  第二次抽題完全一致。

這兩筆只驗證題目 metadata 與抽題消費者，沒有固定或重擲亂數來挑選通過結果。

## 可重生清冊與中文來源

`tools/manual_questions.py` 讀取從 `0EC0:0000` 起算的資料段，失敗即關閉檢查資料長度、
標題／答案容量與序數範圍，再輸出 `text/manual-questions.tsv` 的五個欄位。輸出刻意沒有
答案欄。

目前只有 `Deimos Prison` 已能唯一配對中文來源：archive-order 66、
`SCAN0352_039.jpg`、印刷頁 73、條目 49「在監獄中」。`Technical Skills` 及其餘 38 筆
尚未逐頁完成唯一來源核對，維持未知；不以標題相似度猜補。

## 邊界

- 39 筆表示原版此版本可抽選的 metadata 清冊，不表示 39 筆中文段落已完成。
- 原版答案欄仍存在並由原程式比較；本階段沒有改寫、暴露或自動輸入它。
- 規格仍為 DRAFT；中文覆繪、generation 失效、分頁及 2×／3× 選擇均未在本階段完成。
