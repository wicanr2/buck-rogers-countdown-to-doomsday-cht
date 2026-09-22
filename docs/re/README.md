# 原版觀測證據索引

- [第一百零三階段：第三題手冊覆繪執行期抽樣](phase-103-manual-third-question-runtime.md)：以最新 961 glyph 字庫在原版錯答重抽路徑實際命中 #36，記錄雙倍率、同狀態、像素隔離與 #3／#39 未命中邊界。
- [第一百零二階段：手冊與快捷列覆繪稽核](phase-102-overlay-audit.md)：第一百階段 959 字模的雙倍率首題收據、504 字單頁／3× 密度、白色快捷字母，以及尚缺的玩家路徑驗收。
- [第一百零一階段：身體圖示選擇文字目錄](phase-101-body-icon-text-catalog.md)：沿用正常移動／拒絕／確認 trace，建立七筆固定介面文字的 exact identity、繁中 catalog 與安全矩形；runtime overlay 尚待下一階段。
- [第一百階段：39 題手冊查閱段落翻譯補齊](phase-100-manual-39-translation.md)：37 題中文掃描、2 題英文原書直譯的來源分流、勘誤、504 字靜態驗證與後續抽樣界線。
- [第九十九階段：技能操作列 3× 中文密度](phase-99-action-bar-3x-density.md)：正常技術技能頁操作列接線、白色快捷字母、3× 22 像素中文與 2× 不變的同狀態收據。
- [第九十六階段：倚天手冊中文執行期整合](phase-96-eten-manual-runtime.md)：正式建置器、原版樣式參數、雙倍率中文與錯答清除，以及完整存態語意比較。
- [第九十七階段：手冊 3× 中文密度與第二題](phase-97-manual-cjk-density.md)：2× 不變、3× 22 像素中文字、校正後技術技能翻譯、雙題換題及 restore 收據。
- [第五十五階段：保存、名冊與加入隊伍繁中事件 catalog](phase-55-save-roster-join-translation-catalog.md)：鎖定 18 筆完整路徑 identity，隔離四筆動態姓名並建立七筆繁中 key。
- [第五十六階段：保存、名冊與加入隊伍執行期繁中顯示請求](phase-56-save-roster-join-runtime-display-requests.md)：由唯一 guarded watcher 產生 14 筆請求，四筆動態姓名維持 miss。
- [第九十三階段：倚天字型候選輸入盤點](phase-93-eten-font-candidate-intake.md)：使用者指定候選的字模清冊、691 glyph coverage、Big5 索引分級與權利／對齊停止線。
- [第九十四階段：倚天字型本機建置與對齊原型（prototype）](phase-94-eten-font-local-build-prototype.md)：本機授權下的兩個 16×16 候選、固定手冊狀態（state）、雙倍率範圍約束（containment）與待決的顏色／對齊界線。
- [第九十五階段：倚天 top-pad parser 的格式與索引證據](phase-95-eten-top-pad-parser-evidence.md)：完整 Big5 分區、691 glyph mapping、top-pad、保留區拒絕與 `GOLEMFNT` 載入邊界；不含字型 bytes 或 runtime 接線。

此目錄保存 dosgolem 的原版行為收據與推論分級，不保存原版遊戲、手冊、可還原素材或
其完整輸出。所有位址均須標明使用的位址空間；不可把 IDA 線性位址與 dosgolem 執行期
段位址混用。

| 文件 | 職責 |
| --- | --- |
| [第一階段輸入與啟動收據](phase-1-input-and-startup.md) | 輸入雜湊、權利邊界、dosgolem 能力與正常重播 |
| [第一階段選單文字輸出追蹤](phase-1-menu-text-trace.md) | 一條可觀測文字像素輸出鏈、位址與未知項目 |
| [第二階段文字分派與生命週期追蹤](phase-2-text-dispatch-and-lifecycle.md) | 長度前綴 ASCII 字串、字元 renderer、glyph primitive 與生命週期邊界 |
| [第三階段中文手冊輸入清冊](phase-3-manual-input-inventory.md) | RAR 完整性、解壓成員雜湊與僅 metadata 的頁面定位 |
| [第四階段選單互動與失效生命週期](phase-4-menu-interaction-lifecycle.md) | BIOS Enter 正常路徑、轉場字串輸出與舊文字清除時機 |
| [第五階段種族選擇返回生命週期](phase-5-pick-race-return-lifecycle.md) | BIOS Escape 正常返回、逐位元功能選單重建與反向清除時機 |
| [第六階段清除路徑與失效 hook 證據](phase-6-clear-path-hook-evidence.md) | byte-fill 勘誤、Mode 13h 矩形清除例程、Enter／Escape 動態範圍與 hook 邊界 |
| [第七階段文字 post-call 與 generation 事件](phase-7-text-post-call-generation-event.md) | 末 glyph 完成證據、guarded return、自然落入反例與轉場事件順序 |
| [第八階段功能選單繁中字型與版面 prototype](phase-8-menu-font-layout-prototype.md) | 九筆來源、手冊譯名、字型授權邊界、2×／3× 整數覆繪與 containment |
| [第九階段 dosgolem 通用繁中覆繪基礎](phase-9-dosgolem-xlate-foundation.md) | `xlate` 來源、移植 commit、能力邊界、測試收據與倍率限制 |
| [第十階段繁中 catalog 與字型建置](phase-10-catalog-font-build-pipeline.md) | TSV 驗證、決定性字元清單、GOLEMFNT builder 與 dosgolem 回讀收據 |
| [第十一階段手冊查閱事件映射](phase-11-first-manual-check-event-map.md) | 正常進入路徑、動態題目、錯答重抽與中文掃描對應 |
| [第十二階段手冊題庫結構](phase-12-manual-question-table-inventory.md) | 39 筆定長 schema、解碼器、消費者、無答案 metadata 清冊與動態反向驗證 |
| [第十三階段繁中手冊來源對照](phase-13-manual-source-crosswalk.md) | 39 筆逐項來源、證據分級、OCR 搜尋收據與缺頁邊界 |
| [第十四階段首批短篇手冊段落](phase-14-manual-compact-paragraphs.md) | 八筆原圖校訂、事件鍵、繁中 catalog、長度與失敗即關閉驗證 |
| [第十五階段第二批短篇手冊段落](phase-15-manual-compact-paragraphs-2.md) | 第二批八筆原圖校訂、事件擴充、長度與回歸驗證 |
| [第十六階段第三批已證實手冊段落](phase-16-manual-compact-paragraphs-3.md) | 剩餘候選篩選、五筆原圖校訂、排除原因與回歸驗證 |
| [第十七階段手冊分頁與倍率 prototype](phase-17-manual-pagination-scale-prototype.md) | 真實安全矩形、2×／3× 容量、逐頁對照與 renderer 限制 |
| [第十八階段手冊題目世代與舊覆蓋失效](phase-18-manual-generation-invalidation.md) | 答錯換題時間線、局部清除反例與失敗即關閉世代契約 |
| [第十九階段手冊題目事件收集器 prototype](phase-19-manual-event-collector-prototype.md) | typed lifecycle、真實事件重建與跨世代／亂序負向測試 |
| [第二十階段手冊 catalog 顯示請求 prototype](phase-20-manual-catalog-display-request-prototype.md) | 正式 TSV 精確命中、ordinal bridge 缺口與顯示／語意隔離測試 |
| [第二十一階段手冊序數詞橋接證據](phase-21-manual-ordinal-bridge-evidence.md) | 原版 1–10 長度前綴表、索引 consumer、IDA 收據與可重生 TSV |
| [第二十二階段 dosgolem xlate 通用整數倍率](phase-22-dosgolem-xlate-integer-scale.md) | 2×／3× renderer、邊界安全、真實 GOLEMFNT 冒煙收據與本機 commit |
| [第二十三階段手冊事件 adapter](phase-23-manual-event-adapter.md) | READY 純核心、generation／catalog 正反向測試、正式 TSV 與本機 commit |
| [第二十四階段手冊 runtime watcher](phase-24-manual-runtime-watcher.md) | dispatcher entry／guarded post-call 正式接線、固定狀態 metadata 收據與失敗即關閉測試 |
| [第二十七階段功能選單文字事件清冊](phase-27-menu-event-inventory.md) | 九筆 content-free runtime identity、guarded post-call 收據與正式 TSV 雙向驗證 |
| [第二十八階段功能選單顯示請求純核心](phase-28-menu-display-request-core.md) | READY exact-match catalog、九事件顯示請求與失敗即關閉驗證 |
| [第二十九階段功能選單執行期顯示請求 watcher](phase-29-menu-runtime-request-watcher.md) | guarded post-call 直接產生九筆 request、content-free 收據與 CONFORMED 子規格 |
| [第三十階段種族選單反白與文字安全矩形](phase-30-race-selection-highlight-lifecycle.md) | Down／Up normal→selected 重畫、同終點 framebuffer 與 logical text-safe rectangle |
| [第三十一階段反白 variant 執行期繁中請求](phase-31-selection-variant-runtime-requests.md) | 12-identity exact catalog、13-request 固定重播與舊九事件相容性 |
| [第三十二階段功能選單覆繪倍率 A/B prototype](phase-32-menu-overlay-scale-ab-prototype.md) | 同一原版 framebuffer 的 2×／3× xlate 覆繪、幾何與決策收據 |
| [第三十三階段種族選取列閃爍與色盤生命週期](phase-33-selection-blink-lifecycle.md) | 978 點 palette／row 取樣、黑底黑字選取狀態與無週期重畫證據 |
| [第三十四階段倍率中立的功能選單覆繪核心](phase-34-scale-neutral-menu-overlay-core.md) | READY→CONFORMED 純核心、2×／3× 同 API 與四組逐位元回歸收據 |
| [第三十五階段選定種族後的文字路徑清冊](phase-35-post-race-text-path-inventory.md) | 正常雙 Enter 路徑、性別畫面四筆 content-safe identity 與決定性 framebuffer |
| [第三十六階段性別選擇生命週期](phase-36-gender-selection-lifecycle.md) | Down／Up normal→selected 重畫、Escape 返回功能選單與雙重決定性收據 |
| [第三十七階段性別選擇繁中執行期顯示請求](phase-37-gender-runtime-display-requests.md) | 七 identity 繁中 catalog、18-request 正常路徑與 Escape 失敗即關閉證據 |
| [第三十八階段確認性別後的職業選擇文字路徑](phase-38-post-gender-text-path-inventory.md) | 正常第三次 Enter、七筆職業畫面 identity 與決定性 framebuffer |
| [第三十九階段職業選擇生命週期](phase-39-class-selection-lifecycle.md) | Down／Up normal→selected 重畫、Escape 返回功能選單與雙重決定性收據 |
| [第四十階段職業選擇繁中執行期顯示請求](phase-40-class-runtime-display-requests.md) | 手冊職業譯名、十 identity exact catalog 與三路徑 request 收據 |
| [第四十一階段性別與職業繁中覆繪倍率 A/B](phase-41-character-creation-overlay-ab.md) | 四個真實 framebuffer 的 2×／3× 安全矩形覆繪與決策證據 |
| [第四十二階段確認職業後的角色資料文字路徑](phase-42-post-class-text-path-inventory.md) | 四次正常 Enter 後角色資料／重擲頁的 96 筆 content-safe 事件收據 |
| [第四十三階段重擲提示輸入與動態欄位生命週期](phase-43-reroll-input-lifecycle.md) | `Y` 重擲與 `N` 接受分支的正常 BIOS 輸入、事件及 framebuffer 收據 |
| [第四十四階段角色姓名輸入生命週期](phase-44-character-name-input-lifecycle.md) | 字元、Backspace、Enter 與 Escape 的輸入／回顯／轉場證據 |
| [第五十二階段合法保存後段事件對齊](phase-52-valid-save-event-alignment.md) | 完整技能配置後的圖示／保存／加入角色 checkpoint、未實作服務排除與記憶體候選分級 |
| [第五十三階段保存選項控制流與名冊接納狀態](phase-53-save-choice-control-flow-and-admission-state.md) | 保存分支勘誤、YES 寫檔控制流、決定性與後續 Add 驗證邊界 |
| [第五十四階段已保存角色的名冊與加入隊伍路徑](phase-54-saved-character-roster-and-add-path.md) | 保存檔掃描、角色列、完整載入、加入後移除與雙重正常路徑收據 |
| [第五十七階段明示倍率的執行期繁中覆繪](phase-57-scale-explicit-runtime-overlay.md) | 2×／3× 輸出端覆繪、清除／同原點取代生命週期與同狀態收據 |
| [第六十階段手冊覆繪 READY 前置稽核](phase-60-manual-overlay-ready-prerequisite-audit.md) | 39 題／22 譯文邊界、單頁容量、失敗即關閉與 READY／CONFORMED 分流 |
| [第六十一階段手冊單頁容量驗證](phase-61-manual-single-page-capacity-validator.md) | 36×17 單頁上限、612／613 字邊界與正式 catalog 失敗即關閉收據 |
| [第六十二階段手冊原版題目保留版面 prototype](phase-62-manual-prompt-preservation-prototype.md) | 整框覆蓋操作缺口、保留題目的 36×14 雙倍率對照與待決版面前沿 |
| [第六十三階段性別與職業執行期繁中覆繪](phase-63-gender-class-runtime-overlay.md) | 正常角色建立雙倍率 runtime overlay、轉場失效、同原點取代與像素 containment 收據 |
| [第六十四階段角色資料靜態繁中執行期請求](phase-64-character-sheet-static-runtime-requests.md) | 隔離 35 個靜態 identity，完成 exact catalog、base／Y runtime request 與 framebuffer 非干擾收據 |
| [第六十五階段角色資料頁執行期繁中覆繪](phase-65-character-sheet-runtime-overlay.md) | 35 筆安全矩形、base／Y × 2×／3× runtime overlay、同 palette baseline 與像素 containment |
| [第六十七階段角色姓名靜態提示執行期請求](phase-67-character-name-static-text-runtime-requests.md) | 姓名固定提示 exact request、玩家輸入 miss 與雙重正常路徑收據 |
| [第六十八階段角色姓名提示執行期繁中覆繪](phase-68-character-name-prompt-runtime-overlay.md) | 提示／輸入欄幾何、2×／3× containment 與動態姓名零干擾收據 |
| [第六十九階段角色姓名覆繪轉場失效生命週期](phase-69-character-name-overlay-transition-invalidation.md) | Enter 空終態清除、Escape 同 key 重印與雙倍率無殘字收據 |
| [第七十階段職業技能配置靜態繁中請求](phase-70-career-skill-static-runtime-requests.md) | 四標題／八技能 exact catalog、selected variants 與動態點數 miss 收據 |
| [第七十一階段職業技能配置執行期繁中覆繪](phase-71-career-skill-runtime-overlay.md) | 14 筆 exact 矩形、base／Down 雙倍率取代生命週期與動態數值零干擾收據 |
| [第七十二階段技術技能配置靜態繁中請求](phase-72-technical-skill-static-runtime-requests.md) | 13 個手冊譯名、17 個不重複 identities、共享標題勘誤與 base／Down 收據 |

`workplace/` 是被 Git 忽略的原始輸入與可重生收據存放處；其檔名與雜湊由上述文件引用。
| [第七十三階段：技術技能配置執行期繁中覆繪](phase-73-technical-skill-runtime-overlay.md) | 17 筆專屬矩形、共享標題、穩定 frame 訂正與雙倍率同狀態收據。 |
| [第七十四階段：技能配置底部操作列輸出路徑清冊](phase-74-skill-action-bar-output-path-inventory.md) | 逐字輸出路徑、五標籤幾何、焦點色彩與 disabled unknown 邊界。 |
| [第七十五階段：技能配置底部操作列執行期事件](phase-75-skill-action-bar-runtime-events.md) | Guarded glyph watcher、錨定訂正、八路雙重播與 framebuffer 非干擾收據。 |
| [第七十六階段：技能操作列繁中顯示請求](phase-76-skill-action-bar-display-requests.md) | 五個繁中介面詞、16 個 exact identities、八路 request 與語意隔離收據。 |
| [第七十七階段：技能操作列覆繪幾何與配色前沿](phase-77-skill-action-bar-overlay-geometry.md) | 8-pixel command band、雙倍率字模 containment、底框排除與 normal 配色 prototype。 |
| [第七十八階段：技能操作列配色中立覆繪核心](phase-78-skill-action-bar-style-neutral-overlay-core.md) | 16 個 exact rectangles、明示逐字配色 API、雙候選雙倍率核心驗證。 |
| [第七十九階段：技能操作列配色中立 runtime 生命週期](phase-79-skill-action-bar-style-neutral-runtime-lifecycle.md) | 原子 group 取代、clear／anchor 失效、frame 後明示 palette 重套用。 |
| [第八十階段：技能操作列快捷字母保留與混合寬度版面](phase-80-action-bar-hotkey-preserving-layout.md) | 白色助記字母、原色中文、28-pixel 混合寬度與 Add 空白格擴張證據。 |
| [第八十二階段：host 設定面板控制列視覺 prototype](phase-82-host-settings-panel-visual-prototype.md) | 上方 host 控制列、下推而不遮畫布的面板，以及 2×／3× hit rectangle 契約。 |
| [第八十三階段：手冊保留原題的 504 字容量契約](phase-83-manual-preserved-prompt-capacity-contract.md) | 保留題目時的正式 36×14／504 字幾何、catalog 邊界與已取代 612 字契約的分界。 |
| [第八十四階段：dosgolem host 前端能力盤點](phase-84-dosgolem-host-frontend-capability-audit.md) | 無頭現況、可重用 output compositing、DOS 滑鼠輸入邊界與必須新增的通用 host 能力。 |
| [第八十五階段：手冊繁中 presenter 整合就緒稽核](phase-85-manual-presenter-integration-readiness-audit.md) | 重跑正常手冊 request、xlate／14 行 layout 能力，以及 lifecycle 與字型 READY 缺口。 |
| [第八十六階段：手冊 presentation lifecycle 接線](phase-86-manual-presentation-lifecycle.md) | CONFORMED typed begin／clear／request queue、正常玩家 metadata 重播與無輸入邊界。 |
| [第八十七階段：手冊多行 presenter 純核心](phase-87-manual-multiline-presenter-core.md) | CONFORMED 的 36×14／504、背景＋文字 layer、2×／3×與 lifecycle synthetic 收據；未接玩家 runtime。 |
| [第八十八階段：手冊正式 GOLEMFNT 子集來源稽核](phase-88-manual-formal-font-subset.md) | DRAFT：691 glyph 清單已重生，但本機沒有可核對的候選字型與授權告知。 |
| [第八十九階段：host 倍率預選與 Apply 純核心](phase-89-host-scale-selection-apply-core.md) | CONFORMED 的 selected／active state；不含 backend、hit event 或玩家切換。 |
| [第九十階段：手冊 presentation queue consumer 純核心](phase-90-manual-presentation-queue-consumer.md) | CONFORMED 的 append-only value cursor；不含 watcher callback、command 或玩家畫面。 |
| [第九十一階段：手冊 watcher snapshot bridge 純核心](phase-91-manual-watcher-snapshot-bridge.md) | CONFORMED 的 watcher→consumer 單一轉送；不含 command、字型或玩家畫面。 |
| [第九十二階段：正式字型候選 manifest 驗證補強](phase-92-formal-font-candidate-manifest-validation.md) | CONFORMED 的候選審查工具；不採用、建置或散布字型。 |
