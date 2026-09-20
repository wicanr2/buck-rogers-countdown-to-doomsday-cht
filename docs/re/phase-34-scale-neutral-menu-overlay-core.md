# 第三十四階段：倍率中立的功能選單覆繪核心

## 結論

第 32 階段診斷命令內已驗證的 stamp 建構、字模 ink 計算與安全矩形 containment，已依
dosgolem READY 規格移入 `apps/buckrogers` 正式純核心。核心沒有預設倍率；呼叫端必須明示
正整數 scale，而 2×／3× 由同一 API 驗證。這沒有替使用者選擇正式產品倍率，也尚未把
renderer 接到正常玩家路徑。

## 規格與實作

- dosgolem 規格：`docs/spec/015-buck-rogers-menu-overlay-core.md`，先達 READY 才實作，驗收後
  標為 CONFORMED。
- 基準 dosgolem commit：`41917c85007efe17154cb92422cba3fe6539ad88`。
- 本階段 dosgolem 本機 commit：`64b15779edc9d5be35e1acba0f854ba022008511`；未推送 dosgolem
  遠端。
- 正式核心／測試 SHA-256：
  `f7b442e6d3d234b946a629e2c889e090ecc22eb346f53116322422d48b45ddee`／
  `75fafe6115aabe5525dfd39238fdafc6b7491ad4399fe158bb20731abc7eac52`。
- 改用核心後的診斷命令 SHA-256：
  `c2e2e1e2e385c86a2b70224777d315319a7e44d544dd117033a4623ef57310bd`。

`BuildMenuOverlay` 接受 typed menu entry、16×16 GOLEMFNT、256 色 8-bit RGB palette 與明示
倍率，回傳 `xlate.Layer` 及不含譯文全文的逐事件幾何。它失敗即關閉：拒絕無效倍率／字型、
空或無效譯文、缺字、容量／overflow 不符、越界、空 ink、矩形重疊與重複 event key；任一
事件失敗時不回傳部分 layer。

原文清除矩形仍從 logical `x` 起，繁中 anchor 可位於較右的 `draw_x`；核心以全形空白格
保存這段 offset。色彩只取原版事件的 palette index，因此 selected row 的 index 15 背景與
index 0 字形在現有 palette 都是黑色時，核心保持黑底黑字，不增補反白或游標。

## 固定輸入與重生結果

沿用第 32 階段相同輸入：

- steady／Down indexed framebuffer：
  `d0f70a73…c1cd`／`efaa3d88…78d0`；
- palette：`04579650…64eb`；GOLEMFNT：`553df09b…fe7`；
- events／rectangles／translations：`973a6a1e…da2e`／`3e37efca…982f`／
  `ca331983…8077`。

steady／Down × 2×／3× 四組均重新執行完整命令。新產生的繁中 PNG、base PNG 與 JSON
逐 byte 等於第 32 階段 `output/a/` 基線；JSON SHA-256 保持：

| 畫面 | 2× | 3× |
| --- | --- | --- |
| steady | `ae796fc1…ed13` | `06c342ab…97140` |
| Down | `0e9ee862…6d3` | `2c0dd1d0…758` |

新收據只保存在被 Git 忽略的 `workplace/phase34/output/`。原版 framebuffer、palette、字型
二進位與圖片均未加入版控。

## 驗證與證據等級

- **已證實**：純核心對 2×／3× 產生與既有診斷命令逐位元相同的四組輸出。
- **已證實**：核心不含預設倍率，且 selected 黑底黑字、prefix anchor、缺字、倍率、字型
  尺寸、容量、越界、overflow、重疊、重複事件及原子失敗均有單元測試。
- **已證實**：排除既有非正式 `workplace/` 草稿後，dosgolem 全部正式 packages test／vet，
  以及 `apps/buckrogers`／診斷命令 race detector 通過。
- **未知／未完成**：正式產品倍率、`TextRecorder`／`MenuWatcher` 到本核心的 runtime 接線、
  `Layer.Frame` 失效、轉場連續幀、存讀檔後重建及手冊段落覆繪。

因此本階段只把已證實離線規則收斂成唯一正式純核心；不能宣稱功能選單已在玩家路徑顯示
繁中，也不改變第 25 階段倍率決策仍 pending 的事實。
