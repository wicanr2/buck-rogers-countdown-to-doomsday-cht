# 工作歷程

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
