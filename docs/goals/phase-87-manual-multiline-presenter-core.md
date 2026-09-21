# 第八十七階段：手冊多行 presenter 核心

狀態：完成（純核心；非原版畫面 A/B）

## 目標

以正式 `manual-overlay-layout.tsv` 與已 CONFORM 的 presentation lifecycle queue 建立
`apps/buckrogers` 可注入字型的 14 行手冊 RGBA presenter 核心。它必須在 2×／3× 明示倍率下
按 36×14／504 格 row-major 佈局、清除舊 generation，並對無效 layout、字型、倍率、generation
與 translation 失敗即關閉；本階段不接正常遊戲 CLI 或正式字型。

## 已確認前提

- 正式正文矩形為 `[7,312)×[72,184)`，文字從 `(16,72)` 依 36 欄×14 行、每列 8 logical pixel
  佈局，容量 504；Python verifier 已固定 schema 與 504／505 邊界。
- dosgolem spec 216 的 `ManualPresentationEvent` 已 CONFORM：exact begin、active-context clear、
  catalog-hit request 都帶 generation，並不帶 machine／input reference。
- `xlate.Layer` 與 `ScaleIndexedRGBA` 能只讀 indexed framebuffer／palette 並在 2×／3×生成 RGBA；
  現有 `RuntimeMenuOverlay` 是單列 adapter，不能直接重用。

## 範圍

- 建立並審查一份 dosgolem READY 規格，明定 layout TSV loader、typed constructor、row-major stamp
  builder、lifecycle event consumer、draw／clear 行為、失敗模式與純核心驗收。
- 新增手冊專用 layout loader、runtime core 與單元測試；constructor 只接受 16×16 font 與 2／3 倍率，
  任何正式 catalog rune 缺字時拒絕整個 presenter。
- 以 fixture font／synthetic framebuffer 驗證 14 行 containment、清除、generation 取代、pending clear、
  catalog miss／stale request、非法輸入與 2×／3× RGBA；不聲稱為原版畫面 A/B。

## 不在本階段

- 不建置或散布正式 GOLEMFNT、第三方字型、原版或手冊掃描。
- 不把 core 接入 `cmd/buckrogers-receipt`、正常遊戲 runtime、host 視窗、倍率 Apply 或玩家輸入。
- 不修改原版 DOS framebuffer、VRAM、記憶體、答案驗證、存檔、BIOS／DOS keyboard 或 mouse。

## 完成條件

1. READY 規格完整描述已證實幾何、typed state、輸出、失敗即關閉與權利邊界；production code 只在
   READY 後進入本機 dosgolem branch。
2. core 單元測試證實 14 行、504 格、2×／3×、begin／clear／request lifecycle、value isolation 與
   layout／font／scale／generation 負向案例。
3. core 沒有原版 machine／input 依賴且不產生可散布原作素材；專案資料驗證、main 推送與相關
   GitHub Issue 回寫完成。

## 退出條件

- 若固定 layout 與 xlate cell／glyph 行為無法在同一 renderer 中滿足 containment，維持 DRAFT，
  先做可丟棄 prototype；不得偷偷變更 36×14、字型縮放或清除矩形。
- 若正式 glyph 缺漏、字型授權或正常玩家畫面驗證需要新增資料，標為下一條獨立 gate；不得以
  synthetic fixture 宣稱手冊已中文化。
