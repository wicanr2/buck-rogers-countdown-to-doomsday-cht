# 第四階段：選單互動與覆繪失效生命週期

日期：2026-09-20  
狀態：已完成一條向前轉場收據；返回、捲動與存讀檔生命週期仍未知。

## 正常輸入路徑與重播

固定起點為 `workplace/probe/after-bios-space-100m.state`（#99,999,999）。從此狀態：

1. 在 #100,010,000 將一個 Enter（`0x0D`）排入 BIOS BDA 鍵盤緩衝。
2. 原版於 #100,010,174 以 INT 16h AH=00 取走該 Enter。
3. 原版進入可見的 `PICK RACE` 畫面；#100,000,000–#100,300,000 間，`0763:0424` 有 9 次
   string dispatcher 呼叫。
4. 終點 raw Mode 13h VRAM 的 SHA-256 為
   `d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd`。

相同固定狀態、輸入與終點步數獨立重跑，`phase4-enter-transition.vram` 與
`phase4-enter-transition-replay-b.vram` byte-for-byte 相同。整條路徑未使用 `-poke`、
傳送、forced-win 或原版資料改寫；BIOS BDA 是本作已證實會接受的正常鍵盤輸入通道。

## 互動與輸出生命週期

| 時間／定位 | 觀測 | 等級 | 覆繪含意 |
| --- | --- | --- | --- |
| #100,010,174 | 原版 INT 16h AH=00 取走 Enter。 | 已證實 | 是此選單路徑可重播的玩家輸入接受點。 |
| #100,010,490 | 轉場中的第一筆 `0763:0424` 呼叫。 | 已證實 | 第七階段已證實內容仍是舊功能選單的 `Create New Character` 重畫；它不是新畫面第一筆文字。 |
| #100,031,031 | 原選單已證實文字像素 `A000:838A` 由 `0x0A` 變為 `0x00`；watch 當時記錄 `ip=0CF4:1B3C`。 | 已證實 | 至少該舊選單 glyph 在新文字開始後 20,541 道指令才被原版清除。第六階段已訂正：實際寫入指令為 `0CF4:1B3A REP STOSB`，`1B3C` 是下一個 IP。 |
| #100,033,190 至 #100,221,773 | 後續 8 筆 `0763:0424` dispatcher 呼叫，構成 `PICK RACE` 畫面文字。 | 已證實 | 一個畫面轉場可交錯清除舊墨跡與輸出新文字，不能假定單一原子 repaint。 |
| 轉場前後 VRAM | 功能選單 SHA-256 `b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3`；`PICK RACE` 為上述終點雜湊。 | 已證實 | 畫面確實轉換，而非僅輸入被消耗。 |
| 滑鼠點擊 | 在 `(160,108)` 與 `(80,108)` 各送一次正常 INT 33h 左鍵；原版均讀到一次按下但畫面不變。 | 已證實／未知 | 輸入送達已證實，這兩點不是已證實熱區；不得憑此推定滑鼠選單語意。 |
| 返回、捲動、游標反白、存讀檔 | 未量測。 | 未知 | 尚不能宣稱完整覆繪失效生命週期。 |

收據檔均在被忽略的 `workplace/probe/`：`phase4-enter-transition.log`、
`phase4-transition-old-pixel.log`、兩份終點 VRAM／palette 與各自重播日誌。原版畫面不進
Git；本文件只保存定位、雜湊與觀測結果。

## 結論與 READY 邊界

這條收據推翻「下一筆文字 dispatcher 即可安全清除前畫面覆繪」的假設。DRAFT 覆繪至少
需要在原版接受會轉場的輸入時，或在經證實的畫面 generation／清除事件，立即使舊覆繪
失效；不能等待新文字事件才處理。何者可作為通用、正式的 invalidation hook 尚未證實。

因此目前仍是 DRAFT：下一個必要收據是從 `PICK RACE` 選擇或退出、回到前畫面的正常路徑，
量測重新繪製與 stale overlay 是否可能殘留；完成前不得實作 production 覆繪。

## 後續勘誤

[第六階段](phase-6-clear-path-hook-evidence.md)以 IDA 9.4、原始 bytes 與動態 trace 證實，
watchpoint 顯示的 `0CF4:1B3C` 是 `REP STOSB` 執行後的下一個 IP；真正寫入位於
`0CF4:1B3A`。舊像素清除時間不變，但不得把 `1B3C` 稱為寫入指令或上層清除事件。

[第七階段](phase-7-text-post-call-generation-event.md)再證實 #100,010,490 的內容是
`Create New Character`，完整 post-call 在 #100,025,943，之後才於 #100,028,739 進入矩形
清除；新畫面的下一筆已觀測 dispatcher 是 #100,033,190。故本階段先前所稱「第一筆新字串」
應訂正為「轉場中舊選單的最後一次重畫」。
