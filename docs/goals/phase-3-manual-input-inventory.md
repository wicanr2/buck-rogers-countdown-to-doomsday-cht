# 第三階段目標：中文手冊輸入清冊與頁面定位

狀態：已完成（RAR 清冊、完整性與逐檔 SHA-256 已建立；語意配對仍未開始）  
日期：2026-09-20  
前置：[第二階段文字分派與生命週期證據](phase-2-text-dispatch-and-lifecycle.md)  
工作追蹤：[GitHub Issue #1](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/1)、[#4](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/4)

## 本輪開工讀取紀錄

本檔建立後必須讀回才可開工。本輪沿用已載入的專案 `AGENTS.md`、復古遊戲路由、
dosgolem 文件與輸出端中文化邊界；不重新定義「輸出端覆繪」與「完整 remake」尚未確認的
產品方向。

## 目標

在 Docker 內、以使用者自備的 `珍074-拯救地球.rar` 為唯讀輸入，取得可重生的 archive
內容清冊與頁面／檔案定位資訊，讓日後原版實際出現手冊題目時，能以中文手冊段落來源作
比對。此階段只建立 metadata、雜湊與定位，不把手冊掃描、OCR 全文或可還原內容寫進 Git。

## 成功定義

1. 確認可用的 Docker-only RAR 解壓／列舉工具；記錄映像、版本、輸入雜湊與輸出位置。
2. 將 archive 成員名稱、大小、壓縮資訊與必要時的頁面順序寫入被忽略的 `workplace/`
   清冊；原始檔與解壓內容仍不進 Git。
3. 若 archive 含可辨識頁面，建立只含檔案定位、雜湊與權利邊界的 versioned 索引；不保存
   手冊全文或影像。
4. 若現有隔離工具仍不能讀取 RAR，記錄精確能力缺口與安全的下一步，不把檔案內容猜成
   已盤點。
5. 本輪結束前檢查 Docker 衛生、文件連結與 Git 邊界，推送 `main`，並更新相關 Issue。

## 不屬於本階段

- 不進行 OCR 全文、翻譯、手冊題目配對或遊戲流程改動。
- 不把任何手冊原圖、內容文字或可還原衍生物放進 GitHub。
- 不將 RAR 可列舉誤稱為遊戲手冊功能已接通。
- 不決定專案要維持輸出端中文化或改為完整 remake。

## 退出條件

成功定義所有項目均以可重生 Docker 收據與分級文件支持時完成。若缺少的只有 RAR 容器
工具，記錄該工具缺口後停止依賴內容的分支，不以主機程式或不明來源的輸出繞過。

## 完成收據

[中文手冊輸入清冊](../re/phase-3-manual-input-inventory.md) 記錄 Docker 工具、80 項
archive 完整性、79 個解壓檔 SHA-256 與不含內容的頁面定位索引。
