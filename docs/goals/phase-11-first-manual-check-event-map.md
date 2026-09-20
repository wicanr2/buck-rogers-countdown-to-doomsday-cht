# 第十一階段目標：第一條手冊查閱事件與中文段落映射

狀態：已完成  
日期：2026-09-20  
前置：[第三階段中文手冊輸入清冊](phase-3-manual-input-inventory.md)、
[第七階段文字 post-call 與 generation 事件](phase-7-text-post-call-generation-event.md)、
[第十階段 catalog 與字型建置](phase-10-catalog-font-build-pipeline.md)  
工作追蹤：[GitHub Issue #6](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/6)、
[#8](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/8)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可執行遊戲、搜尋原版或處理手冊。上一輪已完成可重生的繁中字型
管線；本輪不依賴尚未決定的 2×／3× 畫面倍率，而是先建立「原版何時要求查手冊、要求哪一
段、中文來源在哪裡」的第一條可追溯垂直鏈。

## 目標

從正常玩家路徑或可重播的原版輸出定位至少一個真正的手冊查閱事件，保存其原文題目／提示
事件、原版判定前後狀態與返回／重試行為；再於使用者提供的中文說明中找到對應位置，建立
只含定位 metadata、中文顯示 key 與必要短段落的映射草案。中文段落只供未來輸出端覆繪，
不得寫入原版輸入或影響答案判定。

## 成功定義

1. 重新核對原版與中文手冊清冊、雜湊、工具版本及 dosgolem 能力，不把既有推論當事實。
2. 以正常玩家路徑優先取得至少一條手冊查閱畫面；若正常路徑距離過長，允許靜態字串定位
   及可丟棄 probe 縮小入口，但不得把 direct-entry 當完成收據。
3. 記錄該事件的原文、runtime 段:位移／步數、呼叫鏈或其他可回查定位，以及輸入後的
   判定／重試行為；保留已證實、強推論、假說或未知分級。
4. 在中文手冊以 archive-order 頁面及檔案 SHA-256 定位對應內容；Git 只保存必要短譯文、
   key 與 metadata，不保存原始影像、整頁 OCR 或可還原全文。
5. 建立 DRAFT 映射格式，至少連結原版事件、中文來源、顯示 key、顯示時機與未知的版面／
   分頁需求；不改防拷或手冊答案邏輯。
6. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；Docker／擁有權稽核後推送
   `main`，並更新 GitHub Issues #6、#8。

## 不屬於本階段

- 不宣告所有手冊題目已盤點，不把單一事件外推成完整防拷機制。
- 不實作正式 adapter、中文畫面或答案輸入替換，不升級 READY／CONFORMED。
- 不決定 2×／3× 倍率，不選定正式字型，不把原版或中文手冊全文加入 Git。
- 不繞過判定、不自動填答案、不提前顯示與當前事件無關的中文內容。

## 退出條件

至少一條正常玩家可遇到的手冊查閱事件已由原版輸出與中文手冊來源雙向定位，映射草案能
清楚區分顯示段落與答案語意，所有證據可重生且未洩漏受保護的整頁素材。

## 完成收據

[第一條手冊查閱事件與中文段落映射](../re/phase-11-first-manual-check-event-map.md)
已記錄正常選單路徑、第 34 頁 `Deimos Prison` 第十字、錯答重抽、中文掃描來源及
DRAFT 映射。原版答案輸入與判定未修改。
