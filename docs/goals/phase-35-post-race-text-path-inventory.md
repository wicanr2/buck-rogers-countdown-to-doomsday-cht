# 第三十五階段：選定種族後的下一畫面文字路徑清冊

## 狀態

完成

## 本輪目標

由第 30–33 階段相同的穩定 `PICK RACE` 原版 state，透過正常 BIOS Enter 選定目前種族，
以 dosgolem 追蹤 `0763:0424` guarded post-call、矩形清除與終點 framebuffer，辨識下一個
玩家可見畫面的文字事件與生命週期，擴張 Issue #4 的印字路徑證據。這一輪只建立
content-safe 原版清冊與 DRAFT 證據，不翻譯、不覆繪，也不猜測畫面語意。

## 範圍

- 沿用已固定雜湊的 `PICK RACE` state；先用可丟棄 probe 找出安全 Enter step、停止條件與
  下一畫面穩定窗口，不直接把 probe 移入 production。
- 記錄選定種族前後的 BIOS input、`0763:0424` entry／guarded post-call、caller、原文字串
  length／SHA-256、背景／前景色號、row／column、矩形清除與絕對 step。
- 輸出只保存 content-free metadata；原文全文、原版 framebuffer 與 palette 留在被忽略的
  `workplace/`。
- 至少重播兩次並驗證收據與終點 framebuffer 逐 byte 相同；列出新事件、重用事件及未知
  輸出路徑。
- 若需新增正式診斷命令，先建立 dosgolem READY 規格，再實作；完成後更新證據、DRAFT、
  `CONTEXT.md`、`WORKLOG.md` 與索引，推送 `main` 並更新 Issues #4、#7。

## 不在本輪範圍

- 不建立或修改繁中譯文、字型、text-safe rectangle、renderer 或正式 catalog。
- 不選擇 2×／3×，不接正常玩家路徑中文覆繪。
- 不修改角色建立規則、種族選擇、輸入、亂數、存檔或原版記憶體。
- 不把單一選定種族路徑外推為所有種族、性別、職業或角色建立流程已覆蓋。

## 驗收條件

- Goal 已在 probe 前建立並完整讀回。
- 輸入 state、原版檔案、工具版本與位址空間有固定雜湊；所有結論標示證據等級。
- 正常 BIOS Enter 路徑走到穩定下一畫面，兩次重播的 content-safe 收據與終點 framebuffer
  逐 byte 相同，且 recorder 零 pending／drop。
- 每筆新事件保留完整 runtime identity；verifier 對事件數、順序、雜湊、座標、色號與
  時序失敗即關閉。
- dosgolem 正式套件 test／vet、相關 race detector 與專案 verifier 全部通過。
- Docker、擁有權與兩工作樹狀態已核對；dosgolem 僅本機提交，專案 `main` 已推送且
  Issues #4、#7 已更新。

## 預定交付物

- content-safe 的 post-race 原版文字事件收據與 verifier
- `docs/re/phase-35-post-race-text-path-inventory.md`
- 選單覆繪 DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

2026-09-21 完成。固定雙 Enter 正常路徑重播兩次，14-event JSON 與終點 framebuffer 均逐
byte 相同，命令成功退出且零 pending／drop。新增四筆性別畫面 content-safe identity、嚴格
verifier 與 dosgolem CONFORMED spec 016；專案 47 項測試、dosgolem 正式 packages
test／vet 及相關 race detector 全部通過。dosgolem 本機 commit 為
`7009315c5a04981eb1b048e7bba34a0b932fbf6d`，未推其遠端；未翻譯、未覆繪、未選倍率。
