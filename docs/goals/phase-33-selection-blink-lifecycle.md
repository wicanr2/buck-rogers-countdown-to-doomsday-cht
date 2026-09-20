# 第三十三階段：種族選取列閃爍與色盤生命週期

## 狀態

完成

## 本輪目標

釐清第 32 階段固定終點中 selected Terran／Martian 為黑底黑字的原因：由 dosgolem 正常
Enter／Down 路徑連續取樣 indexed framebuffer、palette 與既有文字事件，判定選取提示是
重畫、palette 變化、像素閃爍或其他機制，建立 runtime 覆繪必須遵守的最小充分生命週期證據。

## 範圍

- 沿用第 30／31 階段相同初始 state 與 BIOS Enter／Down 排程，不注入額外遊戲狀態。
- 在 selected Terran 建立後及 Down 改選 Martian 後，以有界固定步數取樣 row 3／4 的原版
  indexed 色號分布、相關 palette RGB、區域 hash 與畫面可見性。
- 同步記錄 `0763:0424` guarded post-call；區分「原版重畫事件」與「同一 indexed pixels 因
  palette 改變而顯示不同」兩種可能。
- 兩次完整重播必須逐 byte 相同；收據不保存原文全文。
- 將證據回填選單覆繪 DRAFT，明列 production renderer 的待驗條件與停止線。
- 若需要新診斷能力，先建立 dosgolem READY 規格，再移入正式命令；純研究 probe 可留在
  被忽略的 `workplace/`。
- 完成後推送專案 `main`，更新 Issues #5、#7；dosgolem 只建立本機 commit，不推遠端。

## 不在本輪範圍

- 不選擇 2×／3×，不接 runtime renderer，不改原版反白／閃爍節奏。
- 不為了讓 selected row 更醒目而自訂顏色、取消閃爍或改成現代游標。
- 不追逐逐週期 VGA 硬體精確度；只量玩家可見相位、遊戲寫入與 palette／像素結果。
- 不處理滑鼠選取、確認種族、其他畫面或手冊分頁。

## 驗收條件

- Goal 已在 probe 前建立並完整讀回。
- 至少覆蓋 selected Terran 穩定期、Down 的 normal Terran／selected Martian 重畫後穩定期。
- 取樣足以證實或排除 palette-only、pixel redraw 與週期性可見性；不以單張終點圖下結論。
- 收據記錄 state／工具／事件資料雜湊、絕對 step、palette、區域 hash／色號計數與推論等級。
- 兩次重播與收據 verifier 通過；正式專案與 dosgolem 測試無回歸。
- Docker、擁有權與兩工作樹狀態已核對；`main` 已推送且 Issues #5、#7 已更新。

## 預定交付物

- `docs/re/phase-33-selection-blink-lifecycle.md`
- content-safe 的連續幀取樣資料與 verifier
- 選單覆繪 DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

2026-09-21 完成。steady／Down 各由相同 state 重播兩次，#100,220,000–#109,990,000
各 978 點收據 pair 逐 byte 相同。完整 palette 全程唯一，色號 0／15 同為黑色且
`selected_contrast=false` 978／978；重畫完成後 row 3／4 hash 與事件數均不再變動，已排除
窗口內 palette-only blink 與週期性 pixel redraw。dosgolem spec 014 已 CONFORMED，本機
commit `41917c85007efe17154cb92422cba3fe6539ad88`，未推其遠端。44 項專案測試與 dosgolem
正式套件驗證通過；未選倍率、未接 runtime renderer。
