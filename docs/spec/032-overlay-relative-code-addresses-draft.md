# 032 — 通用家族的 overlay 程式位址改用 unit 相對定址

狀態：**DRAFT**
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

- 第一次需要時掃描 0–0x3FFFF 的段首，收集 `CD 3F` 開頭、CodeSize 非零、FileOfs 小於
  `GAME.OVR` 大小的表頭，記下 stub 段與 FileOfs。之後每次使用前確認該 stub 段仍以
  `CD 3F` 開頭，否則重新掃描。
- 一個執行期位址 `CS:IP`：若 CS 等於某個已知 stub 的目前 LoadSeg，其身分為
  `OVR:FileOfs:IP`；否則為 `CS:IP`。LoadSeg 每次即時讀取，不快取。
- 解析只讀 DOS 記憶體，不寫入。

### 3.3 範圍

- 只改規格 027–030 的通用家族。舊有專屬家族（技能離開、加入後選單等）使用的
  `37F1:101E` 等位址維持原樣，其收據不變。
- 「既有家族擁有的呼叫端」檢查：舊家族 events 檔的位址是在角色建立期量得，那時的載入段
  已量到（phase-264 §2，三個 checkpoint 一致）：37F1→`2BA60`、2368→`21832`、
  2684→`24CDF`、1C41→`1799A`、1FEB→`27BBE`。比對時把舊家族的這些段換算成 unit 形式，
  與通用家族的 `OVR:` 位址比對；其他段照字面比對。

## 4. 不做什麼

- 不改 overlay 管理器、不強制載入 unit、不改遊戲狀態。

## 5. 驗收

1. 單元測試：表頭掃描（合成記憶體）、LoadSeg 對應、未載入時退回 `CS:IP`、stub 失效時重掃、
   `OVR:` 解析與錯誤格式、所有權檢查的雙形式比對。
2. Salvation III（`lb1.state` 接續）的選單有水平選單命中；太空港戰鬥後（q13 前後）
   的戰鬥勝利、經驗值訊息有引擎訊息命中。
3. 戰鬥 A/B（`abc.sh`）與七條既有回歸路徑與上一輪相同。
