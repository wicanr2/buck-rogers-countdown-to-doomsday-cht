# 第二百二十一階段：命令／狀態列欄位與清除邊界

日期：2026-09-24
狀態：**row 15 與其餘 row 24 維持 DRAFT；既有 `roster.loading` 之合法第三頁轉場另有限縮驗收，見末節**

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

## 2026-09-24 既有載入訊息的合法轉場補證

上述「row 24 尚無可授權固定詞」是當時對**新建命令／狀態列譯文**的結論，
不能抹去已在角色名冊 catalog 中核准的 `roster.loading`。後續從本頁所列
`phase104-post-return-enter-3/control.state` 合法排程 Enter
（`300000000`），在第三頁轉場觀察到同一 21-byte 整串身分
SHA-256 `e920b38b45dd6a828b466a06f4c4c4f63645f1c6a82e488599dc3da46b5280f2`，
row 24 col 0、背景 0／前景 10、caller `0763:1307 → 0763:0424`。
原版 `START.EXE` SHA-256 為
`58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`；
`GAME.OVR` 身分見本頁輸入表。`1841:3E4E`（線性 `1C25E`）是
dosgolem 執行期字串來源，非 EXE 檔案偏移；該記憶體緩衝區會重用，
不可只憑指標辨識譯文。原版 entry `300001389`、guarded return
`300017636`；下一筆不同 caller `37F1:0337 → 0763:026B` 的
glyph entry `308525665` 後，最早相交 A000 pre-write 為 `308525782`。

沿用現有 `text/save-roster-join-runtime-events.tsv` 的 exact key 與
`text/save-roster-join-text-safe-rects.tsv` 的 `[0,168)×[192,200)`
安全矩形，**沒有新增 TSV、watcher 或 presenter**。ignored 原版探針
`command_status_literal_probe_test.go` SHA-256
`ac7f6bb779051a1e4b846da1792ab8c0c85da92be424168149aca53da2f58879`；
11 筆近似身分負例探針 `command_status_roster_identity_negative_test.go`
SHA-256 `e49d46d0bf513935ce715ecc080aaff12d389e93718a6742a5ee18bf1d72e271`。
兩者均由主代理在 Go 1.26.7 的無網路有界 Docker 獨立重跑兩次通過。

正式 CLI 與 state-compare 重生腳本
`workplace/command_status_roster_ab_probe.sh`（ignored；SHA-256
`9d4efaeea05cd05cbc23b25376d4bd7c3a2d4af0b75b6d38084d56d8940a309d`）
亦由主代理獨立執行。硬停 `308000000` 時 2×／3× 均為
`active=roster.loading`、`drew=true`；安全矩形內分別變動
1,272／2,669 像素，外部皆為零。硬停 `309000000` 時自然清層，
兩倍率 `active=null`、`drew=false`，矩形內外差異皆零。
四組 control／覆繪的事件、BIOS 鍵、記憶體、indexed、palette
SHA 均一致，state-compare 的 machine／DOS digest 亦一致。

## 2026-09-24 手冊明示前進鍵與 row 15 命令列的有界比較

低階翻譯子代理沿用本頁已核實的合法第九頁 state（SHA-256
`563ed40ba276c6857c57b05344949dec5891e4596ad783a9fc89b805eae8c2a4`）
與原版 `GAME.OVR`（本頁頂端雜湊），只比較單獨 Enter 對照及
中文手冊明示的 NumLock-8→Enter；兩組均硬停 `370000000`，
沒有猜新鍵或延長盲目探索。ignored 探針為
`workplace/phase224-row15-command-change/row15_probe_test.go`，
SHA-256 `2a22405f42ea06b3c3b0f3909d69b6445aa4c21b300e8930b5133a2e80b2684a`；
收據 `control_enter.json`、`forward8_before_enter.json` 的 SHA-256
分別為 `0a27dd954d75d91027e7380fb404f2d786cfa3025c97af6c5fbb670eaa986ead`、
`83be49cadcb8893547341cf3edd42c1799ea8015eb26f3f7a765913c6bc59e38`。
主代理在唯讀 Docker 內核對上述三份雜湊與兩組各六筆長度 12 的收據；
探針及含原始 bytes 的 JSON 均只留 ignored 工作區，沒有加入 Git。
本次子代理工具為 dosgolem fork `b908226`、Go 1.24.13、
無網路有界 Docker；位址均採本頁定義的 dosgolem 執行期實模式基準。

NumLock-8 於 step `360000165` 被 BIOS 消耗；後續 Enter 於
`361000119` 被消耗，對照 Enter 於 `361000150` 被消耗。兩側
`1FEB:2AF5 → 0763:0424`、row 15 col 17、背景／前景 0／10
各有六筆 12-byte 原文；六筆**整串** SHA、原始 bytes、長度與
字元類別逐筆相同。類別為 `DPDDSLSDDPDD`：其中只有一個孤立
ASCII 字母，沒有可辨識的固定英文詞。兩側首筆都依序經
`026F:029C` 清 row 15 col 17..38、12 格 body 首個 A000 pre-write、
dispatcher entry、受保護返回；對照步數依序為
`361111247/361111403/361111677/361121090`，前進鍵組為
`361111216/361111372/361111646/361121059`。兩側 indexed／palette
雜湊相同；memory digest 不同，但不足以證明 row 15 的玩家語意改變。

**判定：已證實／限上述兩條有界原版路徑。** 這個鍵序沒有提供可安全
新增的固定譯文，正式 TSV 保持不變，row 15 的 DRAFT 狀態與上文
「需真正改變命令／狀態的合法 state」停止線仍有效。
原始 gob/gzip state 位元組不作相等判據。此處 3× 正式 runtime
仍使用 16×16 字型縮放，不能把另外的 22 點離線候選算入驗收。

這只讓**同一個已核准的固定載入訊息**在第三頁合法轉場增列
限縮 CONFORMED 路徑。row 15 的數值／狀態欄、row 24 的
33 格直接 glyph 與其他動態身分、冷開機玩家路徑、存讀檔仍未知；
先前的 DRAFT 停止線對它們繼續有效。
