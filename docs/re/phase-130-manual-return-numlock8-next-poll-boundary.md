# 第一百三十階段：手冊返回 Num Lock 8 分支至下一次鍵盤輪詢

日期：2026-09-22
狀態：**已確認單一合法 Num Lock 8 分支在下一次無鍵 BIOS 輪詢前沒有進入保存／讀檔或玩家可見轉場；此分支到此停止。**

## 問題、輸入與停止條件

第一百二十六階段已確認私有 page6 state（SHA-256
`d20cbc0bf0b7425ab29b26a59666b91bbd32c1e5776ee9593190b4cd8918fcb5`）的 Data Card 明示
Num Lock 前進鍵會被原版取走，並走進 `37F1:118A`。本階段只從同一 state 再排入同一筆
step `331000000` 的 `48h:38h`；不加入第二鍵、不改 state 或原版資料。

診斷在已觀測分支後以 runtime `0C10:0305` 為停止點。dosgolem 的 BIOS INT 16 收據在 step
`331000653` 明確記錄 `AH=01h`、`available=false`；這是**下一次鍵盤輪詢**，早於先前寬追蹤中
才會到達的 caller return。因此本收據在 `331000653` 停止，符合「consumer return 或下一次
key-poll，先到者停止」的界線。

這個 `AH=01h` 判定來自受控 dosgolem BIOS 服務的 content-safe instrumentation：只記錄功能號與
是否有鍵，不記錄任何原版文字、畫面 bytes 或鍵值。它證明原版 consumer 已回到等待／檢查輸入的
控制流，**不**為遊戲狀態、移動、隊伍或選單賦予語意。

## 控制流與狀態 gate 分級

- **已確認（dosgolem 實模式 `segment:offset`）**：`INT 16h/AH=00h` 在 step `331000198` 從 BDA
  取走 `0x4838`，caller chain 為 `37F1:1116 ← 328E:1732`。分支追蹤由已確認的
  `37F1:118A` 延至下一次 `AH=01h` poll；該 poll 不消耗佇列，`keys_pending=0`。
- **已確認（dosgolem service metadata）**：停止前的下一次 poll 為 step `331000653`、`AH=01h`、
  `available=false`、handler runtime `0C10:0305`。這是原版請求 BIOS 服務的可觀測結果，不是
  IDA 位址。
- **強推論（IDA 9.4 裸 OVR file-offset view）**：第一百二十六階段的唯一 32-byte prefix 對應
  `GAME.OVR` file offset `183158`，可見 `AL` 暫存與未命名 `byte_8435` 的零值條件。其輸入
  SHA-256 為 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。此靜態線索沒有
  新增 gate 名稱，也不可與上述 runtime `37F1:*`／`0C10:*` 或檔案 offset 混用。

本階段沒有新的 gate write 證據；`byte_6B49`／`byte_8435` 保持第一百二十六階段的分級與未命名
狀態，不能被稱為保存、隊員、劇情或位置欄位。

## 同狀態 A/B 與玩家可見／檔案邊界

同一私有起始 state、同一終止 step `331000653` 比較單鍵分支與無鍵 control：

| 比較項目 | Num Lock 8 | 無鍵 control | 結論 |
| --- | --- | --- | --- |
| indexed framebuffer SHA-256 | `e6177505…48fa0b6a` | 相同 | 無玩家可見 indexed 畫面差異 |
| palette SHA-256 | `67c6c8a8…f37c55e88` | 相同 | 無色盤差異 |
| dispatcher event／FileOps／writes／未實作服務 | 空 | 空 | 沒有選單、檔案或未實作服務證據 |
| 完整 machine memory SHA-256 | `c108a6be…b743ad999` | `6b8494be…96775f473` | 有內部狀態差異；語意未知，不能忽略或命名 |

所以這只排除「合法 8 直接顯示轉場／進入保存檔 I/O」；不能證明它在遊戲規則中無效，也不構成
遊戲內保存／讀檔 A/B。

## 停止線與唯一下一步

第一百二十三階段的手冊證據仍只明示：讀檔在主選單或隊員管理選單，保存在隊員管理選單 A–J
槽位。這條唯一已證實的 Num Lock 8 路徑已回到無鍵 poll，沒有到達任一入口。因此不再以它重複
嘗試或猜測其他 command key。

下一個可行切片必須先從已盤點的中／英文手冊找出**另一個明示按鍵及其適用條件**，或找回一個
正常玩家可重播、已處於主選單／隊員管理選單的 state；只有其中之一成立，才可以對該條路徑做
同狀態 save/load A/B。否則保存／讀檔分支維持停止。

## 環境、權利與清理

分析、IDA 9.4 和重播均使用一次性、無網路 Docker；原版與 state 唯讀掛載。所有原始 bytes、
IDA DB、state、完整收據與診斷工具只留在 ignored `workplace/phase124-keytrace/` 或
`workplace/dosgolem/`。本階段沒有改正式規則、runtime overlay、翻譯 catalog 或原版資料。

鍵盤 poll metadata 的本機 dosgolem 診斷提交為 `6f828360d61696e822fd206c1fbef7c72ada02b1`
（`buck-rogers-cht-output-overlay` branch；僅本機、未 push）。它預設不收集資料；唯有
`buckrogers-text-receipt -key-trace` 才啟用，並從 `-instruction-trace-from` 起最多保留 4096 筆
content-safe poll metadata。Docker `golang:1.24-bookworm` 下的
`go test ./internal/dos ./cmd/buckrogers-text-receipt -count=1` 通過。

在既有私有輸入與本機已建置 receipt runner 均存在時，下列 content-safe 重播會在首個後續 poll
精確停止；它不包含手冊答案、原版文字或可散布輸入：

```sh
docker run --rm --network none --memory 3g --cpus 2 --pids-limit 256 \
  -u 1000:1000 \
  -v "$PWD/workplace/original/BRcdoom:/orig:ro" \
  -v "$PWD/workplace/phase123-story-page6-enter:/state:ro" \
  -v "$PWD/workplace/phase124-keytrace:/out" -w /orig \
  fd2-go-test-local:latest /out/buckrogers-text-receipt \
  -state /state/page6.state -until 340000000 \
  -bios-key-at 331000000:48:38 -file-ops -unimplemented -key-trace \
  -instruction-trace-from 331000229 -instruction-trace-limit 512 \
  -stop-at-segment 0x0c10 -stop-at-offset 0x0305 -stop-after-step 331000229 \
  -receipt-out /out/forward-numlock-next-poll.json \
  -state-out /out/forward-numlock-next-poll.state
```
