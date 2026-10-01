# 第三百一十三階段：繁簡中文字形來源（規格 050，Issue #36）

日期：2026-10-01
狀態：規格 050 READY 並實作驗收；`tools/package.sh`、`third_party.py`、`讀我.txt`、`font/README.md` 已改。發行包尚未重發（見 §6）。
推論等級：**已證實**＝重跑並比對輸出；**未知**＝未量。
來源 Unifont 17.0.05 只在 ignored 的 `workplace/unifont-src/`；本文只記數字、雜湊與判定。

## 1. 影響範圍（已證實）

`unifont_all-17.0.05.hex.gz` 的平面 0 排序是 `izmg16`（日文）先於 `wqy`（文泉驛），`sort -u` 取先者：兩者重疊的 9,666 個碼位
位圖全部不同，且一律取日文字形。發行字型 zh-TW 清單 2,402 個 CJK 字中 2,309 個、zh-CN 2,339 個中 1,634 個是日文來源。
審查另指出官方預編檔 `font/precompiled/unifont_t-17.0.05.hex`（預設加上 17.0.04 起的台灣來源 `t-source.hex`）；
`t-source` 與預設 `wqy` 對 zh-TW 清單有 2,384 字位圖不同，所以台灣標準字形與 `wqy` 也不相同。

## 2. 決定與實作（已證實）

| 語言 | 字形來源（官方 tarball `font/precompiled/`） | 解出檔 SHA-256 |
|---|---|---|
| zh-TW | `unifont_t-17.0.05.hex` | `169634258e4037b507beaafad5d72edc2e44b3faeaa856d9669e4657d1eee454` |
| zh-CN | `unifont-17.0.05.hex` | `fd79af3613ec1b984a98d33428fdd43fcf06018d18059960d78edeb63d958622` |
| ja、ko | `unifont_all-17.0.05.hex.gz`（不變） | 沿用 |

tarball SHA-256 `f287cffb26e22723aa36e6684869b0f3ff3bfb822c4b01008bd847911ec1b631`。不自製合併工具：審查實測預設檔與「以 `wqy` 取代 `izmg16`」的結果全等。
`tools/package.sh` 先核對 tarball 雜湊，解出兩個 `.hex`、核對各自雜湊，再建 zh-TW、zh-CN 字型；ja、ko 的建置不變。
授權與歸屬：`THIRD-PARTY.md` 與 `讀我.txt` 補上文泉驛點陣宋體（Qianqian Fang，經 Unifont 收錄授權）與 `izmg16`（公有領域）；
zh 字型在此之前就含 `wqy` 字形（zh-TW 93 字），這補上既有缺口。

## 3. 字型層收據（已證實）

| 檔 | 舊 | 新 |
|---|---|---|
| `buckrogers-unifont.golemfnt`（zh-TW） | `5a57d5eb10e00be755c4b780dca8c76b2b62aa224238f425a716c37f20885802` | `7675cf4e97986985cbeb4b5ed447a2a56d68f4c5bdaf29f6f650164179042697` |
| `buckrogers-zh-CN.golemfnt` | `70db5f48b535b4b4d202784941029b52865c5f7e3c08cbbb5da07a298c6faed3` | `2ac47096396778646b9309a59c71d7bba80cf64584d93a782d3b57162cbadd14` |
| `buckrogers-ja.golemfnt` | `ceae5544bcf5cebbffd92a7477f74ec30694cf1447ab143624cd8e9578b43450` | 相同 |
| `buckrogers-ko.golemfnt` | `a3b9a1f92b222ca2dbf5b746e8fe8b827536c68a227be12bd0906214dfedd342` | 相同 |

`package.sh linux` 產出的 zh-TW、zh-CN 字型與手動以同一來源重建的位元組相同（可重現）。
位圖差異（`workplace/phase312/fontdiff.py`，對字元清單）：

- zh-CN：只有 1,634 個取自 `izmg16` 的 CJK 字不同；字格寬度相同；非 CJK 字元相同。
- zh-TW：2,401／2,402 個 CJK 字不同（`unifont_t` 全面採台灣來源字形）；另有 11 個全形標點不同（、。，！「」『』《》…，台灣習慣的位置與字形）；
  `…`（U+2026）原本是 8 點寬字形，新字形 16 點寬，與版面的全形單位（`runeUnits`，只有 ASCII 與 `•` 算半形）一致；其餘字元（ASCII 等）相同。

## 4. 載入層與畫面層收據（已證實）

- 離線重播（`workplace/phase312/replay.sh`，字型換成新字型）：五份輸出與舊字型逐位元組相同。
- `apps/buckrogers` 套件測試（完整環境）：新舊字型的失敗集合相同，都是既有的四個（兩個 scoped menu 字型雜湊測試、兩個未入版控的探針測試）。
- 同一腳本跑到第 6,800 格（zh-TW，2×、3×，舊字型 2×、新字型 2× 與 3× 三次）：`memory_sha256`、`cpu_sha256` 三次相同
  （`471284560fc5865bc4745f5125c9260bf208301856413f11b6acc2a8e3d18780`），字型與倍率不影響遊戲狀態；ECL、水平選單等家族的命中、未命中、失效計數
  新舊字型相同（`ecl` 命中 9、未命中 30、失效 6；`hmenu` 命中 24、未命中 2、失效 10），沒有因墨跡框落到英文原版。
- 接觸表檢視：選單、隊伍表、港口、發射倒數、敘事（單行）在 2×、3× 字形正確、無缺字、無裁切。

## 5. 版面觀察（已證實，是這個決定的代價）

- 新字形佔滿 16 列（zh-TW 清單中 `unifont_t` 有 2,154 字、預設有 2,172 字在第 15 列有墨），舊的日文字形只有 84 字。16 點行距（2×）時上下行的筆畫會相接，
  功能選單這類一字一行的長清單看起來較擠；3×（行距 24 點，字格內 22 點）不受影響。
- 筆畫較舊字形細。標點位置符合台灣習慣（逗號、句號在左下），`……` 變成 16 點寬的置中省略號。
- 這是 Unifont 中文字形本身的設計，不在本規格內加行距；若使用者認為 2× 太擠，退回方案是讓 zh-TW 在 `package.sh` 改回 `unifont_all`（一行），或另開規格調整行距。

## 6. 已改與未做

- README 的 zh-TW、zh-CN 展示截圖（`lang-party-*`、`lang-narr-*`）依新字型重生（同一狀態、runner 以 dosgolem `eee5b77` 重建）；`03-station`、`08-logbook`、
  `11-opening-page1`、`12-battle` 是本機倚天字型，不受影響。
- 已發行的 v1.1.0 發行包與兩支影片仍是舊字形；下次發行才帶新字型（未重發，需要使用者決定時機）。
- 發行包圖示（`appicon.py` 用 zh-TW 字型畫「拯救地球」）隨字型改變，隨下次打包重生。
- 舊的覆繪快照：審查指出 `xlate/layer.go` 把字型 SHA 綁進快照，舊快照在新字型下無法還原（未另行實測）；本機若有含覆繪層的舊快照要重建，不含覆繪層的原版 state 不受影響。
- 角色資料頁（手冊頁、技能頁、戰鬥畫面）的 2×、3× 逐頁接觸表沒有逐一做；已量到的只有 §4 列的畫面（未知：其餘畫面的視覺間距）。
