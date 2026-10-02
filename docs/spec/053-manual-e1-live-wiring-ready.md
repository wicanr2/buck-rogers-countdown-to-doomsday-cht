# 053 — 手冊 E1（3× 英文專名不拆行）接入玩家路徑

狀態：**限縮 CONFORMED**（2026-10-02；範圍：zh-TW 的 3×、離線首題時點與一題實機作答路徑、39 段載入預檢；其餘手冊題未逐題實機。證據 docs/re/phase-317-manual-e1-live.md。兩輪獨立審查的必修與建議已併入）。
日期：2026-10-02
Issue：#21
決定：
- 使用者 2026-09-25 選 E1（3× 保留手冊中的英文專名、整詞換行、2× 不變；英文字首 advance 原定 14px，規格 039 §3.4 之後改為 12px 半形，現行程式 `manualE1PixelLatin = 12`）並要求擴充 dosgolem 共用繪字層。
- 使用者 2026-10-02 選定這一輪只接 **zh-TW**，zh-CN、ja、ko 另開 Issue。
- 使用者 2026-10-02 選定 **E1 與本機英文關鍵字列並存**（完整版發行包自動載入 `local/manual-english.tsv`，不能因此永遠看不到 E1）。

前置：規格 005（手冊 presenter，E1 分支已無頭限縮 CONFORMED）、024（雙層封存）、034（本機英文關鍵字列）、039（半形）、051（ja、ko 手冊段落，不受本規格影響）、dosgolem 規格 234（共用繪字層）。

## 1. 為什麼要做

E1 的純值 plan（`BuildManualE1Plan`）與 3× 繪製只在 `ManualSnapshotOwner` 路徑啟用：`RuntimeManualOverlay.e1Base` 只有 `NewManualSnapshotOwner` 會設，該 owner 只被測試使用。
正式玩家路徑（`LiveRuntime`、`buckrogers-play`）的手冊 presenter 由 `live_lane.go` 的 `NewRuntimeManualOverlayLang` 建立，沒有設 `e1Base`，
所以 3× 的 zh-TW 手冊段落仍用固定格逐字元換列，段落中保留的英文專名會在列尾被拆成兩段。本規格把已驗證的 E1 plan 接進這條路徑，並讓本機英文關鍵字列與它並存。

## 2. 證據

來源：離線探針 `workplace/phase316/zz_p321_e1_probe_test.go.txt`（作者）與審查探針 `workplace/review053/zz_review053_test.go.txt`、`zz_review053b_test.go.txt`（審查者，乾淨匯出的 dosgolem `e992599`），
皆在 Docker、`--network none`、唯讀輸入下執行；皆未入版控。字型：發行 zh-TW `buckrogers-unifont.golemfnt`（SHA-256 `7675cf4e97986985cbeb4b5ed447a2a56d68f4c5bdaf29f6f650164179042697`）、
本機倚天 `buckrogers-eten-top-pad.golemfnt`（`ebe7f0458ebc19ec113ec2c4cd8f0a66d145eac21e6aa8dff6273594f1b1fdc3`）。

已證實：

1. 發行字型在 3× 對正式 `text/manual.zh-TW.tsv` 逐段建 E1 plan 並 `TextLayer`：**39／39 成功**，每段 `Apply` 後 `Draw` 無缺字，預檢約 0.1 秒；倚天字型同樣 39／39。
2. 前提：三個字型（base、derived、half）`Name` 必須非空且互異（`manual_e1_plan.go:535-540`）；`xlate.LoadFont` 回的 `Name` 是空字串，derived 不先命名時預檢是 0／39。
3. 命名 derived 不改變固定格的 3× 輸出（39 段位元組差異 0）。
4. E1 的版面與 generation 無關（generation 1 與 977 的 `TextLayer` 幾何差異 0／39）。
5. 39 段中有 15 段 E1 輸出與固定格逐位元組相同（段落中沒有需要保護的英文詞界），其餘 24 段不同；不同處都在 3× 手冊清底矩形（x21 y216 w915 h336）內，矩形外零差（合成 indexed 與 palette 下）。
6. 2× 路徑不看 `e1Base`（`manual_overlay_runtime.go:284` 的 `o.scale == 3 && o.e1Base != nil`）。
7. `manualEnglishPresenter.sync` 在 `man.e1Plan != nil` 時回 false（`manual_english.go:244`），所以現行本機英文關鍵字列與 E1 互斥。
8. `buckrogers-play` 沒給 `-manual-english` 時，自動找 `local/manual-english.tsv`（`cmd/buckrogers-play/main.go:524-531`，依序 exe 目錄、`../Resources`、cwd）；`tools/package.sh` 的完整版把這個檔放進發行包。
9. 英文關鍵字列放在**段落第 k 列之下**（`manualEnglishLayout(k, …)` 只用到 `first = k+1`，對 k 單調：k 越小越容易放下；字形涵蓋與 k 無關），k 取自固定格換列；它用固定格的半形格（`segmentStamps`）畫。
   關鍵字列在 3× 的 y 是 216+24r，等於 E1 的 `manualE1PixelTextTop + row*manualE1PixelLineH`（行距一致）。
10. 現行 catalog 39 段的 E1 使用列數 k' 都不大於固定格列數 k：38 段相等、1 段少一列。以合成摘錄（三種占位詞長，不含任何真實手冊單字）實測，E1 段落字模底緣都在關鍵字列頂端之上、中間留一列空白，沒有重疊。
11. live 的 compose 對手冊層 `Draw` 丟棄第三個回傳值（`live_lane.go:1039-1041`）；E1 的 `Draw` 在 `DrawChecked` 失敗時回 `(nil, nil, false)`（`manual_overlay_runtime.go:486-490`），之後 `layer()` 會對 nil 索引而 panic（強推論）。
12. `ManualSnapshotOwner.SetStyle` 只把狀態清成 `manualOverlayCleared`，之後的 `Clear` 會被拒（`手冊 clear 狀態無效`），`ManualPresentationConsumer` 錯誤時不推進 cursor，presenter 之後停在原版。live 的 `RuntimeManualOverlay.SetStyle` 只更新 style，plan 保留，接著 `Clear` 正常。
13. live 的 style 在 Begin 時就由 watcher 設好（`watcher.go:160-164`），E1 plan 不含 style，顏色由 `Frame` 每幀的 `show()` 套用。
14. dosgolem 工作樹有未入版控的非測試 Go 檔（`oracle/draft_manual_checkpoint_bridge.go`、`oracle/draft_real_observer_runner.go`、`oracle/draft_restricted_observer_facade.go`），在工作樹直接建 binary 會被編進去。
15. 同時設 `BUCKROGERS_CHT_ROOT` 與 `BUCK_OWNER_PROJECT`，`apps/buckrogers` 仍有約 34 個頂層 SKIP（靠 trace、狀態檔、各語言字型等其他環境變數閘控）；E1 私有 39 段測試由 `BUCK_OWNER_PROJECT` 閘控（`manual_e1_plan_test.go:33`）。

未知：E1 在不同英文詞界的實機樣本（§5 補）；E1 對 ja、ko、zh-CN 字型的相容性（不在本規格範圍）；完整版的倚天字型由打包依現行譯文重建，雜湊可能與上列不同（以載入時預檢為唯一閘門）。

## 3. 契約

### 3.1 啟用條件與 DebugSummary

E1 在下列條件**全部成立**時啟用：語言通道為 zh-TW、倍率為 3×、載入時預檢全部通過、（本機英文關鍵字列已載入時）§3.4 的並存條件成立。其他情形一律走現行固定格路徑，輸出位元組不變。
`LangTest`（規格 040 §5.3 的測試語言）與 zh-CN、ja、ko 的 `e1Base` 必為 nil。 （2026-10-02：zh-CN、ja、ko 的 3× 已由規格 055 啟用，只有 `LangTest` 仍為 nil。）

- 預檢：建 3× presenter 後，以 §3.2 命名的字型對 catalog 的**每一段**呼叫 `BuildManualE1Plan` 與 `plan.TextLayer`（`DisplayRequest{Generation: 1, EventKey, TextKey, Translation: 該段 catalog 譯文}`；不 `Apply`、不留狀態），
  並記下每段 E1 使用的列數 k'（`plan.lines` 中有 token 的最後一列加一）存在 presenter 旁的 `map[eventKey]int`。
  任一段失敗即整體不啟用 E1（`e1Base` 保持 nil），不逐段退回。預檢在 `loadLane` 內完成，早於 `SetManualEnglish`；失敗不停用語言通道。
- `DebugSummary`（zh-TW 區段，接在「英文列」之後）：`manual-e1=on`、`manual-e1=off(preflight:M)`（M 為失敗段數）、`manual-e1=off(keyword:N)`（N 為違反 §3.4 並存條件的題數）、`manual-e1=off(runtime)`。
  只有計數與固定代碼，不得含譯文、錯誤原文、字元或 EventKey。
- runtime 退路：3× zh-TW 的 `manSync.Sync()` 回錯且 `e1Base != nil` 時，把該 presenter 的 `e1Base` 設為 nil，在同一次 `syncManual` 再 `Sync()` 一次（失敗的 Request 沒被 consume，第二次改走固定格）； （2026-10-02：規格 055 §3.4 起對所有啟用 E1 的通道一視同仁。）
  第二次仍失敗則照舊 `resets["manual"]++` 且不再重試（不得無限重試）。只有第二次成功才標 `manual-e1=off(runtime)`（`Sync()` 也可能因非 E1 原因失敗，那種情形不標）。
  不改 `Apply` 的 E1 分支（規格 005 已限縮 CONFORMED）。
- 效能：預檢只對 zh-TW 3× 做，每次載入約 0.1 秒；每次 `LoadLiveRuntime`（含測試）都付這筆成本。 （2026-10-02：規格 055 起四個通道各做一次，約 0.4 秒。）

### 3.2 接線

建立 3× zh-TW presenter 的步驟依序如下，不得改變順序：

1. 照現行用 lane 字型呼叫 `NewRuntimeManualOverlayLang`（不用 clone 建 presenter，否則 `halfFontsOf` 依指標快取會多留一份 half 字型，half 也與其他家族分歧）。
2. `presenter.font.Name = manualDerivedFontIdentity`（presenter 自有的衍生字型，改名不影響其他家族；固定格輸出位元組不變，已證實）。
3. `base := cloneManualBaseFont(font)`（名稱 `manualBaseFontIdentity`）；half 沿用 `presenter.half`（lane 字型的共用 12×24 半形字）。
4. 以這三個物件預檢（§3.1）。
5. 預檢全部通過才設 `presenter.e1Base = base`。預檢失敗時 derived 名稱可保留（與固定格輸出無關）。

其他：

- 不使用 `ManualSnapshotOwner`（它是 host 影格 ticket 路徑）。live 路徑維持現行的 `Apply`／`Frame`／`Draw` 生命週期與 `ManualPresentationBridge`。
- `SetStyle`：live 維持現行 `RuntimeManualOverlay.SetStyle`，只更新 style，不清 plan、不改狀態。**不得**照 `ManualSnapshotOwner.SetStyle` 的失效做法（ticket／epoch 語意，live 沒有）。
- compose 的手冊層必須檢查 `Draw` 的回傳：`rgba == nil` 時不得交給 `layer()`，這一格記 `skips["manual"]++`，手冊層這一格留原版英文。
- 不改共用 `xlate`、`BuildManualE1Plan`、`Apply`、`LoadManualEnglish` 的簽章、catalog 或字型檔。

### 3.3 不變量

1. 所有 2×（五種語言）與 3× 的 zh-CN、ja、ko、en 的 `LiveRuntime` 合成 RGBA（`Compose`）與實作前逐位元組相同。 （2026-10-02：3× 的 zh-CN、ja、ko 不再與實作前相同，見規格 055 §3.5。）
2. 3× zh-TW：與實作前相比，**矩形外零差**；矩形內可以相同也可以不同（39 段中 15 段本來就相同）。會不同的段落集合由單元測試列出（只記 key，不記內容）。
3. 機器狀態（記憶體、CPU、indexed、palette、停止步數）與倍率及 E1 開關無關，逐位元組相同。
4. 離頁（作答後清除）後手冊矩形與原版英文通道逐位元組相同（無殘字）；換題、返回的生命週期與現行相同。
5. 保留的英文專名（連續 ASCII 字母數字詞，含括號專名）不被列尾拆開；每列、全部字模與清除範圍都在既有安全矩形內（plan 本身的保證，預檢已驗 39／39）。
6. 失敗隔離：預檢或 runtime 失敗只關 E1，不停用 zh-TW 通道，也不使手冊家族卡住。

### 3.4 與本機英文關鍵字列並存

英文關鍵字列放在固定格段落的第 k 列之下（`first = k+1`）。E1 的段落列數 k' 若不大於 k，關鍵字列就不會與 E1 段落重疊，現有的列計畫（`ManualEnglish.plans`）不用改。

- **並存條件**：對 `ManualEnglish.plans` 內的每一題，E1 預檢記下的 k' ≤ 固定格的 k（`manualRows(translation, 36, 14)` 的非空列數，與 `LoadManualEnglish` 同算法；以輔助函式共用）。
  這個檢查在 `SetManualEnglish` 載入成功後做（該函式必須在第一個 step 之前呼叫，之後呼叫回錯，所以不與 `Apply` 競態；預檢在 `loadLane` 內早已完成，不重建 plan）。
- 全部成立：E1 保持啟用。現行 catalog 39 段實測全部成立（38 段 k' = k，1 段少一列，少的那列成為段落與關鍵字列之間的空白）。
- 任一題不成立（日後譯文改變使 k' > k）：E1 **整體關閉**（`e1Base` 設回 nil）、`manual-e1=off(keyword:N)`。這個取捨使 `Apply`（規格 005）與 `LoadManualEnglish` 的簽章完全不動。
- `manualEnglishPresenter.sync`：移除 `man.e1Plan != nil` 的排除；其餘畫法不變（用 `man.segmentFonts()` 的固定格半形格，derived 改名不影響輸出）。
- 摘錄部分排除時（`Excluded`）：被排除的題沒有關鍵字列，不參與並存檢查，E1 照常啟用。檔案層問題使面板關閉（`manEngOff`）時，E1 不受影響。
- 性質：`manualEnglishLayout` 對 k 單調，所以 k' ≤ k 時固定格放得下的關鍵字列在 E1 下一定放得下。

## 4. 不在範圍

- zh-CN、ja、ko 的 E1（另開 Issue；ja、ko 的容量要依 E1 的整詞換行規則重算，規格 051 的 13 列上限是固定格的算法）。 （2026-10-02：已由規格 055 實作。）
- 關鍵字列本身的版面改動。
- 2× 的任何變動、`xlate` 共用層、catalog、字型。
- host 的 `ManualSnapshotOwner` 路徑（已 CONFORMED，不動）。

## 5. 驗收

A、B 比對各自從**乾淨匯出**建置（`git archive <commit>` 或獨立 worktree，不含未入版控檔）：A 是實作 commit 的父 commit，B 是實作 commit；
收據記兩個 commit SHA 與兩個 binary 的 SHA-256。同一份 `text/`、同一個發行字型（記 SHA-256）、同一個快照與腳本；不拿既有 phase-316 收據當基準。測試套件也在乾淨匯出上跑。

1. 單元測試（dosgolem；合成 catalog 與字型，另有以 `BUCKROGERS_CHT_ROOT` 與 `BUCK_OWNER_PROJECT`（兩者都指向 Buck repo 根目錄，唯讀）閘控的正式 catalog 測試）：
   - 啟用矩陣：{zh-TW, zh-CN, ja, ko, LangTest} × {2×, 3×}，只有 zh-TW 3× 的 `e1Base` 非 nil。 （2026-10-02：矩陣已由規格 055 §5.1 反轉。）
   - 字型命名順序：未命名 derived 時預檢是 0／39；依 §3.2 命名後 39／39；預檢用的 generation 與 runtime 不同，幾何相同。
   - 預檢失敗負例：fixture 取「段落在固定格剛好 14 列，E1 整詞換行後超過 14 列」，固定格能建構、E1 預檢失敗：`e1Base` 為 nil、通道仍啟用、`DebugSummary` 含 `manual-e1=off(preflight:`。
   - runtime 退路：注入方式是把 presenter 的 `e1Base` 換成尺寸不符的字型（`BuildManualE1Plan` 回錯，固定格不受影響；不要刪 derived 字模，否則固定格退路也缺字）；同一題改以固定格顯示，後續題目照常，`DebugSummary` 為 `manual-e1=off(runtime)`；
     `Sync()` 因非 E1 原因第二次仍失敗時不標 `off(runtime)`、不無限重試。
   - compose 防禦：封存後破壞 derived 字型，`Compose(3)` 不 panic，回傳原版放大畫面，`skips["manual"]` 加一。
   - `SetStyle`：E1 段落可見時改 style，下一個 `Clear` 成功，`ActiveKeys` 歸零。
   - 並存：列出每段的（固定格 k，E1 k'）並斷言違反數為 0（只記 key 與數字）；合成摘錄（fixture 不含任何真實手冊單字，只用占位 ASCII 詞，通過 `LoadManualEnglish` 的格式檢查）下，E1 啟用時關鍵字列照畫，位置在 E1 段落之下、不重疊；
     以合成 catalog 製造 k' > k 的題，`SetManualEnglish` 後 E1 整體關閉、`DebugSummary` 為 `manual-e1=off(keyword:1)`；`ManualSnapshotOwner` 路徑的既有測試全過。
   - 位元組不變：`LiveRuntime` 層對五種語言的 `Compose(2)` 與 zh-CN、ja、ko、en 的 `Compose(3)` 比對實作前的位元組；E1 可見時 `Compose(2)` 與 `Compose(3)` 交替（模擬 F2），2× 位元組不變。 （2026-10-02：3× 的 zh-CN、ja、ko 部分見規格 055。）
   - 39 段中 E1 與固定格不同的 key 集合（只記 key）與其餘 15 段相同的集合。
   - 下列測試必須 PASS 而不是 SKIP：本規格新增的閘控測試、`TestManualE1PlanAll39PrivateCatalog`、`TestManualE1PlanDeimosPrisonEnglishTokens`；套件其餘 SKIP 列入收據，不作為失敗。
2. 離線同狀態重播（`workplace/phase316/run.sh` 的手冊題時點，五種語言 × 2×、3×，runner 的 `-manual-english` 旗標**不傳**）：A、B 的 live RGBA SHA-256 比對：2× 全部與 3× 的 zh-CN、ja、ko、en 相同；
   3× zh-TW 矩形外零差；`memory_sha256`、`cpu_sha256` 相同。取樣時點要把當下可見的手冊 `EventKey` 記入 runner 的 receipt JSON（新欄位，例如 `live_manual_visible_key`，由 `VisibleRequest` 取得；只寫進 receipt，不進 `DebugSummary`），
   並確認那一題屬於「E1 與固定格不同」的集合，A/B 差異真的出現在矩形內；否則換時點。
3. 實機玩家路徑（`buckrogers-play`，`workplace/phase311/run.sh`，`path-repair.txt`，zh-TW 3×）：
   - 不帶摘錄（確認 exe 目錄、`../Resources`、cwd 都沒有 `local/manual-english.tsv`）：A、B 逐格比較，機器雜湊相同；差異格僅限手冊頁矩形；作答後清除那一格矩形與 en 逐位元組相同；之後轉場無殘字。
   - 帶同一份本機摘錄（內容不入 Git；唯讀掛載）：A、B 逐格比較，差異只在手冊矩形內；B 的關鍵字列在段落之下、不與段落重疊；收據只記雜湊，不描述畫面內容。
4. 詞界樣本：至少兩種不同英文詞界的手冊段落（括號專名、列尾專名各一）在實機或離線重播顯示，畫面僅本機檢視，不入 Git，也不描述手冊內容。
5. 打包：`tools/package.sh linux` 通過；`TestPackagedLanes` 對 zh-TW 斷言 `DebugSummary` 含 `manual-e1=on`（只斷言一次，不依語言重複解讀）；完整版的預檢以載入時預檢為閘門。 （2026-10-02：規格 055 起對四種語言各自的通道區塊斷言。）
6. 文件：規格 005 的 E1 判定節加指向本規格的 pointer；規格 034 加指向本規格 §3.4 的 pointer；`docs/re/` 加收據；CONTEXT、WORKLOG、README 更新；Issue #21 依完成條件逐項回報後關閉或標明剩餘項。

## 6. 風險

- 日後譯文改變使某題 k' > k 時，完整版的 E1 會整體關閉（`off(keyword:N)`）；單元測試每次列出 (k, k') 讓這件事在改譯文時即被發現。
- 字型更換（規格 050 的 zh 字形）後 E1 預檢要重跑；預檢在載入時做，字型變動不會悄悄帶壞。完整版的倚天字型由打包依現行譯文重建，以載入時預檢為唯一閘門。
- runtime 退路依賴 `Sync()` 在錯誤時不推進 cursor（`ManualPresentationConsumer.Consume`）；若該語意日後改變，退路要重驗。
- 手冊題的具體英文詞界取決於玩家抽到的題；39 段的 plan 預檢是靜態保證，實機樣本只能抽樣。
- 本機英文關鍵字列只影響本機（摘錄不屬發行包）；一般版玩家路徑不受影響。
