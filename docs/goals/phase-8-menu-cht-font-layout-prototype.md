# 第八階段目標：功能選單繁中字型與版面 prototype

狀態：已完成  
日期：2026-09-20  
前置：[第七階段文字 post-call 與 generation 事件](phase-7-text-post-call-generation-event.md)  
工作追蹤：[GitHub Issue #3](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/3)、[#4](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/4)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可開始盤點或產生 prototype。本輪維持 dosgolem 輸出端繁體中文
覆繪，不修改原版 EXE、資料、規則、手冊驗證或存檔。參考 `psychic-war` 與
`curse_of_the_azure_bonds` 時只採用可重用架構、字型工具與版面驗收方法，不帶入其遊戲
專屬位址、譯文、素材或完成聲明。

## 目標

為功能選單第一條已證實文字路徑建立可丟棄的繁中視覺 prototype：盤點兩個參考專案的
正式字型來源、授權、renderer、catalog 與 text-safe rectangle 契約；建立本作首批功能選單
繁中譯文候選；以 dosgolem 的原生 320×200 色號畫面產生至少兩種整數像素字型／排版對照，
量測 containment、可讀性與原文清除範圍。本階段不把 prototype 當 production hook。

## 成功定義

1. 完整讀取 Golden Box CJK 版面 reference，以及兩個參考專案與字型／overlay 直接相關的
   規格、來源與程式；記錄哪些可重用、哪些不可複製及各自授權邊界。
2. 從既有九筆功能選單／`PICK RACE` dispatcher 收據辨識首批可見原文與 row／column／色彩；
   無法從現有證據證實者標為未知，不猜寫 catalog。
3. 建立只含本階段已證實鍵值的 UTF-8 TSV 草案與驗證規則；繁中不得回流原版語意路徑。
4. 以可追溯且允許本專案使用的字型候選，在原生 320×200 上產生至少兩種可丟棄畫面；每種
   明示 cell、baseline、spacing、色彩、text-safe rectangle 與 overflow 策略。
5. 用像素計算與實際畫面檢查每個候選是否完整清除原文、未越出批准矩形、整數縮放且無濾波；
   若視覺取捨仍有多個合理答案，保留對照供使用者決定，不自行固化成正式產品方向。
6. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；完成 Docker 衛生檢查，推送
   `main` 並更新相關 GitHub Issues。

## 不屬於本階段

- 不建立 production adapter，不把規格升為 READY／CONFORMED。
- 不翻譯劇情、戰鬥、角色名稱或手冊段落；不從掃描手冊擷取可還原全文。
- 不把 PC-98 日文畫面、美術、字型或其他專案譯文當成本作可散布素材。
- 不以放大後看似清楚取代 320×200 原生像素 containment 驗證。

## 退出條件

參考證據、首批 TSV、至少兩個原生尺寸 prototype 與量測報告均可重生，且所有未決視覺取捨
明確列出時結束。若沒有已授權字型可供 prototype，必須記錄候選與授權缺口，不得從原作或
其他遊戲抽取字模冒充可用資產。

## 完成摘要

已由正常 Enter 重播取得九筆來源並以中文說明書核對六個種族譯名；建立 UTF-8 TSV、
GNU Unifont 2×／3× 整數輸出 prototype、重生工具與 containment／授權報告。兩案仍保留
供使用者決定，未建立 production adapter 或把 DRAFT 升級。
