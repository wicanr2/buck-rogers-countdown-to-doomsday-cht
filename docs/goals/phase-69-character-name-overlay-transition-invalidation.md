# 第六十九階段：角色姓名覆繪轉場失效生命週期

狀態：已完成

## 目標

從第六十八階段已 CONFORMED 的姓名提示覆繪出發，沿正常玩家輸入驗證 Enter 確認轉場與
Escape 原地重印兩條路徑；找出原版清除／重畫事件對 overlay stamp 的實際失效作用，確保
繁中提示不殘留到技能配置畫面，也不因 Escape 重複堆疊。

## 範圍

- 重讀第四十四階段姓名輸入生命週期與正式事件清冊，重生短姓名 `A` 的 Enter 正常 BIOS
  路徑，以及已證實只重印提示、不取消的 Escape 路徑，不使用記憶體注入或直接跳轉。
- 以 dosgolem 現有 `026F:029C` 清除矩形 hook 及逐格 invalidation 觀測 active overlay keys；
  若既有通用清除已涵蓋轉場，只補正式收據，不新增遊戲特例。
- 對 Enter 與 Escape 分支各做 control、2×、3×，各倍率雙重重播；驗證 raw framebuffer、
  events、BIOS keys 與姓名輸入語意不受 overlay 影響。
- 驗證 Enter 終態不含 `character.name.prompt`；Escape 終態恰有一個同 key stamp，不能重複
  堆疊。轉場後不得把殘留中文帶入下一頁。

## 不在本階段

- 不翻譯技能配置頁的新文字，不改姓名確認、Escape 重印、Backspace、欄位長度或存檔語意。
- 不選定產品預設倍率，不處理手冊版面。
- 不因單一 event key 硬編清除；若缺少通用可證明的原版失效事件，規格退回 DRAFT。

## 完成條件

1. Enter／Escape 的輸入步數、終態事件、framebuffer 與第四十四階段證據對齊；Escape 不得
   被誤稱為取消。
2. 兩分支在 2×／3× 各雙重重播一致，presentation 欄位外的收據等於 control。
3. Enter 終態 active keys 不含姓名提示；Escape 終態恰有一個姓名提示 key，沒有重複 stamp。
4. 若修改 dosgolem，必須先有 READY 規格，再通過正式測試、vet 與相關 race detector。
5. 專案回歸通過；dosgolem 只提交本機 branch，專案 `main` 推送並更新相關 Issues。

## 退出條件

- 若第四十四階段舊步數因 palette 修正後 state 漂移，以 exact event 與玩家可見終態重新對齊，
  不放寬事件 identity。
- 若 Enter 轉場沒有經過既有清除 hook，先保存原版清除／重畫 callsite 與矩形證據；
  不直接把「離開姓名頁」寫成產品特例。
- 若正常玩家路徑本身無法抵達預期終態，先分類 dosgolem 能力缺口，不用舊截圖冒充新收據。

## 完成摘要

- Enter 正常路徑為 226 events／1 request／225 misses；原版清除 hook 使終態 active keys 為空，
  2×／3× RGBA 均等於 baseline，技能配置畫面沒有姓名提示殘留。
- Escape 路徑為 184 events／2 requests／182 misses；原版只重印提示，兩筆 actions 以同 key
  replace，終態恰有一個 stamp，沒有堆疊。
- 兩分支 control 與 2×／3× 均雙重重播一致；presentation 欄位以外等於 control，raw
  framebuffer 不變。原始解析度實圖已確認 Enter 清除與 Escape 留頁。
- spec 208 已 CONFORMED；本階段沒有加入遊戲專屬清除、選定倍率或更改 Escape 語意。
