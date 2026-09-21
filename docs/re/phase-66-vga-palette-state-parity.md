# 第六十六階段：VGA mode 13h 預設色盤與角色動態值可讀性

日期：2026-09-21  
狀態：完成

## 結論

角色資料頁動態值使用 raw framebuffer 色號 15，但既有 dosgolem state 將 DAC 15 保存為黑色。
這不是舊 state 單獨污染，也不是遊戲主動設黑：現行 dosgolem 由乾淨 `START.EXE` 冷啟動仍可
重現，而探針證實遊戲第一筆 DAC block write 只寫 0–14，明確依賴切入 mode 13h 時的 BIOS
預設色 15。dosgolem 原本只記錄模式、不載預設 DAC，故缺少白色。

## 可追溯證據

- 原始輸入：`START.EXE` SHA-256 `58a34a38…cf1`；dosgolem 修正前 commit `68d0e2f`。
- 冷啟動 #7,520,426 切入 mode 13h；#7,559,527 的 `INT 10h AH=10h AL=12h` 為
  `BX=0000 CX=000F`，只寫 15 格；#7,673,481 才由 `BX=0010 CX=0010` 寫 16–31。
- 遊戲沒有 `3C8/3C9` 直接埠寫入；DAC 0–14 與 16–31 均由上述 BIOS 服務產生。
- DOSBox-X `int10_modes.cpp` 將 mode 13h 列為 `M_VGA`，其 `vga_palette` 前 16 格的 index 15
  為 `(0x3f,0x3f,0x3f)`。這是成熟模擬器交叉證據，不冒稱真實 VGA BIOS ROM 逐位對拍。

推論等級：遊戲局部寫入範圍與 dosgolem 缺口為已證實；採用標準 VGA 前 16 色為成熟模擬器
規格近似。DAC 16–255 的完整 BIOS 預設表不在本輪範圍，保持未知且不猜補。

## 修正與同狀態驗收

dosgolem spec 205 先達 READY，再於 `INT 10h AH=00h` 的 mode 13h 分支載入標準前 16 色；
index 6 固定棕色，index 15 固定白色，index 16 以 sentinel 負例證明不受影響。

- 修正後冷啟動重建 70M state，再由正常 BIOS 空白鍵重建 #99,999,999 state。
- 100M raw framebuffer 修正前後皆為 `b08623d2…a3`；新 palette 為 `39f7fda3…f37d`，
  DAC 15 展開後為 `(255,255,255)`。
- 角色頁 base／`Y` 的 raw framebuffer 仍為 `1f3b8194…d4dd`／`03d9bf1f…0f97`。
- base 為 118 events、43 requests／actions、75 misses；`Y` 為 149／52／52／97；兩者終態
  均為 35 active keys，與階段 65 完全相同。
- 2×／3× 各獨立重播兩次；每組 JSON、RGBA、baseline RGBA、raw framebuffer 全部逐 byte
  相同。HP 動態值區在 2× baseline 有 72 個純白像素，證明原版數值已實際可見。

新 RGBA／baseline SHA-256：base 2× `5615b820…b2b6`／`f3e1b290…c427`，base 3×
`90a8f482…6c08`／`b9532a8b…616f`；`Y` 2× `ca3c62c1…159`／`e056189c…acac`，`Y` 3×
`6d9c3cb9…6e7a`／`ab133713…d94f`。原版素材、state、字型與完整輸出只留在被忽略的
`workplace/phase66/`。

## 邊界

本輪沒有改 raw framebuffer、輸入、翻譯、矩形、規則或存檔，也沒有替使用者選定 2×／3×；
手冊版面決策仍維持待確認。
