# 第八十八階段：手冊正式 GOLEMFNT 子集來源稽核

日期：2026-09-21  
dosgolem 本機分支：`buck-rogers-cht-output-overlay`  
dosgolem 本機提交：`3fc37fe2908c7247447e34dfe18ae3b44855b534`（未推送）  
狀態：**DRAFT 稽核完成；正式候選缺席**

## 已證實事實

- Docker 從正式 `text/manual.zh-TW.tsv` 重生 `workplace/phase88/manual-characters.txt`：691 行，
  SHA-256 為 `dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f`。這只保存譯文
  使用的碼點清單，不含原版或手冊全文。
- 在唯讀 `workplace/` 盤點 `.hex`、`.hex.gz`、`.bdf`、`.pcf`、`.ttf`、`.otf`、`COPYING*`、
  `LICENSE*` 與 `OFL.txt`；除 dosgolem 自身 `LICENSE` 外，沒有原始字型候選或實際授權檔。
- 十份既有、被忽略的 GOLEMFNT 歷史產物皆為 16×16，但 glyph count 是
  24／24／56／77／74／5／47／81／8／15，最大 81，無法覆蓋 691；其 format 也不保存可供
  回查的發行版本、原始輸入或授權文字。
- `tools/catalog_font.py build` 在候選輸入不存在時以 nonzero 結束，並未產生輸出檔；此失敗即關閉
  行為已在 Docker 驗證。

## DRAFT 結論

dosgolem spec 218 將候選檔、雜湊、完整授權告知、691 glyph coverage 與 GOLEMFNT 回讀列為
READY 前置，並明確區分「本機可重生」和「可公開散布」。目前沒有能填入 manifest 的真實候選，
所以沒有新增 GOLEMFNT、runtime flag、字型 loader 或 presenter 接線，也沒有對 GNU Unifont 或
任何其他字型作採用／發行聲明。

## 下一個必要決策

需要使用者提供本機候選字型與完整授權文字，或明確授權取得一個指定候選，才能讓 spec 218
進入 READY。收到前，第八十七階段的 fixture font 只能供純核心測試，不能顯示正式手冊繁中。
