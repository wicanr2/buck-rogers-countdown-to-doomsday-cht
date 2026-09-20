# 字型建置入口

本目錄只保存可重生的字元需求，不提交第三方字型或生成的 `GOLEMFNT` 二進位。
`characters.txt` 必須只由正式 TSV 的 `translation` 欄透過
`tools/catalog_font.py chars` 產生；不得手工加入未使用字元。

目前 prototype 使用本機 GNU Unifont 作測試輸入，不代表正式產品字型決策。該輸入的
授權檔明載 GNU GPL 2+（含字型嵌入例外）與 SIL Open Font License 1.1 條款；任何散布前
仍須連同實際採用版本重新核對完整授權文字與必要告知。

建置及驗證命令見 [`text/README.md`](../text/README.md)。
