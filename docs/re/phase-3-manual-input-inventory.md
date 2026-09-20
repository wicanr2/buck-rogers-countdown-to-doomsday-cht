# 第三階段：中文手冊輸入清冊與頁面定位

日期：2026-09-20  
狀態：archive 清冊與逐檔雜湊已完成；手冊語意與遊戲題目對應仍未知。

## 權利與輸入邊界

`珍074-拯救地球.rar` 是使用者自備、只限本機研究的原作手冊／補完材料。其 SHA-256 為
`4d018c13cf2d7aa632435f8c03042bf42a2c8f901fe563abe432eb9c3f0e74c8`。archive、解壓 JPG、
文字檔及其完整可還原內容都只留在被 Git 忽略的 `workplace/`；本文件不含手冊影像、全文、
OCR 或可用來重建頁面的內容。

## 可重生工具收據

| 項目 | 值 |
| --- | --- |
| Docker 映像 | `coab-manual-extract:bookworm-v1`，`sha256:80b9eb0d0f6d7c22c205196a14ca54ee5e21411b0454d6bf733794e0a534fee5` |
| 工具 | `lsar`／`unar` 1.10.1 |
| 條件 | `--network none`、RAR 唯讀掛載、輸出以 UID/GID 1000 寫入 `workplace/` |
| 列舉清冊 | `workplace/inventory/manual-rar-list.json`，SHA-256 `1f675b8ae4094cecc721b1d0574d152de44aca33953c44a23d0425bbb6251ca4` |
| 完整性收據 | `workplace/inventory/manual-rar-test.log`，SHA-256 `a4d032692555f5eced1adc69a7756f8231e179093b3d7582cfa0f2f185853440`；80 passed、0 failed |
| 解壓檔清冊 | `workplace/inventory/manual-extracted-manifest.json`，SHA-256 `aa4e135b2da63d6c92a94d0a7cf73f17843b1d0f0312ce0a9eaba5ca80de01a4`；79 個實體檔案逐一記錄大小與 SHA-256 |

archive 共有 80 個項目、未壓縮總量 51,002,564 bytes；其中 77 個 JPG、1 個 `Thumbs.db`、
1 個文字檔與 1 個根目錄項目。壓縮方式為 31 個 `Normal v2.9`、49 個未壓縮項目。這是
archive metadata，不宣稱已理解任何頁面內容。

## 頁面定位索引

頁面序列採 archive 的 `XADIndex`，不是印刷頁碼，也不是以 OCR 推定的章節順序。每個
項目的檔名、大小、RAR CRC32、archive index 與解壓 SHA-256 都在上述兩個被忽略清冊中。

| archive index | 檔名序列 | JPG 數 | 定位用途 |
| --- | --- | --- | --- |
| 0–27 | `2F3_SCAN1240_000a.jpg`、`000b.jpg`、`001.jpg` 至 `026.jpg` | 28 | 第一個掃描序列；之後以 index＋檔名＋雜湊引用，不假定其實體頁碼。 |
| 28–76 | `SCAN0352_001.jpg` 至 `SCAN0352_049.jpg` | 49 | 第二個掃描序列；同樣只作手冊段落候選定位。 |
| 77–79 | `Thumbs.db`、`軟體世界說明書補完計劃.txt`、根目錄 | 0 | 非頁面項目；不作遊戲內手冊段落來源。 |

未來只有在原版正常路徑實際顯示手冊題目、並有題目輸出事件證據時，才可把一筆
`archive index + filename + extracted SHA-256` 加到翻譯／手冊索引。此階段沒有做題目配對、
頁面語意判讀或中文顯示。
