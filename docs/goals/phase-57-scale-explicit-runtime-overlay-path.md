# 第五十七階段：明示倍率的執行期繁中覆繪路徑

狀態：完成

## 目標

將第 56 階段正常保存→功能選單→名冊→加入隊伍的 typed 繁中顯示請求，接到 dosgolem
既有 `apps/buckrogers` 倍率中立覆繪核心與 `xlate` renderer，在不設定產品預設倍率的前提下，
分別以明示 2×／3× 重生玩家可見繁中 framebuffer，證實英文墨跡清除、文字安全矩形、動態
姓名保留與遊戲語意隔離。

## 範圍

- 先建立 dosgolem DRAFT 規格，盤點既有 overlay core、request watcher、xlate layer、字型與
  framebuffer 輸出 API；只有證據完整後才升 READY 實作。
- 建立由多份既有 UTF-8 TSV catalog 合併字元的決定性 GOLEMFNT 輸入，不複製譯文權威；
  menu 與 roster catalog 的全部譯文字元都必須有字模。
- 正式 runtime／診斷命令要求明示 `scale=2` 或 `scale=3`；缺省、0、1、4 或其他值失敗即關閉，
  不把任一倍率設為產品預設。
- 在 guarded post-call 後，只對 exact catalog request 清除該事件的 text-safe rectangle 並繪製
  繁中；四筆動態姓名 miss 維持原版像素，不得被清除或替換。
- 由同一正常玩家路徑分別雙重重播 2×／3×；驗證決定性、中文 ink containment、清除後無
  英文殘墨、畫面邊界、動態姓名區域、FileOps、writes、保存檔與輸入完全不變。
- 完成後更新研究、CONTEXT、WORKLOG 與 dosgolem spec；提交 dosgolem 本機分支與專案
  `main`，只推送專案 `main`，並回寫 GitHub Issues。

## 不在本階段

- 不替使用者選定 2× 或 3×，不建立預設倍率、不宣稱任一方案已正式採用。
- 不翻譯四筆動態姓名，不改原版 EXE、存檔格式、名冊資格、加入隊伍控制流或輸入排程。
- 不擴張到尚無 exact catalog 的角色建立資料頁、技能頁或加入後冒險畫面。

## 成功定義

1. 規格依 `RE → DRAFT → READY → implementation → same-state verification → CONFORMED` 完成。
2. 正常路徑 14 筆靜態事件各形成一次覆繪動作；四筆 dynamic miss 零覆繪，且無 pending、
   drop、非預期 miss 或前一請求沿用。
3. 2×／3× 各兩次輸出逐 byte 相同；每筆中文 ink 位於 text-safe rectangle，原英文墨跡已
   清除，動態姓名像素與無覆繪 baseline 對應區域一致。
4. 覆繪前後 events、BIOS input、FileOps、writes、保存檔及原版 machine state 一致；差異只
   存在於明示倍率的輸出 framebuffer／presentation layer。
5. 多 catalog 字型輸入、非法倍率、缺字、溢位、動態姓名誤清除及 framebuffer 越界均有
   失敗即關閉測試；專案與 dosgolem test／vet／race 全部通過。
6. 兩個工作樹乾淨、專案 `main` 已推送、Issues 已更新；dosgolem commit 只留本機分支。

## 退出條件

- 若既有 overlay core 缺少名冊畫面的可靠 text-safe rectangle 或失效生命週期，回到 RE／
  DRAFT 補證據，不以目測座標硬接 production。
- 若覆繪會修改 machine VRAM 並影響後續原版讀回，改為明示 presentation snapshot 層；不得
  讓譯文污染遊戲語意。
- 若 2×／3× 任一方案不符合幾何安全，保留失敗證據並停止該方案，不替使用者默認另一方案。
