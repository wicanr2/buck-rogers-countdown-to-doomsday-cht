# 第四階段目標：選單互動與覆繪失效生命週期

狀態：已完成（Enter 向前轉場與舊文字清除已量到；返回等生命週期仍未知）  
日期：2026-09-20  
前置：[第二階段文字分派與生命週期證據](phase-2-text-dispatch-and-lifecycle.md)  
工作追蹤：[GitHub Issue #3](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/3)、[#4](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/4)

## 本輪開工讀取紀錄

本檔建立後必須讀回才可開工。本輪使用已確認的產品方向：只做 dosgolem 執行期輸出端
繁體中文化，不做 clean-room remake；原版 EXE、資料、規則、手冊驗證與存檔語意保持不變。

## 目標

從第二階段固定的功能選單狀態，以原版正常滑鼠或鍵盤輸入走至少一個選單互動與畫面轉換，
量測文字分派事件、畫面變更、清除／重繪與返回時機。產出用於覆繪失效規則的 dosgolem
收據，而非直接繪製中文。

## 成功定義

1. 建立一條不使用 memory poke、傳送座標、forced-win 或原版資料改寫的正常選單輸入路徑，
   並記錄固定初始狀態、輸入、畫面／狀態檢查點與重播結果。
2. 在互動前後比較原始文字 dispatcher `0763:0424`、字元 renderer、VRAM 與畫面輸出，
   分別記錄已證實的重繪、清除、轉場或未知項目。
3. 對 DRAFT 覆繪規格補充可驗證的失效候選；若現有證據仍不足，明定 READY 前的最小缺口。
4. 本輪完成後檢查 Docker 衛生、文件連結與 Git 邊界，推送 `main`，並更新相關 GitHub
   Issue 的真實狀態。

## 不屬於本階段

- 不畫中文、不建立字型或翻譯 catalog，不修改 dosgolem production path。
- 不以坐標傳送或直接記憶體改寫取代正常玩家輸入。
- 不將本條選單路徑外推為全遊戲文字、手冊提示或完整中文化。

## 退出條件

成功定義均有 dosgolem 可重生收據與分級研究文件支持時結束；若 first blocker 是未知的
輸入語意或觀測缺口，必須記錄最小缺口，不能以猜測 hook 或篡改原版跨越。

## 完成收據

[選單互動與失效生命週期](../re/phase-4-menu-interaction-lifecycle.md) 保存正常 BIOS Enter
路徑、兩次相同 VRAM 重播、新字串分派與舊選單像素清除的精確時序。
