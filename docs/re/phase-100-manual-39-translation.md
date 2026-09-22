# 第一百階段：39 題手冊查閱段落翻譯補齊

更新：2026-09-22。依使用者指定，本階段先完成每題遊戲內可顯示的繁中說明，
逐題試玩留待後續。這是 39 個查閱事件各一段的意譯 catalog，不是中文手冊整章
逐字轉錄；原版答案與判定程式完全不變。每段均不超過現行正文 504 字容量，
來源 TSV 為 [`text/manual.zh-TW.tsv`](../../text/manual.zh-TW.tsv)。

## 來源與勘誤

`text/manual-events.tsv`、`text/manual.zh-TW.tsv` 均為 39 筆，一一對應原版題庫。
37 筆以本機中文掃描原圖核對；第 3 題 `More on Abilities` 與第 39 題 `Roll.`
沒有可直接對應的中文掃描段落，改由[原版英文手冊文字轉錄](https://www.freegameempire.com/games/Buck-Rogers-Countdown-to-Doomsday/manual)
翻譯。來源表 [`text/manual-english-sources.tsv`](../../text/manual-english-sources.tsv)
列出原書 Log Book 第 3 頁、Rule Book 第 42 頁的精確章節定位與 2026-09-22
取得的本機 HTML 快照 SHA-256
`e8528a31b66d76e7162abe358bff1f27d7d5a5d4070914beee470867e59e728a`；
快照只留在被 Git 忽略的 `workplace/`，不散布原書內容。

先前來源對照的三筆低信心項已逐張目視並與原書交叉核查：第 11 題中文
掃描實際有「F. 錢」標題，第 18 題有「F. 接收敵艦」，舊 OCR 漏讀而誤列
`strong-inference`；兩題現以中文原圖直接證實。第 3 題的舊對照把鄰近的
技術／EXP／LEVEL／HP 內容錯當為 `More on Abilities` 全段；原版英文本節實際
只有能力修正表和技能說明的兩句索引，因此刪除錯配，改以英文原書直譯。
第 39 題中文掃描確實缺頁，沒有虛構中文來源。

技能段落另依原版英文校正數字：新角色起初最多選七項一般技能；中文掃描
印為「十七個」，與原版英文的 `seven` 不同。此處只訂正譯文，未改規則。
職業、種族及武器等較長章節採原創短段，保留與該題相關的主要類別、條件和
數值；不是把大段手冊逐字搬入版控，未覆蓋的章節細節也不冒稱已翻完整本手冊。

## 資料與驗證邊界

`tools/manual_crosswalk.py` 以兩條互斥來源路徑驗證：中文掃描需有檔名、
archive-order、SHA-256、印刷頁與原圖錨點，並與本機掃描 manifest 相符；
英文原書則需獨立 TSV 的 HTTPS URL、原書章節、取得日期、SHA-256，且可
選擇核對本機快照。來源不得混用或產生孤兒 record。39 個事件均須精確匹配
原版頁碼／標題／序數，沒有額外譯文鍵。正式手冊字元清單 934 glyph，
清單 SHA-256 `11fab7e2092b9f5c7c0055c3e0a6b3cc938b3f71e7c8910d8f5961a70370d282`；
完整介面聯集 959 glyph，倚天字庫 SHA-256
`1c8bc423568b13702e6056bcff302e9497c09c237955acd95593c2bab04018aa`，
僅在本機 `workplace/`。Python 177 項測試通過，dosgolem `fontcheck`
回讀 `GOLEMFNT 16×16` 的 959 glyph 通過。

這是文字資料完成與靜態驗證，不是 39 題逐題執行期同狀態收據。依使用者
安排，後續再抽樣試玩檢查切題、覆繪、返回與存讀檔；不得以本階段宣稱
全部玩家路徑已通過。
