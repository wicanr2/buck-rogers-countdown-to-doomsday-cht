# 第九十二階段：正式字型候選 manifest 驗證補強

日期：2026-09-21
dosgolem 本機分支：`buck-rogers-cht-output-overlay`
dosgolem 本機提交：`a4a87aad48607ea6ff6e4646de1292f5caaeade9`（未推送）
狀態：**CONFORMED（候選審查工具）**

## 已證實工具缺口與修正

第八十八階段已證實本機缺少候選 source 與完整授權文字；原有 `catalog_font.py` 只能由既有
Unifont parser 建置或驗證 glyph，不能把實際檔案與未來 manifest 的 filename、SHA-256、權利 metadata
連成可重現輸入。第九十二階段新增 `validate-candidate`，只接受被忽略工作區內的 candidate manifest、
source、license 與 catalog。

manifest 必須為 strict schema，且 source／license basename 與 raw SHA-256、character-list SHA、既有
`unifont-hex` format／conversion、`local-validation-only` 和 `undecided` 狀態皆須精確符合。license 必須是
非空 UTF-8 文字；既有 parser 必須找到每個 catalog glyph。成功的 JSON metadata 只列 filename、SHA、
format／version、scope／distribution 與 glyph count，絕不輸出 notice、license 或 bitmap。

## 合成驗證

Docker、無網路、唯讀專案輸入中通過：

```text
python -m unittest discover -s tools -p "test_*.py"  # 158 tests
python tools/manual_overlay_layout.py text/manual-overlay-layout.tsv text/manual.zh-TW.tsv
python tools/catalog_font.py lint text/manual.zh-TW.tsv
```

新增測試覆蓋 successful metadata／CLI stdout、metadata 不洩漏、缺欄、未知欄、source／license／character
hash 漂移、basename、format、conversion、scope、distribution、空 license、缺 source 與 coverage 缺口。
另以正式 `manual.zh-TW.tsv` 的 691 glyph 清單配上暫存 synthetic bitmap source 進行 coverage 測試；該
輸入在 test temporary directory 內消失，從未被標為 candidate、寫入 `workplace/`、建成 GOLEMFNT 或散布。

## 明確邊界

這是候選**審查工具**，不是字型採用或法律判定。它不能證明授權文字充分、允許嵌入或允許散布，也不能
選擇字型家族、取得來源或版本；這些仍等待使用者決定。本機仍沒有 candidate source／完整授權文字，
dosgolem spec 218 與 project spec 005 仍為 DRAFT，手冊中文尚未上畫面。
