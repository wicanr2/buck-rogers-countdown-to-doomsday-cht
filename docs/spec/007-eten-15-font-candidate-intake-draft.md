# 007 — 倚天 15 點字型候選輸入契約

狀態：DRAFT  
日期：2026-09-22  
前置：[手冊正式字型候選 manifest 驗證器](006-formal-font-candidate-manifest-validator.md)、
[手冊繁中輸出端 presenter 整合](005-manual-runtime-presenter-draft.md)、
[第九十三階段候選輸入盤點](../re/phase-93-eten-font-candidate-intake.md)、
[第九十四階段本機建置與對齊原型（prototype）](../re/phase-94-eten-font-local-build-prototype.md)。

## 目的與邊界

本規格記錄使用者指定之本機倚天候選的檔案身分、15 點 Big5 字模結構、對正式手冊字元清冊
（catalog）的覆蓋，以及本機採用已解鎖、公開散布與轉換仍未完成的界線。它不是公開採用宣告、
授權意見、`GOLEMFNT` 正式建置規格或繪製器（renderer）接線許可。

所有候選原檔、完整媒體與完整授權告知都只留在使用者本機的 `/home/anr2/cht/etan_font`；依使用者的
本機遊戲授權產生的衍生字模僅可留在被忽略的 `workplace/phase94/` 或後續明確本機輸出目錄。兩者都不可
加入本專案版控、dosgolem、GitHub Issue、Release 或可散布測試語料。受版控文件只保存必要中繼資料
（metadata）、SHA-256、格式結論與缺口。

## 候選清冊

以下檔案均在 Docker 中以唯讀掛載讀取；`ET353S/FILES/` 是本階段唯一選作候選字模組的路徑。目錄內
另有同名空白安裝媒體佔位檔，故不得依檔名自動挑選其他副本。

| 角色 | 本機相對路徑 | bytes | SHA-256 | 分級 |
| --- | --- | ---: | --- | --- |
| 漢字字模 | `ET353S/FILES/STDFONT.15` | 392,820 | `39ba9c8519d75fe11d5988a8a27e6daa5794ad2ea215108390b0d7e9e53ff701` | 已證實 |
| 全形符號字模 | `ET353S/FILES/SPCFONT.15` | 12,240 | `f32049ba2a7a21db908878a488a2c1d93c389d17398cf46db1390ba89e247605` | 已證實 |
| 符號補充字模 | `ET353S/FILES/SPCFSUPP.15` | 10,950 | `564e99411ce03cb11922d867dce24f8ac23dda4df17c2cdef362b8b22944e376` | 已證實；本 catalog 未使用 |
| 半形字模 | `ET353S/FILES/ASCFONT.15` | 3,840 | `1d0cf09d0a319a9e7039190688c6a905ba4370bd369fbfcfa43b2078480d6918` | 已證實 |
| 媒體容器 | `ET353S.iso` | 18,896,896 | `f8ab57aee05aa7b424bfbd63864adaebf94e5905b46006b5058a5988d5c216e4` | 已證實為存在；尚未證實與上述解出檔的來源關係 |

檔案大小分別整除為 `13,094 × 30`、`408 × 30`、`365 × 30` 與 `256 × 15` bytes。這符合
`STDFONT.15`／`SPCFONT.15`／`SPCFSUPP.15` 的 16×15（每列 2 bytes、MSB-first）及
`ASCFONT.15` 的 8×15（每列 1 byte、MSB-first）裸字模結構；由檔案長度證實結構可行，
不單獨證明字型名稱、版本或散布權利。

## 正式 catalog coverage 證據

以 `tools/catalog_font.py chars text/manual.zh-TW.tsv --out /tmp/manual-characters.txt` 重生正式集合：

- 22 筆 TSV、691 個不重複 Unicode 碼點；清單 SHA-256 為
  `dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f`。
- 以倚天 Big5 分區索引定位，44 個碼點由 `ASCFONT.15` 取得、12 個由 `SPCFONT.15` 取得、
  634 個由 `STDFONT.15` 常用區取得、1 個由 `STDFONT.15` 次常用區取得；缺字與越界均為零。
- 唯一全空字模是 `U+0020`，與空白字元預期相符；不得把它誤判為缺字。`SPCFSUPP.15` 在此集合沒有
  consumer，但保留於候選清冊，不能在未來 catalog 擴張時假定仍不需要。
- 以 `一`、`中`、`猴` 做結構錨點：各自落在 `STDFONT.15` entry 0、66、2,690，均為完整 30-byte
  範圍且有非零 ink。這證實本索引沒有整體位移；字形的視覺對味與垂直對齊仍須在本機 prototype
  中另行檢視，不能由 bit-count 取代。

本階段使用 Python `big5` codec 的 Unicode→Big5 轉換。正式 catalog 沒有觸發 `U+FF5E` 的手動
mapping；若未來譯文新增 codec 歧義符號，必須在資料規格新增逐碼點 mapping 與測試，不可靜默 fallback。

## 未完成的轉換與權利閘門

| 項目 | 分級 | 目前結論與停止線 |
| --- | --- | --- |
| 16×15→執行期（runtime）16×16 | DRAFT | 第 94 階段已以真實候選重生 `bottom-pad`／`top-pad`，兩案皆為 16×16、691 個字模（glyph），2×／3×範圍約束（containment）均通過。使用者已選定 `top-pad`：CJK 與 ASCII source row 0..14 寫入 runtime row 1..15，row 0 為零；`bottom-pad` 已排除。ASCII 水平沿用既有 16-bit 版面的 x=4..11。正式 parser、前景色與 runtime 接線仍未 READY。 |
| 倚天候選 parser | DRAFT | 既有 `validate-candidate` 僅支援 Unifont 十六進位字模，拒絕本候選是正確行為。只有本規格經 evidence review 升為 READY 後，才能新增獨立 ETen parser／manifest schema 與 synthetic tests。 |
| 完整授權告知 | 已證實為缺席 | 候選目錄沒有 `LICENSE*`、`COPYING*`、`COPYRIGHT*` 或 `NOTICE*` 一般檔案。兩份非空 `README.DOC` 可被 CP950 解碼，但沒有可辨識的授權、散布或權利許可條款。這不足以證明世界上不存在權利條款，卻足以證明本候選尚未提供本專案所需的完整告知。 |
| 本機採用／嵌入 | 已證實（使用者授權範圍） | 使用者已明確說明此為以前購買的字型，並授權直接用於本機遊戲。故可在被忽略的 `workplace/` 轉換與嵌入本機產物；這不是對第三方權利的法律判定。 |
| GitHub／公開散布 | 未獲授權 | 使用者的本機授權不等於公開再散布許可。原檔、衍生 `GOLEMFNT`、媒體、完整告知與字模預覽均不得進 Git、GitHub Issue、Release 或公開封包。 |
| 正式前景色來源 | DRAFT | 本階段固定手冊狀態（state）的正文區沒有可供 `RuntimeManualOverlay` 取樣的前景墨跡（ink）；對齊預覽只用原版題目區色盤索引 10 的受控、私有 `Frame` 取樣（sampling）。正式路徑必須另有經審查的色彩來源，不能沿用測試注入。 |

## READY 所需證據

進入本機正式（production）實作前必須同時具備：(1) 使用者已授權的本機使用範圍（已具備，但不代表公開
散布）、(2) 由真實倚天檔案建立、測試覆蓋 691 個碼點（code points）的失敗即關閉解析器（parser），(3) 使用者已在可丟棄
畫面對照後選定 `top-pad` 的 15→16 與 8→16 對齊策略，(4) 生成後 `GOLEMFNT` header、長度、691 個字模（glyph）與每一 glyph
回讀，(5) 經證據審查的正式前景色來源，以及 (6) 本機／可散布產物的明確分類。缺任一項時本規格維持
DRAFT；公開散布另需可回查的公開許可，不能由本機授權推定。
