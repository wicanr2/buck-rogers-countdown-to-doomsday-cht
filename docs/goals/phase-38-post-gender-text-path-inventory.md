# 第 38 階段 Goal：確認性別後的下一畫面文字路徑清冊

狀態：完成

## 目標

從第 35–37 階段相同固定 state，以正常 BIOS Enter 依序進入種族選擇、接受預設種族、接受
預設性別，量測下一個玩家可見畫面的文字事件與 framebuffer。先建立 content-safe 原版證據，
不在觀測前假定畫面名稱或角色建立規則。

## 固定輸入

- dosgolem 工作分支：`buck-rogers-cht-output-overlay`。
- state：`workplace/probe/after-bios-space-100m.state`。
- 原版目錄：`workplace/original/BRcdoom/`，唯讀掛載到 `/orig`。
- 第一個 Enter：#100,010,000；第二個 Enter：#100,240,000。
- 第三個 Enter 必須由可丟棄探測先確認安全時間，再固定正式排程。

## 工作項目

- [x] 以可丟棄 probe 確認第三個 Enter 的安全時間、轉場邊界與下一畫面事件數。
- [x] 以原版 bytes／雜湊核對新增事件的語意角色，但正式清冊不得保存原版英文全文。
- [x] 建立 dosgolem 診斷收據規格；若無需新命令能力，不為湊 commit 複製工具程式碼。
- [x] 正式路徑獨立重跑兩次，確認 JSON 與 framebuffer 可逐位元重生。
- [x] 建立新事件 inventory、嚴格 verifier 與負向測試。
- [x] 明列已證實、強推論與仍未知的角色建立範圍，不外推其他種族／性別分支。
- [x] 更新研究紀錄、舊規格回填、`CONTEXT.md`、`WORKLOG.md` 與索引。
- [x] 在 Docker 內完成專案測試、dosgolem 正式套件測試、靜態檢查與競態檢查。
- [x] 檢查容器生命週期、root-owned 殘留與兩個工作樹。
- [x] 提交 dosgolem 本機分支（若有規格或程式變更）；提交並推送專案 `main`。
- [x] 使用真正的主機 `gh` 更新 GitHub Issues #4 與 #8。

## 完成條件

- 第三個 Enter 使用正常 BIOS 輸入，沒有 direct-entry、狀態注入或自動選答。
- 兩次正式收據與 framebuffer 各自逐 byte 相同，並固定輸入／命令／原版雜湊。
- 新增事件以完整 length／SHA-256／caller／色號／座標／step 驗證，且不保存原版全文。
- 文件只宣稱實際量到的單一路徑，不把畫面相似性當成其他分支證據。
- 本階段不加入譯文、renderer 或倍率預設，不改原版 EXE、資料、規則或存檔。
- 專案 `main` 已推送，Issues #4、#8 已留下可追溯摘要。

## 不在本階段範圍

- 新畫面的繁中譯文與版面。
- 方向鍵、Escape 或下一次確認後的完整生命週期。
- 2×／3× 倍率決策與玩家可見覆繪。
- 手冊段落分頁、答案輸入或角色規則修改。
- 發行包與原版素材散布。
