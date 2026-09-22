# 第九十三階段：倚天字型候選輸入盤點

狀態：完成（DRAFT 候選清冊）

## 目標

依使用者指定的本機倚天字型目錄，建立不散布原始字型的候選輸入清冊，並以實際檔案、雜湊、
格式與完整授權告知查證它是否能成為手冊 691 glyph 的正式字型來源。此階段只做來源／格式／權利
前置證據與 DRAFT 規格；不建置 `GOLEMFNT`、不接 renderer、也不將字型原檔納入 Git。

## 已確認前提

- 使用者已選定 `/home/anr2/cht/etan_font` 的倚天字型作為候選來源，排除下載 GNU Unifont 與改用其他
  候選；此選擇不是授權散布或嵌入的法律結論。
- 手冊正式 TSV 的需求是 691 glyph，character-list SHA-256 為
  `dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f`。
- 現有 `validate-candidate` 只支援 `unifont-hex`；它拒絕未知格式是既有的失敗即關閉邊界，不能把
  倚天 `.15` 字模硬套成已驗證格式。
- 倚天 16×15 字模的 Big5 分區索引及 `STDFONT.15`／`SPCFONT.15` 成對需求是候選格式假說，仍須以
  使用者指定目錄的實際檔案與可辨識 glyph 驗證。

## 範圍

- 在 Docker 以唯讀掛載盤點候選目錄：檔名、regular-file 狀態、大小、SHA-256、可讀的版本／授權告知
  與格式魔術／stride；原始字模與完整授權內容只留在本機來源，不寫進 Git 或 stdout。
- 從正式手冊 691 glyph 對候選 Big5 mapping 做 coverage 與三個已知 anchor glyph 的可重現檢查；缺字、
  codec 歧義、索引越界、glyph 不可辨識或缺少 `SPCFONT.15` 都必須明確分級並失敗即關閉。
- 將查得的格式與權利邊界寫成新的 DRAFT 規格及證據索引；只有證據足夠時才可在下一階段審查為 READY，
  擴充候選驗證器或字型 builder。

## 不在本階段

- 不採用、嵌入、轉檔、散布或下載字型；不宣稱任何授權可供公開發行。
- 不修改手冊譯文、原版 EXE、DOS 輸入、答案判定、存檔、watcher、consumer、bridge、renderer、host
  frontend 或遊戲規則；不把倚天字型寫入 `workplace/`、Git 或 GitHub。
- 不把 `STDFONT.15` 以外的檔案名稱、字型大小、Big5 mapping 或授權內容從參考案例推定為本候選事實。

## 完成條件

1. 清冊可重現地記錄候選檔案 metadata、雜湊、格式檢查與權利告知是否存在，且不洩漏字模或完整授權。
2. DRAFT 規格逐項標註已證實、強推論、假說或未知，明確說明 16×15→runtime 16×16 的轉換、Big5／Unicode
   mapping、標點來源、coverage 與散布停止線。
3. 若完整授權告知、必要字模或 691 glyph coverage 缺席，停在 DRAFT 並列出精確缺口；不得產生字型輸出或
   改寫既有 Unifont validator。
4. 文件、測試、main 推送與相關 GitHub Issue 回寫完成；spec 005 與 dosgolem spec 218 只更新可證實事實，
   不將正式字型或手冊玩家路徑提前稱為完成。

## 退出條件

- 若候選不含完整授權告知或不具可用格式，保留來源清冊與 DRAFT 證據後停止此分支；不得以舊產物或網路
  搜尋補作來源。
- 若查證結果需要指定公開散布、內嵌、fallback 字型或非 16×15 視覺策略，先由使用者決定，再另開階段。

## 完成收據

- Docker 唯讀清冊確認 `ET353S/FILES/` 的 `STDFONT.15`、`SPCFONT.15`、`SPCFSUPP.15` 與
  `ASCFONT.15` 非空且 stride 整除；完整 metadata 與權利邊界已收錄在 spec 007，沒有複製任何原始字模。
- 正式手冊 691 glyph 的 Big5 定位結果為 44 ASCII、12 symbol、634 common CJK、1 secondary CJK，
  缺字及越界均為零，僅 `U+0020` 為預期空白 glyph；`一`／`中`／`猴` 的結構錨點無整體位移。
- 候選缺少完整授權告知，且 16×15／8×15→16×16 的視覺對齊尚無 prototype 與使用者決定。因此 spec 007、
  spec 005 的正式字型 gate 與 dosgolem spec 218 維持 DRAFT；既有 Unifont validator 沒有被放寬。
- Docker 內 158 項 Python 測試、22 段 504 字手冊版面驗證、正式 691-entry character-list 的 SHA-256
  驗證均通過。後續 GitHub Issue 回寫只報 metadata 與 DRAFT 停止線，不上傳候選字模或授權內容。
