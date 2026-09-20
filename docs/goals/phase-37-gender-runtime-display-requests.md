# 第 37 階段 Goal：性別選擇繁中執行期顯示請求

狀態：完成

## 目標

把第 35、36 階段已證實的性別選擇文字 identity，經正式繁中 catalog 與完整事件身分比對，
接成 dosgolem 執行期顯示請求。固定正常玩家路徑須涵蓋初始畫面、Down、Up 與 Escape 前的
重畫事件；不載入字型、不繪圖，也不替使用者決定 2×／3×。

## 前置證據

- 性別畫面初始四筆 identity：`text/post-race-events.tsv`。
- Down／Up／Escape 生命週期：`text/gender-selection-events.tsv`。
- 正式原版收據與 framebuffer：`workplace/probe/phase36-*`。
- dosgolem 工作分支：`buck-rogers-cht-output-overlay`。

## 工作項目

- [x] 從本目錄中文說明或既有可信來源核對性別提示及兩個選項的繁體中文用語。
- [x] 建立嚴格、無孤兒鍵的性別繁中 catalog 與專案端正反向驗證。
- [x] 先建立 dosgolem 規格並完成證據審查，確認事件、catalog、失敗模式與不繪圖邊界達 READY 後才實作。
- [x] 擴充 Buck Rogers 純核心，以完整 identity 精確解析性別畫面的顯示請求。
- [x] 將既有 guarded post-call watcher 接到性別 catalog；未知或不完整事件必須失敗即關閉。
- [x] 以正常 Enter→Enter→Down→Up 路徑重播兩次，驗證事件與繁中顯示請求決定性一致。
- [x] 驗證 Escape 的取消反白事件不會跨畫面保留錯誤請求或污染返回功能選單 generation。
- [x] 更新研究紀錄、`CONTEXT.md`、`WORKLOG.md` 與文件索引。
- [x] 在 Docker 內完成專案測試、dosgolem 正式套件測試、靜態檢查與競態檢查。
- [x] 檢查容器生命週期、root-owned 殘留及兩個工作樹狀態。
- [x] 提交 dosgolem 本機分支；提交並推送專案 `main`。
- [x] 使用真正的主機 `gh` 更新 GitHub Issues #7 與 #8。

## 完成條件

- 正式繁中 catalog 的每個鍵都有可回查來源，且與已證實事件雙向完整對應。
- 初始 normal、selected male、Down selected female、Up selected male 等已證實 variant 都只由完整
  length／SHA-256／caller／色號／座標命中，不能只靠文字內容或座標。
- 真實正常玩家路徑兩次重播的事件／請求收據逐位元一致，零 pending、drop 與 catalog miss。
- Escape 後不沿用性別畫面的舊 generation；返回功能選單仍維持既有行為。
- 不含原版英文全文、不送鍵、不改原版記憶體／規則／存檔、不載入 renderer，也沒有隱含預設倍率。
- 專案 `main` 已推送，Issues #7、#8 已留下可追溯摘要。

## 不在本階段範圍

- 玩家可見的繁中像素覆繪。
- 2×／3× 倍率決策。
- Enter 確認性別後的角色建立流程。
- 手冊段落分頁與答案輸入。
- 發行包或原版素材散布。
