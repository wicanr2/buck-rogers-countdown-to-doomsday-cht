# 第三百一十二階段：zh-TW 譯文修正（Issue #37）

日期：2026-10-01
狀態：修正已入版並驗證；dosgolem `eee5b77`（釘住的雜湊）。
推論等級：**已證實**＝重跑並比對輸出；**強推論**＝由程式或相鄰紀錄推得、未實跑；**未知**＝未量。
英文原文不寫進本文，以事件檔的 SHA-256 前綴定位。

## 1. 修正（已證實）

| key | 事件檔前綴 | 舊 | 新 | 依據 |
|---|---|---|---|---|
| `post_join_menu.join_a_game` | `2e98e6fc27b2` | 加入遊戲 | 圖示選擇 | 原文是「圖示選擇」義；ja、ko 早已依英文譯成對應義 |
| `post_join_menu.show_characters_game` | `b0b21f129832` | 顯示角色所屬遊戲 | 儲存目前遊戲 | 原文是「儲存目前遊戲」義，同上 |
| `character.sheet.mount` | `94ffe249e94e` | 坐騎 | 移動力 | 原文是 movement 的縮寫；ja、ko 為「移動力」「이동력」；安全矩形容量 7 格，三個漢字 6 格 |
| `frag.5a6919a210c7` | `5a6919a210c7` | 護甲等級 生命值（15 單位） | 防禦 生命（9 單位） | 原版欄名片段 5 字元、上限 10 單位；舊譯超過上限，引擎片段通道退回英文。離線重播 zh-TW、zh-CN 各 95 次的寬度閘門由 fail 變 pass |
| `story.page7.line.002` | `286012ec11f1` | 打撈站，並接受打撈 | 救世站，並接受打撈 | 原版同狀態畫面（phase-129 的第七頁六行影像）第二行開頭是站名專有名詞，即詞表的「救世站」，後面才是「打撈」；舊譯把站名誤當成打撈。ja、ko 都譯成站名的音譯 |
| `ecl.4.66.08710` | `f98d4680ba3b` | 巡邏至第 | 巡邏樓層： | 見下 |
| `ecl.4.66.08952` | `d751f89362f6` | 入侵者位於第 | 入侵者所在樓層： | 見下 |

最後兩列：這兩個呼叫的下一次畫字是引擎另外畫出的數字，後面沒有可以補「層」的呼叫（相鄰的 `ecl.4.66.08759`、`08797`、`08893`、
`08906` 是別的句子），所以以「第」結尾會畫成沒頭沒尾的「第 3」。改成與同一組的 `ecl.4.66.02870`（所在樓層：）相同的標籤式。
簡體由 `tools/zh_cn_convert.py` 重新產生（`圖示選擇→图标选择`、`儲存目前遊戲→保存目前游戏` 兩處新的 OpenCC 詞組套用，
已加入 `text/zh-CN-term-review.tsv`，verdict 為 ok）。

ja 的 `ecl.4.66.01705`、`02870`（以「第」結尾）經核對**不需修改**：下一次呼叫 `ecl.4.66.01730` 以「小隊」起首、`02889` 以「層」起首，
句子完整。Issue #35 開放項目中的這四個 key 因此是：zh-TW 兩個已修，ja 兩個確認無誤。

## 2. 決定（規則）

- 手札（logbook）的 zh-TW 以**中文印刷本為準**（使用者 2026-10-01）。zh-TW 手札與英文的差異不當作缺陷，不為了對齊英文而改；
  ja、ko 手札本來就以英文為源，兩者與 zh-TW 不同是設計。後續比對 zh-TW 與英文時，手札家族不列入「不符」清單。

## 3. 檢查與收據（已證實）

- 目錄檢查：`tools/menu_events.py`（post-join menu）、`tools/character_sheet_events.py`、`tools/story_page7_catalog.py` 通過；
  `catalog_font.py chars` 重生 `font/characters.txt` 與版控相同（所有新字都在字元清單內，字型不需重建）。
- `tools/zh_cn_check.sh`、`tools/ja_check.sh`、`tools/ko_check.sh` 全部通過（ja、ko 的 `source` 欄與 zh-TW 對齊）。
- dosgolem：`post-join-menu.zh-TW.tsv` 的雜湊是釘住的 READY fixture，改譯文必須同步改 `postJoinTextSHA`（`eee5b77`）；
  改前離線重播直接報「SHA-256 不符」。
- 離線重播（`workplace/phase312/replay.sh`，dosgolem `0bc270a` 加釘住雜湊修正）對 phase-309 的基準 `post309-1`：
  `replay-ecl.tsv`、`replay-pages.tsv`、`replay-report.tsv`、`baseline-translate.tsv` 逐位元組相同；`replay-engine.tsv` 只有
  `AC HP` 那一列的 zh-TW、zh-CN 各 95 次變動，沒有其他列變動。`ecl.4.66.08710`、`08952` 兩個 key 在重播軌跡中沒有呼叫，所以重播量不到它們。
- 套件測試 `apps/buckrogers`（完整環境）：沒有新的失敗；仍失敗的是 phase-305 §8 記錄過的兩個 scoped menu 字型雜湊測試，
  以及兩個尚未入版控的探針測試（缺原版檔、字型雜湊漂移）。
- 實機畫面：以修正後的資料與重建的 `buckrogers-play` 跑 zh-TW 冷開機到第 3,050 格（3 倍、Unifont，每 10 格輸出）：
  選單第 4 項顯示「圖示選擇」、第 9 項顯示「儲存目前遊戲」，隊伍表頭顯示「防禦 生命」（修正前是原版的 `AC HP`）。

## 4. 未做

- `character.sheet.mount` 的角色資料頁沒有另外截圖，只驗證目錄載入與格數（未知：實際畫面的對齊）。
- `ecl.4.66.08710`、`08952` 沒有執行期收據（未知）。
