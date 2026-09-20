# 第一階段目標：可觀測的原版啟動與文字輸出基線

狀態：進行前（尚未開始量測）  
日期：2026-09-20  
工作追蹤：[GitHub Issue #1](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/1)、[#2](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/2)、[#3](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/3)、[#4](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/4)

## 目標

讓使用者自備的 DOS 英文版《Buck Rogers: Countdown to Doomsday》可在 dosgolem
中沿正常啟動路徑到達至少一個玩家可見的文字畫面，並留下可重播、可追溯的原版
文字輸出觀測基線。這個階段產出的是觀測能力與證據，不是中文覆繪功能。

## 成功定義

第一階段完成時，必須同時具備：

1. 原始 ZIP、中文手冊 RAR 與所用解壓輸入的檔案清冊、SHA-256、權利分類及 Docker
   工具紀錄；原始素材仍只留在本機並被 Git 忽略。
2. dosgolem 以真實 `START.EXE`／`GAME.OVR` 啟動時的能力收據：已支援與未支援的
   CPU、DOS／BIOS、VGA 與檔案服務均有清單，並以原版雜湊與 dosgolem 版本鎖定。
3. 一條不靠傳送座標、強制獲勝或改寫記憶體的最小正常玩家路徑重播，可從固定初始
   狀態走到一個文字輸出檢查點。
4. 至少一條文字輸出呼叫鏈的 trace，含原始 callsite、dosgolem 位址空間、字串來源、
   座標、字型、顏色與清除／捲動時機；每項語意均標示已證實、強推論、假說或未知。
5. 上述資料足以撰寫下一階段的 DRAFT 覆繪規格；任何將進入正式程式路徑的行為都必須
   經證據審查升為 READY。

## 不屬於本階段

- 不繪製中文、不建立完整翻譯 catalog，也不決定中文字型。
- 不將中文手冊段落接入遊戲畫面；只確認手冊題目／提示是否可被觀測，並保留其原版
  輸出證據。
- 不以 DOSBox 或 DOSBox-X 的成功啟動宣稱 dosgolem 支援；它們僅可作診斷與交叉基準。
- 不修改原版 EXE、資料、規則、手冊驗證判定或存檔格式。
- 不宣稱遊戲已可玩、已中文化或完成任何未被正常路徑收據覆蓋的功能。

## 退出條件

當成功定義的五項均以 dosgolem 可重生收據佐證後，本階段結束。若真實啟動路徑首先
遇到尚未支援的機器層能力，應記錄最小缺口、建立 DRAFT 規格並暫停依賴它的後續工作；
不得以猜測或改寫遊戲行為跨越缺口。
