# 第一百零五階段：手冊成功返回後首個劇情畫面追蹤

日期：2026-09-22
狀態：**DRAFT；已取得固定英文 identity，並建立 DRAFT 候選 catalog 與失效候選；尚未完成 READY 審查。**

## 目的與範圍

本階段只追查 phase104 手冊正確作答後，原版進入遊戲的第一個玩家可見畫面。
不記錄手冊答案、按鍵序列、原版全文或可還原素材；不修改原版輸入，也不把未
READY 的試作接入 production。

## 已重生證據

- 正常路徑：`phase104-manual-correct-return/2x.json`，手冊成功返回後第一個
  後續畫面事件從 dosgolem 絕對步 `267025068` 開始。
- 同畫面基準：`phase104-manual-correct-return/2x.baseline.png`，640×400，SHA-256
  `df56e111cba1f223ad5fde2dc28d8197759c1ae6871a9f8fcb9a081cb9f713da`。
- 既有畫面可見一段固定劇情敘述；右側角色姓名與底部狀態列屬動態欄位，不能
  當作固定翻譯 key。
- 當時的 baseline receipt 只列出姓名、狀態與 Loading 等高階事件；在該份 receipt
  中，劇情敘述沒有對應的 `segment:offset`、原文字串 hash、長度或 guarded post-call。

### 繁中術語證據與 DRAFT 候選

`text/story-opening-events.tsv` 與 `text/story-opening.zh-TW.tsv` 現在保存五筆
**DRAFT 候選**，不是 READY catalog，也尚未被 runtime 使用。譯文只採用本機中文手冊
掃描的術語，不納入原版英文全文：

- `SCAN0352_003.jpg`（印刷頁 1–2；SHA-256
  `211ac35f9742479911b2800a04bed58fde9f227574870d05baca14bd7ecfbd88`）明列「美蘇貿易聯邦（RUSSO-AMERICAN
  MERCANTILE, RAM）」及「巴克羅吉斯（BUCK ROGERS）」；因此第五行使用
  「美蘇貿易聯邦（RAM）」、第一行使用「巴克羅吉斯」。
- `SCAN0352_004.jpg`（印刷頁 3；SHA-256
  `08b8504eb4b9adffb0f8b165b157d893040d86b06b121d09977eda531c7c5a6c`）明列「新地球組織（NEW EARTH
  ORGANIZATION, NEO）」；因此第二行使用「新地球組織」。
- 五行其餘語句是依已確認畫面行序所作的繁中 DRAFT 意譯；在 runtime A/B、字型涵蓋、
  39 格安全矩形與失效生命週期完成前，不升級為正式可繪製資料。現有 validator 以
  全形／寬字元 2 格、其他字元 1 格的保守 ETen advance 近似檢查 39 格；這不是 runtime
  renderer 的實測結果，READY 前仍須由實際繪製器驗證。

以目前 12 份 `text/*.zh-TW.tsv`（包含上述五行 DRAFT）在 Docker 內重建 ETen 候選字型，
builder 回報 `GOLEMFNT` 16×16、971 個 glyph，且沒有缺字；候選檔只留在被忽略的
`workplace/phase105-font/`，不進 Git。輸出 SHA-256 為
`188efde53305631f30232ec2177445b3f2c5531613a079f3e254b260a3b8504d`，這只是 DRAFT
涵蓋證據，不代表 runtime 字型已接通或可公開散布。

## 勘誤（2026-09-22）

先前誤把 row `15`／column `17` 的 `1FEB:2AF5` dispatcher 事件分類為劇情。後續對照
baseline 證實它屬上方面板狀態資訊；該 identity **不得**用於劇情 TSV 或 runtime hook。
本階段改以底部綠字 row `17–22`、column 約 `1` 的低階 glyph run 為唯一目標。原有錯誤
定位與其收據保留，僅作勘誤可追溯性。

## 已重生的只讀追蹤

以 `workplace/probe/phase12-before-question.state`（SHA-256
`8cbc27f568057fbf3ce2f91d407953ec94836f2b723f50b7b73e56100e859269`）重播既有的私有
phase104 合法作答排程至步數 `268000000`，連續執行兩次。兩份 content-safe 收據逐 byte
相等，SHA-256 皆為
`1e5ce43a368eecc17b2c4e513ba20ff9e76698991add9f7c4a983079f87445c2`；它們只留在被忽略的
`workplace/phase105-first-story-trace/{run-a,run-b}.json`。

- 上方面板 row `15` 的 dispatcher 事件已排除；它不代表底部劇情。
- 真正底部綠字不是 `0763:0424` 字串 dispatcher，而是 guarded `0763:026B` 的逐 glyph
  路徑。其每 glyph 的 caller／return 為 `0763:04FF`；診斷以「同 caller、mode、repeat、色號、
  row，且 column 連續」聚合，bytes 僅在程序內計算 SHA-256 後丟棄。兩次收據逐 byte 相等，
  `glyph_drops=0`，且 baseline 目視為五行，與下表 rows `17–21` 一致。

| row/column | entry → guarded post-call | 原文長度／SHA-256 | bg/fg |
| --- | --- | --- | --- |
| 17/1 | 268686427 → 270263541 | 37 / `a989ceac7d0b25ad1a02fca8d158c5c47ab25aa28faa329f99016bcbd22d89d2` | 0/10 |
| 18/1 | 270307529 → 271928281 | 38 / `177bcfea0dd3bdba2390155791c7c48097736031d03e90eff9c1e594e7d24dc5` | 0/10 |
| 19/1 | 271971771 → 273373887 | 33 / `c6a67dbd38752114fcf6761f59a57ed0970d0c75ac63696466c8f99d658a963b` | 0/10 |
| 20/1 | 273417761 → 274644543 | 29 / `a0cb29721abfb85c6062169ef8d5c8a0d4e794570a007b472fc3f2c655dcd182` | 0/10 |
| 21/1 | 274689101 → 275652511 | 23 / `f686b3355b648d95981ec5c128fc4e07f0950c983e9543c49a258fbcd1ea5d74` | 0/10 |

### Enter 換頁的清除反證

從 `phase104-manual-correct-return/control.state`（步數 `280000000`）在 `281000000` 送入正常
BIOS Enter，至 `290000000` 兩次重播的收據逐 byte 相等。唯一的 `026F:029C` 呼叫是步數
`287316299`、矩形 `left=33, top=24, right=39, bottom=24`；它是底部狀態列，與劇情 stamp
矩形 `column 1..38 × rows 17..21` 交集為空。既有
`phase104-post-return-enter-2` 的 2×／3× 收據同樣記錄此 clear，且手冊 overlay `active_keys=[]`、
`drew=false`，只能證明手冊覆繪已失效，不能外推劇情覆繪生命週期。

因此不可把 `026F:029C` 寫成劇情清除契約；下一節量測頁面內容重繪的第一個可觀測入口。

### 實際頁面重繪入口（已確認）

以同一首頁 state 在步數 `281000000` 送入一次 BIOS Enter，對 logical rows `17–21`
（indexed framebuffer y=`136..175`）逐指令比較。兩次 content-safe 收據逐 byte 相等；第一筆
劇情區改寫是 step `281020572` 的 `0CF4:1B3A`，差異 bounding box 為 x=`10..294`、y=`137..137`。
它是下一頁重繪的首條掃描線，並非 row `24` 狀態列 clear。診斷只輸出 step、callsite 與差異矩形，
不保存原版像素。

後續有界追蹤在該指令執行前量到 `ES:DI=0xA000:0xAB48`、`CX=304`；
線性視訊偏移 `43848 = 137×320+8`，因此此筆 byte-fill 的目的範圍為
logical row `137`、x=`8..311`，確實與首屏劇情區相交。這給出可在寫入前
以目的 span 相交判定失效的具體例子，不需要在每個指令後掃描整塊劇情區；
它仍不是所有換頁的通用位址規則，其他寫入路徑須保守失效或另行追證。

因此 READY 的失效候選可精確表述為：當 output observer 看見 `0CF4:1B3A` 的此轉場，或看到其第一筆
story-region framebuffer 改寫時，先使目前 story overlay 失效，再容許原版下一頁重繪。這仍是 DRAFT：
需以 runtime A/B 證明在該邊界前失效不殘字，才可 CONFORMED。
- dispatcher 下游的全部 178 個 glyph 呼叫皆經 `0763:049B`（mode `1`、repeat `1`）；診斷
  沒有保存 glyph bytes，兩次均 `glyph_drops=0`。這是 dispatcher ABI 的下游畫字，並非另一個
  可獨立攔截的故事文字路徑。
- 右側資訊網格是 `37F1:*`、row `2` 與 `4–9`、column `17/34/37`；底部狀態列在 row `24`。
  它們含角色姓名／數值等動態欄位，已從固定敘事 identity 排除。

診斷命令的二進位 SHA-256 為
`5a696c1bf727dc02fc1187964d2f9b38a364e367d741e8c8044422c483b7c883`。它新增的
`--clear-trace`／`--glyph-trace` 僅輸出 metadata，未安裝 runtime hook、未改寫 VRAM、原版或輸入。

## 從 DRAFT 到 READY 的精確缺口

RE identity 與正常路徑重播已充分；尚不能越級接 runtime。READY 規格必須先明定：

1. 五個 content-safe event key，精確綁定上述 glyph-run caller、長度、hash、row、column與色號；
2. 該五列的合法繁中 TSV、字型覆蓋、各行 39 格安全矩形與明確 overflow 策略；
3. 將 `0CF4:1B3A`／第一筆 story-region write 定義為轉場失效邊界，並以 runtime A/B 驗證下一頁
   與返回時無殘字；不得誤用 `026F:029C` 狀態列 clear；
4. 同 state 原文／覆繪 A/B 只差核准矩形像素，且右側動態欄與底部狀態列保持不變。

目前的 TSV 僅是可審查的 DRAFT 候選，並由 `tools/story_opening_catalog.py` 做
失敗即關閉的結構／identity／容量檢查；它不代表 READY，也不會被 production dispatcher
讀取。READY 前仍不得建立 production hook 或宣稱已中文化；私有收據中的合法輸入排程與
原文均不得進入版本控制。
