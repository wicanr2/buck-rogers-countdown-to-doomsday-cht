# 第二百八十一階段：隊伍角色記錄、名單指標鏈與性別欄位

日期：2026-09-29
用途：規格 038（玩家角色名判定與顯示）的原版證據。狀態檔、傾印、截圖與角色檔只在 ignored
`workplace/phase281-party-records/`。原版樹 `workplace/play-e2e/orig`（`GAME.OVR` SHA-256 前綴 `3a4ad4856c08fe59`），唯讀。

## 方法

- 以 dosgolem `LoadStateFile` 傾印 4,303 個既有狀態（`checkpoints/` 25、`phase258-ecl-ab/` 26、
  `phase257-text-window-trace/cp/` 4,252，含戰鬥中），並新做 4 個狀態：移除 CELESTE（`rm1`）、再移除 NICOLE STEELE（`rm2`）、
  移除排頭 FLAVIUS（`rmf`）、`rm1` 後加回 CELESTE（`add1`）。全部在 Docker、`--network none`。

## 1. 角色記錄（0x103 = 259 位元組；與 `CHRDATB?.sav`、`*.WHO` 除 0xEB–0x102 舊指標外逐位元組相同）

| 偏移 | 內容 | 等級 |
|---|---|---|
| +0x00 | 名字：長度 1 位元組＋最多 15 字元，欄寬 0x10，大寫 ASCII，不足補 00 | 已證實 |
| +0x26 | 性別：00 MALE、01 FEMALE | 已證實（因果實驗） |
| +0x4C | 00 我方、01 怪物 | 強推論（戰鬥傾印 6 名隊員全 0、11 隻怪物全 1） |
| +0xB9 | 隊員 0–5、怪物 8–10 | 假說 |
| +0xFF | far pointer（off, seg）指向下一筆；末筆 0000:0000 | 已證實（4,303 個傾印全可走通） |
| +0xEB、+0xEF、+0xF7 | far pointer 指向物品記錄 | 假說 |

怪物使用同一結構，戰鬥中串在同一條鏈的隊員之後。

## 2. 性別因果實驗（已證實）

`phase258-ecl-ab/gba3.state`（704.9M，讀 B 槽後的隊伍選單），按 `Up×4, Enter, Enter` 進入 FLAVIUS 的角色頁。
對照組顯示 MALE；在第 704,900,001 步 `-poke` 該記錄 +0x26 為 01 後顯示 FEMALE，其他欄位不變。
六人 +0x26：FLAVIUS 0、CELESTE 1、PIERRE 0、NICOLE STEELE 1、ROARKE 0、JANELLE 1。

## 3. 名單指標鏈

DGROUP 在 dosgolem 固定載入位置為 0EC0（強推論：只在此載入位置成立；覆繪程式應在 hook 當下讀 DS）。

| 位置 | 內容 | 等級 |
|---|---|---|
| `DS:4EC5` | far pointer，指向排頭記錄 | 已證實 |
| `DS:4EC1` | 目前選取或迭代中的角色（戰鬥中也會指到怪物） | 強推論 |
| `DS:3BCC` | far pointer，4,303 個傾印都是 `3A81:0000` | 值已證實，用途未知 |
| `[DS:3BCC]+0x33E` | 我方隊員數（byte） | 已證實 |
| `DS:6749` 起 | far pointer 陣列，隊員在前、怪物在後 | 強推論 |
| `DS:3878`、`387C`、`3BB8`、`3BBE` | 通常指向 FLAVIUS，但移除排頭後不更新，不是排頭 | 已證實（反例 `rmf`） |

- 讀名單：從 `DS:4EC5` 出發沿 +0xFF 走「隊員數」筆。戰鬥中鏈長 8–17 筆而隊員數仍為 6。
- 角色建立期間排頭為空、隊員數 0，正在建立的角色只掛在 `DS:4EC1`。
- 寫入點（已證實，`-watch`／`-regs-at`）在 overlay unit `1799A`（本次段 1C41，段值會變，見 phase-264）：
  段內 `1D07` 為 `C4 3E CC 3B 26 FE 8D 3E 03`（`les di,[3BCC]`＋`dec byte es:[di+033E]`，#713,018,987 時隊員數 6→5）；
  `1D65` 同樣式，推測為加入（未觀測）；`1D35`、`1D39` 移除排頭時改寫 `DS:4EC5`；`010D`、`1D5B` 先清 `DS:4EC1` 再指向新排頭。

## 4. 位址穩定性

- 記錄在 heap，位址隨路徑改變（已證實）：同一個 FLAVIUS 在兩條路徑都在 57472，其後各筆位址不同。
- 同一段遊玩中不增減隊員時記錄不搬動（已證實：遺棄艦入口、交誼廳、多場戰鬥位址相同）。

## 5. 名單何時改變（已證實，隊伍選單操作）

| 操作 | 結果 |
|---|---|
| 移除 CELESTE | 鏈上移除，隊員數 6→5，寫出 `CELESTE.WHO`／`.STF` |
| 再移除 NICOLE STEELE | 隊員數 5→4 |
| 移除排頭 FLAVIUS | `DS:4EC5` 改指 CELESTE；舊空間被重用 |
| 加回 CELESTE | 從 `SAVE\CELESTE.WHO` 讀 259 位元組接在鏈尾，隊員數回 6，畫面順序 CELESTE 最後 |
| 讀 B 槽存檔 | 整條鏈重建 |

未知：劇情 NPC 入隊或離隊是否走同一段程式；角色死亡或逃跑是否改變鏈或隊員數；兩條路徑 heap 位址差異的原因；
新建角色何時串進鏈。

## 6. 名冊與目前隊伍

| 項目 | 位置 | 等級 |
|---|---|---|
| 名冊 | 磁碟 `SAVE\<名>.WHO`（259 位元組）＋`.STF`；ADD 清單逐檔讀前 16 位元組當名字 | 已證實 |
| 名冊是否常駐記憶體 | 未見；ADD 清單每次從檔案讀 | 強推論 |
| 存檔槽 | `SAVGAM?.DAT`＋`CHRDAT?1–6.SAV／.STF`，依鏈順序 | 已證實 |
| 目前隊伍 | heap 中的鏈 | 已證實 |

遊戲內實際順序：FLAVIUS、CELESTE、PIERRE、NICOLE STEELE、ROARKE、JANELLE（鏈、`CHRDATB1–6`、畫面一致）。

## 7. 對規格 038 的含意

- 名字讀 +0x00、性別讀 +0x26，從 `DS:4EC5` 走隊員數筆；不依賴線性位址。
- 戰鬥訊息中的名字可能是怪物：只取鏈上前「隊員數」筆（或 +0x4C = 0）。
- 音譯快取以名字字串為鍵，不以位址為鍵。
