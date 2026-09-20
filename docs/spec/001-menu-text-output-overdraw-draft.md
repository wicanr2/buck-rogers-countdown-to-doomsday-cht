# DRAFT：功能選單文字輸出端覆繪

狀態：DRAFT — 禁止據此實作 production hook  
日期：2026-09-20  
證據：[第二階段文字分派與生命週期追蹤](../re/phase-2-text-dispatch-and-lifecycle.md)、
[第四階段向前轉場](../re/phase-4-menu-interaction-lifecycle.md)、
[第五階段 Escape 返回](../re/phase-5-pick-race-return-lifecycle.md)、
[第六階段清除路徑與 hook 邊界](../re/phase-6-clear-path-hook-evidence.md)

## 玩家可見範圍

此規格只描述原版由標題進入功能選單時、以 `0763:0424` 分派的長度前綴 ASCII 字串。
目標方向仍是「保留原版語意，只在原始輸出後覆繪繁中」，不改 EXE、遊戲規則、手冊驗證、
檔名或存檔。它不涵蓋劇情、戰鬥、角色／物品名稱、手冊提示或任何中文內容。

## 已證實輸入與事件形狀

原版輸入、雜湊、dosgolem commit 與地址空間均見研究證據。對此選單樣本，`0763:0424`
接收下列原始資料：

```text
source: far pointer ES:DI → [length:u8][original_bytes:length]
style/page: u8（完整語意未證實）
background_palette_index: u8
foreground_palette_index: u8
row: u8, 0..24
column: u8, 0..39
```

原版會把字串複製到 stack buffer，再逐 byte 呼叫 `0763:026B`，最後由 `0763:1809` 與
`0763:183A..1863` 畫出 8×8 glyph。可測得的原文畫面矩形為：

```text
x = column × 8
y = row × 8
width = length × 8
height = 8
```

`source` 的內容僅能作顯示比對鍵；繁中不得進入原版比較、資源查找、序列化、檔案路徑或
存檔名稱。DRAFT 尚未決定正式 key 的序列化格式，也不在 repo 保存原版文字 catalog。

## DRAFT 覆繪生命週期

若未來證據審查通過，候選事件必須按以下順序運作：

1. 原版完整執行 `0763:0424` 的字串繪製；不得提前跳過或替換。
2. 僅在已核准的原文顯示鍵、同一個 row／column 與計算後 text-safe rectangle 上，清除
   原文墨跡並畫出繁中 glyph。
3. 原版的下一次重繪、游標、翻頁、捲動、切換畫面、離開或載入狀態必須使覆繪失效或重建；
   不得留殘字。
4. 同一初始狀態、相同輸入與固定 seed（若該路徑引入 RNG）下，原文與繁中執行的原版狀態
   必須一致；允許差異只可出現在經核准的覆繪像素。

### 已量到的轉場失效證據

由功能選單固定狀態送入 BIOS Enter 時，原版在 #100,010,174 接受輸入，於 #100,010,490
先發生一筆新的 `0763:0424` dispatcher，卻到 #100,031,031 才由 watchpoint 當時標為
`0CF4:1B3C` 的路徑將已證實的
舊選單像素 `A000:838A` 從 `0x0A` 清為 `0x00`。完整收據見
[第四階段選單互動與失效生命週期](../re/phase-4-menu-interaction-lifecycle.md)。

所以 DRAFT 的保守規則是：在原版接受可造成轉場的輸入時，現有 overlay 必須立即標示為
失效；不得把「首次看到下一筆字串事件」當成原畫面已清除的證據。這只是失效策略候選，
尚未證實哪一個通用 dosgolem hook 可正確辨識所有轉場。

反向返回亦有相同順序：Escape 在 #100,310,138 被原版取走，#100,310,464 已發生第一筆
dispatcher，但 `PICK RACE` 標題像素到 #100,316,673 才由相同路徑清除；終點
逐位元回到既有功能選單基線。這使保守失效規則同時有進入與返回兩個正常玩家路徑支持，
但仍不能僅憑兩個像素樣本把該寫入端宣稱為通用清畫面 hook。

### 已證實的矩形失效候選

第六階段訂正 watchpoint 地址：實際寫入指令是 `0CF4:1B3A REP STOSB`，`1B3C` 是下一個 IP；
`0CF4:1B2B` 函式只是任意 far pointer 的 byte-fill，已排除為正式 hook。兩條路徑真正共用的
上層事件是 `026F:029C`：在 `DS:3C78 == 3` 的 Mode 13h 分支，它把四個邏輯文字格參數
換算成像素矩形，再逐列填 0。

DRAFT 候選契約因此縮小為：固定輸入雜湊與 runtime bytes 簽章均相符時，在
`026F:029C` 進入點讀取 `bottom/right/top/left` 四個低 byte；若範圍合法且模式為 3，將
`[left×8, top×8, (right+1)×8, (bottom+1)×8)` 內相交的既有 overlay 標為失效，然後讓原版
函式完整執行。Enter 樣本矩形為 `x=8..311, y=16..183`；Escape 返回為
`x=0..311, y=0..183`。此契約仍是 DRAFT，尚未與 post-dispatch 重建事件接通。

## 未知與 READY 閘門

下列項目未達 READY，故禁止 production 實作：

- 如何在 dosgolem 正式觀測／adapter 層可靠地於 `0763:0424` 的原版繪製後附加事件；
- 清除、捲動、游標反白、畫面轉換、返回與存讀檔後的失效時機；
- 在 `0763:0424` 完成原版繪製後可靠送出 post-call 事件，並把矩形失效與後續字串重建歸入
  正確 generation 的方法；
- 中文字型來源、授權、字元清單、基線、行高、寬度、換行與 overflow 策略；
- 選單每一行的完整 text-safe rectangle，以及非靜態畫面的適用性；
- 上游字串表定位與對同內容、不同語意事件的 collision 策略。

升為 READY 前，至少須以 dosgolem 取得一條正常互動路徑，明確量到上述生命週期事件，並
完成原文／繁中 A/B 同狀態收據與中文 glyph containment 驗證。沒有達成這些條件時，DRAFT
只能引導後續量測，不能成為程式碼、測試期望或「已中文化」的依據。
