# 第五十三階段：保存選項控制流與名冊接納狀態

## 輸入與位址基準

- 兩路都由 `workplace/phase52/save-before.state`（絕對 step `119,800,000`）載入；原版輸入
  雜湊沿用第五十二階段固定值。
- 原版目錄唯讀；每路使用獨立 scratch，起始只含 pristine `CHARS.DAX`。
- 本文 `CS:IP` 全為 dosgolem 8086 執行期位址，不與 IDA 線性位址混用。

## 已證實的勘誤

- 先前把保存分支命名反了。直接在 step `120,200,000` 送 Enter 的「預設 Enter」路徑，
  會於 step `120,205,401` 建立 `A.who`，並於 `120,205,903` 建立 `A.stf`。
- 先於 step `120,000,000` 送 Left、再於 `120,200,000` 送 Enter 的路徑不建立這兩個檔案。
  因此第五十至五十二階段稱作「Left→YES」及「預設 NO」的標籤錯誤；可重播輸入與畫面
  收據仍成立，但分支語意及「沒有 DOS write」結論不成立。
- 過去完整配置收據走的是 Left→Enter 不保存分支；不是 dosgolem 吞掉保存。

## 控制流與檔案收據

- 兩路同 step 首次分歧在 `120,000,036`：Left 路為 runtime `0C10:0309`，預設路為
  `0C10:030B`。這是 Left 輸入造成的選項分歧，不把它誤稱為保存 transaction 本身。
- 預設 Enter 路徑依序以 `int 21h/AH=3Ch`、`40h`、`3Eh` 建立、寫入並關閉兩檔；執行期
  trace 保存了 `0CF4:18DB` 的 create 返回及 `0CF4:19A9..19B0` 的 259-byte write。
- `A.who` 為 259 bytes，SHA-256
  `43b7dc3b227c7700d1a60cb3f17a43008e8beaa17ceec0c95873f3d18b34aa53`；`A.stf` 為
  124 bytes，SHA-256 `90bd838048737e5be659fe81ca147174677e86228de8977bf0522e781944b1ab`。
- 兩路 step `120,800,000` framebuffer SHA-256 都是
  `b08623d259a39bb2b3c755b3312e0afe413411bed53649d13e99019c5fbdf3a3`；相同終點畫面不能
  證明沒有檔案副作用。

## 決定性與目前限制

- 兩次獨立重播的兩路 IP trace 各自逐 byte 相同；Left 路 memory、兩路 framebuffer 及
  預設保存路徑的 `A.who`／`A.stf` 亦各自相同。
- 預設保存路徑的兩份完整 memory 有差異，且執行期間呼叫 `int 21h/AH=2Ch` 取時間；尚未
  證明所有 memory 差異都來自時鐘，因此不宣稱完整 memory 決定性。
- 本輪只證實真正保存分支及檔案輸出。兩檔是否足以讓 Add 顯示角色，仍須由同一正常玩家
  路徑接續驗證；檔案內容只留在被忽略的 `workplace/`，不加入版控或散布。
