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
- `PICK RACE` 的 BIOS Escape 返回亦已量到：原版取走 `0x1B` 後，第一筆新文字 dispatch
  仍早於舊標題像素清除；終點逐位元等於既有功能選單基線，獨立重播結果相同。詳見
  `docs/re/phase-5-pick-race-return-lifecycle.md`。
- dosgolem 已依使用者指示複製至被忽略的 `workplace/dosgolem/`，工作分支為
  `buck-rogers-cht-output-overlay`，基準 commit 為 `d9c0c27ca9af8239c7e96272a7165e03d7da04bf`；
  後續 probe 與 adapter 變更只在該副本進行。
- 第六階段已訂正清除定位：watchpoint 的 `0CF4:1B3C` 是 `REP STOSB` 後的下一個 IP；實際
  寫入在 `0CF4:1B3A`，其函式 `0CF4:1B2B` 是通用 byte-fill，已排除為 invalidation hook。
  兩條轉場共用的上層候選是 `026F:029C` Mode 13h 矩形清除例程；Enter 清除
  `x=8..311,y=16..183`，Escape 返回清除 `x=0..311,y=0..183`。完整證據見
  `docs/re/phase-6-clear-path-hook-evidence.md`。
- 第七階段已證實 `0763:0424` post-call：`Create New Character` 最後 glyph 於
  #100,025,833 寫完，#100,025,943 才返回 `37F1:1856`。現有 `OnCall` 足以在 adapter
  觀測 return，但必須由 entry 建立 pending frame，並以 return address、`SS` 及
  `SP == entry SP + 0x10` 排除自然 fall-through；`37F1:15BD` 已有實際反例。Enter 的事件
  順序是舊選單 post-call → 矩形失效 → 新畫面 dispatcher／post-call。完整證據見
  `docs/re/phase-7-text-post-call-generation-event.md`。
- 中文手冊 RAR 已在 Docker 以 `lsar`／`unar` 盤點、完整性測試與解壓；80 個 archive
  項目通過、79 個實體檔案已有 SHA-256 清冊，並有 77 張 JPG 的 archive-order 定位。
  詳見 `docs/re/phase-3-manual-input-inventory.md`。手冊語意、頁碼與原版題目對應仍未知。
- 尚未開始中文覆繪、翻譯 catalog、字型決策或任何原版檔／規則／存檔修改。

下一個受證據閘門約束的工作，是建立可丟棄的功能選單繁中覆繪 prototype：先建立首批譯文、
可追溯字型候選與 text-safe rectangle，再把 guarded post-call 與矩形失效接起來，產生
英文／繁中 A/B 像素收據。prototype、自然 fall-through regression、字型授權與 containment
完成前，功能選單 DRAFT 不升為 READY。
