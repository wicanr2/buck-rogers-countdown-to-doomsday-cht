# 第七十一階段：職業技能配置安全矩形與雙倍率覆繪

狀態：完成

## 目標

以第七十階段已 CONFORMED 的職業技能 exact requests 為唯一文字來源，從 base 與 Down 正常
路徑量出標題、技能列及動態數值邊界，建立 text-safe rectangle catalog，並在 dosgolem 長存
overlay 完成明示 2×／3× 的繁中像素覆繪與選取列失效驗證。

## 範圍

- 每個 event key 使用原版文字起點及長度建立單列安全矩形；任何延伸都必須由同列動態值左界
  或可見面板邊界證實，不得遮住 points／bonus／total。
- 驗證 base 初始注意力 normal→selected，以及 Down 的注意力 selected→normal、無重力
  normal→selected；終態每個畫面位置只能保留一個 active stamp。
- 建立正式 rectangle TSV、資料驗證器及正反例；catalog／rectangle 必須雙向一對一。
- base／Down 各做 control、2×、3×，每種雙重重播；驗證 raw framebuffer、events、BIOS keys、
  動態數值與輸入語意不受 overlay 影響。

## 不在本階段

- 不翻譯底部非 dispatcher 的 ADD／SUBTRACT／DONE，不新增尚未實測的其他 selected variants。
- 不修改技能點規則、數值、加減、完成或離開行為。
- 不選定產品預設倍率，不處理手冊版面。

## 完成條件

1. 14 筆矩形逐一回查 exact event；譯文在 16×16 字型、2×／3× 下完整 containment。
2. 動態 points／bonus／total 欄與矩形外差異均為 0。
3. base／Down 的 active keys 反映 normal／selected 取代，沒有同位置殘留或重複 stamp。
4. control 與 overlay 的原版語意 projection 及 raw framebuffer 相同；所有重播決定性一致。
5. 專案回歸、dosgolem 正式測試／vet／相關 race detector 通過；dosgolem 只提交本機 branch，
   專案 `main` 推送並更新相關 Issues。

## 退出條件

- 若正式譯文超出原文範圍且無已證實空間可延伸，規格退回 DRAFT；不截斷、不縮寫硬塞。
- 若選取列未經通用清除 hook 失效，先保存原版清除 callsite／矩形證據，不以 event key 特例清除。
- 若 2×／3× 無法用同一邏輯矩形保持語意，停止 production 接線並保留實圖差異。

## 完成收據

- 14 筆 exact-width 矩形與 events 雙向一對一；最長技能列右界 x=136，動態數值從 x=184 開始。
- base／Down × 2×／3× 各雙重重播決定性一致；原版 framebuffer 與語意 projection 等於
  Phase 70 control。
- 矩形內差異像素分別為 11,280（2×）與 22,791（3×）；矩形外及動態數值欄均為 0。
- 原始解析度圖已目視確認 normal／selected 取代、色彩、數值與無殘字；未選定產品預設倍率。
- 專案 127 項 Python 測試通過；dosgolem 正式套件 test／vet 與本輪改動套件 race 通過。
