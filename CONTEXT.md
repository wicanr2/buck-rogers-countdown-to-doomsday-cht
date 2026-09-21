# 目前狀態

更新：2026-09-21

第六十五階段已完成：角色資料／重擲頁 35 個靜態 request 已接入 dosgolem 明示 2×／3×
runtime overlay。base／`Y` 各雙倍率雙重重播決定，安全矩形外差異為 0、raw framebuffer
不變；spec 038 已 CONFORMED。產品預設倍率仍未選。此終態 dosgolem palette 將動態值色號
15 映成黑色，未覆繪 baseline 亦如此；這不是中文層清除，動態值可讀性／palette parity 尚未完成。

第六十四階段已完成：角色資料／重擲頁的 35 個靜態 exact identity 已建立繁中 catalog，
dosgolem spec 037 已 CONFORMED。四次 Enter 與其後 `Y` 分支各雙重重播，分別產生 43／52
筆 request；JSON 與 framebuffer 各自逐 byte 相同，原版畫面雜湊未變。動態姓名、身分、
摘要、能力值、技能值與骰值皆未進 catalog；本階段尚未接 renderer，也未選 2×／3×。

第五十七階段已完成：dosgolem 已將 14 筆靜態請求接到輸出端繁中 RGBA 覆繪；
`026F:029C` 清除矩形與同原點取代契約使終態只保留當下 `roster.add_prompt`。
2×／3× 各兩次可決定重生，原版 framebuffer、輸入、FileOps、writes 與存檔不變；
動態姓名列零覆繪差異。spec 035 已 CONFORMED，但 2×／3× 產品預設仍留給使用者決定。

第五十六階段已完成：保存→功能選單→名冊→加入隊伍 catalog 已接入 dosgolem 唯一 guarded
`MenuRequestWatcher`。兩次完整正常路徑皆為 18 events／14 requests／4 dynamic-name misses，
3 writes 與 2,611 FileOps 逐項等於無 catalog baseline；framebuffer 與保存檔亦逐 byte 不變。
spec 034 已 CONFORMED，專案 100 項測試及 dosgolem 全套 test／vet／race 通過。仍未接
renderer，2×／3× 尚待使用者決定。

第五十五階段已完成：第五十四階段保存→名冊→加入正常路徑的 18 筆事件已鎖成 exact identity
清冊。四筆姓名事件分別是固定欄寬 `A`、反白／正常 `A` 與已加入標記 `* A`，均明確禁止進入
翻譯 catalog；兩筆新增靜態文案與五筆尚缺功能選單文案已有正式繁中譯文。97 項專案測試
通過，字元清單含 37 個唯一字元。尚未接 renderer，2×／3× 仍待使用者決定。

## 已確認的產品方向

使用者於 2026-09-20 確認維持原訂的 **dosgolem 執行期輸出端繁體中文化**。已排除
clean-room remake／重寫引擎分支；後續只可在不改動原版 EXE、資料、規則、手冊驗證或
存檔語意的前提下，建立原版輸出事件、中文覆繪與同狀態收據。

- 第一階段「可觀測的原版啟動與文字輸出基線」已以 dosgolem 完成：真實 `START.EXE`／
  `GAME.OVR` 可由固定狀態經 BIOS 空白鍵走到玩家可見功能選單，兩次 raw VRAM 雜湊相同。
- 權威收據與未解項目見 [原版觀測證據索引](docs/re/README.md)；原始輸入與收據只在被
  Git 忽略的 `workplace/`。
- 已完成第二階段：`0763:0424` 已證實讀取 `[length:u8][ASCII bytes]`，再經 `0763:026B`、
  `0763:1809` 到 `0763:183A..1863` 畫出 8×8 英文 glyph；選單樣本含原文字串 pointer、
  色彩與文字格座標。完整證據見 `docs/re/phase-2-text-dispatch-and-lifecycle.md`。
- 清除／捲動、游標反白、畫面轉換、返回與存讀檔後的覆繪失效時機仍未知，因此
  `docs/spec/001-menu-text-output-overdraw-draft.md` 仍是 DRAFT，未授權 production hook。
- 功能選單的 BIOS Enter 轉場現已量到：新字串輸出可早於舊選單像素清除，因此覆繪不能以
  「下一筆字串已輸出」當成畫面失效判定。詳見 `docs/re/phase-4-menu-interaction-lifecycle.md`。
- `PICK RACE` 的 BIOS Escape 返回亦已量到：原版取走 `0x1B` 後，第一筆新文字 dispatch
  仍早於舊標題像素清除；終點逐位元等於既有功能選單基線，獨立重播結果相同。詳見
  `docs/re/phase-5-pick-race-return-lifecycle.md`。
- dosgolem 已依使用者指示複製至被忽略的 `workplace/dosgolem/`，工作分支為
  `buck-rogers-cht-output-overlay`，基準 commit 為 `d9c0c27ca9af8239c7e96272a7165e03d7da04bf`；
  後續 probe 與 adapter 變更只在該副本進行。
- 第六階段已訂正清除定位：watchpoint 的 `0CF4:1B3C` 是 `REP STOSB` 後的下一個 IP；實際
  寫入在 `0CF4:1B3A`，其函式 `0CF4:1B2B` 是通用 byte-fill，已排除為 invalidation hook。
  兩條轉場共用的上層候選是 `026F:029C` Mode 13h 矩形清除例程；Enter 清除
  `x=8..311,y=16..183`，Escape 返回清除 `x=0..311,y=0..183`。完整證據見
  `docs/re/phase-6-clear-path-hook-evidence.md`。
- 第七階段已證實 `0763:0424` post-call：`Create New Character` 最後 glyph 於
  #100,025,833 寫完，#100,025,943 才返回 `37F1:1856`。現有 `OnCall` 足以在 adapter
  觀測 return，但必須由 entry 建立 pending frame，並以 return address、`SS` 及
  `SP == entry SP + 0x10` 排除自然 fall-through；`37F1:15BD` 已有實際反例。Enter 的事件
  順序是舊選單 post-call → 矩形失效 → 新畫面 dispatcher／post-call。完整證據見
  `docs/re/phase-7-text-post-call-generation-event.md`。
- 中文手冊 RAR 已在 Docker 以 `lsar`／`unar` 盤點、完整性測試與解壓；80 個 archive
  項目通過、79 個實體檔案已有 SHA-256 清冊，並有 77 張 JPG 的 archive-order 定位。
  詳見 `docs/re/phase-3-manual-input-inventory.md`。手冊語意、頁碼與原版題目對應仍未知。
- 第八階段已建立首批 UTF-8 繁中 TSV，並由正常 Enter 路徑傾印九筆可見來源；六個種族
  譯名已用中文說明書核對。GNU Unifont 2× 填滿格與 3× 置中兩份本機 prototype 均完整
  清除第一筆 20 格原文且未越界。正式倍率仍待使用者選擇，尚未建立 production adapter。
- 第九階段已把 psychic-war 驗證過的遊戲無關 `xlate` package 移植到 workplace dosgolem
  專用分支，本機 commit `b33cfbf`；`xlate` 與全部正式 packages 均通過。現行 `Draw` 只接受
  3 的倍數倍率，所以仍不能把它解讀為使用者已選 3×。dosgolem 遠端推送待明確外傳授權。
- 第十階段已把 TSV 驗證、決定性字元清單與 Unifont→GOLEMFNT 16×16 子集建置工具納入
  專案。現有 8 筆譯文導出 24 個唯一字模；904-byte prototype 已由 dosgolem production
  `xlate.LoadFont` 回讀並覆蓋全部 29 個譯文字元；fontcheck 位於本機分支 commit `8a22460`。
  字型二進位只留 `workplace/`，正式字型與 2×／3× 決策仍 pending。
- 第十一階段已由載入 A 存檔後的正常功能選單路徑，證實進入冒險會顯示
  手冊查詢。第一題為英文 Log Book 第 34 頁 `Deimos Prison` 第十字；明確錯答
  後原版會重新抽題。對應繁中來源是 `SCAN0352_039.jpg` 印刷頁 73 的「49. 在監獄中」。
  `docs/spec/002-manual-paragraph-overlay-draft.md` 只允許輸出端顯示中文段落，禁止自動作答或改原版判定。
- 第十二階段已證實手冊題庫位於執行期 `0EC0:00C2..0553`，共有 39 筆 30-byte 紀錄；
  頁碼、英文標題與序數已形成可重生清冊。工具不解碼、不輸出答案；第 32 與第 38 筆已
  分別對回動態 `Deimos Prison` 與 `Technical Skills` 抽題。中文來源仍只有前者唯一確認。
- 第十三階段已逐筆建立繁中掃描來源對照：35 筆已證實、3 筆強推論、`Roll.` 1 筆因素材
  只到印刷頁 87 而未知。來源 SHA-256 全部通過既有 manifest 驗證；OCR 只作搜尋線索，
  尚未逐字校訂的段落沒有加入顯示 catalog。
- 第十四階段已由原圖校訂八筆單一短段落，連同既有 Deimos 共建立 9 筆
  `manual-events.tsv → manual.zh-TW.tsv` 精確映射。事件／題庫／來源／catalog 驗證要求
  來源必須為 `confirmed` 且沒有孤兒鍵；段落長度 35–236 字元，尚未據此決定分頁或倍率。
- 第十五階段再由原圖校訂八筆規則／生物／旅程短段落，事件與 catalog 增至 17 筆；新增內容
  長度 31–216 字元，全部通過既有 confirmed 來源與精確題目身分驗證。
- 第十六階段盤點剩餘 18 筆 confirmed 候選，只納入 5 筆非表格、非跨頁且內容完整的項目；
  事件與 catalog 增至 22 筆。其餘 13 筆已依跨頁、長章節、清單或表格分類，不以截斷內容
  湊數；完整排除收據見 `docs/re/phase-16-manual-compact-paragraphs-3.md`。
- 第十七階段以真實手冊查詢 VRAM 建立 2×／3× 分頁 prototype：安全矩形為
  `[7,312)×[7,184)`，正文 36×17 格、每頁 612 字；正式 236 字段落為 1 頁，708 字壓力
  樣本為 2 頁，兩案安全矩形外皆為 0 px 變更。2× 字較大但需擴充目前只接受 3 倍倍率的
  `xlate.Draw`；3× 已受支援但字體相對畫面較小，仍待使用者選擇。
- 第十八階段已由固定狀態兩次重播答錯換題：新題首於 #301,127,835 出現，局部矩形清除
  到 #301,166,163 才發生，證實原版不會先整面清空。DRAFT 契約改以精確題首 entry 立即
  使舊 generation 失效，累積頁碼／標題／序數後，只在 `word?` guarded post-call 顯示新
  中文段落；兩次終態 raw VRAM 雜湊一致。完整收據見
  `docs/re/phase-18-manual-generation-invalidation.md`。
- 第十九階段建立未接入 production 的題目事件收集器 prototype：題首建立 generation，六筆
  guarded post-call 依序累積 page／heading／ordinal，`word?` 才提交唯一鍵。真實事件重建
  `41 / Technical Skills / second`；9 項測試涵蓋缺欄、亂序、重複、未知 caller、錯誤頁碼及
  舊 generation 延遲返回，均失敗即關閉。完整設計見
  `docs/re/phase-19-manual-event-collector-prototype.md`。
- 第二十階段把完整題目鍵接到正式事件與繁中 TSV：`Deimos Prison / tenth` 唯一命中 73 字
  顯示請求，未有完整校訂段落的 `Technical Skills / second` 明確不顯示。12 項測試涵蓋
  generation、精確身分、各層唯一性、孤兒鍵、無效 UTF-8 及顯示請求不含答案。runtime
  ordinal 目前只動態證實 `second → 2`、`tenth → 10`，完整橋接仍是 READY 前置。詳見
  `docs/re/phase-20-manual-catalog-display-request-prototype.md`。
- 第二十一階段以 IDA Pro 9.4 與 runtime dumps 證實原版序數表：consumer 將題庫
  `record[+14]` 乘 19 後加 `0EC0:339B`，索引 `first` 至 `tenth` 十個長度前綴 slots。
  `text/manual-ordinals.tsv` 可由原版 dump 決定性重生，現有 22 筆 catalog ordinal 全數涵蓋；
  7 項正反向測試通過。完整證據見 `docs/re/phase-21-manual-ordinal-bridge-evidence.md`。
- 第二十二階段已在 workplace dosgolem 分支擴充 `xlate.Draw`：正整數倍率皆可用，2×／3×
  的 16×16 字模精確像素、非法倍率與短緩衝區裁切測試均通過；真實 GOLEMFNT 已畫出繁中
  「地球」。本機 commit 為 `ef7f8db32b20a6b9eb6d810bd4e6b99187c55f44`，未推送 dosgolem
  遠端。這不代表已選定產品倍率，詳見 `docs/re/phase-22-dosgolem-xlate-integer-scale.md`。
- 第二十三階段已將第 19–21 階段的事件／序數／catalog 契約審查為 dosgolem READY 子規格，
  並實作 `apps/buckrogers` 未接線純核心。正式 TSV、generation、poisoned 復原與 malformed
  反例測試、`go vet`、race detector 及所有正式 packages 均通過。本機 commit 為
  `8ce092f29d000ea7e6765c4f3389fe484aefa555`，未推送 dosgolem 遠端；玩家可見整合仍為 DRAFT。
- 第二十四階段已完成 dosgolem runtime watcher：`0763:0424` entry 保存 caller／SS／SP，
  只有 return address、相同 SS 與 `SP+0x10` 三重 guard 通過才提交片段；`026F:029C` clear
  亦已接線。由 #266,399,999 固定狀態重播的第一題在 #266,557,246 精確產生
  `manual.page34.deimos_prison.word10` 顯示請求，收據只含 metadata。watcher 不送鍵、不含
  答案、不寫原版狀態且尚未繪圖；dosgolem 本機 commit 為
  `38585dcd9e3861b6fa64a1b89dbec19e5a038dd7`，未推送其遠端。
  詳見 `docs/re/phase-24-manual-runtime-watcher.md`。
- 第二十六階段已完成 README 穩定入口：以 SSI 產品目錄、原版 Rule Book 保存掃描及
  MobyGames 版本／製作資料介紹作品歷史、Gold Box 系譜與核心循環；同時明確標示本專案
  非 remake、原版素材須合法自備、尚無玩家版或 Release，且繁中尚未接入正式畫面。
- 第二十七階段已由相同正常 Enter 固定輸入重生功能選單到 `PICK RACE` 的九筆 dispatcher
  entry／guarded post-call。`text/menu-events.tsv` 以長度／SHA-256、caller、色號與座標連到
  八個正式繁中 key，不保存原文全文；真實 receipt verifier 與正反向 schema 測試均通過。
  dosgolem 本機 commit 為 `98f3bec55d633cc2a69099f187848af4d765b7d1`，未推送其遠端。
- 第二十八階段已把九筆事件接成 dosgolem READY 純核心：`MenuCatalog` 嚴格載入正式事件／
  繁中 TSV，以完整 length／SHA-256、caller、色號與座標精確解析 `DisplayRequest`；真實
  第 27 階段 receipt 九筆全數命中，所有正式 packages test／vet 與 Buck Rogers race
  detector 通過。本機 commit 為 `0be85255d9cd5428c6b55a813410dcacbfd73a4f`，未推送
  dosgolem 遠端；尚未載入字型、繪圖或接入玩家可見路徑，選單整合仍是 DRAFT。
- 第二十九階段已把 `TextRecorder` 與 `MenuCatalog` 接成 CONFORMED runtime request watcher：
  同一正常 Enter 固定狀態在九筆 guarded post-call 各直接提交一筆繁中 `DisplayRequest`，
  零 drop／pending／catalog miss。收據只含事件 metadata、key 與譯文字數；dosgolem 本機
  commit 為 `c6a963dafaf3f060a43816f8a6acbda90aa8b7a0`，未推送其遠端。尚未載入字型或繪圖。
- 第三十階段由正常 Down／Up 證實種族選單 selection lifecycle：舊列先 normal redraw，新列
  再 selected redraw；同終點 Down 差異只在 `(24,24)–(79,39)`、832 pixels，Up 後逐位元
  回到 steady。正式 text-safe rectangle 已分離 col 1 原文清除範圍與 col 3 中文 anchor。
  三筆新增 variant 尚未接入 catalog；dosgolem 本機 commit 為
  `d55a4c84c3474034257cddf58d6fa32cff3d60d4`，未推送其遠端。
- 第三十一階段已把三筆 selection variant 納入正式 12-identity exact catalog；固定
  Enter→Down→Up 路徑兩次都產生逐位元相同的 13-event／13-request 收據，零 drop、pending、
  catalog miss。舊九事件收據仍嚴格驗證前九筆；dosgolem 本機 commit 為
  `79ecc2b9585f02339eef181ecb88b752bee4c2aa`，未推其遠端。字型、renderer 與倍率仍未接入。
- 第三十二階段以 steady／Down 真實 framebuffer、正式 TSV 與 dosgolem `xlate.Draw` 重生
  2×／3× 選單 A/B；兩批逐檔相同，四份收據皆零缺字、零重疊、零安全矩形外差異。
  2× 為 640×400／16×16 滿格，3× 為 960×600／16×16 ink 置中 24×24 格；本機 dosgolem
  commit 為 `09f580877b0d1e34ef00fa44eddefa12898b7e53`，未推其遠端。
- 第三十三階段以 steady／Down 各 978 點長窗口證實：完整 palette 不變，色號 0／15 同為
  黑色，selected row 完成後 pixels 與事件數都維持固定；取樣窗口內沒有 palette blink 或
  週期性 redraw。未來忠實 renderer 必須保留黑底黑字 selection style；dosgolem 本機
  commit 為 `41917c85007efe17154cb92422cba3fe6539ad88`，未推其遠端。
- 第三十四階段已把離線診斷命令的 stamp／ink／containment 規則移入 dosgolem
  `apps/buckrogers` 倍率中立純核心；呼叫端必須明示倍率，沒有產品預設值。steady／Down ×
  2×／3× 的繁中 PNG、base PNG 與 JSON 全部逐 byte 等於第 32 階段基線；spec 015 已
  CONFORMED，本機 dosgolem commit 為 `64b15779edc9d5be35e1acba0f854ba022008511`，未推其遠端。
- 第三十五階段由正常雙 Enter 選定預設種族，兩次重生相同的 14-event 收據與終點
  framebuffer；下一個性別選擇畫面新增提示、兩筆 normal 選項與 selected 第一選項共四筆
  content-safe identity。dosgolem spec 016 已 CONFORMED，本機 commit 為
  `7009315c5a04981eb1b048e7bba34a0b932fbf6d`，未推其遠端；尚未建立譯文或量方向鍵 lifecycle。
- 第三十六階段以正常 Down→Up 與 Escape 完成性別選擇生命週期：前者依序 normal／selected
  重畫兩列並逐位元回到第一列終點；後者先取消男性反白，再重建上一層功能選單，而非返回
  種族選單。兩路徑各自雙重重播一致，專案 50 項測試通過；dosgolem spec 017 已 CONFORMED，
  本機 commit 為 `57daa16fd3ab38ff19b8b1702fecf5b0ca14992d`，未推其遠端。仍未建立性別譯文或 renderer。
- 第三十七階段已把七個性別 identity 與三筆繁中 catalog 接到既有 guarded post-call watcher：
  Enter→Enter→Down→Up 兩次皆為 18 events／18 requests／零 miss；Escape 兩次皆為 22 events／
  15 requests／7 misses，且返回功能選單後不沿用性別請求。dosgolem 共用 exact catalog 核心，
  沒有第二套 watcher；spec 018 已 CONFORMED，本機 commit 為
  `24f0dd55cdce8a929ab513e2a2a1f78afb6fb56b`，未推其遠端。仍未載入字型、繪圖或選倍率。
- 第三十八階段由第三個正常 Enter 接受預設性別，證實下一畫面為五選項職業選擇；兩次
  22-event JSON 與終點 framebuffer 各自逐 byte 相同，新七筆 content-safe identity 已由
  嚴格 verifier 覆蓋。dosgolem spec 019 已 CONFORMED，本機 commit 為
  `371683b7f5793c7104e839202497c742ba3e13c0`，未推其遠端；尚未量職業方向鍵／返回，也未建立
  職業譯文或 renderer。
- 第三十九階段以正常 Down→Up 證實職業第一、二列依序 normal／selected 重畫，並逐位元
  回到第一列初始狀態；Escape 先取消第一列反白，再重建功能選單，而非返回性別選擇。
  兩條路徑各自雙重重播一致，專案 61 項測試通過；dosgolem spec 020 已 CONFORMED，本機
  commit 為 `d8f34f101c719e6939565fe8b6f0d8b531e07ccc`，未推其遠端。尚未建立職業譯文、renderer
  或倍率預設。
- 第四十階段由中文說明書原圖核對五個職業譯名，將十個職業 identity 接到 dosgolem 共用
  exact catalog 與 guarded post-call watcher。steady／Down→Up／Escape 各雙重重播一致，分別
  為 22／26／23 requests；Escape 返回選單的不同 identity 正確形成七次 miss，未放寬比對。
  專案 65 項測試與 dosgolem 正式測試、vet、race 全數通過；spec 021 已 CONFORMED，本機
  commit 為 `0025008fbb7d49c42e352f961585a10e82c118e5`，未推其遠端。仍未載入字型、繪製繁中像素
  或選定倍率。
- 第四十一階段以四個正常玩家路徑 framebuffer 完成性別／職業 2×／3× 覆繪 A/B；八組
  輸出各重生兩批，皆零缺字、零重疊、安全矩形外零差異且 ink contained。2× 是 640×400、
  16×16 滿格；3× 是 960×600、16×16 ink 置中 24×24 格。兩者幾何皆可行，2× 仍較接近
  PC-98 Golden Box CJK 密度，但尚未被使用者選定；spec 022 已 CONFORMED，本機 dosgolem
  commit 為 `73e610943cb26ed3f0990ecd13bd196d12fe162a`，未推其遠端。
- 第四十二階段由第四個正常 Enter 接受預設職業，證實下一畫面為角色資料／重擲能力值頁；
  兩次 118-event JSON 與 framebuffer 各自逐 byte 相同，新增 96 筆事件已區分靜態標籤、
  動態值、能力值、技能與重畫角色。固定 snapshot 可重生相同結果，但 seed 與亂數實作仍
  未辨識，不外推自然開局；dosgolem spec 023 已 CONFORMED，本機 commit 為
  `1e8060b5a83665da1e1b74a4f02cb391f938e25d`，未推其遠端。
- 第四十三階段以正常 BIOS `Y`／`N` 證實重擲與接受分支：`Y` 新增 31 筆事件後回到同一
  提示，`N` 新增 65 筆事件後進入姓名提示。兩分支各自雙重重播一致；固定 snapshot 可
  重生同一組結果，但 seed／亂數公式仍未知。spec 024 已 CONFORMED，dosgolem 本機 commit
  為 `4f899924b35e14fdb7ef23bbb2fcd2620284ae43`，未推其遠端。
- 第四十四階段證實姓名字元逐字回顯，Backspace 直接清除最後字元但沒有 dispatcher 事件；
  非空姓名 Enter 轉入職業技能點配置畫面。Escape 只重印提示，空字串 Backspace 無變化。
  編輯與確認分支各自雙重重播一致；spec 025 已 CONFORMED，dosgolem 本機 commit 為
  `260b3a7f504f7ade6b5487aa591e99911a82bd13`，未推其遠端。
- 第四十五階段以正常 BIOS 輸入證實職業技能配置畫面的 Down 會由第一列移到第二列，預設
  動作下 Enter 可替第一項技能合法加一點；仍有 6 點未用時 Escape 顯示確認提示，`N` 會
  回到逐 byte 相同的配置畫面。三條分支各自雙重重播一致，專案 82 項測試與 dosgolem
  正式測試、vet、race 全數通過；spec 026 已 CONFORMED，本機 dosgolem commit 為
  `a0bb175d4712b92ce183ac1bd8715aaa6b4bcbec`，未推其遠端。減點、`Y` 離開與配置完成後轉場
  仍未證實；本輪未翻譯、接 renderer 或選定倍率。
- 第四十六階段證實職業技能配置的預設 Enter 加點後，Right→Enter 會把同一技能與剩餘點數
  完整還原；終點逐 byte 等於零點／Right 選取畫面。Left 由預設位置環回離開位置；Escape→
  `Y` 在未用 6 點時仍可進入技術技能配置畫面。兩條正式分支各雙重重播一致，專案 85 項
  測試與 dosgolem 正式測試、vet、race 全數通過；spec 027 已 CONFORMED，本機 dosgolem
  commit 為 `dbd262607c90be3a0e92b7173b61bbf140823580`，未推其遠端。技術技能互動與角色建立完成
  仍未證實；本輪未翻譯、接 renderer 或選定倍率。
- 第四十七階段由正常路徑進入技術技能配置，證實 Down 選取移動、Enter 加點、Right→Enter
  完整減回、Escape→`N` 回到逐 byte 相同基線，以及 Escape→`Y` 進入角色身體圖示選擇。
  四條正式分支各雙重重播一致，專案 88 項測試與 dosgolem 正式測試、vet、race 全數通過；
  spec 028 已 CONFORMED，本機 dosgolem commit 為
  `0b66a03808f9d67e2c57ca23e82ad56eb08ac254`，未推其遠端。身體圖示互動與角色建立完成仍未
  證實；本輪未翻譯、接 renderer 或選定倍率。
- 第四十八階段證實四方向鍵皆改變角色身體圖示選取；正式 Right 分支固定為 297 events。
  Enter 與 Escape 顯示逐 byte 相同的確認提示，Enter→`N` 重建並回到圖示基線，Enter→`Y`
  進入儲存詢問畫面。三條正式分支各雙重重播一致，專案 90 項測試與 dosgolem 正式
  test／vet／race 通過；spec 029 已 CONFORMED，本機 dosgolem commit 為
  `b385b85103ada0e381063f4869e42b3f006c2f6b`，未推其遠端。尚未回答儲存詢問，也未翻譯、
  接 renderer 或選定 2×／3×。
- 第四十九階段證實儲存詢問採選項操作：直接字母 `Y` 無作用，直接字母 `N` 接受預設
  `NO`；Left→Enter 接受 `YES`。兩條接受分支都回到逐 byte 相同的功能選單，四份 writable
  overlay manifest 當時也相同。但該命令未設定 `DOS.Scratch`，所以零副作用結論已撤回，
  spec 030 改標 SUPERSEDED；畫面、輸入與事件結論仍有效。
- 第五十階段新增 `-scratch` 與 content-safe `-file-ops`，以正式 scratch-backed 收據重驗：
  `NO`／`YES` 都 shadow `CHARS.DAX` 但沒有 DOS write，四份 scratch 內容皆等於 pristine；
  兩分支進入加入角色功能都沒有角色列並返回相同功能選單。各雙重重播為 316 events，專案
  94 項測試與 dosgolem 正式 test／vet／race 通過，spec 031 已 CONFORMED，本機 dosgolem
  commit 為 `5b5f9b59318033acdd4d444754bb43abc68863d5`，未推其遠端。此路徑使用未用技能點
  離開，不能外推完整配置後的合法角色保存結果。
- 第五十一階段進行中：正常 BIOS 路徑已實際配置完 80 點職業技能與 40 點技術技能，兩者
  歸零後無警告進入身體圖示畫面。第一個完整配置後的保存／名冊 probe 仍沒有 DOS write，
  scratch `CHARS.DAX` 與 pristine 同雜湊並回到空名冊；尚須對齊第 48–50 階段後段事件與
  按鍵時點，未判定為 dosgolem 檔案服務缺口，也尚未形成正式雙重重播或 CONFORMED 規格。
- 第五十二階段已排除後段按鍵時點、身體圖示未移動與已記錄的未實作 DOS／BIOS 服務；
  `-unimplemented`／`-state-out` 的 spec 032／033 已 CONFORMED。完整配置正式雙重重播的
  JSON、framebuffer、scratch 及回讀後 1 MiB memory 一致，但 `SAVE A? YES` 仍無 DOS write，
  Add 仍無角色列。找到的 DGROUP／heap 差異均未被 Add consumer 讀取，原版保存條件仍未知；
  dosgolem 診斷功能在本機 commit `4bb3cc9d83868ea2d827cff33b43e2585c7f16ac`，未推其遠端。
- 第五十三階段已訂正保存選項：由同一 `save-before.state` 直接預設 Enter 才是真正保存，
  會決定性建立 259-byte `A.who` 與 124-byte `A.stf`；Left→Enter 不保存。先前第 49–52 階段
  的 `NO`／`YES` 標籤及零寫檔推論均已追加勘誤。兩路 IP trace 各自雙重一致，保存檔雜湊
  亦一致；完整 memory 因 DOS 取時而尚未證實逐 byte 決定性。下一步以真正保存分支接續
  Add 正常玩家路徑，確認名冊是否顯示角色。
- 第五十四階段已完成保存→Add→加入的正常玩家垂直鏈：Add 先讀 `A.WHO` 的 16-byte 起始區
  與 offset 194 資格 byte，列出角色 `A`；Enter 後顯示 `Loading...Please Wait`，完整讀取
  259-byte `A.WHO` 與兩筆 62-byte `A.stf`，回到 Add 時角色已從可加入名冊移除。兩次完整
  重播的 18-event／2,611-FileOps JSON 在正規化 scratch 路徑後逐 byte 相同，framebuffer
  與保存檔亦相同；未實作服務為空。原空名冊根因已關閉為不保存分支誤標。

下一個前沿決策仍是 2×／3× 輸出倍率；兩者 renderer 能力、倍率中立選單純核心及功能選單／
手冊離線 A/B 都已具備。確認後才能把選定倍率寫入 READY 規格並接入正常玩家路徑 renderer，再做連續幀反白、
轉場清除與同狀態 A/B。3 筆強推論與 `Roll.` 缺頁仍失敗即關閉；runtime 畫面與分頁互動
驗證前，手冊與選單覆繪 DRAFT 不升為 READY。不依賴倍率的目前安全切片是把完整技能配置後
的圖示確認、保存與名冊事件逐項對齊，再重驗合法角色是否可見。

第六十階段已完成手冊覆繪 READY 前置稽核：39 題來源為 35 confirmed、3 strong-inference、
1 unknown；正式事件與譯文各 22 筆，其餘 17 題維持原版英文。正式譯文最長 236 字，均低於
單頁 612 字容量，所以本批不需新增分頁輸入。spec 002 已把正常路徑覆繪、錯答重抽、像素
containment 與同狀態 A/B 正確歸入實作後 CONFORMED；目前唯一 READY blocker 仍是使用者
選定 2×／3×。本輪未修改 dosgolem。

第六十一階段已將手冊單頁容量落成正式資料閘門：`manual_catalog.py` 由 36 欄×17 列導出
612 字上限，612 字通過、613 字失敗即關閉；現有 22 筆正式譯文全部通過。專案回歸增至
103 項並全數通過。本輪沒有新增分頁、截斷或 runtime 行為，dosgolem 未修改；spec 002
仍為 DRAFT，正式倍率仍待使用者選定。

第六十二階段檢視真實手冊畫面後，發現第 17 階段整框 prototype 會遮住原版頁碼、英文標題
與序數，玩家將失去完成原版驗證所需的題目資訊；因此訂正 Phase 60「唯一 blocker 是倍率」
的結論。新的保留題目 prototype 把上方 `[7,312)×[7,72)` 留給原版，只在下方顯示中文；
正文容量為 36×14＝504 字，現有最長 236 字仍單頁。2×／3× 圖均已重生並目視通過。
目前最前沿決策是「保留原版題目」或「整框替換並另設計中文題目提示」；建議前者。使用者
確認前不實作 production presenter，也不將 612 上限改成 504；dosgolem 本輪未修改。

第六十三階段已把性別／職業 exact request 與安全矩形接進 dosgolem 長存 runtime overlay。
正常三 Enter＋Down 路徑在 2×／3× 各兩次均為 24 requests／24 actions、零 miss，終態只保留
職業畫面八個 keys；性別與舊 selected variant 已失效。兩倍率安全矩形外 0 px，原版 raw
framebuffer 全等於既有 class Down 基準。專案 105 項測試與 dosgolem 正式 test／vet／race
通過；dosgolem 本機 commit `e1d2070` 未推遠端。手冊版面與產品預設倍率仍待使用者決定。

第六十六階段已證實角色動態值呈黑是 dosgolem 的 mode 13h BIOS 預設色盤缺口：遊戲只寫
DAC 0–14，讓 index 15 沿用 BIOS 白色。通用修正載入標準 VGA 前 16 色，raw framebuffer、
事件與輸入完全不變；base／`Y`、2×／3× 各雙重重播決定性一致，HP 數值已在 RGBA baseline
成為可見白字。spec 205 已 CONFORMED；完整 DAC 16–255 預設表仍不猜補。產品倍率與手冊
版面仍待使用者決定。

第六十七階段已把角色姓名畫面的固定提示接成 exact runtime request。五鍵正常路徑固定為
183 events／1 request／182 misses；加送玩家 `A` 後為 184／1／183，單 byte 姓名回顯仍
失敗即關閉。兩路各雙重重播的 JSON 與 framebuffer 逐位元一致；本階段未新增安全矩形或
renderer，因此不影響仍待決的產品倍率與手冊版面。
dosgolem 實作已提交於本機 branch，commit `22f46b4`，未推送其遠端。

第六十八階段已將姓名提示接入明示倍率 runtime overlay：提示安全矩形止於 x=128，玩家輸入
始於 x=136。base／輸入 `A` 的 2×／3× 各雙重重播一致；差異只在核准矩形內，輸入欄零差異。
runtime 現在雙向拒絕缺少或孤兒 rectangle。本階段仍未選定預設倍率，也未處理手冊版面。
dosgolem 實作已提交於本機 branch，commit `6e16fe5`，未推送其遠端。

第六十九階段已關閉姓名提示轉場生命週期：`A`→Enter 後通用清除 hook 讓 active keys 歸零，
2×／3× RGBA 等於 baseline；Escape 已訂正為原地重印而非取消，兩次 request 以同 key replace，
終態只留一份 stamp。收據工具現可明示合法空終態 `drew=false`，但仍拒絕缺字或 active-key
不一致；沒有新增姓名專屬清除。本階段仍未選定產品倍率或手冊版面。
dosgolem 實作已提交於本機 branch，commit `8e60489`，未推送其遠端。

第七十階段已把職業技能配置的四個標題、八個一般技能列及兩個已證實 selected identities 接成
exact request。base 為 226／14／212，Down 為 234／16／218；動態點數與未實測 selected
variants 維持 miss。control／catalog 雙重重播的原版語意與 framebuffer 相同。本階段只建立
request，尚未建立安全矩形或繪製技能頁繁中像素。
dosgolem 實作已提交於本機 branch，commit `c4fb58c`，未推送其遠端。

第七十一階段已將上述 14 identities 建立 exact-width 矩形並接入執行期覆繪。
base／Down 的 2×／3× 各雙重重播一致；矩形外與 x≥184 動態數值欄均為 0 px，
原版 framebuffer 及 presentation 欄位外語意與 Phase 70 control 一致。選取列取代與
姓名提示轉場失效均無殘字。產品預設倍率及手冊版面仍待使用者決定。
dosgolem 實作已提交於本機 branch，commit `91407a4`，未推送其遠端。

第七十二階段已將技術技能配置頁接成 exact runtime requests。13 個技能譯名都回到
中文手冊 `SCAN0352_012.jpg` 第 19–20 頁原圖。technical catalog 新增 17 個不重複 identities；
「單項技能上限」與「點數／加值／總計」在兩技能頁是相同 identity，因此共享 career catalog，
不重複定義。base 為 289／32／257，Down 為 297／34／263；control／catalog 的原版語意與
framebuffer 相同。本階段只完成 request，尚未建立技術技能安全矩形或繁中像素覆繪。
<!-- phase-72-dosgolem-commit -->
- dosgolem 本機分支 `buck-rogers-cht-output-overlay` 的第 72 階段提交為 `790a41cbf03d056caedf87f06698f50cae90a8c1`；依專案規範僅保留於 `workplace/dosgolem`，未推送遠端。

第七十三階段已將技術技能配置的 17 個專屬 identities 與兩個 career 共享標題矩形接入 2×／3×
runtime overlay。首次沿用 request 停止點時人工圖像發現 selected stamp 尚為 `Pending`；延後至
下一穩定 frame 後繁中正常顯示，規格已把穩定 frame 與目視驗收列為必要條件。base／Down 的
兩倍率各雙重重播一致，矩形外與動態欄 0 px，原版 framebuffer 與語意不變。產品預設倍率及
手冊版面仍未替使用者決定。
dosgolem 本機分支提交為 `2d8561c8a87e6868c8e0d647fbcf69e6c18169c0`，未推送其遠端。

第七十四階段已證實技能頁底部五個操作標籤不經現有高階 dispatcher，而是
由上層 `37F1` caller 逐字進入 `0763:026B`，再由 `0763:1809` 畫 8×8 glyph。
職業三標籤與技術五標籤的初始／Right 焦點路徑、幾何、caller 與色彩已收進
content-safe 清冊；未觀測到獨立 disabled variant，維持 unknown。dosgolem spec 213 是
DRAFT，下一階段應實作 Buck Rogers 專屬 guarded glyph-event watcher，不能直接當成
原有字串事件。dosgolem 本機提交為 `7d8ca0b`，未推送其遠端。產品倍率與
手冊版面仍未決定。

第七十五階段已將技能頁底部逐字路徑接成 dosgolem `ActionBarWatcher`。
screen anchor 來自 exact 技能畫面標題，technical 只 allowlist 兩個 Phase 72 已證實的
career 共享標題；每字通過 `0763:026B` caller、mode=1、repeat=1、色彩、座標、
SS/SP far-return guard 與完整雜湊後才產生 content-safe event。八條正常路徑雙重播
均為 0 miss、0 drop，watcher/control framebuffer 與其餘語意收據一致；spec 213 已
CONFORMED。底部操作列仍未接繁中 request／overlay，disabled 仍是 unknown；下一個
不依賴產品倍率的安全切片是建立繁中 catalog 與 typed display requests。dosgolem
本機提交為 `356848c`，未推送其遠端。
