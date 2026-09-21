# 第八十七階段：手冊多行 presenter 純核心

日期：2026-09-21  
dosgolem 本機分支：`buck-rogers-cht-output-overlay`  
dosgolem 本機提交：`21c9295c90fac44b5852fd5934a6d027342cde24`（未推送）  
狀態：**CONFORMED（純核心；非原版畫面 A/B）**

## 範圍與前置

本階段消費第八十六階段已 CONFORM 的 answer-free `ManualPresentationEvent` value queue，
在 dosgolem 的 `apps/buckrogers` 加入可注入字型的手冊多行 RGBA presenter。它只讀 indexed
framebuffer、palette、正式 layout、catalog、font 與 lifecycle value；沒有連接 command、正常
遊戲 runtime、host 面板、DOS VRAM、BIOS 輸入、答案比較、檔案或存檔。

正式 `text/manual-overlay-layout.tsv` 的唯一列保持：clear `[7,312)×[72,184)`、文字 anchor
`(16,72)`、36 欄×14 行、504 rune、每行 8 logical pixel、`single-page-reject`、`confirmed`。
上方原版頁碼、英文標題與序數不在本 core 的繪製範圍。

## 已符合的純核心契約

- `LoadManualOverlayLayout` 只接受唯一的正式 TSV schema 與數值；schema、列數、幾何、容量、
  overflow 或 evidence 任一漂移皆失敗即關閉。
- `NewRuntimeManualOverlay` 預先驗證全部手冊譯文：必須是非空有效 UTF-8、最多 504 rune，且
  每個 rune 都有 16×16 font 的有效 32-byte glyph；倍率只能是 2 或 3。
- `begin` 僅接受嚴格遞增、非零 generation；pending `clear` 保持等待；visible `clear` 移除
  自己的兩個 layer；同 generation 重顯、stale request、catalog miss、零／未知事件都不產生
  partial stamp。
- 每個 request 建立 14 個 305×8 背景 stamp 與 14 個 36-cell 文字 stamp。背景 layer 先畫，
  文字 layer 後畫，故未用文字 cell 與 `(7..16)`／`[304..312)` 的左右餘白都會清除原版英文。
- 2×與3×從相同 320×200 indexed baseline 生成 RGBA；16×16 glyph 的 output-pixel offset 分別是
  0 與 4，沿用既有 `xlate.Layer.Draw` 及選單覆繪的已驗證置中契約。

## 隔離驗證收據

在 Docker `golang:1.24-bookworm` 中，以唯讀專案掛載、`--network none`、非 root UID 執行：

```text
go vet ./apps/buckrogers
go test -race ./apps/buckrogers
```

兩者均以 exit 0 完成。單元測試使用 fixture font 和 synthetic indexed frame，驗證：14 行與
504 rune row-major 分配、2×／3× RGBA 尺寸、clear rect 以外零像素差異、兩側餘白清除、
begin → pending clear → request → visible clear → 新 generation、catalog miss、stale request、
錯誤 layout／font／scale／缺字及 defensive-copy。這是 renderer 內部收據，**不是**原版／繁中
same-state 畫面 A/B，也不代表手冊已在正常遊戲中顯示中文。

## 後續 gate

仍須另建 DRAFT，才可將 core 接到實際 runtime：建立可重生且授權可追溯的 691 glyph 正式
GOLEMFNT、載入正式 TSV／catalog、消費 `PresentationEvents()`、接入選定後的 2×／3× active
scale，並對第一題與答錯重抽取得 normal-player same-state A/B。未完成前，規格 005 維持 DRAFT。
