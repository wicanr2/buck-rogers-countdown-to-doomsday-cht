# 第十三階段：39 筆手冊題目與繁中來源對照

## 結論

已逐筆檢查 `text/manual-questions.tsv` 的 39 筆題目，建立繁中掃描來源對照：35 筆為
`confirmed`、3 筆為 `strong-inference`、1 筆為 `unknown`。最後一筆 `Roll.` 所需頁面不在
使用者提供的掃描中；沒有用鄰頁、OCR 相似字或自行翻譯猜補。

本階段只確認來源定位，不把 OCR 當成可直接顯示的校訂譯文。`text/manual.zh-TW.tsv` 因此
仍只保存先前已由影像人工核對的 `Deimos Prison` 段落；其他段落須另做逐字校訂才可加入。

## 輸入與工具收據

- 來源 RAR SHA-256：
  `4d018c13cf2d7aa632435f8c03042bf42a2c8f901fe563abe432eb9c3f0e74c8`。
- 逐檔權威清冊：`workplace/inventory/manual-extracted-manifest.json`；每筆對照另保存實際
  掃描檔 SHA-256，驗證器會與此清冊比對。
- OCR：`rapidocr-onnxruntime 1.4.4`；Docker image
  `tvg-magazine-ocr:rapidocr-1.4.4`，image ID
  `sha256:4a6ab732b5eaacb9a1db27e2071e927ef07f9b00670451fd0e833e94b069ebf1`。
- OCR 搜尋收據只留在被忽略的 `workplace/manual-ocr/`：
  - `phase13-early-pages.json`：
    `b68b0b1c3df305a9848d7137c470aeaf95d250d07aa7f4a7c72f57548eef3304`
  - `phase13-more-pages.json`：
    `4e9b9ab3d8a4f25f959a20339f1e0c05c614c2e383493ab1af080cc38efc8b21`
  - `phase13-pages.json`：
    `10a9b7caf5351973091ab9f618587b22f2c8a265ba1d17d65e9eec2f14bc154d`

OCR 僅用來搜尋章節／條目；結論另以印刷頁碼、原圖標題、英文並列詞或具名劇情內容回查。
OCR 誤字沒有複製進正式中文 catalog。

## 冊別與頁序

第一個 `2F3_SCAN1240_*` 序列是操作說明，並非遊戲手冊查詢所引用的冒險者日誌。題目來源
位於第二個 `SCAN0352_*` 序列：

- 規則題依章節語意落在 `SCAN0352_004..025`。
- 生物與旅程條目落在 `SCAN0352_026..043`；條目編號提供比單純頁差更強的定位。
- 附錄及技能表落在 `SCAN0352_044..046`。
- `SCAN0352_046.jpg` 最後只見印刷頁 87；後續 `047..049` 是磁片／包裝影像，不含下一頁
  手冊內容。因此 `Roll.` 維持 `unknown`，不是「尚未搜尋」。

不能把原版頁碼全程套用固定偏移。`Deimos Prison` 的原版第 34 頁確實對到繁中印刷頁 73，
但後段技能表必須用附錄標題與中英並列欄名定位。

## 分級結果

權威逐筆資料在 `text/manual-source-crosswalk.tsv`：

| 等級 | 筆數 | 判準 |
| --- | ---: | --- |
| `confirmed` | 35 | 中英標題並列、明確中文對譯，或具名條目／人物／事件唯一吻合 |
| `strong-inference` | 3 | `More on Abilities`、`Money`、`Salvage` 的內容唯一吻合，但繁中版改了或省略總標題 |
| `unknown` | 1 | `Roll.`；所需頁面未包含在素材中 |

第二種不同結構的驗證錨點是 `Technical Skills`：它不是旅程條目，而是在
`SCAN0352_046.jpg` 印刷頁 87 的 `TECHNICAL SKILLS：技術性技能` 表格欄，與題庫第 38 筆
直接吻合。這與既有 `Deimos Prison` 的具名旅程條目共同證明配對方法涵蓋不同頁型。

## 可重生驗證與權利邊界

`tools/manual_crosswalk.py` 失敗即關閉檢查：

1. 題庫與對照表都必須恰有 39 筆，且 record、頁碼、英文標題逐筆相同。
2. 狀態只接受 `confirmed`、`strong-inference`、`unknown`。
3. 前兩者必須有檔名、archive-order、SHA-256、印刷頁與中文錨點。
4. `unknown` 必須清空假來源並填寫原因。
5. 提供解壓 manifest 時，每筆掃描 SHA-256 必須吻合。

版控只保存短小來源錨點與 metadata，不保存掃描、整頁 OCR 或可重建手冊的全文，也不保存
答案。來源映射完成不等於段落校字、覆繪實作或原版驗證已完成。
