# 053 — 手冊 E1（3× 英文專名不拆行）接入玩家路徑

狀態：**DRAFT**（2026-10-02，第二版；第一輪獨立審查的 9 項必修與 8 項建議已併入，待第二輪審查）。
日期：2026-10-02
Issue：#21
決定：
- 使用者 2026-09-25 選 E1（3× 英文字母 14px 字首 advance，保留手冊中的英文專名，整詞換行，2× 不變）並要求擴充 dosgolem 共用繪字層。
- 使用者 2026-10-02 選定這一輪只接 **zh-TW**，zh-CN、ja、ko 另開 Issue。
- 使用者 2026-10-02 選定 **E1 與本機英文關鍵字列並存**（完整版發行包自動載入 `local/manual-english.tsv`，不能因此永遠看不到 E1）。

前置：規格 005（手冊 presenter，E1 分支已無頭限縮 CONFORMED）、024（雙層封存）、034（本機英文關鍵字列）、039（半形）、051（ja、ko 手冊段落，不受本規格影響）、dosgolem 規格 234（共用繪字層）。

## 1. 為什麼要做

E1 的純值 plan（`BuildManualE1Plan`）與 3× 繪製只在 `ManualSnapshotOwner` 路徑啟用：`RuntimeManualOverlay.e1Base` 只有 `NewManualSnapshotOwner` 會設，該 owner 只被測試使用。
正式玩家路徑（`LiveRuntime`、`buckrogers-play`）的手冊 presenter 由 `live_lane.go` 的 `NewRuntimeManualOverlayLang` 建立，沒有設 `e1Base`，
所以 3× 的 zh-TW 手冊段落仍用固定格逐字元換列，段落中保留的英文專名會在列尾被拆成兩段。本規格把已驗證的 E1 plan 接進這條路徑，並讓本機英文關鍵字列與它並存。

## 2. 證據

來源：離線探針 `workplace/phase316/zz_p321_e1_probe_test.go.txt`（作者）與審查探針 `workplace/review053/zz_review053_test.go.txt`（審查者，乾淨匯出的 dosgolem `e992599`），
皆在 Docker、`--network none`、唯讀輸入下執行；兩者皆未入版控。字型：發行 zh-TW `buckrogers-unifont.golemfnt`（SHA-256 `7675cf4e97986985cbeb4b5ed447a2a56d68f4c5bdaf29f6f650164179042697`）、
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
9. 英文關鍵字列放在**段落第 k 列之下**（`manualEnglishLayout(k, …)` 的 `first = k+1`），k 取自固定格換列；它用固定格的半形格（`segmentStamps`）畫，與段落的版面技術無關。
10. live 的 compose 對手冊層 `Draw` 丟棄第三個回傳值（`live_lane.go:1039-1041`）；E1 的 `Draw` 在 `DrawChecked` 失敗時回 `(nil, nil, false)`（`manual_overlay_runtime.go:486-490`），之後 `layer()` 會對 nil 索引而 panic（強推論）。
11. `ManualSnapshotOwner.SetStyle` 只把狀態清成 `manualOverlayCleared`，之後的 `Clear` 會被拒（`手冊 clear 狀態無效`），`ManualPresentationConsumer` 錯誤時不推進 cursor，presenter 之後停在原版。live 的 `RuntimeManualOverlay.SetStyle` 只更新 style，plan 保留，接著 `Clear` 正常。
12. live 的 style 在 Begin 時就由 watcher 設好（`watcher.go:160-164`），E1 plan 不含 style，顏色由 `Frame` 每幀的 `show()` 套用。

未知：E1 在不同英文詞界的實機樣本（§5 補）；E1 對 ja、ko、zh-CN 字型的相容性（不在本規格範圍）；完整版的倚天字型由打包依現行譯文重建，雜湊可能與上列不同（以載入時預檢為唯一閘門）。

## 3. 契約

### 3.1 啟用條件與 DebugSummary

E1 在下列條件**全部成立**時啟用：語言通道為 zh-TW、倍率為 3×、載入時預檢全部通過。其他情形一律走現行固定格路徑，輸出位元組不變。
本機英文關鍵字列**不再**是條件（見 §3.4 並存）。`LangTest`（規格 040 §5.3 的測試語言）與 zh-CN、ja、ko 的 `e1Base` 必為 nil。

- 預檢：建 3× presenter 後，以 §3.2 命名的字型對 catalog 的**每一段**呼叫 `BuildManualE1Plan` 與 `plan.TextLayer`（`DisplayRequest{Generation: 1, EventKey, TextKey, Translation: 該段 catalog 譯文}`；不 `Apply`、不留狀態）。
  任一段失敗即整體不啟用 E1（`e1Base` 保持 nil），不逐段退回。預檢在 `loadLane` 內完成，早於 `SetManualEnglish`；失敗不停用語言通道。
- `DebugSummary`（zh-TW 區段，接在「英文列」之後）：`manual-e1=on`、`manual-e1=on(exempt:N)`（N 為 §3.4 的豁免題數）、`manual-e1=off(preflight:M)`（M 為失敗段數）、`manual-e1=off(runtime)`。
  只有計數與固定代碼，不得含譯文、錯誤原文或字元。
- runtime 退路：3× zh-TW 的 `manSync.Sync()` 回錯且 `e1Base != nil` 時，把該 presenter 的 `e1Base` 設為 nil、`manual-e1=off(runtime)`，
  然後在同一次 `syncManual` 再 `Sync()` 一次（失敗的 Request 沒被 consume，第二次改走固定格）。不改 `Apply` 的 E1 分支（規格 005 已限縮 CONFORMED）。
- 效能：預檢只對 zh-TW 3× 做，每次載入約 0.1 秒；每次 `LoadLiveRuntime`（含測試）都付這筆成本。

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
- 不改共用 `xlate`、`BuildManualE1Plan`、catalog 或字型檔；`Apply` 只增 §3.4 的一個豁免條件（對非豁免的鍵行為不變）。

### 3.3 不變量

1. 所有 2×（五種語言）與 3× 的 zh-CN、ja、ko、en 的 `LiveRuntime` 合成 RGBA（`Compose`）與實作前逐位元組相同。
2. 3× zh-TW：與實作前相比，**矩形外零差**；矩形內可以相同也可以不同（39 段中 15 段本來就相同）。會不同的段落集合由單元測試列出（只記 key，不記內容）。
3. 機器狀態（記憶體、CPU、indexed、palette、停止步數）與倍率及 E1 開關無關，逐位元組相同。
4. 離頁（作答後清除）後手冊矩形與原版英文通道逐位元組相同（無殘字）；換題、返回的生命週期與現行相同。
5. 保留的英文專名（連續 ASCII 字母數字詞，含括號專名）不被列尾拆開；每列、全部字模與清除範圍都在既有安全矩形內（plan 本身的保證，預檢已驗 39／39）。
6. 失敗隔離：預檢或 runtime 失敗只關 E1，不停用 zh-TW 通道，也不使手冊家族卡住。

### 3.4 與本機英文關鍵字列並存

英文關鍵字列放在段落之下，位置由段落使用的列數決定；E1 的段落列數可能與固定格不同，所以列的位置要依 E1 的實際列數重算。

- `LoadManualEnglish` 增加一個可為 nil 的參數 `e1Rows func(eventKey string) (k int, ok bool)`，回傳該題 E1 plan 實際使用的段落列數（`plan.lines` 中有 token 的最後一列加一）；
  傳入時，`ManualEnglish` 另存 `plansE1`（以 k 重算 `manualEnglishLayout`，字型涵蓋檢查同原本）。傳 nil 時行為與現行相同。
- **豁免**：固定格有關鍵字列、但 E1 的 k 讓關鍵字列放不下（`manualEnglishLayout` 失敗或字型涵蓋失敗）的題，記入 `e1Exempt`（鍵集合，只存 key）。這些題在 E1 啟用時仍走固定格（`RuntimeManualOverlay` 的 `Apply` 在
  `o.scale == 3 && o.e1Base != nil && !o.e1Exempt[eventKey]` 時才走 E1 分支）。原本就沒有關鍵字列的題（`Excluded`）不豁免。
  這個取捨的理由：看不到關鍵字列會讓使用者無法在本機玩這一題，比專名被拆行更糟。
- `SetManualEnglish`（必須在第一個 step 之前呼叫，之後呼叫回錯，所以不與 `Apply` 競態）：載入成功後對 zh-TW 通道的 3× presenter 設 `e1Exempt`。預檢早已在 `loadLane` 完成；
  `SetManualEnglish` 用 `manPres[i].font`／`half` 只做字形涵蓋檢查，與名稱無關。檔案層問題使面板關閉（`manEngOff`）時，E1 不受影響。
- `manualEnglishPresenter.sync`：移除 `man.e1Plan != nil` 的排除；`man.e1Plan != nil`（該題走 E1）時用 `plansE1[key]`，否則用 `plans[key]`。畫法不變（`man.segmentFonts()` 的固定格半形格）。
- 摘錄部分排除時（`Excluded`）：被排除的題既沒有關鍵字列，E1 照常啟用。

## 4. 不在範圍

- zh-CN、ja、ko 的 E1（另開 Issue；ja、ko 的容量要依 E1 的 14px 英文 advance 重算，規格 051 的 13 列上限是固定格的算法）。
- 關鍵字列本身的版面改動（只改它的起始列來源）。
- 2× 的任何變動、`xlate` 共用層、catalog、字型。
- host 的 `ManualSnapshotOwner` 路徑（已 CONFORMED，不動）。

## 5. 驗收

所有比對基準都在**同一 dosgolem 工作樹**上做 A/B：實作 commit 的父 commit 建 A（runner 與 `buckrogers-play`），實作 commit 建 B；同一份 `text/`、同一個發行字型（記 SHA-256）、同一個快照與腳本；
不拿既有 phase-316 收據當基準。測試套件在實作 commit 的乾淨匯出（不含未入版控檔）上跑。

1. 單元測試（dosgolem；合成 catalog 與字型，另有以 `BUCKROGERS_CHT_ROOT` 閘控的正式 catalog 測試，確認無 `--- SKIP`）：
   - 啟用矩陣：{zh-TW, zh-CN, ja, ko, LangTest} × {2×, 3×}，只有 zh-TW 3× 的 `e1Base` 非 nil。
   - 字型命名順序：未命名 derived 時預檢是 0／39；依 §3.2 命名後 39／39；預檢用的 generation 與 runtime 不同，幾何相同。
   - 預檢失敗負例：fixture 取「段落在固定格剛好 14 列，E1 整詞換行後超過 14 列」，固定格能建構、E1 預檢失敗：`e1Base` 為 nil、通道仍啟用、`DebugSummary` 含 `manual-e1=off(preflight:`。
   - runtime 退路：E1 啟用時注入 plan 建立失敗，同一題改以固定格顯示，後續題目照常，`DebugSummary` 為 `manual-e1=off(runtime)`。
   - compose 防禦：封存後破壞 derived 字型，`Compose(3)` 不 panic，回傳原版放大畫面，`skips["manual"]` 加一。
   - `SetStyle`：E1 段落可見時改 style，下一個 `Clear` 成功，`ActiveKeys` 歸零。
   - 並存：合成摘錄（fixture 不含任何真實手冊單字，只用占位 ASCII 詞，通過 `LoadManualEnglish` 的格式檢查）下，E1 與固定格的關鍵字列都能畫；豁免題走固定格；
     `ManualSnapshotOwner` 路徑的既有測試全過（owner 不設 `e1Exempt`）。
   - 位元組不變：`LiveRuntime` 層對五種語言的 `Compose(2)` 與 zh-CN、ja、ko、en 的 `Compose(3)` 比對實作前的位元組；E1 可見時 `Compose(2)` 與 `Compose(3)` 交替（模擬 F2），2× 位元組不變。
   - 39 段中 E1 與固定格不同的 key 集合（只記 key）與其餘 15 段相同的集合。
2. 離線同狀態重播（`workplace/phase316/run.sh` 的手冊題時點，五種語言 × 2×、3×，**不傳 `-manual-english`**）：A、B 的 live RGBA SHA-256 比對：2× 全部與 3× 的 zh-CN、ja、ko、en 相同；
   3× zh-TW 矩形外零差；`memory_sha256`、`cpu_sha256` 相同。取樣時點要把當下可見的手冊 `EventKey` 記入收據（只放 key，加入 `VisibleRequest` 的輸出或 `DebugSummary`），
   並確認那一題屬於「E1 與固定格不同」的集合，A/B 差異真的出現在矩形內；否則換時點。
3. 實機玩家路徑（`buckrogers-play`，`workplace/phase311/run.sh`，`path-repair.txt`，zh-TW 3×）：
   - 不帶摘錄（確認 exe 目錄、`../Resources`、cwd 都沒有 `local/manual-english.tsv`）：A、B 逐格比較，機器雜湊相同；差異格僅限手冊頁矩形；作答後清除那一格矩形與 en 逐位元組相同；之後轉場無殘字。
   - 帶摘錄（本機，內容不入 Git）：B 的畫面顯示關鍵字列於段落之下、不與段落重疊；豁免題數記入收據；畫面只在本機檢視，不描述內容。
4. 詞界樣本：至少兩種不同英文詞界的手冊段落（括號專名、列尾專名各一）在實機或離線重播顯示，畫面僅本機檢視，不入 Git，也不描述手冊內容。
5. 打包：`tools/package.sh linux` 通過；`TestPackagedLanes` 對 zh-TW 斷言 `DebugSummary` 含 `manual-e1=on`（只斷言一次，不依語言重複解讀）；完整版的預檢以載入時預檢為閘門。
6. 文件：規格 005 的 E1 判定節加指向本規格的 pointer；規格 034 加指向本規格 §3.4 的 pointer；`docs/re/` 加收據；CONTEXT、WORKLOG、README 更新；Issue #21 依完成條件逐項回報後關閉或標明剩餘項。

## 6. 風險

- 豁免題在 3× 仍可能拆英文專名：只在關鍵字列放不下時發生，數量由單元測試列出。
- 字型更換（規格 050 的 zh 字形）後 E1 預檢要重跑；預檢在載入時做，字型變動不會悄悄帶壞。完整版的倚天字型由打包依現行譯文重建，以載入時預檢為唯一閘門。
- runtime 退路依賴 `Sync()` 在錯誤時不推進 cursor（`ManualPresentationConsumer.Consume`）；若該語意日後改變，退路要重驗。
- 手冊題的具體英文詞界取決於玩家抽到的題；39 段的 plan 預檢是靜態保證，實機樣本只能抽樣。
- 本機英文關鍵字列的版面變動只影響本機（摘錄不屬發行包）；一般版玩家路徑不受影響。
