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

使用者隨後在兩張原生圖之間選定 **E1／英文字母 14px advance**，
排除 E2／16px；英文專名、括號詞界、2× 不變及 DRAFT 停止線
如上。這項視覺定案只解除字距分支，不將可丟棄原型自動升 READY
或納入正式輸出。

## 2026-09-25 獨立 READY 審查的未通過項

獨立代理核對正式 `manual_overlay_runtime.go`、`ManualSnapshotOwner`
與共用 `xlate.Layer` 後，判定 E1 **尚未 READY**：測試直接合成
終態 RGBA，未經正式雙層快照、封存、generation、原版重繪失效、
Restore／owner epoch 及換題清層。`xlate.Stamp` 的字首位置由
logical 座標乘 3，不能精確表示 14px；正式 owner 也仍硬驗
每列等於 `manualRows` 的固定 36-rune 切行，與 E1 變動寬度衝突。
因此必須先定義可封存的 3× 實體像素 run／不可變 layout plan，
或明確擴充共用層；兩種架構範圍已請使用者選擇，未替其定案。

另一確定缺口是 39 段含數字、`.`、`/`、`+/-`、百分比與中英文
標點；E1 初版 tokenizer 只合併英文字母與精確全形括號英文詞。
39 段測試目前只證「可容納」，未逐段證實 token round-trip、
非首題詞不拆、標點行首／尾禁則；14px 拉丁字模的實際 ink bbox
也未逐字檢查。2× 相等測試目前是**舊正式 renderer**對既有
`ab-1045`，不是 production 修改後的回歸。這些均須在正式
實作前補證；通過後還須首題、換題清除、返回與 2× 的新版
同狀態 A/B，不能拿此原型圖當完整玩家路徑。

使用者其後選擇將像素精度能力**擴充到 dosgolem 共用繪字引擎**，
排除只為本遊戲手冊建立專用像素層。上述驗收缺口未因架構選擇
自動消失；共用契約、封存與舊畫面相容性須另經 READY 審查。

獨立共用層設計審查提出可選的 `PixelGlyph`／`Stamp.PixelScale`／
`Stamp.PixelGlyphs`，讓原有 `Cells`／`CellW` 仍負責清除、指紋
與透明格，像素 glyph 只負責物理位置。兩份 named font
（base16 ASCII 與 derived22 CJK）都須進入封存 registry，
Snapshot／Restore 以名稱與 bytes 身分回復指標，所有 pixel crop、
座標、字模與父矩形先預檢，不能在 `Draw` 才發現局部壞輸出。
這是**候選 API**，非 READY。ignored fork 的
`xlate/pixel_glyph_draft_test.go` 只用 test-local helper 驗 14px
字首、CJK 22px、括號裁切、越界／缺字／跨倍率拒絕及 partial
`Transparent` 不漏墨；主代理在無網路 Docker 獨立雙重重跑
`TestDraftPixelGlyph*` 與 `go vet ./xlate` 通過。它沒有修改
正式 `xlate`，也未證 Snapshot／Restore、sealed group、owner
生命週期或正式 2× 遊戲畫面相容。

## 2026-09-25 全 39 段詞界補證與行界勘誤

ignored fork 的 `manual_ascii3_wordwrap_draft_test.go` 已將英數與內部
`.`、`/`、`+`、`-`、尾隨 `%` 視為不可拆識別字；短括號英文詞
不可拆，長中文引號內容允許跨行但不讓引號孤立。test-local
14px 計畫以正式 1045 字字型檢查 39／39 段的 rune round-trip、
識別字不拆及墨跡碰撞，最大 ASCII 墨跡寬 8px。收據在私有
`workplace/manual-recheck-20260925-XXfChfDp/ascii3-wordwrap-draft/manual-3x-tokenizer-line-plan-1045.json`，
SHA-256 `12a2869b24af810e27f4b9c6504e01724aff49897313e892ae604d868f27c3d7`；
該 JSON 含譯文及逐行 token，**不得加入 Git**。最初把整段
`「…」` 當成不可拆 token，於 `manual.log.11.the_elevator` 超出
864px；修正為只保護引號邊界後，39 段才通過。E1 舊定向
A/B 再以私有原版輸入重跑，2× 舊正式輸出逐位元同值，3×
原型安全矩形外零差；此處並非新版 production 驗收。

主代理獨立讀取 39 段收據，發現 **3 行以 `space` token 開頭、
11 行以 `space` token 結尾**；例如
`manual.log.57.acidic_victory` 的第 1 行。獨立審查另指出
正式 catalog 含 `……`，初版 terminal 禁行首集合未含 `…`。
因此「39／39 round-trip」只能證明字元未遺失，**不能**
證明版面行界可讀，也不能作為共用 PixelGlyph 的 READY
輸入。下一版 DRAFT 必須將 ASCII 空白定義為 soft separator，
換行時不形成可見行首／行尾空白，同時在來源 span／round-trip
收據明示還原該空白；原始首尾／連續空白、孤立 terminal 與
跨 run 墨跡碰撞需 fail-closed。這是本輪新增的技術勘誤，
不推翻先前 E1 相對 E2 的 14px 視覺選擇。

後續 test-local 版把折行處的 ASCII 空白保留為 **zero-width soft
separator**：來源 token 與 rune round-trip 不丟字，但不產生可見的
行首／行尾空格；原始首尾／連續空白仍 fail-closed。另補
`…` 禁行首及跨 ASCII run 墨跡碰撞斷言。新的私有收據
`workplace/manual-recheck-20260925-XXfChfDp/ascii3-wordwrap-draft/manual-3x-tokenizer-line-plan-soft-separator-1045.json`
SHA-256 為 `e809f87dfd539378af998ab9f70c9a456ee0c7bfc61ddf941267c8a563773916`；
主代理獨立解析，39／39 段、原 3 個行首及 11 個行尾 space token
均仍在來源序列，但這 14 個邊界 token 的寬度全為 0，最大
ASCII 墨跡 8px。先前的 3／11 可見空白結論至此**已訂正**，
保留上段作問題發現歷程。此收據及測試依然只是 DRAFT，
未證正式 owner 的快照／還原或正常玩家路徑。

共用像素精度分支另在 ignored dosgolem fork 新增並索引
`docs/spec/234-xlate-physical-pixel-glyph-plan.md`。獨立審查
先指出舊 `Draw(... ) bool` 無錯誤通道、JSON 不能回查原始指標、
canonical hash 必須固定欄位；規格已依回饋固定八欄
`PixelGlyph`、全層 checked preflight、1:1 crop、SHA-256
編碼與 source／Restore 各自的字型身分判準，升為
**READY（僅共用 API 契約）**。`xlate` production 尚待實作；
Buck 手冊 layout、owner 與同狀態收據仍是獨立 DRAFT 閘門。

共用層的第一段 production 隨後在 ignored fork 本機提交
`8f56d0e`（`xlate/font.go`、`xlate/layer.go`、
`xlate/pixel_glyph_test.go`）：可選 `PixelGlyph`、
`ValidatePixelGlyphPlan`／`DrawChecked` 全層預檢、1:1 crop、
逐像素透明格、legacy `Draw` 遇 physical stamp 零寫入、
optional Snapshot JSON、canonical 字型 SHA-256 與原子 Restore。
獨立審查曾指出字型 `(W+7)`／`H*rowBytes` 溢位及 parent
矩形未限制在畫布內兩項 P1；規格 234 已追加勘誤，程式
與零寫負例亦已修正。正式測試另驗多筆 Restore 第二筆
壞 crop／同名異 bytes、舊 2× Snapshot JSON／RGBA bytes、
字型 map 插入順序與跨倍率拒絕。主代理在無網路 Docker
獨立執行 `go test ./xlate -count=2 && go vet ./xlate` 通過。
這只證共用核心第一段；尚無封存群組、手冊 owner 的
immutable 3× E1 plan、正式首題／換題／返回同狀態收據，
不宣稱規格 234 或 Issue #21 完成。

## 2026-09-25：新版 owner 的首題 E1 局部同狀態收據

上述停止線已有**首題範圍**的新證據，並非整條玩家路徑完成。本機
未推送的 dosgolem fork `c39f72a` 建立正式 E1 plan，`5fcc1d6`
將它接入 3× `ManualSnapshotOwner`；2× 維持原路徑。以既有私有
`workplace/manual-recheck-20260925-XXfChfDp/ab-1045/` 的首題
原版 checkpoint、現行私有翻譯及倚天字型，在無網路 Docker 以
`go test -race ./apps/buckrogers -run '^TestManualSnapshotOwnerOriginalFirstQuestionOracle$' -count=1 -v`
重生原文／中文 owner 投影。測試入口與 A/B 原始檔留在被忽略的
本機工作區；**不得**把原版、譯文、字型或完整收據加入 Git。

- 2× RGBA SHA-256 為
  `1b075d714040d04736cb4c36693ededdb336a0a421bf154c86b722defe97e07e`，
  與既有首題 2× 收據逐位元相同；3× E1 RGBA SHA-256 為
  `6201a394f78608f919dcc74c41ba3a0c0d5a0eaa914a7edc43d20d17f143d49f`。
  3× 歷史固定字格圖不是 E1 的相等目標。
- 原版 indexed framebuffer、palette、記憶體的 control／2×／3×
  收據相同；中文 RGBA 差異只在已核准的邏輯矩形
  `[7,312)×[72,184)`，2× 改變 5,148 像素、3× 改變
  9,108 像素，矩形外皆為零。這些數字不表示每一個墨跡像素
  都已經過人工閱讀驗收。
- 投影前後及 control 相比，專案 `cmd/state-compare` 的正規化
  machine SHA-256 均為
  `0753f1477689b2a78c3df3d19491308186a511d1cc3b0ffaaa939b13cd3694dd`，
  DOS SHA-256 均為
  `8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。
  原始 `.state` 位元組曾有差異；該格式以 gzip／gob 保存含 map
  的資料，位元組順序不是語意相等的判準。保留這次勘誤，後續
  使用正規化比較，不把原始 `cmp` 差異誤報成遊戲狀態改變。

此收據只支持**首題終態**的新版 owner 投影及 2× 不變性；答錯換題、
成功返回、正式 Linux session 與其餘手冊題目仍待新版 E1 同狀態
驗證。規格 005 的 E1 分支仍是 READY，不升 CONFORMED；
[Issue #21](https://github.com/wicanr2/buck-rogers-countdown-to-doomsday-cht/issues/21)
維持 OPEN。

## 2026-09-25：答錯換題與答對返回的新版 E1 同狀態補證

沿用既有私有 `workplace/phase156-manual-runtime-matrix-v4/` 的兩條
合法原版輸入序列，測試入口為本機被忽略的
`TestManualSnapshotOwnerOriginalLifecycleOracle`。`target-002`
以錯答 `x` 加 Enter 換題；`return-clear` 以 `to` 加 Enter
答對返回。原版收據的輸入排程、終點步數、presentation 事件、
indexed framebuffer、palette 與記憶體摘要，在 control／2×／3×
之間一致。新版 owner 只從**現行正式 catalog** 建立待顯示文字；
舊收據的首題譯文字數為 73、現行為 99，因此舊 3× 固定字格
RGBA 不是新版 E1 的相等判準。

主代理以無網路 Docker 獨立重跑
`go test -race ./apps/buckrogers -run '^TestManualSnapshotOwnerOriginalLifecycleOracle$' -count=1 -v`
通過；本機完整私有收據保存在
`workplace/manual-owner-e1-20260925/{target-002,return-clear}/`，
不得加入 Git。量測如下，矩形仍為 `[7,312)×[72,184)`：

| 情境 | 倍率 | owner RGBA SHA-256 | 矩形內差異像素 | 矩形外 |
| --- | --- | --- | ---: | ---: |
| 錯答換題 | 2× | `d4f2af6b4242cd522bac1c4a2de61a7edec179c2c848347ab17bade53146a1c6` | 8,971 | 0 |
| 錯答換題 | 3× E1 | `81772069e584de53ea195209dfc1feed60a96eeec6c59fbea0d7ae659087cd40` | 17,248 | 0 |
| 答對返回 | 2× | `edbbe358864dfca403cb6c0978a44b8c54c86b773781754b4bf2edd7f5b5db9d` | 0 | 0 |
| 答對返回 | 3× E1 | `7a101b0f1aa301d5e684b9b9bd3cca2d2e4024294208c45ec68e0f6841bb6544` | 0 | 0 |

換題後舊 ticket 失效，3× 新題具有效 E1 physical plan；
答對返回後舊 ticket 失效、沒有 E1 plan、`PrepareFrame`
拒絕為不可見 group 建立新 ticket，正式 overlay 與原版
baseline 完全相同。兩情境的 2× RGBA 也與各自既有收據
逐位元相同。主代理另獨立以 `cmd/state-compare -left ... -right ...`
比較每案 control 與 2×／3× owner 前後、以及 owner 前後本身，
共 12 組正規化 machine／DOS 狀態皆 `equal:true`：換題 machine
SHA-256 為
`fc19bc6391234f59ae9b122681227ca4384ca6992e8c3cdd3da90a124e16c532`，
返回 machine 為
`7dcaafdb979d749e906c78c8fb2b5226f9d50e7817157a13ec7a5f1ad485aac1`，
兩案 DOS 均為
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。

這些是既有合法 checkpoint 的**無頭局部同狀態**證據，仍不是
冷開機至返回的正式 Linux 玩家視窗，也不證明其他手冊段落逐題
執行或不同英文專名的實際玩家路徑。規格 005 的 E1 分支仍
READY；Issue #21 與 #14 保持 OPEN。

## 2026-09-25：第三題 RAM 詞界的額外合法存態

同一 phase156 原版序列另有 `target-003`：錯答兩次後，第三次
`request` 指向 `manual.log.57.acidic_victory`，現行正式譯文
含一個 `RAM`。在被忽略的本機 oracle 加入固定的九筆
begin／clear／request 事件、四筆 BIOS 鍵與三個 generation
錨點；3× 正式 E1 plan 必須把該 `RAM` 留在同一個 token／同一行，
`R→A→M` 的實體 x 前進各為 14px，不能靠畫面容納就算通過。
主代理於無網路 Docker 以唯讀原版輸入重跑 `-race` 通過。

第三題終態的 2×／3× owner RGBA SHA-256 分別為
`16e3deccbc282efef74772bc477831e4423b2f82906fbf27d732a4b5d7b3425c`／
`68d18805ac1d3587db63494cd89cfdb8dff6cece0f8dfbb3dbf1118473ef9201`；
核准矩形內分別變 6,612／12,534 像素，外部均零。原版 control、
2×、3× 的輸入排程、indexed、palette、記憶體收據一致；
`cmd/state-compare` 比較 control 與 owner 前後共六組，皆
`equal:true`，machine SHA-256
`bd80fe624434488ff993d9d76cfeb8dfd7c10cafcc9113b99f5d073dd8717c4f`，
DOS SHA-256
`8dd5789e07b42a195c0bb392cd75e489af09521151ca25b4b3fea33a6e818a59`。
私有收據存於被忽略的
`workplace/manual-owner-e1-20260925/target-003/`。

本案的舊第三題譯文 101 字、現行 104 字，所以**舊 2× RGBA
不等於現行 2× 是譯文版本差異，不能當作 E1 字距回歸**；
現行 2× owner 與同次正式 2× 繪製逐位元相同，首題與第二題
仍保有各自的 2× 歷史逐位元收據。此新增情境只覆蓋另一段
`RAM` 的實際詞界，不代表 Deimos、Stockade 或 39 段都已
逐題正常玩家重播，Issue #21 仍 OPEN。

## 2026-09-25：首題三英文專名的量產 E1 詞界斷言

第三題補證只斷言單個 `RAM` 的 14px 字首；首題 `manual.log.49.deimos_prison`
含 3× `RAM`、1× `（Deimos）`、1× 行尾 `Stockade`，此前只有顯示像素收據，
沒有量產 plan 層的三詞不斷行斷言。本機 fork 新增正式測試
`TestManualE1PlanDeimosPrisonEnglishTokens`
（`apps/buckrogers/manual_e1_english_token_test.go`，未推送 fork 遠端）：
以現行正式 catalog＋定版 1,046 字倚天字型建立首題 E1 plan，
逐一核對三詞每次出現都落在單一 sealed token 內（不斷行），
且該段全部 ASCII 字母相鄰字首皆精確 14px。

主代理在無網路 Docker（`eob-remake-go:1.26.7-ebiten2.9.9`、
`--network none`、唯讀掛載）重跑通過；`gofmt`、`go vet`、
`go test -race ./apps/buckrogers -run '^TestManualE1Plan' -count=1`
全綠。這是靜態 plan 斷言，不含原版執行期重播；
Linux 玩家視窗與其餘 38 題逐題重播仍未驗，Issue #21 仍 OPEN。
