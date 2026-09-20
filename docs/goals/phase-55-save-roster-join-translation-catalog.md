# 第五十五階段：保存、名冊與加入隊伍繁中事件 catalog

狀態：已完成

## 目標

以第五十四階段已證實的完整保存→Add→加入正常玩家路徑，建立所有靜態玩家可見文字的
exact dispatcher identity、穩定文字 key 與繁體中文 catalog，並明確隔離動態角色名；為
後續倍率中立顯示請求提供可稽核輸入，不改動原版保存或加入語意。

## 範圍

- 從相同 `save-before.state` 與空白 scratch 重播完整路徑，在 dispatcher entry 擷取短字串、
  caller、長度、SHA-256、座標與色彩；原版文字只保留必要短句，不保存大段內容。
- 逐項分類為靜態可翻譯文字、動態角色名、選取 variant 或既有功能選單 identity；相同英文
  但 caller／幾何不同時不得合併 identity。
- 新增 UTF-8 TSV 繁中 catalog 與 content-safe 事件清冊，驗證 key 唯一、欄數、來源文字、
  漏譯、孤兒 key、NFC、控制碼及字型字元覆蓋輸入。
- 動態角色名維持原始 bytes，絕不進入翻譯 catalog；保存檔名、資格欄位與 FileOps 不得讀取
  譯文。
- 建立純資料 verifier 與正反例測試；本階段不把新 catalog 接進 dosgolem production watcher，
  若後續接線須另經 READY 規格。
- 完成後推送專案 `main` 並更新 GitHub Issues；本階段不修改 dosgolem 正式程式碼。

## 不在本階段

- 不繪製中文像素、不清除英文墨跡、不選定 2×／3×，也不宣稱此畫面已中文化完成。
- 不翻譯動態姓名 `A`，不解析角色檔內容，不修改保存、名冊資格或加入隊伍控制流。
- 不擴張到加入後其他遊戲畫面；只涵蓋第五十四階段固定正常路徑實際出現的靜態文字。

## 成功定義

1. 固定正常路徑的每筆文字事件均有 caller、原文長度／SHA-256、座標／色彩與角色分類。
2. 所有新靜態文字都有唯一 key 與正式繁中譯文；動態角色名明確排除且 verifier 會拒絕將它
   放進 catalog。
3. verifier 對 identity 漂移、重複 key、漏譯、孤兒 key、BOM、非 NFC、控制碼與不應翻譯的
   動態事件失敗即關閉；正反例測試通過。
4. catalog 字元已納入既有字元清單／字型建置輸入，且不要求決定 2×／3×。
5. 研究文件、CONTEXT、WORKLOG 與 Issues 已更新，專案 `main` 已推送，Docker 與兩個工作樹
   乾淨。

## 退出條件

- 若事件字串是動態組合或包含角色資料，保留原始顯示並標為 dynamic，不以單一 fixture 假裝
  靜態翻譯。
- 若相同文案在不同 caller／幾何出現，保留多筆 identity，共用翻譯 key 必須由資料明示。
- 若字型缺字，修正可重生字元清單與字型輸入，不為遷就缺字更改譯文。
