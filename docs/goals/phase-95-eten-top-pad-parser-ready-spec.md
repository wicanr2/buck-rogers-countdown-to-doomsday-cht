# 第九十五階段：倚天 top-pad parser 的 READY 前規格

狀態：已完成
對應工作：[GitHub Issue #12](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/12)

## 目標

把使用者已選的 `top-pad`（第 16 個空白列置頂）從本機可丟棄對照，轉成可經證據審查的倚天 15 點
parser 與本機 `GOLEMFNT` 建置 DRAFT。只有本階段的輸入、分區、轉換、失敗模式、測試與權利邊界足以
審查後，才可升為 READY 並開始正式實作。

## 結果

第九十五階段已以真實但唯讀的本機輸入驗證完整分區、691 glyph mapping、`top-pad` 與 `GOLEMFNT`
載入契約，並把資料、失敗模式、測試與權利停止線寫入 spec 008。spec 008 已 READY，只授權後續
[GitHub Issue #15](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/15) 的本機 builder
implementation；本階段沒有寫入 parser、字型二進位或 runtime hook。

## 已確認前提

- 使用者已採用 `top-pad`，排除 `bottom-pad`；16×15 CJK 與 8×15 ASCII 的 source rows 都寫到 output
  rows 1..15，output row 0 為零。ASCII 水平仍依既有 16-bit layout 置於 x=4..11。
- 本機倚天來源的身份、SHA-256、Big5 分區、691 glyph coverage 與三個結構錨點見 spec 007；原始字型
  與所有衍生字型均不可加入 Git 或公開散布。
- 既有 `validate-candidate` 是 Unifont candidate 審查器，不得放寬、偽裝或改稱為倚天 parser。
- 正式前景色來源（#13）與 presenter 執行期接線（#14）不依賴本階段完成，且不在範圍內。

## 範圍

- 在 Docker 對既有原始字型做唯讀格式／mapping 研究，記錄檔案雜湊、Big5 encoding、SPCFONT／STDFONT
  選擇、ASCII 置中、`top-pad` 行映射、GOLEMFNT 產物契約與每種失敗條件。
- 建立可審查的 DRAFT 規格和 RE 證據；若每個未知均有足夠可重生證據，才另行審查升為 READY。
- 規劃 production parser 的合成測試，將真實字型只作本機 integration input；不得把它放入測試 fixture。

## 不在範圍

- 不在 DRAFT 狀態寫入 dosgolem production parser、公開字型建置器、renderer、command 或遊戲 loop。
- 不改原版 EXE、DOS VRAM、輸入、答案判定、存檔、翻譯語意或檔案鍵值。
- 不選定手冊前景色、不沿用第九十四階段 private palette-index-10 sampling，也不宣稱手冊中文已完成。

## 完成條件

1. DRAFT 逐項分級為已證實、強推論、假說或未知，保留來源檔、SHA-256 與可回查的 Big5／glyph index。
2. READY 審查清楚定義 typed input、輸出、top-pad 規則、全量 coverage、錯誤／越界／codec fail-closed、
   產物本機路徑與公開散布停止線。
3. 只有 READY 後才另開 implementation 子階段；若任一格式或映射結論未達證據門檻，保留 DRAFT 並停止。
4. 文件、Docker 驗證、main 推送與 #12 回寫完成；dosgolem branch 在本階段不推送。（已完成）
