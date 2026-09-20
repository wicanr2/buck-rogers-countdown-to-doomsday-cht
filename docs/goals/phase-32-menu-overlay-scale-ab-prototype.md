# 第三十二階段：功能選單覆繪倍率 A/B prototype

## 狀態

完成

## 本輪目標

以第 31 階段已證實的 13-request 正常路徑為基礎，對同一個原版功能／種族選單 framebuffer
分別套用 2× 與 3× 繁中點陣字覆繪，建立可並列檢視、可重生且有幾何量測的決策收據，讓
使用者能依實際畫面選擇正式倍率。

## 範圍

- 讀取 Golden Box／PC-98 CJK 介面的功能選單或角色建立相關版面證據，只採用結構模式，
  不複製受保護圖像、文字或配色。
- 沿用正式 `menu-events.tsv`、`menu.zh-TW.tsv`、`menu-text-safe-rects.tsv` 與 GOLEMFNT
  建置輸入；原版遊戲、手冊與字型二進位仍只留在被忽略的 `workplace/`。
- 從同一固定 dosgolem 狀態取得原版 indexed framebuffer，分別產生 2×、3× prototype；
  兩案必須使用相同事件、翻譯、色彩角色、清除矩形與輸入終點。
- 量測每筆譯文 ink bounding box、text-safe rectangle containment、重疊、裁切與原矩形外
  差異；輸出 metadata 收據不得含原文全文。
- 建立原版／2×／3× 並列圖，供使用者做單一倍率決策；prototype 不進 production path。
- 推送專案 `main` 並更新 Issues #5、#7；dosgolem 若只增加診斷工具則建立本機 commit，
  不推其遠端。

## 不在本輪範圍

- 不替使用者選擇 2× 或 3×，不把建議當成授權。
- 不將 renderer 接到正式 runtime watcher，不升格選單覆繪 DRAFT，不宣稱玩家可見中文化完成。
- 不變更原版 EXE、資料、規則、輸入、存檔、手冊驗證或畫面狀態。
- 不處理手冊長段落分頁、其他選單、滑鼠路徑或發布封包。

## 驗收條件

- Goal 已在實作前建立並完整讀回。
- 2×／3× 皆由相同原版 framebuffer、正式繁中 catalog 與相同事件集合產生，重跑決定性一致。
- 每個覆繪欄位都有明確 text-safe rectangle；矩形外像素零變更，無裁切、無相鄰列重疊。
- 並列圖可在原生 320×200 邏輯尺寸與整數放大尺寸檢視，沒有平滑濾鏡。
- 收據記錄輸入／工具版本、倍率、字型、事件鍵、幾何與輸出雜湊；受保護素材不進 Git。
- 專案測試與資料 verifier 通過；Docker 容器、檔案擁有權及兩個工作樹狀態已核對。
- 本輪完成後推送 `main`，Issues #5、#7 留有可回查的 commit、收據與待決問題。

## 預定交付物

- `docs/re/phase-32-menu-overlay-scale-ab-prototype.md`
- 可重生的 A/B prototype 工具或明確命令
- 被忽略的原版／2×／3× PNG 與 content-safe JSON 收據
- `CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

2026-09-21 完成。steady／Down 的 2×／3× 均以正式資料和 dosgolem `xlate.Draw` 生成；
兩批輸出逐 byte 相同，四份收據皆為零缺字、零矩形重疊、零安全矩形外差異，ink 全數
contained。dosgolem 診斷規格 013 已 CONFORMED，本機 commit 為
`09f580877b0d1e34ef00fa44eddefa12898b7e53`，未推其遠端。原生圖已目視檢查；本階段未選
倍率、未接 runtime renderer，第 25 階段共同決策仍等待使用者確認。
