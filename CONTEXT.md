# 目前狀態

更新：2026-09-21

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

下一個前沿決策仍是 2×／3× 輸出倍率；兩者 renderer 能力、倍率中立選單純核心及功能選單／
手冊離線 A/B 都已具備。確認後才能把選定倍率寫入 READY 規格並接入正常玩家路徑 renderer，再做連續幀反白、
轉場清除與同狀態 A/B。3 筆強推論與 `Roll.` 缺頁仍失敗即關閉；runtime 畫面與分頁互動
驗證前，手冊與選單覆繪 DRAFT 不升為 READY。不依賴倍率的下一個安全切片是職業技能點配置
畫面的方向鍵／加減／確認／返回生命週期。
