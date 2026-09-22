# 007 — 倚天 15 點字型候選輸入契約

狀態：DRAFT  
日期：2026-09-22  
前置：[手冊正式字型候選 manifest 驗證器](006-formal-font-candidate-manifest-validator.md)、
[手冊繁中輸出端 presenter 整合](005-manual-runtime-presenter-draft.md)、
[第九十三階段候選輸入盤點](../re/phase-93-eten-font-candidate-intake.md)。

## 目的與邊界

本規格只記錄使用者指定之本機倚天候選的檔案身分、15 點 Big5 字模結構、對正式手冊 catalog 的
coverage 與仍未解決的權利／轉換缺口。它不是採用宣告、授權意見、`GOLEMFNT` 建置規格或
renderer 接線許可。

所有候選原檔、完整媒體、完整授權告知與任何衍生字模都只留在使用者本機的
`/home/anr2/cht/etan_font`；不可加入本專案、dosgolem、GitHub Issue、Release 或可散布測試語料。
受版控文件只保存必要 metadata、SHA-256、格式結論與缺口。

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
| 16×15→runtime 16×16 | 未知 | `RuntimeManualOverlay` 只接受每 glyph 32-byte 16×16。第 15 列應置於上方或下方、8×15 ASCII 的水平／垂直定位，以及其與 36×14 格線的視覺結果，尚未有 prototype 證據；不得自行選擇 padding。 |
| 倚天候選 parser | DRAFT | 既有 `validate-candidate` 僅支援 Unifont 十六進位字模，拒絕本候選是正確行為。只有本規格經 evidence review 升為 READY 後，才能新增獨立 ETen parser／manifest schema 與 synthetic tests。 |
| 完整授權告知 | 已證實為缺席 | 候選目錄沒有 `LICENSE*`、`COPYING*`、`COPYRIGHT*` 或 `NOTICE*` 一般檔案。兩份非空 `README.DOC` 可被 CP950 解碼，但沒有可辨識的授權、散布或權利許可條款。這不足以證明世界上不存在權利條款，卻足以證明本候選尚未提供本專案所需的完整告知。 |
| 採用／嵌入／公開散布 | 未知 | 使用者指定候選來源不等於取得嵌入或公開散布許可。未取得可回查的完整許可前，僅能做本機唯讀研究；不得建立字型產物。 |

## READY 所需證據

進入實作前必須同時具備：(1) 可回查的候選版本與完整授權／告知文字，(2) 由真實倚天檔案建立、
測試覆蓋 691 code points 的失敗即關閉 parser，(3) 使用者在可丟棄畫面對照後選定 15→16 與 8→16
對齊策略，(4) 生成後 `GOLEMFNT` header、長度、691 glyph 與每一 glyph 回讀，及 (5) 字型權利與
本機／可散布產物的明確分類。缺任一項時本規格維持 DRAFT。
