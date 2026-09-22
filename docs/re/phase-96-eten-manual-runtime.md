# 第九十六階段：倚天手冊中文執行期整合

日期：2026-09-22。範圍：實作已確認需求，不新增設計分支。

dosgolem 本機實作提交：`3e293cd`（`buck-rogers-cht-output-overlay` 分支，未推送上游）。

## 已證實交付

- `tools/eten_font.py` 由本機倚天來源產出 691 個 16×16 top-pad 字模，大小 25583 bytes，
  SHA-256 `78c10dec8055110764013007899c4455b91256a78f94e212294ac9c51c01364e`。
  來源入口、命令及權利界線見 [字型入口](../../font/README.md)。
- 本機 dosgolem 的 `cmd/buckrogers-text-receipt` 已接通 Watcher → Bridge → Consumer →
  RuntimeManualOverlay。前景／背景取自原題 dispatcher 參數；本次為 fg=10、bg=0，
  不改寫 VRAM。不具樣式證據時拒絕繪製；調色盤更新不復活已失效圖層。
- 首題 `manual.page34.deimos_prison.word10` 顯示正式 catalog 的 73 字段落。
  2×／3× 各有 3776 個中文變更像素，正文矩形外均為 0。
- 輸入錯答後原版自行重抽；新題未命中現有 catalog，舊中文完全清除，兩倍率像素差均為 0。
- 兩情境的事件、記憶體、原始 indexed 畫面、調色盤及完整持久化機器／DOS 狀態均等於控制組。
  gob 的 map 編碼及 map 衍生 handle 陣列順序不固定，故不以壓縮檔 bytes 作語意相等判準。
  `cmd/state-compare` 解碼既有完整 schema，正規化 map／handle 排序後比較 SHA-256；不改存態格式。

## 重跑入口及本機收據

使用既有 `golang:1.24-bookworm` 建置 dosgolem 的 `cmd/buckrogers-text-receipt` 與
`cmd/state-compare`，再以 `python:3.12-slim` 執行下列命令。所有步驟限 Docker，非主機命令。
容器使用非 root、資源限額、`--rm`、`--network none`；先驗證掛載來源存在。
專案唯讀掛 `/project`，其 `workplace/` 可寫；原版 `workplace/original/BRcdoom` 唯讀掛 `/orig`。

```sh
python tools/manual_runtime_smoke.py \
  --command workplace/dosgolem/workplace/out/buckrogers-text-receipt \
  --state-compare workplace/dosgolem/workplace/out/state-compare \
  --state workplace/probe/phase12-before-question.state \
  --font workplace/phase96-font/buckrogers-eten-top-pad.golemfnt \
  --out-dir workplace/phase96-first-rerun
```

錯答案例另指定新的 `--out-dir`，加上
`--until 301240000 --bios-key-at 300100000:2d:78 --bios-key-at 301100000:1c:0d --expect cleared`。
腳本拒絕覆寫既有收據。首題停止步數 266557247，初始步數 266399999。
輸入狀態 SHA-256：`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`。
這是固定原版完整狀態重播，不宣稱已另行設定或辨識亂數種子。

本輪收據位於 `workplace/phase96-first-final/`、`workplace/phase96-wrong-final/`，
各含 `verification.json`、完整存態比較摘要、原版／覆繪 RGBA、PNG 及原始事件收據。
首題覆繪 RGBA SHA-256：

- 2×：`da3007bc54ecd0e52dd6a7f8979619808e54521ca6e176686403374dcafed5fb`。
- 3×：`c1d3e53b47f3b4a05afce34d2f011f0dac01b5e16b0ebe150ecba66c10950b87`。

專案 Python 測試 172 項通過；dosgolem 的 machine、DOS、狀態比較命令、Buck Rogers、
xlate、文字收據命令測試通過，手冊子代理另完成 race 與 vet。
字型、遊戲、完整狀態與圖片只留本機，不加入 GitHub。

## 限制及後續

舊 phase12 固定狀態的 palette 15 為黑，原版控制組的部分英文亦不可見；沒有擅自補白色。
這不妨礙中文矩形隔離驗收，但不能據此宣稱原題周邊文字目視可讀性已完整驗收。
錯答第二題未命中 catalog，不代表它已中文化。返回、存讀檔與互動式前端尚未完成驗收，
GitHub #14 保持開啟。此文件不改變快捷字母白色、其餘文字沿用原色的既定需求。

規格入口：專案 [spec 008](../spec/008-eten-top-pad-local-font-builder-draft.md)，
本機 `workplace/dosgolem/docs/spec/222-buck-rogers-manual-runtime-presentation.md`。
