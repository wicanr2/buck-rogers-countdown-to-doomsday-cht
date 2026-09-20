# DRAFT：功能選單文字輸出端覆繪

狀態：DRAFT — 禁止據此實作 production hook  
日期：2026-09-20  
證據：[第二階段文字分派與生命週期追蹤](../re/phase-2-text-dispatch-and-lifecycle.md)

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

## 未知與 READY 閘門

下列項目未達 READY，故禁止 production 實作：

- 如何在 dosgolem 正式觀測／adapter 層可靠地於 `0763:0424` 的原版繪製後附加事件；
- 清除、捲動、游標反白、畫面轉換、返回與存讀檔後的失效時機；
- 中文字型來源、授權、字元清單、基線、行高、寬度、換行與 overflow 策略；
- 選單每一行的完整 text-safe rectangle，以及非靜態畫面的適用性；
- 上游字串表定位與對同內容、不同語意事件的 collision 策略。

升為 READY 前，至少須以 dosgolem 取得一條正常互動路徑，明確量到上述生命週期事件，並
完成原文／繁中 A/B 同狀態收據與中文 glyph containment 驗證。沒有達成這些條件時，DRAFT
只能引導後續量測，不能成為程式碼、測試期望或「已中文化」的依據。
