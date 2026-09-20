# 文字目錄

本目錄保存 UTF-8 繁體中文顯示文字；鍵值只供 dosgolem 輸出端覆繪查詢，不得回寫原版
記憶體、規則、驗證答案或存檔。原版完整字串清冊與受著作權保護素材不納入 Git。

目前 `menu.zh-TW.tsv` 僅是第八階段已由正常玩家路徑及中文說明書共同證實的 DRAFT。

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
