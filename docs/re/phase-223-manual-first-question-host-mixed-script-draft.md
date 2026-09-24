# 第二百二十三階段：手冊首題實體視窗與中英混排 DRAFT

狀態：**DRAFT 視覺及接線原型**。本階段沒有修改正式譯文、字型、
手冊 presenter 或 Linux session；不代表冷開機直播、39 題逐題、
換題、存讀檔或玩家可用前端已驗收。

## 輸入與實驗邊界

- 首題原版終態 `control.state` SHA-256
  `2cdb2065a22591fb2909272611b66ee5f84fb211e30c9fe5c2769421f3b5ee22`；
  原版 `START.EXE` SHA-256
  `58a34a38b1db455202d2d30daa82915982d7d905932b46bdc7371cb466226cf1`。
  原版與已購倚天字型只在本機 ignored `workplace/`，唯讀掛載。
- 正式 `text/manual.zh-TW.tsv` 的首題 `manual.log.49.deimos_prison`
  目前為 73 字元，保留 `RAM`、`Deimos`、`Stockade` 的拉丁字母；
  對應原版手冊位置與 identity 仍依[規格 005](../spec/005-manual-runtime-presenter-draft.md)。
- 測試程式為 ignored
  `workplace/cold-boot-live-turn-proto/manual_owner_window_draft_test.go`
  SHA-256 `8e06dab9985b9a83d91273a38dc5f91835ba0a0c5898a16fc56091725145412a`，
  以及 ignored `workplace/dosgolem/apps/buckrogers/manual_ascii3_typography_draft_test.go`
  SHA-256 `6b92cbfad35f1e0b0dcc204a8a6b8e7b29f3b1c2c0a1c7ecb6cf1970468e7042`。
  工具是 dosgolem fork `cbd5683`、Go 1.26.7、Ebitengine 2.9.9，
  有界無網路 Docker／Xvfb。PNG 僅存 ignored `workplace/`，不入 Git。

## 真實視窗的限縮正收據

從已核實的 step 266557247 原版終態及 formal begin→clear→request
presentation queue，建立兩份正式 `ManualSnapshotOwner`，分別以 2×、3×
對同一個 indexed／palette 影格投影。正式 `frontend/ebiten.Game` 接收實體
X11 設定→暫選 3×→Apply；2×／3× 分別產生 39／15 次 snapshot，
每一張均逐 byte 等於既有正式原版收據的同倍率 RGBA。測試期間
`Machine.Steps` 保持 266557247、原版 indexed 全畫面不變。
私有視窗圖 `manual-first-question-3x-host.png` SHA-256
`5130bbfd4104583ecc52ef3ebf1c748db0084565ba54e4ae64315501a08047fa`。

這份測試的 `Advance` 故意是 no-op，只驗「已量原版終態→正式手冊
owner→實體 host 畫面」；不是從 cold boot 走到首題的直播 session。
字型與譯文只用於顯示，沒有進答案或 DOS 記憶體。

## 視覺觀測與 A／B／C／D 原型

實體圖初看像有英文殘字；核對 formal TSV 與原版清除 layer 後，
那些字母其實就是譯文內的 `RAM`、`Deimos`、`Stockade`。因此
**「原版英文未清掉」已被推翻**，不可把它當成清層故障。
真正問題是每個半形拉丁字母在 3× 仍佔 24px cell，詞被拉長，
`Deimos` 的括號還碰到固定 36-rune 行界。這是玩家可見的混排品質問題。

用同一首題、同一原版終態建立下列本機圖；正式程式與 TSV 均未變：

| 版 | 私有 PNG | 僅供判讀的改動 |
| --- | --- | --- |
| A | `manual-3x-A-current-ascii16.png` | 正式 3×：拉丁字模 16 點、字格 24px。 |
| B | `manual-3x-B-derived-ascii22.png` | 拉丁字模也最近鄰放大到 22 點，字格不變；A/B 差 865 像素，核准手冊正文矩形外零差。 |
| C | `manual-3x-C-chinese-names-mockup.png` | 只在測試記憶體把首題英文專名改為繁中排版示意，62 字元；**不是核定譯名**，未寫正式 catalog。 |
| D | `manual-3x-D-compact-latin-mockup.png` | 保留原譯文，單詞內試 18px 拉丁 advance；固定 row-major 分行及單詞後空白仍未解。 |

A／B 的 RGBA SHA-256 分別為
`c6e87ba6267ae12f99f7110c02328e0844c32946e7ad8a77cae70a6bb712206e`／
`96be22db1c850f6850e976c1104153a039f7cdfb5a37e95e98e08d3a28cc7e69`；
C／D 分別為
`97f4f2cd397d5c4d7e763bef120e1a651f7135dbb5191c624c98ac1d12ef17e3`／
`5aa777e6f99aa423651bb04ad741a1a71fab7cac8238f28a1e6d62bc79bfe338`。
這些都是同一原版影格上的測試繪製，不能將 C 的縮寫文字或 D 的
像素後處理直接搬入 production。後續是產品取捨：保留中文手冊的
英文專名並設計混排／詞界，或逐項核定繁中專名；已請使用者選擇，
決定前不改正式手冊段落。

PC-98／金盒繁中版面參考只支持將字模尺寸、字格 advance、行高分開
測量；原版行為及畫面仍以《拯救地球》DOS/dosgolem 為準。

## 2026-09-24 首題 request 前後的同狀態邊界

Terra 子代理從合法本機 checkpoint
`phase12-before-question.state`（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）
分別在首題 request 前 `266557245` 與 request 後 `266557247`
停止；沒有注入答案或繞過原版驗證。後一停點的 ignored 收據
`workplace/manual-runtime-slice-20260924-rerun/verification.json`
SHA-256
`dfde90860736fe46ee309f6e9098ca06a1ec49f78c79cd9b27bba0ece8bc0d36`。
原版事件依序為 begin `266486493`、clear `266524821`、request
`266557246`，request 身分為
`manual.page34.deimos_prison.word10`／`manual.log.49.deimos_prison`。
在 request 後同一原版 state 的 2×／3× control A/B 中，正文
安全矩形內各有 3,776／6,591 個像素差，矩形外均零；兩側
machine／DOS 雜湊同值，檔案操作及寫入計數均零。此為從合法
checkpoint 至首題的正常原版續行，**不是從冷開機到首題的完整
玩家路徑**。

為檢查「尚未要求手冊時不顯示正文」，子代理使用**獨立 ignored
DRAFT clone** 的 `-draft-allow-manual-pending-terminal`，僅容許
同一 generation 已有 begin、clear 而 request／action／active key
皆零的停點輸出空覆繪收據。正式 CLI 未變，且不用該旗標時仍以
`pending=true` 拒絕。它拒絕的原因是通用文字 recorder 在最後
glyph dispatcher 的 guarded post-call 前仍 pending，並非手冊
presenter 已建立中文 action。clone `main.go` SHA-256
`4805d4c26c12724ba315608f51b59524cdc33a405312eab14ca00e35fb6710ca`。
前停點 2×／3× JSON 收據 SHA-256 分別為
`dbabea46f5eeafbeeaab85fa32eabc43013d33775e7d8528684063fefd6da90b`／
`bd617258295e52416c47e029e73e6b43dc82b2c76de088c5dea3b55261baf5f5`；
兩倍率均 `actions=[]`、`active_keys=[]`、`drew=false`，baseline
與覆繪 RGBA 同雜湊，正文內外差異皆零；control 與覆繪
machine／DOS 雜湊均相同。

**證據等級：已證實／僅上述合法 checkpoint 與 DRAFT 收據工具。**
這補的是首題顯示開關的雙側同狀態驗證；正式 pending-terminal
收據契約、直播 Linux session、39 題逐題與存讀檔仍未完成。

## 2026-09-25 保留英文專名的變動字距 E1／E2 原型

使用者已選擇保留中文印刷手冊中的 RAM、Deimos、Stockade，
改善 3× 混排及英文詞界；上節 C 的新造全中文名稱不獲採用。
舊 A／B／C／D 收據對應當時的譯文與字型，不能冒作現行原型。
從現行 1,045 字本機倚天子集及首題新收據
`workplace/manual-recheck-20260925-XXfChfDp/ab-1045/`，在 ignored
dosgolem fork 建立 `manual_ascii3_wordwrap_draft_test.go` 可丟棄原型。
初版 D 只把英文墨跡縮在原來每字 24px 的位置內，主代理於原生
960×600 圖檢視後確認單詞後仍有固定格洞，故沒有把它當正式方案。

第二版改成整行共同游標：CJK 每字前進 24px、空格 8px，
`（`／`）` 依現行字模墨跡分別前進 10／11px；連續英文及
`（Deimos）` 類括號專名是不可拆 token，後續中文字由 token
實際終點續排。英文單字 advance 各產生兩個候選：E1 14px，
E2 16px。兩者皆不改正式 TSV、原版 state、字型來源或 2×
renderer，且均沿用既有手冊安全矩形。這些數值是**原型參數**，
尚待使用者根據並列圖選定，不是 READY 規格。

| 候選 | 私有原生 3× 圖 | 對現行正式 RGBA 的差異 |
| --- | --- | ---: |
| E1／14px | `workplace/manual-recheck-20260925-XXfChfDp/ascii3-wordwrap-draft/manual-3x-e1-14px-variable-1045.png` | 13,250 pixels |
| E2／16px | `workplace/manual-recheck-20260925-XXfChfDp/ascii3-wordwrap-draft/manual-3x-e2-16px-variable-1045.png` | 13,094 pixels |

兩者對首題的核准 clear rectangle 外差異均為 0；RAM、Deimos、
Stockade 都各自完整落在單一行。DRAFT 測試另檢查全部 39 段
在兩候選的 36 欄×14 行等價安全幅內可容納、2× 正式 RGBA
與 `ab-1045` 逐位元相同，並以 37 格英文詞、505 字正文及
35 個中文字後接 `RAM` 驗證超長拒絕或整詞換行。主代理在
無網路有界 Docker 獨立重跑四個定向測試及
`go vet ./apps/buckrogers`，均通過；完整 token／行像素收據與圖
只在 ignored 私有目錄，不進 Git。

**停止線：**E1／E2 只有 test-local compositor 的首題圖與靜態
39 段容量，尚未改 `manualRows`、正式 `RuntimeManualOverlay` 或
`ManualSnapshotOwner`，沒有新的 production 同狀態 A/B、換題
清除、正式 Linux 視窗或 39 題逐題正常玩家驗收。
[Issue #21](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/21)
保持 OPEN，待字距選擇、獨立 READY 審查與正式實作。
