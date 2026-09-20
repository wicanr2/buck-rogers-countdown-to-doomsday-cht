# 工作歷程

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
