# 第三十階段：種族選單反白與文字安全矩形生命週期

## 狀態

完成

## 本輪目標

由第 29 階段正常 Enter 路徑繼續，以原版正常方向鍵移動種族選單游標，量測選取反白時的
dispatcher／guarded post-call、畫面色號、座標、原文矩形與重繪順序，補齊玩家可見中文覆繪
必需的 selection lifecycle 與 logical text-safe rectangle 證據。

## 範圍

- 以 dosgolem 固定狀態與 BIOS 鍵盤輸入走正常玩家路徑；不使用 memory poke、傳送或改寫
  原版選項狀態。
- 若既有 receipt command 只能排一鍵，先為診斷工具加入可重播、可測試的多筆排程 BIOS key，
  不把測試輸入功能混入 `MenuRequestWatcher`。
- 先重生 Enter 到穩定 `PICK RACE`，再送 Down，必要時送 Up 回到原選項；記錄所有完成文字
  事件、VRAM 變更及按鍵排入／消費區間。
- 判定反白是重畫文字、改 palette、矩形填色或其他機制；只把動態證實的 event identity、
  logical rectangle 與失效順序寫入 DRAFT。
- 建立九個既有選單事件的 logical text-safe rectangle 清冊，驗證繁中譯文在一行一格字模
  版面下不侵入相鄰 row；不依此選定 2×／3×。
- dosgolem 如有工具變更則建立本機 commit、不推其遠端；專案 main 推送並更新 Issues #5、#8。

## 不在本輪範圍

- 不選 2×／3×、不建立 production `xlate.Stamp`、不畫中文或宣稱視覺 parity。
- 不確認種族選項、不建立角色、不研究 transaction／遊戲規則。
- 不從單一 Down／Up 樣本外推其他選單、滑鼠、存讀檔或訊息捲動。

## 驗收條件

- 正常 Enter → 穩定種族選單 → Down（及必要的 Up）可由同一固定狀態決定性重播兩次。
- 收據能區分 steady frame、按鍵後舊選項失效、新選項反白與完成 post-call；所有位址標明
  dosgolem runtime `segment:offset`。
- 反白事件的 caller、length／SHA-256、色號、row／column 與 VRAM 變更都有 content-free
  收據；未證實機制保持 unknown，不以畫面猜測冒充。
- `text/menu-text-safe-rects.tsv` 或等價正式資料逐 event key 定義 320×200 logical rectangle、
  單行容量與 overflow policy；驗證 key 完整、矩形合法、互不侵入相鄰 row 且譯文可容納。
- 所有新增診斷工具、資料 verifier、專案測試與相關 dosgolem 測試通過。
- Docker 清理與擁有權檢查正常；兩個工作樹乾淨，main 已推送，Issues #5、#8 已更新。

## 預定交付物

- 可重播 Down／Up selection 收據與必要的 dosgolem 診斷工具
- `text/menu-text-safe-rects.tsv` 與失敗即關閉 verifier／測試
- `docs/re/phase-30-race-selection-highlight-lifecycle.md`
- 選單覆繪 DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

- 同一固定狀態的 Enter→Down→Up 兩次重播產生完全相同 13-event 收據；Down 先 normal
  redraw Terran、再 selected redraw Martian，Up 反向復原。
- 相同 #100,600,000 終點的 steady／Down-only 差異恰為 `(24,24)–(79,39)`、832 pixels；
  Up 後 64,000-byte framebuffer 逐位元等於 steady。
- 新增四筆 content-free selection lifecycle identity、正式 logical text-safe rectangle、
  receipt／geometry verifier；清除範圍與 col 3 中文 anchor 已分離。
- 專案 39 項資料測試、dosgolem 全部正式 packages test／vet 與相關 race detector 通過。
- dosgolem 本機 commit 為 `d55a4c84c3474034257cddf58d6fa32cff3d60d4`，未推送其遠端。
