# 032 — 通用家族的 overlay 程式位址改用 unit 相對定址

狀態：**CONFORMED**（2026-09-26：兩輪獨立審查後 READY；§5 驗收見 phase-265）
日期：2026-09-26
前置：規格 028（水平選單）、029（引擎訊息）、phase-263、
[phase-264](../re/phase-264-overlay-units-and-text-glyphs.md)。

## 1. 問題

規格 028 的選單印字程序 `37F1:0243`、規格 029 的呼叫端白名單（`1FEB:051D`、`2A65:2163`
等）都寫成絕對段位址。這些程式碼在 `GAME.OVR` 的 Turbo Pascal overlay unit 裡，
每次載入的段位址會變。太空港一段遊玩的追蹤中，同一個偏移出現在多個段：

| 偏移 | 出現的段（次數） |
|---|---|
| `235A` | 2099、20D1、216E、2A65、2AA5、2AF2、2C17、2CB0、2DEA、31B4、332F… |
| `051D` | 1C41、1FEB、25A6、26BB、29DF、2B5A、2CB8、2F78、326F |
| `0815` | 1F90、2158、2D14、2D97、312B |

Salvation III 的收據中水平選單 Hits 為 0，戰鬥後大量引擎訊息未命中，原因即在此。

## 2. 原版證據

- 詳見 phase-264 §1–2。overlay stub 表頭（Turbo Pascal overlay 管理器格式，強推論）：
  段首 `CD 3F`；偏移 2 SaveReturn、4 FileOfs（dword）、8 CodeSize、0x0A FixupSize、
  0x0C EntryPts、0x0E CodeListNext、**0x10 LoadSeg**、0x12 Reprieved、0x14 LoadListNext。
  LoadSeg 為 0 表示未載入。
- stub 段固定在 EXE 映像內（六個狀態的 stub 段相同，已證實）。
- 目前用到的 unit（以 LoadSeg 與追蹤中的段相符判定，兩個以上狀態一致，已證實）：

| FileOfs | stub 段 | CodeSize | 曾記錄的段 | 用到的偏移 |
|---|---|---|---|---|
| `2BA60` | `021F` | `24F1` | 37F1、2A65 | 0243（選單）、235A、2163、2184 |
| `27BBE` | `0206` | `37CE` | 1FEB | 051D、0560、0A58 |
| `081D9` | `016E` | `22BD` | 1F90 | 0815、086C、088D、08DF |
| `0D80A` | `0183` | `2617` | 2C2B | 24BD |
| `114F6` | `019F` | `495A` | 265F | 062D |

## 3. 契約

### 3.1 位址表示

- 程式位址寫成兩種：主程式段 `SSSS:OOOO`（如 `0763:0424`，不變），
  overlay unit `OVR:FFFFF:OOOO`（FileOfs 五位十六進位、段內偏移）。
- `text/engine-dispatch-callers.tsv`、`text/engine-dispatch-name-callers.tsv` 中屬於
  §2 表列 unit 的呼叫端改寫成 overlay 形式；水平選單印字程序改為 `OVR:2BA60:0243`。

### 3.2 執行期解析

- 第一次需要時掃描段 0–0x3FFF（線性 0–0x3FFFF）的段首，符合下列全部條件才視為 stub 表頭
  （依據：phase-264 §2 的記憶體傾印中，跳躍表項也以 `CD 3F` 開頭、每項 5 位元組，連續
  排列；表頭之後不接另一組 `CD 3F`。已知表頭的 CodeSize 最小 0xC0。這些篩選是依觀察
  訂的，強推論）：
  1. 位移 0–1 為 `CD 3F`；
  2. 位移 4 不是 `CD`，且位移 5–6 不是 `CD 3F`（排除跳躍表項）；
  3. CodeSize（位移 8）大於 0x40；
  4. FileOfs 非零且小於 `GAME.OVR` 長度 0x33497。
- 每次解析前確認每個已知 stub 仍符合上列條件且 FileOfs 未變，否則重新掃描。
- 一個執行期位址 `CS:IP`：若恰有一個 stub 的目前 LoadSeg 等於 CS，其身分為
  `OVR:FileOfs:IP`；沒有則為 `CS:IP`；**兩個以上 stub 同時回報該段**時不解析
  （退回 `CS:IP`，即該家族不命中），並記入診斷計數。不依掃描順序挑一個。
  依據：傾印中未載入的 unit LoadSeg 都是 0，同一時刻各已載入 unit 的段互不相同
  （六個狀態，已證實）；Turbo Pascal overlay 管理器卸載時是否一定歸零未單獨驗證，
  所以保留這道防護。
- LoadSeg 每次解析時即時讀取。解析只在候選位址出現時做：水平選單先比對 IP 是否為
  0x0243，相符才解析 CS；dispatcher 只在 `0763:0424` 進入時解析呼叫端。不在每一步執行。
- 解析只讀 DOS 記憶體，不寫入。

### 3.3 受影響的介面

- `hmenu.go` 的印字程序常數由 `Address` 改為 `CodeKey{Unit, Offset}`。
- `engine_dispatch.go`：白名單與只翻怪物名清單由 `map[Address]bool` 改為
  `map[CodeKey]bool`；`ObserveEntry` 的呼叫端參數改為 `CodeKey`（返回位址仍用執行期
  `Address` 比對）；`OwnedCallers` 回傳 `CodeKey`。
- `live_runtime.go` 持有一個解析器，於上述兩處呼叫。
- 兩個呼叫端清單 TSV 改用 §3.1 的寫法。

### 3.4 範圍

- 只改規格 027–030 的通用家族。舊有專屬家族（技能離開、加入後選單等）使用的
  `37F1:101E` 等位址維持原樣，其收據不變。
- 「既有家族擁有的呼叫端」檢查：舊家族 events 檔的位址是在角色建立期量得，那時的載入段
  已量到（phase-264 §2，三個 checkpoint 一致）：37F1→`2BA60`、2368→`21832`、
  2684→`24CDF`、1C41→`1799A`、1FEB→`27BBE`、2807→`081D9`、2E13→`00904`、2A33→`07DA5`。
  表內收錄 phase-264 量到的全部筆數，也涵蓋舊家族程式常數用到的段（手冊家族的
  `2A33:01ED`；修訂 2026-09-26，漏收時規格 033 會把它正規化成不可匹配）。
  比對時把舊家族的這些段換算成 unit 形式，
  與通用家族的 `OVR:` 位址比對；其他段照字面比對。
- 這張換算表是封閉的：新增專屬家族、或在其他時間點記錄 overlay 位址前，要先量該時刻的
  載入段並補進表內，否則所有權檢查會漏判。

## 4. 不做什麼

- 不改 overlay 管理器、不強制載入 unit、不改遊戲狀態。

## 5. 驗收

1. 單元測試：表頭掃描（合成記憶體，含跳躍表項排除）、LoadSeg 對應、unit 換段後以新段命中、
   舊段不再命中、未載入時退回 `CS:IP`、兩個 stub 同段時不解析並計數、stub 失效時重掃、
   `OVR:` 解析與錯誤格式、所有權檢查的雙形式比對。
2. Salvation III（`lb1.state` 接續）的選單有水平選單命中；太空港戰鬥後（q13 前後）
   的戰鬥勝利、經驗值訊息有引擎訊息命中。
3. 戰鬥 A/B（`abc.sh`）與七條既有回歸路徑與上一輪相同。
