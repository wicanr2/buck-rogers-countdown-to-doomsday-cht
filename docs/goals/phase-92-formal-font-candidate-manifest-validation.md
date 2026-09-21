# 第九十二階段：正式字型候選 manifest 驗證補強

狀態：完成（候選審查工具）

## 目標

稽核並補強正式手冊字型候選的 manifest 驗證，使未來使用者提供的本機候選能在**不採用、不下載、
不散布**字型前，先以固定來源檔／授權文字雜湊與 691 glyph 需求完成失敗即關閉檢查。此階段只改善
候選審查工具與其測試；不選定任何字型、不可輸出可用字型產物。

## 已確認前提

- spec 218 維持 DRAFT：本機尚無候選字型檔與完整授權文字；691 glyph 清單及 SHA-256 已固定。
- 手冊 presenter constructor 已拒絕缺 glyph 的 16×16 字型，但 fixture font 只可用於合成測試，不能成為
  正式來源。
- 使用者尚未選擇提供候選或授權下載；任何候選採用、網路取得或散布判定都必須等待該決策。

## 範圍

- 在 Docker 中盤點目前 `font/README.md`、spec 218、既有候選檢查工具及其測試，找出 manifest 對來源
  字型檔、完整授權文字、雜湊、格式與 coverage 的可機械驗證缺口。
- 若缺口已由現有正式工具覆蓋，只建立可重現的審查收據並停止；若未覆蓋，先建立 DRAFT→READY 規格，
  再新增最小 fail-closed validator 與 synthetic tests。
- validator 的輸出只可為 metadata、雜湊、coverage count 與錯誤；不得輸出字模位元、字型原文、完整
  授權全文、手冊掃描或可還原素材。

## 不在本階段

- 不下載、採用、轉檔或散布任何字型；不修改正式 catalog／譯文、手冊內容、renderer、watcher、consumer、
  bridge、原版 EXE、DOS input、答案、存檔或 host frontend。
- 不把 synthetic fixture、系統字型或未附完整授權文字的檔案標為正式候選；不建立 GOLEMFNT 產物。

## 完成條件

1. 規格清楚指出 manifest 的可證實欄位、fail-closed 邊界、權利資料邊界與「驗證候選不等於採用」的
   停止線；只有 READY 規格可授權工具改動。
2. 既有或新增工具能以 synthetic inputs 驗證缺檔、空授權、雜湊不符、格式不符、coverage 不足、
   未知 manifest 欄位與成功 metadata 路徑；沒有候選時不產生任何字型輸出。
3. 專案資料驗證、main 推送與相關 GitHub Issue 回寫完成；spec 005 僅更新字型驗證工具的事實，
   不將字型 DRAFT 或玩家可見手冊中文提前標完成。

## 退出條件

- 若現有工具已完整覆蓋本目標，記錄證據並停止，不建立重複 validator 或第二套 manifest 格式。
- 若要驗證的欄位會指定字型家族、版本、取得來源或散布方式，停止並請使用者決定；不可由工具預設。

## 完成收據

- `tools/catalog_font.py validate-candidate` 已完成 strict JSON manifest、來源與授權文字 basename／
  SHA-256、非空 UTF-8 授權文字、既有 parser coverage 與 character-list SHA 驗證；它不寫 GOLEMFNT，
  stdout 只含 metadata，且不回顯 notice、license 或 glyph bytes。
- Docker 內 158 項 Python 測試、正式手冊 504 字版面與 catalog lint 均通過。synthetic source 覆蓋正式
  691 glyph 清單，但不構成候選字型、採用或散布；沒有將任何 candidate 寫入工作區或 Git。
- dosgolem 本機 branch 的 `a4a87aad48607ea6ff6e4646de1292f5caaeade9` 已回填 spec 218 的工具邊界，
  仍維持 DRAFT。使用者尚須提供候選與完整授權文字，或明確授權取得來源，才可進入字型 READY。
