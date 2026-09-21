# 第七十五階段：技能配置底部操作列執行期事件

日期：2026-09-21  
狀態：完成

## 結論

dosgolem 已能在不改原版畫面、輸入或技能狀態的前提下，將職業與技術技能頁
底部的逐字 glyph 呼叫收旂為 content-safe `ActionBarEvent`。事件只含畫面、key、
normal／focus variant、長度、SHA-256、字格與安全矩形；不含原文 bytes。

dosgolem spec 213 已依 RE → DRAFT → READY → implementation → same-state verification
升為 CONFORMED。本階段沒有譯文 request 或 overlay，所以不宣稱操作列已中文化。

## 實作契約

- screen anchor 只由 exact catalog request 建立：
  `career.screen.remaining_points.heading` 或 `technical.screen.general_points.heading`。
- technical 畫面只額外保留 Phase 72 已證實的兩個 career 共享標題 key；不使用
  模糊前綴擴張。其他 exact request 會撤銷錨定。
- `026F:029C` 清除只丟棄未完成 candidate，不只因同畫面的 row 24 重畫而
  誤判離開技能頁。
- 每個 `0763:026B` 字元都要通過 caller、SS 與 `SP+0x12` far-return guard；
  `mode=1`、`repeat=1`、row、column、色彩與逐字 caller 全部 exact match 才收集。
- 完整候選的 SHA-256 必須命中 `text/skill-action-bar-events.tsv`。disabled variant
  仍為 `unknown`，沒有被一般 normal variant 取代。

## 實作中訂正

1. 首條 career 收據顯示技能頁內的局部 clear 會在標題後發生，所以「任一 clear
   撤銷 screen anchor」過度寬鬆。
2. 第二次證實 row 24 本身也會在同畫面重畫前清除，因此最終將 screen anchor
   與 candidate 生命週期分開。
3. 回讀 Phase 74 原始 JSON 訂正 mode 低位為 1，不是初始規格中的 0。
4. technical 收據重現兩個 career 共享標題。這是 Phase 72 既有證據，最終以兩個
   exact allowlist key 保留 technical anchor。

每次缺口都先回到 DRAFT，修正 spec 與負向測試後才再重跑；沒有以放寬雜湊、
caller、座標或色彩來讓收據通過。

## 正常路徑收據

| 路徑 | action events | watcher JSON SHA-256 | terminal framebuffer SHA-256 |
|---|---:|---|---|
| career base | 3 | `c6cc0742411a8d1dda981bbc3e81697659888558622504757a1372ed8210fa1c` | `a1cd728cecaa720357f680f2be66e857f401ee5b0113f9959b23143e0fae95f7` |
| career Subtract | 6 | `c55056d5bb810d3025b7f94fdadaa4bacd3d8ad348bf99aa29a583971be3bca2` | `5dc661e499e1b37fbcadf5241e162b8747ebf9b0899d2dc3d8ff531e3153c195` |
| career Done | 9 | `3266c5f5c36c36939a1209904153263b7f58fae84738d585672bc59db86ff00a` | `2522860657a6d8237ad832e109188627243aa9e23dd5f2b12a58ee6411e85c65` |
| technical base | 8 | `07c056f2907ce851f3abc0cdffb6f4fdbf90b218eee5b982bc5b37094349488e` | `6bf7f9bb55720d24d2193bd1bffcc4abedd7278eb291db4d37398888c183432a` |
| technical Subtract | 13 | `8788c18fb3a43683e31e9f0751febbaaf634e541a7a20949625bbdecf52c28f5` | `32d71c8d84bc4c711421eb5cfff0e6bfd086233db8bd9516b4d4152e962ed057` |
| technical Prev | 18 | `dbec43a2f1b0983ab39bc558db0df62fddc5fc09197381707855d584349c9e00` | `e1473c16c051f0fce10f9445d4ba30a9687879e669d342fb08933b19067e6b0a` |
| technical Next | 23 | `c5fd8a9247af9d6da5b85970e832b3f069ef408d5597afc937f67c863fb945ee` | `fbaf03ae5107ee1eb2cdf1cd8f9037a0c2834bc0add0a29baf8bb724edfac7ed` |
| technical Done | 28 | `9afb5ccb43b0399efc3a0e3057662bcdcdeb23da3424c55ae85be9824d5e6c1f` | `f03c2a01e63b1dcce410c80f8f6a333f72257f615a5fa1773b3ec90c1f4c9958` |

每條 watcher 都重跑 A/B，JSON 逐 byte 一致；watcher A/B/control framebuffer 也逐 byte
一致。移除 `action_bar_*` metadata 後，watcher 與 control 其餘 JSON 完全相同。八路
皆為 0 miss、0 drop。正式 verifier 是 `tools/skill_action_bar_runtime_receipt.py`，本機原始收據
位於被忽略的 `workplace/phase75/`。

## 回歸

- 專案 Python：142 項通過。
- dosgolem：全部正式套件 test 與 vet 通過。
- 本階段相關 `apps/buckrogers` 與 `cmd/buckrogers-text-receipt` race detector 通過。
