# 第一百零九階段：第四次 Enter 後的 command loop 分類

日期：2026-09-22
狀態：**已分類為 row 24 命令／狀態輸出；固定性待比對，本階段不建立第四頁固定劇情 catalog。**

## 勘誤（2026-09-22）

重新對照既有 `workplace/phase104-post-return-enter-4/baseline.png`（SHA-256
`209881731d8c49699336d7ece0575b514899945785e9174a6f036935bf4769c3`）
與同停止點 `control.indexed`（SHA-256
`4f9d1bb280724737ca72599c3e7d387c23c076f7e0a8637d8d3ebc9164514bf2`）後，
畫面下方明確出現**新的固定劇情敘述**。因此本階段「沒有第四頁固定劇情」的
結論已被原版畫面反證；此處的 low-level glyph trace 只找到 row 24，不能外推
為第四頁沒有文字。可能是不同印字路徑、trace 篩選條件或停止點對齊問題，
須另做窄範圍追蹤。以下保留當時 trace 與錯誤推論形成過程，不將它當現況。

## 範圍與證據邊界

本階段只重播被忽略的本機 dosgolem state，確認
`phase104-post-return-enter-4` 是否在第四次 Enter 後仍產生固定敘事 glyph
run。原版遊戲、手冊、完整英文輸出與字型均未寫入版控；本文件只保存
content-safe identity metadata。

輸入 state 為 `workplace/phase104-post-return-enter-3/control.state`，在
dosgolem 執行步 `300000000` 排程一筆正常 BIOS Enter（scan `0x1c`、ASCII
`0x0d`），執行至 `310000000`。輸出收據為被忽略的
`workplace/phase109-page4-from300/page4.json`。此命令在 Docker 的
`golang:1.24-bookworm` 工具鏈中執行，沒有 runtime overlay 或 VRAM 修改。

## 觀測結果

- 觀測到一筆 row 24 命令／狀態輸出：`original_length=21`，原文 identity SHA-256
  `e920b38b45dd6a828b466a06f4c4c4f63645f1c6a82e488599dc3da46b5280f2`。
- 其 caller 為 dosgolem 執行期段位址 `0763:049B`（segment `1891`、offset
  `1179`），背景色 `0`、前景色 `10`、row `24`、column `0`；逐 glyph
  trace 覆蓋 column `0..20`。
- 高階事件同樣是 row 24、caller `0763:1307`（segment `1891`、offset
  `4871`），不是 page2／page3 固定劇情使用的 caller `0763:04FF`。
- 收據的 `state_start` 為 `300000000`、`stopped_at` 為 `310000000`，輸入
  `bios_keys` 僅一筆，且沒有 rows `17..21` 的固定故事 glyph run。

上述當時只確認 trace 覆蓋 row 24 命令／狀態路徑。單次收據不足以判定整行
每個欄位都是動態，也不足以否定同一畫面的其他文字路徑；頁面下方確有劇情
的反證見本文件開頭勘誤。row 24 在完成比對前仍不能猜譯。

既有 `phase104-post-return-enter-4/baseline.png` 可作本機視覺參考，但單張
畫面沒有 caller、長度與 hash identity，且不等於 Enter 後新繪製的固定 glyph
證據。因此本階段不建立 `story-page4-events.tsv` 或
`story-page4.zh-TW.tsv`，也不新增翻譯候選。

## 下一個可翻譯靜態輸出

目前最小可翻譯靜態輸出是已完成 evidence identity 的 page1–page3 固定劇情
catalog；第四次 Enter 後應先另開動態 command/status inventory，逐欄確認
哪些欄位是固定介面詞、哪些是姓名／數值／狀態，再分別建立 exact identity。
在取得該證據前，row 24 維持 miss，不建立 editorial 翻譯或 runtime 接線。

## 可重生命令與權利界線

命令使用 project/workplace 的 dosgolem 原始碼與忽略的本機輸入，在 Docker
內執行：

```text
go run ./cmd/buckrogers-text-receipt \
  -state /repo/workplace/phase104-post-return-enter-3/control.state \
  -until 310000000 \
  -bios-key-at 300000000:1c:0d \
  -glyph-trace -glyph-trace-from 300000000 \
  -receipt-out /repo/workplace/phase109-page4-from300/page4.json
```

命令只輸出 metadata；原版 state、資料檔、畫面與 glyph bytes 均留在
`workplace/`，不加入 GitHub 或公開包。
