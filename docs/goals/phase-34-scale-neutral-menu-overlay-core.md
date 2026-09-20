# 第三十四階段：倍率中立的功能選單覆繪核心

## 狀態

完成

## 本輪目標

把第 27–33 階段已證實的功能選單事件、顯示請求、文字安全矩形與 selected 黑底黑字
契約，整理成一份不選定產品倍率的 dosgolem READY 子規格，並將第 32 階段診斷命令內
已驗證的純覆繪邏輯移入 `apps/buckrogers` 正式核心。核心必須由呼叫端明示 2× 或 3×，
不得暗定產品預設值，也不得在本輪接入正常玩家路徑。

## 範圍

- 盤點 `cmd/buckrogers-overlay-prototype` 與 `apps/buckrogers` 的現況，辨識可移入正式核心的
  遊戲專屬 renderer 契約；通用 glyph rasterization 繼續留在 `xlate`。
- 建立 dosgolem READY 規格，固定 typed input、原文清除矩形、繁中 anchor、安全矩形、
  normal／selected 色彩、倍率參數、失敗模式與輸出邊界。
- 實作純函式／純型別核心；呼叫端必須明示正整數倍率，本輪驗收至少涵蓋 2× 與 3×。
- 以第 32 階段 steady／Down 真實 framebuffer、正式 catalog 與字型重生 A/B，確認輸出與
  既有收據一致，且沒有安全矩形外差異、缺字或事件重疊。
- 更新專案證據、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；完成後推送 `main` 並更新
  Issues #5、#7。

## 不在本輪範圍

- 不替使用者選擇 2×／3×，不建立預設倍率、不宣稱第 25 階段完成。
- 不把 renderer 接到 `TextRecorder`／正常玩家路徑，不升級整份選單覆繪規格為 READY。
- 不處理手冊段落分頁、其他選單、劇情／戰鬥文字、存讀檔或發行封包。
- 不改原版 EXE、遊戲資料、規則、字串比較、存檔或輸入。

## 驗收條件

- Goal 已於程式／規格變更前建立並完整讀回。
- dosgolem 子規格在實作前達 READY，且明列證據等級、位址空間、輸入雜湊、失敗模式、
  權利邊界與同狀態驗收方法。
- 正式核心沒有隱含倍率；2×／3× 都由相同 API 通過單元測試與真實 framebuffer 收據。
- 第 32 階段診斷命令改用正式核心，不保留第二套相同行為；輸出逐 byte 與既有基線一致。
- dosgolem 正式套件 test／vet、Buck Rogers race detector 與專案 verifier 全部通過。
- Docker、擁有權與兩工作樹狀態已核對；dosgolem 僅本機提交，專案 `main` 已推送且
  Issues #5、#7 已更新。

## 預定交付物

- dosgolem `apps/buckrogers` 倍率中立覆繪核心與測試
- dosgolem 規格與索引更新
- `docs/re/phase-34-scale-neutral-menu-overlay-core.md`
- 選單覆繪 DRAFT、`CONTEXT.md`、`WORKLOG.md` 與本索引更新

## 完成紀錄

2026-09-21 完成。dosgolem spec 015 先達 READY，實作與真實回歸通過後標為 CONFORMED。
正式純核心沒有預設倍率；steady／Down × 2×／3× 的繁中 PNG、base PNG 與 JSON 全部逐
byte 等於第 32 階段基線。全部正式 packages test／vet 與兩個相關 race detector 通過。
dosgolem 本機 commit 為 `64b15779edc9d5be35e1acba0f854ba022008511`，未推其遠端；未接
正常玩家路徑，2×／3× 決策仍 pending。
