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

下一個不依賴倍率決策的工作，是依來源對照逐字校訂首批繁中段落並建立可顯示 catalog，
同時保留 3 筆強推論與 `Roll.` 缺頁的失敗即關閉狀態。段落完整性、錯答 generation 失效與分頁 prototype 驗證前，
手冊覆繪 DRAFT 不升為 READY。
