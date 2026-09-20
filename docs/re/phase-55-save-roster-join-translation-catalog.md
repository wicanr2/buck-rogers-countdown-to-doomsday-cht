# 第五十五階段：保存、名冊與加入隊伍繁中事件 catalog

## 結論

第五十四階段的 18-event 正常玩家路徑已完整轉成
`text/save-roster-join-events.tsv`。前 11 筆是既有功能選單 identity；後七筆中只有
`Add a character: ` 與 `Loading...Please Wait` 是靜態介面文字，正式譯為「加入角色：」與
「載入中……請稍候」。其餘四筆皆含角色姓名，必須維持原始 bytes，不得查詢翻譯 catalog。

## 動態姓名證據

| 原始 bytes | 長度 | SHA-256 | 分類 |
| --- | ---: | --- | --- |
| `A` 加 14 個空白 | 15 | `f7872bdce8d40b314454ee51a0bbe13fe4c4ccb5d19d6b1299ac7d1a9ddab60c` | 固定欄寬姓名 |
| `A` | 1 | `559aead08264d5795d3909718cdd05abd49572e84fe55590eef31a88a08fdffd` | 反白／正常姓名 |
| `* A` | 3 | `d60b849846dd57b81aeb8f3b6e545341c143750c10c36c6681532e25ad9edcfb` | 已加入標記與姓名 |

這三組 bytes 的 SHA-256 均由隔離 Docker 重算並對上正式收據；因此 15-byte 事件不是標題或
清除命令，3-byte 事件也不是靜態 `Add`。這項分類避免把單一 fixture 的姓名硬編成譯文。

## 靜態文字與 key

- 本路徑沿用既有 `menu.create_new_character`；另外五個功能選單 key 與兩個名冊 key 收在
  `text/save-roster-join.zh-TW.tsv`。
- `roster.add_prompt` 對應兩個 caller／幾何相同、時間不同的事件 identity；清冊仍保留兩筆，
  只共用譯文 key。
- `roster.loading` 保留不同 caller `0763:1307`，不得只用原文雜湊放寬比對。

## 驗證

`tools/save_roster_join_catalog.py` 以 canonical 清冊 SHA-256 鎖住第五十四階段 exact identity，
再驗證 18 筆順序、caller、長度／雜湊、座標／色號、角色分類、漏譯與孤兒 key。動態姓名若
出現任何 `translation_key` 即失敗。共用 catalog lint 另拒絕 BOM、非 UTF-8、非 NFC、控制碼、
重複 key 與非法來源。

2026-09-21 於 `python:3.13-alpine`、`--network none` 執行：97 項專案測試全部通過；新增 catalog
導出 37 個唯一字元供後續 GOLEMFNT 字型輸入。此階段沒有接 renderer，也沒有選定 2×／3×。

