# 第九十五階段：倚天 top-pad parser 的格式與索引證據

日期：2026-09-22
對應工作：[GitHub Issue #12](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/12)
輸入權利分類：使用者已購買並明確授權的第三方字型，僅限本機遊戲使用；原檔、衍生字型與預覽均不進 Git、GitHub、Release 或公開封包。

## 方法與輸入

在 `python:3.12-slim` 一次性、無網路 Docker 容器中，以唯讀掛載讀取正式
`text/manual.zh-TW.tsv` 與下列三個倚天字模。探針不寫入任何字型、圖片或原始內容，只輸出集合數與摘要雜湊。

| 角色 | 相對於本機倚天媒體的路徑 | bytes | SHA-256 |
| --- | --- | ---: | --- |
| 半形 | `ET353S/FILES/ASCFONT.15` | 3,840 | `1d0cf09d0a319a9e7039190688c6a905ba4370bd369fbfcfa43b2078480d6918` |
| 全形符號 | `ET353S/FILES/SPCFONT.15` | 12,240 | `f32049ba2a7a21db908878a488a2c1d93c389d17398cf46db1390ba89e247605` |
| 標準漢字 | `ET353S/FILES/STDFONT.15` | 392,820 | `39ba9c8519d75fe11d5988a8a27e6daa5794ad2ea215108390b0d7e9e53ff701` |

正式 catalog 字元集合為 691 個碼點，清單 SHA-256 是
`dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f`。本次將每一個碼點的
Unicode、Big5 bytes、來源區與 entry index 序列化後，只記錄其摘要
`761776561142c97c3e53b7d275f4a535379dd2d88d359b14dbe747093b4738f0`，不把字模 bytes 寫入文件。

## 已證實的索引規則

對合法 Big5 pair `(hi, lo)`，先計算 raw index：

```text
column(lo) = lo - 0x40,  若 0x40 <= lo <= 0x7E
           = lo - 0x62,  若 0xA1 <= lo <= 0xFE
raw(hi, lo) = (hi - 0xA1) * 157 + column(lo)
```

非法 lead、trail 與未列出的 raw 區間都失敗即關閉。已由來源檔長度與端點探針共同驗證的分區如下：

| raw 範圍 | Big5 範圍 | 來源與 entry | 分級 |
| ---: | --- | --- | --- |
| 0..407 | `A140..A3BF` | `SPCFONT.15[raw]` | 已證實 |
| 471..5,871 | `A440..C67E` | `STDFONT.15[raw - 471]`，0..5,400 | 已證實 |
| 6,280..13,972 | `C940..F9FE` | `STDFONT.15[5,401 + raw - 6,280]`，5,401..13,093 | 已證實 |

因此 `STDFONT.15` 的 13,094 格精確等於常用區 5,401 格加上次常用區 7,693 格；不能把目前 catalog
只有一個次常用字（`C9AB`）誤寫成 parser 的單點特例。`A3C0`、`C6A1`、`C840` 等保留區已由探針確認遭拒。
`SPCFSUPP.15` 沒有目前 catalog consumer，不得作為靜默 fallback；若未來需要它，必須另開資料／規格工作。

## 編碼、字形與對齊收據

- 容器內 CPython 3.12 的標準 `big5` codec 對 691 個正式碼點皆產生恰好兩 bytes；ASCII 則直接以 0..255
  entry 取 `ASCFONT.15`。codec 無法編碼、輸出非兩 bytes 或落在未證實分區時都必須失敗即關閉。
  現行集合沒有 `U+FF5E` 等已知歧義碼點；未來出現時不得靜默替換，必須先新增逐碼點對照與測試。
- 探針結果為 ASCII 44、`SPCFONT.15` 12、標準常用區 634、標準次常用區 1；唯一全空 glyph 是
  `U+0020` 空白。其餘 690 格都有 ink。
- 使用者已選擇 `top-pad`：16×15 CJK glyph 的 raw 30 bytes 前置 `00 00`；8×15 ASCII 的每列先左移
  4 bits 成為 MSB-first 16-bit row（x=4..11），再前置 `00 00`。因此 runtime 16×16 glyph 的 row 0 恒為零，
  source rows 0..14 精確寫到 output rows 1..15；`bottom-pad` 已排除。
- dosgolem `xlate.LoadFont` 已證實只接受嚴格長度的 `GOLEMFNT`：magic 8 bytes、little-endian
  `W=16`／`H=16`／glyph count，接著每 glyph 為 Unicode `u32`、來源 tag `u8`、32 bytes bitmap。手冊
  `RuntimeManualOverlay` 建構時會檢查所有正式碼點皆存在且每格為 32 bytes，故 parser 不能部分成功。

## 可重生摘要與結論

探針以 256／408／13,094 三個來源格數、所有端點與保留 gap、691 個 catalog glyph、top-pad row 0 與
ASCII x=4..11 同時驗證。結果沒有缺字、越界或非預期空白。上述格式、分區、codec、對齊與 runtime 載入
邊界均為**已證實**；本機 parser 的實作尚未開始，故本文件不宣稱已建置或已接入遊戲。

正式前景色來源屬 #13，presenter 的正常玩家接線屬 #14，兩者不由本收據推定。
