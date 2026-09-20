# 目前狀態

更新：2026-09-20

## 已確認的產品方向

使用者於 2026-09-20 確認維持原訂的 **dosgolem 執行期輸出端繁體中文化**。已排除
clean-room remake／重寫引擎分支；後續只可在不改動原版 EXE、資料、規則、手冊驗證或
存檔語意的前提下，建立原版輸出事件、中文覆繪與同狀態收據。

- 第一階段「可觀測的原版啟動與文字輸出基線」已以 dosgolem 完成：真實 `START.EXE`／
  `GAME.OVR` 可由固定狀態經 BIOS 空白鍵走到玩家可見功能選單，兩次 raw VRAM 雜湊相同。
- 權威收據與未解項目見 [原版觀測證據索引](docs/re/README.md)；原始輸入與收據只在被
  Git 忽略的 `workplace/`。
- 已完成第二階段：`0763:0424` 已證實讀取 `[length:u8][ASCII bytes]`，再經 `0763:026B`、
  `0763:1809` 到 `0763:183A..1863` 畫出 8×8 英文 glyph；選單樣本含原文字串 pointer、
  色彩與文字格座標。完整證據見 `docs/re/phase-2-text-dispatch-and-lifecycle.md`。
- 清除／捲動、游標反白、畫面轉換、返回與存讀檔後的覆繪失效時機仍未知，因此
  `docs/spec/001-menu-text-output-overdraw-draft.md` 仍是 DRAFT，未授權 production hook。
- 功能選單的 BIOS Enter 轉場現已量到：新字串輸出可早於舊選單像素清除，因此覆繪不能以
  「下一筆字串已輸出」當成畫面失效判定。詳見 `docs/re/phase-4-menu-interaction-lifecycle.md`。
- 中文手冊 RAR 已在 Docker 以 `lsar`／`unar` 盤點、完整性測試與解壓；80 個 archive
  項目通過、79 個實體檔案已有 SHA-256 清冊，並有 77 張 JPG 的 archive-order 定位。
  詳見 `docs/re/phase-3-manual-input-inventory.md`。手冊語意、頁碼與原版題目對應仍未知。
- 尚未開始中文覆繪、翻譯 catalog、字型決策或任何原版檔／規則／存檔修改。

下一個受證據閘門約束的工作，是從 `PICK RACE` 量測選擇／退出後的返回與重繪，建立可用
的畫面 generation／invalidation hook 證據，再審查功能選單 DRAFT 是否可升為 READY。
