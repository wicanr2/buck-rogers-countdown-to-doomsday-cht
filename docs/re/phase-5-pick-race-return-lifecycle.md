# 第五階段：種族選擇畫面的離開與返回生命週期

日期：2026-09-20  
狀態：已完成一條正常 Escape 返回收據；正式 generation／invalidation hook 仍未知。

## 執行器與固定起點

依使用者指示，先把乾淨的 `/home/anr2/cht/dosgolem` 複製到被 Git 忽略的
`workplace/dosgolem/`，並在副本建立 `buck-rogers-cht-output-overlay` 分支。分支基準為
dosgolem commit `d9c0c27ca9af8239c7e96272a7165e03d7da04bf`；後續 probe 與 adapter 工作均以此副本
為工作樹，不直接修改原始 dosgolem 目錄。

由第四階段的 `after-bios-space-100m.state` 重播 BIOS Enter，在 #100,300,000 保存
`PICK RACE` 狀態：

- 狀態檔 SHA-256：
  `ffcc0444e585ceb7d2d355fd9ebef3d57604483343d02831d5007c6d39a84d2c`
- 起點 raw Mode 13h VRAM SHA-256：
  `d0f70a73b80b1998c0744ae2bb2903dba4783104fbfccc3ded41d70e8eacc1cd`
- `PICK RACE` 標題的已觀測像素為 `A000:1549`（畫面 `(9,17)`），起點色號 `0x0D`。

上述狀態、原版素材與所有 raw 收據只保存在 `workplace/`，不加入 Git。

## 正常 Escape 返回路徑

從固定狀態以 probe 的 BIOS BDA 鍵盤輸入，在 #100,310,000 排入 Escape（`0x1B`），未使用
`-poke`、傳送、forced-win、原版資料改寫或滑鼠候選座標。原版行為如下：

| 時間／定位 | 觀測 | 等級 | 覆繪含意 |
| --- | --- | --- | --- |
| #100,310,138 | 原版以 INT 16h AH=00 從 BIOS BDA 取走 `0x1B`。 | 已證實 | Escape 是這條路徑的正常輸入接受點。 |
| #100,310,464 | 返回流程第一筆 `0763:0424` string dispatcher，由 `37F1:1856` 呼叫。 | 已證實 | 返回開始產生文字時，舊 `PICK RACE` 畫面尚未清完。 |
| #100,316,673 | `A000:1549` 由 `0x0D` 變為 `0x00`，寫入端為 `0CF4:1B3C`。 | 已證實 | 舊標題像素比第一筆 dispatcher 晚 6,209 道指令清除。 |
| #100,417,141 至 #100,544,786 | 另有 7 筆 `0763:0424` 呼叫，重建功能選單文字。 | 已證實 | 返回亦是清除與文字輸出交錯的非原子轉場。 |
| #101,000,000 | 終點 raw VRAM 為 `b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3`。 | 已證實 | 終點 64,000 bytes 逐位元等於既有功能選單基線。 |

相同固定狀態、Escape 與終點步數獨立重播，`phase5-escape.vram` 與
`phase5-escape-replay-b.vram` byte-for-byte 相同。這條路徑沒有引入需固定的玩家可見 RNG。

## 工具行為勘誤

第一次要求在 `-steps 100300000` 同時保存 #100,300,000 狀態時，probe 沒有產生狀態檔：
主迴圈在執行每一步之前檢查 checkpoint，但終止條件在步數等於上限時先離開。改以
`-steps 100300001`、checkpoint 仍指定 #100,300,000 後成功保存。這是 probe 命令終點的
開區間行為，不是原版遊戲或快照內容失敗。

## 結論與下一閘門

向前進入與 Escape 返回都由 `0CF4:1B3C` 清除所監看的舊文字像素，且兩條路徑皆先發生
`0763:0424` 呼叫、後清除舊像素。因此「看到下一筆字串輸出」已被兩個方向的正常路徑反證為
不可靠的 overlay invalidation 訊號。

目前仍不能把 `0CF4:1B3C` 宣稱為通用畫面清除函式：只證實它是兩個樣本像素的實際寫入端，
尚未建立函式邊界、呼叫參數、清除矩形或所有畫面轉場的涵蓋性。下一階段應針對該寫入端與
其呼叫鏈建立最小充分證據，再審查 DRAFT 是否可定義正式 generation／invalidation hook。
