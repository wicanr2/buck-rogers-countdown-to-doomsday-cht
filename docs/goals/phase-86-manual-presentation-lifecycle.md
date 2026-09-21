# 第八十六階段：手冊 presentation lifecycle 接線

狀態：完成

## 目標

將已 READY 的手冊 runtime watcher 擴充為一條只含 presentation metadata 的 typed lifecycle
queue，使未來手冊 RGBA presenter 能準確收到 begin、clear 與 request 的 generation 邊界；完成
規格、dosgolem 實作、單元測試與正常玩家 metadata 收據，但不繪製中文段落。

## 已確認前提

- `2A33:01ED` 的精確題首會建立新 generation 並使舊 visible 失效；`026F:029C` 的 clear
  可在 pending 中途出現；只有 `2A33:0309` 的 guarded post-call 可產生 `DisplayRequest`。
- `DisplayRequest` 已只含 generation、event key、text key、translation，不含答案、輸入或原版
  狀態寫入。現有 `Observation` 的 begin／clear 缺 generation，不能當 presentation API。
- 這是一條 adapter metadata 能力；不改原版規則、畫面、VRAM、BIOS／DOS 輸入、存檔、host UI
  或手冊字型，亦不替 presenter 建立任何 RGBA stamp。

## 範圍

- 固定目前 dosgolem branch／revision，檢閱 watcher、collector、既有 request watcher 的事件 API
  與測試，建立帶分級與失敗即關閉行為的 READY 規格。
- 在 `apps/buckrogers` 建立 answer-free lifecycle event 型別與 defensive-copy queue；精確 begin、
  clear、catalog-hit request 才可發射。事件不得攜帶英文原文、答案、DOS 狀態或 renderer 參照。
- 對 begin→pending-clear→request、visible-clear、catalog miss、guard drop／nested frame 與 caller
  異常加上單元測試；重跑至少一條正常玩家 metadata 收據，確認輸出仍不注入輸入。

## 不在本階段

- 不建立 14 行 presenter、GOLEMFNT、RGBA 圖片、host 面板或 2×／3× runtime switch。
- 不把 lifecycle queue 接到 oracle、機器記憶體寫入、BIOS key queue、DOS mouse 或存檔。
- 不將未校訂、`strong-inference` 或 `unknown` 手冊內容加入 catalog。

## 完成條件

1. READY 規格明示 event schema、狀態轉移、generation、queue 可見性、失敗即關閉與原版輸入邊界。
2. dosgolem 實作與測試證實 queue 只在已證實 watcher 分支產生，且回傳值不可反向修改內部 state。
3. 正常玩家重播的 request metadata 與既有收據一致，原版輸入與 framebuffer 不受影響。
4. 無原版或手冊素材進入 Git；本專案文件、main 推送與相關 GitHub Issue 回寫完成。

## 完成結果

- dosgolem 本機 branch `buck-rogers-cht-output-overlay` 已以 commit
  `47397ebd18e63a0daa4cb54bd593c5fbfd549ada` 實作並 CONFORM 規格 216；分支沒有推送。
- lifecycle queue 只在 exact begin、active-context clear 與 exact catalog-hit request 發射，並以
  value-copy 回傳；pending clear、visible clear、catalog miss、guard／nested failure 與回傳值回寫
  均有測試。
- 正常玩家 state 重播的既有 request 未變，新增 metadata 順序為 begin→clear→request，三筆均為
  generation 1；沒有 injected input 或中文像素。
- 手冊 presenter、GOLEMFNT 與 2×／3× RGBA A/B 不在本階段，仍保持 DRAFT。

## 退出條件

- 若 begin／clear 的 generation 或 pending 語意無法由現有 collector／收據無歧義導出，維持 DRAFT，
  回到原版事件證據；不得以外部陣列輪詢猜測。
- 若 lifecycle API 需要 presentation renderer、host UI 或未證實的原版輸入語意才可成立，停止該
  分支並分離為新的 DRAFT，不擴張此階段。
