# 第一百九十一階段：技能頁離開確認提示的原文勘誤與繁中草稿

日期：2026-09-23
狀態：**原文身分已證實；繁中 TSV 為 DRAFT，未接正式 watcher／覆繪。**

## 本次勘誤

先前私有翻譯盤點將職業技能頁的確認提示列為原文未知。本次代理直接從
唯讀原版 `GAME.OVR` 檔案 offset `0x25A2B` 取 33 bytes，SHA-256
`65108526a62ebc58d90c1406cce2b83133f5a8fa5221f87e6f62f40589bc07a9`，
與既有 `career-skill-exit-events.tsv` 的 exact identity 完全一致；故「找不到
原句」的舊結論已被原始 bytes 否定。技術技能頁的同類提示位於檔案 offset
`0x25A4D`、長 34 bytes，SHA-256
`5592b4048986b175d187438df9b7ecd154cdedc775a9ff290231d5e3863a9a9b`，
也與 `technical-skill-exit-events.tsv` 一致。兩個 offset 都是**檔案位移**，
不是 dosgolem 實模式位址。

原版 `GAME.OVR` SHA-256 為
`3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0`。
原版文字與可還原 bytes 只在 ignored
`workplace/skill-exit-translation-draft-20260923.md` 與唯讀原版輸入，
本文件及 TSV 不保存原版全文。

## 可追溯的顯示事件與譯文

兩筆原版事件均為 `37F1:101E`（dosgolem 實模式 caller）、row 24、
column 0、背景 0／前景 13；career entry→return 為
`102701085→102726497`，technical 為 `103601017→103627195`。
兩句正式候選只保存在
[`skill-exit-confirmation.zh-TW.tsv`](../../text/skill-exit-confirmation.zh-TW.tsv)：
沿用既有技能頁 catalog 的「職業技能點數／一般技能點數」術語，分別表達
尚有點數未用與離開詢問，不改原版按鍵或判定。譯文各 17 個 Unicode 字元，
來源標為編輯性介面詞 `runtime-interface`，不是中文手冊逐字引文。

## 仍缺的 READY 門檻

原句與事件身分的證據等級是**已證實**；兩句繁中為**編輯性 DRAFT**。
尚未量到提示清除與恢復時的最早 A000 相交寫入、選擇尾碼的獨立顏色／
生命週期、文字安全矩形、2×／3×墨跡 containment、正式輸出 watcher
及原文／繁中同狀態 A/B。既有第 188 階段的多色 Exit 尾碼屬**另一個
功能選單**，不得把它的座標或顏色套用到技能頁。

本次僅新增 DRAFT TSV；它不能進入原版記憶體、比較、存檔或判定流程，
亦不表示技能頁確認提示已中文化。原版與字型產物維持 ignored 本機資料。
