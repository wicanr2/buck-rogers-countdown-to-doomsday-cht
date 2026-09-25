# 第二百二十六階段：TANDY 等待的按鍵入口判別

狀態：**已證實／僅無頭收據與診斷重播。** 不含畫面比對，
不推論按鍵的遊戲語意（推進／忽略）。

## 觀測

- 無鍵 120M（`cmd/run` 診斷）：停 `0763:0CAA`，TANDY／NUMLOCK 橫幅，
  落點收束於 `0CF4` 迴圈，int16h 被問 633,660 次，鍵盤中斷 0 次。
- 同條件預置一空白鍵（`cmd/run -keys " "`＝`TypeKeys`＋`TypeScan`）：
  120M 停 `0763:0C96` 同區，int16h 633,662 次，**機器佇列仍剩
  2 個掃描碼**；300M 亦然（`0763:0CAF`，int16h 1,832,308 次，
  掃描碼仍剩 2，中斷仍 0）。`d.Keys` 的鍵 300M 步無人取走。
- 同序列經 sealed 路徑（launcher `-keys " "`＝`DeliverBIOSKey`→
  `PushKey`→BDA 環優先）：15×10M 每回合 pending 皆 1→0，
  覆蓋 0–150M 含 TANDY 區；另有單回合 300M 1→0。

## 結論

TANDY 等待不經 `d.Keys` 取鍵（否則 TypeKeys 早該被看見）；
它讀 BDA 環（`0040:001A/001C` 直讀，如 `PushKey` 註解所述之常見
寫法）或硬體埠，而 BDA 環正是 sealed `Deliver` 投遞的第一站。
`keyTick` 的 stub 守衛（向量 09 未裝處理常式即 stall）解釋機器
佇列殘留：等鍵迴圈不依賴 IRQ1，診斷 runner 的 `TypeScan` 鍵永遠
送不出去。**真實遊玩輸入必須走 sealed Deliver／BDA 環，
診斷 `-keys`（TypeKeys）不能用於過 TANDY。**

## 限制與下一步

- 消耗≠推進：只證佇列深度變化，未證 TANDY 已過；需畫面比對
  （前端切片）。
- IRQ1 全程 0 次：硬體鍵盤中斷路徑在無 int09 安裝時天然 stall，
  屬既有設計（`keyboard.go:88-114`），非本階段新缺口；正常玩家
  路徑一律經 sealed 投遞，不受影響。
- 診斷暫存（`/tmp` probe 樹）已清；原版全程唯讀掛載。
