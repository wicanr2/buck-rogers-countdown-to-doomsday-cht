# 008 — 倚天 top-pad 本機字型建置器

狀態：CONFORMED（本機字型建置器）
日期：2026-09-22
前置：[倚天 15 點字型候選輸入契約](007-eten-15-font-candidate-intake-draft.md)、
[第九十五階段索引證據](../re/phase-95-eten-top-pad-parser-evidence.md)、
[手冊繁中輸出端 presenter 整合](005-manual-runtime-presenter-draft.md)。
後續實作：[GitHub Issue #15](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/15)。

## 目的與停止線

本規格只定義一個供使用者本機使用的倚天 15 點 → 16×16 `GOLEMFNT` 建置器。它從正式 UTF-8
手冊及介面
catalog 導出 glyph 集合，對固定身份的本機字型檔做 Big5 索引，並產生可被 dosgolem `xlate.LoadFont`
讀取的二進位。它不是字型散布器、授權意見、遊戲安裝器、前景色決策、手冊 presenter 接線，亦不改寫
原版 EXE、VRAM、輸入、答案判定、存檔或任何遊戲資料。

實作位置預定為獨立的 `tools/eten_font.py`；它可重用 `tools/catalog_font.py` 的 UTF-8 TSV 驗證與
決定性碼點排序，但不得改變或放寬既有 Unifont parser、`build`、`validate-candidate` 的語意。這是本機
建置前置工具，不進入 dosgolem 的遊戲迴圈；#14 只能在此規格 READY 且產物經本機驗證後，才選擇性載入其
輸出給已存在的 `xlate.Font`／`RuntimeManualOverlay`。

原檔、完整媒體、衍生 `GOLEMFNT`、sidecar manifest 與預覽一律只能留在被忽略的 `workplace/`。不得加入
Git、GitHub Issue、Release、公開封包或可散布 fixture。

## 預定命令與 typed input

正式命令如下；必須在 Docker 內使用本機唯讀字型來源：

```text
python3 tools/eten_font.py build text/manual.zh-TW.tsv \
  --asc /local/ET353S/FILES/ASCFONT.15 \
  --spc /local/ET353S/FILES/SPCFONT.15 \
  --std /local/ET353S/FILES/STDFONT.15 \
  --out workplace/local-font/buckrogers-eten-top-pad.golemfnt \
  --manifest-out workplace/local-font/buckrogers-eten-top-pad.json
```

`build` 必須接受一個或多個與現有 `catalog_font.py` 同 schema 的 UTF-8 TSV，先以既有嚴格 catalog
驗證讀入，再取排序、去重後的 Unicode codepoints。第九十六階段首版手冊為 691 glyph、
character-list SHA-256 `dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f`，
其固定輸出雜湊仍作歷史回歸。後續正式譯文增補必須更新測試收據並由正式 catalog
重建字模；多 catalog 可共享文字 key，但合併的是字元聯集，不可把跨檔重用誤判為重複翻譯。

三個 source argument 都必須是一般檔，並在任何解析前精確匹配下列 filename、byte length 與 SHA-256：

| argument | filename | bytes | SHA-256 |
| --- | --- | ---: | --- |
| `--asc` | `ASCFONT.15` | 3,840 | `1d0cf09d0a319a9e7039190688c6a905ba4370bd369fbfcfa43b2078480d6918` |
| `--spc` | `SPCFONT.15` | 12,240 | `f32049ba2a7a21db908878a488a2c1d93c389d17398cf46db1390ba89e247605` |
| `--std` | `STDFONT.15` | 392,820 | `39ba9c8519d75fe11d5988a8a27e6daa5794ad2ea215108390b0d7e9e53ff701` |

輸出與 sidecar 必須 resolve 在本 repository 的 `workplace/` 下；不存在的父目錄可在全部驗證通過後建立。
不得接受 `..` 逃離、符號連結逃離或 repository 外輸出。輸入原檔永遠唯讀。sidecar 只可記錄命令版本、
catalog SHA、source metadata、glyph count、output SHA 與本機／不可散布分類；不得含字模、原版或手冊全文。

## codec、分區與 glyph 轉換

非 ASCII 的每一 Unicode rune 必須以 CPython 標準 `big5` codec 編碼，且結果必須恰好是兩 bytes。不得
以忽略錯誤、替代字元、最佳努力或其他 codec fallback 繼續。若將來正式 catalog 新增 codec 歧義碼點，
必須先以明列的 Unicode→Big5 mapping、來源與 synthetic test 修訂本規格；第 1 版不可自動接納。

對合法 `hi,lo` 套用 `raw=(hi-0xA1)*157+column(lo)`，其中 `column` 與可接受 trail 如 phase 95
證據所示。唯一可讀分區是：

| 條件 | source tag | source entry |
| --- | ---: | --- |
| ASCII `U+0000..U+00FF` | 1 | `ASCFONT.15[codepoint]`，每格 15 bytes |
| raw 0..407 | 2 | `SPCFONT.15[raw]`，每格 30 bytes |
| raw 471..5,871 | 3 | `STDFONT.15[raw - 471]`，每格 30 bytes |
| raw 6,280..13,972 | 4 | `STDFONT.15[5,401 + raw - 6,280]`，每格 30 bytes |

其餘 valid Big5 raw range、`SPCFSUPP.15`、source 超界與未知 source tag 一律拒絕，不得 fallback。
每個 CJK 30-byte glyph 轉為 `00 00 + raw`；每個 ASCII source row 左移 4 bits 轉成 16-bit MSB-first
row 後，轉為 `00 00 + 15 rows`。這固定使用者選定的 `top-pad`：output row 0 為零，source rows 0..14
在 output rows 1..15，ASCII ink 在 x=4..11。`bottom-pad` 不得提供為參數或隱藏預設。

## 輸出、回讀與失敗即關閉

輸出必須是按 codepoint 遞增、唯一的 `GOLEMFNT`：`GOLEMFNT` magic、little-endian `W=16`、`H=16`、
glyph count 等於正式 catalog 字元聯集，及每格 `u32 codepoint + u8 source tag + 32-byte bitmap`。所有 glyph 生成完成後才可以
原子替換 `--out`；失敗不得留下新檔或覆蓋既有有效輸出。產出後需由 builder 自行嚴格回讀 header、總長、
codepoint 順序、tag、32-byte bitmap 與末端位置，並以 dosgolem `xlate.LoadFont` 做本機 integration 回讀。

除了 `U+0020`，任何全零 glyph 都失敗；任何缺 glyph、重複 codepoint、UTF-8／TSV 格式錯誤、catalog SHA
驗證失敗、codec 失敗、來源身份不符、非法／保留 Big5 區、索引超界、row 寬度不符、輸出／sidecar 路徑逃離、
header／回讀不符都必須以非零結束，且不繪圖、不改 VRAM、不啟動遊戲。

## 測試與審查條件

實作階段需有不含第三方字型 bytes 的 synthetic tests，至少覆蓋：三來源格數與雜湊拒絕、ASCII／SPC／常用／
次常用四分區、六個端點、三個保留 gap、codec／非兩 bytes 拒絕、top-pad row 與 ASCII x=4..11、唯一排序、
無非空 blank、GOLEMFNT round-trip、atomic failure 及 `workplace/` 路徑限制。使用者本機來源只可在 Docker
integration run 做實際 glyph 數與來源雜湊收據；公開 CI 在來源缺席時必須明確 skip，而不是下載、模擬或把字型塞進 fixture。

READY 審查已逐項確認上述 typed input、分區、codec、對齊、輸出、失敗模式、權利邊界與測試設計均無未知。
本機建置器已實作為 `tools/eten_font.py`，12 項合成測試涵蓋來源身份、分區端點、字模格式、輸出路徑與
第二次檔案替換失敗的回復。真實來源產出 25,583 bytes、691 字模，SHA-256 為
`78c10dec8055110764013007899c4455b91256a78f94e212294ac9c51c01364e`；dosgolem `xlate.LoadFont`
回讀為 16×16、691 字模。本工具的 CONFORMED 不代表全遊戲中文化或字型可公開散布。

第九十七階段擴充為多 catalog 並重建校正後正式譯文：10 份 catalog 聯集 760 glyph，
本機輸出 SHA-256 `6fb92d1bcde389ee02c2953cf175838f21be5dd8782f87aaad40c0837cb29624`；
校正後手冊單檔 707 glyph、character-list SHA-256
`71a67c4e475b0150ff65ea99c0d7666322485ae5884a414e6ce649a0d558bb45`。
以上為新增收據，未抹除首版歷史輸入與輸出。

## 2026-09-24：正式接線前的唯讀核驗

`tools/eten_font.py verify` 已新增唯讀核驗入口。它自行列舉 `text/*.zh-TW.tsv`
的完整正式集合，重算嚴格 TSV 字元聯集、固定身分的三個倚天來源、
`GOLEMFNT` 全部 bytes 與 canonical manifest bytes，並與 `workplace/` 中
既有兩檔逐 byte 比對；不修補或重建輸出。缺檔、catalog 增減／內容變更、
原始字型變更、字模或 sidecar 改動均拒絕。呼叫者在建立規格 024 的
手冊 owner 前，應於唯讀掛載的 Docker 容器執行：

```text
python3 tools/eten_font.py verify \
  --asc /etan/ET353S/FILES/ASCFONT.15 \
  --spc /etan/ET353S/FILES/SPCFONT.15 \
  --std /etan/ET353S/FILES/STDFONT.15 \
  --font workplace/current-font/buckrogers-eten-top-pad.golemfnt \
  --manifest workplace/current-font/buckrogers-eten-top-pad.json
```

此命令假設已將本機 `/home/anr2/cht/etan_font` 唯讀掛到容器 `/etan`，
專案唯讀掛到 `/project` 並以其為工作目錄；掛載前仍須核對來源存在。
`tools/test_eten_font.py` 的 15 項合成測試通過。實際唯讀核驗涵蓋
24 份正式 TSV、1,028 個字模，輸出 SHA-256 為
`150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
這只證明當次本機來源、譯文與字型產物一致；正式 Linux session 尚未
呼叫此核驗入口，不能據此宣稱啟動時已失敗即關閉或全遊戲中文化。
