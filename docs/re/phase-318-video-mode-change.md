# 第三百一十八階段：視訊模式設定時覆繪層整層失效（規格 052，Issue #22）

日期：2026-10-02
狀態：規格 052 READY 並實作驗收；dosgolem `fd63193`（實作）、`c5f92c8`（測試補齊）。發行包尚未重發。
推論等級：**已證實**＝重跑並比對輸出；**未知**＝未量。
原版素材、畫格只在 ignored 的 `workplace/phase318/`；本文只記雜湊、計數與判定。

## 1. 輸入（已證實）

| 項目 | 值 |
|---|---|
| A（實作的父 commit） | dosgolem `c695eb4`（含規格 053），乾淨匯出；runner `85cc80973d1a6fb7…`、`buckrogers-play` `d4b644f851f44cb5…`、`buckrogers-session` `d1b5eb851b63cb71…`（前 16 碼） |
| B（實作 commit） | dosgolem `fd63193`，乾淨匯出；runner `b3dce7172317b8f0…`、`buckrogers-play` `82950da6180759c9…`、`buckrogers-session` `bc2f9d4d66e1414c…` |
| P（探針） | B 的 scratch 複本，只在 `VideoModeChange` 開頭印 `MODEEVENT`（模式、步數、各 lane 的 active 家族）；不入版控 |

建置腳本 `workplace/phase318/build-ab.sh`、`build-extra.sh`（Docker、`--network none`、`GOPROXY=off`）。

## 2. 單元與套件測試（已證實）

- 通用層：`internal/machine/mode_observer_test.go`（預設不通知、`ObserveModeChanges` 每次模式設定恰一次且 callback 時模式已更新、`ModeChanges` 照舊追加、nil 關閉、不進機器狀態）；
  `internal/dos/bios_mode_observer_test.go`（`int 10h AH=00` 與 `AX=0093h` 各恰一次）；`session/observer_test.go` 三項（合成 COM 事件一次且不改 `machineDigest`、callback panic 停在該步之後、一般 observer 不受影響）。
- Buck 層 `live_mode_change_test.go` 10 項：body icon 重置後 generation 仍遞增且下一個畫面被接受、action bar 重置後無錨點時 Apply 被拒、手冊三種起始狀態（Visible → 一筆 Clear 且真正的清除不再送、Pending → poisoned、閒置 → 不動）、
  post-join 三種分支（閒置不重建、進行中重建不計數、failed 不動）、post-join 跨事件 return 與 failed 後下一個 entry 仍 fail closed、exit prompt Q1 顯示中發事件後 Q2 entry 在每個倍率各 fail 一次（`resets["exit-prompt"] == 2`）、
  空 runtime 發事件後 `DebugSummary`、`Resets()`、合成結果不變且 `ActiveFamilies` 為空、九個 story 家族在空狀態下 watcher 位元組不變、`liveLane` 與 `LiveRuntime` 欄位反射分類。
- 乾淨匯出（B，不含未入版控檔）設 `BUCKROGERS_CHT_ROOT` 與 `BUCK_OWNER_PROJECT`：`go vet` 通過；`apps/buckrogers` 412 項 PASS、0 FAIL、19 SKIP（`TestPackagedLanes` 因缺 `BUCKROGERS_PKG_ROOT` 而 SKIP，由 `package.sh` 執行）；`internal/machine`、`internal/dos`、`session`、`presentation`、`xlate`、`host` 全過。

## 3. 迴歸：既有 state 起跑的重播（已證實，**不證明** mode 13h 路徑）

`workplace/phase318/p254.sh`：phase254 七條（story、opening、manual、post、skill、action、body）A、B 各跑，共 52 個時點（2×、3×）：
52 個 live RGBA 逐位元組相同；52 份收據的 `memory_sha256`、`indexed_sha256`、`palette_sha256`、停止步數相同。這些重播從 state 起跑，不經 `SetVideoMode`，所以只證明新碼在沒有模式事件時不改行為。

## 4. 注入：`-inject-mode-event`（已證實）

text-receipt 新增僅供測試的 `-inject-mode-event MODE`：主迴圈在 `-until` 正常結束後、輸出之前對 LiveRuntime 呼叫一次 `VideoModeChange`（不呼叫 `SetVideoMode`，機器狀態不變），並把注入前合成、原版放大畫面的 SHA-256 與注入前 active 家族清單寫進收據。
同一 state、同 `-until`、`-lang zh-TW`，對照組（不注入）與注入組：

| 檢查 | phase254 七條（52 點） | 補點：ECL、hmenu、logbook、劇情第 2 至 9 頁（22 點，`extra.sh`） |
|---|---|---|
| 對照組與注入組的 `memory_sha256`、`cpu_sha256`、`indexed_sha256`、`palette_sha256`、停止步數 | 全相同 | 全相同 |
| 注入後 live RGBA 等於原版放大畫面 | 52／52 | 22／22 |
| 注入前合成（不等於原版）且 active 家族非空（非真空） | 42 點 | 22 點 |
| 注入前合成等於對照組的 live 輸出 | 52／52 | 22／22 |

沒有 active 家族的 10 個點（手冊題出現前後兩個時點、劇情首屏前後三個時點，各 2×、3×）不計入非真空；非真空的 64 個點涵蓋的家族：action-bar、body-icon、ecl-text、engine-dispatch、exit-prompt、hmenu、logbook、manual、menu、post-join、skill-exit、story-opening、story-page2 至 story-page9。
未涵蓋：手冊英文列（衍生面板，隨手冊 Clear 自動丟掉，只有單元測試涵蓋手冊三種起始狀態）。

## 5. 冷啟動（已證實）

| 驅動 | 事件序列（探針 P） | A、B、P 比對 |
|---|---|---|
| `buckrogers-session`（zh-TW，預設時脈，12 回合 × 1,000,000 步） | 恰一次：模式 13h（19），步數 7,520,426，zh-TW 的 active 家族為空 | 全部 JSON 行逐位元組相同；最後一格 RGBA 相同（`ee5b3741ab75bc1a…`）；stderr 相同 |
| `buckrogers-play`（四 lane，zh-TW 2×，`path-repair.txt`，5,700 格，預設 `-clock 50`） | 恰一次：模式 13h，步數 7,438,070（與 session 不同：`-clock 50` 的時脈調整），四條 lane 的 active 家族皆為空 | `memory_sha256`（`fe5f8f9f…`）、`cpu_sha256`（`75e8fe4f…`）與規格 051／053 實機重播相同；570 張畫格逐位元組相同；`resets` 欄相同 |

「冷啟動時所有家族皆空」由強推論轉為已證實（探針在事件當下記錄）。

## 6. 邊界與未知

- 有輸入路徑（含離開 DOS）的模式事件序列未量（`path-repair.txt` 在離開之前結束）：**未知**。事件落在 glyph、dispatcher 或 ECL 呼叫進行中的行為由單元測試的 straddle 與 fail-closed 計數涵蓋，沒有實機樣本。
- text-receipt 內的 legacy 家族（收據證明線）本輪沒接模式事件。
- `state.Load`／`Snapshot.Restore` 的顯示不連續不在本規格範圍（`LiveRuntime` 沒有 restore 入口）。
- 平面模式（Buck 不用）的 320×200 畫面尺寸假設與 menu recorder 跨事件補畫的後果見規格 052 §6。
- 既有計數：play 路徑的 `resets` 本來就有 `post-join:70 skill-exit:32`（A、B 相同），不是本規格造成。

## 7. 已改與未做

- 已改：dosgolem（`internal/machine`、`session`、`apps/buckrogers`：`live_mode_change.go`、`live_story.go`、`cmd/*`）；Buck 規格 052 READY 並標記驗收範圍；規格 026 契約第 5 條加 pointer。
- 未做：發行包尚未重發。
