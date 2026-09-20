# 第 22 階段：dosgolem xlate 通用整數倍率

## 狀態

完成

## 本輪目標

在 workplace dosgolem 分支擴充通用 `xlate` renderer，使 16×16 GOLEMFNT 可用 2× 與既有
3× 整數倍率繪製；保留像素銳利、無濾波、裁切安全與既有 3× 行為，不替《拯救地球》選定倍率。

## 範圍

- 回讀目前 `xlate.Draw`、`Layout` 與測試，確認倍率限制的實際原因。
- 將 renderer 的倍率契約改為可驗證的正整數縮放，至少支援 2×、3×。
- 增加 2×／3× 像素 footprint、色彩、裁切、缺字與非法倍率測試。
- 使用專案現有 GOLEMFNT 與正式繁中文字元做原生解析度 smoke；輸出只留 workplace。
- 在 dosgolem 工作分支提交本機 commit；未獲額外授權前不推送 dosgolem 遠端。

## 不在本輪範圍

- 不決定《拯救地球》正式採 2× 或 3×。
- 不接入遊戲專用事件 adapter 或 production 中文覆繪。
- 不採非整數縮放、抗鋸齒或影像濾波。
- 不改變 `Layout` 的換行、分頁或字元格語意。
- 不複製 PC-98 美術、邊框、圖示或遊戲文字。

## 驗收條件

- `xlate.Draw` 的 2× 與 3× 有精確像素測試，既有測試全數通過。
- scale 0、負值及超出目標 bounds 的輸入失敗即關閉或安全裁切，不發生 panic／越界。
- 真實 GOLEMFNT 至少繪製一組繁中字元，2×／3× 均維持整數像素與無濾波。
- workplace dosgolem 工作樹乾淨並有本機 commit；不推送其遠端。
- 專案測試通過，並完成 Docker 容器、擁有權與工作樹檢查。
- 推送專案 `main`，更新 GitHub Issues #6 與 #8。

## 預定交付物

- workplace dosgolem 的 `xlate` 程式、測試與本機 commit
- `docs/re/phase-22-dosgolem-xlate-integer-scale.md`
- `docs/spec/002-manual-paragraph-overlay-draft.md`、`CONTEXT.md`、`WORKLOG.md` 與索引更新

## 完成紀錄

- workplace dosgolem 本機 commit：`ef7f8db32b20a6b9eb6d810bd4e6b99187c55f44`。
- 2×／3×、非法倍率、裁切與既有正式套件測試全數通過。
- 真實 GOLEMFNT 已在 2×／3× 畫出繁中「地球」；收據留在 `workplace/phase22-xlate-smoke/`。
- 沒有推送 dosgolem 遠端，也沒有選定《拯救地球》的正式倍率。
