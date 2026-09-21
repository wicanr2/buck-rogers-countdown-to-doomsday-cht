# 第七十三階段：技術技能配置安全矩形與雙倍率覆繪

狀態：完成

## 目標

以第七十二階段已 CONFORMED 的技術技能 exact requests，以及第七十一階段已驗證的共享標題
矩形為輸入，建立技術技能配置畫面的 text-safe rectangle catalog，並在 dosgolem 長存 overlay
完成明示 2×／3× 的繁中像素覆繪、選取列取代與動態數值隔離驗證。

## 範圍

- 為 17 個技術專屬 identities 建立單列安全矩形；兩個共享標題沿用 career rectangle，不重複定義。
- 合併時驗證 event、translation、rectangle 三者雙向完整，重複 identity 與孤兒矩形失敗即關閉。
- 驗證 base 初始第一列 normal→selected，以及 Down 後第一列 selected→normal、第二列 normal→selected。
- base／Down 各做 control、2×、3×，每種雙重重播；比對原版 framebuffer、事件、輸入、
  動態 points／bonus／total 與 active overlay keys。

## 不在本階段

- 不翻譯未經 dispatcher 證實的底部 ADD／SUBTRACT／DONE，也不新增未實測 selected variants。
- 不修改技能點規則、數值、加減、完成、離開、存檔或任何原版語意。
- 不選定產品預設倍率，不處理手冊題目版面。

## 完成條件

1. 技術專屬 17 筆矩形與 technical events 雙向一對一；合併 career 後，所有 19 個可翻譯位置
   都有唯一矩形，且譯文在 16×16 字型、2×／3× 下完整 containment。
2. 矩形外與動態 points／bonus／total 欄差異均為 0。
3. base／Down 的 active keys 正確反映 normal／selected 取代，同一畫面位置不殘留重複 stamp。
4. control 與 overlay 的原版語意 projection、raw framebuffer 完全相同；所有重播決定性一致。
5. 專案回歸、dosgolem 正式測試／vet／相關 race detector 通過；dosgolem 只提交本機 branch，
   專案 `main` 推送並更新相關 GitHub Issues。

## 退出條件

- 若譯文超出已證實安全範圍，規格退回 DRAFT，不截斷、不縮寫硬塞。
- 若共享標題矩形與技術畫面實際幾何不一致，停止合併並回到原版事件證據重新分級。
- 若 normal／selected 無法由通用清除 hook 正確取代，先補生命週期證據，不寫技能專屬清除特例。
- 若 2×／3× 無法共用同一邏輯矩形，停止 production 接線，不代替使用者選定倍率。

## 完成收據

- 17 筆 technical exact-width 矩形與事件雙向一對一；兩個共享標題沿用 career rectangles，
  合併後沒有重複或孤兒 identity。
- 第一輪沿用 request 收據停止點時 selected stamp 尚為 `Pending`，人工圖像揭露英文殘字；規格
  退回 DRAFT。延後到下一個穩定 frame 後證實不是 renderer 缺陷，並把穩定 frame 與人工檢查
  納入正式驗收。
- base／Down × 2×／3× 各雙重重播一致；矩形內差異為 16,611／34,423 px，矩形外與動態欄
  都是 0 px，原版 framebuffer 與語意 projection 不變。
- 四張正式 PNG 已目視確認 selected 繁中取代、色彩、列距與數值完整；未選定產品預設倍率。
- 專案 136 項 Python 測試、dosgolem 全正式套件 test、`go vet` 與相關 race detector 通過。
