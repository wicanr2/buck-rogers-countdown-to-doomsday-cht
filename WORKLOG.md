# 工作歷程

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
