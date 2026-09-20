# 第十四階段：首批短篇繁中手冊段落校訂

## 結論

八筆來源已證實、位於單一短段落的手冊內容完成原圖校訂，加入 `text/manual.zh-TW.tsv`；
連同既有 `Deimos Prison`，目前共有 9 筆可顯示段落。`text/manual-events.tsv` 將每筆
`page + heading_ascii + ordinal` 唯一綁定到 `text_key`，沒有答案欄或自動輸入資料。

本階段不處理長章節、表格、跨頁內容、3 筆強推論或缺頁的 `Roll.`，因此沒有暗中決定分頁
格式。規格仍是 DRAFT，也尚未把這些資料接入 dosgolem production path。

## 原圖校訂收據

裁切由原始 2208×1091 雙頁 JPG 以 ImageMagick 取左／右半頁產生，只留在被忽略的
`workplace/manual-crops/phase14/`。原始掃描 SHA-256 由
`text/manual-source-crosswalk.tsv` 指向；裁切 SHA-256 如下：

| 題目 | 印刷條目 | 裁切檔 | SHA-256 |
| --- | --- | --- | --- |
| `The Elevator` | 11. 昇降機 | `elevator.jpg` | `4adf0d2399a00e3f97f314e2869bc617336d3a1ac945cbbff702006380655632` |
| `The King in 0-G` | 18. 無重力狀態下的蛙王 | `king-zero-g.jpg` | `a3ccaddf4478ebbe86d6a58bc67a90c8d6820e1bf93e03d7d89623017b7d79ce` |
| `Jupiter Arrival` | 32. 抵達木星 | `jupiter-arrival.jpg` | `639112feaee9233f52a6022b2495c2448c2d75658ee48f11d91efdc8e439cca8` |
| `The Great Rift` | 43. 大裂縫 | `great-rift.jpg` | `ffaf7f58606ad8a882555a378a6c1ae6f1d003272977cdc397e32f9f4da76562` |
| `Buck's Capture` | 56. 巴克羅吉斯被捕 | `buck-capture.jpg` | `b3fa875943a86fd44ea7c6090a2b6a66687140dded54a9462df887fa195337a0` |
| `Acidic Victory` | 57. 蛙王的勝利 | `acidic-victory.jpg` | `e0c38ab74195a0e3618e7f67be40bdf15738a2eec30bf845a12432a9f49bd79d` |
| `Alert Screen` | 63. 閃爍的螢幕 | `alert-screen.jpg` | `3a2f0ce517240d369ce093feda0397104c3b211bc505fdb357886bfe10125994` |
| `Lens Treatise` | 68. 有關鏡片的消息 | `lens-treatise.jpg` | `54a236fe132904e5eaed609c29c33cf4416ad66194848e90dbaa3d5ca8a65440` |

文字逐字回查原圖；只正規化全／半形空白、拉丁詞與中文間距、引號／省略號，以及不改變語意
的明顯排印字形。沒有從 OCR JSON 複製文字。`source=manual-and-runtime` 表示中文內容來自
手冊、事件識別來自原版執行期題庫，不表示八題都曾由正常玩家路徑實際抽中。

## Catalog 與長度

| `text_key` | Unicode 字元數 |
| --- | ---: |
| `manual.log.11.the_elevator` | 162 |
| `manual.log.18.king_in_zero_g` | 77 |
| `manual.log.32.jupiter_arrival` | 236 |
| `manual.log.43.great_rift` | 71 |
| `manual.log.49.deimos_prison` | 73 |
| `manual.log.56.bucks_capture` | 119 |
| `manual.log.57.acidic_victory` | 101 |
| `manual.log.63.alert_screen` | 35 |
| `manual.log.68.lens_treatise` | 100 |

字元數只是後續排版輸入，不是「能放進一頁」的證據。現行 TSV 每筆仍是一個不含控制字元的
單行段落；長章節如何分段、換頁或保留表格，留待玩家可見 prototype 與使用者決策。

## 失敗即關閉驗證

`tools/manual_catalog.py` 同時讀取題庫、來源對照、事件表及繁中 catalog，要求：

1. 事件的 record、頁碼、英文標題及序數與原版題庫逐項相同。
2. 只有 `confirmed` 來源可以成為顯示事件。
3. `event_key` 內的頁碼與序數必須和 typed 欄位一致。
4. 事件鍵、文字鍵皆唯一，每個文字鍵存在於 catalog，catalog 也不能有未映射孤兒。

19 項相關單元測試、catalog lint 及真實四檔交叉驗證全數通過。這證明資料內部一致與來源
資格，不證明 dosgolem 覆繪、分頁或正常玩家路徑已完成。
