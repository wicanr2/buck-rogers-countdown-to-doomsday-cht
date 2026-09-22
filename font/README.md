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

使用者提供候選與完整授權文字後，必須先在 Docker 內執行候選審查：

```sh
python3 tools/catalog_font.py validate-candidate text/manual.zh-TW.tsv \
  --manifest workplace/phaseNN/input/candidate-manifest.json \
  --source workplace/phaseNN/input/candidate.hex.gz \
  --license workplace/phaseNN/input/COPYING
```

命令只輸出檔名、SHA-256、format／version 與 glyph count metadata，不寫入 GOLEMFNT。它要求 strict
manifest、來源與授權文字雜湊、691 glyph coverage、`local-validation-only` 與 `undecided` 發行狀態；
通過只代表候選可進入後續權利審查，不代表採用、嵌入或可散布。

第九十三階段已依使用者指定，唯讀盤點本機倚天 `ET353S/FILES/` 的 15 點字模；其對正式手冊 691
碼點的定位結果、檔案雜湊與停止線見
[`docs/spec/007-eten-15-font-candidate-intake-draft.md`](../docs/spec/007-eten-15-font-candidate-intake-draft.md)。
它不是既有 Unifont validator 的輸入：候選仍缺完整授權告知，且 16×15／8×15 至 runtime 16×16 的
對齊尚未經 prototype 與使用者決定，因此不得建置任何字型產物。
