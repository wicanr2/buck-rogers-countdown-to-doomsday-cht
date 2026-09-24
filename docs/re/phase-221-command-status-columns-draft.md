# 第二百二十一階段：命令／狀態列欄位與清除邊界

日期：2026-09-24
狀態：**DRAFT 原版觀測；沒有可授權翻譯的固定詞**

## 問題與停止線

第九頁後的合法 Enter 曾被誤看成第十頁候選；[第一百三十六階段](phase-136-story-page10-enter-stop-line.md)
已證實只有 row 15 命令／狀態列六次重畫，沒有新故事 glyph。更早的
[第一百一十階段](phase-110-command-status-inventory.md)只量到 row 24
21 格 identity，[第一百一十二階段](phase-112-command-turn-manual-evidence.md)
又量到手冊明示 4／6 的 row 24 直接繪字。本輪只在這三條**既有合法路徑**
比較原文字節的相等欄位與 A000 寫入；不延長第九頁自然離頁探針、不探索新鍵。

## 輸入、工具與位址空間

| 輸入／工具 | 固定身分 |
| --- | --- |
| 原版 `GAME.OVR`，本機 `/orig/GAME.OVR` 唯讀 | SHA-256 `3a4ad4856c08fe5973179f1d907feed1d870af99d08abd1cb884b316324f3cc0` |
| 合法第九頁 `workplace/page9-next-trace/page9-a.state` | SHA-256 `563ed40ba276c6857c57b05344949dec5891e4596ad783a9fc89b805eae8c2a4` |
| 手冊返回後 `workplace/phase104-post-return-enter-3/control.state` | SHA-256 `49d4bb0681269fca1954f3e02cb2cffe93bac48086d607dcfa5d975174750cc0` |
| dosgolem fork | commit `cc0b17ac92b1e3aea8ff676936684ddcf8064594` |
| 可丟棄 probe | ignored `workplace/dosgolem/apps/buckrogers/command_status_columns_probe_test.go`，SHA-256 `64878462674a39e53fa700294bd4da5b51504becfa1c8ff822f97e89453ae2cc` |
| 工具 | 既有 `eob-remake-go:1.26.7-ebiten2.9.9`，Go `1.26.7 linux/amd64`，無網路有界 Docker |

所有 `segment:offset` 均為 **dosgolem 執行期實模式位址**；A000 offset 是
Mode 13h 320×200 的單 byte 視訊位移，非 IDA 線性位址。probe 從原版
`0763:0424` dispatcher 或 `0763:026B` glyph 入口暫讀 bytes，只在記憶體
比較；輸出只含整串 SHA-256、欄位相等／變動遮罩、步數、writer 及矩形，
沒有原文、單字節雜湊、字模或可還原畫面。原版與完整存態均留 ignored。

第一次容器少掛既有 `/orig/GAME.OVR`，`state.Load` 在任何重播前明確失敗；
確認來源目錄後以唯讀 `/orig` 掛載原樣重跑通過。這是容器設定失誤，
不是原版或 dosgolem 行為差異。probe 的起點檢查亦由「必須早於按鍵步」
修為容許 state 與既有按鍵排程同在 `300000000`；沒有改輸入或停止點。

## 有界重播結果

| 路徑 | 排程／硬停止 | 已量原文路徑 | 同路徑欄位比較 |
| --- | --- | --- | --- |
| 第九頁後 row 15 | `361000000` Enter；`370000000` | `1FEB:2AF5 → 0763:0424`，row 15 col 17，六筆各 12 bytes；六筆完整 SHA、entry step 均逐筆等於第一百三十六階段 | 六筆的 zero-based 第 **0** 格不同；第 **1–11** 格 bytewise 相同。這只是在同一存態／時間窗觀察到的穩定後綴，不是跨遊戲狀態的固定詞證明。 |
| 早期 row 24 Enter | `300000000` Enter；`310000000` | `0763:1307 → 0763:0424`，row 24 col 0，一筆 21 bytes，SHA-256 `e920b38b45dd6a828b466a06f4c4c4f63645f1c6a82e488599dc3da46b5280f2` | 只有一筆，21 格均**無欄位固定性比較**。 |
| 早期 row 24 轉向 | `302000000` 數字鍵盤 4、`304000000` 數字鍵盤 6；`310000000` | `37F1:0337 → 0763:026B`，row 24 col 0，兩筆各 33 glyph；兩筆完整 SHA 均為 `00df727dbe5dc2fd691488463bb9a24f7b951bb3d37ac4c142b59996adf555ea` | 0–32 格在這對輸入中全同；第一百一十二階段未證實方向／座標狀態真的改變，故不能稱為跨狀態固定標籤。 |

row 15 六筆完整 SHA 依序是
`f79a55d262f6fad8b1c452dff14538a7c9d1d7fe80710a7c32a65d20d2f3e990`、
`71acf265857c8c3ed8215a92d449ed2d2f189014aef16dd9ec83d7a93f50303c`、
`fc399efbe66ecb225bed82f042f457e26c87c2f1c550c097f883e016dcd3ae0d`、
`07bafe8e810d56fb813fe77dea795c8d512ae46230bc917c57c3becbb468eecf`、
`514f6f6c20881d279579b7896f1cb3b5a74ad4396a14f2d695c49a2637310b84`、
`a833fa64677710d2b8e776137220154e2fe51ffa965ffadc361c63be3770f66c`。
這些是**整串**身分，不可拆成單字元反查表。

### 清除與 A000 先後

- **row 15，已證實於這六次重畫：**每次 `026F:029C` 在 dispatcher entry
  前 430 steps 接受 `top=bottom=15,left=17,right=38`。第一筆 clear entry
  `361111247`，本體 `[x=136,232)×[y=120,128)` 的首筆 A000 pre-write
  `361111403`、writer `0CF4:1B3A`、offset `38536`；dispatcher entry
  `361111677`。六次本體共 9,216 筆相交 pre-write，其中 `0CF4:1B3A`
  4,608 筆，繪字 `0763:184D` 4,005 筆、`0763:1854` 603 筆。
  `left..right` 是原版清除呼叫的 22 個文字格參數；9,216 只統計
  12 格原文本體，不能冒稱已量整個 22 格的逐 pixel 清除。清除範圍
  大於原文長度，未來任何覆繪都不得侵入右側未分類欄位。
- **row 24 Enter，已證實於此一路徑：**21 格本體的首筆 A000 pre-write
  `300000391`，writer `0CF4:1B3A`，早於 dispatcher entry `300001389`；
  本體共 4,032 筆，按 writer 為 clear `0CF4:1B3A` 1,344、
  `0763:184D` 2,147、`0763:1854` 541。後續可見的 `026F:029C`
  entry 在 `308551930`，只清 row 24 col 33..39；不能把這筆
  **右側**清除說成 21 格文字本體的失效事件。
- **row 24 的 4／6，已證實於此 pair：**兩筆 33 格 body 共 4,224 筆
  A000 pre-write，恰為 `2×33×64`；首筆 `302002466` 在 col 0／row 24，
  writer `0763:184D`，兩個 writer 分別 3,382／842 筆。兩筆
  `026F:029C` entry 分別在 `302028614`／`304028613`，只清
  row 24 col 33..39，**不與 0..32 本體相交**。這條路徑目前靠原版
  逐格重畫本體，沒有已量到的本體 clear 呼叫。

## 判定與下一個最小證據

已證實的是**欄位在這些重播內是否相同／不同**、caller、step、
原文整串身分和上述清除／pre-write 邊界；不是欄位的玩家語意。
row 15 第 0 格的變動原因未知；第 1–11 格是否跨狀態固定未知。
row 24 的 21 格與 33 格不共享 caller／長度，不能合併成一條譯文；
4／6 的 33 格相同也未證明不同遊戲狀態下固定。完整清層、尾碼、
存讀檔、正常 Linux 玩家入口與 2×／3× 文字安全矩形均未驗。

下一步只需取得**已有玩家證據支持的另一個合法且確實改變命令／狀態的
state**，與上述 identity 在同 caller／row／column 下私下逐格比對；
再量變動欄的來源、固定欄的原文詞界、每條路徑最早相交 pre-write／
Stop／Restore 及安全矩形。若無此可比狀態，就維持 DRAFT；不把
「目前相同」冒稱固定繁中詞，不新增翻譯 TSV 或 production watcher。

## 重生界線

在既有 image 的無網路、`--rm`、限記憶體／CPU／PID Docker 內，唯讀掛
專案與本機原版目錄至 `/project`、`/orig`，以使用者 UID/GID 執行：

```text
COMMAND_STATUS_PROBE_CASE=row15
COMMAND_STATUS_PROBE_STATE=/project/workplace/page9-next-trace/page9-a.state
go test ./apps/buckrogers -run '^TestCommandStatusColumnsProbe$' -count=1 -v

COMMAND_STATUS_PROBE_CASE=row24_enter 或 row24_turn
COMMAND_STATUS_PROBE_STATE=/project/workplace/phase104-post-return-enter-3/control.state
go test ./apps/buckrogers -run '^TestCommandStatusColumnsProbe$' -count=1 -v
```

`row15`、`row24_enter`、`row24_turn` 的硬停止分別固定為
`370000000`、`310000000`、`310000000`；不得為找第九頁出口而延長。
完整原版、存態與 probe 保持 ignored／私有；本文件只記 content-safe 摘要。

## 2026-09-24 跨進度合法初態比對勘誤

本節追加獨立於上段三條短窗的**第二初態**，不覆寫原先「當時沒有跨狀態
證據」的歷史結論。從手冊正確作答前的合法
`workplace/probe/phase12-before-question.state`（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）
載入本機私有成功返回收據
`workplace/phase104-manual-correct-return/control.json`（SHA-256
`777f73b28c41ce7e62775eaaa81c92af4e474720e3f264b4ab723e83c8549ac1`）
內的三筆**既有** BIOS 排程，止於 `280000000`；答案不輸出、不加入 Git。
另一側仍使用上述第九頁合法 state，既有 `361000000` Enter，硬停止
`370000000`。兩個初態與輸入都來自已驗玩家路徑；它們證實故事進度與
row 15 輸出內容不同，但尚未證實「命令選項」或具名狀態變數改變。

dosgolem fork commit 仍是 `cc0b17ac92b1e3aea8ff676936684ddcf8064594`，
原版 `GAME.OVR` SHA-256 仍是本頁頂端所列值。ignored 一次性
`command_status_cross_state_probe_test.go` SHA-256 為
`e532cd6c1f5a82790e81652c6832fd2312bfdd82f4e14d7e70ac49ba513294b7`。
在既有 `eob-remake-go:1.26.7-ebiten2.9.9`、Go `1.26.7 linux/amd64` 的
唯讀無網路有界 Docker 內，執行
`go test ./apps/buckrogers -run '^TestCommandStatusCrossStateProbe$' -count=2 -v`
兩次均通過，entry／整串 SHA、欄位遮罩及 A000 首寫一致。最初一次性 probe
錯把 `row`／`col` 的 byte 參數當完整 word，比對不到 entry；修正探針的
型別截取後，以**相同** state／輸入／停止點重跑通過，非遊戲或 dosgolem 缺陷。

| 已證實 row 15 col 17、caller `1FEB:2AF5` | 原文整串身分與邊界 |
| --- | --- |
| 早期第一筆 | `267092572`，11 bytes，SHA-256 `341424568dde6246402816f2c2007d9a24f4fc1a7b22ab48f7a13177003932cd`；`026F:029C` 清 row 15 col 17..38 於 `267092142`，首筆相交 A000 pre-write `267092298`，writer `0CF4:1B3A`，offset `38536`，entry 前本體清寫 768 筆。 |
| 早期第二筆 | `268564251`，12 bytes，SHA-256 `2a44b824ee9c300be7e30d80e5af1178fd654de6509bd82db39acb955185db51`；清除 `268563821`，首寫 `268563977`，同 writer／offset、768 筆。 |
| 第九頁後六筆 | 12 bytes；六個完整 SHA 與 entry 均與本頁上段及第一百三十六階段一致。每筆 `026F:029C` 清 row 15 col 17..38 後，恰有 768 筆本體清寫，再進 dispatcher；首筆清除／A000／entry 為 `361111247`／`361111403`／`361111677`。 |

此處 768 筆只統計固定的 row 15 col 17..28 **12 格觀測矩形**在
dispatcher 前的 A000 寫入；早期第一筆原文實長 11 格，不可把第 12 格
說成該筆原文 glyph，也不能把 768 當成完整 22 格 clear 的逐 pixel 計數。

早期 12 格對後期六筆 12 格，zero-based 位置 **1–4、6–11
逐 byte 相同**；位置 **5** 必不同，位置 **0** 對後期第 2–6 筆也不同
（對第 1 筆恰相同）。早期 11 格若右對齊到 12 格，早期位置
2、3、5–10 相同，0、1、4 不同。這只是字節相等遮罩；右對齊是比較方式，
不是原版欄位格式或語意證明。12 格的 ASCII 類別形狀為
`DPDDSLSDDPDD`，11 格為 `DPDSLSDDPDD`，其中 D 是 ASCII 數字、
S 是空白、P 是非 ASCII 英文字母／數字／空白的其他 byte；**沒有
ASCII 英文字母**。P 不推定為特定符號或詞。即使有逐 byte 不變位置，
本輪仍找不到可審核的固定英文詞與動態欄來源，故不能產生譯文 key。

另以已存的 96 份 phase104–139／page6–10 相關 JSON 候選篩查，93 份
可解析為物件、1 份解析錯誤；此統計包含不同格式的收據，不代表
93 條獨立玩家路徑。目標 row 24 的 `0763:1307 → 0763:0424` 21 格
只見 `e920b38b…` 同一整串身分；`37F1:0337 → 0763:026B` 33 格
只見 `00df727d…` 同一整串身分。page6→9 換頁、phase110 只改 Enter
時間，以及 phase112 的 4／6 都**不是**不同的 row 24 命令／狀態值。
因此 row 24 仍缺「同 caller／row／col，且來源可證的不同值」；
row 15 則雖有跨進度不同內容，仍缺可核准翻譯的固定詞與失效驗收。
不延長第九頁盲目按鍵，不新增 TSV 或正式覆繪。
