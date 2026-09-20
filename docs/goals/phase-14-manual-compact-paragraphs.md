# 第十四階段目標：首批短篇繁中手冊段落校訂

狀態：完成  
日期：2026-09-20  
前置：[第十三階段繁中來源對照](phase-13-manual-source-crosswalk.md)  
工作追蹤：[GitHub Issue #6](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/6)、
[#8](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/8)

## 本輪開工讀取紀錄

本檔建立後必須完整讀回才可裁切掃描、校字或修改 catalog。本輪已重新載入專案規則、
復古遊戲路由、`reverse-engineer-retro-game-remake` 技能與規格閘門契約。第十三階段的
來源對照只證明定位；本輪每筆文字仍須回到原始掃描逐字核對。

## 目標

選取來源為 `confirmed`、內容位於單一短段落且不需要先決定多頁資料格式的題目，建立首批
可顯示繁中 catalog。預定處理 `The Elevator`、`The King in 0-G`、`Jupiter Arrival`、
`The Great Rift`、`Buck's Capture`、`Acidic Victory`、`Alert Screen`、`Lens Treatise`。
每筆保留題目鍵、來源掃描與人工校訂收據；不得直接採用 OCR 誤字。

## 成功定義

1. 對八個來源頁建立只留在 `workplace/` 的可重生裁切或原圖回查收據，逐字核對標題與段落。
2. 為八筆建立唯一 `event_key → text_key` 映射，加入 UTF-8 繁中 catalog；不包含答案。
3. 擴充 catalog 驗證，使手冊文字鍵與 39 筆題庫／來源對照一致，未知或強推論不得誤入。
4. 記錄每筆字數與目前單行 TSV 邊界；長章節、表格與跨頁內容留待另訂分頁資料格式，不在
   本輪暗中決定。
5. 更新研究文件、DRAFT、`CONTEXT.md`、`WORKLOG.md` 與索引；在 Docker 內通過測試、
   擁有權與容器稽核後，推送 `main` 並更新 GitHub Issues #6、#8。

## 不屬於本階段

- 不實作 production dosgolem 覆繪，不升級 READY／CONFORMED。
- 不決定 2×／3× 倍率、分頁 UI、長章節換頁格式或正式字型。
- 不處理 `strong-inference`、`unknown`、表格或跨頁長章節。
- 不解碼、保存、顯示或自動輸入英文答案。

## 退出條件

八筆短篇段落均有原圖逐字核對、可驗證鍵值與來源 metadata；catalog lint 及來源一致性測試
通過，未把 OCR、自動作答或未定分頁格式混入正式資料。

## 完成收據

- 八張半頁裁切均由原始掃描在 Docker 內重生並保存 SHA-256；文字已逐張目視校訂。
- 新增八筆繁中段落；連同既有 Deimos，`manual-events.tsv` 與 catalog 共 9 筆精確映射。
- `manual_catalog.py` 要求題庫身分一致、來源為 `confirmed`、事件鍵頁碼／序數一致、鍵值唯一
  且無孤兒 catalog。
- 19 項測試、catalog lint 與真實題庫／來源／事件／文字交叉驗證通過。
- 已記錄 35–236 字元的實際長度範圍；未藉此決定頁數、倍率或 production 版面。
