# 第四十五階段：職業技能點配置的選取、加減與離開生命週期

狀態：已完成

## 目標

從第四十四階段相同固定 state 與正常姓名確認路徑到達職業技能點配置畫面，辨識方向鍵、
加減鍵、Enter 與 Escape 的實際作用，量測選取列、點數變更及離開畫面的文字／像素生命週期，
建立 content-safe、可重播且失敗即關閉的正式收據。

## 範圍

- 先以同一固定 state 的獨立 probe 分支測試 Up／Down／Left／Right、`+`／`-`、Enter、Escape。
- 以事件次序、數值 identity、indexed framebuffer 差異及下一畫面判斷按鍵語意，不猜規則。
- 正式驗證至少涵蓋選取移動、一次合法點數變更及一條可判定的離開／拒絕路徑。
- 固定完整 BIOS 排程、事件 step／identity、終點 framebuffer、原版與命令雜湊；不保存原版
  英文全文，也不把動態數值列為譯文。
- 建立嚴格 verifier、正反例測試、dosgolem 診斷規格與研究文件。
- 完成測試與衛生檢查後，提交 dosgolem 本機分支、推送專案 `main` 並更新 Issues。

## 不在本階段

- 不修改技能點總額、上限、bonus、職業規則或角色資料。
- 不以記憶體注入、直接設定點數或測試專用跳關取代正常輸入。
- 若確認後進入新子系統，只量到第一個穩定玩家可見邊界。
- 不翻譯技能配置畫面，不建立 catalog／renderer，不選定 2×／3×。

## 成功定義

1. 正常 BIOS 輸入證實選取移動、加減或拒絕，以及 Enter／Escape 中可判定的離開行為。
2. 正式分支各從同一 state 獨立重播兩次，JSON 與 64,000-byte framebuffer 逐 byte 相同。
3. 清冊區分靜態標籤、動態點數、選取重畫、拒絕提示與轉場事件，保留 exact identity／step。
4. verifier 對輸入排程、事件數、次序、step、identity、畫面及輸入雜湊漂移失敗即關閉。
5. dosgolem 規格達 CONFORMED；正式套件測試、`go vet`、相關 race detector 與專案測試通過。
6. 專案 `main` 已推送、Issues 已更新，兩個工作樹與 Docker 生命週期乾淨。

## 退出條件

- 若候選鍵都沒有可判定效果，保存負面證據並窄幅追查輸入 consumer，不注入狀態。
- 若改點需要先滿足未明條件，先記錄拒絕分支與畫面證據，不猜測點數規則。
- 若確認離開要求配置完全部點數，本階段不批次猜配；只建立最小正常配置路徑或另開切片。

## 完成結果

- Down、Enter 加點及 Escape→`N` 拒絕離開三條正式分支，各自雙重重播逐 byte 相同。
- 三份 content-safe 清冊、嚴格 verifier 與正反例測試已建立；專案 82 項測試通過。
- dosgolem spec 026 已達 CONFORMED；全部正式 packages test／vet 與相關 race detector 通過。
- 本階段沒有翻譯配置畫面、接入 renderer、修改規則或替使用者選定 2×／3×。
