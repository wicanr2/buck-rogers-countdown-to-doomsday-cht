# 第八十二階段：host 設定面板控制列視覺 prototype

狀態：完成

## 目標

依使用者決定，以 dosgolem 視窗頂端的 host-only 滑鼠按鈕開啟倍率設定面板。先在原版
320×200 畫面之外建立可丟棄 prototype，驗證控制列、面板、點擊區與遊戲內容／DOS 滑鼠
座標徹底分離，再形成通用 host UI 的 DRAFT 規格。

## 已確認決策

- 以設定面板切換 2×／3×，不是遊戲內選單、直接快捷鍵或單鍵循環。
- 由視窗頂端滑鼠按鈕開啟面板，控制事件只在 host 消費，不得送進 DOS BIOS／IRQ。
- 原版遊戲畫布維持 320×200 logical pixels；host 控制列與面板不得覆蓋、縮放或改寫遊戲內容。

## 範圍

- 查證現有 dosgolem 是否已有可重用的視窗、RGBA presentation 或 host 滑鼠分流層。
- 以真實 2×／3× Buck Rogers framebuffer 製作控制列／設定面板的可丟棄原生解析度 prototype。
- 量測控制列高、遊戲畫布原點、按鈕與面板 hit rectangle；定義點擊進入／離開 host UI 時
  DOS 不得收到滑鼠移動、按鍵或座標。
- 寫出通用層與 `apps/buckrogers/` 資料／覆繪層的責任邊界。

## 不在本階段

- 不建立 production 視窗前端、不綁定最終按鈕文案、快捷鍵、預設倍率或設定持久化。
- 不修改原版 EXE、遊戲選單、VRAM、DOS 滑鼠／鍵盤、存檔或規則。
- 不把 mockup 視為正常玩家路徑或 same-state 收據。

## 完成條件

1. 2×／3× prototype 都保持原版畫布完整，並清楚顯示 host 控制列與面板的非遊戲範圍。
2. 每個 hit rectangle 都有 output-pixel 座標、縮放規則與不送入 DOS 的契約。
3. 不可重用的現有能力與需新增的通用層明確分級；不把 Buck Rogers 特例寫進 engine。
4. 依 prototype 結果向使用者提出下一個單一視覺／操作決策；專案 `main` 推送並更新 Issues。

## 退出條件

- 若任何控制列配置需裁掉、平移或蓋住原版畫布，排除該配置；不得以遊戲畫面退讓換取 host UI。
- 若 host 前端尚不存在，prototype 只能定義 presentation contract，不可假裝已有可測視窗事件。

## 完成收據

- 以真實 Phase 62 手冊 framebuffer 產生 2×／3×、各兩個 active selection 的四張 prototype。
- 面板展開後畫布完整下推：2× 為 y=80、3× 為 y=120；每張 copied canvas SHA-256 與來源一致。
- 面板鈕與兩個倍率 option 的 output hit rectangles 已列入研究證據；命中必須在 DOS 轉換前消費。
- 已區分通用 host UI 與 Buck Rogers presentation adapter；無現成視窗 frontend 的事實維持 unknown。
