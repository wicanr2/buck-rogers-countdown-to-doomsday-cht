# 第一百一十二階段：手冊轉向按鍵與可逆 command/status 重播

日期：2026-09-22
狀態：**已用手冊明示的數字鍵盤 4／6 完成一次輸入 pair；終態畫面回復，但尚未證明左右轉向實際生效。**

## 手冊證據

英文手冊本機快照 `workplace/buckrogers-original-manual-english.html` 的 SHA-256
為 `e8528a31b66d76e7162abe358bff1f27d7d5a5d4070914beee470867e59e728a`。其第 6
頁只說方向控制依 Data Card，未指定本機鍵位，因此不單獨拿它送鍵。

使用者提供的中文掃描原圖明示了本機鍵位：

- `2F3_SCAN1240_007.jpg`（印刷頁 10，SHA-256
  `fb753f5889012f76ae7e8f58ebf765e32bfcc19ad7001dce2b69f3f30483c7e4`）：數字
  鍵盤 8／4／6／2 對應前進／左轉／右轉／後退的方向圖。
- `2F3_SCAN1240_008.jpg`（印刷頁 11–12，SHA-256
  `28d1c1c21b3de5b2af7cb63e79ecbe9075e08a3bca1525cd5e4398947b959ea7`）：延續
  鍵盤方向圖，並列出 Esc、Alt+Q 等其他控制；本輪不送這些鍵。

既有 OCR 清冊 `workplace/manual-ocr/phase13-pages.json`（SHA-256
`10a9b7caf5351973091ab9f618587b22f2c8a265ba1d17d65e9eec2f14bc154d`）只作頁面
定位，原圖才是按鍵證據；OCR 文字不進 Git。

## 輸入 pair 與中間狀態

從 `workplace/phase104-post-return-enter-3/control.state`（300M 終態）開始，
在 Docker 內送出：

- `302000000:4b:00`：數字鍵盤 4，左轉
- `304000000:4d:00`：數字鍵盤 6，右轉

dosgolem 收據 `workplace/phase112-command-turn/turn.json` 的 SHA-256 為
`4422f1dbec6c862f011143d0a873959bc8e76bc507e8f6936503dd7d232a2cab`。兩個按鍵
都被 BIOS 收取，未產生高階 action event；各自重畫同一筆 row 24 文字：

- caller：`37F1:0337`（segment 14321、offset 823）
- row 24、column `0..32`、背景 15、前景 0
- `original_length=33`
- identity SHA-256：`00df727dbe5dc2fd691488463bb9a24f7b951bb3d37ac4c142b59996adf555ea`

為確認不能只看終態，另以相同 300M state 在只送 4 鍵、於 303M 停止的中間
收據 `workplace/phase112-command-turn/intermediate/left.json` 重播。其 indexed
framebuffer SHA-256 是 `9bb708331258b5239c1bfd7b299c0594c4be4475b0523b07c40387790db3958c`，
與無輸入基準 `workplace/phase112-command-turn/intermediate/base.indexed`
及既有 `phase104-post-return-enter-3/control.indexed` 相同。中間 trace 只有
row 24 的 33-cell glyph run，沒有地圖區、方向指示或座標欄的 indexed 差異，
也沒有高階 action event 或可直接解讀的方向／座標 state。因此證據只支持
「手冊標示的 4／6 輸入 pair，終態畫面回復」，不支持「原版左右轉向已生效」
的結論。

中間收據 `left.json` SHA-256 為
`7815c8a21907cd98019b999934fdf13fd15c32106dbbfdea4d518b9ee8f4bc76`；無輸入
基準 `base.json` SHA-256 為
`ec3875b24e637900e1ff5e69eee125fcc6dc3702c65760fd26b1aab84ba05e93`。兩份 state
因執行步／時鐘欄位不同而不能以 raw state 雜湊判斷動作；本輪採 indexed frame、
glyph trace 與高階 event 欄位作內容安全比較。

## 分類與停止線

- row 24：新增 33-cell command/status identity；維持原文與 miss。兩次輸入的
  identity 相同，但沒有第三種狀態可分離固定標籤與動態值。
- 上方角色名稱／數值：本輪沒有新增 glyph run，維持原文與 miss。
- 固定介面詞：本輪沒有取得可證實的不變詞，因此不新增 DRAFT TSV、validator
  或安全矩形。

下一個有界步驟是以手冊同樣明示、且不改規則的另一種合法輸入取得不同狀態；在
那之前不得把 33-cell row 24 內容拆成固定中文詞或接入 runtime。
