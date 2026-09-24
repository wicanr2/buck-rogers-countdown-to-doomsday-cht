# 工作歷程

## 2026-09-25 — 第三頁詞義校譯與手冊混排方向

- 子代理依第三頁原版 `THE NERVOUS CHATTER DIES DOWN` 的固定事件
  與畫面，把 `.003` 的「先前的喧鬧聲」限縮訂正為「緊張的交談聲」；
  第二、四頁無確證可改。三份專屬 catalog lint 通過。
- 24 份 TSV 的字元清單及本機倚天 2× 子集重建為 1,045 字，
  `build`／`verify` 通過。全體 catalog 一起交給單份 lint 時因
  既有跨檔共用 `character.skill.notice` 而正確報重複 key；改依
  契約逐份 lint，24 份均通過；第三頁 READY 版面與五項單元測試
  通過。這是驗證命令用法問題，非譯文重複或產品缺陷。
- 校譯後同一合法首題以新字型重生 control／2×／3×，原版狀態
  相等、矩形外零差；正式 Snapshot owner 定向測試通過，雙倍率
  RGBA 與前次逐位元相同。雜湊與私有路徑見[規格 024](docs/spec/024-manual-layer-group-font-identity-ready-candidate.md)。
- 第三頁校譯本身亦從合法第二頁終態重跑穩定入頁 A/B：雙倍率
  五行可見、零缺字、矩形外零差，control／2×／3× 的 indexed 與
  完整 machine／DOS state 相等；詳見[第一百四十四階段追加收據](docs/re/phase-144-story-page3-runtime-conformance.md)。
  初次 CLI 因缺必填 PNG 輸出被拒，補齊後同條件通過；另一次
  Docker 工具目錄誤掛 `/bin`，改掛 `/toolsbin` 後重跑通過，均屬驗證命令問題。
- 使用者選擇保留手冊中的 RAM、Deimos、Stockade，改善 3× 混排
  與英文詞界；排除示意圖中的未核准全中文新譯名。這是版面
  DRAFT 工作，不改手冊 catalog、原版判定或 2× 既有顯示；
  已另建[Issue #21](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/21)
  保存範圍、依賴、完成條件與素材邊界。
- ignored fork 的可丟棄 E1／E2 原型把 3× 英文改為整行共同游標
  14px／16px advance，英文詞與括號專名不拆，39 段均可容納、
  首題矩形外零差、2× 正式 RGBA 不變；主代理看過兩張原生
  960×600 圖並重跑四項定向測試與 vet。正式 presenter 未改，
  見[第二百二十三階段追加](docs/re/phase-223-manual-first-question-host-mixed-script-draft.md)。
- 使用者隨後選定 E1 的 14px 英文字母 advance，排除 E2／16px；
  此選擇不取代獨立 READY 審查與正式接線後的原版同狀態驗收。
- 獨立審查指出 E1 原型繞過正式雙層 owner，且共用 `xlate.Stamp`
  的 3× 座標無法精確表達 14px；39 段 tokenizer／標點與字模
  幾何也未完整驗。規格 005 的新增混排契約保持 DRAFT；已向使用者提出像素
  精度層要限於本遊戲手冊或擴充共用引擎的單一架構問題，並在
  ignored fork 安排不依賴此決定的 token／字模補證。
- 使用者選擇擴充 dosgolem 共用繪字引擎來承載 E1 的 14px
  實體像素 advance，排除 Buck 手冊專用旁路；正式共用 API、
  seal／snapshot 身分與舊覆繪逐位元相容仍需先審查至 READY。
- 另一位 Terra 在 ignored fork 交付 test-local 共用 PixelGlyph
  幾何原型；主代理獨立雙重重跑 14px 字首、括號 crop、透明格、
  失敗即關閉與合成舊 2× 測試及 vet 通過。正式 xlate、封存、
  Snapshot／Restore 與遊戲前端均未修改；見[第二百二十三階段追加](docs/re/phase-223-manual-first-question-host-mixed-script-draft.md)。
- 39 段 test-local tokenizer 已補英數識別字、括號與長引號
  處理，正式字型最大 ASCII 墨跡 8px；主代理解析私有收據
  後發現 3 行首、11 行尾空白，獨立審查又指出 `…` 禁行首
  漏洞。已明記 DRAFT 勘誤並安排 soft separator 與標點負例，
  不能以 39／39 round-trip 宣稱版面 READY。
- 後續 test-local 修正讓該 3／11 個邊界空白零寬保留而不漏原文，
  補 `…` 禁行首與跨 run 墨跡檢查；主代理獨立讀取 39 段
  私有收據，確認 14 個邊界空白皆寬 0。這只訂正 DRAFT
  版面缺口，未成正式手冊 presenter。
- dosgolem fork 新增並索引規格 234；獨立審查三輪修正
  `DrawChecked` 全層失敗即關閉、固定 `PixelGlyph` ABI、
  canonical font SHA-256、source／Restore 身分及 shared／adapter
  驗收範圍後，**僅共用 xlate API 契約**升 READY。
  已交派 production 共用層實作；Buck adapter 仍 DRAFT。
- 共用 `xlate` 第一段 production 在 ignored fork 本機提交
  `8f56d0e`：可選 `PixelGlyph`、全層 checked preflight、
  physical crop／透明格、legacy `Draw` 零寫入拒絕、
  optional 快照與字型 SHA-256 原子 Restore。獨立審查
  發現 parent 出界及字型尺寸溢位兩項 P1，已先回填規格
  再修程式並補負例；另補多筆壞 Restore、同名不同字模、
  舊 2× JSON／RGBA bytes 與雜湊順序測試。主代理以
  無網路 Docker 獨立雙重重跑 `go test ./xlate -count=2`
  及 vet 通過，root 殘留與本專案容器皆無。封存群組、
  adapter owner／layout 和玩家路徑仍待完成；不稱 234
  CONFORMED。

## 2026-09-25 — A 版沿用、手冊現行字型同狀態複驗與第九頁停止線

- 使用者再次選 A；正式 3× host 面板已是倚天原生 24×24 中文／
  16×24 ASCII，不重複改字型接線；遊戲畫布 3× 仍是獨立的 22×22。
  既有 Docker／Xvfb 映像重跑五標籤量測、正式繪製／2× 保持不變及
  拒絕 22 點輸入的三項定向測試，均通過。
- 舊私有首題 A/B 用的字型與譯文已過時，故從合法首題前狀態以
  現行 1,046 字字型重生 control／2×／3×。原版狀態三組相等，
  安全矩形外零像素差；正式雙層 Snapshot owner 亦與 CLI
  雙倍率 RGBA 逐位元相等。只證固定首題，不代表完整 Linux session。
  收據與失敗 fixture 勘誤見[規格 024](docs/spec/024-manual-layer-group-font-identity-ready-candidate.md)。
- 第九頁同一合法 state 的數字鍵盤 8／4／6／2 各一鍵有界雙重重播，
  全部已讀取，但到硬停仍無故事區 pre-write／像素變動／DOS 退出；
  探針增加斷言後定向測試與 vet 通過。遊戲內自然離頁不猜測，
  詳見[第二百一十九階段](docs/re/phase-219-story-page9-runtime-entry-ab.md)。
- 原版、掃描手冊、存態、截圖、倚天來源與衍生字型僅在 ignored
  `workplace/`；本輪 Docker 為無網路有界一次性容器，未發布素材。

## 2026-09-25 — 3× A 版再確認與 Delta 觀測器限縮複審

- 使用者再次選 A：3× host 設定面板採倚天原生 24 點，排除
  衍生 22 點。核對正式畫筆、規格與先前 Docker 定向測試，
  既有實作已符合；遊戲畫布字型不因本決定更動。
- 本機 ignored dosgolem fork 新增 tagged Delta 觀測器原型：
  callback 只見凍結 `CallView`、回傳 hook 增量；runner 在成功
  返回後同步安裝。合成 MZ 測試涵蓋動態 return hook、callback
  error／panic、視圖複本、受監看 stack 零額外讀取；內部負例證實
  「非空增量＋error」不裝 hook 且 machine 零步。合法原版首題
  checkpoint 與獨立 `Watcher.Install` 基線仍有 9 筆 observation、
  3 筆 presentation 及有限終態相同。Docker 定向測試、單 goroutine
  競態測試與 vet 通過；獨立複審仍判為 DRAFT，跨 goroutine 排他、
  正式 Owner 私有 boot／Close 及可玩入口尚未完成。
- 低階翻譯代理核對前 18 筆手冊來源，主代理以雜湊一致的本機英文
  HTML 快照抽查，訂正 9 筆確證誤譯；原文判定與 key 不變。手冊
  crosswalk、catalog、39 段 504 字版面檢查通過。24 份 TSV 重生的
  `font/characters.txt` 為 1,046 字，SHA-256
  `7aa7ed9f4fbff670cdba023b8c5f3a20486423c42393b94495c3c7da6eace55b`；
  本機 2× 倚天字型與 manifest 已 build／verify，正式前端的
  `TestLoadHostFontsFromReviewedManifestsLocal` 在 Docker／Xvfb 以
  新 2× 與既有 3× A 版通過。初次使用登入 shell 執行測試映像時
  `go` 不在 PATH，確認映像原有 Go／Xvfb 後改用非登入 shell 重跑
  通過，屬驗證環境而非產品缺陷。私有字型及原版手冊不入 Git。

## 2026-09-24 — 3× 面板字型定案核對與 Oracle 預算回繞修正

- 使用者再次選定 A：3× 設定面板採倚天原生 24 點。核對現行
  `frontend/ebiten` 畫筆、雙子集 loader、規格 004 與本機原型，
  既有實作已符合此限縮選項；未改遊戲畫布 3× 字型或 2× 排版。
  既有映像缺 `xauth`，故 `xvfb-run` 首次失敗僅屬測試環境；改用
  有 trap 的直接 Xvfb 後，相同 3× 字型前端定向測試與 vet 通過。
- 本機 dosgolem fork `7444caf` 修正 `Oracle.RunUntil` 的步數加預算溢位：
  修正前零步誤回預算耗盡，修正後執行前明確拒絕。通用回歸測試
  與先前 tagged DRAFT 矩陣同步更新；舊收據保留，研究紀錄追加
  勘誤。此切片不使正式 session／Linux 玩家入口完成。
- 子代理的原版首題 paired-checkpoint 測試經主代理改成單一標籤、
  不依賴其他未提交 DRAFT helper 的自包含收據，提交本機 fork
  `2c96d19`。主代理以既有 Docker 映像、唯讀原版與 checkpoint
  獨立重跑測試及 vet；手冊 begin／clear／request 與終點有限欄位
  兩側相同。未接正式 `Owner.Advance`，#18 維持開啟。

## 2026-09-24 — 正式手冊雙層封存元件

- 本機 dosgolem fork `cbd5683` 新增雙層 callback 封存投影與
  `ManualSnapshotOwner`，只提交四個正式程式／測試檔；其餘既有 ignored
  診斷檔保留。雙倍率合成正反例涵蓋字型內容、14 行身分、舊票失效、
  讀幀時失效及失敗後零部分 RGBA。主代理在唯讀、無網路 Docker
  獨立重跑定向競態測試與 `go vet`，均通過。
- [規格 024](docs/spec/024-manual-layer-group-font-identity-ready-candidate.md)
  仍為限縮 READY：caller 字型來源驗證、Linux session 接線、原版
  同狀態與正常玩家手冊路徑尚未完成，不稱 CONFORMED。

## 2026-09-24 — 第四、五頁跨頁引號校正與雙倍率重播

- 低階翻譯代理只修改第四頁末與第五頁末各一處引號，原文 key 不變。
  依既有合法原版存態，各重播 stable 與同執行 Enter 離頁的
  control／2×／3×，合計 12 組；雙頁皆零缺字、文字矩形外零差、
  原版 JSON 與存態同值，離頁 active 6／5→0 且 RGBA 回到 baseline。
- 私有收據在 ignored
  `workplace/page4-5-punctuation-recheck-20260924/manifest.json`
  （SHA-256 `b669b0e887a9ab7ac0e466c70bfc0ccea2679f4dc5c41d5f00426df4316aac23`）。
  只更新[第四頁](docs/re/phase-147-story-page4-runtime-ab-pending-audit.md#2026-09-24跨頁引號標點勘誤後重驗)
  與[第五頁](docs/re/phase-148-story-page5-runtime-ab-pending-audit.md#2026-09-24跨頁引號標點勘誤後重驗)
  原有固定路徑的限縮 CONFORMED 收據；其他路徑未知。

## 2026-09-24 — 手冊封存投影限縮 READY 複審

- 補上原始 layer 空 stamp、封存前同名異字模及讀影格時 owner 失效三項
  可丟棄負例；合成雙倍率、`vet`、競態測試通過。獨立複審將
  [規格 024](docs/spec/024-manual-layer-group-font-identity-ready-candidate.md)
  限縮升為 READY，僅授權手冊雙層封存投影與 session 字型身分正式實作。
  原版同狀態、玩家路徑與 Linux session 未因此完成。
- 本機倚天來源在 Docker 內按全部 24 份正式 catalog 重建字型 sidecar；
  字元聯集仍為 1,028 glyph，字模二進位 SHA-256 不變，sidecar SHA-256
  更新為 `d359ee25ae89b301daded39a1ba253b2324850f2b935ae57276e3a1377a1212c`。
  來源、字模、sidecar 只留 ignored `workplace/`，不加入 Git。

## 2026-09-24 — 手冊群組與前端故障的可丟棄原型

- 手冊背景／正文的封存群組模型已在 Docker 以合成 2×／3× 影格通過只讀一幀、
  字型深複製、群組竄改、Clear／模擬 Restore 與 callback 逸出負例，定向測試、
  `vet`、競態測試均通過；正式 owner 與跨 watcher 接線尚未實作，
  [規格 024](docs/spec/024-manual-layer-group-font-identity-ready-candidate.md)保持 DRAFT。
- 正式 `Game.Draw` 的可檢查 snapshot／3× 字型缺字故障，已由 ignored wrapper
  在下一次 Update 前同步通知合成 owner；目前只驗控制流程，沒有正式 session
  或資源 Close，[規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)
  仍是 READY 候選。獨立審查確認整批路由的完整快照、共同版本及不可失敗提交
  仍是 READY 前缺口。
- 第九頁既有合法 state 的 `8`／`2` 固定窗口未出現離頁相交寫入；依停止線不
  再延長同一探針。入頁已驗，自然離頁未知，Issue #20 保持開啟。

## 2026-09-24 — 第八頁閉引號勘誤與正式重驗

- 低階翻譯代理將第八頁第四行補上全形右引號，完成跨頁引號；catalog
  檢查與倚天字型覆蓋通過。原文鍵不變。
- 以同一合法第七頁 state 和唯讀原版，重跑穩定畫面及合法離頁各
  control／2×／3× 六條。兩倍率四 key、零缺字、矩形外零差，
  machine／DOS 同狀態；離頁 active 4→0、RGBA 等於 baseline。
  [第一百五十七階段](docs/re/phase-157-story-page8-runtime-conformance.md#2026-09-24-標點勘誤重驗)
  追加新收據與來源雜湊，保留舊收據作歷史；第八頁只維持原有限縮
  CONFORMED，沒有擴張完整遊戲中文化聲明。

## 2026-09-24 — 技能頁離開問句本體正式 A/B

- 本機 dosgolem fork 將兩句 exact 問句接到正式 watcher／presenter／收據
  runner；補上任意 writer、含同值 A000 首寫的本體 pre-write 清層，
  以及實際 DOS Exit 清層。Stop／Restore／Discontinuity／Fault 核心負例、
  雙倍率六格尾碼 sentinel 與定向 Go test／vet／race 通過。
- 從職業／技術各自合法 Escape 前 state，取得 control／2×／3× 的
  active、N、Y 私有收據；像素只改問句本體，四條終態全畫面無殘層，
  原版 JSON 與 indexed 逐 byte 相同。獨立審查核准
  [第二百零二階段](docs/re/phase-202-skill-exit-runtime-ab.md)的限縮
  CONFORMED；存讀檔、Restore 正式接線、前端與冷開機不在本次驗收。

## 2026-09-24 — 技能頁離開提示原版寫入與尾碼 DRAFT

- 從合法技能頁原版 state 以本機診斷 runner／probe 取得職業與技術
  問句的首次變值 A000 相交寫入，以及 dispatcher 外六格多色選擇
  尾碼；私有收據與兩個不同起始 state 的雜湊見
  [第一百九十七階段](docs/re/phase-197-skill-exit-confirmation-prewrite-draft.md)。
  主代理以固定 probe binary 分別重跑兩筆 watch-file，SHA 均相同。
- 新建[規格 020](docs/spec/020-skill-exit-confirmation-overlay-draft.md)
  作 DRAFT typed 覆繪邊界；N／Y 後含同值清除、尾碼完整重畫、
  正式同狀態 A/B 未完成，不能接 production。
- [第一百九十九階段](docs/re/phase-199-skill-exit-font-containment-draft.md)
  沿用既有本機字型解析器，在 Docker 對兩筆 DRAFT TSV 做 2×／3×
  靜態安全矩形與缺字檢查，兩者均零越界、零缺字；這不是正式
  原版執行期或 N／Y 清層收據。
- [第一百九十八階段](docs/re/phase-198-skill-exit-ny-all-store-prewrite-draft.md)
  用兩個固定合法 Escape 前 state 各重播 N／Y，對本體與尾碼各量
  首筆含同值 A000 store；career N、technical N 的尾碼和 technical Y
  本體均早於舊變值 watcher 的首筆，故正式清層不得依賴變值事件。
  八筆私有收據與可重生診斷來源已固定；完整尾碼清除、DOS 停止與
  執行期覆繪仍待驗。
- [第二百階段](docs/re/phase-200-skill-exit-body-only-lifecycle-fake-draft.md)
  建立 ignored typed fake，固定兩句 exact Entry／Return、四條 N／Y
  首筆、段內 offset 正規化、雙倍率尾碼 sentinel、pending／active 的
  Stop／Restore／Discontinuity／Fault 失效矩陣；主代理補兩個 Entry
  caller 負例後於 Docker 重跑全通過。
- [第二百零一階段](docs/re/phase-201-skill-exit-body-only-ready-review.md)
  獨立審查核准規格 020 的 body-only 限縮 READY，尾碼保留原版且
  不再要求逐格尾碼研究；正式 watcher／presenter、session bridge
  與同狀態 A/B 留待後續實作／CONFORMED，Issue #17 仍開啟。

## 2026-09-24 — 設定面板同批鍵盤隔離

- 獨立稽核指出正式 `Game.Update` 的 Apply＋Enter 同一更新回合會在
  面板收合後把 Enter 放入 BIOS；依使用者既定面板鍵盤隔離決策，
  先建 dosgolem READY spec 232，再以本機 fork `71f19cb` 修正。
  Apply／Cancel 同批多鍵均零 BIOS，關面板畫布鍵盤仍可轉送；
  Docker／Xvfb Go test、vet、race 及獨立程式審查通過。只將這個
  host 鍵盤邊界限縮標 CONFORMED，見[第一百九十六階段](docs/re/phase-196-ebiten-panel-batch-keyboard-gate.md)。
- 另由獨立代理建立[規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)
  的 DRAFT typed session 回合契約；instruction budget／step receipt、
  cold boot、active composite 與 Close 尚未正式實作，不因此升格規格 004。

## 2026-09-24 — 正式面板暫停與加入角色後七列逐寫入清層

- 本機 dosgolem `c273db6` 依獨立審查的 READY spec 231，讓正式
  `Game.Update` 在面板展開、Open／Select／Cancel／Apply 回合略過 `Advance`；
  2×／3× 真實 X11 測試驗收收合當回合零呼叫、下一關閉回合恢復。
  [第一百九十四階段](docs/re/phase-194-formal-ebiten-panel-pause-conformance.md)
  只將 callback 排程標為 CONFORMED，冷開機與完整 DOS session 未完成。
- 本機 dosgolem `540a522` 在正式收據加入不含原文／像素的 A000 pre-write
  watcher transition 記錄；以同一合法 state／十筆鍵量到七次 active→empty，
  row20 普通回寫後兩倍率覆繪均與 baseline 相同。獨立審查只將固定七列
  與第七列清層限縮標 CONFORMED；真正 Exit 等仍 DRAFT。
  詳見[第一百九十五階段](docs/re/phase-195-post-join-prewrite-runtime-receipt.md)。

## 2026-09-23 — 前端面板暫停的 fake 回合契約

- 依使用者已確認的「面板展開時暫停 DOS」決定，以 ignored 純 Go fake 驗證
  Open／Select／Cancel／Apply 同回合零 Step、下一關閉回合恢復，以及故障後
  `Close` 一次且不得再推進。主代理在既有無網路 Docker 映像重跑測試通過。
- 此收據只限 fake；正式前端仍缺 typed session、冷開機及混合事件分類。
  限制與來源雜湊見[第一百九十三階段](docs/re/phase-193-frontend-session-fake-draft.md)，
  規格 004 未升 READY。

## 2026-09-23 — 種族建立 runtime 覆繪與離頁限縮收據

- 從固定 `after-bios-space-100m.state` 以 Enter `100010000`、Down `100240000`、Up
  `100300000`、Enter `100400000` 重播 Create New Character → Pick Race → Down → Up → Enter。
  為隔離共享 dosgolem 後續提交，runner 由 `2755f7ca526b4e8fdfc469e30d9c0ffb871c4958` archive；
  `buckrogers-text-receipt/main.go` SHA-256 為
  `c19bde17973ecc1473042945f6a40f1cce8635b45ccfeaf1426c2d1ade586f1c`。
- 正式 menu TSV 和倚天 16×16 字型的 2×／3×各兩次確認前收據均有 13 events／requests／actions、
  零 miss、零缺字與逐 byte 決定性；安全矩形外差異為 0。最後 Enter 後 #100,406,278 的
  `026F:029C` `(bottom=22,right=38,top=2,left=1)` 清除使 active overlay 歸零，終態 RGBA
  等於 baseline，machine／indexed／palette 與 control 一致。
- 完整重播接著進性別頁的 4 筆 menu-only miss 是下一頁非 menu identity，未混入種族路徑的
  零 miss 結論。私有收據與 immutable runner 留在 `workplace/phase160-race-runtime/`；spec001
  只把固定路徑標為 CONFORMED，整體仍 DRAFT，generation／streaming 總契約與未覆蓋畫面仍缺。

## 2026-09-22：第九十五階段倚天 top-pad parser READY 規格（已完成）

- 使用者選定 `top-pad`：output row 0 為零、source rows 0..14 寫入 rows 1..15；`bottom-pad` 已排除。
- 以無網路、唯讀 Docker 探針核對 `ASCFONT.15`／`SPCFONT.15`／`STDFONT.15` 的固定身份與完整分區：
  691 glyph 全數覆蓋，映射為 ASCII 44、全形符號 12、常用區 634、次常用區 1；唯一空 glyph 是空白。
- 新增 phase 95 RE 收據與 spec 008，將 codec、保留區拒絕、top-pad、`GOLEMFNT` 回讀、原子輸出、
  synthetic／本機 integration 測試與不可散布邊界列為 READY；既有 Unifont 工具沒有改動。
- Docker 中正式 catalog lint、158 項 Python 測試與 691 glyph 探針皆通過。新增 #15 實作工作；本階段
  沒有寫 parser、字型二進位或 runtime hook，dosgolem 本機分支也未推送。

## 2026-09-21：第六十五階段角色資料頁執行期繁中覆繪

- 建立 35 筆安全矩形；`AC`／`THAC0` 只擴張到同列 col 35 動態值左界，其餘保持原文寬度。
- 真實 PNG 將 `THAC 指數` 訂正為「命中指數」；重建 74-glyph GNU Unifont 子集。
- dosgolem spec 038 依 READY→實作→CONFORMED；base／`Y` × 2×／3× 各雙重重播，矩形外
  差異皆為 0，raw framebuffer 不變。終態色號 15 為黑色的既有限制另行明示。

## 2026-09-21：第六十四階段角色資料靜態繁中請求

- 從 96 筆角色資料事件隔離 35 個靜態 exact identity；建立繁中 catalog、來源分級與動態值
  排除 verifier。
- dosgolem spec 037 依 READY→實作→CONFORMED；新增角色紙 catalog 旗標並沿用既有
  `MenuRequestWatcher`，未接 renderer。
- 四次 Enter 與其後 `Y` 分支各重跑兩次：118／149 events、43／52 requests；JSON 與
  framebuffer 各自逐 byte 相同，原版畫面雜湊未變。

## 2026-09-21：第五十四階段已保存角色加入隊伍（已完成）

- 由第五十三階段同一保存提示 state，使用預設 Enter 真正保存，再以 Down→Enter 進入 Add；
  Add 讀取 `A.WHO` 的名冊區段後列出角色 `A`。
- 在名冊按 Enter 後，原版顯示 `Loading...Please Wait`，完整讀取 259-byte `A.WHO` 與兩筆
  62-byte `A.stf`；完成後角色從可加入名冊移除，正常玩家加入鏈閉合。
- 兩次由空白 scratch 完整重播各有 18 events、2,611 FileOps、3 write metadata；JSON 只差
  scratch 絕對路徑，正規化後 SHA-256 都是
  `302f42b72a0536da4893892f0e79dc055a6b355ca70f98bb1f63b60380c9f68c`。終點 framebuffer
  與兩個保存檔亦逐 byte 相同。
- 未實作服務為空，沒有修改 dosgolem production code；第 50、52、53 階段已追加關閉勘誤。

## 2026-09-21：第五十三階段保存選項控制流勘誤（已完成）

- 從第五十二階段同一 `save-before.state` 比對 Left→Enter 與預設 Enter；兩路各獨立重播
  兩次，IP trace 各自逐 byte 相同。
- 預設 Enter 於 step `120,205,401`／`120,205,903` 建立 `A.who`／`A.stf`，檔案大小及
  SHA-256 在兩次重播一致；Left→Enter 不建立兩檔。先前 `NO`／`YES` 分支名稱與零寫檔結論
  已推翻並在 phase 49、50、52 文件追加勘誤。
- Left 造成的同 step 首次控制流分歧為 `120,000,036`，runtime `0C10:0309` 對
  `0C10:030B`；保存路徑的 DOS create／write／close 與小範圍 runtime trace 已保存。
- 兩路終點 framebuffer 仍逐 byte 相同。預設保存路徑的完整 memory 受 DOS 取時影響而未
  宣稱逐 byte 決定性；下一步接續 Add 重驗名冊。

## 2026-09-21：第五十二階段合法保存後段事件對齊（進行中）

- 上一輪分類為有進展；載入復古遊戲、規格閘門、dosgolem 與 IDA Pro 9.4 契約，建立並
  完整讀回第 52 階段 Goal。
- 七個正常玩家 checkpoint 證實圖示確認、`SAVE A? YES`、返回功能選單與 Add 選取均落在
  預期狀態；完整配置路徑最後 26 筆事件與第五十階段逐筆相同。
- spec 032／033 先達 READY，再實作可選 `-unimplemented` 與 `-state-out`；正式雙重重播的
  1,457-event JSON、framebuffer、scratch 逐 byte 相同，savestate 回讀後 1 MiB memory 亦
  逐 byte 相同。未實作服務與 DOS write 均為空，兩份規格升為 CONFORMED。
- 完整／未用技能點保存後 DGROUP 只差 `0EC0:388B`，但 Add 路徑對它零讀寫；heap 差異 bytes
  亦沒有被 Add consumer 讀取。IDA 9.4 一次性 START.EXE database 沒有 operand `0x388B`
  直接命中，未把零 xref 外推成沒有間接存取。
- Right 選圖不改保存結果；Down×3 曾誤認為 Drop，但實測為 Joystick-Mouse Initialize，已
  保留勘誤。空名冊的原版保存條件仍未知，未修改平台或遊戲語意。
- dosgolem 全部正式 packages test／vet 與 Buck Rogers／receipt race detector 通過。
- dosgolem 本機分支 commit 為 `4bb3cc9d83868ea2d827cff33b43e2585c7f16ac`，未推其遠端；
  專案 94 項 Python 測試亦全數通過。

## 2026-09-21：第五十一階段完整技能配置（進行中）

- 建立並完整讀回第 51 階段 goal；由正常 BIOS 路徑實測職業技能 80 點與技術技能 40 點，
  訂正早先把職業中途剩餘值誤當總點數的紀錄。
- 不使用 direct-entry、記憶體注入或未用點數確認捷徑，實際以 Enter／Down 將兩類點數配置
  歸零；技術技能 Escape 已無警告並進入身體圖示畫面。
- 第一個完整配置後的保存／名冊 probe 仍無 DOS write，scratch `CHARS.DAX` 與 pristine
  同雜湊，終點回到空名冊功能選單。現階段只把它列為待對齊的後段輸入／條件，不外推為
  dosgolem 缺口；正式雙重重播、verifier 與 CONFORMED 規格尚未完成。

## 2026-09-20：第三十階段種族選單反白與文字安全矩形

- 建立並完整讀回第 30 階段 goal；載入 GUI 還原與 localized geometry 契約，只處理
  presentation／selection，不研究確認後 transaction。
- implementation 前建立診斷多鍵排程 READY 規格；新增嚴格 `-bios-key-at` 與
  `-screen-out`，完成兩次 Enter→Down→Up 重播後標為 CONFORMED。
- Down 動態證實先 normal redraw Terran、再 selected redraw Martian；Up 先 normal redraw
  Martian、再 selected redraw Terran，四筆均通過 guarded post-call。
- 相同終點 steady／Down-only 只差 `(24,24)–(79,39)`、832 pixels；Down→Up framebuffer
  逐位元回到 steady，兩次 13-event JSON 亦完全相同。
- 新增 selection identity、text-safe rectangle 與 verifier；一般選項清除 col 1 含縮排原文，
  中文 draw anchor 改用動態證實的 col 3。39 項專案測試全綠。
- dosgolem 全部正式 packages test／vet 與相關 race detector 通過，本機 commit
  `d55a4c84c3474034257cddf58d6fa32cff3d60d4` 未推送遠端。本輪未選倍率或畫中文。

## 2026-09-20：第二十九階段功能選單執行期顯示請求 watcher

- 建立並完整讀回第 29 階段 goal；重新載入顯示／語意隔離與規格閘門契約。
- implementation 前建立 READY runtime watcher 規格，只核准 recorder → exact catalog →
  display request，不接 renderer、輸入或原版狀態寫入。
- 新增 `MenuRequestWatcher` 並擴充 `buckrogers-text-receipt` 的可選 catalog 模式；既有純事件
  模式保留，兩個 catalog 參數必須成對提供。
- 同一 #99,999,999 固定狀態於 #100,010,000 排入正常 Enter，直接得到九筆 request、零
  drop／pending／miss；content-free verifier 逐筆核對並拒絕全文洩漏。
- 新增兩項專案 verifier 測試後共 34 項全綠；dosgolem 全部正式 packages test／vet 與
  Buck Rogers／receipt command race detector 通過，子規格標為 CONFORMED。
- dosgolem 本機 commit 為 `c6a963dafaf3f060a43816f8a6acbda90aa8b7a0`，未推送其遠端；
  本輪未選 2×／3×、載入字型或繪圖。

## 2026-09-20：第二十八階段功能選單顯示請求純核心

- 建立並完整讀回第 28 階段 goal；倍率決策仍 pending，只處理不依賴 2×／3× 的純解析層。
- 在 implementation 前建立 dosgolem READY 規格，固定兩份正式 TSV 的 schema、SHA-256、
  exact identity、共用翻譯鍵與失敗即關閉契約。
- 新增 `MenuCatalog`：完整比對 length／SHA-256、caller、色號與座標，只為已完成事件回傳
  繁中 `DisplayRequest`；不保存英文全文、不繪圖、不送輸入或修改原版狀態。
- Phase 27 真實收據九筆全數解析；負向測試涵蓋 identity 各欄、sequence、大小寫格式、
  數值界線、重複與 TSV 關聯錯誤。Terran 選項／標題合法共用 text key。
- Docker 內全部正式 packages test／vet 與 Buck Rogers race detector 通過。兩個 Go image
  的登入 shell 找不到 `gofmt`，改用 image 內絕對路徑；非 root cache 改置 `/tmp` 後乾淨重跑。
- dosgolem 本機 commit 為 `0be85255d9cd5428c6b55a813410dcacbfd73a4f`，未推送其遠端。
- 尚未選定 2×／3×，未接 `xlate.Stamp`、矩形失效或玩家可見覆繪。

## 2026-09-20：第九階段 dosgolem 通用 xlate 基礎

- 建立並完整讀回第九階段 goal；逐檔讀取來源 `xlate`、測試與規格 202／203，確認來源
  `e515870`、目標基準 `d9c0c27`，未整串 cherry-pick 混有 oracle／cmd 變更的歷史。
- 只移植遊戲無關 package、測試與規格索引，建立 workplace dosgolem commit `b33cfbf`；
  沒有帶入 psychic-war 位址、譯文、狀態或字型資產。
- Docker 的 `xlate` 詳細測試全綠；正式 package roots 全數 exit 0。`go test ./...` 唯一失敗
  是被忽略 FD2 research workplace 的三個 `main` 衝突，已精確分類且未改寫他案資料。
- 記錄現行通用層只接受 3 倍倍率；2× 若獲選須先做規格修訂，未把既有能力當成產品定案。
- dosgolem 遠端 push 因缺少明確外傳授權遭安全審核拒絕；本機 commit 保留，未繞過。

## 2026-09-20：第八階段繁中字型與版面 prototype

- 由固定狀態正常重播 Enter，於九次 dispatcher entry 傾印來源，證實功能選單與種族選單
  的九筆字串；中文說明書頁 8–10 核對地球人、火星人、金星人、水星人、萬能工匠、
  沙漠跑者六個既有譯名。
- 建立 `text/menu.zh-TW.tsv`，只供輸出端顯示；沒有修改原版 EXE、資料、規則或存檔。
- 比對 psychic-war 的 `xlate` 與 curse_of_the_azure_bonds 的 text-safe rectangle／字形涵蓋
  經驗；排除授權未確認的倚天字模，prototype 改用具授權檔的 GNU Unifont。
- 以原始 320×200 色號畫面產生 2× 填滿 16×16 格與 3× 在 24×24 格置中兩案；兩案均用
  背景色清除已證實的 20 格矩形、最近鄰整數放大且不越界。PNG 留在 `workplace/`。
- 正式輸出倍率屬玩家可見取捨，保留兩案等待使用者決定；未把 prototype 當 production。

## 2026-09-20：第七階段 post-call 與 generation 順序

- 依新建並完整讀回的第七階段 goal，從固定功能選單狀態重播正常 BIOS Enter；第一筆
  `0763:0424` entry 為 #100,010,490，caller post-call `37F1:1856` 為 #100,025,943。
- 同步傾印來源 bytes，確認這筆仍是舊選單 `Create New Character`；最後一個 `r` glyph 的
  64 個不同 VRAM 位址於 #100,025,234–#100,025,833 全部寫完，post-call 晚 110 道指令。
- IDA Pro 9.4 一次性 16-bit database 證實 caller `37F1:1851` 是 far call、return 為
  `1856`；dispatcher 尾端是 `0763:04B0 RETF 0Ch`。九筆 Enter 畫面 dispatcher 的 entry／
  return 均符合 `SS` 相同、`SP = entry SP + 0x10`。
- 找到不能只看 return address 的反例：`37F1:15BD` 在第一筆真正以它為 return address 的
  dispatcher 之前，已因正常 fall-through 命中一次。DRAFT 因此要求 entry pending frame、
  return address、`SS` 與 `SP` 四者共同配對。
- 已閉合 Enter 時間線：舊選單 post-call #100,025,943 → 矩形失效 #100,028,739 → 清除返回
  #100,032,997 → 新畫面 dispatcher #100,033,190 → post-call #100,040,266。現有 `OnCall`
  足以表達 guarded return，未證實需要先擴充通用 dosgolem API。
- 尚未建立 production adapter；下一階段是首批繁中譯文、字型／text-safe rectangle 與
  可丟棄 A/B 覆繪 prototype。

## 2026-09-20：第六階段清除路徑與 hook 邊界

- 依新建並讀回的第六階段目標，以 workplace dosgolem 分支重播 Enter 與 Escape 正常路徑；
  保存 runtime segment bytes、IP trace、暫存器、caller、VRAM 寫入與呼叫計數。
- 訂正先前定位：watchpoint 記錄的 `0CF4:1B3C` 是 `REP STOSB` 後的下一個 IP，實際寫入在
  `0CF4:1B3A`；`0CF4:1B2B` 只是一個通用 byte-fill，已排除為正式 invalidation hook。
- IDA Pro 9.4 主證據與 objdump 交叉驗證均證實 `026F:029C..0508` 是依模式清除邏輯格矩形
  的例程。Mode 13h 下，Enter 動態為 168 列×304 bytes，Escape 返回為 184 列×312 bytes；
  首末 VRAM offset 與靜態公式一致。
- Enter 的 byte-fill 觀測窗有 169 次呼叫，其中 168 次屬矩形例程，另一次 caller 為
  `37F1:14DC`；已分開計數，未用總數冒充矩形高度。
- IDA 初版探針先後暴露舊 API、raw loader base、資料庫保存與退出 API 問題；只將無 traceback、
  schema／雜湊／16-bit／非 root 全部通過的 fill-v5 納入證據。rectangle-v1 的函式尾界落在
  `RETF 8` 中間，已以 `[0x029C,0x0509)` 重建 rect-v2；舊產物保留在 `workplace/` 作勘誤。
- DRAFT 現只把 `026F:029C` 列為帶參數的矩形失效候選；尚未實作 production adapter，下一個
  缺口是 `0763:0424` 原版繪製完成後的 post-call／generation 事件。

## 2026-09-20：第五階段 Escape 返回與 workplace dosgolem 分支

- 依新建並讀回的第五階段目標，以原版正常 BIOS Escape 從 `PICK RACE` 返回功能選單；
  未使用 memory poke、傳送、forced-win 或原版資料改寫。
- 依使用者指示，將乾淨 dosgolem 複製到被忽略的 `workplace/dosgolem/`，建立
  `buck-rogers-cht-output-overlay` 分支；基準為 `d9c0c27ca9af8239c7e96272a7165e03d7da04bf`，
  後續實驗改由該副本執行。
- Escape 在 #100,310,138 被原版取走；第一筆 dispatcher 在 #100,310,464 發生，
  `PICK RACE` 標題像素 `A000:1549` 至 #100,316,673 才由 `0CF4:1B3C` 清除。
- 終點 VRAM 逐位元等於既有功能選單基線，第二次獨立重播亦相同；DRAFT 因此取得一進一退
  兩條正常路徑的失效證據，但 `0CF4:1B3C` 尚未證實為通用清除 hook。
- 首次將 checkpoint 與 `-steps` 設成相同步數時，因 probe 在終點前先退出而未寫出狀態；
  改以終點多一道指令、checkpoint 維持原步數後成功。此為工具命令的開區間行為，非遊戲失敗。

## 2026-09-20：第四階段選單轉場與失效生命週期

- 使用者確認維持 dosgolem 輸出端繁體中文化並排除 clean-room remake；已同步更新
  `CONTEXT.md`。
- 依新建並讀回的第四階段目標，從 `after-bios-space-100m.state` 以 BIOS BDA Enter 正常
  進入 `PICK RACE`；未使用 memory poke、傳送或 forced-win。
- Enter 在 #100,010,174 被原版取走；新 dispatcher 在 #100,010,490 開始，但舊選單像素
  `A000:838A` 直到 #100,031,031 才被 `0CF4:1B3C` 清除。DRAFT 因此改為保守地在轉場輸入
  被原版接受時失效，未把下一筆字串輸出誤用為清除訊號。
- 相同起點、Enter 與終點步數重播兩次 raw VRAM byte-for-byte 相同。兩次滑鼠候選點均被
  原版讀到但沒有畫面變化，保留為輸入語意未知，未強行推定熱區。

## 2026-09-20：第三階段中文手冊 archive 清冊

- 依本輪新建並讀回的 `docs/goals/phase-3-manual-input-inventory.md`，檢查既有 Docker
  映像後重用 `coab-manual-extract:bookworm-v1` 的 `lsar`／`unar` 1.10.1。
- RAR 唯讀掛載、無網路執行：80 個 archive 項目完整性測試全數通過；解壓 79 個實體檔案
  到被忽略的 `workplace/manual-extracted/`，並產生逐檔 SHA-256 manifest。
- 文件只保存 archive metadata、工具、雜湊與掃描檔 archive-order 定位；未做 OCR、內容
  摘錄、題目配對或中文顯示，也未將原始／解壓素材納入 Git。

## 2026-09-20：第二階段文字分派與 DRAFT

- 依本輪新建並讀回的 `docs/goals/phase-2-text-dispatch-and-lifecycle.md`，由既有固定狀態
  重跑 dosgolem probe，沒有改動原版或 dosgolem 程式碼。
- 傾印並以 16 位元反組譯檢查執行期 `0763` 段；證實 `0763:0424` 長度前綴 byte-string
  dispatcher、`0763:026B` 字元 renderer、`0763:1809` glyph wrapper 與
  `0763:183A..1863` pixel primitive 的資料流。
- 以段:位移在 #71,107,500 傾印 `5747:0002`，取得長度 `0x14` 與 ASCII
  `Create New Character`；詳情與推論等級見 `docs/re/phase-2-text-dispatch-and-lifecycle.md`。
- 首次以 `-dump-mem-at` 將實模式地址誤作 IDA 地址，得到全零輸出；已用 `-dump-seg` 在同一
  固定流程重跑並更正。這是觀測位址空間失誤，不是原版資料結論。
- 新增覆繪 DRAFT，明定清除／捲動、中文字型與安全矩形尚未解決；未新增 production 程式、
  翻譯、字型或 adapter。

## 2026-09-20：第一階段原版可觀測基線

- 在無網路、唯讀原始輸入掛載的 Docker 容器中建立 ZIP／RAR 雜湊清冊；ZIP 解壓到
  `workplace/original/BRcdoom/`，RAR 僅完成格式與雜湊登記。
- 以 dosgolem commit `d9c0c27ca9af8239c7e96272a7165e03d7da04bf` 啟動真實
  `START.EXE`／`GAME.OVR`，保存 #70,000,000 的狀態並以 BIOS BDA 空白鍵到達功能選單。
- 同一固定狀態獨立重播兩次，Mode 13h raw VRAM 雜湊一致；研究收據索引於
  `docs/re/README.md`。
- IDA 9.4 最小探針建立被忽略的 `START-v2.i64`；其靜態位址空間與 dosgolem 執行期地址
  已在證據文件分開記錄。
- 環境／工具限制：Mode 13h 不能使用 planar `-dump-at`；改以 `-dump-vram`。現有離線映像
  沒有 RAR 解壓器，故未假裝已取得手冊內容。兩者均非原版功能缺陷。
- 本批工作使用一次性 `docker run --rm`；未建立本專案長駐容器。原始素材與收據仍在
  `workplace/`，沒有納入 Git。
# 2026-09-20：第十階段 catalog 與 GOLEMFNT 建置管線

- 建立並完整讀回第十階段 goal；依路由載入在地化顯示／語意隔離、字型與規格閘門契約。
- 新增失敗即關閉 TSV lint、決定性字元清單與 Unifont `.hex`／`.hex.gz` 到 16×16
  `GOLEMFNT` builder；6 組 Python 正反向測試全數通過。
- 現有 8 筆譯文導出 24 個唯一字元；本機 Unifont prototype 為 904 bytes，字型二進位留在
  被忽略的 `workplace/`，未把測試來源升格為正式產品字型。
- workplace dosgolem 新增 `cmd/fontcheck`，直接以 `xlate.LoadFont` 回讀，確認 24 個 glyph
  覆蓋合併譯文的 29 個碼點；Go command 與 `xlate` 測試均通過，本機 commit 為
  `8a224601a7d09fc8d0f63ab65828eb7f64fa0200`。
- Go 映像的登入 shell 重設 PATH，兩次造成 `gofmt` 找不到；固定 PATH 並用非登入 shell
  後乾淨通過，分類為容器環境問題。

# 2026-09-20：第十一階段手冊查詢映射

- 建立並完整讀回第十一階段 goal；以已載入 A 存檔的固定狀態，從功能選單正常送入
  六次 Down 再 Enter，取得第一個手冊查詢畫面。
- workplace dosgolem 新增具名 BIOS 鍵、scratch 還原後 override、DOS FindFirst 目錄屬性與
  `-call-length-string`。後者在繪圖呼叫當下保存共用暫存區，證實題目是英文 Log Book
  第 34 頁 `Deimos Prison` 第十字。
- 輸入明確錯誤的 `x` 後，原版立即重抽為第 41 頁 `Technical Skills` 第二字；未繞過、
  未自動作答。
- 對回中文掃描 `SCAN0352_039.jpg` 印刷頁 73 的「49. 在監獄中」，建立一筆繁中
  短段落 catalog 與 DRAFT 映射。原圖、整頁 OCR、state、VRAM 與 trace 均留在被忽略的
  `workplace/`。
# 2026-09-20：第十二階段手冊題庫結構

- 建立並完整讀回第十二階段 goal；以 dosgolem 執行期資料與 IDA Pro 9.4 追查手冊題庫，
  證實 `0EC0:00C2..0553` 有 39 筆、每筆 30 bytes。
- 保留 raw offset／bytes／執行期 segment 與 IDA database 位址；證實頁碼、標題長度與
  18-byte 區、序數、答案長度與 8-byte 區，以及 `encoded - 6 + field_length` 解碼公式。
- 新增失敗即關閉的 `tools/manual_questions.py` 與 5 項測試。工具只輸出頁碼、標題、序數
  與 offset；答案只驗證結構容量，不解碼、不輸出、不用於自動作答。
- 由真實資料重生 `text/manual-questions.tsv` 並逐位元核對；第 32、38 筆分別吻合動態
  `Deimos Prison` 第十字與 `Technical Skills` 第二字。
- 中文來源目前仍只有 `Deimos Prison` 唯一確認；其餘 38 筆維持未知，未模糊猜補。
# 2026-09-20：第十三階段繁中手冊來源對照

- 建立並完整讀回第十三階段 goal；確認第一個掃描序列是操作說明，題庫來源位於第二個
  `SCAN0352_*` 冒險者日誌序列，未混用冊別。
- 重用 `tvg-magazine-ocr:rapidocr-1.4.4` 在無網路一次性容器處理必要頁面；OCR JSON 只留在
  `workplace/manual-ocr/` 作搜尋線索，正式文件只保存短小錨點及雜湊。
- 建立 39 筆 `manual-source-crosswalk.tsv`：35 筆已證實、3 筆強推論、1 筆未知；每筆來源
  均附 archive-order、掃描 SHA-256、印刷頁與中文錨點。
- `Deimos Prison` 以條目 49 驗證，`Technical Skills` 以印刷頁 87 中英並列附錄表驗證；
  `Roll.` 的下一頁不在素材中，沒有猜補。
- 新增失敗即關閉對照驗證器及 4 項測試；連同既有題庫測試共 9 項通過，實際 manifest
  雜湊與現有中文 catalog lint 亦通過。未逐字校訂的 OCR 段落沒有加入顯示 catalog。
# 2026-09-20：第十四階段首批短篇手冊段落

- 建立並完整讀回第十四階段 goal；選取八筆來源已證實、單一短段落的題目，避免在尚未決定
  分頁格式前處理長章節或表格。
- 在一次性 ImageMagick 容器從唯讀原始掃描重生八張半頁裁切，逐張目視校訂；OCR 只作前輪
  定位線索，沒有把 OCR 誤字搬入 catalog。
- 新增八筆繁中手冊段落及 `manual-events.tsv`；連同既有 Deimos 共 9 筆。事件只保存頁碼、
  英文標題、序數與文字鍵，不含答案或自動輸入資料。
- 新增 `manual_catalog.py` 與 4 項反向測試，失敗即關閉檢查題庫身分、confirmed 來源、
  event key、唯一文字鍵與孤兒 catalog；全套 19 項測試與真實四檔驗證通過。
- 九筆文字長度為 35–236 Unicode 字元；只記錄為後續 prototype 輸入，未推定能放進單頁，
  未決定 2×／3× 或 production 版面。
# 2026-09-20：第十五階段第二批短篇手冊段落

- 建立並完整讀回第十五階段 goal；選取 Damage、Terrine 與六筆旅程條目，均為來源已證實且
  可由單一段落表示的內容。
- 在一次性 ImageMagick 容器重生八張半頁裁切並逐張目視校訂；Talon 與前輪 Great Rift
  共用同一半頁，但文字與事件鍵分開保存。
- 事件與繁中 catalog 由 9 筆增至 17 筆；沒有答案、自動輸入、原版資料改寫或未決分頁格式。
- 全套 19 項測試、catalog lint 與真實題庫／來源／事件／文字交叉驗證通過；新增段落長度
  為 31–216 Unicode 字元，未把字數誤當版面完成證據。

# 2026-09-20：第十六階段第三批已證實手冊段落

- 建立並完整讀回第十六階段 goal；由題庫、來源對照及既有事件表找出 18 筆尚未映射的
  confirmed 候選，再逐張目視原圖判斷內容形狀。
- 只納入 2456(Now)、Unused Skills、Range、Rocketships、Earth 五筆完整且非表格／跨頁內容；
  其餘 13 筆依長章節、跨頁、清單或表格留下明確排除原因。
- ImageMagick 首次沿用固定裁切尺寸時即由實際影像尺寸發現漏邊，未採為證據；正式裁切改用
  各圖東／西 50%，逐張目視校訂並保存 SHA-256 收據。
- 事件與繁中 catalog 由 17 筆增至 22 筆；全套 19 項測試、catalog lint 與真實四檔交叉
  驗證通過，新增段落長度為 35–190 Unicode 字元。

# 2026-09-20：第十七階段手冊分頁與倍率 prototype

- 建立並完整讀回第十七階段 goal；依共同決策技能只做可丟棄 2×／3× 對照，不替使用者
  選定倍率或改 production 路徑。
- 由 dosgolem 真實手冊查詢 VRAM 的色號逐列／逐欄量得金框內部
  `[7,312)×[7,184)`，以一格內距建立 36 欄×17 行正文、每頁 612 字的共同格線。
- 使用正式 236 字 Jupiter Arrival 段落重生兩種倍率，各為 7 行／1 頁；另用明示的三次
  重複壓力樣本驗證 708 字為 20 行／2 頁，所有輸出在安全矩形外均為 0 px 變更。
- 逐張目視確認金框、正文與頁尾；整張預覽造成第二頁標題似乎消失，放大裁切證實像素完整，
  因而未把檢視縮放問題記成產品缺陷。
- 回查 dosgolem `xlate`：現行 `Draw` 只接受 3 的倍數倍率，`Layout` 是每個 Unicode 字元
  一格。2× 需擴充通用 renderer；3× 已受支援但 16×16 字模相對畫面較小。

# 2026-09-20：第十八階段手冊題目世代與舊覆蓋失效

- 建立並完整讀回第十八階段 goal；從 #299,999,999 固定狀態以 BIOS BDA `x`、Enter 重播
  既有錯答路徑，未改寫答案、記憶體或原版判定。
- 兩次重播均取得相同九筆新題 dispatcher、同一矩形清除與按鍵消費序列；終態 raw VRAM
  SHA-256 同為 `769cb2925b05bd6aeabe6fb5f4bc0872b57ae58507daf1fc02e9ca1d2340b4af`。
- 窄時間窗畫面證實新題前三筆先覆寫，`026F:029C` 局部清除才出現；排除等待整面空白及
  第一筆後立即畫中文。DRAFT 契約改為題首 entry 先失效舊世代，`word?` guarded post-call
  才顯示完整新題段落。
- 首次執行因非 root Go cache 指向 `/.cache` 失敗，第二次因狀態保存的 `/orig` 未掛載失敗；
  固定 `GOCACHE=/tmp/go-build` 並將已驗證原版目錄唯讀掛到 `/orig` 後乾淨重跑。兩次失敗
  都未產生可誤認為成功的 VRAM 收據。

# 2026-09-20：第十九階段手冊題目事件收集器 prototype

- 建立並完整讀回第十九階段 goal；在倍率決策 pending 時，只處理不依賴 2×／3× 的事件
  收集器，維持 DRAFT 規格與 production 閘門。
- 被忽略的 Python prototype 將題首 entry、六筆 guarded post-call、局部 clear 與 generation
  token 建模；真實第十八階段事件重建唯一鍵 `41 / Technical Skills / second`，不保存答案。
- 9 項正反向測試通過；缺欄、亂序、重複、未知 caller、錯誤常值／頁碼及舊 generation
  延遲返回均不會產生顯示請求。prototype 保留在 `workplace/phase19/`，未移入正式路徑。

# 2026-09-20：第二十階段手冊 catalog 顯示請求 prototype

- 建立並完整讀回第二十階段 goal；載入顯示／語意隔離契約，維持翻譯只由正式 UTF-8 TSV
  提供，沒有把中文段落或答案內嵌到 prototype。
- 發現 runtime 輸出英文序數詞而事件 TSV 保存數字；只採用 dosgolem 已動態證實的
  `second → 2` 與 `tenth → 10`，未以一般英文常識批次猜補其餘序數。
- 正式 TSV 的 `Deimos Prison / tenth` 唯一命中 73 字顯示請求；尚未收錄完整段落的
  `Technical Skills / second` 明確不顯示，沒有模糊比對或臨時補文。
- 12 項正反向測試涵蓋 generation、精確身分、題目／事件／文字鍵唯一性、孤兒鍵、無效
  UTF-8、ordinal 歧義與顯示請求無答案；prototype 仍只在 `workplace/phase20/`。

# 2026-09-20：第二十一階段手冊序數詞橋接證據

- 建立並完整讀回第二十一階段 goal；載入 IDA Pro 9.4 技能、工具契約、逆向證據與規格閘門。
- IDA Pro 9.4 匯出證實 `2A33:02B7..02D2` 讀題庫 `+14`、乘 `0x13`、加 `DS:339B`，索引
  `0EC0:33AE..3459` 的 first 至 tenth 十個長度前綴 slots；second／tenth 另有動態事件交叉驗證。
- 第一次 IDA 未指定 processor，腳本未執行；第二、三次分別遇到 `mem2base` module 與參數
  API 差異。改用 `ida_loader.mem2base(..., -1)` 並從新 database 重跑後，JSON schema、`.i64`、
  位址空間、輸入雜湊與輸出擁有權均通過；失敗 fragments 已逐一刪除。
- 新增可重生 `manual-ordinals.tsv`、解析器與 7 項測試；現有 22 筆事件使用的 2–10 全部
  涵蓋，原版表中的 1 亦保留。資料不含答案，尚未接入正式 adapter。

# 2026-09-20：第二十二階段 dosgolem xlate 通用整數倍率

- 建立並完整讀回第二十二階段 goal；載入復古中文化、CJK 點陣介面與規格閘門契約。
- workplace dosgolem 的 `xlate.Draw` 改為接受正整數倍率；預設字模倍率使用
  `max(1, scale/3)`，讓 2× 可畫 16×16 字模並保留既有 3×／6× 行為。
- 新增 2× 精確 footprint／色彩、非法倍率不改輸出及短緩衝區安全裁切測試；所有正式 Go
  packages（排除 `workplace/`）在無網路一次性 Docker 容器全數通過。
- production `xlate.LoadFont` 讀取真實 `menu-unifont16.golemfnt`，2×／3× 均畫出繁中
  「地球」；PNG 與 JSON 收據只留在被忽略的 `workplace/phase22-xlate-smoke/`。
- dosgolem 本機 commit 為 `ef7f8db32b20a6b9eb6d810bd4e6b99187c55f44`，未推送其遠端；
  本階段沒有替使用者選定產品倍率，也未接入 production adapter。
- 首次兩個 Go 容器因登入 shell 遺失 `/usr/local/go/bin`，修正後又發現非 root 快取預設為
  `/.cache`；改用映像內絕對路徑及 `/tmp` 的 `GOCACHE`／`GOPATH` 後乾淨重跑。兩者皆為
  容器環境問題，不是 renderer 缺陷。

# 2026-09-20：第二十三階段手冊事件 adapter 規格與正式核心

- 建立並完整讀回第 23 階段 goal；重新載入復古中文化、dosgolem 能力與規格閘門契約，並
  由主機 gh 回讀 Issues #6、#8 的遠端權威狀態。
- 將第 18–21 階段證據審查成 dosgolem `007-buck-rogers-manual-event-adapter` READY 規格；
  只批准未接 hook／renderer 的純核心，不把所有入口覆蓋的強推論冒稱已證實。
- 新增 `apps/buckrogers` Collector 與 Catalog：generation、poisoned 復原、原版 1–10 序數、
  三份嚴格 TSV 與 exact-match 顯示請求均有正式 Go 測試，不含答案或輸入副作用。
- 首次 Go 測試因測試變數 `g2` 超出作用域而未編譯；修正測試後乾淨重跑。契約複核再補上
  event ordinal 必須存在於原版橋接表的載入拒絕，避免把無法命中的壞資料視為可用 catalog。
- `go vet`、race detector、正式專案 TSV 與 dosgolem 所有正式 packages 全數通過。本機
  dosgolem commit 為 `8ce092f29d000ea7e6765c4f3389fe484aefa555`，未推送其遠端。
- 產品端 `003-manual-event-adapter` 只保存整合邊界與權威指標；總體手冊覆繪仍為 DRAFT，
  沒有選定 2×／3× 或接入玩家可見路徑。

# 2026-09-20：第二十四階段手冊 runtime watcher 與真實事件收據

- 建立並完整讀回第 24 階段 goal；載入復古中文化、dosgolem 與規格閘門契約。
- 新增 READY runtime watcher 規格與 `apps/buckrogers.Watcher`；dispatcher entry 保存字串、
  caller、SS、SP 與 generation，只有三重 guarded return 通過才提交 Collector。
- 新增 `cmd/buckrogers-receipt`，只透過 dosgolem internal state 重播既有診斷狀態，沒有擴張
  `oracle` 公開持久化 API；輸出只含事件鍵、文字鍵與翻譯字數。
- 第一題由 #266,399,999 跑至 #266,557,246，精確產生
  `manual.page34.deimos_prison.word10`／`manual.log.49.deimos_prison`／73 字元請求；沒有注入按鍵。
- `go test ./...` 首輪只被既有 `workplace/fd2-input-parity-20260907` 重複 `main` 阻擋；排除
  非正式 `workplace/` 後，全部正式 packages 的 test／vet 與 watcher race detector 通過。
- 專案 26 項正式 Python 題庫、序數、來源、catalog 與字型資料測試全數通過。
- 本階段未選 2×／3×，未建立 renderer、分頁輸入或玩家可見完成聲明。
- dosgolem 本機 commit 為 `38585dcd9e3861b6fa64a1b89dbec19e5a038dd7`；依授權邊界未推送
  dosgolem 遠端。

# 2026-09-20：第二十六階段 README 遊戲歷史與技術定位

- 第 25 階段 2×／3× 父層決策仍等待使用者確認；依共同決策閘門沒有把沉默視為授權，改做
  不依賴倍率且由遠端 Issue #11 明確要求的 README 工作。
- 建立並完整讀回第 26 階段 goal，載入 README 標準與專案文件職責契約。
- 以 SSI 1992 年產品目錄、原版 Rule Book 保存掃描、MobyGames 版本與 DOS credits 查證
  1990 年平台、開發／發行、TSR 授權、Gold Box 系譜與玩法結構；README 相鄰提供來源連結
  並記錄 2026-09-20 查閱日期。
- README 明確區分 dosgolem 輸出覆繪與 remake／EXE 修改，保存手冊驗證與語意隔離，並
  誠實標示沒有玩家版、Release 或已完成中文化聲明。
- Docker 內檢查 14 個 Markdown 連結，其中 8 個相對入口全數存在；標題為單一 H1 與同層
  H2，沒有嵌入原版受保護素材或把工作流水帳塞進 README。

# 2026-09-20：第二十七階段功能選單文字事件清冊

- 第 25 階段倍率決策仍 pending；建立並完整讀回第 27 階段 goal，選擇不依賴倍率的
  content-free 選單 runtime identity 垂直切片。
- 新增 dosgolem `TextRecorder` 與 `buckrogers-text-receipt`：只保存原文 length／SHA-256、
  caller、低位元組色號／座標及 entry／post-call step，不保留原文、不翻譯也不繪圖。
- 第一次重播在 state 載入後立刻排入 Enter，使九筆事件提前 9,971 道；確認內容正確但未採。
  修正為 #100,010,000 排入後重跑，九筆 entry 完全對齊第 4 階段，且全數通過三重 guard。
- 新增 `menu-events.tsv`、schema validator 與 receipt verifier；九筆 hash／length 逐筆對回
  第 8 階段原始 dump，八個 `menu.zh-TW.tsv` key 雙向完整覆蓋，沒有原文全文。
- 專案 32 項正式 Python 測試、真實 JSON receipt、dosgolem 全部正式 packages test／vet
  與 Buck Rogers race detector 通過。
- dosgolem 本機 commit 為 `98f3bec55d633cc2a69099f187848af4d765b7d1`，未推送其遠端；
  本階段沒有選 2×／3× 或建立玩家可見覆繪。

# 2026-09-20：第三十一階段反白 variant 執行期繁中請求

- 建立並完整讀回第 31 階段 goal；在倍率決策仍 pending 時，只閉合不依賴 renderer 的
  selection exact-catalog 垂直切片。
- 正式 `menu-events.tsv` 由 9 筆擴充為 12 個唯一 identity；normal Terran、selected Martian、
  normal Martian 各有獨立 event key，selected Terran 重用既有 identity。
- `race-selection-events.tsv` 加入逐事件 `event_key`，並與 text-safe rectangles、正式 inventory
  進行完整 identity 交叉驗證；舊九事件／九 request verifier 仍只接受精確前九筆。
- 固定 Enter→Down→Up 排程重生兩次，兩份 13-event／13-request 收據逐位元相同，SHA-256
  為 `eb619b596f312aa61a2e5ea335c3c57157a0cd7cb2cf6350e03aaaaf03748b2f`，且零 drop、
  pending、catalog miss。
- 專案 41 項 Python 測試與正式收據 verifier 通過。dosgolem `go test ./...` 首次只被既有
  非正式 workplace 多個 `main` 阻擋；排除 `/workplace/` 後，全部正式 packages test／vet
  與 Buck Rogers race detector 通過。
- dosgolem 本機 commit 為 `79ecc2b9585f02339eef181ecb88b752bee4c2aa`，未推其遠端；本階段
  未載入字型、未繪圖，也未替使用者選定 2×／3×。

# 2026-09-21：第三十二階段功能選單覆繪倍率 A/B prototype

- 建立並完整讀回第 32 階段 goal；載入共同決策、Golden Box CJK UI 與規格閘門契約，
  只製作可丟棄 A/B，不替使用者選倍率或接入 production。
- 新增 dosgolem `buckrogers-overlay-prototype`：直接使用 `xlate.Draw`，嚴格讀正式事件、譯文、
  text-safe rectangles 與 GOLEMFNT，輸出不含原文／譯文全文的幾何 JSON。
- 初版把 `cmd/probe` 已轉好的 8-bit `.pal` 誤當 raw 6-bit DAC；依 `writeShot` 原始碼訂正為
  直接 RGB 後重生所有產物。另一個初版錯誤是把 draw capacity 當完整清除寬度，已改為扣除
  col 1→3 的兩格前導區再驗證。
- steady／Down × 2×／3× 各重生兩次，兩批逐檔相同；四份收據均為七個 visible event、
  零缺字、零矩形重疊、零安全矩形外差異，所有 ink contained。
- 原生圖目視確認：2× 的 16×16 字模填滿格且字距緊密；3× 的同一字模置中 24×24 格、
  相對較小。selected row 在原版固定終點本來就是黑底黑字，prototype 忠實保留，未美化。
- dosgolem spec 013 已 CONFORMED；全部正式 packages test／vet 與相關 race detector 通過。
  本機 commit 為 `09f580877b0d1e34ef00fa44eddefa12898b7e53`，未推其遠端。
- 第 25 階段倍率決策仍 pending；建議維持 2×，等待使用者依實圖確認。

# 2026-09-21：第三十三階段種族選取列閃爍與色盤生命週期

- 建立並完整讀回第 33 階段 goal；倍率決策仍 pending，因此只處理不依賴倍率的 selection
  原版可見性證據。
- 先由既有終點證實 selected Terran／Martian 仍有 index 15 背景與 index 0 glyph pixels，
  排除「文字未畫」；再建立固定 step 的 palette／row region 連續取樣。
- 第一批每 1,000 steps 取樣到逐字重畫過程；為避免短窗口外推，正式收據延長至
  #110,000,000，每 10,000 steps 取 978 點，steady／Down 各重播兩次。
- palette SHA-256 全窗口唯一，色號 0／15 皆為 `(0,0,0)`，contrast 978／978 為 false；
  steady 自 #100,230,000、Down 自 #100,260,000 起，row 3／4 hash 與事件數完全固定。
- 新增嚴格 verifier 與負向測試；44 項 Python 測試通過。dosgolem spec 014 已 CONFORMED，
  全部正式 packages test／vet 與相關 race detector 通過。
- dosgolem 本機 commit 為 `41917c85007efe17154cb92422cba3fe6539ad88`，未推其遠端；未選
  2×／3×，未接 renderer，也未把原版不可見 selection 自行美化。

# 2026-09-21：第三十四階段倍率中立的功能選單覆繪核心

- 上一輪分類為有進展；重新載入復古遊戲、dosgolem 與規格閘門入口，建立並完整讀回第 34
  階段 goal。倍率決策仍 pending，本輪只處理不依賴產品預設倍率的純核心。
- 先建立 dosgolem READY spec 015，再新增 `apps/buckrogers.BuildMenuOverlay`；typed input
  明示事件、譯文、色號、安全矩形、anchor、容量、overflow 與 scale，任一錯誤整批回 nil。
- 診斷命令改用正式核心，移除原有 stamp 建構、ink 計算與 containment 第二套邏輯。
- steady／Down × 2×／3× 使用第 32 階段相同真實輸入重生；四組繁中 PNG、base PNG 與
  JSON 全部逐 byte 等於既有基線，四份 JSON SHA-256 未變。
- dosgolem 排除既有非正式 `workplace/` 後，全部正式 packages test／vet，以及
  `apps/buckrogers`／診斷命令 race detector 通過；spec 015 標為 CONFORMED。
- dosgolem 本機 commit 為 `64b15779edc9d5be35e1acba0f854ba022008511`，未推其遠端；本輪
  未接正常玩家路徑、未建立預設倍率，也未宣稱功能選單已玩家可見中文化。

# 2026-09-21：第三十五階段選定種族後的文字路徑清冊

- 上一輪分類為有進展；重新載入復古遊戲、dosgolem 與規格閘門入口，建立並完整讀回第 35
  階段 goal，選擇不依賴 2×／3× 決策的下一條正常玩家文字路徑。
- 可丟棄 probe 由相同 #99,999,999 state 排入兩次正常 BIOS Enter，證實選定預設種族後
  進入性別選擇畫面，新增提示、兩筆 normal 選項及 selected 第一選項共四筆事件。
- dosgolem spec 016 先達 READY；`buckrogers-text-receipt` 新增 `-receipt-out`，以同一次
  encode 保證 stdout／檔案逐 byte 相同，不改既有 JSON schema。
- 正式排程重播兩次，14-event JSON 逐 byte 相同（SHA-256 `0c24a9fa…7dab`），終點
  framebuffer 亦逐 byte 相同（SHA-256 `dcf947d1…715c`），兩次皆零 pending／drop。
- 新增 `text/post-race-events.tsv` 與嚴格 verifier；專案 47 項測試、dosgolem 全部正式
  packages test／vet 及相關 race detector 通過，spec 016 標為 CONFORMED。
- dosgolem 本機 commit 為 `7009315c5a04981eb1b048e7bba34a0b932fbf6d`，未推其遠端；本輪
  未建立譯文、字型、幾何或 renderer，也未外推性別選單完整 lifecycle。

# 2026-09-21：第三十六階段性別選擇生命週期

- 建立並完整回讀第 36 階段 Goal；範圍只量正常 Down／Up／Escape，不依賴仍 pending 的
  2×／3× 倍率決策。
- 可丟棄 probe 證實 Down 先 normal 重畫男性列再 selected 重畫女性列，Up 反向復原；
  Escape 先取消男性反白，再重建上一層功能選單，並非返回種族選單。
- 正式 Down→Up 與 Escape 路徑各重播兩次；各自 JSON 與 64,000-byte framebuffer 逐 byte
  相同，且通過完整 identity、絕對 step、排程與輸入雜湊驗證。
- 新增 12 筆 content-safe 生命週期清冊、嚴格 verifier 與三項負向測試；專案 50 項 Python
  測試通過。清冊不保存原版英文全文，也不猜譯尚未納入 catalog 的返回選單列。
- dosgolem spec 017 已 CONFORMED，本機 commit 為
  `57daa16fd3ab38ff19b8b1702fecf5b0ca14992d`，未推其遠端；本輪沒有翻譯、繪圖或選倍率。

# 2026-09-21：第三十七階段性別選擇繁中執行期顯示請求

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 能力文件，建立並完整回讀
  第 37 階段 Goal。
- 中文說明書 `SCAN0352_005.jpg` 原圖證實「性別」用語；男性／女性採標準介面譯詞並明示為
  `runtime-interface`，未把沒有命中的 OCR 線索冒充來源。
- 先建立 READY spec 018，再將 menu／gender catalog 共用同一 exact identity loader 與 resolver；
  catalog 合併遇 identity 衝突即拒絕，watcher 與 recorder 沒有複製第二套。
- 正式 Down→Up 路徑兩次皆為 18 events／18 requests／零 miss；Escape 路徑兩次皆為 22 events／
  15 requests／7 misses，返回功能選單後沒有沿用性別 request。兩組收據各自逐 byte 相同。
- 新增正式七 identity inventory、三鍵繁中 catalog、交叉證據 validator 與 request verifier；
  專案 55 項測試及真實收據通過。
- dosgolem 255 份 spec 索引、全部正式 packages test／vet 與相關 race detector 通過；spec 018
  已 CONFORMED，本機 commit `24f0dd55cdce8a929ab513e2a2a1f78afb6fb56b`，未推其遠端。
- 本輪沒有載入字型、清除原文、繪製繁中像素或選定 2×／3×。

# 2026-09-21：第三十八階段確認性別後的職業選擇文字路徑

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 能力文件，建立並完整回讀
  第 38 階段 Goal。
- 從相同固定 state 在 #100,400,000 排第三個正常 Enter；probe 證實接受預設性別後進入
  職業選擇，新增提示、五個 normal 選項及 selected 第一選項共七筆事件。
- 一次性原版 bytes／候選雜湊核對七筆語意；臨時 `/tmp` 腳本已刪除，正式檔案不保存原文。
- 先建立 READY spec 019，再將三鍵路徑正式重播兩次；22-event JSON 與 64,000-byte
  framebuffer 各自逐 byte 相同。
- 新增 `post-gender-events.tsv`、嚴格 verifier 與三項測試；專案 58 項測試及真實收據通過。
- dosgolem spec 索引 256 份、全部正式 packages test／vet 與相關 race detector 通過；
  spec 019 已 CONFORMED，本機 commit `371683b7f5793c7104e839202497c742ba3e13c0`，未推其遠端。
- 本輪未建立職業譯文、text-safe rectangle、renderer 或倍率預設，也未外推其他角色分支。

# 2026-09-21：第三十九階段職業選擇生命週期

- 建立並完整讀回第 39 階段 Goal；只量測正常 Down／Up／Escape，不依賴仍 pending 的倍率決策。
- Down 先 normal 重畫第一職業、再 selected 重畫第二職業；Up 反向復原，終態逐位元等於
  第 38 階段職業畫面。Escape 先取消第一列反白，再重建功能選單，而非返回性別選擇。
- 兩條路徑各重播兩次；JSON 與 framebuffer 各自逐 byte 相同。新增 12 筆 content-safe
  清冊、嚴格 verifier 與三項負向測試；專案 61 項 Python 測試通過。
- dosgolem spec 020 已 CONFORMED；正式套件測試、`go vet` 與相關 race detector 通過，本機
  commit 為 `d8f34f101c719e6939565fe8b6f0d8b531e07ccc`，未推其遠端。本輪沒有翻譯、繪圖、倍率預設
  或原版資料修改。

# 2026-09-21：第四十階段職業選擇繁中執行期顯示請求

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 40
  階段 Goal。
- 由 `SCAN0352_007.jpg` 至 `SCAN0352_009.jpg` 原圖核對太空船駕駛員、戰士、工程師、
  流浪漢與醫生；建立十 identity、六鍵繁中 catalog 及交叉證據 validator。
- 先建立 READY spec 021，再以共用 exact parser 新增 `LoadClassCatalog`，receipt command 加入
  成對 class flags；沿用同一 watcher，未建立模糊比對或第二套流程。
- steady、Down→Up、Escape 各重播兩次，pair 內 JSON 逐 byte 相同。Escape 的七筆返回選單
  identity 與初始 menu 不同，首次 30-request 預期正確失敗後訂正為 23 requests／7 misses。
- 專案 65 項測試與正式 verifier、dosgolem 全部正式套件測試、`go vet` 及相關 race detector
  通過；spec 021 已 CONFORMED，本機 commit 為
  `0025008fbb7d49c42e352f961585a10e82c118e5`，未推其遠端。本輪未載入字型、繪圖或選定 2×／3×。

# 2026-09-21：第四十一階段性別與職業繁中覆繪倍率 A/B

- 上一輪分類為有進展；載入復古逆向與 PC-98 Golden Box UI 技能，建立並完整讀回第 41
  階段 Goal，維持不替使用者選倍率。
- 建立性別七筆、職業十筆 logical text-safe rectangles；validator 由 exact identity 導出位置、
  原文寬度與容量，拒絕改寬、越界、錯 anchor、缺鍵或譯文溢出。
- 正常 BIOS 路徑重生 gender／class steady／Down 四個 framebuffer，各兩次逐 byte 相同；
  擴充既有離線 prototype 的 exact screen variant，不另造 renderer 核心。
- 四狀態 × 2×／3× 各重生兩批，JSON、繁中 PNG、base PNG 逐檔相同；全部零缺字、零重疊、
  零安全矩形外差異且 ink contained。目視確認 2× 緊密滿格、3× 四周留白，最長六字皆完整。
- `catalog_font` 補納正式 `runtime-interface` 來源，性別與職業共用 GOLEMFNT 決定性建置。
- 專案 70 項測試與真實 A/B verifier、dosgolem 全部正式套件測試、`go vet` 及相關 race
  detector 通過；spec 022 已 CONFORMED，本機 commit 為
  `73e610943cb26ed3f0990ecd13bd196d12fe162a`，未推其遠端。本輪未接 runtime Layer 或選定 2×／3×。

# 2026-09-21：第四十二階段確認職業後的角色資料文字路徑

- 重新載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 42 階段 Goal；範圍不依賴
  仍 pending 的 2×／3× 倍率決策。
- 從相同固定 state 排入第四個正常 BIOS Enter，確認進入角色資料／重擲能力值頁；新增 96 筆
  guarded post-call 完成事件，分成靜態標籤、動態角色值、能力值、技能、重畫與重擲提示。
- 正式路徑獨立重播兩次；118-event JSON 與 64,000-byte framebuffer 各自逐 byte 相同。
  固定 snapshot 可重生相同能力值，但本輪沒有宣稱已識別 seed、亂數實作或一般骰序。
- 新增 96 筆 content-safe 清冊、嚴格 verifier 與三項正反例測試；原版二進位沒有直接命中
  runtime 短字串，未猜測其壓縮／解碼機制，正式檔案也不保存英文全文。
- dosgolem spec 023 已 CONFORMED，本機 commit 為
  `1e8060b5a83665da1e1b74a4f02cb391f938e25d`，未推其遠端；本輪沒有翻譯角色資料頁、接
  renderer、修改角色規則或選定輸出倍率。
- 首次 `go test ./...` 誤納被忽略的舊 `workplace/fd2-input-parity-20260907`，因三個獨立 probe
  各自定義 `main` 而失敗；分類為驗證範圍問題後，在同一映像排除 `workplace/` 重跑全部
  正式 packages test／vet 與 Buck Rogers race detector，結果全數通過。

# 2026-09-21：第四十三階段重擲提示輸入與動態欄位重畫生命週期

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門及 dosgolem 契約，建立並完整讀回
  第 43 階段 Goal。
- 從相同固定 state 分別送出 `Y`、`N`、Enter、Space、Escape：`Y` 重擲並回到同一提示，
  `N` 與 Enter 到達相同姓名提示終點，Space／Escape 只重印原提示且畫面不變。
- spec 024 先達 READY；`Y` 與 `N` 各正式重播兩次，149-event／183-event JSON 及各自
  64,000-byte framebuffer 均逐 byte 相同。沒有重擲挑值，也未把 snapshot 結果外推為一般骰序。
- 新增兩份 content-safe 清冊、嚴格 verifier 與三項正反例測試；專案 76 項測試、dosgolem
  全部正式 packages test／vet 與 Buck Rogers race detector 通過，spec 024 升為 CONFORMED。
- 同輪修正 `docs/spec/000-index.md` 遺漏的 Buck Rogers 020–023，並登錄 024；本輪沒有翻譯、
  接 renderer、修改角色規則或選定 2×／3×。dosgolem 本機 commit 為
  `4f899924b35e14fdb7ef23bbb2fcd2620284ae43`，未推其遠端。

# 2026-09-21：第四十四階段角色姓名輸入生命週期

- 上一輪分類為有進展；載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 44
  階段 Goal。
- Probe 證實 `A`、`B` 各產生單字元回顯事件；Backspace 不產生文字事件，但終點像素顯示
  第二字元清除。Escape 只重印提示，空字串 Backspace 無事件也無像素差異。
- spec 025 先達 READY；正式「AB→Backspace」與「A→Enter」分支各重播兩次，185-event／
  226-event JSON 與 framebuffer 各自逐 byte 相同。Enter 後停在職業技能點配置畫面，未操作。
- 新增兩份 content-safe 清冊、嚴格 verifier 與三項正反例測試；專案 79 項測試、dosgolem
  全部正式 packages test／vet 與 Buck Rogers race detector 通過，spec 025 升為 CONFORMED。
- 本輪沒有翻譯玩家姓名、改姓名規則、配置技能、接 renderer 或選定 2×／3×。
- dosgolem 本機 commit 為 `260b3a7f504f7ade6b5487aa591e99911a82bd13`，未推其遠端。

# 2026-09-21：第四十五階段職業技能點配置生命週期

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 45
  階段 Goal。
- Probe 證實 Down 由第一列移到第二列，預設動作 Enter 對第一項技能合法加一點；`+`／`-`
  無事件或像素變化，Left／Right 只改變底部動作選取，未外推其完整語意。
- 尚有 6 點未用時 Escape 顯示離開確認；`N` 後回到與操作前逐 byte 相同的配置畫面。
- spec 026 先達 READY；選取、加點、拒絕離開三條分支各正式重播兩次，234／231／227-event
  JSON 與 framebuffer 各自逐 byte 相同。
- 新增三份 content-safe 清冊、嚴格 verifier 與三項正反例測試；專案 82 項測試、dosgolem
  全部正式 packages test／vet 與 Buck Rogers race detector 通過，spec 026 升為 CONFORMED。
- 本輪沒有翻譯技能配置畫面、改點數或職業規則、接 renderer、測試 `Y` 離開或選定 2×／3×。
  dosgolem 本機 commit 為 `a0bb175d4712b92ce183ac1bd8715aaa6b4bcbec`，未推其遠端。

# 2026-09-21：第四十六階段職業技能動作選單與確認離開

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 46
  階段 Goal。
- Probe 證實預設 Enter 加點後 Right→Enter 以五筆重畫還原同一技能與剩餘點數；終點逐 byte
  等於零點／Right 選取畫面。Left 從預設位置環回離開位置並顯示未用點數確認提示。
- Escape→`Y` 從未用 6 點的確認提示進入技術技能配置畫面，而非停在提示；新畫面包含 62 筆
  content-safe 完成事件。
- spec 027 先達 READY；可逆減點與確認離開兩條分支各正式重播兩次，236／289-event JSON
  與 framebuffer 各自逐 byte 相同。
- 新增兩份清冊、嚴格 verifier 與三項正反例測試；專案 85 項測試、dosgolem 全部正式
  packages test／vet 與 Buck Rogers race detector 通過，spec 027 升為 CONFORMED。
- 本輪沒有翻譯技能畫面、配置技術技能、修改規則、接 renderer 或選定 2×／3×。dosgolem
  本機 commit 為 `dbd262607c90be3a0e92b7173b61bbf140823580`，未推其遠端。

# 2026-09-21：第四十七階段技術技能配置生命週期

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 47
  階段 Goal。
- 由正常職業技能 Escape→`Y` 路徑進入技術技能頁；Down 以八筆事件移到第二列，Enter 合法
  增加第一項一點，Right→Enter 再以五筆事件完整減回。
- Escape→`N` 在一筆確認提示後逐 byte 回到技術技能基線；Escape→`Y` 進入角色身體圖示
  選擇畫面，沒有把確認提示誤當離開完成。
- spec 028 先達 READY；四條分支各正式重播兩次，297／299／290／296-event JSON 與
  framebuffer 各自逐 byte 相同。
- 新增四份 content-safe 清冊、嚴格 verifier 與三項正反例測試；專案 88 項測試、dosgolem
  全部正式 packages test／vet 與 Buck Rogers race detector 通過，spec 028 升為 CONFORMED。
- 本輪沒有翻譯技術技能／身體圖示畫面、修改規則、接 renderer 或選定 2×／3×。dosgolem
  本機 commit 為 `0b66a03808f9d67e2c57ca23e82ad56eb08ac254`，未推其遠端。

# 2026-09-21：第四十八階段角色身體圖示選擇生命週期

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 48
  階段 Goal。
- Probe 證實四方向鍵都改變圖示選取；Enter 與 Escape 顯示逐 byte 相同的圖示確認提示。
- Enter→`N` 重建並回到逐 byte 相同的圖示基線；Enter→`Y` 進入儲存詢問畫面。
- spec 029 先達 READY；移動、拒絕與確認三條分支各正式重播兩次，297／302／298-event
  JSON 與 framebuffer 各自逐 byte 相同。
- 新增三份 content-safe 清冊、嚴格 verifier 與兩項正反例測試；專案 90 項測試、dosgolem
  正式 packages test／vet 與 Buck Rogers race detector 通過，spec 029 升為 CONFORMED。
- `go test ./...` 首次只被既有未納版控 `workplace/fd2-input-parity-20260907` 多個 `main` 衝突
  阻擋；排除 `workplace/` 後以相同容器乾淨重跑通過。本輪沒有翻譯、接 renderer、回答儲存
  詢問或選定 2×／3×。dosgolem 本機 commit 為
  `b385b85103ada0e381063f4869e42b3f006c2f6b`，未推其遠端。

# 2026-09-21：第四十九階段儲存詢問與角色建立完成生命週期

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 49
  階段 Goal。
- Probe 證實儲存詢問不是字母 `Y`／`N` 對話框：直接 `Y` 沒有事件或像素變化，字母 `N`
  接受預設 `NO`；Left 改變反白後 Enter 才是實際 `YES` 路徑。
- `NO` 與 `YES` 都回到逐 byte 相同的功能選單；各自兩份 fresh writable overlay 的寫後
  manifest 全部逐 byte 等於 pristine manifest，沒有把選項文字誤報為磁碟寫入。
- spec 030 先達 READY；字母 `Y`、預設 `NO` 與選取 `YES` 三條分支各正式重播兩次，
  298／305／305-event JSON 與 framebuffer 各自逐 byte 相同。
- 新增兩份 content-safe 清冊、嚴格 verifier 與兩項正反例測試；專案 92 項測試、dosgolem
  正式 packages test／vet 與 Buck Rogers race detector 通過，spec 030 升為 CONFORMED。
- 本輪沒有推導存檔格式、證實記憶體內名冊、翻譯畫面、接 renderer 或選定 2×／3×。
  dosgolem 本機 commit 為 `024399bf9478c014a7e43922b66e6f2f941c836e`，未推其遠端。

# 2026-09-21：第五十階段角色名冊與 scratch-backed 重驗

- 上一輪分類為有進展；重新載入復古遊戲、規格閘門與 dosgolem 契約，建立並完整讀回第 50
  階段 Goal。
- 追查空名冊時發現第四十九階段命令沒有設定 `DOS.Scratch`；舊 manifest 不能證明沒有副作用。
  保留原畫面／事件證據，將 spec 030 標為 SUPERSEDED 並追加勘誤，沒有重寫錯誤形成歷史。
- spec 031 先達 READY；收據命令新增失敗即關閉的 `-scratch` 與可選 `-file-ops` metadata，
  並補空值、有效目錄、一般檔案與不存在路徑的正反例測試。
- scratch-backed FileOps 證實 `NO`／`YES` 都以讀寫模式 shadow `CHARS.DAX`，但沒有 DOS write；
  四份正式 scratch manifest 只含內容等於 pristine 的 `CHARS.DAX`。
- 兩分支進入加入角色功能後都沒有角色列並返回相同功能選單；各自兩次 316-event JSON、
  framebuffer 與 manifest 逐 byte 相同。
- 新增兩份清冊、嚴格 verifier 與兩項正反例測試；專案 94 項測試、dosgolem 正式 packages
  test／vet 與 Buck Rogers race detector 通過，spec 031 升為 CONFORMED。
- 本輪沒有推導角色資料格式、翻譯、接 renderer 或選定 2×／3×。下一切片須完整配置技能點
  後再重驗合法角色保存，不能把本輪未用點數路徑外推成一般角色建立規則。dosgolem 本機
  commit 為 `5b5f9b59318033acdd4d444754bb43abc68863d5`，未推其遠端。
# 2026-09-21：第五十五階段保存、名冊與加入隊伍繁中 catalog

- 由第五十四階段 18-event 正常路徑建立 exact identity 清冊，保留 caller、長度／SHA-256、
  色號與文字格座標。
- 以 SHA-256 反查證實名冊事件為 `A` 加 14 空白、`A` 與 `* A`；四筆含姓名事件全數分類為
  dynamic，禁止進入翻譯 catalog。
- 新增「加入角色：」「載入中……請稍候」及五筆功能選單繁中譯文；既有建立角色 key 維持
  單一權威，沒有複製譯文。
- 新增失敗即關閉 verifier 與三項正反例測試；專案測試由 94 增至 97 項，全數通過；新增
  catalog 可決定性導出 37 個字元。
- 本輪未接 dosgolem production watcher／renderer，也未選定 2×／3×；dosgolem 工作樹沒有
  正式程式變更。
# 2026-09-21：第五十六階段保存、名冊與加入隊伍執行期顯示請求

- spec 034 依 DRAFT→READY→implementation→原版 oracle 驗收升為 CONFORMED；沒有把 RE
  結論直接寫進 production。
- 擴充唯一 menu catalog 至 21 個 identity；roster projection 只含加入提示與載入提示兩個
  identity，並以既有 exact parser／merge／watcher 產生請求。
- 兩次 fresh scratch 完整重播皆為 18 events、14 requests、4 動態姓名 misses、3 writes、
  2,611 FileOps；正規化 JSON SHA-256 均為 `898963d5…b19299`。
- 新舊模式的事件、輸入、FileOps、writes、framebuffer 與保存檔完全相同，證實譯文請求沒有
  污染存檔、名冊或加入語意。
- 新增正式 receipt verifier 與正反例測試；專案 100 項測試及 dosgolem 全部正式 packages
  test／vet、Buck Rogers／receipt race detector 通過。
- 本輪未載字型、清除英文、繪製中文或選定 2×／3×；dosgolem commit 只留本機分支。

# 2026-09-21：第五十七階段明示倍率執行期繁中覆繪

- 將 menu 與 roster 安全矩形、合併 catalog 字型與 runtime request 接入長存 `xlate.Layer`；
  命令必須明示 2× 或 3×，沒有建立預設倍率。
- 首輪重播暴露舊 stamp，spec 誠實退回 DRAFT；後續接入已證實的 `026F:029C` 清除矩形，
  並新增同原點輸出取代契約，沒有依 event key 硬編清單。
- 修正後 2×／3× 各兩次均為 18 events、14 requests、4 dynamic misses、14 actions，終態
  只有 `roster.add_prompt`；同倍率 RGBA 逐 byte 一致。
- raw framebuffer、events、BIOS keys、2,611 FileOps、3 writes 與存檔全部等於無覆繪 baseline；
  RGBA 差異只在終態安全矩形，動態姓名列零差異。spec 035 升為 CONFORMED。

# 2026-09-21：第五十八階段覆繪證據固化與交接

- 建立第 57 階段研究紀錄並掛入證據索引；更新 `CONTEXT.md`、spec 035 與 Goal 狀態，
  保留首輪失敗與退回 DRAFT 的訂正歷史。
- 專案 101 項 Python 測試全數通過；dosgolem 正式套件 `go test`、`go vet` 與
  `xlate`／`apps/buckrogers`／`cmd/buckrogers-text-receipt` race detector 全數通過。
- dosgolem 變更已提交於本機 `buck-rogers-cht-output-overlay` 分支，commit `b2fb855`；
  依權利邊界不推送其遠端。
- 差異檢查通過；本輪 Docker 容器已清理。專案根的 root-owned `original/` 是本輪前已存在
  且已確認為空的 Docker 掛載殘留，已只刪除該空目錄，沒有遺失可恢復資料。

# 2026-09-21：第六十階段手冊覆繪 READY 前置稽核

- 重驗 39 筆題庫、來源對照、22 筆正式事件／譯文與 10 筆序數橋接；來源分布為
  35 confirmed、3 strong-inference、1 unknown。
- 22 筆正式譯文最長 236 字，均可放入 36×17＝612 字單頁；其餘 17 題明定 catalog miss
  並保留原版英文，不猜補、不模糊匹配，也不新增分頁按鍵。
- 訂正 spec 002 的關卡：資料、watcher 與失敗即關閉屬 READY 前置；正常路徑覆繪、錯答
  重抽、containment 與同狀態 A/B 改列實作後 CONFORMED 驗收。
- 專案 101 項 Python 測試及 dosgolem 手冊 adapter／watcher 正式與 race 測試通過；本輪
  未修改 dosgolem。唯一 READY blocker 仍為使用者尚未選定 2×／3×。

# 2026-09-21：第六十一階段手冊單頁容量失敗即關閉驗證

- 核對第 17 階段 prototype 與正式 catalog parser 都以 Python Unicode 字元計數；一個字元
  對應 `xlate.Layout` 的一個邏輯格。
- `manual_catalog.py` 由 36 欄×17 列導出 612 字上限；新增 612 字正例與 613 字負例，超限
  會指出 record、實際字數與上限，不會截斷或默認分頁。
- 正式 22 筆 catalog 通過，完整 Python 回歸由 101 增至 103 項並全數通過。
- 首次聚焦命令因未設定 `PYTHONPATH` 在收集階段失敗；以正確環境重跑 6 項乾淨通過，分類
  為測試命令問題。本輪未修改 dosgolem，正式倍率仍待使用者選定。

# 2026-09-21：第六十二階段手冊原版題目保留版面 prototype

- 原始解析度檢視證實第 17 階段整框 prototype 會遮住頁碼、英文標題與序數；這些是玩家
  完成原版答案驗證所需的操作資訊，不能直接升為 production。
- 建立被忽略的可丟棄重生器與 2×／3× 對照：保留上方原版題目，只在下方
  `[7,312)×[72,184)` 顯示最長 236 字正式譯文；容量為 36×14＝504 字。
- 兩張圖均目視確認金框、原版題目及繁中正文無重疊。Phase 60「只剩倍率」已依新證據訂正；
  新前沿是版面保留方式，建議保留原版題目。
- 依共同決策閘門，production presenter 暫停等待使用者選擇；本輪不修改 dosgolem、不設定
  預設倍率，也不新增中文題目提示或自動答案。

# 2026-09-21：第六十三階段性別與職業 runtime overlay

- dosgolem spec 036 先達 READY，再把 gender／class rect 以完整 catalog 配對旗標接到既有
  `RuntimeMenuOverlay`；孤兒 rect、缺表、部分輸入與非法倍率均失敗即關閉。
- 權威正常三 Enter＋Down 路徑的 baseline、2××2、3××2 均為 24 events／requests；覆繪模式
  另有 24 actions，零 miss／缺字。終態只留職業畫面八 keys，性別與舊 variant 已清除。
- 同倍率 JSON／RGBA 逐 byte 相同；raw framebuffer 五份相同。2×／3× 安全矩形內差異為
  3,288／6,225 px，外部皆 0；原始解析度目視無跨列、裁切或殘字。
- 第一次原版掛載多一層目錄、第二次誤用相近 state，分別在載入與 24-event 閘門失敗；修正
  精確路徑與權威 state 後乾淨重跑，沒有放寬期望。
- 專案回歸增至 105 項並通過；dosgolem 全部正式 test／vet 與相關 race 通過，本機 commit
  `e1d2070` 未推遠端。產品倍率與手冊版面仍未代替使用者決定。

# 2026-09-21：第六十六階段 mode 13h 預設色盤修正

- 由乾淨 `START.EXE` 冷啟動證實遊戲只以 BIOS block write 設 DAC 0–14 與 16–31，沒有
  `3C8/3C9` 直接寫入；index 15 應沿用 mode 13h BIOS 預設白色。
- dosgolem spec 205 依成熟模擬器色表先達 READY；通用實作只載入標準 VGA 前 16 色，
  單元測試另以 sentinel 保證 DAC 16 未被猜補。
- 修正後重建 70M／100M state；100M raw framebuffer 雜湊不變，DAC 15 為白色。角色頁
  base／`Y`、2×／3× 各雙重重播一致，原版 HP 動態值已在 baseline 實際可見。
- 全部 Go packages 測試通過；沒有選定產品倍率或手冊版面，也沒有推送 dosgolem 遠端。
- 專案 Python 回歸 109 項通過；正式 Go 套件 `vet` 與相關 race detector 通過。第一次
  Python 命令誤指不存在的 `tests/`，第一次 `vet ./...` 又掃入既有 `workplace/` 重複
  `main`；修正為實際 `tools/` 與排除研究暫存套件後，以同一容器乾淨重跑。

# 2026-09-21：第六十七階段角色姓名靜態提示執行期請求

- 從第六十六階段固定 state 沿四次 Enter＋`N` 正常路徑重生姓名畫面，確認固定提示 exact
  identity；完整英文只在一次性本機探針核對，未納入正式 catalog。
- 建立一筆繁中「角色姓名：」catalog、嚴格來源驗證器與 dosgolem loader／命令列接線；未設
  text-safe rectangle，不啟用 renderer。
- 正常路徑為 183 events／1 request／182 misses；加送 `A` 為 184／1／183，證實玩家輸入
  echo 維持 miss。兩路各雙重重播，JSON 與 framebuffer 逐位元一致。
- 專案 113 項 Python 測試與 dosgolem 全套 Go 測試、vet、相關 race detector 均通過；
  dosgolem 本機 commit 為 `22f46b4`，未推送其遠端。

# 2026-09-21：第六十八階段角色姓名提示執行期繁中覆繪

- 由 exact event 與玩家回顯清冊證實提示 `[0,128)×[192,200)`、輸入欄 x=136；建立正式
  rectangle catalog 與資料驗證器。
- name-prompt rect 已接入長存 presenter；新增 catalog／rectangle 雙向 event-key coverage，
  缺表與孤兒 rect 都失敗即關閉。
- base／輸入 `A` 的 2×／3× 各雙重重播一致；差異 941／2,038 pixels 全在矩形內，輸入欄
  與矩形外均為 0。原始解析度實圖確認提示完整且 `A` 可見。
- 專案 117 項 Python 測試、dosgolem 全套 Go 測試、vet 與相關 race detector 全數通過。
- dosgolem 實作已提交於本機 branch，commit `6e16fe5`，未推送其遠端。

# 2026-09-21：第六十九階段角色姓名覆繪轉場失效生命週期

- 重讀第四十四階段後先訂正本輪假設：Escape 不取消，只重印姓名提示並留在原畫面。
- 首次 Enter overlay 重播證實 layer 已清空，但收據命令錯把合法 `drew=false` 當失敗；spec 208
  先達 READY，再讓空 active keys／零缺字的終態可正式輸出。
- Enter 226／1／225 的終態 2×／3× RGBA 等於 baseline；Escape 184／2／182 以同 key replace，
  終態只留一份 stamp。兩分支 control 與雙倍率各雙重重播一致，raw framebuffer 不變。
- 專案 119 項 Python 測試、dosgolem 全套 Go 測試、vet 與相關 race detector 全數通過；
  原始解析度實圖確認技能頁無殘字、Escape 留頁且無重複提示。
- dosgolem 實作已提交於本機 branch，commit `8e60489`，未推送其遠端。

# 2026-09-21：第七十階段職業技能配置靜態繁中請求

- 從姓名確認與 Down 正常路徑清冊隔離四個標題、八個一般技能列及兩個 selected identities；
  動態剩餘點數、points、bonus、total 全部維持 miss。
- 技能譯名逐筆鎖定既有角色資料正式 catalog；建立 14-event／12-text-key TSV、來源驗證器與
  dosgolem loader／成對旗標。
- base 雙重重播為 226／14／212，Down 為 234／16／218；catalog 與 control 的原版語意及
  framebuffer 相同。
- 專案 123 項 Python 測試、dosgolem 全套 Go 測試、vet 與相關 race detector 全數通過；
  本階段未建立安全矩形或 renderer。
- dosgolem 實作已提交於本機 branch，commit `c4fb58c`，未推送其遠端。

# 2026-09-21：第七十一階段職業技能配置執行期繁中覆繪

- 以 14 個 exact identities 的原文起點與長度建立安全矩形；動態數值欄從 x=184 開始。
- dosgolem 新增 `-career-skill-rects`，與 career-skill catalog 成對失敗即關閉，並併入
  長存 presenter。
- base／Down × 2×／3× 各雙重重播；原版 framebuffer 不變，矩形外與動態數值欄
  差異均為 0。四張原始解析度圖已目視通過。
- 專案 Python 回歸 127 項通過；dosgolem 正式套件 test／vet 通過。`go test ./...`
  會掃入既有 `workplace/fd2-input-parity-20260907` 三個獨立 main，改以排除研究暫存套件
  的同容器命令乾淨重跑。
- 全套 race 的未改動 `internal/cpu` 首次在 2 GiB 被系統終止，改用 8 GiB 後仍先觸及
  套件 10 分鐘逾時，期間沒有 race 報告或斷言失敗。本輪改動的 `apps/buckrogers` 與
  `cmd/buckrogers-text-receipt` 已獨立 race 通過；不將未完成的全 CPU race 冒稱通過。
- 本階段不選定產品預設倍率，不改手冊版面。
- dosgolem 實作已提交於本機 branch，commit `91407a4`，未推送其遠端。

# 2026-09-21：第七十二階段技術技能配置靜態繁中請求

- 從職業技能 Escape→`Y` 正常路徑隔離技術頁的固定標題、13 個技能列與前兩列
  selected variants；所有技能譯名都以中文手冊原圖校訂。
- 首次合併因兩個標題和 career catalog 具有相同 exact identity 而失敗即關閉。spec 211
  退回 DRAFT，修正為共享既有 identity，再審查為 READY；technical catalog 從 19 筆修正為
  17 筆不重複 identities，命令列也強制同時提供 career catalog。
- base control／catalog 各雙重重播為 289 events／16→32 requests／273→257 misses；Down 為
  297／16→34／281→263。原版語意與 framebuffer 不變。
- 專案 131 項 Python 測試、dosgolem 正式套件 test／vet 與本輪改動套件 race 全數通過。
- 本階段不建立安全矩形、不繪製繁中像素，不選定產品預設倍率或手冊版面。
<!-- phase-72-dosgolem-commit -->
- dosgolem 本機提交：`790a41cbf03d056caedf87f06698f50cae90a8c1`（分支 `buck-rogers-cht-output-overlay`，未推送）。

## 2026-09-21 — 第七十三階段：技術技能配置雙倍率覆繪

- 建立 17 筆 technical exact rectangles，兩個共享標題沿用 career rectangles；加入 CLI 旗標與
  缺少依賴時的失敗即關閉檢查。
- 首輪 PNG 揭露 selected 英文殘字，立即將 spec 212 退回 DRAFT；查明停止點早於下一垂直回掃，
  延後 100,000 steps 後 request 數不變且繁中正確，重新審查 READY 並完成 CONFORMED。
- base／Down × 2×／3× 各雙重重播，原版 framebuffer、語意 projection、矩形外與動態欄均無差異；
  正式圖已人工檢查。
- 專案 136 項 Python 測試、dosgolem 全正式套件 test、`go vet` 與相關 race detector 通過。
- dosgolem 本機提交：`2d8561c8a87e6868c8e0d647fbcf69e6c18169c0`（分支
  `buck-rogers-cht-output-overlay`，未推送）。

## 2026-09-21 — 第七十四階段：技能配置底部操作列輸出路徑

- 用 dosgolem 正常輸入重生職業 base／Subtract／Done 焦點及技術 base／Subtract／
  Prev／Next／Done 焦點；八條收據均來自同一固定 savestate。
- IDA 9.4 證實 `0763:026B` 是低階字元輸入，`0763:1809` 是 8×8 glyph
  renderer；原來的 `0763:0424` 高階 dispatcher 不在此路徑。
- 建立 8-row content-safe 清冊、驗證器與負向測試；disabled variant 保持
  `unknown`，未翻譯、未實作 overlay。
- 收據 SHA-256：career base `0b3b9cf1…e429`、Subtract `624aa186…daf`、Done
  `850d18e6…f137`；technical base `bd82bf11…7f2`、Subtract `ede95606…cdd`、Prev
  `c147f860…371a`、Next `4ba2b122…f36`、Done `9ca6aba1…d6e`。完整雜湊保存於
  `docs/re/phase-74-skill-action-bar-output-path-inventory.md` 所引用的本機收據。
- dosgolem 新增 spec 213（DRAFT），只規劃 guarded glyph-event watcher；本階段沒有
  production 程式碼變更，也未選定 2×／3× 或手冊版面。
- dosgolem 本機提交：`7d8ca0b`（分支 `buck-rogers-cht-output-overlay`，未推送）。

## 2026-09-21 — 第七十五階段：技能配置底部操作列執行期事件

- spec 213 先補齊輸入雜湊、typed 狀態、exact anchor、失效、失敗模式、垂直鏈、
  驗收與權利邊界後升 READY，才實作 `ActionBarWatcher`。
- runtime 初次證據依序曝露局部 clear、row 24 重畫、mode=1 及 technical 共享
  career keys 四個契約細節。每次都先回 DRAFT 修 spec／負向測試，再用同一路徑
  重跑；雜湊、caller、色彩與座標未放寬。
- career base／Subtract／Done 與 technical base／Subtract／Prev／Next／Done
  的事件數為 3／6／9／8／13／18／23／28。每路 watcher A/B JSON 逐 byte
  一致，0 miss、0 drop。
- 八路 watcher A/B/control framebuffer 均逐 byte 一致；去除 action metadata 後，watcher 與
  control 的其餘 JSON 也一致。收據 verifier 為 `tools/skill_action_bar_runtime_receipt.py`。
- 專案 142 項 Python 回歸、dosgolem 全部正式套件 test／vet 及相關 race detector
  通過；spec 213 已 CONFORMED。本階段沒有譯文、request 或 overlay。
- dosgolem 本機提交：`356848c`（分支 `buck-rogers-cht-output-overlay`，未推送）。

## 2026-09-21 — 第七十六階段：技能操作列繁中顯示請求

- 建立 `skill-action-bar.zh-TW.tsv`，五個譯文採 `runtime-interface` 來源；事件與譯文
  雙向覆蓋，career／technical 及 normal／focus 共用文字鍵。
- dosgolem 新增 16-identity exact resolver 與 watcher request 佇列；純 event 模式維持相容。
- 初次 runtime 因漏掛 savestate 所需 `/orig/GAME.OVR` 失敗且未產生收據；確認來源後以
  唯讀 `/orig` 重跑，沒有放寬產品契約。
- 八路 event／request 數為 3／6／9／8／13／18／23／28；A/B、control 語意與 framebuffer
  全數一致，0 miss／drop。專案 144 項 Python 與 dosgolem 全套 test／vet／race 通過。
- spec 214 已 CONFORMED；本階段沒有操作列覆繪，也未決定產品倍率或手冊版面。
- dosgolem 本機提交：`6d17fd3`（分支 `buck-rogers-cht-output-overlay`，未推送）。

## 2026-09-21 — 第七十七階段前置：操作列幾何與配色 prototype

- 依本輪 goal 先量測 Phase 71／73 真實 framebuffer 與既有 16×16 GOLEMFNT renderer。
- 證實 exact `y=192..200` 在 2×／3× 均能容納字模；16 logical-pixel 候選會蓋住底框，排除。
- 以正式譯文建立首字白／次字綠與全綠兩種 career／technical、2×／3× 可丟棄圖；technical
  2× 的 `y<192` 像素逐 byte 等於既有基底。
- 原版 normal 混色沒有自然的繁中首字母對應，依共同決策閘門暫停 production 配色；spec 215
  保持 DRAFT。dosgolem 本機提交 `952c596`，未推遠端。

## 2026-09-21 — 第七十八階段：配色中立操作列覆繪核心

- 建立 16 筆 normal／focus exact rectangles 與 Python verifier；同 action variant 可共用幾何，
  同畫面跨 action 重疊、缺漏、孤兒、容量及 geometry drift 均失敗即關閉。
- dosgolem 建立不含 normal 預設值的 multi-color stamp builder；caller 必須逐 rune 明示已證實的
  palette 10／15，focus 固定 palette 15 底／0 字。
- `[15,10]` 與 `[10,10]` 兩候選均在 2×／3× 通過核心 containment，不構成產品選擇；CLI 未接線。
- 專案 149 項 Python、dosgolem 全套 test／vet／Buck Rogers race 通過。dosgolem 本機提交
  `236cb3b`，未推遠端；spec 215 保持 DRAFT。

## 2026-09-21 — 第七十九階段：配色中立 runtime 生命週期

- `RuntimeActionBarOverlay` 強制 constructor 注入 normal 配色；`Frame` 在通用指紋／錨點初始化後
  重套 caller palette，修正全綠候選會被原版首字白覆寫的風險。
- normal／focus 依 exact rectangle 原子取代；partial clear 造成 group 不完整時整組移除。
- career／technical anchor 切換、unrelated event 清除及 technical shared career keys 保留均測試。
- 完整 `go test ./...` 通過；全域 vet 被既有未版控 workplace 三個 probe `main` 衝突攔下，改以
  正式 package 清單重跑 vet，另跑 Buck Rogers race，均通過，未刪改其他研究資料。
- dosgolem 本機提交 `6d230a1`，未推遠端；spec 215 保持 DRAFT，正式 CLI 等待配色決策。

## 2026-09-21 — 第八十階段：快捷字母保留與混合寬度版面

- 接受使用者修正：排除全綠及首個中文字白色，改為括號內 A／S／P／N／D 保持白色，
  括號與繁中標籤使用原版 palette 10；focus 仍為黑字白底。
- 以 Phase 71／73 真實 framebuffer 與正式 Unifont 來源重生 2×／3× prototype；五字顯示
  採 ASCII 4 px、CJK 8 px 前進，總寬 28 px。Add 擴用 `[24,32)` 空白後沒有重疊或框線侵入。
- 正式 catalog、矩形驗證器與 dosgolem renderer 已改為失敗即關閉的混合寬度／固定配色契約；
  原子 group lifecycle 保持不變。
- 可見首字母身分已證實，但 A／S／P／N／D 直接鍵盤作用尚未實測，文件只稱助記字母。
- spec 215 升 READY；完整正常玩家路徑 runtime overlay 收據留待後續 CONFORMED 階段。
- 專案 149 項 Python 測試通過；dosgolem 正式 packages 的 test／vet 及 Buck Rogers race 通過。
  `go test ./...` 仍會掃到既有未版控 `workplace/fd2-input-parity-20260907` 三個 probe 的重複
  `main`，未誤改其他研究資料。
- dosgolem 本機提交：`8bfd5b4`（分支 `buck-rogers-cht-output-overlay`，未推送）。

## 2026-09-21 — 第八十一階段前置：手冊版面與倍率方向確認

- 使用者採保留原版題目的方案 A；production 正文收斂為 36×14＝504 字，排除整框替換。
- 使用者不選單一固定倍率，要求遊戲執行中可在 2×／3× 間調整；Phase 25／59 的固定倍率
  門檻因此完成並由第八十一階段 runtime switch 契約接手。
- 查證 dosgolem 現有玩家路徑只有命令列明示倍率，未發現 host-only 快捷鍵／設定選單；
  正式綁鍵前須由使用者決定入口，不得借用會送入 DOS 的 BIOS key queue。
- 使用者選擇 dosgolem 外層設定面板，而非直接快捷鍵或單鍵循環；面板開啟鍵及設定生命週期
  仍在共同決策前沿。

## 2026-09-21 — 第八十二階段：host 設定面板控制列 prototype

- 使用者確認由視窗頂端 host-only 滑鼠按鈕開啟面板，排除 `F10`／`Ctrl+F10`。
- 以 Phase 62 真實手冊 framebuffer 產生 2×／3×、各兩種 active selection 的四張圖；面板
  位於控制列下方並將畫布下推，沒有覆蓋原版／繁中像素。複製後遊戲畫布 SHA-256 與來源一致。
- 2× 視窗為 640×480、畫布自 y=80；3× 為 960×720、畫布自 y=120。所有 host hit rectangles
  在 DOS 座標轉換／BIOS／IRQ 前消費。
- dosgolem 目前無現成互動視窗 frontend；prototype 僅定義通用 host layout／input contract。
  下一個共同決策是 option click 的立即套用或二次確認語意。

## 2026-09-21 — 第八十三階段：手冊保留原題的 504 字容量契約

- 將現行手冊正文正式固定為下方 `[7,312)×[72,184)` 的 36×14 格、504 字容量；原版上方
  頁碼、英文標題與序數保持不動。
- 新增 layout TSV 與 verifier；schema、幾何、containment、504／505 邊界、22 筆 catalog 全部
  納入失敗即關閉驗證，最大正式段落為 236 字。
- 將 spec 002 與文字目錄收斂到 504 字；612 字只保留歷史 prototype／收據脈絡。未接
  dosgolem presenter，未改寫原版輸入或手冊答案判定。

## 2026-09-21 — 第八十四階段：dosgolem host 前端能力盤點

- 固定並檢閱 dosgolem 本機 `8bfd5b4`；README、command inventory、source search 與 Go 測試
  共同證實現況是無頭觀測器，沒有可直接接用的視窗或 host pointer event loop。
- 既有 xlate／Buck Rogers overlay 能從 raw indexed framebuffer、palette 與 active stamps
  生成 2×／3× RGBA，但 runtime scale 是 constructor-only；DOS 模擬滑鼠維持對拍輸入，不混入 host UI。
- 新增 spec 004 DRAFT，將通用 presenter、host hit-test、輸入隔離與重繪責任獨立於
  `apps/buckrogers/`；option click 套用語意與 backend 選擇保持未定，沒有實作 dosgolem。

## 2026-09-21 — 第八十五階段：手冊繁中 presenter 整合就緒稽核

- 使用者確認倍率操作採 C：option 只選取，Apply 才提交 2×／3×；面板收合與持久化沒有自行推定。
- 以目前 `8bfd5b4e5802f65d428d3fb439196b3c571c002b` 重跑正常玩家手冊 state，固定 request 與
  第 24 階段一致，未注入按鍵、未輸出答案或原版全文。
- 從正式 22 筆手冊譯文重生 691 碼點字型需求清單；它只是被忽略的研究輸出，尚非正式字型。
- 建立 spec 005 DRAFT：xlate 可提供只讀 RGBA／逐格失效，但需新增手冊專屬的 14 行 builder 與
  帶 generation 的 begin／clear／request presentation lifecycle；既有選單 presenter 不可直接套用。
- 沒有變更 dosgolem production code、DOS 輸入、原版答案驗證、存檔或遊戲資料。

## 2026-09-21 — 第八十六階段：手冊 presentation lifecycle 接線

- dosgolem 新增 answer-free `ManualPresentationEvent` value queue；精確 begin、active-context clear
  與 exact catalog-hit request 都帶 generation，queue／request 回傳值不可回寫 watcher。
- `buckrogers-receipt` 只投影 lifecycle 的 step、kind、generation、event／text key 與 rune count，
  沒有輸出 translation 全文、英文原文或答案。
- 正常玩家重播仍止於 #266,557,247；既有 request 不變，新增 begin→pending clear→request 三筆
  generation 1 metadata。沒有 injected input、machine write、中文 renderer 或原版素材輸出。
- spec 216 已 CONFORM；Go unit、vet 與 race 驗證通過。dosgolem 本機提交為
  `47397ebd18e63a0daa4cb54bd593c5fbfd549ada`，分支未推送。

## 2026-09-21 — 第八十七階段：手冊多行 presenter 純核心

- dosgolem 新增 `RuntimeManualOverlay` 與嚴格 `manual-overlay-layout.tsv` loader；它消費既有
  answer-free lifecycle value，建立 14 個完整 clear-band 背景 stamp 與 14 個 36-cell 文字 stamp，
  不寫 DOS VRAM、不讀寫輸入、答案或存檔。
- constructor 預先拒絕錯誤 layout／catalog／16×16 字型／glyph／2×或3×以外倍率；lifecycle 拒絕
  stale generation、catalog miss、部分 request 與非法狀態。2×／3× synthetic RGBA 測試確認清除
  矩形外零差異、504 rune row-major 與 defensive-copy。
- spec 217 已 CONFORM（僅純核心）；Docker 的 Go vet 與 race 測試均通過。dosgolem 本機提交為
  `21c9295c90fac44b5852fd5934a6d027342cde24`，分支未推送。正式字型、command 接線與正常玩家 A/B
  仍未完成。

## 2026-09-21 — 第八十八階段：手冊正式 GOLEMFNT 子集來源稽核

- 從正式手冊 catalog 重生 691 glyph 清單（SHA-256
  `dc656f0729ac3c02abe691d463e62454d1505fbe4d8122aa6056822332a6667f`），放在被忽略的
  `workplace/phase88/`；缺少候選輸入時 builder 以 nonzero 結束且不產生輸出。
- 唯讀盤點證實 workspace 沒有原始字型與完整授權文字；十份歷史 GOLEMFNT 最大 81 glyph，
  既不能覆蓋 691 也不能反推來源／授權。沒有下載、採用或散布字型。
- dosgolem spec 218 維持 DRAFT，明定 input manifest 與可散布停止線；本機提交
  `3fc37fe2908c7247447e34dfe18ae3b44855b534` 未推送。等待使用者提供或明確授權取得候選後，
  才能進入 READY。

## 2026-09-21 — 第八十九階段：host 倍率預選與 Apply 純核心

- 依使用者的 C 建立通用 `host.ScaleController`：Select 只變 `selectedScale`，Apply 才原子提交
  `activeScale`，重複 Apply／回選原值皆無額外變更；無效 scale、nil 與回傳值污染皆失敗即關閉。
- Docker 的 `go test`、`go vet`、race 與直接 import 檢查通過；core 只依賴 `fmt`，沒有 DOS、
  machine、oracle、adapter 或 command 依賴，也沒有畫面、鍵盤、滑鼠、VRAM、存檔副作用。
- spec 219 已 CONFORM（純核心）；dosgolem 本機提交為
  `9240c3b19ad5eaba7a44a2b9b4f4420fe1653a0a`，未推送。backend、hit event、面板狀態、持久化、
  實際 runtime 重繪及玩家路徑驗收仍為後續 DRAFT。

## 2026-09-21 — 第九十階段：手冊 presentation queue consumer 純核心

- dosgolem 新增 `ManualPresentationConsumer`，只接受 watcher 的 append-only event value snapshot；
  先驗證完整已消費 prefix，再以 presenter `Apply` 成功作為 cursor 的唯一提交點。完整重播為 zero-op，
  歷史 mutation／snapshot shrink 均在 presenter 前拒絕；中段失敗僅保留成功 prefix。
- Docker 的 `go test ./apps/buckrogers`、`go vet ./apps/buckrogers` 與 race 檢查通過。合成測試涵蓋
  begin→clear→request、replay、未知及無 begin request、partial failure、defensive-copy 與 nil；
  consumer 唯一直接 import 是 `fmt`，沒有 machine、oracle、input、command 或 renderer 依賴。
- spec 220 已 CONFORM（純核心）；dosgolem 本機提交為
  `b0721c605619a9e689c934994408e009e9231ff9`，未推送。沒有接 watcher callback、遊戲 loop、正式字型、
  frame／draw 或 normal-player A/B；手冊 runtime 中文顯示仍未完成。

## 2026-09-21 — 第九十一階段：手冊 watcher snapshot bridge 純核心

- dosgolem 新增 `ManualPresentationBridge`，只取得 `Watcher.PresentationEvents()` defensive value
  snapshot 並原樣交給 consumer；不保存第二份 cursor、不讀 `Observations()`、不重試／重排 event，且不會
  吞掉 consumer 的 history drift 或 partial-failure error。
- Docker 的 `go test ./apps/buckrogers`、`go vet ./apps/buckrogers` 與 race 檢查通過。合成測試涵蓋
  begin→clear→request 分批 append、完整 replay zero-op、watcher history drift、partial failure 重試與
  nil；bridge 唯一直接 import 是 `fmt`，沒有 machine、oracle、input、command、renderer 或 font 依賴。
- spec 221 已 CONFORM（純核心）；dosgolem 本機提交為
  `bac3f3fafc3cc40b78eee66fdb1f756f21509e53`，未推送。同時修正 spec 220 頂端狀態。沒有 command、
  遊戲 loop、正式字型、frame／draw 或 normal-player A/B；手冊 runtime 中文顯示仍未完成。

## 2026-09-21 — 第九十二階段：正式字型候選 manifest 驗證補強

- `tools/catalog_font.py` 新增 `validate-candidate`：strict JSON manifest 必須與實際 source／license
  basename、SHA-256、非空 UTF-8 授權文字、既有 Unifont parser glyph coverage 與 catalog character-list
  SHA 一致；未知欄、policy 漂移、格式／conversion 不符、缺輸入、空 license 與缺 glyph 都失敗即關閉。
- 成功只以 JSON 輸出 filename、SHA、format／version、scope／distribution 與 found／required count，不
  回顯 notice、license 或 glyph bytes，且命令沒有字型 output path。158 項 Python 測試、正式 691 glyph
  synthetic coverage、504 字版面與 catalog lint 都通過；沒有 candidate 或 GOLEMFNT 產物。
- project spec 006 已 CONFORM（候選審查工具）；dosgolem 本機提交
  `a4a87aad48607ea6ff6e4646de1292f5caaeade9` 僅回填 spec 218 邊界，未推送。字型來源／完整授權文字、
  採用、build、runtime 與 normal-player A/B 仍未完成。

## 2026-09-22 — 第九十三階段：倚天字型候選輸入盤點

- 依使用者選定的本機倚天來源，在 Docker 唯讀盤點 `ET353S/FILES/STDFONT.15`、`SPCFONT.15`、
  `SPCFSUPP.15` 與 `ASCFONT.15`；只保存檔名、大小與 SHA-256，沒有複製字模、媒體或完整 README。
- 以正式手冊 691 code points 重生 coverage：44 ASCII、12 symbol、634 common CJK、1 secondary CJK，
  缺字為零；`U+0020` 是唯一預期空白字模。`一`／`中`／`猴` 的 entry 0／66／2,690 結構錨點沒有位移。
- 新增 spec 007 DRAFT 與 RE 收據，明定候選仍缺完整授權告知、既有 Unifont validator 不可冒充支援、
  以及 16×15／8×15→16×16 對齊必須先做 prototype 與使用者決定。

## 2026-09-22 — 第九十四階段：倚天字型本機建置與對齊 prototype

- 使用者明確確認先前購買的倚天字型可直接放入本機遊戲；此決定解鎖本機轉換／嵌入，不擴張為 Git、
  GitHub、Release 或公開封包的再散布許可。
- Docker 由 spec 007 固定雜湊的 15 點來源重生 bottom-pad、top-pad 兩份 16×16／691 glyph
  `GOLEMFNT`，全量回讀通過；產物、重生器、畫面與 manifest 都僅在忽略的 `workplace/phase94/`。
- 以固定 Deimos Prison state 與 `RuntimeManualOverlay` 建立兩案的 2×／3×預覽；四張均零缺字且 clear
  rectangle 外零像素差。正文在原版畫面中全黑，故 preview 僅在 private `Frame` sampling 使用原題目區
  palette index 10；DOS VRAM、輸入、答案、原版 EXE、runtime loop 與 dosgolem production code 均未改。
- 對齊的使用者選擇仍待回覆；production ETen parser、正式前景色來源、runtime 接線與 normal-player A/B
  繼續維持 DRAFT，不能宣稱手冊中文已完成。

## 2026-09-22 — 第九十四階段後續：倚天字型對齊決定

- 使用者選定 B：`top-pad`，第 16 個空白列置頂；排除 `bottom-pad`。這固定 16×15 CJK 與 8×15 ASCII
  source rows 至 runtime 16×16 row 1..15，row 0 為零；水平 ASCII 仍在 x=4..11。
- 依賴已拆入 GitHub #12（正式 ETen parser／本機建置）、#13（原版前景色來源）與 #14（手冊 presenter
  正常玩家 runtime 接線）。第九十四階段的 private palette-index-10 取樣仍只屬對齊預覽，不能升格為正式策略。

## 2026-09-22 — 第九十六階段：由調查轉入中文化實作

- 依使用者要求指揮兩位 Terra，交付倚天正式建置器與手冊執行期接線；主代理加入獨立 RGBA 與完整狀態整合驗收。
- 首題 2×／3× 中文實際顯示、正文外差異為零；錯答換題未命中 catalog 時清除舊段落，完整原版狀態不變。
- 修正存態驗證方法：gob map 及 handle 序列順序可不同，改以完整既有 schema 解碼正規化比較；未變更原版存態格式。
- Python 172 項及相關 Go 測試通過，手冊子代理完成 race／vet；原始資料、字型與圖片均留 workplace。
- 詳細成果、重跑入口與限制見 [第九十六階段收據](docs/re/phase-96-eten-manual-runtime.md)。#14 尚有返回／存讀檔驗收，保持開啟。

## 2026-09-22 — 第九十七階段：手冊中文字密度與第二題

- 使用者確認 2× 可維持，3× 中文字應更大、更緊；手冊 presenter 的 3× 在記憶體由 16×16 取樣成 22×22，2× 輸出雜湊保持不變。
- 低階模型新增 `Technical Skills` 題與譯文；主代理對中文手冊第 87 頁原圖審核，刪除誤入的其他技能分類並重建 760 glyph 的正式本機倚天字庫。
- 首題、錯答後第二題的 2×／3× 正文外差異均為零，原版完整持久化狀態與控制組相等；restore 穩定點亦無舊中文殘影。
- 通用 watcher 在中途步數會正確拒絕未完成呼叫的收據，已改用已證實返回點 `266585072` 驗收。遊戲內返回／存讀檔仍在 #14。
- 詳見 [第九十七階段收據](docs/re/phase-97-manual-cjk-density.md)；一切原版、字型與圖像只保留在 `workplace/`。
- dosgolem 變更已提交本機分支 `4b58dc7`；專案 main 的翻譯、字型工具與收據將推送 private GitHub，交接時核對 clean worktree 與無殘留容器。
- 同一倚天字庫另沿正常角色建立路徑整合七組已證實 UI catalog；2×／3× 各 17 個終態中文 key，矩形外均 0 像素差，完整原版狀態與控制組相等。重跑入口 `tools/ui_runtime_smoke.py`。
- 低階模型依原圖補入 8 筆正式手冊題，現為 31／39；主代理訂正流浪漢與水星兩處字句。10 份 catalog 字庫重建為 880 glyph（僅本機），173 項 Python 測試通過；新題目前僅完成資料／版面驗證，尚非逐題玩家路徑驗收。
- 操作列進入正常技術技能頁：白色快捷字母不變、3× 中文擴至 22×22 並縮緊字距；2× RGBA 與前版逐位元相同。雙倍率同狀態、矩形外零像素差，其他焦點及離頁返回另待驗收。詳見 [第九十九階段收據](docs/re/phase-99-action-bar-3x-density.md)。
- 2026-09-22 依使用者「先完成翻譯」將手冊題目段落補至 39／39：新增八題一對一事件與原創繁中意譯，第 3／39 題以原版英文手冊直譯，另存 URL／章節／本機快照 SHA；第 11／18 題訂正舊 OCR 漏讀標題，第 7 題採原版英文 seven 而非中文掃描誤印的十七。每段 ≤504 字，39 題來源、事件與版面驗證通過；十份 catalog 倚天字庫重建為 959 glyph，僅在被忽略的 `workplace/`。逐題玩家路徑抽樣留待後續，詳見 [第一百階段收據](docs/re/phase-100-manual-39-translation.md)。
- 2026-09-22 續推中文化：新增角色身體圖示畫面七筆 exact 譯文與安全矩形；原圖 `READY ACTION` 核對後譯為「準備動作」。11 份正式 catalog 倚天字庫重建為 961 字模，只留本機 `workplace/phase101-font/`；完整 Python 測試 181 項通過。此切片尚未接 runtime，見[第一百零一階段](docs/re/phase-101-body-icon-text-catalog.md)。
- 同日手冊與快捷列稽核以第一百階段 959 字模重播首題，雙倍率正文外零差異；新 961 字模另由正式載入器回讀。稽核邊界見[第一百零二階段](docs/re/phase-102-overlay-audit.md)。使用者確認第一個可玩前端先支援 Linux、架構保留其他平台；新建 GitHub Issue #16，spec 004 仍為 DRAFT，未替使用者決定後端、焦點或設定持久化。
- 手冊正常路徑的連續錯答實際命中第三題 `Acidic Victory`；最新 961 字模下 2×／3× 中文均可見、缺字與正文外差異為零，完整原版狀態等於控制組。純手冊收據不再因未啟用的操作列 watcher 中止；啟用時維持失敗即關閉，請求型 watcher 優先序已修正並由本機 dosgolem commit `640f918` 測試。#3／#39 未自然命中，不能外推全部題目；見[第一百零三階段](docs/re/phase-103-manual-third-question-runtime.md)。
- 以本機手冊合法查答後，2×／3× 正常返回的手冊覆繪均完全失效、完整 machine／DOS 狀態與控制組相等；Escape 則被原版當錯答重抽，不能當返回。答案與可還原按鍵僅存忽略的 `workplace/`；存讀檔仍無可銜接的手冊後 checkpoint，見[第一百零四階段](docs/re/phase-104-manual-success-return.md)。
- 前端選擇由使用者確認 Go／Ebitengine，排除 SDL3；既有 2.9.9 Docker image 的 Linux／Xvfb 可丟棄原型可開 320×200 logical、3× 視窗，但尚非遊戲前端。焦點與設定面板行為仍待決，spec 004 維持 DRAFT。

## 2026-09-22 — 第一百一十六至一百一十七階段：真實遊戲前端原型與首屏覆繪對拍

- 使用者定案 Linux 首版以 Ebitengine 顯示，啟動預設 2×、倍率只在本次遊戲期間有效；設定面板開啟時停送遊戲鍵盤，Apply 後收合，未 Apply 關閉則取消暫選，再開回到目前倍率。真實原版 state 已於 Docker／Xvfb 的 Ebitengine 原型顯示並由明示 BIOS 鍵盤橋推進；原型仍以空 active layer 呈現，不是可玩中文版。見[第一百一十六階段](docs/re/phase-116-game-loaded-ebiten-prototype.md)。
- dosgolem 本機分支接上第一頁五行 READY 劇情的 guarded return-edge watcher、覆繪及故事區失效。從合法手冊成功返回 state 以相同私有輸入重播，2×／3× 各命中五筆、零缺字、安全矩形外零差異，原版 indexed framebuffer／palette 相同；轉頁清除、完整開機玩家路徑與存讀檔仍待驗，spec010 保持 READY。見[第一百一十七階段](docs/re/phase-117-story-opening-runtime-ab.md)。
- 既有畫面證實第四頁另有六行劇情；早先將該頁判成僅命令列的說法已追加勘誤。六筆繁中僅為 visual-transcription DRAFT，尚未找回首次繪製前 state 或 glyph caller，不能接 runtime。見[第四頁勘誤](docs/re/phase-113-story-page4-corrigendum.md)與[state 停止線](docs/re/phase-115-page4-state-recovery-stop.md)。

## 2026-09-22 — 第一百一十九階段：首屏 Enter 轉場的實際失效邊

- 從合法手冊成功排程延伸 Enter，2×／3× 都在 `281020548`、`0CF4:1B3A`、`A000:AA08`／`CX=304` 的 row 136 video span 執行前清除首屏五行。第二頁終態覆繪逐 byte 等於 baseline，原版記憶體／indexed 畫面／palette 與無覆繪控制組一致。
- 舊研究在 `281020572`、row 137 量到的是第一筆可見像素差異，並非第一筆寫入；追加勘誤並修正 READY spec 010 的失效邊，保留舊收據與錯誤形成原因。存讀檔／restore 與完整開機玩家路徑仍未驗，spec010 不升 CONFORMED。見[第一百一十九階段收據](docs/re/phase-119-story-opening-enter-lifecycle.md)。

## 2026-09-22 — 第一百二十階段：真實 Ebitengine 畫面接上作用中繁中劇情層

- 本機 dosgolem 以穩定的 story active layer pointer 接到 host 只讀投影；真實原版 state 與合法輸入產生的五行 READY 繁中已在 Docker／Xvfb Ebitengine 視窗顯示。初版將 2× 16×16 字模直接放大至 3×，視覺檢查發現中文字距過大；隨後改在 host Apply 時重建 3× 22×22 CJK 輸出 presenter，2×、Cancel 後 2×、Apply 後 3× 的 RGBA 均逐像素等於正式 CLI，原版 indexed 不變。
- 這是受控 host event 的 ignored prototype，不是正式可玩前端；pointer hit、實體鍵盤映射、完整玩家路徑、其他 overlay 的倍率切換與存讀檔仍待驗。見[第一百二十階段收據](docs/re/phase-120-game-active-story-layer-prototype.md)。

## 2026-09-22 — 第一百二十一至一百二十二階段：手冊恢復邊界與第五頁敘事

- 手冊成功返回後的 dosgolem savestate 無鍵恢復，2×／3× 均無舊中文覆繪復活、原版狀態與控制組相等；它不是原版遊戲內保存／讀檔。手冊後合法保存入口尚未證實，故不猜按鍵。保留 spec002 歷史 22／691 基準並追加現況 39／39 勘誤，見[第一百二十一階段](docs/re/phase-121-manual-savestate-restore-boundary.md)。
- 從第四頁私有終態合法 Enter 量到第五頁底部五行敘事的低階 glyph 身分；最初的譯文誤配右側人物姓名，主代理檢視原圖後攔下並訂正，維持 DRAFT。新譯文使全部 catalog 需求增至 1006 字模；舊 997 字模正確拒絕九個新字，隨後以本機倚天重建並由 dosgolem 正式 loader 驗證 1006／1006 覆蓋。未接 runtime 或驗轉場，見[第一百二十二階段](docs/re/phase-122-story-page5-enter-trace.md)。

## 2026-09-22 — 第一百二十三階段：手冊後遊戲內保存入口邊界

- 英文手冊與中文 Data Card 指明：讀檔可在主選單或隊員管理選單，保存僅在隊員管理選單並選 A–J 槽位。成功返回分支續按已證實的 Enter 至 330M 仍只見 command/status；依手冊 Num Lock 前進鍵送入數字鍵盤 8，以及無鍵延長，均沒有新畫面、dispatcher event 或檔案操作。
- 這不能證明遊戲已進可操作冒險狀態，更不能拿建角分支的保存收據冒充手冊後 save/load。下一步是追 330M 的鍵盤 consumer 與選單轉場；未猜其他鍵、未改原版 state。見[第一百二十三階段](docs/re/phase-123-manual-return-save-load-entry-boundary.md)。

## 2026-09-22 — 第一百二十四階段：第四頁首次 glyph trace 勘誤

- 從第三頁合法 state 於絕對步 `301000000` 排入唯一正常 BIOS Enter，兩次 Docker／dosgolem 重播均維持第四頁 indexed framebuffer SHA-256 `4f9d1bb…`，並產生逐 byte 相同的 content-safe receipt；沒有輸出原文、答案、畫面或原始 state。
- 先前的「unknown caller」是舊 receipt 二進位未包含現有 glyph／return-edge 診斷所致，並非 page4 沒有 glyph path。現有來源在暫存容器重建後，量到 row 17–22 六筆 `0763:04FF → 0763:026B` guarded runs 與 entry／post 步數；`story-page4-events.tsv` 因而改為 `confirmed`／`DRAFT`。
- 逐筆比對既有 visual-transcription：line 1–5 的 length／SHA-256 都不符合低階 trace，line 6 相符。私有原圖複核後修訂繁中 DRAFT 第 3–6 行的語意順序，避免將時代資訊錯接到前一子句；來源仍為 `runtime-editorial`，未升格、未接 runtime。尚未完成文字安全矩形、失效邊界、同狀態 A/B 或 runtime 接線，不能升 READY。
- 私有收據只留在 ignored `workplace/page4-lowlevel-probe/`；容器皆以 `--rm` 完成，檢查產物為目前 UID/GID，沒有遺留專案相關容器或 root-owned 檔案。

## 2026-09-22 — 第一百二十六階段：手冊返回後的鍵盤 consumer 邊界

- 同一合法 330M state 與 Num Lock 8 重播證實：`INT 16h/AH=00h` 取走 `0x4838`，並回交 `37F1:1116`；有界指令 trace 顯示其後走 `37F1:113F → 37F1:118A` 非零輸入邊。原版玩家語意仍未知。
- IDA 9.4 的裸 OVR file offset 對照只作分級線索，不與 dosgolem 實模式位址混用；未接到選單、A–J 槽位或保存檔寫入。下一步只追這條已觀測分支至 consumer return 或下一次 key-poll，見[第一百二十六階段](docs/re/phase-126-manual-return-keyboard-consumer-boundary.md)。

## 2026-09-22 — 第一百二十七階段：面板外滑鼠 A/B 與譯文校對

- ignored Ebitengine/Xvfb 原型對同一私有原版 state、同一個面板外真實 click 做不轉送／實驗性 DOS mouse 轉送 A/B。前者座標不變，後者由 `(160,100)` 變 `(100,82)`；兩者 BIOS、IRQ 與 indexed 畫面不變。原版未 Step，不能宣稱實際遊戲操作效果。正式轉送 UX 仍待使用者選擇，見[第一百二十七階段](docs/re/phase-127-pointer-miss-ab-prototype.md)。
- 低階翻譯代理校對第二至五頁 DRAFT；第二至四頁不變，第五頁第四行縮為「讓它成為本應有的」。第四頁仍遵循第 124 階段的已證實 glyph 行序；全部仍未接 runtime。第五頁 catalog 八項測試通過。

## 2026-09-22 — 第一百二十八階段：第六頁固定敘事身分與 DRAFT 譯文

- 從第五頁合法 state 於已證實時間送入唯一 BIOS Enter，兩次 dosgolem receipt 逐 byte 相同；第六頁 row 17–22 六行 `0763:04FF → 0763:026B` exact identity 已鎖入 TSV。第一個新 glyph 前的故事區原版寫入只證明前頁失效候選，不足以證明正式 stamp lifecycle。
- 低階翻譯代理依私有底部裁切建立六行繁中 DRAFT，右側姓名與 row 24 排除；專名尚無可靠固定繁中譯名，暫保留原文。已補 catalog key、Unicode 與保守寬度驗證；全部 17 份 TSV 本機倚天重建為 1014 glyph，dosgolem 正式 loader 對 6084 個譯文字元檢查零缺字。仍未接 runtime 或完成 2×／3× A/B，見[第一百二十八階段](docs/re/phase-128-story-page6-enter-trace.md)。
- 使用者其後確認面板關閉時 canvas 內非 host 點擊轉送原版 DOS mouse、面板開啟時所有 pointer 由 host 消費；排除永不轉送。這是 MouseBridge 設計輸入，不表示 phase127 的未 Step 原型已證明玩家可見效果。
## 2026-09-22 — 第一百二十五階段：實體 host input prototype

- Docker/Xvfb／xdotool 對真實 Ebitengine 視窗驗證設定開啟、3×暫選、Cancel 回 2×且重開仍 2×、Apply 3×收合，以及面板開啟時 Enter 隔離、關閉後 Enter BIOS 排隊。
- Xvfb 固定視窗與 logical layout letterbox 導致座標漂移，runner 已以當前 X11 geometry 與比例換算重播；這不是正式視窗規格。host hit 不寫 DOS；pointer miss 不轉送 DOS mouse 仍是待決 UX，不升 READY／可玩版。

## 2026-09-22 — 第一百三十階段：Num Lock 8 的下一次 key-poll 停止線

- 同一私有 330M state／同一合法 Num Lock 8 從已確認的 `37F1:118A` 受控追蹤；dosgolem BIOS metadata
  在 `331000653` 明確記錄 `INT 16h/AH=01h`、無可用鍵，故在第一個後續 poll 停止，不追加第二鍵。
- 同終止 step 的無鍵 control 與單鍵分支 indexed framebuffer／palette 相同，dispatcher、FileOps、writes
  與未實作服務均空；完整記憶體雜湊不同但語意未知。未到主選單、隊員管理、A–J 或保存／讀檔。
- IDA 9.4 的 file-offset 線索保持第一百二十六階段既有分級；本輪僅增加 content-safe BIOS poll
  instrumentation，未改正式 runtime 或遊戲規則。詳見[第一百三十階段](docs/re/phase-130-manual-return-numlock8-next-poll-boundary.md)。
- 診斷程式已在 ignored 本機 dosgolem branch 提交 `6f828360d61696e822fd206c1fbef7c72ada02b1`
  （未 push）；poll trace 預設關閉，啟用後由起點與 4096 筆上限限制。Docker Go 1.24 的
  `go test ./internal/dos ./cmd/buckrogers-text-receipt -count=1` 通過，重跑入口已追加至 phase130。

## 2026-09-22 — 第一百二十九階段：第七頁固定敘事與繁中候選

- 從第六頁合法 state 送入一筆 BIOS Enter，兩次原版收據逐 byte 相同；另從同狀態重生 indexed 畫面、色盤與 PNG，固定敘事六行均可核對。
- 低階翻譯代理依私有裁切建立六行繁中 DRAFT；identity、key、來源、NFC 與寬度驗證通過。右側人物姓名與動態狀態列排除。尚未接 runtime，見[第一百二十九階段](docs/re/phase-129-story-page7-enter-trace.md)。

## 2026-09-22 — 手冊前景色契約證據格式與滑鼠邊界定案

- 重新核對第九十六階段的私有首題收據與 dosgolem 原版 dispatcher 參數讀取端；補齊原版輸入／state／工具雜湊、實模式位址、事件 step、indexed／palette 雜湊與推論分級。色號 10 僅為該題該 state 的觀測值；缺樣式時不繪製。GitHub #13 的限定工作因此完成並關閉，#14 的返回、存讀檔與其餘題目仍開啟。
- 使用者定案面板關閉時畫布內滑鼠轉 DOS；已轉送 Down 後，即使畫布外、控制列、面板放開或失焦，也要 Release 一次且不移動 DOS 座標。dosgolem 本機 spec228 仍 DRAFT；fake 2×／3× 事件矩陣通過，但真實有界原版收據與正式接線尚未完成。
- 其後 2×／3×各自取得真實 Ebitengine／Xvfb 畫布內 Down→Up 與 Down→控制列 Up 的 dosgolem 有界 Step 收據；外部 Up 只 Release、不 Move。舊 gzip/gob 位元組 hash 不能跨 run 比較，已訂正並以 `cmd/state-compare` 確認 3×兩例的起始正規化狀態相等。完整矩陣、玩家操作因果 A/B 與正式接線仍待完成，見[第一百三十三階段](docs/re/phase-133-real-ebiten-mouse-bounded-step.md)。

## 2026-09-22 — 第一百三十一／一百三十二階段：第八頁草稿與第二頁 READY 審查

- 第七頁合法終態在第 341M step 送一筆 BIOS Enter；兩次第八頁收據逐 byte 相同，故事區四行 row 17–20 建立 content-safe identity 與繁中 DRAFT，row 24 動態列排除。19 份譯文聯集本機倚天子集為 1025 字模，正式 loader 對 6175 個譯文字元零缺字；全套 Python 測試 225 項通過。第八頁尚未接 runtime，見[第一百三十一階段](docs/re/phase-131-story-page8-enter-trace.md)。
- 第二頁 READY 審查從合法首屏 state 重播到四行穩定 frame，控制組與既有首屏覆繪 2×／3×的原版終態相同，且前頁 active stamp 在首個相交 video-span 前失效；safe rectangle 與字模 containment 通過。續從第二頁穩定 state 合法 Enter，量到早於第三頁文字的最早相交原版 pre-write，並確認 far-return 與相對 SS/SP。
- 獨立審查抓出可丟棄負向測試將合法四行誤當錯序的缺陷；修為真正錯序、partial drift 與 return-edge 負例後，主代理和審查代理各自在 Docker 未快取重跑通過。spec 011 因此限縮升 READY，四筆 event status 升 `confirmed/READY`；全套 Python 測試 226 項通過。這只授權第二頁 adapter 實作，尚未宣稱 runtime A/B 或中文化完成。

## 2026-09-22 — 第一百三十四階段：第九頁單行敘事草稿

- 從第八頁合法終態送一筆 BIOS Enter，兩次原版收據逐 byte 相同；故事區 row 17 唯一固定行有 guarded glyph identity 與私有裁切。row 24 動態狀態列與右側姓名排除。
- 低階翻譯代理建立單行繁中 DRAFT，主代理依私有原句把帶強制拘押意味的「押送」校正為「列隊離開」；20 份譯文聯集本機倚天子集 1026 字模，正式 loader 對 6182 個譯文字元零缺字。尚未接 runtime，見[第一百三十四階段](docs/re/phase-134-story-page9-enter-trace.md)。

## 2026-09-22 — 第一百三十五階段：滑鼠焦點與放開邊緣

- Docker／Xvfb 的真實 Ebitengine 2× canvas Down 後，另一視窗取得焦點使 `IsFocused` 由真轉假；bridge 只 `ReleaseMouse(0)`、不 Move，DOS 左鍵由 1 清為 0。孤兒與重複實體 `mouseup` 未經 Ebitengine public API 形成額外 release edge，故沒有額外 DOS 呼叫；不得冒稱 bridge 收到該事件。3× panel-open 前提的新 Down／Up 對 DOS 零呼叫。
- 四個案例的起點以 dosgolem `cmd/state-compare` 正規化比較均相等；仍缺完整四角、實體 host hit/miss 路由與正常玩家因果 A/B，spec228 保持 DRAFT。詳見[第一百三十五階段](docs/re/phase-135-real-ebiten-mouse-focus-loss-and-release-edges.md)。

## 2026-09-22 — 第一百三十六至三十八階段：故事停止線、滑鼠路由及第三頁清除

- 第九頁後的合法 Enter 雙重重播只有 command/status 重畫，無固定故事第十頁；低階翻譯代理不建立猜測 catalog。另對照私有原版畫面，修正第 5 頁「終於」、第 7 頁 `salvage station` 與第 8 頁 `escorted to` 的三處繁中措辭，事件身分與 DRAFT 狀態不變。全套 Python 231 項通過；依現行 20 份 catalog 重建本機倚天 1024 字模，正式 dosgolem loader 對 6179 個譯文字元零缺字，私有 GOLEMFNT SHA-256 為 `b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`。
- 真實 Ebitengine 2×／3× host Open hit 與 open-panel 空白 miss、3× accepted Down 後 panel-open chrome Up 已補收據；DOS API 依已確認邊界隔離或只 release。面板核心對空白 miss 仍回未消費，不能冒稱完整 host route；MouseBridge 保持 DRAFT。
- 第二頁 runtime 已有雙倍率同狀態正例與退出收據；獨立稽核發現 loader 漏驗 caller／guard、presenter 非原子 Apply，已在本機 dosgolem 修正並補部分負例。spec 011 暫維持 READY，等待完整雙倍率失敗矩陣與同幀核驗。
- 本機 dosgolem `f6579d9` 新增 content-safe story fill pre-write 診斷與邊界測試。從第三頁合法 state 兩次 Enter 重播逐 byte 相同，最早與五行安全矩形相交的原版寫入為 step `301108549`、`0CF4:1B3A`、`A000:AA08`、304 bytes；首個可見差異晚 24 step。這只是第三頁 READY 前置證據，未接 runtime。見[第一百三十六階段](docs/re/phase-136-story-page10-enter-stop-line.md)、[第一百三十七階段](docs/re/phase-137-real-host-panel-route-and-3x-cleanup.md)及[第一百三十八階段](docs/re/phase-138-story-page3-exit-prewrite.md)。

## 2026-09-22 — 第一百三十九階段：第三頁控制流與 DRAFT 規格

- 從第二頁合法終態送 Enter，兩次第三頁收據逐 byte 相同；固定故事五行的 144 個 glyph 全部經 `0763:03D6`、opcode `0xCA` 的真實 RETF 返回 `0763:04FF`。首筆有界指令 trace 證實 entry SS 不變、return SP 增 `0x12`；絕對 SS/SP 只當本次錨點。已建立[第一百三十九階段](docs/re/phase-139-story-page3-return-edge.md)與[spec 012 DRAFT](docs/spec/012-story-page3-overlay-draft.md)，等待獨立 READY 審查，不接 production。
- 獨立審查指出首筆 stack trace 不足以代表全部 144 筆。本機 dosgolem `a9f2afd` 把 content-safe entry SS/SP 加入 return-edge JSON，從同一 state 雙重重播，144 筆逐一符合 same SS／相對 SP+`0x12`、RETF opcode 與 caller；收據逐 byte 相同。保留原收據並追加訂正，spec012 仍因純核心負例未審完維持 DRAFT。

## 2026-09-22 — 第一百四十至四十二階段：身體圖示停止線、第二頁驗收與第三頁 READY

- 身體圖示的七筆高階 identity 尚不足以實作；[第一百四十階段](docs/re/phase-140-body-icon-ready-evidence-stop.md)列出真實 glyph return 與最早安全矩形 pre-write 的缺口，維持 DRAFT。先前誤判缺 Go 工具鏈，已訂正為現有 `golang:1.26.7-bookworm` 可用。
- 第二頁補齊真實 return、原子提交、雙倍率失敗矩陣及正式 catalog 身分鎖定；本機 dosgolem `2f8c807` 的 targeted vet/race 通過。從同一合法 state 以最新程式重跑 control／2×／3×及合法 Enter 離頁，原版狀態相同、覆繪只在安全矩形內，離頁後零殘字。[第一百四十一階段](docs/re/phase-141-story-page2-runtime-conformance.md)使 spec 011 只在這條路徑升 CONFORMED。
- 第三頁 144 筆逐筆 entry／return stack 證據與可丟棄 typed 核心負例通過獨立審查。[第一百四十二階段](docs/re/phase-142-story-page3-ready-review.md)將 spec 012 及五筆身分目錄升 READY；尚未接正式 runtime、未做 A/B，不宣稱 CONFORMED。

## 2026-09-22 — 第一百四十三至四十四階段：第四頁低階證據與第三頁限縮驗收

- 第四頁代理雙重重播六行 192 個 glyph 的逐筆 RETF／同 SS／相對 SP+`0x12`，及 page4→page5 最早相交 `0CF4:1B3A` pre-write；[第一百四十三階段](docs/re/phase-143-story-page4-ready-evidence-draft.md)維持 DRAFT，等待獨立 READY 審查，沒有接 production。
- Terra 代理於本機 dosgolem `aae577f` 接上第三頁五行正式 watcher／presenter／CLI；主代理審查 144 筆原版 ABI 高位均為零後，先補 spec 012，再以 `9a9b769` 對七個 word 的非零高位失敗即關閉並加測。相關 Go 套件 Docker vet／race 通過。
- 從合法第二頁終態以同一 Enter 做 control／2×／3×，再以第二筆 Enter 做離頁三組；最新程式與本機倚天字型的同狀態驗證顯示五行可讀、矩形外零差異、原版 machine／DOS state 全等，離頁前寫入使 active 5→0，終態 RGBA 無殘字。專案 234 項 Python 測試及[第一百四十四階段](docs/re/phase-144-story-page3-runtime-conformance.md)的唯讀真實收據驗證通過；spec 012 只在此路徑升 CONFORMED。

## 2026-09-22 — 第一百四十五階段：第五頁 READY 前低階證據

- 從私有第四頁合法終態雙重重播第五頁，168 glyph（rows 17–21：34／38／35／36／25）逐筆直接證實 `0763:03D6`／`0xCA` RETF 回到 `0763:04FF`、entry／return 同 SS、相對 SP+`0x12`，七個 ABI word 的高位遮罩均為零；絕對 stack 值不作 runtime identity。
- 從私有第五頁合法終態雙重重播第六頁，將舊「第一筆可見 story pixel」與最早 pre-write 分開：最早相交 `[8,320)×[136,176)` 候選矩形的 `0CF4:1B3A` fill 是 step `321118382`、`A000:AA08`、304 bytes；舊 step `321118406` 是晚 24 step 的首筆可見差異。rectangle 仍為強推論，未建立正式 TSV。
- `story_page5_catalog` 的八項負例及 DRAFT 正例通過；本機 1014-glyph 倚天 top-pad 以 dosgolem loader 對第五頁 51 個譯文字元零缺字。收據、字型與原版只在 ignored `workplace/`。已建立[第一百四十五階段](docs/re/phase-145-story-page5-ready-evidence-draft.md)與索引；catalog 維持 DRAFT，未改 dosgolem production code、未 push。Docker 容器均為 `--rm`，無殘留容器。

## 2026-09-22 — 第四頁診斷幾何勘誤與滑鼠純核心修正

- 第四頁獨立 READY 審查指出[第一百四十三階段](docs/re/phase-143-story-page4-ready-evidence-draft.md)把只監測 rows 17–21 的 `storyFillIntersects()` 收據誤當成六行矩形最早 pre-write；已保留舊收據並追加勘誤。固定本機 dosgolem `564d53f` 雙重重跑 192 筆 return 一致，私有 typed 核心三項測試與第四頁 57 字元字型 coverage 通過；仍需擴至 row 22 的 committed content-safe 診斷，第四頁維持 DRAFT。
- 滑鼠 ignored `phase128` 原型原先對畫布內 Up 也只 Release；依既有 DRAFT 契約修正為畫布內 `Move→Release`、畫布外／panel／失焦只 Release。雙倍率四角與邊界 fake 測試在 `golang:1.26.7-bookworm` Docker 的 vet／race 通過；真實 Ebitengine／dosgolem 矩陣未驗，spec 228 仍 DRAFT。本機 dosgolem 文件 commit `564d53f` 留存勘誤，未推上游。
- 本機 dosgolem `ac1f7fb` 以 READY（僅診斷）的 `-story-fill-rows 6` 補量第四頁 row 22；同一合法 state 的兩份收據逐 byte 相同，48 筆 span 均相交完整六行矩形，最早 pre-write 仍為 step `310023777`。舊五行誤判的勘誤保留；第四頁譯文及 runtime 尚未經 READY 審查，仍維持 DRAFT。

## 2026-09-22 — 第四頁限縮 READY 與滑鼠畫布內放開重驗

- Terra 獨立審查第四頁六行 identity、192 筆 return、六行 pre-write、譯文目錄及本機字型覆蓋，建立[規格 013](docs/spec/013-story-page4-overlay-draft.md)並將六筆 exact catalog 升 READY。這只准開始實作第四頁固定六行及已量 Enter 離頁，正式 runtime／同狀態 A/B 尚未完成。
- 修正後的 ignored MouseBridge 原型以真實 Ebitengine／Xvfb 在 2×、3× 重播畫布內 Down→Up；兩份私有收據分別記錄 `Move→Press→Move→Release`、button 0→1→0，輸入 API 邊界的 BIOS／IRQ／indexed／memory 不變。第一次 2× 執行因錯誤覆蓋 image 的 GOPATH 而觸發離線下載失敗，已中止並沿用 image 原設定乾淨重跑；證據見[第一百四十六階段](docs/re/phase-146-real-ebiten-inside-up-corrected.md)。MouseBridge 仍 DRAFT。
- 第五頁 Terra 獨立審查補足五行 disposable typed-core 的原子／失敗即關閉負例，並以現行正式本機字型 loader 對 51 個譯文字元零缺字回讀、2×／3×靜態墨跡零越界。[規格 014](docs/spec/014-story-page5-overlay-ready.md)及五筆 exact catalog 限縮升 READY；尚未接正式 runtime 或同狀態 A/B。
- 第四頁 watcher／catalog／presenter 的可測核心已在本機 dosgolem `63396bb` 提交，相關套件的 Docker test／vet／race 通過；CLI、A/B 與離頁收據未完成，不能升 CONFORMED。

## 2026-09-23 — 第四頁正式接線與同執行離頁 A/B

- 主代理在本機 dosgolem `1cf9ec4` 接通第四頁 CLI；Docker Go test／vet／race 通過。從合法第三頁終態的 control／2×／3×皆六 key 啟用、零缺字、安全矩形外零差、原版 JSON 與正規化存態全等；同一次執行送第二筆 Enter 後，兩倍率於已量 pre-write 由 active 6→0，終態 RGBA 等於 baseline。第一個從第四頁獨立 state 直接離頁的測試未曾建立 active，不足以驗清除，已以雙 Enter 重跑訂正；詳見[第一百四十七階段](docs/re/phase-147-story-page4-runtime-ab-pending-audit.md)。完整失敗矩陣尚缺，spec 013 暫維持 READY。

## 2026-09-23 — 第五頁正式接線與同執行離頁 A/B

- Terra 在本機 dosgolem `0f3ea89` 完成第五頁 watcher／presenter／CLI；主代理從提交後 runner 重跑穩定 2×及同執行雙 Enter 2×，與私有收據逐 byte 相同。control／2×／3×皆五 key 啟用、零缺字、安全矩形外零差，原版 JSON 與正規化存態全等；離頁 active 5→0，終態 RGBA 等於 baseline。詳見[第一百四十八階段](docs/re/phase-148-story-page5-runtime-ab-pending-audit.md)。完整失敗即關閉矩陣仍待獨立審查，spec 014 維持 READY。

## 2026-09-23 — 第四／五頁限縮 CONFORMED 與第六頁前置診斷

- Terra 在本機 dosgolem `5652f11` 補第四頁 ABI、return、未知／不相交寫入負例；`a2dba44` 補第五頁 presenter 原子負例。主代理於 `6181e31` 再補第五頁完整 hash gate、return step、已啟用後未知／不相交寫入與雙倍率缺字、非 READY 負例；`6dcc427` 補第四頁正式 loader 的雙倍率缺字、DRAFT catalog 拒絕。Docker Go test／vet／race 通過；原先 control／2×／3×及離頁私有收據雜湊回讀相符，未修改 runtime code。因此[規格 013](docs/spec/013-story-page4-overlay-draft.md)與[規格 014](docs/spec/014-story-page5-overlay-ready.md)只在固定合法 Enter 進入／離頁路徑升 CONFORMED，完整開機、其他離頁與存讀檔未驗。
- Terra 雙重重播第六頁 200 筆 glyph 的 return／ABI 與離頁 48 筆候選矩形相交 pre-write；主代理回讀兩組 state 及雙份收據 SHA-256。[第一百四十九階段](docs/re/phase-149-story-page6-ready-prerequisite-diagnostics.md)保留精確 runner 身分未記錄的限制，第六頁保持 DRAFT，不接 production。

## 2026-09-23 — 真實 Ebitengine 雙倍率四角與排除邊界

- Terra 將 ignored Linux／Xvfb 原型擴成資料驅動 geometry harness，真實 Ebitengine 2×／3×四角均映射到 DOS `(0|319,0|199)` 且 `Move→Press→Move→Release`；控制列、右與下 exclusive 邊界均零 DOS API。十四份私有收據、原型競態測試與 1 logical-pixel 觀測 guard 的非正式範圍見[第一百五十階段](docs/re/phase-150-ebiten-mouse-geometry-prototype.md)。MouseBridge／Linux 前端仍 DRAFT，cleanup 完整矩陣與正常玩家因果未驗。

## 2026-09-23 — 離開畫布仍放開的雙倍率實體矩陣

- Terra 延伸 ignored Xvfb／Ebitengine harness，雙倍率各重播控制列、畫布外右側、面板預先開啟、失焦的已接受 Down→cleanup；皆只 Release、不 Move，DOS 最後有效座標不變，BIOS／IRQ 未觸。3×孤兒與重複 X11 mouseup 的 Ebitengine public API 未暴露新 release edge，據實記停止線。十份私有收據見[第一百五十一階段](docs/re/phase-151-ebiten-mouse-release-cleanup-prototype.md)；下邊界、正式面板 hit/miss 與 Linux 正式前端仍未完成。

## 2026-09-23 — 第六頁限縮 READY

- Terra 在 ignored `workplace/page6-ready-atomic-core/` 建立可丟棄六行 typed-core、失敗即關閉負例及雙倍率字型 containment；以本機 dosgolem `6dcc427` 重建 runner，從合法第五／六頁 state 各雙重重生，與先前 entry／exit 收據逐 byte 相同。另位 Terra 獨立審查訂正錯誤檔名造成的初步誤判後，確認[規格 015](docs/spec/015-story-page6-overlay-ready.md)與六筆 event catalog 只在固定六行及已量 Enter 離頁升 READY；正式 watcher／presenter／CLI 與同狀態 A/B 未完成。證據與勘誤見[第一百四十九階段](docs/re/phase-149-story-page6-ready-prerequisite-diagnostics.md)。

## 2026-09-23 — 第六頁正式接線與限縮 CONFORMED

- Terra 在本機 dosgolem `e3e1db1` 完成六行 core，主代理 `a7304e3` 補真正缺字及 presenter 原子負例，Terra `0ce4948` 接正式 CLI。主代理以最新 runner 從合法第五頁終態重生 control／2×／3×穩定及同執行 Enter 離頁：六 key 啟用、零缺字、安全矩形外零差、原版事件與正規化 machine／DOS 全等；離頁 active 6→0，終態 RGBA 等於 baseline。Docker Go test／vet／race 通過；[第一百五十二階段](docs/re/phase-152-story-page6-runtime-conformance.md)保存私有收據雜湊、工具與權利邊界。規格 015 只在固定路徑升 CONFORMED，不外推完整開機、存讀檔或其餘遊戲文字。

## 2026-09-23 — 第七頁 READY 審查與面板 pointer 原型

- Terra 以精確 runner 從合法第六／七頁 state 雙重重播，取得第七頁 190 glyph 的 return／ABI 與合法離頁最早相交 pre-write；可丟棄 typed-core、正式 DRAFT 拒絕與雙倍率靜態字模 containment 見[第一百五十三階段](docs/re/phase-153-story-page7-ready-prerequisite-diagnostics.md)。獨立審查指出 ABI 低位映射／drift 負例與正式 3× renderer 幾何兩缺口；Terra 已在 ignored 工具補上並重生收據。複審又找到 row137 左 margin 不相交寫入誤清覆繪的原型缺陷；Terra 改為逐列半開區間並補測，待末次獨立審查。舊第 129 階段「首筆寫入」亦已追加勘誤。第七頁仍 DRAFT，未接 production。
- Terra 的 ignored Linux／Xvfb 原型補雙倍率面板 Open／一般命中／空白 miss、閉面板畫布轉送，以及外部／控制列／面板／失焦只 Release 的真實事件收據；[第一百五十四階段](docs/re/phase-154-ebiten-panel-pointer-miss-prototype.md)記錄面板核心空白 miss 尚回未消費的正式接線缺口。前端與 MouseBridge 仍 DRAFT。
- Terra 修正第七頁 ignored pre-write 為逐列半開相交並重生私有收據；獨立末次審查核對雜湊與邊界反例後，確認[規格 016](docs/spec/016-story-page7-overlay-ready.md)及六筆 event catalog 可限縮升 READY。這只授權正式 watcher／presenter／CLI 接線；control／2×／3×同狀態 A/B 與離頁無殘字尚未做，未升 CONFORMED。

## 2026-09-23 — 第七頁正式接線初驗與第八頁原版蒐證

- 本機 dosgolem `37a6775`、`a5743ab`、`baecc72`、`0ddd860`、`1961e69`、`fe1beb0` 逐步接上第七頁 watcher、strict loader、presenter 與負例；獨立稽核發現 absolute step provenance 與 runtime step 順序混稱、discontinuity 可復活舊事件及雙倍率 failure matrix 未全。`d42567d` 原子接通 CLI 並修前兩項；[規格 016](docs/spec/016-story-page7-overlay-ready.md)已澄清絕對步數只屬固定原版收據，runtime 必須允許合法玩家於不同時間 Enter。完整雙倍率負例仍待補，尚不升 CONFORMED。
- 主代理以 dosgolem `d42567d` 從合法第六頁 state 重生第七頁 control／2×／3×：六 key、零缺字、安全矩形外零差；又在同一程序連排 331M／341M Enter，兩倍率都記錄 step `341018656` 的 active 6→0、終態 RGBA 與 baseline 相等，正規化 machine／DOS 與控制組相同。第七頁完整 failure matrix 尚待獨立通過，現況仍 READY 而非 CONFORMED。
- 第八頁原版證據在[第一百五十五階段](docs/re/phase-155-story-page8-ready-prerequisite-evidence.md)補四行 130 glyph 的雙重 SS/SP／RETF 收據，以及 page8→page9 最早相交 pre-write；缺字型真實幾何與 typed-core，仍 DRAFT。
- [第一百五十六階段](docs/re/phase-156-story-page7-runtime-ab-pending-failure-audit.md)固定第七頁 runner、六份 stable／同程序離頁 A/B 收據及正規化 state digest；同程序 pre-write active 6→0 與終態 RGBA==baseline 已證實。獨立稽核撤銷「runtime 必須鎖絕對 step」與「離頁未測 active 清除」兩項誤判，仍要求正式 2×／3×完整 failure matrix；規格 016 維持 READY。
- 第八頁 DRAFT 候選由低階翻譯代理逐行核對原版畫面，現有四行譯文忠實且不需改動；另位代理以現行倚天字型重生 2×／3×正式幾何 containment，logical `[8,96)×[136,168)` 零缺字、零越界。私有收據與仍缺 typed-core 的停止線追加至[第一百五十五階段](docs/re/phase-155-story-page8-ready-prerequisite-evidence.md)。
- 本機 dosgolem `940e5f3` 完成第七頁 2×／3×完整 failure matrix；主代理獨立重跑 apps／CLI 定向 test、vet、race 均通過。全樹 race 的既有 CPU 單步測試超過 10 分鐘且無 race report，未冒稱全樹通過。結合同狀態正例與同程序 active 6→0，[規格 016](docs/spec/016-story-page7-overlay-ready.md)只在固定六行與已量 Enter 離頁升 CONFORMED；完整開機及存讀檔仍未知。
- 第八頁 ignored typed-core 補 exact identity、130 glyph return／ABI、原子群組、逐列 pre-write 與 restore 等失敗即關閉；正式 DRAFT catalog 被拒，只用暫存 READY fixture 測正例。私有 receipt SHA 與限制已追加[第一百五十五階段](docs/re/phase-155-story-page8-ready-prerequisite-evidence.md)，尚待獨立 READY 審查，未接 production。
- 第八頁首次獨立 READY 審查確認原版 entry／exit、譯文與字型 containment 證據成立，但發現 typed-core 只測四個人工整行物件，receipt writer 將 130 筆與 exit step 常數倒填，未直接驗四份原始 JSON。已退回補端到端 parser／mutation 負例；正式 catalog 保持 DRAFT。
- 原代理將第八頁 verifier 改為直接讀雙重 entry／exit 與同重播 glyph-run JSON，逐筆驗 130 return edge、聚合四行 hash 並自行找 earliest pre-write；mutation 負例直接改收據資料，新 receipt 可逐 byte 重生。edge schema 未逐筆明文輸出 glyph low byte，改由同重播 run SHA 承諾；已交第二次獨立 READY 審查，尚未升級。
- 第八頁第二次審查一度同意以 logical `[8,96)×[136,168)` 限縮 READY；主代理在寫正式規格時反查原文最長 38 glyph，發現該矩形只包 11 個中文字格、會留下右側英文殘字。已撤回升級並退回重訂完整原文清除矩形、字型 containment 與 pre-write typed-core；catalog 保持 DRAFT。
- 原代理以 max 38 glyph 與 exit 32/32 scanline 的 x=8／CX=304 fill，將第八頁最小已量矩形訂正為 `[8,312)×[136,168)`；新增字型與 typed-core corrigendum receipts，保留並 backlink 舊窄矩形收據。新幾何零缺字／越界且端到端 verifier 六項通過，正交第三次獨立 READY 審查。
- 第八頁第三次獨立審查重生兩份 corrigendum receipts，確認完整英文清除右界、32 列 fill、端到端 130 edge 與失敗即關閉契約；[規格 017](docs/spec/017-story-page8-overlay-ready.md)及四筆 event catalog 只在固定四行與已量 Enter 進出升 READY。正式 runtime／A/B 未接，未升 CONFORMED。

## 2026-09-23 — 第八頁正式接線與限縮 CONFORMED

- Terra 在本機 dosgolem `c0f6d76` 原子接通第八頁 strict loader、watcher、verified RETF、逐列 pre-write 失效、presenter、RGBA／PNG 與 JSON receipt。另一代理獨立審查 flags、generation、完整英文清除矩形與雙倍率失敗即關閉，Docker 定向 test／vet／race 均通過。
- 從合法第七頁終態重生 control／2×／3×，兩倍率均四 key、零缺字、安全矩形外零差，正規化 machine／DOS 與控制組相等；同程序兩筆 Enter 在 step `351154334` 記錄 active 4→0，離頁終態 RGBA 等於 baseline。人工檢視兩張 PNG 亦確認英文四行完整清除、人物與右側動態區不受影響。詳見[第一百五十七階段](docs/re/phase-157-story-page8-runtime-conformance.md)。規格 017 只在此固定路徑升 CONFORMED，完整開機、存讀檔及第九頁仍未知。

## 2026-09-23 — 第九頁 entry 補強與 lifecycle 停止線

- 以本機 dosgolem `c0f6d76` 建置固定 runner，從合法 page8 state 雙重重生第九頁；兩份 content-safe entry 收據逐 byte 相同，20 glyph 均直接證實 `0763:03D6`／`0xCA` 返回 `0763:04FF`、同 SS、SP+`0x12` 及七 ABI word 高位為零，與既有單行 DRAFT identity 一致。
- 從合法 page9 state 在 361M 送 Enter 的兩份 exit 收據亦逐 byte相同，但到 370M 都沒有 story fill 或 story pixel write。有界 key probe 證實 Enter 在 step `361000150` 由 BIOS AH=00 消費，之後只於 row 15 產生 command/status glyph；不能把這個轉場當成 page9 覆繪失效。真正清除故事區的合法後續動作與最早相交 pre-write 尚未知，故停止 READY typed-core、不接 production，頁 9 維持 DRAFT。證據、runner 與限制見[第一百三十四階段](docs/re/phase-134-story-page9-enter-trace.md)；私有原版、state 與完整收據只留 ignored `workplace/`。
- 續以中文手冊明示的數字鍵盤 4／6，各自從同一 page9 state 做雙重 361M–361.1M 有界重播；兩鍵均在 `361000150` 被 BIOS 消費，唯一寫入是 step `361028641` 的 row 24 command/status clear 與 33 glyph。四份 content-safe receipt 的 `story_fill_writes`／`story_pixel_write` 均空，未碰故事區；收據在 ignored `workplace/page9-lifecycle-search/`。固定 runner 與原版均沿用前項，Docker `--rm` 容器已清理。頁 9 仍 DRAFT；後續需先由手冊證實適用於此 state 的不同玩家動作，不能猜鍵。
- 同一 consumer 使手冊明示的 Num Lock 8 成為合法候選；雙重 receipt 在 `361000150` 消費 `48:38` 後，依指定的下一 `0C10:0305` poll 於 `361000605` 停止（遠早於 362M safety cap）。兩份 SHA-256 均為 `fdb75c61c2a5f1d6c800be4088bea9ff92a4378b4ac51560b96cd685a17112a2`，無 event、clear、glyph、return、story fill 或 story pixel 寫入。這不是 8 無效的語意結論；只是 page9 失效仍未知，按停止條件不延長或猜鍵，頁 9 維持 DRAFT。Docker `--rm` 容器已清理。

## 2026-09-23 — 身體圖示低階 return／ABI 與 pre-write 停止線

- 從 dosgolem `c0f6d76b0eb60caa72e74a619c1b981c91b340a5` 以 `git archive` 建立 ignored、可丟棄 probe source；只在副本擴大 glyph-return trace caller 篩選，production dosgolem 與本專案 runtime 均未修改。probe runner SHA-256 為 `d8e29a6d7597c8f0757aeee5d7fe24f2f6e30894f0080189a4917ec192a7a740`；`GAME.OVR` SHA-256 為 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`，起始 state SHA-256 為 `cfe15d3c66c9fe3c2e684815740a0cc0165e59d08ab5866370608d49f8a8e164`。
- 依已證實的正常移動、Enter→N、Enter→Y 路徑各雙重重播，三組 JSON A／B 逐 byte 相同，SHA-256 為 `464b2c648553729bdd6ffc28158fdceb653421a2f14c878f96c357d658379033`、`382ca0d5d8ca070ec42a9faa2efba9666b872ce98fc817193852783ba95b6eec`、`14aecfcd5c7f77e5e9855690dc8a592e70b2aa9250972533a5bd47865bb90a00`。七筆文字逐 glyph 證實 `0763:03D6`／`0xCA` RETF 回 `0763:049B`、同 SS、SP+`0x12`；每次字串首 glyph 的七 ABI word 高位 mask 為 `0x7c`，其餘 glyph 為零。位址均為 dosgolem 8086 實模式 `segment:offset`，非 IDA 線性位址。
- 現有 runner 無法排除圖示／背景在首 glyph 前已寫入安全矩形，故 glyph entry 不能當成最早 pre-write。READY 前必須新增受限於七個安全矩形的通用 pre-execution video-write 或逐 step framebuffer 診斷，再以三條合法路徑雙重重播；在此之前不建立 READY typed-core、不接 production，身體圖示保持 DRAFT。完整終態 framebuffer 雜湊與限制見[第一百四十階段](docs/re/phase-140-body-icon-ready-evidence-stop.md)。

## 2026-09-23 — 身體圖示 READY 候選包

- 本機 dosgolem `2755f7c` 以明示 body trace 補 `REP STOSB` 與 IDA 已證實 `0763:184D/1854` 單 byte glyph store；同值重畫亦可記錄，非 A000、未知 opcode／位址與不相交 span 不輸出。refuse A/B 逐 byte 相同，receipt SHA-256 `7971fd3aae514698cb8ee8846affb852b1e09b33e86640560bb6f79d2a880348`；六個已量 active 轉場的 earliest pre-write 與位址空間見[第一百四十階段](docs/re/phase-140-body-icon-ready-evidence-stop.md)。
- ignored `workplace/body-icon-ready-atomic-core/` 新增可丟棄 typed-core，直接解析正式 catalog／rects、三路 return 與 pre-write receipts，鎖七 identity、首 glyph ABI mask `0x7c`／其餘零、verified RETF、generation／原子群組、restore／discontinuity 及 unknown／duplicate／partial 負例；正式 DRAFT catalog 被拒，正例只用暫存 READY fixture。正式 Phase 101 倚天字型的 2×／3× containment 通過。Docker 5 項測試全綠，typed receipt SHA-256 `22017162ace0bbaebbf16fcbddcd0478a6c346f0c66b1c99d6f3b6e7503e64bd`。spec009 與 catalog 維持 DRAFT，未接 production，等待另一代理獨立 READY 審查。

## 2026-09-23 — 身體圖示完整 A000 證據與 READY 審查拒絕

- dosgolem `9eb9457` 新增預設關閉的通用 A000 pre-write observer；aggregate 收據仍觀察
  每筆寫入並保存順序摘要、writer groups、連續 spans 與各矩形 first，不再逐像素輸出。
  move／refuse／confirm 三組 A／B 均逐 byte 相同；refuse 安全矩形命中 66,176 次，證實
  舊 65,536 cap 會截斷。完整觀察訂正 confirmation／save prompt first：confirm 為
  `106216585`、refuse 為 `106679837`，兩者都是 `0763:184D` glyph store；舊文件所列稍後
  F3AA fill 不是 first。
- typed-core 擴充為 11 項測試並通過，會拒絕偽造較早寫入、舊 F3AA-first confirmation、
  非法低階 ABI、混合／部分群組及全零字模；receipt 明示 `ready:false`。獨立 Terra 審查
  另以 Docker 重跑 Python 11/11 與 dosgolem Go test／vet，拒絕升 READY：正式 watcher／
  dirty-state 尚未證明能在任何 writer 的 first intersecting write 前安全介入，且真實三路
  event 時序尚未直接驗證 group／transition／generation。spec009、catalog 維持 DRAFT，
  未接 production。

## 2026-09-23 — 身體圖示限縮 READY 通過

- ignored typed-core 再將真實 move／refuse／confirm return-event 收據按 step 直接餵入
  watcher，驗得 2／3／3 代合法群組；A000 dirty-state adapter 以完整 spans 與 commit 合併，
  在 first intersecting write 前原子失效整代。未知 writer／key、提早或缺失 first、錯
  generation、partial／mixed／duplicate、同值寫、跨 group 與 span 跨 commit 等負例均
  失敗即關閉。14/14 通過，新 receipt SHA-256 `982e29362e5b98d812f91ba481b21fb8388932acee28f108d70d47444b7b1985`。
- 第二位獨立 Terra 以 Docker 重跑 typed-core 與 dosgolem 定向測試後判定限縮 READY 通過；
  「尚未接 production」屬 READY 後的 implementation，不再形成循環阻擋。spec009 只授權
  七 identity 與固定 move／refuse／confirm 路徑；離開儲存詢問、restore、完整開機、其他
  輸入與未觀察 writer 仍排除。production 尚未接線，未標 CONFORMED。

## 2026-09-23 — 身體圖示固定三路限縮 CONFORMED

- dosgolem 本機分支 commit `ae36f540ee6097ab77c135d12d4c05c7520c315a` 接入正式 body
  icon watcher、A000 pre-write dirty-state 原子失效及倚天 2×／3× presenter；正式 app／CLI
  的 test、race、vet 均通過。全樹測試只被 ignored workplace 多個研究 probe 的重複 `main`
  擋住，已分類為探針包裝問題。
- move／refuse／confirm 各做 control／2×／3× A／B，共 18 份收據；summary SHA-256
  `befbe1e11ffba4334dae1122da6e549b415f7d3b3583f3e374cd00007b6659a0`。三路的核心
  machine／DOS／indexed／palette／input／file events 與 A000 aggregate 跨倍率相等；A／B
  逐 byte 相同，missing glyph、矩形外差異與動態圖示污染皆為零，first-write clear 通過。
- 獨立 Terra 重跑 production race／vet、14 項 typed verifier 與收據雜湊後 PASS。收據 runner
  與 final commit 只差有效七列 catalog 不會觸發的行數 guard，無須全量重跑。spec009 只在
  固定三路與已量視窗標 CONFORMED；save-prompt 離頁、restore、full boot 及其他路徑仍排除。

## 2026-09-23 — 首屏固定五行限縮 CONFORMED

- 本機 dosgolem `9f4c5f0` 補首屏 strict catalog／generation／receipt gate、未知 execution epoch
  清除，及 2×／3× fail-closed 矩陣；partial、mixed、duplicate、錯 generation/key、缺字與
  非 READY catalog 均零 stamp、零 draw。Docker 定向 `go test`／`go vet`／`go test -race` 的
  apps 與 receipt CLI 通過。
- 以固定 runner、合法 `phase12-before-question.state` 與既有私有 BIOS receipt 重生
  `workplace/phase160-story-opening-replay/` 的 control／2×／3×首屏及同程序 Enter 離頁。
  `state-compare` 證實 control↔兩倍率 normalized machine／DOS 全等；raw `.state` bytes
  含序列化差異，不作 parity 比較。首屏 active 五 key、矩形外零差；Enter 在
  `281020548`／`0CF4:1B3A`／`A000:AA08`／`CX=304` 使 active 5→0，終態 RGBA==baseline，
  且沒有第二頁 overlay。spec010 只在此固定五行與已量正常 Enter 離頁升 CONFORMED；
  第二頁、其他離頁、完整開機與實際存讀檔均排除。

## 2026-09-23 — 規格與文字索引現況勘誤

- 回查 spec 005、010、017 的檔案狀態與已推送的同狀態收據，訂正
  `docs/spec/README.md` 原先仍列 DRAFT／READY 的舊狀態；同步訂正 `text/README.md`
  對身體圖示與劇情第 1、4–8 頁「未接 runtime」的過時敘述。只修現況入口，保留各階段
  歷史證據及限縮範圍；本次沒有變更譯文、遊戲程式或原版資料。

## 2026-09-23 — 現行倚天字型字元清單同步

- 發現版控內 `font/characters.txt` 仍只有早期 24 字，而完整 20 份 TSV 已需 1024 字；
  也發現跨畫面共享的文字鍵會使原本 `chars` 的跨檔唯一鍵檢查誤拒字型聯集。
- `chars` 改為逐檔驗證後取 Unicode 字元聯集，`lint`／`build` 的跨檔唯一鍵限制不變，
  並新增共享鍵回歸測試。Docker 14 項字型工具測試通過；重生清單 SHA-256
  `daa100bfbcc917a3f9dc811a2b34262a9e26dc5666c0b085c58c1d0815abbd93`。
- 本機倚天 `top-pad` 產物位於被忽略的 `workplace/current-font/`，GOLEMFNT SHA-256
  `b2b63c89f73abc9fbd13054d2efef355455b33e9ebdd56604e7c76f1e5aad7eb`；20 份 TSV
  全部譯文字元回讀零缺字、零多餘字模。字型與來源均未加入 Git。

## 2026-09-23 — 加入角色後功能選單七項譯文候選

- Terra 從 phase54 已加入角色的合法 state 以 Right→Enter 正常返回功能選單，雙重 receipt
  及 framebuffer 逐 byte 相同；私有證據在 `workplace/phase158-post-join-exit-probe/`。
  七項固定文字有原始 caller、列、色彩、長度／雜湊；動態隊伍資料與已收錄鄰項排除。
- 較輕量模型依現有繁中術語與手冊文字提出七項譯法；主代理將其隔離成獨立
  DRAFT catalog，不送入正式 runtime。兩項帶 `game` 的命令只依字面翻譯，未證實功能語意；
  選取反白、安全矩形與清除生命週期仍待證據審查。
- 因新譯文需求，Docker 以唯讀倚天來源重建 21 份 catalog 的本機字型：1026 字模，
  `font/characters.txt` SHA-256 `04d33bb125b00dad647abadfb3c9da8f7a714d722581fc6676d393a32eb6a03f`，
  GOLEMFNT SHA-256 `ef9fb6c9c2206a98286089888d3cf554a8fb491738f76fe0559bf7bcdcdbbc2d`。

## 2026-09-23 — 加入角色後功能選單選取與離頁收據

- Terra 以同一合法 `a-joined.state` 雙重重播七項 normal／selected 變體；普通回寫
  `37F1:1856`、反白 `37F1:175D`，色號分別 `0/10`、`15/0`。正常 Down 僅清除
  row 24 prompt，不觸七項文字。
- 正常 `EXIT TO DOS` Enter 於 step `125119490` 取得第一筆覆蓋七列的
  `026F:029C` pre-write；雙重 JSON 與 framebuffer 各逐 byte 相同。主代理回讀原始
  hash／事件／clear 範圍後寫入[第一百六十一階段](docs/re/phase-161-post-join-menu-selection-and-exit.md)。
  其他選項語意及中文覆繪仍未知，catalog 維持 DRAFT。

## 2026-09-23 — 正式 MouseBridge 限縮符合性

- dosgolem 本機分支 `429c6e8` 將 spec228 限縮升 READY；Terra 隨後以
  `023e1dd` 實作 generic `host.MouseBridge`，`1dafb0a` 補極大尺寸溢位與 host
  capture 重複 Down 的失敗即關閉。主代理獨立重跑 host vet／test／race 通過。
- ignored Ebitengine/Xvfb harness 改為直接使用正式 bridge；phase179 七份 2×／3×
  control／click 及 2× release-only 收據，與舊原型的 API 與完整 phases 逐欄相等。
  主代理核對來源／收據雜湊後，本機 dosgolem `c20ab29` 限縮標 CONFORMED，
  `4589bfe` 訂正首頁狀態文字。證據與未驗範圍見[第一百七十九階段](docs/re/phase-179-formal-mousebridge-conformance.md)。
- 尚未接正式 Linux 玩家視窗；spec004、Issue #16 保持開啟。dosgolem 專用分支未推上游。

## 2026-09-23 — 加入角色後選單 DRAFT 規格獨立審查

- Terra 建立規格 018 的安全矩形、雙倍率倚天靜態 containment 與 20 筆 request 的
  可丟棄世代原型；主代理在 Docker 內獨立重跑四項正反例通過。
- 審查維持 DRAFT：七筆首次繪製之外的反白／普通回寫變體尚未進版本化 exact 表，
  `026F:029C` clear 收據也不能排除其他 A000 writer 更早碰中文字區。READY 前只補
  這些證據與 typed 失敗矩陣；正式程式與同狀態 A/B 留到 READY 後，不製造驗收迴圈。

## 2026-09-23 — 加入角色後選單完整 A000 寫入勘誤

- Terra 從同一合法 state 以本案 dosgolem fork `4589bfe` 雙重重播完整 A000 pre-write；
  含同值寫入的兩份私有收據逐 byte 相同。七個 active generation 最早相交寫入均為
  `0763:184D` 原版 glyph primitive，早於原先只量到的 Exit 全選單 clear。
- 七列初畫、普通回寫、反白共 21 個 exact 變體已寫入可版控 TSV；row 20 普通回寫後的
  row 21 反白未收錄，候選契約先失效並拒絕殘留。原先 Exit clear 收據保留，
  在[第一百六十一階段](docs/re/phase-161-post-join-menu-selection-and-exit.md)追加勘誤；
  權威 fork 來源與雜湊見[第一百八十階段](docs/re/phase-180-post-join-menu-complete-a000-prewrite-corrigendum.md)。
- 曾以原 dosgolem HEAD `d9c0c27` 取得觀測，但 Machine／DOS／VideoWrite 與本案 fork
  存在差異，故不作正式依據；改由 fork 重生。spec018 仍 DRAFT，未接正式 runtime。

## 2026-09-23 — 加入角色後選單限縮 READY 獨立審查

- 主代理核對 21 筆精確變體、七筆繁中候選、phase161 與權威 fork phase180 各雙重收據，
  並以 Docker 獨立重跑七項可丟棄正反例通過；字型零缺字、零溢位及所有輸入雜湊見
  [第一百八十一階段](docs/re/phase-181-post-join-menu-ready-review-candidate.md)。
- 依規格閘門，只把已量的七項初畫／逐列 Down 重畫限縮升 READY，授權下一步接正式
  watcher／loader／generation core／RGBA presenter。row20→未收錄 row21、restore／stop／未知 writer
  必須失敗即關閉。此階段未做 runtime A/B，不宣稱畫面已中文化或整個選單 CONFORMED。

## 2026-09-23 — Host 介面文案補入倚天字型子集

- 真實 Ebitengine／Xvfb 前端原型的倚天字型檢查發現主機面板「套用」缺字；
  因原子集只由遊戲譯文 TSV 產生，這是資料清單缺口，不是 DOS 原版問題。
- 新增 `text/host-ui.zh-TW.tsv` 作「設定／套用／取消／2×／3×」唯一正式文案來源，
  Docker 以 22 份 TSV 重建 1028 字模。字元清單、私有 GOLEMFNT 與 manifest 雜湊見
  [字型入口](font/README.md)，輸出所有權為目前使用者，未把字型 bytes 加入 Git。
- 同一有界實體 X11 測試在新字型下通過：2×／3×畫面分別為 640×436／960×654，
  設定按鈕可量到白色字模墨跡，Open→Apply 3×→canvas click 的 DOS 呼叫為
  `Move,Press,Move,Release`。這仍是空遊戲畫布的 DRAFT 前端原型，不是可玩中文版。

## 2026-09-23 — 新字型再審與 Linux 前端實體事件

- `host-ui.zh-TW.tsv` 使倚天子集變成 1028 字模，與 post-join 限縮 READY 原先釘選的
  1026 字模 SHA 不同；正式接線先暫停。主代理用新字型在 Docker 重跑七項 verifier
  全通，21 個 exact variant、雙倍率七列零缺字／零越界；新字型與收據 SHA、歷史 pin
  的關係已追加於[第一百八十一階段](docs/re/phase-181-post-join-menu-ready-review-candidate.md)。
- dosgolem 本機分支 `97e5f4f` 將 Linux host 面板標籤改為呼叫端注入，測試從正式 TSV
  取字；Docker／Xvfb 真正執行 2× 開面板、選 3×、Apply、畫布點擊，
  `go test`／`go vet` 均通。實體收據與截圖只在 ignored `workplace/`，
  詳見 fork `docs/re/phase-180-linux-ebiten-router-draft.md`；仍無原版玩家畫布。
- 子代理以本機 fork `ab1731c` 把 post-join READY 的 loader／watcher／presenter 小切片
  接入 `cmd/buckrogers-text-receipt`，定向測試與 vet 通過；私有正常玩家路徑 2×／3×
  同狀態 A/B 尚未取得，故 spec018 不能升 CONFORMED。

## 2026-09-23 — 加入角色後選單局部正常路徑 A/B

- 本機 dosgolem fork `35bd3fb` 釘選現行倚天 SHA，`ce0cdb8` 修正 entry／return
  row gate，`157ec93` 依 phase180 證據只在 active layer 監看 A000 失效；初畫期
  `0CF4:1B3A` 不再誤報未知 active writer。主代理獨立 Docker 重跑 apps／CLI test
  與 vet 通過。
- fork `cb3ca77` 修正 3× 覆繪後，control／2×／3× 同狀態終態 JSON 的已收錄欄位
  逐位元組相同（事件、BIOS 按鍵、記憶體、原始畫面與色盤；不涵蓋完整 DOS／檔案狀態）；
  主代理獨立回讀私有 RGBA，七列安全矩形外零差、內部 2× 6521／3× 13659
  個變動像素。row 21 未收錄 identity 以退出碼 1 拒絕，不產生新覆繪收據。
  雜湊、原版位址基準與驗收限制見[第一百八十二階段](docs/re/phase-182-post-join-menu-runtime-ab-partial.md)。
- 原始壓縮檔、savestate、字型與 RGBA 留在 ignored `workplace/`；本輪 Docker
  容器皆一次性清理。曾發現 dockerd 因不存在掛載來源代建的 root-owned
  `workplace/phase182-postjoin-ab` 空目錄，主代理確認無內容後只移除該精確目錄，
  並改用存在且 owner 1000 的輸出路徑。尚缺逐幀 active→empty 與 Exit clear
  後無殘字，spec018 保持 READY。

## 2026-09-23 — 功能選單 Enter 路徑的原版身分勘誤

- 舊 phase161、spec018、上述歷程把 step `125100053` 的 Enter 說成
  `Exit to DOS` 離頁。主代理重新對 `START.EXE` SHA-256
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`
  定長逐 byte 回查：row 21／offset `0xE421` 是 `Exit to DOS`，但舊收據
  Enter 前最後反白的是 row 12／offset `0xE2E9` 的 `Create New Character`。
  兩筆原文各自唯一吻合雙重顯示事件 SHA；舊清除的 step／矩形仍有效，
  「Exit clear」語意撤回。詳見新索引的
  [第一百八十三階段](docs/re/phase-183-post-join-exit-identity-corrigendum.md)。
- 低階翻譯代理已為 row 21 提出「返回 DOS」等短譯，但只是 DRAFT 候選；
  新 row 21 生命週期與真正 Exit Enter 當時仍須原版雙重重播，再經獨立 READY 審查。
  這次只訂正文獻與安排 DRAFT 探針，沒有修改原版資料、正式譯文或
  既有七列 READY watcher。

## 2026-09-23 — 真正 Exit to DOS 確認分支與 Linux 真實畫布原型

- 從合法加入角色存態選到 row 21 後直接 Enter，雙收據證實先顯示離開詢問；
  首次 Y 再顯示未存檔確認，N 清除並重畫原選單，兩次 Y 則在步數上限前使
  DOS `Exited`。四組雙收據 SHA、原版短提示的檔案 offset、BIOS 消費 step 與
  仍未量的最早 A000 pre-write 見[第一百八十三階段](docs/re/phase-183-post-join-exit-identity-corrigendum.md)。
  未把舊 row 12 clear 重新命名為 Exit clear，也未接 row 21 正式覆繪。
- 本機 dosgolem fork 的 Linux Ebitengine DRAFT 原型已由私有加入角色存態顯示
  真實 320×200 原版畫布，實體 X11 輸入完成面板攔截、2×→3× Apply 與關面板後
  Enter 送入 DOS；收據與限制在 fork 的 `docs/re/phase-180-linux-ebiten-router-draft.md`。
  這不是完整冷開機、正式中文覆繪生命週期或可玩版本的驗收。
- 後續 ignored row21 A000 觀測器以唯一 `[72,160)×[168,176)` 矩形雙重重播，
  找到 Enter 後普通回寫的首筆相交 pre-write：step `124800903`、`0763:184D`、
  像素 `(72,168)`；修正舊探針註解後再次重播 SHA 一致。原始檔與收據雜湊
  見[第一百八十三階段](docs/re/phase-183-post-join-exit-identity-corrigendum.md)。
  N／Y-Y 後續邊界與正式中文覆繪仍待驗，不因此升格 spec018。

## 2026-09-23 — 真實繁中作用層接入 host 視窗與 Exit 提示 DRAFT

- ignored Ebitengine caller 現在以正式通用 `frontend/ebiten.Game` 驅動已 READY 的
  首屏五行繁中 watcher；真實 X11 滑鼠完成設定、2×→3× Apply，期間原版連續
  推進 3904 instructions。程式內 2×／3× 私有 RGBA 與既有 CLI 收據逐位元組
  相等，詳細 SHA、來源與限制見[第一百八十五階段](docs/re/phase-185-ebiten-real-active-layer-router-draft.md)。
  這是從合法私有 checkpoint 開始的 DRAFT 原型，未收進正式玩家 launcher。
- Exit row21 與兩個提示另建可丟棄 typed／A000 探針；權威 fork 原始碼重跑仍與
  既有 runner 的停止點差六步，已保存[第一百八十四階段](docs/re/phase-184-exit-prompt-draft-prototype.md)
  勘誤與候選邊界，沒有把 DRAFT 翻譯塞進正式 catalog。

## 2026-09-23 — 校正翻譯目錄與前端規格的目前狀態

- `text/README.md` 的「post-join 選單尚未接 runtime」與「舊全選單 clear 屬 Exit」
  均與第一百八十二／一百八十三階段收據矛盾；已訂正為七列正式 runtime 局部 A/B
  通過、舊 clear 屬 row 12、真正 row 21 Exit 仍 DRAFT。
- spec004 末尾追加第一百八十五階段真實繁中作用層接入通用 Ebitengine Game 的現況，
  保留從私有 checkpoint 到正式可玩前端的未完成門檻，不回寫早期原型歷史。
- 在 Docker 內重跑 22 份正式 TSV 的字元聯集，與 `font/characters.txt` 完全相等，
  計 1028 字模；`tools/test_catalog_font.py` 14 項通過。第一次 unittest 指令因
  `PYTHONPATH` 未含 `tools` 而匯入失敗，明示環境路徑後在同一 image 重跑通過，
  非產品程式缺陷。
- 同一 Docker-only 邊界另以 `PYTHONPATH=tools python3 -m unittest discover -s tools
  -p 'test_*.py'` 重跑全部既有文字／幾何工具測試，240 項通過；這驗證工具內部
  自洽，不代表尚未接通的原版玩家路徑已中文化。

## 2026-09-23 — Exit 停止點控制組與冷開機前端 READY 缺口

- 同 fork／同 state／同 13 筆鍵盤步點下，A000 探針及原 text runner 都在
  `125006324` 停止，前者與既有收據相同、後者兩次逐位元組相同；
  step `125006323` 執行前為 `0CF4:0192`、`Exited=false`，執行後退出。
  因此六步差異不由 A000 observer 造成；舊 `125006330` 收據仍保留，
  其環境／產物來源未證實。詳見[第一百八十七階段](docs/re/phase-187-exit-stop-six-step-corrigendum.md)。
- 獨立前端稽核確認正式 `frontend/ebiten.Game` 只有視窗 loop，沒有 cold-boot
  composition root 或多作用層 owner；typed session、失敗邊界與正常玩家驗收
  矩陣見[第一百八十六階段](docs/re/phase-186-linux-ebiten-cold-boot-lifecycle-ready-gap-audit.md)。
  當時設定面板展開期間是否暫停 DOS CPU 尚未定案，未以原型現況冒充需求。
  使用者其後明確選定「開面板暫停 DOS CPU；關閉／Apply 收合後恢復」，
  排除原型持續 Step；已記入 spec004，後續需以有界回合實測。
- 代理初次離線前端測試缺 Ebitengine module cache；主代理沿用既有專用 image
  重跑，首次因沒有 `DISPLAY`／Xvfb 而使 GLFW 初始化失敗，加入有界 Xvfb 後
  `frontend/ebiten`、`host`、`presentation`、`apps/buckrogers` 四套 Go 測試
  全通。這是容器環境訂正，不是冷開機玩家路徑驗收。

## 2026-09-23 — 真實繁中視窗的面板暫停／恢復原型

- 在 ignored caller 增加獨立 `-router-pause-draft`，不改正式
  `frontend/ebiten.Game`。既有私有合法 checkpoint 的五行首屏繁中作用層透過
  真實 X11 點擊完成「開面板→暫選 3×→Cancel→重開→3×→Apply」；開面板
  89 個回合與兩次收合當回合均零 DOS Step，下一關閉回合各前進 16 步。
- 2×／3× 的 RGBA 均逐位元組等於既有 CLI 收據；完整 JSON 雜湊、來源 pin、
  step 錨點與停止線見[第一百八十九階段](docs/re/phase-189-ebiten-panel-pause-resume-draft.md)。
  本次未證實完整 DOS 狀態不變，也不是冷開機玩家前端或正式規格符合性。

## 2026-09-23 — 真正 Exit 提示的文字身分與多色尾碼

- 代理以固定 fork／私有加入角色 state，對 N 與 Y→Y 各重播兩次；兩分支收據
  各自逐位元組一致，退出步點重生為 `125006324`。兩個 row 24 提示的
  guarded identity、row21→提示及提示間的 A000 首筆相交寫入見
  [第一百八十八階段](docs/re/phase-188-exit-prompts-draft-evidence.md)。
- 可見六格選擇尾碼走另一條 glyph path，會依狀態多色／反白；因此沒有假定
  白色 Y/N，也沒有把提示加入正式 TSV 或 watcher。第二提示到 DOS 退出前
  未見自然相交清除，仍需終止清理與獨立 READY 審查。

## 2026-09-23 — 技能離開提示原文勘誤與正式前端 session 稽核

- 低階翻譯代理從本機原版 `GAME.OVR` offset 與事件 SHA 重新核實職業、
  技術技能兩句 Exit 確認提示，推翻前一輪「職業原句未知」；新 DRAFT
  譯文集中於 `text/skill-exit-confirmation.zh-TW.tsv`，未接正式 watcher。
  在 Docker 內 lint 通過；23 份繁中 TSV 的字元聯集仍逐 byte 等於現有
  1028 字模 `font/characters.txt`，不需為此換掉已釘選字型。
  原始定位與未驗邊界見[第一百九十一階段](docs/re/phase-191-skill-exit-confirmation-translation-draft.md)。
- 前端代理按固定 dosgolem fork API 審核冷開機 session：正式 `Game.Update`
  尚無 typed budget／step receipt／phase，單層 snapshot 也未聚合所有中文
  watcher，且缺 preflight／teardown；只寫 DRAFT 稽核，不改正式前端。
  代理使用的乾淨 Go 映像缺離線 Ebitengine module cache，未把 frontend 編譯失敗
  冒稱產品缺陷或通過；見[第一百九十階段](docs/re/phase-190-linux-frontend-session-ready-prerequisites.md)。
  主代理其後以既有 `eob-remake-go:1.26.7-ebiten2.9.9`、非登入 shell
  及有界 Xvfb 重跑 frontend／host／presentation／Buck Rogers 四套測試
  全通；已在同一研究文件追加環境勘誤，API 缺口仍在。

## 2026-09-23 — 加入角色後第七列的正式清層 A/B

- 沿同一合法 state 與十筆原版按鍵，在 row20 普通回寫前與返回後各取
  control、2×、3×收據，四個覆繪輸出又各重播一次，JSON／RGBA
  逐 byte 重生。兩停點三模式原版 JSON 逐 byte 相同；返回後的
  2×／3×覆繪 RGBA 均等於各自 baseline，證實這條固定分支
  回寫後不留七列繁中層。完整限制見
  [第一百九十二階段](docs/re/phase-192-post-join-menu-prewrite-runtime-ab.md)。
- 本機 dosgolem fork 新增雙倍率、同值 A000 pre-write 的 presenter
  清層回歸測試；定向與 `apps/buckrogers` 全套測試、vet 通過。
  CLI 不接受在 dispatcher pending 的單步停止點做成功收據，故未將
  回寫前／後兩張圖冒稱逐指令 active→empty 驗收。
- 首輪容器使用登入 shell 導致 Go 不在 PATH，改非登入 shell；後續
  嚴格 runner 拒絕停止點以後的鍵與大寫 scan hex，依原有十筆
  步點、兩位小寫十六進位重跑。這些是命令／環境錯誤，沒有改原版
  或放寬 watcher。Go module stat cache 權限警告非致命，測試仍通過。

## 2026-09-24 — 技能操作列英文尾字修正與限縮驗收

- 檢查正式 PNG 發現短譯文後仍殘留原版英文。於本機 dosgolem fork
  `674e3e3` 將操作列 presenter 改為先清除完整核准矩形，再畫白色
  助記字母與原版配色繁中；補正常／焦點 2×／3×、部分顯示群組
  失敗即關閉的回歸測試。
- 從同一合法 state 重播八條操作路徑及技術頁 Escape→Y；修正前
  runner 被英文尾段負控制拒絕，修正後乾淨建置的九條 control／2×／3×
  各雙重播通過原版 JSON、indexed 同狀態及安全矩形差分，離頁無殘層。
  正式 Go test、vet、race 與獨立審查通過；收據及未驗範圍見
  [第二百零四階段](docs/re/phase-204-action-bar-runtime-conformance.md)。
- Linux session 可丟棄 fake 另補同批 Open／Apply／Cancel＋Enter 負例；
  收合後下一關閉回合才恢復 DOS。這是 DRAFT 模型，不是正式前端
  完成收據，見[第二百零三階段](docs/re/phase-203-linux-session-mixed-batch-fake-review.md)。

## 2026-09-24 — 前端 session 故障後拒絕復活的 DRAFT 負例

- ignored typed fake 先成功前進七步，再分別注入 Deliver／Advance 故障；
  後續 Open＋DOS 候選鍵遭拒、兩次重試零步且 epoch 不變，重複 Close
  副作用恰一次。Docker 內五組 fake 測試全通過；見
  [第二百零五階段](docs/re/phase-205-linux-session-failed-close-once-fake.md)。
- 這只是可丟棄模型。Snapshot／Draw／observer、真實 DOS 指令數、
  cold boot 與資源收束未接；規格 004／019 均維持 DRAFT。

## 2026-09-24 — machine 步數與停止原因最小實驗

- 獨立審查指出 session fake 把 epoch 直接加 budget，不能代表真實
  machine 指令差分。在 ignored dosgolem `workplace/` 建立合成 COM
  可丟棄探針，Docker 唯讀雙重執行結果逐位元組相同：零預算零步、
  預算耗盡兩步、條件／斷點兩步早停、未實作指令在第二次 Step 回錯。
- 最重要的勘誤是錯誤案例仍回原始 `StopBudget`，但非空 error 應
  優先分類；`m.Steps` 已計入失敗嘗試。詳見
  [第二百零六階段](docs/re/phase-206-linux-session-machine-step-delta-draft.md)。
  規格 019 只補 DRAFT 收據，不升 READY，不改正式前端。
- 曾嘗試讀取既有冷開機原版 PNG 供視覺檢查；權限審查因完整受限
  影像會進入工具通道而拒絕。未改以其他通道繞過，該張圖未作本輪
  視覺證據；步數實驗使用無原版素材的合成 COM，與此限制無關。

## 2026-09-24 — 前端回合六階段故障 fake

- 在既有 ignored session fake 旁新增 `TurnFake` 與測試，驗證面板開啟時
  零 fake DOS 步而 host 畫面繼續更新、Snapshot 純讀、六階段各別故障後
  不再執行後續階段／不復活，以及 Close 副作用一次。
- 唯讀、無網路 Docker 中以 Go 1.26.7 執行 `go test -count=1 -v ./...`，
  八組頂層測試全通；來源雜湊、限制與重生條件見
  [第二百零七階段](docs/re/phase-207-linux-session-six-stage-fault-fake.md)。
  正式 Draw 故障回報、實際 machine 步數與冷開機未由此驗收；規格 019
  維持 DRAFT。原型沒有原版素材，未改 production。

## 2026-09-24 — 原版冷開機至繁中選單的靜態視窗原型

- 代理在 ignored `workplace/cold-boot-frontend-proto/` 從 `START.EXE` 第零步
  建立 DOS、先安裝選單 watcher，再用既有輸入於 1 億步界線內到達已量選單。
  原版唯讀、scratch 獨立可寫；Ebitengine／Xvfb 將預先算好的 2×繁中
  終態繪出三幀。缺字零，watcher misses 24；收據見
  [第二百零八階段](docs/re/phase-208-cold-boot-menu-ebiten-prototype-draft.md)。
- 主代理以唯讀 Docker 核對來源、收據雜湊與安全統計，未做第二次完整
  冷開機重播，也未把原版影像傳入工具通道。原型尚無 live DOS 視窗回合，
  未改正式程式，不作 READY／可玩完成聲明。
- 本輪專用映像的執行中／已停止容器清單為空；兩個本輪研究工作目錄均無
  root-owned 檔案或誤建的 `.md` 目錄。私有 `out/`／`scratch/` 留在 ignored
  `workplace/`，未加入版控。
- 規格 019 經子代理獨立唯讀審查仍判 DRAFT：事件順序、實際步數／停止
  原因映射及正式 Draw 錯誤回報三項仍缺明確可實作契約。已委派合成
  machine 的補證切片；不以靜態冷開機畫面代替 READY。
- 主代理唯讀核對本機 fork `frontend/ebiten/game.go`：`Draw` 的三個可檢查
  錯誤會鎖在 `Game.err`，下次 `Update` 可阻止推進；但 session owner
  未同步收到 Failed／Close。已把這個 DRAFT 邊界補進規格 019，
  未直接改正式前端。

## 2026-09-24 — 冷開機後真實視窗回合的 DOS 暫停／恢復

- 代理另建 ignored live-turn 原型，不動釘選的靜態原型或正式程式。
  原版從第零步到已量選單後，正式 `frontend/ebiten.Game.Update` 每個
  關閉面板回合讓同一 machine 增加 16 步；實體 X11 點擊 Open、
  持續展開、Cancel 收合當回合零步，下個關閉回合恢復 16 步。
- 主代理唯讀 Docker 核對原型／收據雜湊、步數與工作目錄擁有權；
  完整數值與限制見[第二百零九階段](docs/re/phase-209-cold-boot-live-ebiten-panel-pause-draft.md)。
  首輪舊 host 字型缺 `×`，改用已驗 current-font 後成功；未做 3×、
  同狀態 A/B 或存讀檔，規格 004／019 仍 DRAFT。

## 2026-09-24 — DOS 退出與停止收據合成補證

- 子代理以合成 COM 量到：DOS 正常退出仍可回 raw `StopBudget`；
  正預算呼叫對起點已成立的 predicate 會多嘗試一步，CPU error
  也可與 raw `StopBudget` 並存。主代理在唯讀無網路 Docker
  另從新路徑重跑一致；表格與輸入版本見
  [第二百一十階段](docs/re/phase-210-session-stop-receipt-probe-draft.md)。
- 新實驗曾覆寫 phase206 已釘選的 ignored 原始來源。發現後用
  `apply_patch` 將新探針分開存放，舊檔 SHA-256 已精確恢復為
  `4edf58d7cd13aef2bca7c9a686b523c844680730e69b4efd1f70e69b1d935bda`；
  主代理再次獨立核對。這次只補現行 API 證據，未決定正式
  receipt 政策或改 production。
- 本批 Docker 結束後專用映像容器清單為空；live-turn、phase206、phase210
  工作目錄沒有 root-owned 檔案或誤建的 `.md` 目錄。私有收據與
  scratch 均留在 ignored `workplace/`。

## 2026-09-24 — 合成 typed session 收據候選

- 子代理在全新 ignored phase211 原型中，以退出前置檢查、Step
  差分、error 優先及原始停止碼保存組成候選收據；合成 DOS 退出、
  CPU error、predicate／breakpoint、零預算兩方案與兩種 epoch
  候選量均有負例。主代理以唯讀無網路 Docker 獨立重跑五組測試全通。
  證據與未定契約見[第二百一十一階段](docs/re/phase-211-synthetic-session-receipt-candidate-draft.md)。
- 本批未更動 phase206／phase210 釘選探針或正式程式；零預算／Epoch
  不因 fake 綠燈而被默認決定，規格 019 繼續 DRAFT。

## 2026-09-24 — 3× host 倚天字型視覺前置

- 在未載原版的唯讀 Docker 中，既有 `psychic-war` ETUNPACK 工具成功
  解出本機倚天 24 點明體 13,094 字；面板六個中文字元與數字／符號
  都有原生字模。九種 24→22 直接裁切全會損墨點，因此不能把
  22×22 validator 與原生 24 點素材硬湊成已完成 3× Apply。
- ignored host-only A/B 將原生 24 點與原型衍生 22 點並列，九字零缺字、
  五項控制項均無越界。主代理核對本機輸入、工具、收據及 PNG 雜湊；
  未把字型或影像送入工具通道，未改 production。證據及選擇停止線見
  [第二百一十二階段](docs/re/phase-212-host-only-3x-eten-font-ab-draft.md)。
- 本批專用 Docker 映像的容器清單為空；兩個字型研究工作目錄沒有
  root-owned 檔案或誤建 `.md` 目錄。產生的字型／PNG／收據均只在
  ignored `workplace/`，不進 GitHub。

## 2026-09-24 — 面板暫停確認與真正 Exit 問句前置

- 使用者確認設定面板開啟時暫停 DOS；既有正式 `Game.Update` 的局部
  CONFORMED 排程與專案規格已採相同語意。主代理以無網路 Docker／
  有界 Xvfb 重跑 `frontend/ebiten` 測試通過；這不是完整玩家前端。
- 翻譯代理盤點 23 份繁中 TSV、194 筆資料列（手冊 39 筆），現有
  catalog、選單與手冊檢查通過；穩定 key 無安全漏譯。真正 Exit 問句
  另建 GitHub #19，依賴 #8；不把 DRAFT identity 猜成正式 catalog。
- [第二百一十三階段](docs/re/phase-213-exit-prompt-font-draft.md)固定兩句
  DRAFT 用字並驗倚天 2×／3× 靜態墨跡及原版尾碼保護區；
  [第二百一十四階段](docs/re/phase-214-exit-prompt-body-lifecycle-fake-draft.md)
  的 ignored 模型補上兩層短暫共存、含同值首寫與未知 writer 負例。
  主代理審查時發現第二問 Entry 其實早於第一問清層，已訂正原型並
  補 Return-before-clear 負例；唯讀 Docker 重跑七組頂層測試通過。
  兩者仍不授權 production。
- [規格 021](docs/spec/021-post-join-exit-prompt-body-only-draft.md)已把兩句
  問句本體的 exact 身分、原版多色尾碼零覆繪、失效與終止條件寫為
  DRAFT，並掛入現有規格索引。獨立審查先抓到 row 21 Enter 上下文未在
  fake 建立；再次核對專案原文＋callsite＋座標辨識原則後，將其保留為
  已驗來源路徑，不設成 watcher 必需 guard。此限縮不改原版判定，
  [第二百一十五階段](docs/re/phase-215-exit-prompt-body-ready-review.md)
  因而只核准兩句本體為 READY。正式 watcher／TSV 與原版 A/B 尚未做。
- 另一個 ignored 2× 冷開機原型同時接選單與手冊 watcher，但本次只
  觸發選單、手冊事件為零；故不是多層呈現驗收。限制已回填 Issue #16。

## 2026-09-24 — 真正 Exit 問句本體正式雙倍率對拍

- 使用者確認設定面板展開期間暫停 DOS；先前正式 `Game.Update`
  雙倍率暫停排程已限縮驗過，但完整 Linux 可玩 session 仍未完成。
- 真正 row 21 Exit 的兩句繁中問句新增正式 TSV 及 dosgolem
  watcher／presenter，只覆繪 row 24 本體並保護六格原版多色尾碼。
  完整字型與原版素材均留本機 ignored `workplace/`。
- 首次正式 A/B 的 q1／N 暫時綠燈被下七列正常 `0763:1854` 寫入推翻；
  撤回舊結論後，先以[第二百一十六階段](docs/re/phase-216-exit-q2-glyph-writer-draft-corrigendum.md)
  首列勘誤及[第二百一十七階段](docs/re/phase-217-exit-prompt-full-body-writer-review.md)
  可重生八列雙重原版收據補證，再限縮修訂規格 021，沒有直接加全域
  writer 白名單。正式 watcher 的相交判定由首列修成完整八列。
- [第二百一十八階段](docs/re/phase-218-exit-prompt-runtime-ab.md)的
  24 份啟用 FileOps 追蹤的控制組／2×／3× 雙重端點收據，及六份
  N／Y→Y／Stop 正式生命週期軌跡，均逐位元組可重播。主代理與獨立
  審查核對原版記憶體、畫面、鍵盤與零筆 FileOps 自證；兩句中文 RGBA
  差異只在本體，N／退出無殘層，q2 Entry 與 q1 active 交疊、同值
  A000 首寫失效、q2 guarded Return 及 Stop 均由正式 hook 證實。
  主代理在唯讀、無網路 Docker 獨立重跑 Go app／receipt 測試通過。
- 因此規格 021 只對此固定合法加入角色存態的 N／Y→Y、雙倍率無頭
  路徑及已量生命週期限縮升 CONFORMED；Restore 後重入、其他玩家
  路徑、存讀檔與 Linux 實體視窗仍未驗。私有完整收據及字型未加入
  Git 或 GitHub。dosgolem workplace 分支已於本地提交 `a01e342`，
  未推送其遠端；主專案 private `main` 已提交並推送 `78e05f4`。
  GitHub Issue #19 已追加限縮範圍並以 completed 關閉；較廣的中文化、
  Restore 與 Linux 玩家視窗仍由其他 Issue／規格追蹤。
- 本輪結束核對 `docker ps -a`：所列容器皆屬其他專案，沒有本專案
  執行中或已停止容器；Docker 內掃描工作樹無 root-owned 產物或
  誤建 `.md` 目錄。完整原版輸入、字型、RGBA 與私有收據仍留 ignored
  `workplace/`，未推送遠端。

## 2026-09-24 — 面板暫停重申、session READY 前補證與第九頁勘誤

- 使用者再次定案：設定面板展開時暫停 DOS，Cancel／Apply 收合同回合
  仍零步，下一個關閉回合恢復。唯讀核對正式 `Game.Update` 與
  [第一百九十四階段](docs/re/phase-194-formal-ebiten-panel-pause-conformance.md)：
  此規則已有 callback 排程的限縮 CONFORMED，並非完整可玩版。
- [規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)
  收斂成 session-turn 限縮 READY 候選。獨立審查發現原 fake 的 epoch
  對暫停回合不增，且 pointer／keyboard 尚無整批純資料預檢；
  [Issue #18 審查紀錄](docs/re/issue-18-session-turn-ready-candidate-review.md)
  保留此阻塞與 `phase193` 正確 Docker 掛載勘誤。ignored fake 隨後補驗
  成功批次 epoch 遞增、零預算拒絕、單次 `Advance` 及混合輸入原子拒絕，
  有界無網路 Docker 的 fake 測試通過。仍缺同一 typed owner 的真實
  machine 收據與正式橋接提交驗證，未改 production、未升 READY。
  主代理獨立重跑時，首個容器因未指定 Go 快取目錄而遭唯讀權限拒絕；
  改依審查文件指定可寫 `/tmp` 與既有 Ebitengine 映像，以同一 fake
  測試乾淨重跑通過。此為驗證環境設定錯誤，不是產品失敗。
- 新建 private GitHub Issue #20 追蹤第九頁固定單行，
  [規格 022](docs/spec/022-story-page9-overlay-draft.md)與索引已建立。
  合法 page8→page9 Docker 重播推翻初稿「所有相交 A000 寫入皆清 pending」：
  原版 20 個 glyph frame 內有 1,280 筆相交 pre-write，每格 64 筆；
  已在[第一百三十四階段勘誤](docs/re/phase-134-story-page9-enter-trace.md)
  保留原錯誤與新證據。候選規格區分建構中預期字格寫入與 active 後清層；
  私有倚天字型在正式 renderer 的 2×／3× 本體幾何零越界，catalog 六項
  測試通過。自然離頁與正式 A/B 未驗，TSV 仍 DRAFT、規格仍待獨立審查。
- 修正規格索引的 021 過時 READY 說法，與既有固定 N／Y→Y 路徑
  限縮 CONFORMED 結論一致。本批未提交原版素材、掃描手冊、字型或
  私有收據；主專案 private `main` 已提交並推送 `7118d73`。
  交接前 `docker ps -a` 無本專案容器，工作樹無 root-owned 產物或
  誤建 `.md` 目錄；其他專案容器未動。

## 2026-09-24 — 第九頁正式入頁對拍、前端批次契約與 A 字型選擇

- 使用者重申設定面板展開時暫停 DOS；既有正式 `Game.Update` 僅對
  callback 排程限縮符合，完整 DOS state／session 尚未完成。
- Issue #18 的 ignored typed owner 已接真實合成 COM `Machine.Steps`
  差分。真實 bridge 負例發現直接提交 canvas Down 後遇非法 Apply
  會留下 DOS 左鍵；規格 019 與審查紀錄補上整批純路由預檢、
  不可變 DOS action 清單、來源狀態核對及正反例矩陣。
  正式橋接未改，規格仍 READY 候選。
- 規格 022 經獨立審查只將第九頁固定入頁單行升限縮 READY，
  TSV identity 同步標 READY。dosgolem fork 新增正式 watcher、
  catalog、presenter、owner 與 CLI 接線；[第二百一十九階段](docs/re/phase-219-story-page9-runtime-entry-ab.md)
  的 control／2×／3× 私有同狀態收據中，machine snapshot、DOS、
  indexed 及正規化 metadata 一致，中文字像素只在核准矩形。
  主代理另以唯讀 Docker 重跑 Go 測試、`go vet`、私有存態讀回及
  逐像素檢查。首次私有測試漏掛既有 `/orig/GAME.OVR` 而在還原前
  失敗，補上唯讀原版目錄後原樣比較通過，屬容器設定錯誤。
  自然離頁與清層後畫面仍未量，Issue #20 保持 OPEN，規格不升
  CONFORMED。已驗 page9 正式程式在本機 dosgolem fork 分支提交為
  `7930b7a`；未推送 dosgolem 遠端，ignored 原版探針不入版控。
  後續以同一合法第九頁存態，對手冊明示前進 8／後退 2 各雙重
  有界重播到 `370000000`：兩鍵被讀取、均無故事矩形 pre-write、
  故事像素變化或 DOS 結束。達硬停止線即止，不擴新鍵位；
  真實出口與清層後 A/B 仍待正常玩家流程或來源證據。
- 使用者看過 A／B 圖後選 A 原生倚天 24 點、排除 B 衍生 22 點。
  主代理獨立核對原型收據與正式字型 API，僅將規格 004 的 3×
  host 字型子契約限縮升 READY；整體前端仍 DRAFT，正式字型
  接線與實體 3× Apply 另行驗收。原版、已購字型、PNG 與完整
  私有收據均留 ignored `workplace/`，不送 Git／GitHub。

## 2026-09-24 — A 原生字型正式畫筆與版控重建入口

- 本機 dosgolem fork `cc0b17a` 將 3× 設定面板改成原生倚天
  Wide 24×24＋ASCII 16×24 typed 字型；2× 16×16 既有畫筆保留。
  合成 Game.New 負例、2×→3×→2×、Draw 缺字後阻止下一回合
  DOS 輸入／步進均通過。使用本機私有 A 子集的真實
  Ebitengine／Xvfb `RunGame` 讀回 RGBA，五個標籤像素逐點符合
  字模，22 點裁切界外的 102 個墨點仍在；切回 2× 的 1,116,160
  bytes 畫面全同。主代理另以唯讀 Docker/Xvfb 獨立重跑
  `frontend/ebiten` 全套測試與 `go vet` 通過。
- 新增不含字模的[版控抽字工具](tools/eten_host_font3.py)及合成
  測試，四份本機來源先鎖 SHA-256，輸出限定 ignored `workplace/`
  並在失敗時保留舊三檔。主代理以唯讀原始倚天與解壓器、只寫
  ignored 輸出目錄獨立重建，Wide／ASCII 字型及 manifest SHA
  與[第二百一十二階段](docs/re/phase-212-host-only-3x-eten-font-ab-draft.md)
  新收據一致；專案工具測試 247 例通過。字型、衍生 GOLEMFNT、
  圖片與原版仍不入 Git。
- 以上是 host-only 限縮實作與畫面收據，沒有正式 cold boot 玩家
  入口、原版 DOS raw／BIOS／IRQ／存檔同狀態 A/B，故規格 004
  整體 DRAFT，3× 字型子契約保持 READY、不升 CONFORMED。
- 本輪主專案 private `main` 先後提交並推送 `2396a76`（第九頁
  入頁收據、session 契約與 A 決定）及 `6eba525`（A 字型重建
  工具與正式畫筆收據）；Issue #20、#18、#16 均已追加限縮
  進度，保持 OPEN。dosgolem workplace 分支本地提交 `7930b7a`
  與 `cc0b17a`，未推送其遠端。三個一次性第九頁 probe Go 檔
  仍在 fork 工作樹未追蹤，未納入提交；原版、已購字型、
  GOLEMFNT 子集及完整收據均在 ignored `workplace/`。
- 結束檢查 `docker ps -a` 僅見其他專案容器，本專案無殘留；
  Docker 內掃描本工作樹無 root-owned 產物或誤建 `.md` 目錄。

## 2026-09-24 — 正式譯文與下一個未譯輸出盤點

- 唯讀盤點 `text/`：目前有 24 份 `*.zh-TW.tsv`；固定劇情首屏至第九頁
  共 42 筆 READY identity。`CONTEXT.md` 的現況計數由 23 訂正為 24；
  `font/README.md` 的第一百九十一階段 23 份收據保留其歷史語境。
- [規格索引](docs/spec/README.md)顯示首屏至第八頁僅各自已量路徑
  限縮 CONFORMED；第九頁只有合法入頁固定單行限縮 READY，未量
  自然離頁。手冊、建角、技能及加入角色後介面各有譯文與不同的
  限縮驗收範圍，不能將 TSV 存在等同整段玩家流程已中文化。
- [第一百三十六階段](docs/re/phase-136-story-page10-enter-stop-line.md)
  的合法第九頁後 Enter 雙重重播只量到 row 15、column 17 的
  12-cell 命令／狀態列六次重畫，六筆原文雜湊不同，沒有新的固定
  故事 glyph；[第一百一十](docs/re/phase-110-command-status-inventory.md)
  與[第一百一十二階段](docs/re/phase-112-command-turn-manual-evidence.md)
  的更早 row 24 命令／狀態列也未拆出固定詞與動態欄位。兩者均無
  READY 翻譯契約，本輪未新增 TSV、譯文或第十頁故事候選。下一步
  只需以既有合法玩家狀態取得可比的不同命令／狀態輸出，私下逐格
  分離固定與動態部分，再補原文 identity、覆繪／清除邊界及規格審查；
  不延長第九頁按鍵探針或猜測原文。
- 在有界、無網路、唯讀 Docker 中執行
  `python -m unittest discover -s tools -p 'test_story_page*_catalog.py' -q`：
  50 項通過；逐檔讀取 24 份 TSV 的 196 筆譯文，抽出 1028 字模，
  與 `font/characters.txt` 逐 byte 相同。這些只驗 catalog／字型清單
  自洽，非 row 15／24 的原版對拍。
  本輪不修改 dosgolem fork、原版素材或私有字型，不提交或推送；
  `docker ps -a` 無本批一次性容器，工作根未見 root-owned 產物或
  誤建 `.md` 目錄。

## 2026-09-24 — Issue #18 同批輸入後段錯誤反證

- 於 ignored dosgolem fork 新增專用合成負例：真正 `Game.Update` 同批先送
  canvas Down，後段鍵盤因未設定 BIOS transport 回一般錯誤，DOS 左鍵仍
  留在按下狀態；BIOS pending、`Machine.Steps` 與 `Advance` 均為零。
- 已在 [Issue #18 審查紀錄](docs/re/issue-18-session-turn-ready-candidate-review.md)
  保存測試名稱、檔案雜湊、限制與下一步。唯讀 Docker／Xvfb 中
  `go test -count=1 ./frontend/ebiten`、`go vet ./frontend/ebiten` 通過。
  規格 019 仍為 READY 候選，不據此修改 production 或宣稱可玩。

## 2026-09-24 — Issue #16 多作用層合成 DRAFT 補證

- 本機 dosgolem fork 的 ignored `presentation/composite_draft_test.go`
  建立僅測試用、單次 indexed／palette 讀取的兩層合成候選；2×／3×
  固定 z-order、原 layer bytes 不變，以及缺群組、重複 slot／z、過期
  generation、缺字、壞字模長度與 stamp 越界的拒絕矩陣通過。
- 獨立審查指出 manifest 仍由呼叫者自報、generation 未綁正式 owner；
  `xlate.Draw` 原本也不檢查字模長度與 stamp 幾何。已在測試用 evaluator
  補上繪圖前檢查，但正式 provider／session 未改。證據與下一個
  READY 切片記於[第二百二十階段](docs/re/phase-220-linux-active-composite-draft.md)。
- 既有鎖版 Docker image 中 `go test -count=1 ./presentation` 與
  `go vet ./presentation` 通過。這不含原版遊戲、手冊、字型、
  真實 presenter 並存或玩家路徑；規格 004 仍 DRAFT。

## 2026-09-24 — Issue #18 純資料路由原型

- ignored `frontend/ebiten/route_plan_candidate_test.go` 以值狀態先規劃
  同批 host／滑鼠／鍵盤動作，測得 Down 後非法 Apply、缺 BIOS
  transport、過期 Up 的整批拒絕，以及合法轉送與真實 bridge 同值。
- 正式 bridge 缺完整 `pressedEpoch` 快照、真實一致來源 token 與不可再失敗
  的提交 API；已補入[Issue #18 審查紀錄](docs/re/issue-18-session-turn-ready-candidate-review.md)。
  Docker／Xvfb 的 frontend 全套測試與 `vet` 通過；規格 019 仍為 READY
  候選，不把測試用原型接進 production。

## 2026-09-24 — Issue #8 命令／狀態列欄位有界原版探針

- [第二百二十一階段](docs/re/phase-221-command-status-columns-draft.md)以
  原版 `GAME.OVR`、兩份既有合法私有 state 及 ignored probe，重生
  row 15 六筆、row 24 Enter 一筆與數字鍵盤 4／6 兩筆；只輸出整串
  SHA、欄位相等遮罩、caller／step、原版 clear 與 A000 writer，不輸出
  原文或可還原畫面。
- row 15 的 12 格在六次同態重畫中第 0 格變動、1–11 格相同；row 24
  的 21 格 dispatcher 與 33 格直接 glyph 是不同路徑，右側 col33..39
  clear 不可冒充 0..32 本體清除。三條 probe 在有界 Docker 通過。
- [規格 023](docs/spec/023-command-status-overlay-draft.md)保持 DRAFT：
  跨狀態固定詞、詞界、完整失效與雙倍率安全矩形未證，故未新增 TSV、
  watcher 或第十頁故事候選。第一次 probe 少掛原版檔是環境設定失敗，
  已核對唯讀來源後以相同停止線重跑通過。

## 2026-09-24 — 3× 原生字型回歸與前端 READY 缺口

- 依使用者選定的 A 方案，在既有有界、無網路 Docker／直接 Xvfb 重跑
  `TestNativeHostFont3` 四組測試；正式畫筆的五標籤像素數為
  334／135／132／356／366，原生 24 點有 102 個墨點位於 22×22
  裁切邊界外，2× 往返 1,116,160 bytes 完全相同。第一次使用
  `xvfb-run` 因 image 缺 `xauth` 而未啟動測試，改由容器內有界
  Xvfb 與 trap 清理後通過；這是驗證環境問題，不是產品缺陷。
- 正式手冊 presenter 的合成雙層測試揭露 3× 衍生字型未命名，
  目前單層 snapshot provider 會拒絕；測試內命名及登錄後可重現
  presenter 的 RGBA。獨立審查又指出測試用合成器的 nil stamp
  可 panic，manifest／generation 無正式 owner 保證；[第二百二十階段](docs/re/phase-220-linux-active-composite-draft.md)
  已標明限制，不升 READY。
- Issue #18 的 ignored session／route 原型新增完整值 ABA 與外層
  source token 可繞過負例；規格 019 與審查紀錄保留共同 owner
  候選，未動 production、未升 READY。
- Issue #8 以手冊成功返回與第九頁後兩個合法進度雙重播 row 15，
  確認同 caller／位置有不同身分，但沒有可核准固定英文詞界；
  row 24 仍只有各自單一身分。phase221／規格 023 保持 DRAFT，
  不新增 TSV 或正式 watcher。

## 2026-09-24 — 3× 面板 A 決定與 BIOS 前檢限縮實作

- 使用者選定 3× host 設定面板使用倚天原生 24 點 A 版，排除衍生
  22 點 B 版；正式 `HostFont3` 路徑原已接通，遊戲畫布字型不變。
  本機忽略工作區的私有子集重跑正式 Ebitengine／Xvfb 實體像素
  測試：五標籤墨點數 334／135／132／356／366，原生 24 點在
  22×22 裁切界外保有 102 點，2× 往返 1,116,160 bytes 相等。
- fork 規格 233 經 READY 與獨立實作審查後，正式補上 BIOS 鍵盤
  建構／回合／交付前檢，修正缺 BIOS 或 `DOS.M` 已改指他機時
  的部分副作用入口；單元、`vet`、競態測試通過，規格僅限縮
  CONFORMED。修正前反證保留為不編入測試的 `.go.txt`。
- [Issue #18 審查紀錄](docs/re/issue-18-session-turn-ready-candidate-review.md)
  已追加驗收與停止線。規格 019 的整批路由、session owner、
  正常玩家路徑仍未完成，不宣稱 Linux 可玩版已完成。

## 2026-09-24 — 手冊首題 owner 原版收據與字型唯讀核驗

- `tools/eten_font.py verify` 使用全部 24 份正式 TSV、固定 SHA-256 的三個
  倚天來源，唯讀重算本機 GOLEMFNT 及 sidecar 並逐 byte 通過：1,028
  字模，字型 SHA-256 `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`。
  15 項合成測試涵蓋 catalog／字模／sidecar／來源變動拒絕，不寫輸出。
  正式 Linux session 尚未呼叫此入口；用法與邊界記於[規格 008](docs/spec/008-eten-top-pad-local-font-builder-draft.md)。
- 子代理用正式原版 runner 的首題固定 state，重播 control／2×／3×，
  memory／indexed／palette／DOS state 相同；再把 begin／clear／request
  收據與終態影格交正式 `ManualSnapshotOwner`。主代理在唯讀 Docker
  獨立重跑 2×／3×：owner 與正式 presenter RGBA 逐 byte 同值，僅
  `[7,312)×[72,184)` 內分別變更 3,776／6,591 像素，外側零；
  owner 前後 machine／DOS state 相同。第一次漏掛 `/orig` 導致
  `GAME.OVR` 還原失敗，補上已驗來源唯讀掛載後同測試通過。
  私有檔案僅在 ignored `workplace/manual-owner-oracle-20260924/`；
  [規格 024](docs/spec/024-manual-layer-group-font-identity-ready-candidate.md)
  保持限縮 READY，不能推定正式 Linux 直播接線或其他 38 題完成。
- 另一子代理以正式 `Game.New`／`Update` 證實同批滑鼠與鍵盤可指向
  不同 DOS，或在回合前檢後改 `DOS.M`，使鍵盤拒絕前留下左鍵與座標。
  主代理在唯讀 Docker／Xvfb 獨立重跑兩個合成負例及 `go vet` 通過。
  [規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)與
  [Issue #18 審查紀錄](docs/re/issue-18-session-turn-ready-candidate-review.md)
  已補共同 DOS／machine 身分及提交排他性停止線，未改正式回合，
  Issue #18 繼續開放。

## 2026-09-24 — 原版選單 3× 實體切換與字距原型

- 原版冷開機功能選單在實體 Ebitengine 視窗完成 2×→3× Apply；
  A24 host 設定面板的本機像素測試通過，舊 22 點面板輸入會被正式
  驗證閘門拒絕。面板開啟期間 DOS 零步，收合後恢復。
- 遊戲畫布另以目前 16 點與可丟棄衍生 22 點 A/B：六筆 active
  主選單在核准矩形外零差異；九個 `function.menu.*` 變體通過
  合成字寬、字色、缺字與 ASCII 像素不變檢查。這不是正式
  3× 畫布字型變更，也不是其他選單的動態重繪驗收；
  [第二百二十二階段](docs/re/phase-222-original-menu-3x-typography-draft.md)維持 DRAFT。
- Issue #18 的共同 DOS／machine、generation、一次提交合成 owner
  測試與 `go vet` 通過；正式 bridge 仍可遭外部 `DOS.M` 改指，
  規格 019 保持候選，不能宣稱 Linux session 已完成。

## 2026-09-24 — 原版選單動態字距與手冊首題實體視窗

- 子代理從已驗原版選單 state 送 Down→Up，量到 normal／selected
  四筆精確 post-call；主代理在唯讀 Docker／Xvfb 獨立重播通過。
  兩個停點 2× 候選與正式 16 點逐 byte 相同，3× 22 點候選的
  改動限核准文字矩形；正式程式未改，送限縮 READY 審查。
- 原版手冊首題終態與 formal begin→clear→request 值由正式
  `ManualSnapshotOwner` 交真正 Ebitengine 視窗，實體 Apply 後
  2×／3× 分別有 39／15 張逐 byte 等於舊收據的畫面，原版
  indexed／步數不變。初看像殘字的 `RAM` 等英文字母，其實在
  正式繁中 TSV 裡；已訂正誤判，留下四版私有排版原型，專名
  取捨待使用者答覆。[第二百二十三階段](docs/re/phase-223-manual-first-question-host-mixed-script-draft.md)
- #18 獨立反例確認：合成 owner 禁止自身 rebind 仍擋不住
  公開 `DOS.M` 在提交區間改指，滑鼠與 BIOS 鍵可分流；規格 019
  不升 READY，不以一次預檢冒稱原子性。

## 2026-09-24 — 十鍵字距原型與手冊譯文校訂

- 子代理新增 #16 ignored 十鍵路由／字型身分與 builder 失敗矩陣，
  主代理逐行審閱並在唯讀 Docker／Xvfb 獨立重跑通過。原型證實
  21 事件中僅十鍵的 3× 可限縮，2× 與 race 不變；現行 builder
  接受未引用的壞字模及 4×，未預檢整套衍生會 panic。保持 DRAFT，
  未改正式 dosgolem 分支。
- 翻譯稽核子代理檢查 24 份繁中 TSV／196 筆，確認結構與事件覆蓋，
  主代理只修四處義務語氣「必需」及一個多餘「處」。手冊 39 題
  catalog／504 字容量及 11 個單元測試通過；依全部正式譯文重建
  本機 ignored 倚天字型與 manifest，唯讀 `verify` 通過，
  1,028 字模／GOLEMFNT SHA-256 保持不變。新版
  `text/manual.zh-TW.tsv` SHA-256 為
  `dbdeb6f476502a04e65d825e5f2dff60d466f972b664f303dffd3c3ef9681eb2`，
  本機 manifest SHA-256 為
  `10717ce16a85db92e8630114b7868c75818f7ac8e5540ea11608d0e1d8baa405`；
  兩個私有字型產物都留在 ignored `workplace/current-font/`。
- 訂正 `text/README.md` 的選單事件數、Exit 問句與第九頁舊狀態
  描述；正式譯文專名與尚無充分來源的風格建議均未擅改。
- 獨立 READY 複審發現原 DRAFT 混淆單次 builder 與逐事件 runtime，
  且普通 `xlate.Layer.Restore` 不驗字型指標／指紋。規格 004 已補
  canonical `MenuCatalog.Resolve`、逐事件失敗上送及同 session
  封存 owner 邊界；僅十鍵 3× 畫布字模子契約限縮升 READY，
  正式程式與原版同狀態驗收仍未完成。
- #18 的 ignored callback 反例由主代理在唯讀 Docker／Xvfb 獨立
  重跑五項定向測試與 `go vet` 通過：同一 DOS 指標仍可因公開
  `DOS.M` 改指，把 move／press callback 及 BIOS key 分流；
  逐 action 補檢只會在已有 DOS 副作用後晚拒。規格 019 仍 DRAFT，
  不把合成反例當成原版發生過的事件。
- #16 的正式 scoped runtime 四檔已由主代理逐行審查，在唯讀 Docker
  重跑定向測試、`apps/buckrogers` 與文字收據工具全測試、`go vet`
  通過；本機正式 21 事件 2×／3× 分流及 22 點字型指紋驗證通過。
  原版同狀態與實體視窗回切另驗，尚不升 CONFORMED。
- #18 子代理的私有目標 session 可丟棄原型及公開別名反例，由主代理
  逐行審閱並在唯讀 Docker／Xvfb 重跑六項定向測試、`go vet` 通過。
  它只支援 Down＋Enter 合成批次，正式 `Game.New(Config)` 尚不具備
  同等排他性；規格 019 維持 DRAFT。
- #16 dosgolem 本機分支 `3b02f88` 提交正式十鍵 scoped 3× 程式。
  ignored 原版同狀態測試 SHA-256 `eabaab5367bfbd30c182c957e609d5c1e2aeb3f4372bbadf3194219e5e5e1790`
  由主代理獨立重跑通過：Down／Up 四模式原版 indexed／palette／
  step 同值、2× 舊新 RGBA 相同、3× 差異限作用中安全矩形。
  舊／新 CLI 3× 同因停點 layer pending 而 `drew=false active=3`；
  無 CLI 覆繪收據，真正視窗回切未驗，保持限縮 READY。
- 較輕量子代理第二輪唯讀校對 24 份正式 TSV；主代理修正手冊
  第 18 段病句。「直昇機」及「船體維修」的正式畫面名稱有中文
  手冊來源約束，未僅按現代寫法或手冊規則段落的詞面一致性改動。
  逐檔 TSV
  lint、手冊 39 段／504 字容量、相關單元及職業技能矩形測試通過。
  本機私有倚天字型由全部 24 catalog 重建再 verify：1,028 glyph，
  GOLEMFNT SHA-256 保持 `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`，
  新 ignored manifest SHA-256 為
  `459adb3d4cf49bbc36aca06902a2729d5b9cc61c19979343a9652bbd04eeb7eb`；
  新 `text/manual.zh-TW.tsv` SHA-256 為
  `9958e4d6255276d8646849ae2e4d46c650f5c75d06e2775e18b5a32eab65fbef`。
- #16 的 CLI 終態錨定 ignored 原型由主代理獨立重跑舊／新 3×
  通過：`Pending` 的三筆文字在相同 stop step／indexed／palette
  補一次正式 `Frame` 後可繪，原版記憶體與步數未變；不把它冒稱
  真實新畫格。正式 CLI 目前先寫 baseline 再驗 `Draw`，失敗會留下
  部分輸出；完整收據語意與提交順序仍待確認，未改 production。
- #16 另一子代理以正式 scoped 2×／3× runtime 接真正 Ebitengine
  視窗，從原版 checkpoint 的選單狀態操作 Apply 2×→3×→2×；
  主代理獨立重跑通過：面板回合零 DOS 步，2× 往返 RGBA 同值，
  3× 核准矩形外零差且無缺字。這是限縮視窗收據，非完整 #18
  玩家 session；CLI 終態缺口仍待決定及正式修正。

## 2026-09-24 — 第 18 項路由矩陣與推進故障鎖存

- 子代理在 ignored 測試證實純計畫能處理五類合法路由，但目前私有
  session 原型只接受 Down＋單鍵；提交前目標／layout 漂移可零副作用
  拒絕，提交期間排他仍未證實。
- 另一子代理修補 ignored typed 推進原型的 terminal 根因鎖存；首次
  machine fault 後重試保持 `OriginalFault` 與原始 error，零新步、
  不再呼叫 machine。主代理逐行審查、核對 SHA，於 Docker 獨立重跑
  該 package 測試與 `go vet` 通過。正式程式未改，規格 019 與
  Issue #18 仍是 DRAFT／開放；不得把原型當作 Linux 可玩 session。

## 2026-09-24 — 第 16 項 CLI 驗證後才寫檔

- 本機 dosgolem fork `18575d2` 調整四條文字收據 CLI 路徑：先完成
  覆繪與驗證，再寫 baseline／overlay。正式套件測試與 `go vet`
  於無網路、唯讀、有界 Docker 通過。
- 原版選單已驗 Down 停點仍因 `Pending` 回 `drew=false active=3`，
  但不再建立任一 RGBA；同 state 有效 2× 停點仍產出兩份 RGBA
  與 JSON。只修繪製驗證失敗留下半份收據；第二檔 I/O 失敗的
  多檔交易與終態收據選項仍待處理，未將 #16 宣稱完成。

## 2026-09-24 — 第 8 項既有載入訊息轉場與第 18 項滑鼠快照

- 第三頁合法 Enter 的 row 24 21-byte 訊息沿用既有 `roster.loading`。
  主代理重跑原版探針、11 筆身分負例及 control／2×／3× 入頁和
  自然清層；machine／DOS digest 與事件相同，安全矩形外零差。
  規格 023 僅就此一路徑回填限縮 CONFORMED，其餘 DRAFT。
- ignored 私有 session v2 原型已擴充合法輸入矩陣；獨立反例揭露
  `pressedEpoch` 鏡像可漏掉橋內轉態。dosgolem fork `7ff0581`
  新增唯讀值快照，主代理重跑 host 測試、競態測試與 vet 通過。
  尚無正式 owner／提交排他／Draw 收束，#18 仍未完成。

## 2026-09-24 — 前端批次原型使用正式滑鼠快照

- Terra 子代理把 ignored 私有批次 v2 的預檢與終態比對改為
  `MouseBridge.Snapshot()` 五值，修補 `PressedEpoch` 鏡像盲點；
  跨 epoch 漂移在提交前拒絕，合法跨 layout 放開與純計畫等價。
  主代理在唯讀有界 Docker／Xvfb 重跑完整前端套件測試與 vet 通過。
  ABA／排他提交及正式 session 仍未完成。
- 現況稽核發現規格 024 正文已限縮 READY，規格索引卻仍寫 DRAFT；
  已按現行規格與合成／首題收據修正索引，不擴張成手冊玩家路徑
  或正式 Linux session 的 CONFORMED。

## 2026-09-24 — 收據工具多檔回復、手冊字型重驗與翻譯稽核

- 子代理提交本機 dosgolem fork `a18e86a`、`c08263b`：
  正式文字收據 CLI 在程序內發布失敗時回復舊檔、撤銷新檔，
  另拒絕同實體路徑及 symlink 目標。主代理用既有專案 image
  重跑單元、競態測試、vet 與原版 `roster.loading` 四組
  control／2×／3× 入頁／清層，全部通過；當機／斷電不保證原子。
- Terra 子代理唯讀稽核 24 份正式 TSV：無空譯，逐檔 lint、
  249 項工具測試及字元清單重建通過；無可自主修正的確定漏譯。
  `CARLETON JURADIAN` 是待定專名，不擅自音譯；技能操作列
  `(A)/(S)/(P)/(N)/(D)` 保留原字母與原白色規則。
- 主代理額外以本機 `/home/anr2/cht/etan_font` 唯讀來源跑
  `tools/eten_font.py verify`：24 份 catalog、1,028 字模與
  GOLEMFNT SHA-256 `150c93afaa10f1f09f146c9b67ba6fdca35aa5d13d1b6f965cfdedb33a8a5174`
  一致；正式雙層手冊元件的競態測試及 vet 通過。這仍不是
  Linux session 啟動時的來源前檢或手冊正常玩家存讀檔收據。

## 2026-09-24 — 3× host 原生字型載入與第九頁 Ctrl+C 清層

- 使用者選定設定面板 A 版倚天原生 24 點，排除 22 點 B 版。
  子代理在 ignored dosgolem 分支提交 `0d9a22d`、`f51c455`：
  增加 24×24 Wide／16×24 ASCII 本機雙子集載入、雜湊及
  coverage／幾何檢查；主代理複審發現首次實作有讀取後重開檔案的
  替換競態，後續改為雜湊與解析同一份 bytes。合成負例及本機
  倚天測試通過。正式 Linux session 尚未接此 loader。
- 低階翻譯子代理稽核第九頁 catalog，只找到唯一已驗固定單行，
  現有 `story.page9.line.001` 譯文完整且 lint 通過；不猜補未量原文。
  中文 Data Card 的 Ctrl+C 記載引出實際出口實驗。
- 主代理先以合法第九頁 state 的原版有界 probe 證實 `2e:03`
  在 `361000689` 退出，再從合法第八頁 state 正式跑
  control／2×／3× Enter→Ctrl+C。dosgolem fork `99584d8`
  增加 Stop 與 active 前後數量收據；同次 active `1→0`、
  正規化 JSON／indexed 相同、RGBA 終態零殘層。
  [第二百一十九階段](docs/re/phase-219-story-page9-runtime-entry-ab.md)
  已追加證據，規格 022 僅此退出路徑限縮 CONFORMED。
- 第一次套件重跑漏掛私有測試所需 `/project`，第二次漏掛
  `/orig`；確認是容器設定失誤，補上兩個唯讀掛載後以同一組
  `go test`／`go vet` 乾淨通過，非產品故障。

## 2026-09-24 — 3× host 字型封存與 session 輸入政策補證

- 主代理修正正式 `Game.New` 驗字後仍保留外部可變字型 map 的別名：
  2×、3× 的 glyph bytes 在建構時深複製，外部後續刪字、改字模
  或改尺寸不再改變畫面字形。dosgolem 本機 fork `e471bcb`；
  Docker／Xvfb 的定向測試、`./frontend/ebiten ./host ./presentation`
  完整相關套件、`go vet` 及定向 `-race` 通過。定向測試首輪
  誤用已配置 epoch 的滑鼠橋而被正式檢查拒絕，換新橋後同命令
  乾淨重跑；屬測試夾具問題，非產品故障。
- Terra 子代理獨立複審 Issue #18：正式 `Game.Update` 仍逐事件
  交付、`DOS.M` 可改指，ignored owner 不具排他提交或正式
  Draw／Close，故規格 019 不升 READY。後續以 ignored 矩陣
  證實四類現行非命中輸入保持無動作，主代理於同映像重跑
  `TestDraftCurrentNoopRoute` 全通過；證據追加於
  [Issue #18 審查紀錄](docs/re/issue-18-session-turn-ready-candidate-review.md)。
- 低階翻譯子代理只讀稽核 24 份正式繁中 TSV（196 筆）與 39 筆
  已確認手冊 crosswalk，沒有可依現有證據確定的空譯或漏鍵；
  功能選單未達 READY 的原文身分不猜補，正式譯文未改。
- 本輪 Docker 一次性容器均已停止並由 `--rm` 清理；唯讀檢查
  專案沒有 root 擁有檔或誤建的 `.md` 目錄。ignored 探針仍留
  `workplace/`，未加入版控。

## 2026-09-24 — 2× host 本機字型載入與 session owner 原型

- 3× 設定面板依使用者已選的 A 版維持倚天原生 24×24 Wide／
  16×24 ASCII；未把遊戲畫布的 3× 字型視為同一契約。本機
  dosgolem fork `b908226` 新增預設 2× 16×16 字型的本機載入器：
  同一份 bytes 做 SHA-256 核對與解析，建構前驗標籤／安全矩形；
  同時共用 3× 載入器的底層讀取程序，不改兩倍率的畫筆。
- Docker／Xvfb 的 2×／3× 載入器定向測試含合成負例與本機倚天
  字型均通過；`./frontend/ebiten ./host ./presentation` 完整測試
  與 `go vet` 通過。正式 Linux 啟動器未接線，呼叫端預期雜湊的
  獨立來源核驗亦未完成；這不是可玩版或正常存讀檔收據。
- Terra 子代理新增 ignored `session_owned_commit_draw_draft_test.go`；
  主代理核對雜湊並獨立重跑四個定向 Docker／Xvfb 子測試通過。
  可丟棄原型覆蓋私有 owner、整批預檢晚到失敗零 DOS 副作用、
  未命中事件無動作與真實 `Game.Draw` 錯誤後一次 Close 計數。
  正式 `Game.Config`、`DOS.M`、排他提交、同步故障 API 與實際
  資源 Close 仍未封閉；規格 019、004 維持 DRAFT。
- 所有本輪一次性測試容器已由 `--rm` 清理；`docker ps -a` 未見
  本專案殘留容器，唯讀檢查沒有 root 擁有檔或誤建 `.md` 目錄。
  ignored 探針保留在 `workplace/`，沒有加入 Git。

## 2026-09-24 — 原版冷開機字型前檢、首題雙側收據與封閉 session 起步

- ignored Linux 原版視窗原型改成在建立 DOS machine 前，以正式
  `LoadHostFont2`／`LoadHostFont3` 對同次讀取的本機倚天子集做雜湊、
  coverage 與幾何前檢；原版冷開機後實體 Apply 3× 仍可見主選單，
  面板回合零 DOS 步。這是[第二百二十二階段](docs/re/phase-222-original-menu-3x-typography-draft.md)
  的 DRAFT 原型，未接正式啟動器。
- Terra 子代理從合法首題 checkpoint 量 request 前後：前側 2×／3×
  均零手冊作用層與零像素差；後側繁中差異只在正文安全矩形，
  machine／DOS 狀態相同且無檔案寫入。前側使用 ignored DRAFT
  收據工具放行精確 pending 停點；正式 CLI 仍拒絕該停點。
  見[第二百二十三階段](docs/re/phase-223-manual-first-question-host-mixed-script-draft.md)。
- 規格 019 經獨立審查，僅新建封閉 session owner 契約升限縮 READY。
  Terra 子代理加入單事件純值 `host.PlanMouseRoute`；主代理加入
  `Game.Draw` 首次可檢查故障的同步回呼，提交於本機 fork `b062c5b`。
  Docker／Xvfb 相關套件、
  定向 `-race`、`go vet` 與格式檢查通過。兩個元件尚未接成
  封閉 owner；規格 004 仍 DRAFT、Issue #18 保持開啟。
- 低階翻譯子代理稽核 24 份正式繁中 TSV 共 196 筆；無可依現有
  原文證據安全新增的固定譯文，未猜補未確認的第九頁後續輸出。
  後續以同一合法第九頁 state 比較 Enter 與手冊明示
  NumLock-8→Enter；row 15 各六筆整串身分逐筆相同，僅有一個
  孤立 ASCII 字母、無可辨固定英文詞，正式 TSV 未改。
  收據與限制已追加[第二百二十一階段](docs/re/phase-221-command-status-columns-draft.md)。
- 主代理再使 `Game.Draw` 首次故障後停止重讀 snapshot，提交本機 fork
  `6e85c32`；Terra 子代理依規格 019 的限縮 READY 新建私有
  `session.Owner` 生命週期外殼，提交本機 fork `117e0cc`。
  主代理複核時發現初稿在 LoadEXE 前呼叫 `DOS.Install()`，已請
  子代理撤回並固定 Booting 不可推進；建構失敗路徑亦補
  `DOS.Close()`。owner 的 OS 資源測試只證單次 Close 能力，
  不冒稱 DOS handle 收據。主代理以既有 Docker／Xvfb image
  獨立重跑 session／frontend／host／presentation、session `-race`、
  `go vet` 與格式檢查通過；私有 Boot、整批 Commit、step 收據及
  Draw→owner 接線仍待實作。

## 2026-09-24 — 手冊譯文校對與 host 前檢收斂

- 低階翻譯子代理對前十筆已確認手冊映射逐筆核對中文掃描頁與
  英文原文，只修正 `manual.career.rogues` 的「反應極快／可選種族／
  職業技能」，以及 `manual.rules.medic_skills` 的設備故障診斷與
  治療疾病；沒有增刪 key、數值或遊戲輸出攔截。主代理在 Docker
  獨立重跑 catalog lint、字型覆蓋與 `git diff --check` 通過。
- dosgolem 本機專用分支 `00b5663` 新增純值 `PlanPanelRoute`，
  正式 `PanelController.Route` 以同一計畫提交面板狀態。完整 host
  單元／競態測試、vet 與格式檢查在 Docker 通過；它只是輸入
  批次預檢的必要元件，不是封閉 session 的整批排他提交。
- Terra 子代理在同分支 `79047a8` 完成本機 2×／3× host 字型
  manifest 前檢。來源 SHA-256 必須由呼叫端另行審核，manifest
  不能自行證明來源；此介面設計為在建立 DOS machine／視窗前
  檢查輸出 hash、字模與標籤。主代理以既有 Docker image、
  有界 Xvfb 獨立重跑前端／host／presentation 套件、vet 與格式
  檢查通過；子代理另以 ignored 本機倚天重建產物通過實際
  2×／3× 清單收據。此介面尚未接正式 Linux 啟動器，沒有玩家
  冷開機與存讀檔收據，#16／#18 保持開啟。
- 原版遊戲、手冊掃描、本機字型及 ignored 實驗檔均未加入上述
  fork commits。一次性 Docker／Xvfb 容器於工作後清理；未發現
  本專案 root-owned 檔案或誤建的 `.md` 目錄。

## 2026-09-24 — 手冊校譯、字型新鮮度與 session 收據

- 低階翻譯子代理複核第 11–20 筆已確認手冊映射，依中文掃描印刷頁 33
  與英文 Log Book 頁 14 修正 `manual.world.rocketships` 的維生系統
  誤譯；未猜補原文未證實的句子。catalog lint、crosswalk、手冊上限與
  覆繪版面檢查通過。
- 24 份正式 TSV 重生 `font/characters.txt`，本機 2× 倚天字型重建為
  1,035 字模，`eten_font.py verify` 通過。dosgolem 前檢現在核對
  2× manifest 列出的全部目前譯文 SHA-256，以及 3× host 文案；
  合成負例與本機實際 2×／A 版 3× 載入收據通過。這只防止舊譯文
  子集被載入，不代表正式啟動器已接線。
- Terra 子代理在本機 fork 實作限縮 READY 的合成 typed `Advance`
  收據，主代理重跑 session／frontend 測試與 vet 通過。裸 machine
  推進不觸發 Buck Rogers Watcher；observer-aware runner、整批提交、
  原版冷開機、Draw 故障接線與正常玩家驗收仍待完成，Issue #18 保持開啟。
- 上述 dosgolem 改動僅提交在本機分支 `b8c6bca`，沒有推送 fork；
  主專案的文字、字元清單與交接文件另行提交至 private `main`。
- 工作僅在受限 Docker／Xvfb 容器測試與建字型；本機原版、掃描與
  倚天檔未納入 Git。一次性容器已清理，未見 root-owned 檔案或
  誤建 `.md` 目錄。

## 2026-09-24 — 手冊第 21–39 筆續校與觀測接縫原型

- 低階翻譯子代理核對第 21–30 筆中英手冊，主代理獨立回看英文原文後，
  修正 Terrine 服役背景、Scot.dos 警報的第三座馬利波薩、昇降機
  與 RAM 攻擊先後、機械人索要零件／能源電池及沙漠猴駕艦的事件
  順序。第 25–28、30 筆未改；主代理唯讀抽核第 31–39 筆既有
  OCR／映射，未找到足以確認的新誤譯。
- 第二批定稿後再次重生正式 24 份 TSV 的字元清單與本機倚天
  2× 字型：1,025 字模，builder verify 與 dosgolem 正式 loader
  逐字回讀 1,025／1,025 通過。前一筆 1,035 字模是第一批後的
  中途收據，不再代表目前譯文；3× host-only A 版原生 24 點文案未變。
- Terra 子代理交付未提交的通用 `Machine.RunUntilObserved` DRAFT
  接縫與合成測試；主代理獨立重跑 machine／oracle 測試與 vet 通過。
  它尚未接 Buck Rogers Watcher，且現行 Oracle 還有條件、退出、
  guard 及 stub 語意；此接縫不得直接冒稱正式輸出攔截已接通，
  留待規格審查後才可併入 production。

## 2026-09-24 — 3× 面板 A 版確認與封閉輸入回合限縮接線

- 再核對使用者選定的 3× host 面板倚天原生 24 點 A 版；B 衍生
  22 點不進正式前端。這項決定已在 `CONTEXT.md` 與 Issue #16，
  不與遊戲畫布的獨立 3× 字型契約混淆。
- 手冊譯文變動使候選字型測試的舊 934 字模與雜湊斷言過時；
  `a38cd8f` 改以目前正式 TSV 推導，Docker 內 14 項測試通過並
  推送 private `main`，Issue #14 已註記。
- Terra 在 workplace dosgolem 分支提交 `329d816` 的限縮封閉
  session 輸入批次。獨立審查先找出面板狀態／滑鼠版面漂移、同批
  host-hit／canvas Down 矛盾與過期版面下失焦放開三項反例；修正後
  對無法私有投影的面板轉換於 DOS 動作前拒絕，收據改明示為已提交
  呼叫數。主代理在 Docker／Xvfb 獨立重跑 session、host、frontend、
  session 競態測試及 vet 通過。這只保存安全骨架，不是 Linux
  玩家版；缺口記於 Issue #18。
- DRAFT 原版手冊 checkpoint 觀察測試重現 begin→clear→request，
  並與無觀察控制組核對記憶體／CPU；獨立審查指出 generic observer
  與 Oracle 的停止／退出／錯誤排序不同，尚不可接正式 session 或
  宣稱原版正常玩家路徑已中文化。

## 2026-09-24 — 封閉面板版面投影與手冊觀測順序對照

- Terra 依規格 019 的限縮 READY 契約交付 `host.ProjectPresentationLayout`
  與封閉 `session.Owner` 的 Open／Apply／Cancel 私有版面投影。獨立複審
  找出非正式幾何初值、無變化／轉換時掩蓋損壞來源，以及畫布 Down
  同批 Open 先送 DOS 等反例；主代理補負例與拒絕條件後，獨立
  spot-check 未再發現確定的 DOS 誤送。工作只提交本機 dosgolem
  分支 `0546e2a`，未推遠端；host／session／frontend 套件測試、
  host／session 競態測試與 vet 在 Docker／Xvfb 全通過。
- 現有 Ebitengine 視窗的面板命中幾何抽成純函式（`3b8688e`），
  後續改與封閉 owner 共用同一純版面投影（`2901c98`）；2×／3×
  五個控制項的內外邊界、frontend／host／session 測試與 vet 通過。
  這是正式前端元件去重，不是新的可玩入口。
- 子代理以同一原版手冊 checkpoint 補 DRAFT paired-oracle 測試：
  `Watcher.Install(oracle)` 與 raw pre-step adapter 的 begin／clear／
  request、style、return guard、memory、邏輯 CPU、indexed 與 palette
  終點一致；initial predicate、hook breakpoint、DOS exit、HALT 的
  觀測排序則不同。主代理在唯讀原版 Docker 獨立重跑 tagged 測試
  與 vet 通過；測試橋僅在 `draft_manual_checkpoint` tag 編入，
  未提交正式 machine／session／Oracle 程式或宣稱等價。
- private `main` `f6e21ca` 訂正目前正式手冊字元清單的釘版 SHA；
  翻譯／字型工具完整 Python 單元測試 249／249 通過並推送。
  Issue #18 已登記限縮進度與仍缺的 owner runner、冷開機與玩家路徑。

## 2026-09-24 — 值型 View 的同值 ABA 與失敗邊界

- 依規格 019 的封閉 owner 路線，Terra 在本機 dosgolem fork 建立
  tagged 合成 View 原型；獨立 reviewer 逐次指出故障後半份 View、
  Running 缺版面、版本遞增、純 Prepare 與 owner 收束，以及真正
  同值 ABA 的缺口。主代理補上 Running／非正規版面、面板故障不
  重讀、fresh／stale token、值漂移、暫停與執行中 Advance、
  Stopped、溢位前置的負例，並只提交本機 fork `337ac83`，未推送。
- Docker／Xvfb 唯讀重跑 tagged `go test ./session`、tagged `go vet`
  與正式 `go test ./session` 通過；主專案翻譯／字型工具 249／249
  通過。規格 019 僅將輸入擷取值型 View／來源版本子契約升 READY，
  不宣稱 formal Owner、Snapshot、冷開機或玩家路徑已接通。
  主專案原版與本機倚天素材未加入 Git；一次性容器已清理。

## 2026-09-24 — 值型 View 限縮正式接線

- Terra 子代理把已審的 `View`、`CapturedUpdate.SourceGeneration` 與
  全批次同源核對接入本機 dosgolem fork 正式 `session.Owner`，提交
  `a7cb0eb`，未推遠端；先前未相關的 dirty 診斷檔均保留。
- 獨立審查找出鍵盤／面板批次可混拼 stale layout 的漏洞；修正後
  所有批次在首筆 DOS 動作前核對版本、版面存在、正規幾何與滑鼠
  目前版面。真同值 ABA、失焦放開、零版面鍵盤批次及故障單次
  Close 都有定向測試。主代理在無網路 Docker／Xvfb 獨立重跑
  session／host／frontend 測試、tagged DRAFT、session 競態測試與
  vet，均通過；reviewer 最終核准此限縮切片。
- [規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)
  只更新實作狀態，不升整體 CONFORMED。原版冷開機、Watcher、
  畫面 Snapshot、正式 Linux 玩家入口與正常玩家路徑仍待完成。

## 2026-09-24 — 觀測器與 Snapshot 下一片 DRAFT 審查

- Terra 子代理針對逐步觀測提出 tagged 合成測試；獨立 reviewer 找出
  收據的 defer／回傳順序錯誤，修正後主代理在 Docker 重跑定向測試
  通過。整包 `apps/buckrogers` 測試另受既有未提交探針硬讀 `/project`
  私有 fixture 影響，不當作產品缺陷或通過收據。
- 該測試依賴另一份未提交的 `internal/machine` DRAFT 接縫；為避免
  乾淨工作樹出現不可重生的 tagged 測試，本機 fork 已以 `0fff233`
  撤銷剛才的 `0c55ece` 測試提交，內容仍可由 Git 歷史恢復，
  不計入正式驗證。Oracle 的守衛／hook／stub 順序與 Watcher 安裝
  入口仍待獨立規格與實作。
- 另一位 reviewer 唯讀盤點正式畫面元件，確認單幀來源、封閉
  有序作用層與手冊雙層票券可重用；但 owner 尚無影格身分、完整
  作用層清冊與同步故障矩陣。兩條後續工作均維持 DRAFT，未接
  Linux 玩家入口。[規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)
  已列最小缺口。

## 2026-09-24 — 快照 owner 合成 DRAFT 與翻譯缺口複核

- 主代理在本機 dosgolem fork 新增 `draft_session_snapshot` 合成矩陣；
  reviewer 先找出作用層／字型延後封存、票券不綁實際 owner 的
  假通過。補凍結內容、獨立 frameID、同值換 owner 與倍率往返
  ABA 等負例後，reviewer 核准僅作 DRAFT 證據，提交 `670b126`，
  未推送 dosgolem fork。主代理在無網路 Docker 重跑完整 tagged
  session 測試、競態與 vet 通過；測試只用合成 2×1 畫格，不含原版。
- `Owner.Snapshot`、正式 `Layer.Frame`、Clear／Restore、原版觀測器
  與 Linux 玩家入口仍未接。另稽核 Issue #17：職業／技術兩句固定
  Escape→N／Y 已有限縮同狀態 CONFORMED，但正式 session／正常玩家
  存讀檔未涵蓋，Issue 保持開啟。
- 低階翻譯代理只讀稽核 24 份正式繁中 TSV 196 筆與 39 個手冊
  事件鍵，無空譯、重複鍵或確定新漏譯；row 15 與動態 status
  欄不猜補，正式譯文零變更。Docker 批次均 `--rm`；本輪不
  建立發行包或搬運原版／已購字型。

## 2026-09-24 — Oracle 觀測順序 DRAFT 與未譯安全區盤點

- Terra 在本機 dosgolem fork 新增自包含的 tagged 合成 Oracle
  回圈測試；主代理獨立 Docker 重跑，reviewer 複審後僅核准 DRAFT
  局部順序證據。合成 Buck Watcher 動態 return hook 可觸發，
  `Steps(n)`／`Budget(n)` 的預算邊界與正式 Owner 收據不同；
  測試以 `unsafe` 暫時別名私有資源，不進正式路徑。
- 低階模型盤點 24 份正式 TSV 共 196 筆與十個已有安全矩形的
  靜態輸出家族，未找到有足夠證據卻漏譯的固定短字串。主代理
  獨立重生 1,025 字元清單並訂正紀錄中的跨 catalog 唯一性聲明；
  未動正式譯文或本機字型。原版／手冊與私有字模仍留 ignored
  `workplace/`，#8／#18 及 Linux 玩家入口保持開放。

## 2026-09-24 — Oracle 停止收據負例與接線邊界

- Terra 子代理新增自包含 tagged 合成停止收據矩陣；主代理逐行複核，
  在無網路 Docker 重跑測試與 vet，提交本機 fork `b2580a7`，
  未推 dosgolem 遠端。末步退出／HLT／A0000、預算加法回繞及
  raw Stop 不可推定的反例使 observer-aware `Advance` 維持 DRAFT。
- 獨立代理提出唯讀呼叫視圖與有限期動態 hook 的設計候選，
  但正式 watcher 清冊與冷開機尚未驗。低階翻譯代理唯讀複核
  row 15 後仍無可核准固定詞；未改譯文、原版與字型均留本機。

## 2026-09-24 — 3× 原生字型先驗接線與第 15 列收束

- 主代理在 ignored 冷開機原型改以正式來源清單載入雙倍率倚天
  字型，不再鎖過期 2× 輸出檔；原版 1 億步後的 Xvfb 實體
  Apply 測試通過，3× 原生 24 點面板有 31 次快照。這只是
  DRAFT 原型；原版與字型均未加入 Git。詳見
  [第二百二十二階段](docs/re/phase-222-original-menu-3x-typography-draft.md)。
- 獨立代理審查觀測器 runner，發現 watcher 資源邊界與正常
  預算／退出停止分類矛盾；主代理訂正[規格 019](docs/spec/019-linux-frontend-session-turn-boundary-draft.md)，
  未升 READY、未接正式 Owner。翻譯代理核對 24 份 TSV 無安全
  固定詞缺口；另一代理以兩個合法進度量到第 15 列 `N/E`
  方向值及原版 0/10 色參數，保留原文與原色、不新增 TSV。

## 2026-09-25 — 手冊火箭譯文勘誤與受限觀測器原型

- 低階翻譯代理核對手冊 crosswalk records 11–14；11–13 未見可確定譯誤。
  record 14 對照本機 `SCAN0352_019.jpg`（印刷頁 33，SHA-256
  `88ec475c179e5aeeed1a90ada1a410de8d417f670dc0ed886e4a36deefb36ba5`）
  改正 `manual.world.rocketships` 被替換的末句。未變更專名與中英混排政策。
- 由正式 24 份 TSV 重生 `font/characters.txt` 1,023 字及本機倚天 top-pad 子集；
  Docker `eten_font.py build`／`verify` 通過，字型／manifest 雜湊見規格 024。
  先前 1,025 字與字型雜湊已過期；新 manifest 在 Docker／Xvfb 通過正式
  雙倍率來源預檢測試，但未重跑原版實體視窗 Apply。
- Terra 在 ignored dosgolem fork 製作 restricted Oracle facade 測試；主代理指出
  同 package concrete `.o` 資源洩漏後，代理改置 oracle package 私有型別。
  主代理獨立重跑合法 checkpoint paired test 與 vet，通過 9 筆 observation、
  3 筆 presentation 的局部對照。callback fault 的同步中止仍是反例，
  規格 019 維持 DRAFT，無 production runner 或 Owner 接線。
- 所有原版 checkpoint、掃描手冊與已購倚天來源／衍生字型仍僅在 ignored
  `workplace/` 或使用者本機目錄；未打包或公開散布。

## 2026-09-25 — 接收敵艦譯文與 runner 同步停止原型

- 低階翻譯代理核對手冊 crosswalk records 15–18；水星、地球、火星三列無
  可確定譯誤。record 18 按本機中文掃描印刷頁 40 刪除無該頁支持的
  回收信標／帳戶／燃料轉移等細節；`Salvation` 另由英文原版 Log Book
  第 18 頁補證。中文頁末尾艦種 OCR 不確定，譯文只用「修船」。
- 正式字元清單由 1,023 減至 1,016；本機倚天 2× 字型與 manifest
  重生／verify，Docker／Xvfb 正式雙倍率來源預檢通過。雜湊見規格 024；
  未重跑原版實體視窗 Apply，亦未完成 Linux session。
- Terra 在 ignored dosgolem fork 新增 tagged 真實 Oracle runner 原型，
  合成 MZ 矩陣量到 callback error／panic 當次指令前同步中止、
  動態 return hook、末步 exit 與 budget 分型。主代理獨立 Docker
  重跑測試及 vet，僅記為 DRAFT；正式 Owner／Watcher 資源封閉、
  cold boot 與正常玩家路徑未證。
- 依使用者選定的 3× 倚天原生 24 點 A 版，主代理在 Docker／Xvfb
  重跑正式 host 畫筆測試與本機原生子集像素測試：五處標籤的
  3× 墨跡／安全矩形通過，22 點版會失去的尾端仍可見；
  2×→3×→2× 畫面位元組一致、host 點擊未送 DOS mouse。
  這是 host-only 收據，不是原版完整玩家路徑。
- 低階翻譯代理續核手冊 crosswalk records 19–24，六列均未發現須按
  已證實來源修正的譯誤，正式 TSV 與 1,016 字清單不變。第 21–24
  筆遇到本機繁中掃描的改寫或縮略，尤其升降機抵達佛柏前是否已
  遭 RAM 攻擊的敘述與英文原版相反；現有譯文由本機英文原版手冊
  支持，保留原文語意，不以疑似中譯誤句覆蓋。這是來源差異，
  不是玩家路徑驗收。

## 2026-09-25 — 3× 面板 A 版確認、手冊末批校譯與 observer 閘門複審

- 使用者再確認 3× host 設定面板採倚天原生 24 點 A 版；現行
  `Game.New`／`drawText3` 已採 24×24 中文與 16×24 ASCII，排除
  22 點衍生面板字型。主代理在 Docker／Xvfb 重跑正式前端定向測試
  通過；首次 `xvfb-run` 因 image 缺 `xauth` 失敗，改用有 trap 的
  Xvfb 後乾淨通過。這是 host 字型元件收據，不是 Linux 可玩版。
- 低階代理核對手冊 crosswalk records 25–39；25–30 未改，31–39
  原提出七筆修正。主代理對照本機英文 Log Book／Rule Book 後保留
  Log 44、49、56、57、63、68 六筆語意訂正，撤回技術技能表一筆：
  英文表格把 `Jury Rig` 與 `Repair Weapon` 均列為 `A,SC`，不能譯成
  僅限冒險。繁中掃描與英文原段有出入處依英文原意處理；Deimos、
  Stockade、RAM 專名政策未改。
- 正式 24 份 TSV 重生 `font/characters.txt` 為 1,030 字，SHA-256
  `4f556806112e4231909f03b723b6677d14404df73a5fe6ebd632127f327dadce`。
  本機倚天 top-pad 2× 字模 SHA-256
  `c76e29f449d3ae78c1467c6ddf583ac9e3e219a4f3707c65bcf22a0cd6c806b9`，
  manifest SHA-256
  `987a106639f19cba1c0317dde9987783a3b2efce761bc7c1f44d244cd3a19b99`；
  手冊 catalog／39 段版面、逐份 catalog lint、builder verify 與正式
  2×／3× manifest 前檢均在無網路 Docker 通過。跨 catalog 合併 lint
  曾因既有共用 key 失敗，改用正確的逐份 lint 後重跑通過；未將其
  當成產品缺陷。字型二進位、原版與掃描手冊都留在 ignored 本機。
- observer runner 的合法 checkpoint tagged DRAFT 組合收據經主代理
  獨立重跑，量到 9 observation／3 presentation 並與獨立
  `Watcher.Install` 基線同狀態。獨立審查要求明確事件錨點、共用
  安裝路徑與 installer 故障負例；代理在容量中斷前留下試驗性補件，
  主代理修掉因最新譯文而過期的硬碼字數斷言，Docker 定向測試與
  tagged vet 通過。複審仍發現 registrar 可在 `Run` 後延遲註冊，
  規格 019 維持 DRAFT，不接正式 Owner；詳見該規格勘誤。
- 本批所有一次性 Docker 工作使用 `--rm`、無網路與相稱資源限制。
  收尾 `docker ps -a` 無本專案容器；Docker 內掃描本工作樹無
  root-owned 檔案或誤建 `.md` 目錄，修改的 TSV／字元清單及本機
  字型均屬 UID/GID 1000:1000。Linux 玩家入口、原版完整玩家
  路徑與存讀檔同狀態仍未完成；#14／#16／#18 保持開啟。

## 2026-09-25 — 3× 原生面板字型重驗與觀測器註冊閘門

- 使用者再次選定 3× 設定面板 A 版倚天原生 24 點，排除 22 點衍生版；
  現行本機 dosgolem fork 已接 24×24 中文、16×24 ASCII。主代理
  以唯讀本機子集、無網路 Docker／Xvfb 重跑 `TestNativeHostFont3LocalPixels`
  與 3× 載入／幾何負例，全數通過。這是 host-only 合成畫格，非完整
  Linux 玩家入口或原版 DOS 同狀態。
- tagged DRAFT observer runner 移除對外 registrar，加入首次 Install、
  限時 scoped registrar、錯誤優先與重入 Run 保護；合成 MZ 負例覆蓋
  重複安裝、捕獲後延遲註冊、nil hook、忽略錯誤、callback 內重入及
  首錯／零步收束。主代理在唯讀原版掛載的 Docker 重跑 oracle 與
  Buck 合法 checkpoint 定向測試及 vet，全部通過。獨立複審仍指出
  跨 goroutine 註冊與 CallView 未凍結兩個缺口，故規格 019 仍 DRAFT；
  不接正式 Owner，下一候選改以 callback 回傳值型 hook 增量。
- 低階翻譯代理核對角色頁 35 個 key、原版事件、版面與字型，現行
  lint／2×／3× 收據通過且未留下譯文變更。`Use Jetpack` 目前兩頁均
  譯「使用飛行器」；手冊索引可定位技能章，但本輪未證實專名詞，
  故不在缺少來源核對時改動共用 key 或字型子集。
- 本輪未改原版遊戲、手冊與私有字型；未發布產物。Docker 工作均為
  `--rm`／無網路／有資源限制；收尾仍需核對容器及 root-owned 殘留。

## 2026-09-25 — 共用 3× 實體像素字首封存與 E1 adapter 草案

- 依使用者的共用引擎選擇，本機 dosgolem fork 的 `1e05ff6` 將
  physical glyph 納入 sealed group：來源字型指標先核對，投影以
  `DrawChecked` 全層預檢；錯倍率、未登錄字型在讀原版影格前拒絕，
  舊單層投影不再靜默漏畫。規格 234 補記於 `1d13dba`。
- `5fe9707` 加入局部 Clear 與三幀來源變動無殘字測試；
  `go test ./xlate ./presentation` 及 `go test -race` 均在有界、
  無網路 Docker 通過，規格 234 再補記於 `6136d2f`。
  測試使用合成字型，不能替代手冊正式同狀態收據。
- 獨立複審又以 `2702c56` 補上 physical glyph 部分 Add、錨定格
  全失效、sealed group generation／epoch 變造的正式合成負例；
  主代理重跑 `go test -race ./xlate ./presentation -count=1`
  通過，規格 234 補記於本機 fork `4935435`。
- E1 14px adapter 的 14 行純值版面、零寬行界空白 source span、
  雙字型身分與固定編碼 layout hash 已形成規格 005 DRAFT 候選；
  針對可變指標、漏入 hash 的矩形／列欄位及非 ASCII 重疊，
  代理已迭代修正。獨立審查再指出窄括號過寬會越左界、
  39 段測試未建 plan、空尾列表示不合法；補上明確拒絕、
  真字型 39／39 plan checked draw／Snapshot／Restore、
  source span 與 hash 變造負例後，主代理於 Docker 獨立重跑
  `-race -count=2` 通過，獨立複審准許規格 005 E1 分支升 READY。
  這只開啟 production 實作，未改正式 `ManualSnapshotOwner` 或 2× 路徑。
- 低階翻譯代理覆核故事第 5–8 頁：四份 lint 與字型覆蓋均通過、
  目前 TSV 雜湊符合既有收據，未取得可證實的新增誤譯；
  因原文收據只有雜湊而非全文，這不構成逐字英中人工校對。
  正式 TSV 與本機字型未因此修改。
- #18 的 tagged Delta runner 並行 probe 由競態偵測器重現
  machine steps 讀寫競爭；test-local atomic CAS gate 的
  `Run`／`Install`／callback 重入零步負例經主代理 Docker
  `-race` 重跑通過。兩者都只是 DRAFT，正式 Owner／Linux
  session 尚未接線，規格 019 已追加停止線與測試入口。

## 2026-09-25 — E1 正式計畫與手冊 owner 第一片

- 本機 dosgolem fork `c39f72a` 建立正式 `ManualE1Plan`：14px 英文
  字首、保留英文專名詞界、純值來源 span、雙字型封印、實際括號
  crop、過寬與游離連接符拒絕、14 列 physical／legacy 空尾列。
  正式 39／39 本機 catalog 測試逐段跑 checked draw、Snapshot／
  Restore 後逐像素相等與 3／11 零寬 separator；主代理以唯讀
  私有輸入在 Docker 重跑 `-race`／vet 通過。原版或完整譯文
  未進 Git。
- 本機 fork `5fcc1d6` 使 3× 正式 `ManualSnapshotOwner` 經
  `BuildManualE1Plan`、雙字型 sealed group 與 checked projection；
  plan／字型變造、跨倍率、Clear／SetStyle／換題後的舊 ticket，
  以及投影錯誤後修回資料仍不可復活的負例通過。2× 舊路徑
  保留，合成快照與 RGBA golden bytes 不變。
- 主代理 Docker 定向 `-race`／vet 均通過。直接跑整個工作樹的
  `apps/buckrogers` 曾因既有未版控 command-status 探針缺少私有
  checkpoint／TSV 而失敗；以同一已版控 HEAD 加本次三個正式
  owner 檔在一次性乾淨容器重跑 `apps/buckrogers`、`presentation`、
  `xlate` 全套通過，將環境缺件與產品回歸分開。新版原版同狀態
  A/B 當時尚未取得，E1 分支不得稱 CONFORMED。

## 2026-09-25 — E1 首題新版 owner 同狀態驗證

- 使用既有私有 `ab-1045` 原版 checkpoint 與現行本機 catalog／
  倚天字型，在無網路 Docker 重跑正式 3× E1 owner 的首題
  A/B。2× RGBA SHA-256 與舊收據逐位元同值；3× E1 的中文
  差異僅在核准手冊矩形，外部零差。control／2×／3× 的原版
  indexed、palette、記憶體，以及正規化 machine／DOS
  狀態摘要一致。細節見 phase 223，私有收據不入版控。
- 原始 `.state` 的一次位元組比較出現差異；查明 gzip／gob
  map／handle 順序後，改用專案既有 `cmd/state-compare` 重跑
  control／2×／3×，正規化摘要全相同。保留這筆方法勘誤，
  不將非決定性序列化誤報成遊戲狀態變化。
- 此時僅首題終態有新版 E1 原版收據；答錯換題、成功返回、
  正式 Linux session 與其餘 38 題未因此驗收。規格 005
  E1 分支維持 READY，Issue #21 不關閉。

## 2026-09-25 — E1 換題／返回局部同狀態補證

- 獨立代理沿用 phase156 兩條合法原版 checkpoint，為錯答 `x`
  加 Enter 換題及答對 `to` 加 Enter 返回建立被忽略的本機
  owner oracle；主代理在無網路 Docker 重跑 `-race` 通過。
  換題的 2×／3× 差異只在核准矩形內，返回清除後內外零差；
  兩案舊 ticket 均失效，2× 終態 RGBA 與舊收據逐位元相同。
- 原版 control／2×／3× 的輸入排程、indexed、palette、
  記憶體一致；主代理另用 `cmd/state-compare` 獨立比較
  control、owner 前後共 12 組 machine／DOS 正規化狀態，
  全為 `equal:true`。精確 RGBA／狀態摘要見 phase 223，
  原版存態及原始收據留在被忽略的本機工作區。
- 此為固定 checkpoint 的局部驗收，不是冷開機 Linux 玩家
  視窗，也未覆蓋其餘 38 題或不同英文詞界的 runtime 樣本。
  規格 005 E1 分支仍 READY，Issue #21／#14 不關閉。
