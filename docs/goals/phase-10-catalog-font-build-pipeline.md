# 第十階段目標：繁中 catalog 與 GOLEMFNT 建置管線

狀態：已完成  
日期：2026-09-20  
前置：[第九階段 dosgolem 通用繁中覆繪基礎](phase-9-dosgolem-xlate-foundation.md)  
工作追蹤：[GitHub Issue #5](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/5)、
[#7](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/7)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可新增工具或字型目錄。本階段只建立不依賴 2×／3× 決策的翻譯
資料驗證、字元清單與 GOLEMFNT 建置能力；GNU Unifont 僅作具授權的測試輸入，不自動成為
正式產品字型，生成的 prototype 字型留在 `workplace/`。

## 目標

把第八階段的 `text/menu.zh-TW.tsv` 從手工草案提升為可機器驗證的顯示資料：失敗即關閉地
檢查 UTF-8、標頭、欄數、空值、重複 key、控制字元、正規化與來源枚舉；由所有可見譯文
決定性產生排序後字元清單。建立讀取 GNU Unifont `.hex`／`.hex.gz` 並輸出 dosgolem
`GOLEMFNT` 16×16 子集的工具與測試，再由 dosgolem `xlate.LoadFont` 回讀實際產物驗證。

## 成功定義

1. 完整讀取專案規範、在地化顯示／語意隔離入口、相關字型方法與第九階段 `GOLEMFNT`
   契約；確認字型來源授權文字與雜湊。
2. catalog lint 對 UTF-8、精確欄位、唯一 key、非空繁中、允許來源值、禁用控制字元與 NFC
   提供正反向測試；測試不得依賴原版素材。
3. 字元清單只由正式 TSV 的 `translation` 欄衍生，固定排序、換行與 UTF-8；缺字失敗即關閉。
4. font builder 支援 Unifont 8×16／16×16 記錄，統一置中輸出 16×16 GOLEMFNT；檔頭、碼點、
   來源 byte、字模長度與決定性有單元測試。
5. 使用本機唯讀 GNU Unifont 產生被忽略的 prototype 子集，經 dosgolem `xlate.LoadFont`
   實際回讀並確認所有 catalog 字元均存在；記錄輸入／輸出 SHA-256，不提交字型二進位。
6. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；Docker／擁有權稽核後推送
   `main`，更新相關 GitHub Issues。

## 不屬於本階段

- 不選擇 2× 或 3×，不宣告 GNU Unifont 為正式產品字型。
- 不建立 Buck Rogers adapter，不接 runtime hook，不升級 READY／CONFORMED。
- 不複製倚天、Noto、Cubic 或其他專案字型資產；不加入原版／手冊素材。
- 不翻譯本輪尚未由原版事件證實的劇情、戰鬥或手冊段落。

## 退出條件

catalog、字元清單與 GOLEMFNT 工具均有正反向測試，真實 Unifont 子集能由 dosgolem 回讀且
覆蓋現有八筆繁中，所有產物與授權邊界可追溯；正式倍率與字型選擇仍保持 pending。
