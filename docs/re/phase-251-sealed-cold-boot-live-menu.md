# 第二百五十一階段：sealed 冷開機的即時選單覆繪

日期：2026-09-26  
狀態：**已證實／單次重播。**

## 輸入

- dosgolem fork `0ab7900`：規格 238 的 sealed Owner 逐步觀測器、`Owner.Digest`、
  `bootroot` 保留 mtime，以及 `cmd/buckrogers-session` 的 `-text-dir`／`-script`／
  `-rgba-out`。
- 原版 `START.EXE` 經 `bootroot.Prepare` 複製成存檔樹後冷開機，零 checkpoint。
  25 回合 × 10M 步，第 13、16 回合開頭各送一次空白鍵（120M、150M），停在 250M。

## 結果

- 三組：無觀測器、掛選單即時覆繪並輸出 2×、掛選單即時覆繪並輸出 3×。
  三組的記憶體、CPU、indexed、palette 雜湊全部相同（記憶體 `96002fc5…`、
  indexed `d0f70a73…`）。觀測器不改變原版狀態。
- 250M 是種族選擇屏。合成畫面的標題、六個種族選項與底列提示都是繁中，
  2× 與 3× 皆目視確認；畫面圖檔含原版美術，只留 ignored workplace。

## 過程中修正的非決定性

第一次三組的記憶體雜湊互不相同，CPU／畫面相同。原因是 `bootroot` 複製存檔樹時
沒有保留來源 mtime，而 sealed session 的 DOS `Root` 就是這棵樹，檔案時間經 DTA
進入遊戲記憶體。修正寫入 dosgolem 規格 237 §2.5 後，三組一致。

## 發現的後續缺口

sealed session 只設 DOS `Root`、沒有設 `Scratch`。依 dosgolem 規格 009，這時寫檔
只記帳、不落地，玩家在 sealed session 裡存檔不會真的寫入。可玩前端前必須處理。

私有收據留在 ignored `workplace/phase251-sealed-live-menu/`。
