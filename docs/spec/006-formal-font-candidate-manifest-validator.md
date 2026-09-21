# 006 — 手冊正式字型候選 manifest 驗證器

狀態：CONFORMED（候選審查工具）
日期：2026-09-21
前置：[手冊繁中輸出端 presenter 整合](005-manual-runtime-presenter-draft.md)、
dosgolem spec 218、[第八十八階段字型來源稽核](../re/phase-88-manual-formal-font-subset.md)。

## 目的與邊界

建立可重現的**候選審查**，讓未來由使用者提供或明確授權取得的本機字型能在 build 前驗證來源檔、
完整授權文字、格式、691 glyph coverage 與 metadata。驗證成功只代表候選可進入後續權利審查與
READY gate；不是採用、嵌入、散布、字型建置、renderer 接線或玩家可見中文的許可。

候選原始字型、完整授權文字與任何 manifest instance 一律只能放在被忽略的 `workplace/`；Git 只保存
validator、schema 與 synthetic tests。validator 不可產生 GOLEMFNT、字模、手冊文字、授權全文或原版內容；
stdout 只可輸出 filename、SHA-256、format、version、notice 欄位是否存在與 coverage count。

## 已證實前提

- dosgolem spec 218 已證實正式 `manual.zh-TW.tsv` 的 character-list SHA-256 為
  `dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f`，共 691 glyph；候選與完整
  授權文字目前均缺席，故 spec 218 維持 DRAFT。
- `tools/catalog_font.py` 已有 deterministic `character_list_bytes`、Unifont `.hex`／`.hex.gz` 的
  8×16／16×16 parser，與缺 glyph／重複／格式錯誤 fail-closed 行為；它沒有 manifest parser、來源或授權
  檔 SHA 驗證，也不區分本機驗證與散布狀態。
- `RuntimeManualOverlay` 只接受 16×16、32-byte-per-glyph 的完整字型；fixture 與舊產物不能提供可回查
  的來源或權利證據。

## 擬定 manifest 與命令契約

validator 加入既有 `tools/catalog_font.py`，新增 `validate-candidate` 子命令：

```text
python tools/catalog_font.py validate-candidate text/manual.zh-TW.tsv \
  --manifest workplace/phaseNN/input/candidate-manifest.json \
  --source workplace/phaseNN/input/candidate.hex.gz \
  --license workplace/phaseNN/input/COPYING
```

manifest 是嚴格 JSON object，恰有下列欄位：

```json
{
  "schema": "buck-rogers-manual-font-candidate/v1",
  "source_filename": "candidate.hex.gz",
  "source_version": "使用者提供的版本或日期",
  "source_sha256": "64 個小寫十六進位字元",
  "source_format": "unifont-hex",
  "conversion_rule": "unifont-8x16-or-16x16-to-golemfnt-16x16",
  "license_filename": "COPYING",
  "license_sha256": "64 個小寫十六進位字元",
  "attribution_notice": "非空 metadata",
  "embedding_notice": "非空 metadata",
  "character_list_sha256": "64 個小寫十六進位字元",
  "validation_scope": "local-validation-only",
  "distribution_status": "undecided"
}
```

檔名欄只能是沒有目錄分隔符的 basename，必須精確等於 `--source`／`--license` basename。source 與
license 必須是非空 regular file，其實際 SHA-256 必須精確符合 manifest。`source_format` 與 conversion
rule 只接受既有 parser 已支援的值；其他格式拒絕，不代表其字型品質或授權無效。catalog 推導出的
character-list SHA 必須符合 manifest，然後以既有 parser 讀出每個 required glyph；不足、重複或格式錯誤
一律失敗。未知、缺少、型別錯誤或空值欄位均拒絕。

成功 stdout 為 JSON metadata，必含 schema、source／license filename+SHA、source format+version、
character-list SHA、required／found count、validation scope 與 distribution status；不得回顯
attribution／embedding notice、license 或字模內容。

## DRAFT 驗收與停止線

synthetic tests 必須覆蓋：成功的最小 catalog+hex+license、缺 source、缺／空 license、source／license／
character-list 雜湊不符、basename 不符、未知或缺欄、非法 scope／distribution、unsupported format、
conversion rule 漂移、coverage 缺字與成功 metadata 不洩漏 notice／license／glyph bytes。所有失敗不得
建立 output file。

實作前必須確認既有 parser 是唯一 glyph coverage 解碼器，新增命令不寫檔且不改 `build` 語意。若候選
格式超出既有 `unifont-hex` parser、欄位要求需指定取得來源／字型家族，或要宣稱可散布，停止並請使用者
決定；不得擴張本工具替代授權或產品選擇。

## READY 證據審查

目前 `tools/catalog_font.py` 已將 catalog→sorted codepoint→`character_list_bytes` 與
Unifont glyph coverage 置於同一個 deterministic module；新增 JSON parser 可以重用這兩個純函式，
不必創造第二份字模解碼或 character-list 算法。既有 `build` 只在 `--out` 時寫檔，因此獨立的
`validate-candidate` subcommand 可完全不呼叫 `_write_if_changed`，沒有誤產生字型的路徑。

source／license 的 basename、raw SHA-256、manifest strict schema、scope 與 distribution state 均為
可機械判斷的 facts；完整授權是否足夠、字型是否採用及可否散布仍是使用者與後續權利審查的決策，
validator 只能要求非空實際文字，不能宣稱法律結論。現有 `unifont-hex` 支援是既有 builder 的能力
邊界，不是選定任何候選；未知 format 失敗即關閉並保留未來由使用者決定擴充的空間。

typed input、輸出 metadata、失敗模式、synthetic test 與權利停止線均已完整，故本規格升為 **READY**。
它只授權既有工具的無寫入候選驗證與測試；不授權下載、採用、build、renderer 接線或散布。

## CONFORMED 候選審查工具收據

2026-09-21，`tools/catalog_font.py validate-candidate` 已實作 strict JSON manifest、source／license
basename 與 SHA-256、非空 UTF-8 授權文字、既有 `unifont-hex` parser 的完整 glyph coverage，以及
character-list SHA 比對。它不接受未知／缺失／重複 JSON 欄位、雜湊或 policy 漂移、unsupported format、
conversion rule 漂移、path basename 漂移、缺 source、空 license 或任何缺 glyph；所有失敗都在
GOLEMFNT 建置前停止。

Docker 內 `python -m unittest discover -s tools -p "test_*.py"` 通過 158 項。新增 synthetic tests 覆蓋
成功 metadata、command stdout、metadata 不回顯 notice／license／glyph bytes、缺欄、未知欄、三種 SHA
漂移、basename、format、conversion、scope、distribution、空 license、缺 source 與 coverage 缺口；成功或
失敗都不建立字型 output。`manual_overlay_layout.py` 與正式 catalog lint 亦通過。

本收據只證實審查工具，**不是字型候選採用、完整授權法律結論、GOLEMFNT build、renderer 接線或玩家可見
中文**。本機仍沒有 candidate source 或完整授權文字，dosgolem spec 218 與 spec 005 的正式字型／
normal-player A/B gate 繼續是 DRAFT。
