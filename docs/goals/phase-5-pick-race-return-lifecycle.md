# 第五階段目標：種族選擇畫面的離開與返回生命週期

狀態：已完成（Escape 正常返回與逐位元重播已量到；正式 hook 仍待下一階段證明）  
日期：2026-09-20  
前置：[第四階段選單互動與覆繪失效生命週期](phase-4-menu-interaction-lifecycle.md)  
工作追蹤：[GitHub Issue #3](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/3)、[#4](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/4)

## 本輪開工讀取紀錄

本檔建立後必須讀回才可開工。本輪沿用已確認方向：僅以 dosgolem 在原版輸出端覆繪繁體中文；
不做 clean-room remake，不變更原版 EXE、資料、規則、手冊驗證或存檔語意。

## 目標

由第四階段已證實的 `PICK RACE` 正常到達狀態，量測一條原版可接受的選擇、取消或離開輸入，
以及其後的畫面清除、文字重繪與（若原版路徑提供）返回行為。結果用來縮小覆繪 generation／
invalidation hook 的證據缺口，不直接繪製中文。

## 成功定義

1. 從固定 `PICK RACE` 狀態以 BIOS BDA 鍵盤或已證實熱區的原版正常輸入，取得至少一條會改變
   玩家可見畫面或選擇狀態的路徑；記錄輸入被原版接受的證據。
2. 對該路徑量測 `0763:0424`、至少一個既知舊文字 VRAM 像素與終點 VRAM，分開記錄輸入、
   dispatch、清除與重繪的先後，不把未量到的返回行為推定為已證實。
3. 以相同初始狀態、相同輸入與相同步數重播終點 VRAM，保留雜湊和可重生收據；無法重播時
   以失敗證據界定下一個最小觀測缺口。
4. 只在證據支持的範圍更新 `docs/re/`、DRAFT 規格、`CONTEXT.md`、`WORKLOG.md` 與索引；
   完成後驗證 Docker 衛生、推送 `main` 並更新相關遠端 Issue。

## 不屬於本階段

- 不實作 dosgolem production hook、不畫中文、不建立字型或翻譯 catalog。
- 不用 `-poke`、傳送、forced-win、原版資料改寫或其他診斷捷徑替代玩家輸入。
- 不將一條種族選擇路徑外推為所有選單、手冊關卡或完整中文化。

## 退出條件

成功定義均有可重生的 dosgolem 收據與推論等級文件支持時結束；若可用輸入語意或觀測能力
不足，必須記錄最小阻塞證據並保持 DRAFT，不得猜測正式 invalidation hook。

## 完成收據

[種族選擇畫面的離開與返回生命週期](../re/phase-5-pick-race-return-lifecycle.md) 保存
`PICK RACE` 固定狀態、BIOS Escape 消費、舊標題像素清除、功能選單重建與兩次相同 VRAM
重播收據；`workplace/dosgolem/` 的專用分支配置亦記錄於該文件。
