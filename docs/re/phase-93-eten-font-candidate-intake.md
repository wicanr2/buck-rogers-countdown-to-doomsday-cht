# 第九十三階段：倚天字型候選輸入盤點

日期：2026-09-22  
輸入權利分類：使用者本機第三方字型／安裝媒體；唯讀研究輸入，不可加入 Git 或散布。

## 目的

驗證使用者指定的 `/home/anr2/cht/etan_font` 是否提供足以進入字型 DRAFT 的實際 15 點字模，並把
字型來源、Big5 coverage 與權利缺口同時留下可追溯記錄。本文件不保存字模位元、完整 README 或
授權文字。

## 可重現方法

在 Docker `python:3.12-slim`，`--network none`、`--user 1000:1000` 下，唯讀掛載候選目錄及專案，
執行下列類型的檢查：

1. 對候選 `STDFONT.15`、`SPCFONT.15`、`SPCFSUPP.15`、`ASCFONT.15` 記錄大小與 SHA-256，並驗證
   30-byte／15-byte stride 整除。
2. 以正式命令重生手冊 character list，驗證 691 entries 與既有 SHA-256。
3. 對每一個 Unicode code point 做 Big5 編碼、分區索引、檔案 bounds 與非空 glyph 檢查；空白字元
   是唯一允許的全空 glyph。輸出只包含類別計數、缺字計數、索引與 ink 統計，沒有 glyph bytes。
4. 搜尋候選目錄的標準授權檔名，並只對非空 README 做 CP950 可解碼性與授權關鍵詞計數；不輸出其內容。

## 觀測結果

| 結論 | 分級 | 證據 |
| --- | --- | --- |
| 16×15 漢字與符號來源均存在 | 已證實 | `ET353S/FILES/STDFONT.15` 是 392,820 bytes（13,094 entries），`SPCFONT.15` 是 12,240 bytes（408 entries）；完整 hashes 見 spec 007。 |
| 半形來源存在 | 已證實 | `ET353S/FILES/ASCFONT.15` 是 3,840 bytes（256 entries）。 |
| 691 glyph 全部有對應字模位置 | 已證實 | 44 ASCII、12 symbol、634 common CJK、1 secondary CJK；missing 0，除了 `U+0020` 外 nonblank 缺口 0。 |
| Big5 分區沒有整體偏移 | 強推論 | `一`／`中`／`猴` 分別落在 entry 0／66／2,690，均 in-bounds 且有 ink；尚未在本機畫面完成視覺錨點對照。 |
| 字型版本及媒體與解出檔的關係 | 未知 | `ET353S.iso` 與 `ET353S/FILES/` 均存在，但本階段沒有掛載／解讀 ISO 來證實來源關係，也不由路徑名稱推定版本。 |
| 完整授權或嵌入許可 | 已證實為缺席 | 沒有標準授權檔名；兩份非空 README 沒有授權／permission 關鍵詞。這是本機告知缺席的證據，非法律結論。 |
| 15→16 及 8→16 對齊 | 未知 | 現有 runtime 格式強制 16×16，而候選是 16×15／8×15；尚未做可丟棄對照或使用者視覺決策。 |

## 結論

倚天候選已解除「沒有實際字模」的缺口，並可覆蓋現有手冊字元；但沒有解除完整授權告知與
16×15／8×15 轉 16×16 的選擇。其後續規格為 DRAFT
[`007-eten-15-font-candidate-intake-draft.md`](../spec/007-eten-15-font-candidate-intake-draft.md)；
不得建置字型、接入 runtime 或聲稱玩家可見手冊中文已完成。
