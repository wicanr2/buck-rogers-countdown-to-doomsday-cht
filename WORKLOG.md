# 工作歷程

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
