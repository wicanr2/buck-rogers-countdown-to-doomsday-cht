# 第五十一階段：完整技能配置與合法角色保存

狀態：進行中

## 目標

由正常角色建立路徑實際配置完全部職業與技術技能點，不使用未用點數確認捷徑，再完成圖示與
保存流程，驗證合法角色的 scratch 寫入、名冊可見性及第一個可判定的加入結果。

## 範圍

- 從固定 state 走完整正常 BIOS 前綴，以方向鍵與 Enter 實際分配全部 80 點職業技能與 40 點
  技術技能；先探測各列可接受的點數，不假設單列上限或職業規則。
- 以畫面剩餘點數、事件 identity、Escape 結果與 framebuffer 證明點數已用完；不以固定按鍵
  次數本身宣稱配置完成。
- 經正常圖示確認與保存選項進入功能選單，再以 scratch-backed FileOps、檔案 manifest 與
  加入角色畫面驗證保存及名冊結果。
- 正式分支從相同 state 與空白 scratch 獨立重播兩次，固定 BIOS 排程、事件 step、原版與
  命令雜湊、64,000-byte indexed framebuffer 及檔案差異。
- 建立 dosgolem 診斷規格、content-safe 清冊、嚴格 verifier、正反例測試與研究文件。
- 完成後提交 dosgolem 本機分支、推送專案 `main` 並更新 GitHub Issues。

## 不在本階段

- 不推導所有技能的遊戲效果、最大值公式或最佳配點。
- 不使用 direct-entry、記憶體／點數注入、自動改值或測試跳關。
- 不解析或散布完整角色檔內容；只保存檔名、大小、雜湊與必要差異 metadata。
- 不翻譯技能／名冊畫面、不接 renderer、不選定 2×／3×。

## 成功定義

1. 正常玩家操作證實職業與技術技能的剩餘點數皆歸零，並在沒有未用點數警告下離開。
2. 保存後 scratch 產物及 FileOps 可重播，pristine original 維持不變。
3. 新角色在加入角色流程的可見性與至少一條選取／加入或返回結果獲得可判定證據。
4. 正式分支雙重重播的 JSON、framebuffer、manifest 與檔案雜湊逐 byte 相同。
5. verifier 對輸入、事件、step、identity、畫面、檔案差異、原版與命令雜湊漂移失敗即關閉。
6. dosgolem 規格達 CONFORMED；專案測試、正式 Go packages、`go vet` 與相關 race detector
   通過。
7. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 若單列達上限，改由正常 Down 移至下一列繼續，不猜測或繞過限制。
- 若點數歸零後的離開控制與先前不同，只保存實測路徑並更新規格，不沿用未用點數流程。
- 若合法保存暴露新的 DOS 檔案服務缺口，先回填 dosgolem 並重生正式收據，不用 DOSBox
  取代最終證據。

## 2026-09-21 進度收據

- 已由正常 BIOS 路徑實測職業技能起始為 80 點，並將全部點數配置完成後直接進入技術技能
  畫面；原先記載的 6 點是中途畫面誤讀，已訂正。
- 技術技能起始為 40 點；以正常 Enter／Down 配置歸零後，Escape 不再出現未用點數警告，
  而是進入身體圖示畫面。終態收據為 `workplace/phase51-skills-zero-v2.json` 與 64,000-byte
  framebuffer（皆為被 Git 忽略的本機證據）。
- 第一個完整配置後的圖示確認／保存／加入角色探測仍回到空名冊；scratch 只含未變更的
  32,070-byte `CHARS.DAX`，SHA-256 為
  `22140498a21cc5f2074dbe2a766c808c0e54a8404181e1264f939f046d59e8b5`，且 FileOps 沒有
  DOS write。此結果尚未判定是後段按鍵時點或原版條件，下一步須與第 48–50 階段事件逐項
  對齊；不得先宣稱 dosgolem 寫檔缺口。
