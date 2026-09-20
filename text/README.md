# 文字目錄

本目錄保存 UTF-8 繁體中文顯示文字；鍵值只供 dosgolem 輸出端覆繪查詢，不得回寫原版
記憶體、規則、驗證答案或存檔。原版完整字串清冊與受著作權保護素材不納入 Git。

目前 `menu.zh-TW.tsv` 僅是第八階段已由正常玩家路徑及中文說明書共同證實的 DRAFT。
`menu-events.tsv` 以事件鍵、正式文字鍵、原文長度／SHA-256、caller、色號與文字格座標保存
同一路徑的九筆 typed identity；不保存原文全文。`tools/menu_events.py` 驗證 schema、順序、
唯一性、bounds 與 `menu.zh-TW.tsv` 雙向覆蓋。
`post-race-events.tsv` 保存選定預設種族後性別畫面的四筆 content-safe identity；目前只有
原版事件證據，尚未加入繁中 catalog 或正式 renderer。`tools/post_race_receipt.py` 會把它
與既有選單 inventory、固定雙 Enter 收據及終點 framebuffer 一起驗證。
`manual-questions.tsv` 是原版 39 筆可抽題的頁碼、標題與序數清冊，不含答案；可由
`tools/manual_questions.py` 對執行期 `0EC0:0000` 資料段重生。`manual.zh-TW.tsv` 只收錄
已唯一核對中文掃描來源並回到原圖校字的段落，目前共有 22 筆。

`manual-ordinals.tsv` 保存原版 1–10 序數詞、runtime 位址與完整 19-byte slot；可由同一份
執行期資料段透過 `tools/manual_ordinals.py` 重生。它只橋接題目顯示身分，不含答案。

`manual-source-crosswalk.tsv` 逐筆記錄題目對應掃描、archive-order、SHA-256、印刷頁、
中文錨點與證據等級。它是來源索引，不是可直接顯示的譯文 catalog；OCR 未經逐字校訂的
內容不得搬入 `manual.zh-TW.tsv`。可用下列命令搭配本機解壓清冊驗證：

```sh
python3 tools/manual_crosswalk.py text/manual-questions.tsv text/manual-source-crosswalk.tsv \
  --manifest workplace/inventory/manual-extracted-manifest.json
python3 tools/manual_catalog.py text/manual-questions.tsv text/manual-source-crosswalk.tsv \
  text/manual-events.tsv text/manual.zh-TW.tsv
python3 tools/manual_ordinals.py workplace/probe/phase12-manual-runtime-0EC0_0000.bin \
  text/manual-ordinals.tsv --events text/manual-events.tsv
python3 tools/menu_events.py text/menu-events.tsv text/menu.zh-TW.tsv
python3 tools/menu_receipt.py workplace/phase27/menu-receipt.json \
  text/menu-events.tsv text/menu.zh-TW.tsv
```

`manual-events.tsv` 是 DRAFT 事件映射：只允許來源為 `confirmed` 的題目，以頁碼、英文標題及
序數精確指向一筆文字鍵。它不含英文答案，也不會送鍵或改寫原版記憶體。

## 驗證與 prototype 字型

以下命令必須在專案規範要求的隔離 Docker 容器內執行：

```sh
python3 tools/catalog_font.py lint text/menu.zh-TW.tsv
python3 tools/catalog_font.py chars text/menu.zh-TW.tsv --out font/characters.txt
python3 tools/catalog_font.py build text/menu.zh-TW.tsv \
  --font /inputs/unifont.hex.gz \
  --out workplace/font/menu-unifont16.golemfnt
```

`lint` 失敗即關閉地驗證 UTF-8、精確標頭及欄數、唯一 key、非空譯文、來源枚舉、控制／
格式字元與 NFC。`chars` 依 Unicode 碼點排序，每行固定為 `U+XXXX<TAB>字元`；字型建置若
缺任一字模、遇到非 8×16／16×16 字模或格式錯誤便中止。
