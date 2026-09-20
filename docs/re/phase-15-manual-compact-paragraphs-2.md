# 第十五階段：第二批短篇繁中手冊段落校訂

## 結論

第二批八筆來源已證實的單段內容完成原圖校訂，手冊事件與繁中 catalog 由 9 筆增至 17 筆。
新資料同樣只包含原版題目識別與中文顯示文字，不包含答案、自動按鍵或原版記憶體改寫。

## 原圖校訂收據

半頁裁切只留在 `workplace/manual-crops/phase15/`；原始掃描雜湊由來源對照表保存。

| 題目 | 中文錨點 | 裁切 SHA-256 |
| --- | --- | --- |
| `Damage` | C. 傷害 | `f67f64514000bae592ee5fce94564296b78079158bbb915298631b18a7b090fb` |
| `Terrine` | TERRINE（殺手） | `66bd874b457d7cd1d20b30ccf79115ea738aa28b593422dded6c0542ca6e74c2` |
| `Scot's Alarm` | 5. Scot.dos 的警告 | `3b955bdf9e8d4cc93b4dc0c538d4c96cc20bbfa478969ebbc9ad5062ad875a8e` |
| `Meeting with Robot` | 15. RAM 機械人 | `85fc8a1591dc67f8c3e8a9a58ea28e27b6c122289827acc5b4df86858eceeb8e` |
| `Robot and Buck` | 25. 巴克和機械人 | `6fb58176dd190f511163c396650b1c4055502f6a00a0d8f60cd034d7201b117b` |
| `Buck's Speech.` | 27. 巴克的演講 | `52caf94b9a85ef061dbe5e698425f6e2d8d0351bd4989efabd5a7b0ff485d235` |
| `Desert Ape Pilots` | 37. 沙漠猴與航艦 | `bb32b2c0a2cb77c6a21a592a7e5106a530e39473cf076c6f43f02cf804c8c0d7` |
| `Talon's Speech` | 44. 泰隆（Talon）的講話 | `ffaf7f58606ad8a882555a378a6c1ae6f1d003272977cdc397e32f9f4da76562` |

文字處理沿用第十四階段契約：回查原圖，正規化空白、標點與明顯排印字形，不從 OCR 複製。
`Talon's Speech` 與前輪 `The Great Rift` 位於同一半頁，因此裁切雜湊相同，但兩筆文字與
事件鍵各自獨立。

## 新增段落長度

| `text_key` | Unicode 字元數 |
| --- | ---: |
| `manual.rules.damage` | 118 |
| `manual.bestiary.terrine` | 31 |
| `manual.log.5.scots_alarm` | 141 |
| `manual.log.15.meeting_with_robot` | 157 |
| `manual.log.25.robot_and_buck` | 151 |
| `manual.log.27.bucks_speech` | 141 |
| `manual.log.37.desert_ape_pilots` | 216 |
| `manual.log.44.talons_speech` | 192 |

全套 19 項既有測試、catalog lint 與真實題庫／來源／事件／文字交叉驗證通過。測試證明
資料資格與內部一致，不證明分頁、覆繪或玩家路徑完成。
