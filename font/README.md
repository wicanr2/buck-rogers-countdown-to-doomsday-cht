# 字型建置入口

本目錄只保存可重生的字元需求，不提交第三方字型或生成的 `GOLEMFNT` 二進位。
`characters.txt` 必須只由正式 TSV 的 `translation` 欄透過
`tools/catalog_font.py chars` 產生；不得手工加入未使用字元。

歷史 prototype 曾使用本機 GNU Unifont 作測試輸入，不代表正式產品字型決策。第八十八階段
已證實目前 `workplace/` 沒有可回查的原始輸入或實際授權文字；舊 GOLEMFNT 產物也不能反推
來源或授權，因此不得當作正式候選。未來候選的授權檔若明載 GNU GPL 2+（含字型嵌入例外）及
SIL Open Font License 1.1 條款，仍須連同實際採用版本重新核對完整文字與必要告知；這不是
採用或可散布的聲明。

建置及驗證命令見 [`text/README.md`](../text/README.md)。
