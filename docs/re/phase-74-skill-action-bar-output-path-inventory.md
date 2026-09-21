# 第七十四階段：技能配置底部操作列輸出路徑清冊

日期：2026-09-21  
狀態：完成

## 結論

職業技能與技術技能頁的底部操作列不是預烘圖，也不經過已有的高階長度前綴
dispatcher `0763:0424`。上層程式逐字以 far call 進入 `0763:026B`，後者再以
`0763:1809` 的 8×8 glyph renderer 寫入 Mode 13h framebuffer。因此下一階段應新增
「字元事件錨定器」，不得把此路徑伪裝成原有字串 dispatcher 事件。

## 原始定位與參數

- 輸入：從 `workplace/phase66/fixed-after-bios-space-100m.state` 正常玩家路徑重生。
- IDA 9.4 輸入是執行期 `0763:0000` 的 8 KiB 快照，SHA-256 為
  `436711fefc7071fcaf0811ef0b4243a5f2fd42840ca0f3b11aaaf121454deac6`。IDA database EA
  等於 runtime offset，本文位址一律寫為 dosgolem runtime `0763:offset`。
- `0763:026B` 參數：`[BP+06]` mode、`[BP+08]` glyph、`[BP+0A]` repeat、
  `[BP+0C]` background、`[BP+0E]` foreground、`[BP+10]` row、`[BP+12]` column。
- `0763:1809` 參數：glyph、background、foreground、row、column；`0763:184D`
  寫背景色，`0763:1854` 寫前景色。字型 far pointer 來自 `DS:5F32`。
- 所有底列字元的上層 runtime caller 皆在 segment `37F1`：焦點為 `0337`，
  一般標籤首字為 `0391`，其餘字為 `03CE`。此處只把 caller 當事件身分，
  不以推測名稱覆蓋原始位址。

## 幾何、色彩與生命週期

`text/skill-action-bar-events.tsv` 保存八個畫面配置、五個語意標籤的 content-safe
identity。全數位於 row 24，y 範圍 `[192,200)`；字格寬 8 px。

| 畫面 | 標籤 | column | 矩形 x | 已驗證焦點 |
|---|---|---:|---:|---|
| career | `action.add` | 0 | `[0,24)` | 初始 |
| career | `action.subtract` | 4 | `[32,96)` | Right 一次 |
| career | `action.done` | 13 | `[104,136)` | Right 兩次 |
| technical | `action.add` | 0 | `[0,24)` | 初始 |
| technical | `action.subtract` | 4 | `[32,96)` | Right 一次 |
| technical | `action.prev` | 13 | `[104,136)` | Right 兩次 |
| technical | `action.next` | 18 | `[144,176)` | Right 三次 |
| technical | `action.done` | 23 | `[184,216)` | Right 四次 |

一般狀態為黑底，快捷鍵首字前景 15、其餘字前景 10；焦點狀態為背景 15、
前景 0。Right 每移動一次都重畫完整操作列；職業頁 17 字元，技術頁 27 字元。
八條路徑均已有決定性本機收據。

## 證據分級與邊界

- 路徑、caller、字元順序、幾何、色彩及焦點移動為「已證實」。
- 初始與 Right 路徑未觀測到獨立的 disabled 畫法或 caller；是否存在不可用狀態保持
  `unknown`，不由色彩或操作語意推定。
- 清冊只保存長度與 SHA-256，不保存原作字串；未實作繁中覆繪，不宣稱已中文化。

## 收據

- IDA JSON：`workplace/phase74/phase74-ida-action-bar-v3.json`，SHA-256
  `ed762a88a45f2c722ac5cba61d296d4ee3304ebe15fa13fc8aef23fed4a465bd`。
- IDA database：`workplace/phase74/phase74-action-bar-v3.i64`，SHA-256
  `e27cd73ae86a208e8df6ad97318f9d67d77d6fdee7eee9239c3c3ed4b3d3aa6d`。
- 八條 JSON 收據的 SHA-256 記於本階段 `WORKLOG.md`項目；原始收據留在被忽略的
  `workplace/phase74/`。
- 驗證器：`tools/skill_action_bar_events.py`；它失敗即關閉地拒絕 schema、位址、
  幾何、色彩、雜湊、覆蓋與證據分級漂移。
