# 目前狀態

更新：2026-09-20

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

下一個前沿決策仍是 2×／3× 輸出倍率；兩者的 renderer 能力都已具備，確認後才能把選定倍率
接入正常玩家路徑覆繪。不依賴倍率的下一個技術切片是正式 dispatcher／guarded post-call
接線證據與測試。3 筆強推論與 `Roll.` 缺頁仍失敗即關閉；畫面 A/B 與分頁互動驗證前，
手冊覆繪 DRAFT 不升為 READY。
